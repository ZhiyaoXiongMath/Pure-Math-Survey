"""Editable TikZ defaults and mechanical identity checks; no mathematical approval."""
from __future__ import annotations
import math
import re
from .common import canonical, diagnostic, sha, require
from .dependencies import route_inputs
from .plans import consumption


def token(identity):
    return identity if re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',identity) else 'g'+sha(identity.encode())[:16]


def graph_map(inv,plan):
    selected={s['node_id']:s for s in plan['selections']};consumed=consumption(inv,plan)
    routes=[r for r in inv.routes if r['id'] in plan['route_ids']]
    used={k for r in routes for k in route_inputs(r)|{r['target']}}
    nodes=[]
    for key in sorted(consumed):
        n=inv.nodes[key]
        formal=n.statement is not None and (n.meta['kind']=='definition' or selected.get(key,{}).get('statement_treatment','full')=='full')
        if formal and (n.meta['kind']!='definition' or key in used):
            kind=n.meta.get('statement_kind',{'definition':'definition','example':'example'}.get(n.meta['kind'],'theorem'))
            nodes.append({'id':key,'token':token(key),'reference':'node:'+key,'environment':kind})
    formal_ids={n['id'] for n in nodes}
    for key in used:
        require(key in formal_ids or (inv.nodes[key].meta['kind']=='method' and inv.nodes[key].statement is None),
                'GRAPH_FORMAL_STATEMENT_REQUIRED','Selected route interfaces need full statements in the manuscript: '+key,'plan.json',key)
    groups=[]
    for route in routes:
        for i,group in enumerate(route['premise_sets'],1):
            groups.append({'route_id':route['id'],'alternative':i,'alternatives':len(route['premise_sets']),
                'join':token(route['id'])+'-'+str(i),'target':route['target'],'nodes':group['nodes'],
                'additional_inputs':group['additional_inputs'],'status':route['status'],'mapping':route['mapping']})
    return {'schema_version':'3.0.0','nodes':nodes,'groups':groups,
        'meaning':'Same selected formal statements and grouped routes; mathematical implication is not certified.'}


def graph_tex(inv,plan):
    from .exports import tex_text
    m=graph_map(inv,plan);nodes={n['id']:n for n in m['nodes']};levels={k:0 for k in nodes}
    for _ in nodes:
        for group in m['groups']:
            if group['target'] in levels:
                levels[group['target']]=max(levels[group['target']],1+max((levels[k] for k in group['nodes'] if k in levels),default=-1))
    positions={}
    for level in sorted(set(levels.values())):
        keys=[k for k in nodes if levels[k]==level]
        for i,key in enumerate(keys):positions[key]=(4.8*(i-(len(keys)-1)/2),-3.5*level)
    lines=['% Editable layout; identities and premise groups derive from generated/graph-map.json.',
        '% Edit coordinates and short mathematical labels; preserve literal node/ref and route connections.',
        r'\begin{tikzpicture}[pmsgraph]']
    for key,row in nodes.items():
        x,y=positions[key]
        lines += ['% unit: '+key,r'\node[pmsresult] ('+row['token']+f') at ({x:g},{y:g})'+' {'+row['environment'].title()+r'~\ref{'+row['reference']+'}};']
    for index,group in enumerate(m['groups']):
        target=group['target'];join=group['join'];x,y=positions[target];x+=(group['alternative']-(group['alternatives']+1)/2)*1.7;y+=1.5
        style='pmsunresolved' if group['status']=='unresolved' else 'pmsedge'
        label='joint inputs' if len(group['nodes'])>1 else 'input'
        if group['alternatives']>1:label+='; alternative '+str(group['alternative'])
        if group['status']=='unresolved':label+='; unresolved'
        lines += ['% route: '+group['route_id']+' premise_set '+str(group['alternative']),
            r'\node[pmsjoin] ('+join+f') at ({x:g},{y:g})'+' {'+tex_text(label)+'};']
        for key in group['nodes']:
            if key in nodes:lines.append(r'\draw['+style+'] ('+nodes[key]['token']+') -- ('+join+');')
            else:
                name='method-'+str(index)+'-'+token(key)
                lines += ['% note-owner: '+name+' '+join,r'\node[pmsannotation] ('+name+f') at ({x+4.6:g},{y:g})'+' {Method description: '+tex_text(inv.nodes[key].meta['title'])+'};',r'\draw[pmsattachment] ('+name+') -- ('+join+');']
        lines.append(r'\draw['+style+'] ('+join+') -- ('+nodes[target]['token']+');')
        if group['additional_inputs']:
            name='inputs-'+join
            lines += ['% note-owner: '+name+' '+join,r'\node[pmsannotation] ('+name+f') at ({x+4.6:g},{y-0.7:g})'+' {'+tex_text('; '.join(group['additional_inputs']))+'};',r'\draw[pmsattachment] ('+name+') -- ('+join+');']
    lines += [r'\end{tikzpicture}',r'\par\noindent Joint-input boxes require all incident premises; numbered alternatives are separate routes. Dashed lines indicate unresolved connections; dotted attachments scope notes without asserting implications.','']
    return '\n'.join(lines).encode('utf-8')


