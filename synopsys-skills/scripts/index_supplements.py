#!/usr/bin/env python3
"""Add locally available API/utility references and optional captured driver help."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from config import state_dir


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db',type=Path,default=state_dir()/'command_index.sqlite')
    ap.add_argument('--inventory',type=Path,default=state_dir()/'tool_inventory.json')
    ap.add_argument('--help-log',action='append',default=[],metavar='TOOL=FILE')
    args=ap.parse_args()
    if not args.db.is_file():ap.error('Build a private documentation index first')
    tools=json.loads(args.inventory.read_text())['tools']
    con=sqlite3.connect(args.db)
    if 'start_line' not in [r[1] for r in con.execute('PRAGMA table_info(docs)')]:
        con.execute('ALTER TABLE docs ADD COLUMN start_line INTEGER DEFAULT 1')
    count=0
    def add(tool,name,kind,p,description,line=1,tool_id=None):
        nonlocal count
        identifier=tool_id or tool['id'];p=Path(p).absolute()
        if con.execute('SELECT 1 FROM docs WHERE tool=? AND path=? AND name=?',(identifier,str(p),name)).fetchone():return
        con.execute('INSERT INTO docs(tool,version,installation,name,kind,path,sha256,description,effect,stages,availability,start_line) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                    (identifier,tool['directory_version'],tool['installation'],name,kind,str(p),hashlib.sha256(p.read_bytes()).hexdigest(),description,'consult original side effects','consult current stage prerequisites','documented source; execution unproven',line));count+=1
    for tool in tools:
        root=Path(tool['installation'])
        if tool['id'] in {'ndm-library-manager','ic-compiler-ii','fusion-compiler'}:
            for p in (root/'doc/LM/man').glob('cat[12]/*'):
                if p.is_file():add(tool,re.sub(r'\.[12]$','',p.name),'manual',p,'Local Library Manager manual',tool_id='ndm-library-manager')
        if tool['id']=='starrc':
            for p in (root/'help/mw_help').glob('*.html'):
                add(tool,p.stem,'milkyway-help',p,'Utility API documentation; not extraction-control syntax')
        if tool['id']=='ic-validator':
            for p in (root/'include').rglob('*.rh'):
                raw=p.read_text(errors='replace');add(tool,p.name,'pxl-header',p,'Declarations; encrypted definitions remain unavailable')
                text=re.sub(r'#pragma PXL encrypted begin.*?#pragma PXL encrypted end',lambda m:''.join('\n' if c=='\n' else ' ' for c in m.group()),raw,flags=re.S)
                for line_no,line in enumerate(text.splitlines(),1):
                    m=re.match(r'^\s*(\w+)\s*:\s*(?:\w+\s+)*function\s*\(',line)
                    if m:add(tool,m.group(1),'pxl-api',p,'Plaintext API declaration; read defaults/restrictions in original',line_no)
    for item in args.help_log:
        identifier,filename=item.split('=',1)
        matches=[t for t in tools if t['id']==identifier]
        if len(matches)!=1:ap.error('Help-log tool must identify exactly one inventory entry')
        tool=matches[0];p=Path(filename)
        add(tool,'driver-usage','driver-help',p,'Captured local driver help')
        for line_no,line in enumerate(p.read_text(errors='replace').splitlines(),1):
            m=re.match(r'^\s*(--?[A-Za-z][A-Za-z0-9_-]*)(?:\s|\[|,|\||$)',line)
            if m:add(tool,m.group(1),'driver-option',p,line.strip(),line_no)
    con.commit();total=con.execute('SELECT count(*) FROM docs').fetchone()[0];con.close()
    print(json.dumps({'added':count,'total_entries':total}))


if __name__=='__main__':main()
