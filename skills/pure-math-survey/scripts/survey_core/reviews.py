"""Evidence binds actual bytes and an explicit scope; records are human assertions."""
from __future__ import annotations
from pathlib import Path
import re
from .common import VERSION, all_files, diagnostic, file_hash, read_json, require, relative, safe, valid_date
from .models import fields
from .dependencies import required_closure

def load_review(path: Path) -> dict:
    obj = read_json(path)
    fields(obj, {'review_id':str,'kind':str,'reviewer_mode':str,'inputs':list,'findings':list,'unchecked_items':list,'disposition':str}, path.name)
    if 'schema_version' in obj:
        require(obj['schema_version'] in (VERSION, '2.1.0', '2.2.0'),'SCHEMA_UNSUPPORTED','Unsupported review schema',path.name)
    require(isinstance(obj.get('scope',{}),dict),'REVIEW_INVALID','Review scope must be an object',path.name)
    if 'editorial_policy' in obj.get('scope', {}):
        from .profiles import supported_contract
        require(obj.get('schema_version') in ('2.1.0','2.2.0') and supported_contract(obj.get('schema_version'),obj['scope']['editorial_policy']),
                'SCHEMA_UNSUPPORTED','Review schema and policy must match exactly',path.name)
    else:
        require(obj.get('schema_version', VERSION) == VERSION, 'SCHEMA_UNSUPPORTED', 'New review schemas require their explicit policy', path.name)
    from .profiles import POLICY, R3_READINGS
    mode_findings = obj.get('scope', {}).get('mode_findings', {})
    require(isinstance(mode_findings, dict), 'REVIEW_INVALID', 'mode_findings must be an object', path.name)
    if obj.get('scope', {}).get('editorial_policy') != POLICY:
        require(not set(R3_READINGS) & set(mode_findings),
                'SCHEMA_UNSUPPORTED', 'r3 output responsibilities require the explicit r3 policy', path.name)
    if obj.get('schema_version') != '2.2.0':
        scope = obj.get('scope', {})
        findings=scope.get('mode_findings',{})
        require(isinstance(findings,dict),'REVIEW_INVALID','mode_findings must be an object',path.name)
        require('view' not in scope and not ({'view_focus','exposition_design'} & set(findings)),
                'SCHEMA_UNSUPPORTED', 'rc2 review responsibilities require schema 2.2.0', path.name)
        for entry in scope.get('contribution_reviews', {}).values() if isinstance(scope.get('contribution_reviews', {}), dict) else []:
            require(not isinstance(entry, dict) or 'prior_result_checks' not in entry, 'SCHEMA_UNSUPPORTED', 'rc2 prior checks require schema 2.2.0', path.name)
    else:
        contributions=obj.get('scope',{}).get('contribution_reviews',{})
        require(isinstance(contributions,dict),'REVIEW_INVALID','contribution_reviews must be an object',path.name)
        for entry in contributions.values():
            require(isinstance(entry,dict) and isinstance(entry.get('prior_result_checks'),list),
                    'REVIEW_INVALID','rc2 contribution review requires typed prior_result_checks',path.name)
            for check in entry['prior_result_checks']:
                require(isinstance(check,dict) and all(isinstance(check.get(k),str) for k in
                    ('prior_result_id','source_id','version','locator','outcome','finding'))
                    and check['outcome'] in {'not_performed','accepted','revise','limited'},
                    'REVIEW_INVALID','Invalid prior-result support check',path.name)
    require(obj['kind'] in {'source','mathematical','coverage','output_semantic','visual'},'REVIEW_INVALID','Invalid review kind',path.name)
    require(obj['reviewer_mode'] in {'author_reread','independent_review','not_performed'},'REVIEW_INVALID','Do not label self-review independent',path.name)
    require(obj['disposition'] in {'accepted','revise','limited'} and 'reviewed_at' in obj,'REVIEW_INVALID','Invalid review disposition/date',path.name)
    require(obj['reviewed_at'] is None or valid_date(obj['reviewed_at']),'REVIEW_INVALID','Review date is not a real nonfuture date',path.name)
    require(obj['disposition']!='accepted' or (valid_date(obj['reviewed_at']) and obj['reviewer_mode']!='not_performed' and obj['findings']), 'REVIEW_INVALID','Accepted reviews require actual date, reviewer and findings',path.name)
    require(all(isinstance(x,str) and x.strip() for x in obj['findings']), 'REVIEW_INVALID', 'Findings must be substantive nonempty text entries',path.name)
    if obj['reviewer_mode']=='independent_review':
        require(isinstance(obj.get('reviewer'),str) and obj['reviewer'].strip(),'REVIEW_INVALID','An independent review must identify its actual reviewer; self-review is not independent',path.name)
    paths=[]
    for binding in obj['inputs']:
        fields(binding,{'path':str,'sha256':str},path.name); relative(binding['path'])
        require(re.fullmatch('[a-f0-9]{64}',binding['sha256']),'REVIEW_INVALID','Invalid binding hash',path.name)
        paths.append(binding['path'])
    require(len(paths)==len(set(paths)), 'REVIEW_INVALID','Duplicate input binding',path.name)
    require(isinstance(obj.get('scope',{}),dict),'REVIEW_INVALID','Review scope must be an object',path.name)
    return obj

