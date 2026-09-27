#!/usr/bin/env python3
"""Validate JSON by asset role, including nested templates; no mathematical grading."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def validate_asset_json(assets: Path) -> dict:
    if not assets.is_dir():
        raise ValueError(f"Assets directory does not exist: {assets}")
    templates=[];bibliographies=[]
    for path in sorted(assets.rglob('*-template.json')):
        value=json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(value,dict) or value.get('schema_version') != '1.0.0':
            raise ValueError(f'Invalid template schema: {path}')
        templates.append(path.relative_to(assets).as_posix())
    for path in sorted((assets/'reference-samples').rglob('references.json')):
        value=json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(value,list) or not value:
            raise ValueError(f'Invalid sample bibliography: {path}')
        keys=[]
        for r in value:
            if not isinstance(r,dict) or not all(r.get(k) for k in ('key','title','author')):
                raise ValueError(f'Invalid bibliography record: {path}')
            keys.append(r['key'])
        if len(keys)!=len(set(keys)): raise ValueError(f'Duplicate sample citation key: {path}')
        bibliographies.append(path.relative_to(assets).as_posix())
    if not templates and not bibliographies:
        raise ValueError('No supported JSON assets found; nothing was validated')
    return {'status':'PASS','scope':'JSON shape/role only','templates':templates,'bibliographies':bibliographies}

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--assets',type=Path,default=ROOT/'assets')
    args=p.parse_args()
    try: print(json.dumps(validate_asset_json(args.assets),indent=2))
    except (OSError,ValueError,TypeError) as exc: p.exit(1,f'Asset validation failed: {exc}\n')
    return 0
if __name__=='__main__':raise SystemExit(main())
