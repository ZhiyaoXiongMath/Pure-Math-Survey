"""Stable CLI envelopes and exit codes. --json is accepted at every position."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
from .common import VERSION,SOFTWARE_VERSION,SurveyError,diagnostic,file_hash,read_json,relpath,result,safe,write_json,writer

class Parser(argparse.ArgumentParser):
    def error(self,message):raise SurveyError('CLI_ARGUMENT_INVALID',message)

def parser()->Parser:
    p=Parser(description='Pure Math Survey 2.1.0: knowledge first, immutable inputs, honest evidence.');p.add_argument('--version',action='store_true')
    sub=p.add_subparsers(dest='command')
    i=sub.add_parser('init');i.add_argument('--output',type=Path,required=True);i.add_argument('--topic',required=True);i.add_argument('--scope',type=Path,required=True);i.add_argument('--title');i.add_argument('--language',default='en')
    k=sub.add_parser('kb');ks=k.add_subparsers(dest='action',required=True)
    for name in ('validate','index','freeze','verify','readiness','diff'):
        x=ks.add_parser(name);x.add_argument('project',type=Path)
        if name=='verify':x.add_argument('--snapshot',required=True)
        if name=='readiness':x.add_argument('--plan',required=True)
        if name=='diff':x.add_argument('--from',dest='old',required=True);x.add_argument('--to',dest='new',required=True)
    o=sub.add_parser('output');os=o.add_subparsers(dest='action',required=True)
    for name in ('plan','prepare','validate','build','render','package','review-template','reading-budget','history'):
        x=os.add_parser(name);x.add_argument('project',type=Path)
        if name=='prepare':x.add_argument('--plan',required=True);x.add_argument('--draft',action='store_true')
        elif name=='plan':
            x.add_argument('--output',required=True);x.add_argument('--snapshot',required=True);x.add_argument('--profile',default='minimal',choices=['minimal','thematic','lecture','paper']);x.add_argument('--view',default='integrated',choices=['integrated','foundations','results','methods','boundaries'],help='Reader emphasis for goals, node uses, writing tasks and semantic reading; preserves profile and canonical obligations')
            x.add_argument('--question',action='append');x.add_argument('--principal',action='append');x.add_argument('--title');x.add_argument('--draft',action='store_true');x.add_argument('--comparison-group');x.add_argument('--max-pages',type=int)
        else:x.add_argument('--output',required=True)
        if name=='validate':
            x.add_argument('--stage',choices=['plan','structure','release'],default='plan')
            x.add_argument('--policy',choices=['current','recorded'],default='current',help='recorded is read-only and never authorizes package')
        if name=='render':x.add_argument('--dpi',type=int,default=120)
        if name=='package':x.add_argument('--to',type=Path,required=True)
        if name=='review-template':x.add_argument('--kind',choices=['output_semantic','visual'],required=True);x.add_argument('--to')
    r=sub.add_parser('review');rs=r.add_subparsers(dest='action',required=True);x=rs.add_parser('template');x.add_argument('project',type=Path);x.add_argument('--kind',choices=['source','mathematical','coverage'],required=True);x.add_argument('--id',action='append',required=True);x.add_argument('--to');x.add_argument('--principal-statements',action='store_true')
    return p

def execute(a)->dict:
    if a.version:
        from .profiles import OUTPUT_SCHEMA, POLICY, POLICIES, SUPPORTED_CONTRACTS
        return result('version','OK',{'version':SOFTWARE_VERSION,'schema_version':VERSION,'output_schema_version':OUTPUT_SCHEMA,'editorial_policy':POLICY,'supported_output_schemas':list(POLICIES),'recorded_policies':POLICIES,'supported_output_contracts':[{'schema_version':v,'editorial_policy':p} for v,p in sorted(SUPPORTED_CONTRACTS)],'python':sys.version})
    if a.command=='init':
        from .knowledge import init_project
        return init_project(a.output,a.topic,a.scope,a.title,a.language)
    root=a.project.absolute()
    if a.command=='kb':
        from .knowledge import validate_knowledge,index_knowledge
        from .snapshots import freeze_snapshot,verify_snapshot,diff_snapshots
        from .readiness import assess_readiness
        if a.action=='validate':return validate_knowledge(root)
        if a.action=='index':return index_knowledge(root)
        if a.action=='freeze':return freeze_snapshot(root)
        if a.action=='verify':return verify_snapshot(root,a.snapshot)
        if a.action=='diff':return diff_snapshots(root,a.old,a.new)
        return assess_readiness(root,safe(root,relpath(root,a.plan),True))
    if a.command=='review':
        from .knowledge import inventory
        from .reviews import review_template,source_inputs,mathematical_inputs,coverage_inputs
        inv=inventory(root);f={'source':source_inputs,'mathematical':mathematical_inputs,'coverage':coverage_inputs}[a.kind]
        paths=set()
        for k in a.id:paths|=f(inv,k)
        scope=None
        if a.kind=='coverage':
            from .reviews import knowledge_scope_template
            scope=knowledge_scope_template(inv,a.id)
        if a.principal_statements:
            from .profiles import POLICY, principal_template
            from .common import require
            require(a.kind=='mathematical', 'CLI_ARGUMENT_INVALID', '--principal-statements is for mathematical review')
            require(all(inv.nodes[k].statement is not None for k in a.id),'CANONICAL_BLOCK_MISSING','Principal review requires canonical statements')
            scope={'node_ids':a.id,'editorial_policy':POLICY,'statement_reviews':{k:principal_template(inv.nodes[k].statement) for k in a.id}}
        template=review_template(root,a.kind,a.id,paths,scope)
        if a.kind=='coverage':
            template['unchecked_items'].append('For each check, add a findings string beginning with its check name and a colon, the actual answer or failure, and a project-root-relative Markdown link to the knowledge file#subsection. Bind every cited route file in inputs. Do not use manuscript locations or claim real-reader/external review without that evidence.')
        if a.to:
            with writer(root):
                target=safe(root,relpath(root,a.to))
                from .common import require
                require(not target.exists(),'DESTINATION_EXISTS','Never overwrite an existing review; choose a new record path',str(a.to))
                write_json(target,template)
        return result('review.template','PENDING_TEMPLATE',{'review':template,'path':a.to})
    if a.command=='output':
        from .models import load_plan
        from .plans import create_plan,validate_plan,consumption
        from .exports import prepare_output,validate_structure,output_inputs
        from .build import build_output,render_output,reading_budget
        from .release import assess_release,package_output
        if a.action=='plan':return create_plan(root,a.output,a.snapshot,a.profile,a.view,a.question,a.principal,a.title,a.draft,a.comparison_group,a.max_pages)
        if a.action=='prepare':return prepare_output(root,safe(root,relpath(root,a.plan),True),a.draft)
        out=safe(root,'outputs/'+a.output)
        if a.action=='history':
            from .history import verify_history
            return verify_history(root,a.output)
        if a.action=='reading-budget':return reading_budget(root,a.output)
        if a.action=='build':return build_output(root,a.output)
        if a.action=='render':return render_output(root,a.output,a.dpi)
        if a.action=='package':return package_output(root,a.output,a.to)
        if a.action=='validate':
            if a.stage=='release':return assess_release(root,a.output,policy_mode=a.policy)
            if a.stage=='structure':return validate_structure(root,a.output)
            plan=load_plan(out/'plan.json');inv=validate_plan(root,plan)
            return result('output.plan','VALID',{'output_id':a.output,'consumed_nodes':sorted(consumption(inv,plan))})
        from .reviews import review_template
        plan=load_plan(out/'plan.json');inv=validate_plan(root,plan)
        if a.kind=='output_semantic':
            paths=output_inputs(out);scope={'output_ids':[a.output],'profile':plan['profile'],'node_ids':sorted(consumption(inv,plan)),
                  'whole_manuscript':False,'checks':[], 'principal_locations':{},'proof_steps':{},'proof_locations':{}}
            from .profiles import review_scope_template, principal_template, four_modes
            scope.update(review_scope_template(plan))
            if four_modes(plan):
                scope['statement_reviews']={s['node_id']:principal_template(inv.nodes[s['node_id']].statement) for s in plan['selections'] if s['role']=='principal_answer'}
        else:
            m=read_json(safe(out,'evidence/render-manifest.json',True))
            paths={'build/main.pdf','build/build-report.json','evidence/render-manifest.json'}|{x['path'] for x in m['pages']}
            scope={'output_ids':[a.output],'pdf_sha256':m['pdf_sha256'],'pages':[x['page'] for x in m['pages']],'page_findings':[]}
        template=review_template(out,a.kind,[a.output],paths,scope)
        if a.to:
            with writer(root):
                target=safe(out,a.to)
                from .common import require
                require(not target.exists(),'DESTINATION_EXISTS','Never overwrite an existing review; choose a new record path',a.to)
                write_json(target,template)
        return result('output.review-template','PENDING_TEMPLATE',{'review':template,'path':a.to})
    raise SurveyError('CLI_ARGUMENT_INVALID','Select a subcommand; use --help')

def main(argv:list[str]|None=None)->int:
    argv=list(sys.argv[1:] if argv is None else argv);as_json='--json' in argv;argv=[a for a in argv if a!='--json']
    try:
        a=parser().parse_args(argv)
        if not a.version and a.command is None:raise SurveyError('CLI_ARGUMENT_INVALID','A command is required; use --help')
        report=execute(a);code=3 if report['status']=='NEEDS_WORK' else 0
    except SurveyError as e:
        d=e.diagnostic;code=e.exit_code
        if d['code'] in {'READINESS_REQUIRED','RELEASE_NOT_READY','DRAFT_NOT_RELEASABLE'}:code=3
        if d['code'].startswith(('BUILD_','RENDER_')):code=4
        report=result('error','NEEDS_WORK' if code==3 else 'ERROR',errors=[d])
    except (OSError,subprocess.SubprocessError) as e:
        code=4;report=result('error','ERROR',errors=[diagnostic('TOOL_OR_IO_FAILED',str(e))])
    except (ValueError,KeyError,TypeError,UnicodeError) as e:
        code=2;report=result('error','ERROR',errors=[diagnostic('CONTRACT_INVALID',str(e))])
    if as_json:print(json.dumps(report,ensure_ascii=False,indent=2))
    else:
        print(report['operation']+': '+report['status'])
        for x in report['errors']+report['warnings']:print(f"{x['code']}: {x['path']} {x['message']}")
        print(json.dumps(report['artifacts'],ensure_ascii=False,indent=2))
    return code