def check_review_bindings(root: Path, review: dict, required: set[str] | None = None) -> list[dict]:
    errors=[]; paths=set()
    for binding in review['inputs']:
        p=binding['path']; paths.add(p); file=safe(root,p)
        if not file.is_file() or file_hash(root,p)!=binding['sha256']:
            errors.append(diagnostic('REVIEW_STALE',f"Review {review['review_id']} no longer matches this input",p))
    missing=(required or set())-paths
    if missing:
        errors.append(diagnostic('REVIEW_SCOPE_INSUFFICIENT',f"Review {review['review_id']} omits necessary inputs: {', '.join(sorted(missing))}"))
    return errors

def blocking_unchecked(review:dict)->list:
    return [v for v in review['unchecked_items'] if not (isinstance(v,dict) and v.get('blocking') is False and v.get('reason'))]

def reviews_in(root:Path, directory:str='evidence/reviews')->list[tuple[str,dict]]:
    result=[]
    for p in all_files(root,directory):
        if p.endswith('.json') and isinstance(read_json(safe(root,p,True)),dict) and 'review_id' in read_json(safe(root,p,True)):
            result.append((p,load_review(safe(root,p,True))))
    return result

def find_review(root:Path, records:list[tuple[str,dict]], kind:str, scope_field:str, key:str,
                required:set[str], extra_check=None)->tuple[dict|None,list[dict]]:
    candidates=[]; diagnostics=[]
    for path,r in records:
        if r['kind']==kind and key in r.get('scope',{}).get(scope_field,[]):
            errors=check_review_bindings(root,r,required)
            if extra_check is not None: errors += extra_check(r)
            if r['disposition']=='accepted' and not blocking_unchecked(r) and not errors:
                return r,[]
            candidates.append(r); diagnostics.extend(errors)
    return None,diagnostics

def source_inputs(inv, source_id:str)->set[str]:
    s=inv.sources[source_id]; out={inv.source_paths[source_id]}
    for field in ('reading_note','local_path'):
        if s['access'].get(field):out.add(s['access'][field])
    return out

def mathematical_inputs(inv,node_id:str)->set[str]:
    kr=inv.project['knowledge_root']; paths={'project.json',inv.project['scope_file'],kr+'/conventions.tex'}
    for key in comparison_evidence_closure(inv,required_closure(inv.nodes,{node_id})):
        paths.add(inv.nodes[key].path)
        for s in inv.nodes[key].meta['sources']:
            paths |= source_inputs(inv,s['source_id'])
    return paths

def comparison_evidence_closure(inv,ids:set[str])->set[str]:
    """Bind compared endpoints, without making navigation into proof edges.

    Only relation nodes actually consumed by the proof/selection provide pairs;
    do not recursively follow arbitrary navigation from endpoint nodes.
    """
    endpoints={edge['target'] for key in ids if inv.nodes[key].meta['kind']=='relation'
               for edge in inv.nodes[key].meta['links'] if edge['relation']=='compares_with'}
    return set(ids) | required_closure(inv.nodes,endpoints)

def coverage_inputs(inv,question_id:str)->set[str]:
    kr=inv.project['knowledge_root']
    paths={'project.json',inv.project['scope_file'],kr+'/coverage.json',kr+'/overview.md',kr+'/discovery.md',inv.nodes[question_id].path}
    for q in inv.coverage['questions']:
        if q['question_id']==question_id:
            for k in q['answer_nodes']+q['mechanism_nodes']+q['boundary_nodes']:
                paths.add(inv.nodes[k].path)
    return paths


def knowledge_scope_template(inv, question_ids: list[str]) -> dict:
    """Use existing scope fields for an r3 question-route reading."""
    from .profiles import POLICY, R3_READINGS
    nodes = set(question_ids)
    for q in inv.coverage['questions']:
        if q['question_id'] in question_ids:
            nodes.update(q['answer_nodes'] + q['mechanism_nodes'] + q['boundary_nodes'])
    return {'editorial_policy': POLICY, 'question_ids': question_ids,
            'node_ids': sorted(nodes), 'checks': list(R3_READINGS)}


