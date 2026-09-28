"""Explicit legacy entry dispatch. v1 manifest semantics are not silently upgraded."""
from __future__ import annotations
import json
from pathlib import Path
import sys
from .common import SurveyError,diagnostic,result

def dispatch(entry:str,argv:list[str])->int|None:
    root=next((Path(a) for a in argv if not a.startswith('-') and Path(a).is_dir() and ((Path(a)/'project.json').exists() or (Path(a)/'project-manifest.json').exists())),None)
    if root is None or not (root/'project.json').exists():return None
    from .cli import main
    if (root/'project-manifest.json').exists():
        print(json.dumps(result('legacy.dispatch','ERROR',errors=[diagnostic('MANIFEST_CONFLICT','Both native and legacy root manifests exist; choose an explicit migration boundary')])));return 2
    output=argv[argv.index('--output')+1] if '--output' in argv and argv.index('--output')+1<len(argv) else None
    stage=argv[argv.index('--stage')+1] if '--stage' in argv and argv.index('--stage')+1<len(argv) else 'plan'
    if entry=='validate_project.py':args=['kb','validate',str(root)]
    elif output and entry=='check_reading_budget.py':args=['output','reading-budget',str(root),'--output',output]
    elif output:
        mapped='release' if stage=='release' or entry=='check_reading_budget.py' else ('structure' if entry=='check_mathematical_structure.py' else 'plan')
        args=['output','validate',str(root),'--output',output,'--stage',mapped]
    elif entry in {'check_problem_formulation.py','check_survey_selection.py'}:
        args=['kb','validate',str(root)]
    else:
        print(json.dumps(result('legacy.dispatch','ERROR',errors=[diagnostic('V2_EXPLICIT_OUTPUT_REQUIRED','For a native v2 project supply --output ID, or use survey.py output explicitly. No v1 audit was inherited.')])));return 2
    if '--json' in argv:args.append('--json')
    else:print('Native v2 dispatch; v1 document/audit semantics are not applied.',file=sys.stderr)
    return main(args)
