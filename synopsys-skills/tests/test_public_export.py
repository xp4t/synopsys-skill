import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from export_public import export_public, find_private_data


class PublicExportTests(unittest.TestCase):
    def test_export_omits_runtime_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'repo';root.mkdir();(root/'README.md').write_text('Public guide')
            private=root/'synopsys-skills/validation';private.mkdir(parents=True)
            (private/'console.log').write_text('private tool output')
            (root/'synopsys-skills/tool_inventory.json').write_text('{"private":true}')
            (root/'unreviewed.txt').write_text('private notes')
            out=Path(tmp)/'public';export_public(root,out)
            self.assertEqual([p.name for p in out.iterdir()],['README.md'])

    def test_export_rejects_personal_path_in_readme(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'repo';root.mkdir()
            (root/'README.md').write_text('/'+'/'.join(['home','private-account','project']))
            with self.assertRaises(ValueError):export_public(root,Path(tmp)/'public')

    def test_common_private_identifiers_are_detected_without_echoing_values(self):
        samples=['.'.join(['10','2','3','4']), '27000@'+'internal-host', 'person'+'@'+'example.test']
        for value in samples:
            findings=find_private_data(value)
            self.assertTrue(findings)
            self.assertNotIn(value,str(findings))

    def test_export_preserves_only_internal_relative_skill_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'repo';source=root/'synopsys-skills/skills/demo';source.mkdir(parents=True)
            (source/'SKILL.md').write_text('Public skill')
            links=root/'.agents/skills';links.mkdir(parents=True)
            (links/'demo').symlink_to('../../synopsys-skills/skills/demo')
            out=Path(tmp)/'public';export_public(root,out)
            self.assertTrue((out/'.agents/skills/demo').is_symlink())
            self.assertTrue((out/'.agents/skills/demo/SKILL.md').exists())

    def test_export_rejects_external_skill_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'repo';links=root/'.agents/skills';links.mkdir(parents=True)
            (links/'external').symlink_to(Path(tmp)/'private')
            with self.assertRaises(ValueError):export_public(root,Path(tmp)/'public')


if __name__=='__main__':unittest.main()