def markdown_anchors(text: str, *, require_content: bool = False) -> set[str]:
    """Resolve bounded Markdown subsection syntax, excluding literal content.

    Explicit anchors must occupy their own unindented line. Arbitrary inline
    HTML is not interpreted as a renderable address or a visibility guarantee.
    """
    front = re.match(r'\A\ufeff?---\r?\n.*?\r?\n(?:---|\.\.\.)[ \t]*(?:\r?\n|$)', text, re.S)
    if front: text = text[front.end():]
    anchors = set(); counts = {}; fence = None; comment = False; html_stack = []
    content_anchors = set(); sections = []; explicit = set(); reference_definition = False
    # Markdown code spans may cross newlines. Preserve their line/column shape
    # so an anchor on a middle line cannot become falsely visible.
    code_mask = re.sub(r'(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)',
                       lambda m: re.sub(r'[^\r\n]', ' ', m[0]), text, flags=re.S)
    for line, masked in zip(text.splitlines(), code_mask.splitlines()):
        if fence is not None:
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(fence[1]) + r',}\s*', line):
                fence = None
            continue
        # A literal `<!--` must not hide subsequent real headings. Code text
        # in a heading still contributes to its ordinary heading slug below.
        comment_line = comment or line.lstrip().startswith('<!--')
        visible = []; visible_mask = []; position = 0
        while position < len(line):
            if comment:
                end = masked.find('-->', position)
                if end < 0: break
                position = end + 3; comment = False
            else:
                start = masked.find('<!--', position)
                if start < 0:
                    visible.append(line[position:]); visible_mask.append(masked[position:]); break
                visible.append(line[position:start]); visible_mask.append(masked[position:start])
                position = start + 4; comment = True
        line = ''.join(visible); masked = ''.join(visible_mask)
        if comment_line: continue
        if not line.strip():
            reference_definition = False
            continue
        if re.match(r'^(?: {4}| {0,3}\t| {0,3}>)', line): continue
        reference = re.match(r'^ {0,3}\[[^\]]+\]:[ \t]*(.*)$', masked)
        if reference:
            reference_definition = 'title' if reference[1].strip() else 'destination'
            continue
        if reference_definition == 'destination':
            reference_definition = 'title'
            continue
        if reference_definition and re.fullmatch(r' {0,3}(?:"[^"\n]*"|\'[^\'\n]*\'|\([^\n]*\))[ \t]*', masked):
            continue
        reference_definition = False
        if re.fullmatch(r' {0,3}([*_-])(?:[ \t]*\1){2,}[ \t]*', masked):
            continue
        mark = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if mark:
            fence = (mark[1][0], len(mark[1])); continue
        if not masked.strip(): continue
        # A heading written inside a raw HTML block is not a Markdown heading.
        # Ignore such blocks conservatively instead of guessing CSS visibility.
        tag = re.match(r'^ {0,3}<(/?)([A-Za-z][A-Za-z0-9-]*)\b[^>]*>', line)
        anchor = re.fullmatch(r' {0,3}<a\s+(?:id|name)=[\"\']([^\"\']+)[\"\']\s*>(?:</a>)?\s*', masked, re.I)
        if anchor and not html_stack:
            anchors.add(anchor[1]); explicit.add(anchor[1]); continue
        if html_stack or tag:
            for closing, name in re.findall(r'<(/?)([A-Za-z][A-Za-z0-9-]*)\b[^>]*>', masked):
                name = name.casefold()
                if closing:
                    if html_stack and name == html_stack[-1]: html_stack.pop()
                elif name not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
                    html_stack.append(name)
            continue
        heading = (re.match(r'^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$', line)
                   if re.match(r'^ {0,3}#{1,6}\s', masked) else None)
        if heading:
            value = re.sub(r'[^\w\- ]', '', heading[1].casefold()).replace(' ', '-')
            count = counts.get(value, 0); counts[value] = count + 1
            name = value + (f'-{count}' if count else '')
            anchors.add(name)
            level = len(re.match(r'^ {0,3}(#+)', line)[1])
            sections = [(key, depth) for key, depth in sections if depth < level]
            sections.extend((key, level) for key in explicit)
            explicit.clear()
            sections.append((name, level))
        elif re.search(r'\w', masked, re.UNICODE):
            # Headings, anchors, comments and code blocks alone do not locate
            # an explanation. Content may live in a descendant subsection.
            content_anchors.update(key for key, _ in sections)
            content_anchors.update(explicit)
    return content_anchors if require_content else anchors


