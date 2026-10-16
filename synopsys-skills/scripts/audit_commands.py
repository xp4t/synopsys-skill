#!/usr/bin/env python3
"""Match generic command candidates against the user's private manual index."""
import argparse
import json
from pathlib import Path
import sqlite3
from config import ROOT, state_dir


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db',type=Path,default=state_dir()/'command_index.sqlite')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    if not args.db.is_file():ap.error('Generate a private command index first')
    catalog=json.loads((ROOT/'references/tool_catalog.json').read_text())
    con=sqlite3.connect(f'file:{args.db}?mode=ro',uri=True)
    result=[];missing=[]
    for tool,profile in catalog.items():
        if not profile['suggested_script_option'] or tool in {'verdi','vc-static'}:continue
        for stage in profile['stages']:
            for command in stage['commands'].split():
                rows=con.execute('SELECT path,sha256,version FROM docs WHERE tool=? AND name=? AND kind=? ORDER BY version,path',(tool,command,'manual')).fetchall()
                result.append({'tool':tool,'stage':stage['stage'],'command':command,'sources':[{'path':p,'sha256':h,'version':v} for p,h,v in rows[:3]]})
                if not rows:missing.append({'tool':tool,'command':command})
    con.close()
    if args.output:
        with args.output.open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps({'references_checked':len(result),'unresolved_in_local_index':missing},indent=2))
    raise SystemExit(1 if missing else 0)


if __name__=='__main__':main()
