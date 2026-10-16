#!/usr/bin/env python3
"""Index and retrieve installed Synopsys documentation without copying manuals."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess
from html.parser import HTMLParser
from config import state_dir

ROOT = Path(__file__).resolve().parents[1]
DB = state_dir() / 'command_index.sqlite'


class PlainHTML(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in {'script','style'}: self.skip+=1
        if tag in {'p','div','br','li','h1','h2','h3','tr','pre'}: self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in {'script','style'} and self.skip: self.skip-=1
        if tag in {'p','div','li','h1','h2','h3','tr','pre'}: self.parts.append('\n')
    def handle_data(self,data):
        if not self.skip: self.parts.append(data)


def read_text(path):
    p = Path(path)
    if p.suffix == '.pdf':
        return subprocess.run(['pdftotext', '-layout', str(p), '-'],
                              capture_output=True, check=True, timeout=45).stdout.decode(errors='replace')
    data = gzip.open(p, 'rb').read() if p.suffix == '.gz' else p.read_bytes()
    s = data.decode(errors='replace')
    if p.suffix in {'.html','.htm'}:
        parser=PlainHTML();parser.feed(s);s=''.join(parser.parts)
    # Some manuals contain a stray backspace immediately after a newline.
    # A regex-only repeat would never consume it and would spin forever.
    output = []
    for ch in s:
        if ch == '\b':
            if output and output[-1] != '\n':
                output.pop()
        else:
            output.append(ch)
    return ''.join(output)


def build(inventory, output):
    if output.exists():
        raise ValueError('Refusing to overwrite an earlier command index; use a new --db path.')
    data = json.loads(inventory.read_text())
    output.parent.mkdir(parents=True,exist_ok=True)
    con = sqlite3.connect(output)
    con.execute('CREATE TABLE docs (id INTEGER PRIMARY KEY, tool TEXT, version TEXT, installation TEXT, name TEXT, kind TEXT, path TEXT, sha256 TEXT, description TEXT, effect TEXT, stages TEXT, availability TEXT)')
    con.execute('CREATE INDEX names ON docs(tool,version,name)')
    seen = set()
    for tool in data['tools']:
        root = Path(tool['documentation_root'] or tool['installation'])
        # Manuals from embedded ICC2/StarRC need their own doc roots, not parent products.
        for p in root.rglob('*'):
            if not p.is_file():
                continue
            parts = p.parts
            is_man = bool(re.search(r'/cat[1234n]/', str(p)))
            is_doc = p.suffix in {'.pdf', '.info'} or p.name.startswith('help_') or (p.suffix == '.gz' and p.name.endswith('.txt.gz'))
            if not (is_man or is_doc):
                continue
            key = (tool['id'], str(p))
            if key in seen:
                continue
            seen.add(key)
            kind = 'manual' if is_man else 'document'
            name = re.sub(r'\.[1234n](\.gz)?$', '', p.name) if is_man else p.name
            desc = ''
            availability = 'documented; execution availability not established'
            if is_man:
                s = read_text(p)
                match = re.search(r'\nNAME\s*\n(.*?)(?:\n\s*\n|\nSYNTAX)', s, re.S)
                desc = re.sub(r'\s+', ' ', match.group(1)).strip() if match else ''
                # A mention is a search hint, not a deprecation judgment.
                if re.search(r'deprecat|obsolete|no longer supported', s, re.I):
                    availability += '; contains lifecycle wording: read original restrictions'
            effect = 'query-candidate; verify manual' if name.startswith(('report_', 'get_', 'list_', 'query_', 'help', 'man', 'check_')) else 'unknown; read manual before execution'
            con.execute('INSERT INTO docs(tool,version,installation,name,kind,path,sha256,description,effect,stages,availability) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        (tool['id'], tool['directory_version'], tool['installation'], name, kind, str(p), hashlib.sha256(p.read_bytes()).hexdigest(), desc, effect, 'consult stage guide and manual prerequisites', availability))
    # Additional installed product manuals without a primary executable are discoverable.
    indexed_paths = {x[1] for x in seen}
    for inst in data['installations']:
        for pstr in inst['documentation']:
            p = Path(pstr)
            if pstr in indexed_paths:
                continue
            con.execute('INSERT INTO docs(tool,version,installation,name,kind,path,sha256,description,effect,stages,availability) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        (inst['product_directory'], inst['directory_version'], inst['directory'], p.name, 'document', pstr, hashlib.sha256(p.read_bytes()).hexdigest(), '', 'unknown', 'read original', 'documentation only'))
    con.commit()
    n = con.execute('SELECT count(*) FROM docs').fetchone()[0]
    con.close()
    print(json.dumps({'entries': n, 'index': str(output)}))


def search(db, tool=None, version=None, query='', kind=None, limit=30, installation=None):
    con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    con.row_factory = sqlite3.Row
    where, args = ['(name LIKE ? OR description LIKE ?)'], [f'%{query}%', f'%{query}%']
    for key, value in [('tool', tool), ('version', version), ('kind', kind), ('installation', installation)]:
        if value:
            where.append(f'{key}=?')
            args.append(value)
    rows = con.execute('SELECT * FROM docs WHERE ' + ' AND '.join(where) + ' ORDER BY (name=?) DESC,tool,version,name,path LIMIT ?', args + [query, limit]).fetchall()
    con.close()
    result = [dict(x) for x in rows]
    for row in result:
        registry = state_dir()/'validation/commands'/row['tool']/'commands.json'
        provenance = registry.parent/'invocation.json'
        if registry.exists() and provenance.exists():
            invocation = json.loads(provenance.read_text())
            if any(str(arg).startswith(row['installation']+'/') for arg in invocation['argv']):
                row['global_runtime_command_present'] = row['name'] in json.loads(registry.read_text())
                row['runtime_evidence'] = str(registry)
        row['manual_section'] = next((x for x in Path(row['path']).parts if re.fullmatch('cat[1234n]',x)), None)
    return result


def retrieve(db, identifier, start=None, lines=100, contains=None):
    con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    con.row_factory = sqlite3.Row
    row = con.execute('SELECT * FROM docs WHERE id=?', (identifier,)).fetchone()
    con.close()
    if row is None:
        raise ValueError('Unknown document id')
    p = Path(row['path'])
    if hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
        raise ValueError('Local document changed; rebuild the version index before use')
    text = read_text(p).splitlines()
    if start is None:
        start=max(1,(dict(row).get('start_line') or 1)-3)
    if start<1 or lines<1:
        raise ValueError('Start/line count must be positive')
    if contains:
        matches = [i for i, line in enumerate(text) if contains.lower() in line.lower()]
        if not matches:
            raise ValueError('Search text absent from document')
        start = max(1, matches[0] - 5)
    end = min(len(text), start - 1 + min(lines, 500))
    return dict(row), '\n'.join(f'{i+1}: {text[i]}' for i in range(start - 1, end))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db', type=Path, default=DB)
    sub = ap.add_subparsers(dest='command', required=True)
    p = sub.add_parser('build'); p.add_argument('--inventory', type=Path, default=state_dir() / 'tool_inventory.json')
    p = sub.add_parser('search'); p.add_argument('query', nargs='?', default=''); p.add_argument('--tool'); p.add_argument('--version'); p.add_argument('--installation'); p.add_argument('--kind'); p.add_argument('--limit', type=int, default=30)
    p = sub.add_parser('show'); p.add_argument('id', type=int); p.add_argument('--start', type=int); p.add_argument('--lines', type=int, default=100); p.add_argument('--contains')
    args = ap.parse_args()
    if args.command == 'build':
        build(args.inventory, args.db)
    elif args.command == 'search':
        print(json.dumps(search(args.db, args.tool, args.version, args.query, args.kind, args.limit, args.installation), indent=2))
    else:
        row, content = retrieve(args.db, args.id, args.start, args.lines, args.contains)
        print(json.dumps(row)); print(content)


if __name__ == '__main__':
    main()