def knowledge_scope_errors(inv, question_id: str, review: dict) -> list[dict]:
    """Check fixed KB task evidence; never infer understanding from the record.

    Existing findings strings start with a required check name and contain a
    project-root-relative Markdown link to the actual knowledge subsection.
    Existing inputs bind every cited file. No manuscript locations are used.
    """
    from urllib.parse import unquote
    from .profiles import POLICY, R3_READINGS, filled, mapping
    from .common import SurveyError
    scope = mapping(review.get('scope')); errors = []
    def fail(code, message, path='evidence/reviews'):
        errors.append(diagnostic(code, message, path, question_id))
    if scope.get('editorial_policy') != POLICY:
        fail('KNOWLEDGE_REVIEW_POLICY_REASSESSMENT_REQUIRED',
             'Record the four r3 knowledge tasks against the current node and route bytes; historical acceptance does not supply them.')
        return errors
    expected = knowledge_scope_template(inv, [question_id])
    checks = scope.get('checks', [])
    nodes = scope.get('node_ids', [])
    if (not isinstance(checks, list) or not all(isinstance(x, str) for x in checks)
            or not set(R3_READINGS) <= set(checks)):
        fail('KNOWLEDGE_REVIEW_PENDING', 'Knowledge scope must name all four actual understanding checks.')
    if (not isinstance(nodes, list) or not all(isinstance(x, str) and x in inv.nodes for x in nodes)
            or not set(expected['node_ids']) <= set(nodes)):
        fail('KNOWLEDGE_REVIEW_SCOPE_INSUFFICIENT', 'Knowledge review must identify the question and its actual answer, mechanism and boundary nodes.')
        nodes = expected['node_ids']
    required = coverage_inputs(inv, question_id) | {inv.nodes[k].path for k in nodes}
    findings = review.get('findings', [])
    for task in R3_READINGS:
        rows = [x.split(':', 1)[1].strip() for x in findings
                if isinstance(x, str) and re.match(r'^' + re.escape(task) + r'\s*:', x)]
        if not rows or any(not filled(row) for row in rows):
            fail('KNOWLEDGE_REVIEW_PENDING', f'Record the actual {task} answer, omissions and repairs in findings, not an accepted label.')
            continue
        for row in rows:
            links = re.findall(r'\[[^\]]+\]\(([^\s()]+)\)', row)
            local = [unquote(x) for x in links if '.md#' in x and '://' not in x]
            if not local:
                fail('KNOWLEDGE_REVIEW_LOCATION_INVALID', f'{task} needs a project-relative knowledge Markdown subsection link.')
            for link in local:
                path, _, anchor = link.partition('#')
                try:
                    file = safe(inv.root, path, True)
                    require(path.startswith(inv.project['knowledge_root'] + '/') and path.endswith('.md') and anchor,
                            'KNOWLEDGE_REVIEW_LOCATION_INVALID', 'Use a knowledge Markdown file and a concrete subsection anchor', path)
                    require(anchor in markdown_anchors(file.read_text(encoding='utf-8'), require_content=True),
                            'KNOWLEDGE_REVIEW_LOCATION_INVALID', 'Knowledge subsection needs actual non-code body content', path)
                    required.add(path)
                except (SurveyError, OSError, UnicodeError) as exc:
                    fail('KNOWLEDGE_REVIEW_LOCATION_INVALID', f'{task}: {exc}', path)
    errors.extend(check_review_bindings(inv.root, review, required))
    return errors

def review_template(root:Path,kind:str,keys:list[str],required:set[str],scope:dict|None=None)->dict:
    from .profiles import POLICIES
    selected_policy = (scope or {}).get('editorial_policy')
    require((selected_policy is None and 'editorial_policy' not in (scope or {})) or
            (isinstance(selected_policy, str) and selected_policy in {p for names in POLICIES.values() for p in names}),
            'SCHEMA_UNSUPPORTED', 'Unknown review policy')
    version = next((v for v,names in POLICIES.items() if selected_policy in names), VERSION)
    return {'schema_version':version,'review_id':'REPLACE-WITH-STABLE-REVIEW-ID','kind':kind,'reviewer_mode':'not_performed',
            'reviewed_at':None,'inputs':[{'path':p,'sha256':file_hash(root,p)} for p in sorted(required)],
            'scope':scope or { {'source':'source_ids','mathematical':'node_ids','coverage':'question_ids'}.get(kind,'output_ids'):keys},
            'findings':[],'unchecked_items':['Actual scoped reading and substantive findings have not been recorded.'], 'disposition':'revise'}