def literal_commands(text, command):
    """A TikZ command ends at an unbraced, unescaped semicolon, not label punctuation."""
    from .tex import TOKEN
    commands=[];cursor=0
    for match in re.finditer(r'\\'+command+r'\b',text):
        if match.start()<cursor:continue
        depth=0;i=match.end()
        while i<len(text):
            if text[i]=='\\':
                token=TOKEN.match(text,i);i=token.end() if token else i+1;continue
            if text[i]=='{':depth+=1
            elif text[i]=='}':depth-=1
            elif text[i]==';' and depth==0:
                commands.append(text[match.start():i+1]);cursor=i+1;break
            i+=1
    return commands


def graph_errors(inv,plan,raw):
    """Check literal graph membership and grouping, leaving mathematical labels to authoring."""
    from .structure import strip_comments
    m=graph_map(inv,plan);text=strip_comments(raw);errors=[]
    def add(message):errors.append(diagnostic('GRAPH_IDENTITY_INVALID',message,'manuscript/architecture_graph.tex'))
    nodes={n['id']:n for n in m['nodes']}
    node_commands=literal_commands(text,'node')
    declarations={};node_statements={}
    for statement in node_commands:
        match=re.match(r'\\node\s*\[([^\]]*)\]\s*\(([^)]+)\)',statement)
        if not match:
            add('Use literal named nodes with explicit styles');continue
        options,name=match.groups()
        if name in declarations:add('Duplicate graph node identity: '+name)
        declarations[name]=options;node_statements[name]=statement
    if len(node_commands)!=len(re.findall(r'\\node\b',text)):add('Unterminated or unsupported graph node declaration')
    edges=[(options,a.split('.')[0],b.split('.')[0]) for options,a,b in re.findall(r'\\draw\s*\[([^\]]*)\]\s*\(([^)]+)\)(?:\.[A-Za-z]+)?\s*(?:--|to(?:\[[^\]]*\])?)\s*\(([^)]+)\)',text)]
    if len(edges)!=len(re.findall(r'\\draw\b',text)) or re.search(r'\\(?:path|edge)\b',text):
        add('Use literal draw connections with -- or to[...]; unsupported path syntax cannot establish graph consistency')
    if re.search(r'pms(?:graph|result|join|edge|unresolved|annotation|attachment)/\.',text):
        add('Keep the installed semantic graph styles unchanged; customize node coordinates and local appearance')
    def connection(a,b,style):
        return any(x==a and y==b and style in [v.strip() for v in options.split(',')] for options,x,y in edges)
    for key,row in nodes.items():
        if row['token'] not in declarations or 'pmsresult' not in [v.strip() for v in declarations[row['token']].split(',')]:add('Missing formal graph node '+key)
        node_statement=node_statements.get(row['token'],'')
        if r'\ref{'+row['reference']+'}' not in node_statement:add('Graph node must reference its formal statement: '+key)
    expected=set()
    for group in m['groups']:
        join=group['join'];style='pmsunresolved' if group['status']=='unresolved' else 'pmsedge'
        if join not in declarations or 'pmsjoin' not in [v.strip() for v in declarations[join].split(',')]:add('Missing premise-set join '+join)
        for key in group['nodes']:
            if key in nodes:
                expected.add((nodes[key]['token'],join))
                if not connection(nodes[key]['token'],join,style):add('Missing or wrong premise connection '+key+' -> '+join)
        expected.add((join,nodes[group['target']]['token']))
        if not connection(join,nodes[group['target']]['token'],style):add('Missing or wrong route conclusion '+join)
    for options,a,b in edges:
        if re.search(r'(?:^|,)\s*(?:[<>-]+(?:\{|$|,)|arrows\s*=)',options):
            add('Do not override the direction or unresolved status of a semantic connection')
        if not any(style in [v.strip() for v in options.split(',')] for style in ('pmsedge','pmsunresolved','pmsattachment')):
            add('Use an explicit edge, unresolved connection or note attachment style: '+a+' -> '+b)
        if ('pmsedge' in [v.strip() for v in options.split(',')] or 'pmsunresolved' in [v.strip() for v in options.split(',')]) and (a,b) not in expected:add('Unrecorded implication '+a+' -> '+b)
        if 'pmsunresolved' in [v.strip() for v in options.split(',')] and any(mark in options for mark in ('->','<-','pmsedge')):add('Unresolved connections cannot assert a directed proof arrow')
    owners=dict(re.findall(r'^%\s*note-owner:\s*(\S+)\s+(\S+)\s*$',raw,re.M))
    for group in m['groups']:
        note_names=[]
        if group['additional_inputs']:note_names.append('inputs-'+group['join'])
        index=m['groups'].index(group)
        note_names += ['method-'+str(index)+'-'+token(k) for k in group['nodes'] if k not in nodes]
        for name in note_names:
            if name not in declarations or owners.get(name)!=group['join']:
                add('Missing required input/method note attached to its premise set: '+name)
    for name,options in declarations.items():
        if 'pmsannotation' in [v.strip() for v in options.split(',')]:
            owner=owners.get(name)
            if owner not in declarations or not (connection(name,owner,'pmsattachment') or connection(owner,name,'pmsattachment')):add('Method/input note needs an explicit owner attachment: '+name)
        if 'pmsresult' in [v.strip() for v in options.split(',')] and name not in {n['token'] for n in m['nodes']}:add('Result node does not correspond to a selected formal statement: '+name)
    return errors
