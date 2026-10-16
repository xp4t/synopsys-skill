import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from execution import execute
from flow import load_manifest


class PortabilityTests(unittest.TestCase):
    def test_execute_uses_existing_environment_without_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with patch('execution.subprocess.Popen', wraps=__import__('subprocess').Popen) as call:
                result=execute(sys.executable,['-c','print("ready")'],root/'run',5)
            self.assertTrue(result['process_ok'])
            self.assertEqual(call.call_args.args[0][0],sys.executable)

    def test_manifest_paths_are_relative_to_manifest_and_tool_uses_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'top.v').write_text('module top;endmodule')
            (root/'design.sdc').write_text('# supplied constraints')
            (root/'stage.py').write_text('print("ok")')
            m={'design':'top','top':'top','rtl':['top.v'],'sdc':'design.sdc','requirements':{'clock_period_ns':1},
               'tools':{'python':{'executable':'${PYTHON}'}},'stages':[{'id':'rtl','tool':'python','script':'stage.py'}]}
            p=root/'flow.json';p.write_text(json.dumps(m));loaded=load_manifest(p)
            self.assertEqual(loaded['rtl'],[str(root/'top.v')])
            self.assertEqual(loaded['tools']['python']['executable'],sys.executable)

    def test_missing_environment_input_is_not_silently_replaced(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'flow.json'
            p.write_text(json.dumps({'rtl':['${SNPS_UNSET_TEST_INPUT}'],'stages':[]}))
            with patch.dict(os.environ,{},clear=True),self.assertRaises(ValueError):load_manifest(p)

    def test_license_configuration_is_not_written_to_invocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            endpoint='27000@'+'private-server'
            with patch.dict(os.environ,{'SNPSLMD_LICENSE_FILE':endpoint}):
                execute(sys.executable,['-c','pass'],Path(tmp)/'run',5)
            self.assertNotIn(endpoint,(Path(tmp)/'run/invocation.json').read_text())


if __name__=='__main__':unittest.main()
