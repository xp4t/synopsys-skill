#!/usr/bin/env python3
"""Expose canonical skills in platform-specific roots without overwriting entries."""
import argparse
import json
import os
from pathlib import Path
import re
from execution import ROOT


def install(project, check=False):
    project=Path(project).resolve()
    plans=[]
    for source in sorted((ROOT/'skills').iterdir()):
        skill=source/'SKILL.md'
        if not skill.is_file():
            continue
        name=re.search(r'^name: ([a-z0-9-]+)$',skill.read_text(),re.M).group(1)
        if source.name!=name:
            raise ValueError('Canonical directory and skill name must match')
        for platform,subdir in [('codex','.agents/skills'),('claude','.claude/skills')]:
            dest=project/subdir/name
            if dest.exists() or dest.is_symlink():
                if not dest.is_symlink() or dest.resolve()!=source.resolve():
                    raise FileExistsError('Existing entry will not be replaced: '+str(dest))
            plans.append((platform,source,dest))
    if not check:
        for platform,source,dest in plans:
            dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.is_symlink():
                dest.symlink_to(os.path.relpath(source,dest.parent),target_is_directory=True)
    return [{'platform':platform,'name':source.name,'path':str(dest),
             'discoverable_file':(dest/'SKILL.md').is_file(),'target':str(source)} for platform,source,dest in plans]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--project',type=Path,required=True)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args();result=install(args.project,args.check)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if all(x['discoverable_file'] for x in result) else 2)


if __name__=='__main__':
    main()
