#!/usr/bin/env python3
"""Validate public skill metadata, links, Tcl framing and optional local tools."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import os
from config import ROOT, state_dir
from install import install


def validate(project, tools=False):
    errors=[];skills=[]
    for f in sorted(ROOT.rglob('SKILL.md')):
        if any(x in f.parts for x in ('validation','__pycache__')):continue
        text=f.read_text()
        match=re.match(r'^---\n(.*?)\n---\n',text,re.S)
        if not match:
            errors.append(str(f)+': missing frontmatter');continue
        header=match.group(1)
        names=re.findall(r'^name: ([a-z0-9-]+)$',header,re.M)
        descriptions=re.findall(r'^description: (.+)$',header,re.M)
        if len(names)!=1 or len(descriptions)!=1 or len(names[0])>64:
            errors.append(str(f)+': invalid name/description');continue
        description=descriptions[0]
        if description.startswith('"'):
            try:description=json.loads(description)
            except ValueError:errors.append(str(f)+': malformed quoted description');continue
        if not description or len(description)>1024:
            errors.append(str(f)+': invalid description length')
        if f.parent.parent.name=='skills' and names[0]!=f.parent.name:
            errors.append(str(f)+': directory/name mismatch')
        skills.append({'name':names[0],'path':str(f)})
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if target.startswith(('https:','http:','#')):continue
            if not (f.parent/target.split('#')[0]).resolve().exists():errors.append(str(f)+': missing reference '+target)
    if tools:
        inventory=state_dir()/'tool_inventory.json'
        if not inventory.is_file():errors.append('Generate a private local inventory before --tools validation')
        else:
            for tool in json.loads(inventory.read_text()).get('tools',[]):
                if not os.access(tool['executable'],os.X_OK):errors.append('Unavailable executable: '+tool['id'])
    tcl=[]
    for f in sorted((ROOT/'templates').glob('*.tcl')):
        if not shutil.which('tclsh'):
            tcl.append({'path':str(f),'status':'not checked: tclsh unavailable'});continue
        script='set f [open $::env(SNPS_TCL_FILE) r]\nset s [read $f]\nclose $f\nputs [info complete $s]\n'
        p=subprocess.run(['tclsh'],input=script,text=True,capture_output=True,env=dict(os.environ,SNPS_TCL_FILE=str(f)))
        complete=p.returncode==0 and p.stdout.strip()=='1'
        tcl.append({'path':str(f),'complete':complete,'scope':'structural framing only'})
        if not complete:errors.append(str(f)+': incomplete Tcl framing')
    adapters=install(project,check=True)
    if any(not x['discoverable_file'] for x in adapters):errors.append('Missing project platform adapter; run install.py')
    return {'skills':skills,'tcl':tcl,'adapters':adapters,'errors':errors,'passed':not errors}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--project',type=Path,default=ROOT.parent)
    ap.add_argument('--tools',action='store_true')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args();result=validate(args.project,args.tools)
    if args.output:
        with args.output.open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps({'skills':len(result['skills']),'adapters':len(result['adapters']),'tcl_templates':len(result['tcl']),'errors':result['errors'],'passed':result['passed']},indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__=='__main__':main()
