"""User-configurable paths; generated installation data stays outside source."""
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def state_dir():
    explicit=os.environ.get('SNPS_STATE_DIR')
    if explicit:return Path(explicit).expanduser().absolute()
    base=Path(os.environ.get('XDG_STATE_HOME',str(Path.home()/'.local/state')))
    return base/'synopsys-skills'
