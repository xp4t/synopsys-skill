import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from execution import execute, fingerprint, checkpoint, verify_checkpoint, classify, gds_integrity
from policy import compare, validate_change, validate_result
from flow import preflight, run_flow, protected_paths
from optimize import optimize
from docs import read_text, retrieve


class FrameworkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='snps-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def script(self, body, name='stage.py'):
        p = self.root / name
        p.write_text(body)
        return p

    def test_argv_preserves_metacharacters(self):
        p = self.script('import sys,json; print(json.dumps(sys.argv[1:]))')
        args = ['a b', '$HOME', '`touch SHOULD_NOT_EXIST`', 'x;y', 'a!b', 'a"b']
        result = execute(sys.executable, [str(p)] + args, self.root / 'run', 5)
        self.assertEqual(result['returncode'], 0)
        self.assertEqual(json.loads((self.root/'run/console.log').read_text()), args)
        self.assertFalse((self.root/'run/SHOULD_NOT_EXIST').exists())

    def test_zero_exit_error_is_failure(self):
        p = self.script('print("Error: unknown command frobnicate (CMD-005)")')
        result = execute(sys.executable, [str(p)], self.root/'run', 5)
        self.assertFalse(result['process_ok'])
        self.assertIn('invalid_command', result['failure_categories'])

    def test_executable_symlink_name_is_preserved(self):
        p=self.script('#!/bin/bash\nprintf "%s" "${0##*/}"\n','dispatcher')
        p.chmod(0o755)
        link=self.root/'dc_shell';link.symlink_to(p)
        result=execute(str(link),[],self.root/'run',2)
        self.assertEqual(result['returncode'],0)
        self.assertEqual((self.root/'run/console.log').read_text(),'dc_shell')

    def test_timeout_retained(self):
        p = self.script('import time; print("started",flush=True); time.sleep(20)')
        result = execute(sys.executable, [str(p)], self.root/'run', 0.2)
        self.assertTrue(result['timed_out'])
        self.assertIn('started', (self.root/'run/console.log').read_text())
        self.assertTrue((self.root/'run/execution.json').exists())

    def test_timeout_kills_descendant_group(self):
        p=self.script('import os,signal,subprocess,sys,time\nchild=subprocess.Popen([sys.executable,"-c",\'import signal,time; signal.signal(signal.SIGTERM,lambda *args:time.sleep(3));time.sleep(20)\'])\nprint(child.pid,flush=True)\ntime.sleep(20)\n')
        execute(sys.executable,[str(p)],self.root/'run',0.3)
        pid=int((self.root/'run/console.log').read_text().strip())
        import time
        time.sleep(0.03)
        status=Path('/proc')/str(pid)/'stat'
        if status.exists():
            self.assertEqual(status.read_text().split()[2],'Z')

    def test_run_directory_not_reused(self):
        execute('/bin/true', [], self.root/'run', 1)
        with self.assertRaises(FileExistsError):
            execute('/bin/true', [], self.root/'run', 1)

    def test_checkpoint_tampering_detected(self):
        p = self.script('original', 'design.ddc')
        record = checkpoint([p], self.root/'checkpoint')
        self.assertTrue(verify_checkpoint(record))
        (self.root/'checkpoint/design.ddc').write_text('changed')
        self.assertFalse(verify_checkpoint(record))

    def test_checkpoint_input_mutation_does_not_change_copy(self):
        p = self.script('original', 'design.ddc')
        record = checkpoint([p], self.root/'checkpoint')
        p.write_text('modified')
        self.assertTrue(verify_checkpoint(record))

    def test_gds_structure(self):
        p = self.root/'small.gds'
        p.write_bytes(bytes.fromhex('00060002025800040400'))
        self.assertTrue(gds_integrity(p)['structural_records_only'])
        p.write_bytes(bytes.fromhex('000600020258'))
        with self.assertRaises(ValueError):
            gds_integrity(p)

    def test_license_error_not_design_tuning(self):
        self.assertIn('license', classify('Error: Unable to checkout license for ICCompilerII'))
        with self.assertRaises(ValueError):
            validate_change({'parameter':'utilization','old':0.7,'new':0.6}, {'utilization':0.7},
                            {'utilization':{'min':0.4,'max':0.8}}, 'license')

    def test_hard_constraint_change_blocked(self):
        with self.assertRaises(ValueError):
            validate_change({'parameter':'clock_period_ns','old':1,'new':2}, {'clock_period_ns':1},
                            {'clock_period_ns':{'min':0.5,'max':3}}, 'timing')

    def test_stale_old_parameter_blocked(self):
        with self.assertRaises(ValueError):
            validate_change({'parameter':'utilization','old':0.9,'new':0.6}, {'utilization':0.7},
                            {'utilization':{'min':0.4,'max':0.8}}, 'congestion')

    def test_regression_reverts(self):
        policy={'objective':'area_um2','direction':'min','min_relative_improvement':0.01,
                'limits':{'wns_ns':{'min':0},'area_um2':{'max':100}},'guardrails':{'wns_ns':{'max_regression':0,'direction':'max'}}}
        self.assertEqual(compare({'area_um2':80,'wns_ns':0.1},{'area_um2':75,'wns_ns':-0.1},policy)['decision'],'revert')
        self.assertEqual(compare({'area_um2':80,'wns_ns':0.1},{'area_um2':75,'wns_ns':0.2},policy)['decision'],'keep')

    def test_nan_missing_metrics_cannot_pass(self):
        policy={'objective':'area_um2','direction':'min','limits':{'wns_ns':{'min':0}}}
        for candidate in [{'area_um2':10}, {'area_um2':10,'wns_ns':float('nan')}]:
            self.assertEqual(compare({'area_um2':20,'wns_ns':0},candidate,policy)['decision'],'revert')

    def test_nonfinite_optional_metric_cannot_pass_stage(self):
        (self.root/'report.rpt').write_text('report')
        with self.assertRaises(ValueError):
            validate_result({'status':'pass','checks':{'equivalence':True,'proof_coverage_clean':True},'reports':['report.rpt'],'metrics':{'area':float('nan')}},self.root,'formal',[],{})

    def test_document_overstrike_and_stray_backspace(self):
        p=self.script('NAME\n\bfoo f\bfoo\n','manual.2')
        self.assertEqual(read_text(p),'NAME\nfoo foo\n')

    def test_document_html_is_bounded_readable_content(self):
        p=self.script('<html><script>secret code</script><p>clock options</p></html>','manual.html')
        self.assertIn('clock options',read_text(p))
        self.assertNotIn('secret code',read_text(p))

    def test_guardrail_direction_cannot_be_guessed(self):
        p={'objective':'area_um2','guardrails':{'tns_ns':{'max_regression':0}}}
        self.assertEqual(compare({'area_um2':100,'tns_ns':0},{'area_um2':90,'tns_ns':-5},p)['decision'],'revert')

    def test_explicit_tns_guardrail_rejects_regression(self):
        p={'objective':'area_um2','guardrails':{'tns_ns':{'max_regression':0,'direction':'max'}}}
        self.assertEqual(compare({'area_um2':100,'tns_ns':0},{'area_um2':90,'tns_ns':-5},p)['decision'],'revert')

    def test_missing_formal_check_blocks(self):
        (self.root/'report.rpt').write_text('FAILED')
        result={'status':'pass','checks':{'equivalence':False},'reports':['report.rpt'],'metrics':{}}
        with self.assertRaises(ValueError):
            validate_result(result, self.root, 'formal', [], {})

    def test_false_string_is_not_true(self):
        (self.root/'report.rpt').write_text('FAILED')
        with self.assertRaises(ValueError):
            validate_result({'status':'pass','checks':{'equivalence':'true'},'reports':['report.rpt']},self.root,'formal',[],{})

    def test_empty_directory_cannot_be_report_evidence(self):
        (self.root/'reports').mkdir()
        with self.assertRaises(ValueError):
            validate_result({'status':'pass','checks':{'equivalence':True,'proof_coverage_clean':True},'reports':['reports']},self.root,'formal',[],{})

    def test_result_report_cannot_escape_attempt(self):
        (self.root/'report.rpt').write_text('report')
        attempt=self.root/'attempt';attempt.mkdir()
        with self.assertRaises(ValueError):
            validate_result({'status':'pass','checks':{'equivalence':True,'proof_coverage_clean':True},'reports':['../report.rpt']},attempt,'formal',[],{})

    def manifest(self):
        rtl=self.script('module top; endmodule', 'top.v')
        sdc=self.script('create_clock -period 1 [get_ports clk]', 'top.sdc')
        stage=self.script('import json,os\nfrom pathlib import Path\nPath("report.rpt").write_text("evidence")\nn=int(os.environ["SNPS_ATTEMPT"])\nif n==1:\n print("Error: License checkout failed")\nelse:\n Path("result.json").write_text(json.dumps({"status":"pass","checks":{"rtl_elaborated":True,"rtl_checked":True},"reports":["report.rpt"],"metrics":{}}))\n')
        return {'design':'toy','top':'top','rtl':[str(rtl)],'sdc':str(sdc),'requirements':{'clock_period_ns':1},
                'parameters':{},'allowed_parameters':{},'max_attempts':2,'license_retries':1,
                'stages':[{'id':'rtl','tool':'test','script':str(stage),'timeout_s':5}],
                'tools':{'test':{'executable':sys.executable,'script_option':None,'mode':'script'}}}

    def test_controlled_license_retry_retains_history(self):
        manifest=self.manifest()
        result=run_flow(manifest,self.root/'flow',partial=True)
        self.assertEqual(result['status'],'partial-stage-validated')
        self.assertEqual(len(result['attempts']),2)
        self.assertTrue((self.root/'flow/rtl/attempt-001/execution.json').exists())
        self.assertTrue((self.root/'flow/rtl/attempt-002/result.json').exists())

    def test_license_budget_exhaustion(self):
        manifest=self.manifest();manifest['license_retries']=0
        result=run_flow(manifest,self.root/'flow',partial=True)
        self.assertEqual(result['status'],'blocked')
        self.assertEqual(len(result['attempts']),1)

    def test_flow_wall_budget_bounds_stage(self):
        manifest=self.manifest();manifest['wall_budget_s']=0.01
        slow=self.script('import time;time.sleep(.2)','slow.py');manifest['stages'][0]['script']=str(slow)
        result=run_flow(manifest,self.root/'flow',partial=True)
        self.assertEqual(result['status'],'blocked')
        self.assertLess(result['elapsed_s'],0.2)

    def test_transitive_inputs_and_stage_scripts_are_protected(self):
        manifest=self.manifest();dep=self.script('cell model','cells.db');manifest['inputs']=[str(dep)]
        protected=protected_paths(manifest)
        self.assertIn(str(dep),protected)
        self.assertIn(manifest['stages'][0]['script'],protected)

    def test_retargeted_rtl_symlink_blocks_promotion(self):
        import threading,time
        manifest=self.manifest()
        declared=Path(manifest['rtl'][0]);original=declared.with_name('original.v');declared.rename(original);declared.symlink_to(original)
        other=self.script('module different;endmodule','other.v')
        good=self.script('import time,json\nfrom pathlib import Path\ntime.sleep(.15)\nPath("report.rpt").write_text("pass")\nPath("result.json").write_text(json.dumps({"status":"pass","checks":{"rtl_elaborated":True,"rtl_checked":True},"reports":["report.rpt"]}))','slow-good.py')
        manifest['stages'][0]['script']=str(good)
        def switch():
            time.sleep(.05);declared.unlink();declared.symlink_to(other)
        worker=threading.Thread(target=switch);worker.start()
        result=run_flow(manifest,self.root/'flow',partial=True);worker.join()
        self.assertEqual(result['status'],'blocked')

    def test_full_preflight_requires_clock_and_timing_limits(self):
        manifest=self.manifest();manifest['requirements']={'clock_period_ns':-1,'functional_reference':'example','corners':[],'hard_limits':{},'ir_em_required':False}
        errors=preflight(manifest,partial=False)
        self.assertTrue(any('positive' in e for e in errors))
        self.assertTrue(any('wns_ns' in e for e in errors))

    def test_optimization_reports_effective_recovery_parameters(self):
        manifest=self.manifest();manifest['parameters']={'utilization':.7}
        manifest['allowed_parameters']={'utilization':{'min':.4,'max':.8}}
        bad=self.script('print("Error: placement congestion")','bad.py')
        good=self.script('import json,os\nfrom pathlib import Path\nPath("report.rpt").write_text("metrics")\nPath("result.json").write_text(json.dumps({"status":"pass","checks":{"rtl_elaborated":True,"rtl_checked":True},"reports":["report.rpt"],"metrics":{"area":float(os.environ["SNPS_PARAM_utilization"])*100}}))','good.py')
        manifest['stages'][0]['script']=str(bad)
        manifest['stages'][0]['recovery_candidates']=[{'category':'congestion','reason':'test','documentation':[str(bad)],'changes':[{'parameter':'utilization','old':.7,'new':.6}],'script':str(good)}]
        result=optimize(manifest,{'metric_stage':'rtl','max_trials':0,'policy':{'objective':'area'}},self.root/'opt',partial=True)
        self.assertEqual(result['parameters']['utilization'],.6)
        self.assertEqual(result['metrics']['area'],60)

    def test_full_preflight_rejects_missing_physical_contract(self):
        errors=preflight(self.manifest(), partial=False)
        self.assertTrue(any('technology' in x for x in errors))

    def test_failed_formal_stops_floorplan(self):
        manifest=self.manifest()
        bad=self.script('import json\nfrom pathlib import Path\nPath("report.rpt").write_text("failed equivalence")\nPath("result.json").write_text(json.dumps({"status":"pass","checks":{"equivalence":False},"reports":["report.rpt"]}))','formal.py')
        sentinel=self.script('from pathlib import Path\nPath("UNSAFE").write_text("bad")','floorplan.py')
        manifest['stages']=[{'id':'formal','tool':'test','script':str(bad),'timeout_s':5},{'id':'floorplan','tool':'test','script':str(sentinel),'timeout_s':5}]
        result=run_flow(manifest,self.root/'flow',partial=True)
        self.assertEqual(result['status'],'blocked')
        self.assertFalse((self.root/'flow/floorplan').exists())


if __name__=='__main__':
    unittest.main()
