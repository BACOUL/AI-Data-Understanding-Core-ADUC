from __future__ import annotations
import importlib.util, json, subprocess, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TOOL=ROOT/"tools"/"aduc_relations.py"
EXAMPLES=ROOT/"examples"/"relations"
spec=importlib.util.spec_from_file_location("aduc_relations",TOOL)
assert spec and spec.loader
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class RelationProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ref=json.loads((EXAMPLES/"reference-cases.json").read_text())
        cls.inv=json.loads((EXAMPLES/"invalid-cases.json").read_text())
        cls.byid={c["id"]:c for c in cls.ref["cases"]}
        cls.reg,_=module.registry(cls.ref["registry"],EXAMPLES)
        cls.defaults=cls.ref["defaults"]
        cls.bad={s["id"]:module.patch(cls.byid[s["base"]],s["patch"]) for s in cls.inv["cases"]}

    def test_suites(self):
        r=module.run(EXAMPLES/"reference-cases.json",EXAMPLES/"invalid-cases.json")
        self.assertTrue(r["ok"],r["failures"])
        self.assertEqual(r["referenceAccepted"],13)
        self.assertEqual(r["invalidRejected"],20)

    def test_inverse_requires_authority(self):
        good=module.evaluate(self.byid["inverse-part"],self.reg,self.defaults)
        bad=module.evaluate(self.bad["reverse-dependency"],self.reg,self.defaults)
        self.assertEqual(good["result"]["p"],"urn:aduc:predicate:hasStrictPart")
        self.assertIn("ADUC-REL-INF-001",{e["code"] for e in bad["errors"]})

    def test_close_match_is_not_exact(self):
        r=module.evaluate(self.bad["close-as-exact"],self.reg,self.defaults)
        self.assertIn("ADUC-REL-SEM-001",{e["code"] for e in r["errors"]})

    def test_skos_closure_uses_transitive_superproperty(self):
        r=module.evaluate(self.byid["broader-closure"],self.reg,self.defaults)
        self.assertEqual(r["result"]["p"],"http://www.w3.org/2004/02/skos/core#broaderTransitive")

    def test_open_world_and_explicit_negative(self):
        self.assertEqual(module.evaluate(self.byid["unknown"],self.reg,self.defaults)["result"]["truth"],"unknown")
        self.assertEqual(module.evaluate(self.byid["negative"],self.reg,self.defaults)["result"]["truth"],"false")

    def test_causation_is_not_inferred(self):
        r=module.evaluate(self.bad["correlation-causation"],self.reg,self.defaults)
        self.assertIn("ADUC-REL-CAUSE-001",{e["code"] for e in r["errors"]})

    def test_graph_integrity(self):
        for case,code in [("functional-conflict","ADUC-REL-CONFLICT-001"),("exact-broad-conflict","ADUC-REL-CONFLICT-003"),("part-cycle","ADUC-REL-CYCLE-001")]:
            with self.subTest(case=case):
                r=module.evaluate(self.bad[case],self.reg,self.defaults)
                self.assertIn(code,{e["code"] for e in r["errors"]})

        inferred=module.patch(self.byid["dependency"],[["set",["a",0,"auth"],"inferred"]])
        r=module.evaluate(inferred,self.reg,self.defaults)
        self.assertIn("ADUC-REL-AUTH-002",{e["code"] for e in r["errors"]})

        contradiction=module.patch(self.byid["dependency"],[
            ["set",["a",0,"auth"],"canonical"],
            ["append",["a"],{"id":"urn:rel:not-dep","s":"urn:r:a","p":"urn:aduc:predicate:dependsOn","o":"urn:s:b","pol":"negative","auth":"canonical"}]
        ])
        r=module.evaluate(contradiction,self.reg,self.defaults)
        self.assertIn("ADUC-REL-CONFLICT-004",{e["code"] for e in r["errors"]})

    def test_scope_and_lifecycle(self):
        for case,code in [("outside-time","ADUC-REL-SCOPE-001"),("outside-context","ADUC-REL-SCOPE-001"),("contested-use","ADUC-REL-LIFE-001"),("deprecated-use","ADUC-REL-LIFE-001")]:
            with self.subTest(case=case):
                r=module.evaluate(self.bad[case],self.reg,self.defaults)
                self.assertIn(code,{e["code"] for e in r["errors"]})

    def test_export_is_deterministic(self):
        a=module.evaluate(self.byid["export"],self.reg,self.defaults)
        b=module.evaluate(self.byid["export"],self.reg,self.defaults)
        self.assertEqual(a["result"]["jsonld"],b["result"]["jsonld"])
        self.assertEqual(a["result"]["statements"],2)
        self.assertEqual(a["result"]["triples"],2)

    def test_cli(self):
        c=subprocess.run([sys.executable,str(TOOL),str(EXAMPLES/"reference-cases.json"),str(EXAMPLES/"invalid-cases.json"),"--format","json"],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(c.returncode,0,c.stderr)
        r=json.loads(c.stdout);self.assertTrue(r["ok"]);self.assertEqual(r["referenceAccepted"],13);self.assertEqual(r["invalidRejected"],20)

if __name__=="__main__":unittest.main()
