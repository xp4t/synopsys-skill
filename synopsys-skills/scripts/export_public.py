#!/usr/bin/env python3
"""Export portable source; omit runtime state and reject common private data."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil

PATTERNS={
    'personal_path':re.compile(r'/(?:home|Users)/[^\s/"\']+'),
    'fixed_installation':re.compile(r'/(?:opt|tools|eda)/[A-Za-z0-9_.-]+'),
    'network_address':re.compile(r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])'),
    'license_endpoint':re.compile(r'\b\d{2,5}@[A-Za-z0-9_.-]+'),
    'email_address':re.compile(r'\b[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
    'hardware_address':re.compile(r'\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b'),
    'credential_value':re.compile(r'''(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*["']?[A-Za-z0-9+/=_-]{20,}'''),
}
BLOCKED_DIRS={'__pycache__','validation','run_details','checkpoints','restores','runs','.local','.private','private','dist'}


def find_private_data(text):
    # Findings identify the category and line, never repeat the matched value.
    return [{'category':name,'line':text.count('\n',0,m.start())+1}
            for name,pattern in PATTERNS.items() for m in pattern.finditer(text)]


def public_files(root):
    root=Path(root).absolute()
    candidates=[root/'README.md',root/'.gitignore']
    bundle=root/'synopsys-skills'
    candidates += [bundle/name for name in ['README.md','READINESS.md','SKILL.md']]
    for folder,extensions in [('scripts',{'.py'}),('tests',{'.py'}),('templates',{'.tcl','.py'}),('skills',{'.md'}),('references',{'.md'}),('examples',{'.md','.json','.tcl','.sdc','.sv','.sp'})]:
        for p in (bundle/folder).rglob('*'):
            if p.is_file() and p.suffix in extensions and not any(x in BLOCKED_DIRS for x in p.relative_to(root).parts):
                candidates.append(p)
    candidates.append(bundle/'references/tool_catalog.json')
    selected=[]
    for p in sorted(set(candidates)):
        if not p.is_file():continue
        if p.is_symlink():raise ValueError('Unexpected linked public source: '+str(p.relative_to(root)))
        selected.append(p)
    links=[]
    for platform in ['.agents','.claude']:
        for p in sorted((root/platform/'skills').glob('*')):
            if not p.is_symlink():raise ValueError('Platform entries must link to canonical public skills')
            target=os.readlink(p)
            resolved=(p.parent/target).resolve()
            canonical=(bundle/'skills').resolve()
            if Path(target).is_absolute() or not resolved.is_relative_to(canonical) or not (resolved/'SKILL.md').is_file():
                raise ValueError('Platform link must be relative and stay within public skills')
            links.append(p)
    return selected,links


def export_public(root,out=None):
    root=Path(root).absolute();files,links=public_files(root)
    findings=[]
    for p in files:
        try:text=p.read_text()
        except UnicodeDecodeError:raise ValueError('Non-text content in public source selection')
        findings += [dict(item,path=str(p.relative_to(root))) for item in find_private_data(text)]
    if findings:raise ValueError('Private-data candidates in public source: '+json.dumps(findings))
    if out is not None:
        out=Path(out).absolute();out.mkdir(parents=True,exist_ok=False)
        for p in files:
            dest=out/p.relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
        for p in links:
            dest=out/p.relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True);dest.symlink_to(os.readlink(p),target_is_directory=True)
    return {'files':len(files),'skill_links':len(links),'private_data_findings':0}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    ap.add_argument('--out',type=Path,help='New destination directory; omit to scan without copying')
    args=ap.parse_args()
    try:result=export_public(args.root,args.out)
    except (ValueError,FileExistsError) as e:ap.error(str(e))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
