#!/usr/bin/env python3
"""Extract candidate metrics with provenance; never establishes signoff closure."""
import argparse
import json
from pathlib import Path
import re
from execution import fingerprint


def extract(path, kind, unit):
    text=Path(path).read_text(errors='replace')
    metrics={}
    if kind=='area':
        values=re.findall(r'Total cell area:\s*([+\-\d.eE]+)',text)
        if values:
            metrics['cell_area_'+unit]=float(values[-1])
    elif kind=='timing':
        values=re.findall(r'\bslack\s*\((?:MET|VIOLATED)\)\s*([+\-\d.eE]+)',text)
        if values:
            metrics['worst_reported_slack_'+unit]=min(map(float,values))
    elif kind=='power':
        for label,key in [('Total Dynamic Power','dynamic_power_'),('Cell Leakage Power','leakage_power_')]:
            values=re.findall(re.escape(label)+r'\s*=\s*([+\-\d.eE]+)',text)
            if values:
                metrics[key+unit]=float(values[-1])
    return {'metrics':metrics,'report':str(Path(path).resolve()),'sha256':fingerprint(path),
            'unit_asserted_by_caller':unit,'scope':'candidate metrics in this report only; no coverage or signoff conclusion'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('report',type=Path);ap.add_argument('--kind',choices=['area','timing','power'],required=True)
    ap.add_argument('--unit',required=True,help='Read report/library units first; do not guess')
    args=ap.parse_args();result=extract(args.report,args.kind,args.unit)
    print(json.dumps(result,indent=2,allow_nan=False))
    raise SystemExit(0 if result['metrics'] else 2)


if __name__=='__main__':
    main()
