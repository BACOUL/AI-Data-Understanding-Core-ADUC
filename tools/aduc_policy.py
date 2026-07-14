#!/usr/bin/env python3
"""Deterministic reference evaluator for ADUC Policy Profile 0.1."""

from __future__ import annotations
import argparse,copy,hashlib,json,re
from datetime import datetime,timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]; DEFAULT=ROOT/"examples"/"policy"
HEX=re.compile(r"^[0-9a-f]{64}$"); AUTH={"inferred":0,"reviewed":1,"verified":2,"canonical":3}
EXEC={"permission","prohibition","duty"}; HUMAN={"recommendation","legalNotice","classification"}
ODRL="http://www.w3.org/ns/odrl/2/"; ADUC="urn:aduc:term:"

def load(p:Path)->Any:return json.loads(p.read_text(encoding="utf-8"))
def iri(v:Any)->bool:return isinstance(v,str) and bool(urlparse(v).scheme)
def E(c:str,m:str)->dict[str,str]:return {"code":c,"message":m}
def tm(v:str)->datetime:
    x=v[:-1]+"+00:00" if isinstance(v,str) and v.endswith("Z") else v
    d=datetime.fromisoformat(x)
    if d.tzinfo is None:raise ValueError
    return d.astimezone(timezone.utc)

def registry(ref:Any,base:Path):
    if not isinstance(ref,dict) or not isinstance(ref.get("path"),str) or not HEX.fullmatch(str(ref.get("sha256",""))):
        return None,[E("ADUC-POL-VOCAB-001","pinned registry required")]
    p=(base/ref["path"]).resolve()
    try:p.relative_to(base.resolve())
    except ValueError:return None,[E("ADUC-POL-VOCAB-001","unsafe registry path")]
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=ref["sha256"]:
        return None,[E("ADUC-POL-VOCAB-001","registry unavailable or changed")]
    r=load(p)
    if r.get("registryId")!=ref.get("registryId") or r.get("registryVersion")!=ref.get("registryVersion"):
        return None,[E("ADUC-POL-VOCAB-001","registry identity mismatch")]
    return r,[]

def vrequest(q:Any,r:dict)->list[dict[str,str]]:
    e=[]
    if not isinstance(q,dict):return [E("ADUC-POL-REQUEST-001","request required")]
    for k in ("target","requester","recipient","action","purpose","spatial","environment"):
        if not iri(q.get(k)):e.append(E("ADUC-POL-REQUEST-001",f"{k} must be IRI"))
    if not HEX.fullmatch(str(q.get("targetDigest",""))):e.append(E("ADUC-POL-TARGET-002","request digest required"))
    if q.get("action") not in r.get("actions",{}):e.append(E("ADUC-POL-ACTION-002","unknown request action"))
    if q.get("purpose") not in r.get("purposes",{}):e.append(E("ADUC-POL-PURPOSE-002","unknown request purpose"))
    if q.get("environment") not in r.get("environments",{}):e.append(E("ADUC-POL-SCOPE-002","unknown environment"))
    try:tm(q.get("at"))
    except Exception:e.append(E("ADUC-POL-SCOPE-002","invalid request time"))
    if not isinstance(q.get("evidence",[]),list) or not all(iri(x) for x in q.get("evidence",[])):
        e.append(E("ADUC-POL-EVIDENCE-001","invalid request evidence"))
    return e

def vpolicy(p:Any,objs:Any,ev:Any,r:dict):
    e=[]
    if not isinstance(p,dict):return None,[E("ADUC-POL-DOC-001","policy required")]
    if not isinstance(objs,dict):return None,[E("ADUC-POL-TARGET-001","object table required")]
    if not isinstance(ev,dict):return None,[E("ADUC-POL-EVIDENCE-001","evidence table required")]
    pid,t=p.get("id"),p.get("target")
    if not iri(pid):e.append(E("ADUC-POL-DOC-001","policy id must be IRI"))
    if not iri(t) or t not in objs:e.append(E("ADUC-POL-TARGET-001","target not bound"))
    elif objs[t].get("kind") not in {"resource","version"}:e.append(E("ADUC-POL-TARGET-001","invalid target kind"))
    dg=p.get("targetDigest")
    if not HEX.fullmatch(str(dg or "")):e.append(E("ADUC-POL-TARGET-002","target digest required"))
    elif t in objs and objs[t].get("digest")!=dg:e.append(E("ADUC-POL-TARGET-002","target digest mismatch"))
    if p.get("mode") not in r.get("policyModes",[]):e.append(E("ADUC-POL-DOC-001","invalid mode"))
    if p.get("disclosure") not in r.get("disclosureStates",[]):e.append(E("ADUC-POL-STATE-001","invalid disclosure"))
    if p.get("auth") not in AUTH:e.append(E("ADUC-POL-AUTH-001","invalid authority"))
    for k in ("method","prov","by"):
        if not iri(p.get(k)):e.append(E("ADUC-POL-AUTH-001",f"{k} must be IRI"))
    pe=p.get("evidence")
    if not isinstance(pe,list) or not pe or not all(iri(x) and x in ev for x in pe):
        e.append(E("ADUC-POL-EVIDENCE-001","bound policy evidence required"))
    if p.get("auth")=="inferred":
        c=p.get("confidence")
        if not isinstance(c,(int,float)) or isinstance(c,bool) or not 0<=c<=1 or not iri(p.get("confidenceMethod")):
            e.append(E("ADUC-POL-AUTH-002","calibrated confidence required"))
    if p.get("conflict","clear") not in {"clear","contested"} or p.get("life","active") not in {"active","deprecated"}:
        e.append(E("ADUC-POL-STATE-001","invalid conflict or lifecycle"))
    v=p.get("valid")
    try:
        if not isinstance(v,dict) or tm(v["start"])>=tm(v["end"]):raise ValueError
    except Exception:e.append(E("ADUC-POL-SCOPE-002","invalid validity interval"))
    s=p.get("supersedes")
    if s is not None and (not iri(s) or s==pid):e.append(E("ADUC-POL-COMPOSE-001","invalid supersedes"))
    inh=p.get("inheritsFrom",[])
    if inh:
        if not isinstance(inh,list) or not all(iri(x) and x!=pid for x in inh):e.append(E("ADUC-POL-COMPOSE-001","invalid inheritance"))
        if p.get("compositionState")!="resolved":e.append(E("ADUC-POL-COMPOSE-001","inheritance unresolved"))
        ce=p.get("compositionEvidence")
        if not isinstance(ce,list) or not ce or not all(iri(x) and x in ev for x in ce):
            e.append(E("ADUC-POL-COMPOSE-001","composition evidence required"))
    rules=p.get("rules")
    if not isinstance(rules,list):return None,e+[E("ADUC-POL-RULE-001","rules array required")]
    ids=[]; norm=[]
    for x in rules:
        if not isinstance(x,dict):e.append(E("ADUC-POL-RULE-001","rule object required"));continue
        rid,fx=x.get("id"),x.get("effect")
        if not iri(rid):e.append(E("ADUC-POL-RULE-001","rule id must be IRI"))
        else:ids.append(rid)
        if fx not in r.get("effects",[]):e.append(E("ADUC-POL-RULE-001","unsupported effect"))
        if fx in EXEC and x.get("machineEvaluable") is not True:e.append(E("ADUC-POL-RULE-002","executable rule not declared"))
        if fx in HUMAN and x.get("machineEvaluable") is not False:e.append(E("ADUC-POL-LEGAL-001","human statement made executable"))
        if fx in EXEC:
            a=x.get("action")
            if not iri(a):e.append(E("ADUC-POL-ACTION-001","action must be IRI"))
            elif a not in r.get("actions",{}):e.append(E("ADUC-POL-ACTION-002","unknown action"))
            elif fx in {"permission","prohibition"} and r["actions"][a].get("category")!="primary":e.append(E("ADUC-POL-ACTION-002","primary action required"))
            elif fx=="duty" and r["actions"][a].get("category")!="duty":e.append(E("ADUC-POL-DUTY-001","duty action required"))
            if not iri(x.get("assigner")):e.append(E("ADUC-POL-PARTY-001","assigner required"))
        ps=x.get("purposes",[])
        if fx in {"permission","prohibition"}:
            if not isinstance(ps,list) or not ps or not all(iri(z) for z in ps):e.append(E("ADUC-POL-PURPOSE-001","controlled purposes required"))
            elif not all(z in r.get("purposes",{}) for z in ps):e.append(E("ADUC-POL-PURPOSE-002","unknown purpose"))
        for k in ("assignee","recipient","spatial","environment"):
            if x.get(k) is not None and not iri(x.get(k)):e.append(E("ADUC-POL-PARTY-001" if k in {"assignee","recipient"} else "ADUC-POL-SCOPE-002",f"invalid {k}"))
        if x.get("environment") is not None and x["environment"] not in r.get("environments",{}):e.append(E("ADUC-POL-SCOPE-002","unknown rule environment"))
        if fx=="duty":
            if x.get("phase") not in {"preUse","postUse"}:e.append(E("ADUC-POL-DUTY-001","invalid duty phase"))
            if x.get("satisfied") is True and not x.get("satisfiedBy"):e.append(E("ADUC-POL-DUTY-002","satisfaction evidence required"))
            sb=x.get("satisfiedBy",[])
            if sb and (not isinstance(sb,list) or not all(iri(z) and z in ev for z in sb)):e.append(E("ADUC-POL-DUTY-002","invalid satisfaction evidence"))
        claim=x.get("claim")
        if claim in {"consent","legalCompliance","ownership"}:
            kind={"consent":"consent","legalCompliance":"legalAssessment","ownership":"ownership"}[claim]; ce=x.get("claimEvidence")
            if not isinstance(ce,list) or not ce or not all(iri(z) and z in ev and ev[z].get("kind")==kind and iri(ev[z].get("provenance")) for z in ce):
                e.append(E("ADUC-POL-CLAIM-001",f"{claim} evidence required"))
        norm.append(copy.deepcopy(x))
    if len(ids)!=len(set(ids)):e.append(E("ADUC-POL-RULE-003","duplicate rule id"))
    by={x.get("id"):x for x in norm if iri(x.get("id"))}
    for x in norm:
        refs=x.get("duties",[])
        if x.get("effect")=="permission" and refs and (not isinstance(refs,list) or not all(iri(z) and z in by and by[z].get("effect")=="duty" for z in refs)):
            e.append(E("ADUC-POL-DUTY-001","unresolved duty reference"))
    out=copy.deepcopy(p);out["rules"]=norm
    return out,e

def matches(x:dict,q:dict)->bool:
    return x.get("effect") in {"permission","prohibition"} and x.get("action")==q.get("action") and q.get("purpose") in x.get("purposes",[]) and (x.get("assignee") is None or x["assignee"]==q.get("requester")) and (x.get("recipient") is None or x["recipient"]==q.get("recipient")) and (x.get("spatial") is None or x["spatial"]==q.get("spatial")) and (x.get("environment") is None or x["environment"]==q.get("environment"))
def satisfied(x:dict,q:dict,ev:dict)->bool:
    refs=x.get("satisfiedBy",[]); qe=set(q.get("evidence",[]))
    if refs:return bool(set(refs)&qe)
    kind=x.get("requiredEvidenceKind")
    return bool(kind and any(ev.get(z,{}).get("kind")==kind for z in qe))

def export_policy(p:dict)->dict:
    g=[{"@id":p["id"],"@type":ODRL+"Policy",ODRL+"target":{"@id":p["target"]},ADUC+"targetDigest":p["targetDigest"],ADUC+"authorityLevel":p["auth"],ADUC+"disclosureState":p["disclosure"],ADUC+"policyMode":p["mode"],ADUC+"provenanceActivity":{"@id":p["prov"]}}]
    types={"permission":ODRL+"Permission","prohibition":ODRL+"Prohibition","duty":ODRL+"Duty","recommendation":ADUC+"Recommendation","legalNotice":ADUC+"LegalNotice","classification":ADUC+"Classification"}
    for x in sorted(p["rules"],key=lambda z:z["id"]):
        n={"@id":x["id"],"@type":types[x["effect"]]}
        if iri(x.get("action")):n[ODRL+"action"]={"@id":x["action"]}
        if iri(x.get("assigner")):n[ODRL+"assigner"]={"@id":x["assigner"]}
        if iri(x.get("assignee")):n[ODRL+"assignee"]={"@id":x["assignee"]}
        if x.get("purposes"):n[ADUC+"purpose"]=[{"@id":z} for z in sorted(x["purposes"])]
        if x.get("duties"):n[ODRL+"duty"]=[{"@id":z} for z in sorted(x["duties"])]
        g.append(n)
    return {"@graph":g}

def evaluate(c:dict,r:dict)->dict:
    ev=c.get("evidence",{});p,e=vpolicy(c.get("policy"),c.get("objects",{}),ev,r);q=c.get("request",{});e+=vrequest(q,r);act=c.get("act",{}).get("t")
    if p is None:return {"valid":False,"errors":e}
    if act=="export":
        return {"valid":False,"errors":e} if e else {"valid":True,"errors":[],"result":{"policies":1,"rules":len(p["rules"]),"jsonld":export_policy(p)}}
    if act!="evaluate":e.append(E("ADUC-POL-ACTION-003","unsupported harness action"))
    if e:return {"valid":False,"errors":e}
    if q["target"]!=p["target"]:return {"valid":True,"errors":[],"result":{"outcome":"notApplicable"}}
    if q["targetDigest"]!=p["targetDigest"]:return {"valid":False,"errors":[E("ADUC-POL-TARGET-002","target versions differ")]}
    if p.get("conflict","clear")!="clear" or p.get("life","active")!="active":return {"valid":True,"errors":[],"result":{"outcome":"requiresHumanReview","reason":"policyNotReliablyActive"}}
    if p["disclosure"]!="complete":return {"valid":True,"errors":[],"result":{"outcome":"requiresHumanReview","reason":"incompleteDisclosure"}}
    if AUTH[p["auth"]]<AUTH["reviewed"]:return {"valid":True,"errors":[],"result":{"outcome":"requiresHumanReview","reason":"insufficientAuthority"}}
    if not tm(p["valid"]["start"])<=tm(q["at"])<tm(p["valid"]["end"]):return {"valid":True,"errors":[],"result":{"outcome":"deny","reason":"policyOutsideValidity"}}
    hit=[x for x in p["rules"] if matches(x,q)];deny=[x for x in hit if x["effect"]=="prohibition"]
    if deny:return {"valid":True,"errors":[],"result":{"outcome":"deny","reason":"prohibition","ruleIds":sorted(x["id"] for x in deny)}}
    by={x["id"]:x for x in p["rules"] if iri(x.get("id"))}
    for permission in sorted((x for x in hit if x["effect"]=="permission"),key=lambda z:z["id"]):
        duties=[by[z] for z in permission.get("duties",[])]
        pre=sorted(x["id"] for x in duties if x.get("phase")=="preUse" and not satisfied(x,q,ev))
        if pre:return {"valid":True,"errors":[],"result":{"outcome":"deny","reason":"unsatisfiedPreUseDuty","dutyIds":pre}}
        post=sorted(x["id"] for x in duties if x.get("phase")=="postUse" and not satisfied(x,q,ev))
        out={"outcome":"permit","ruleId":permission["id"]}
        if post:out["outstandingDuties"]=post
        return {"valid":True,"errors":[],"result":out}
    if any(x.get("effect")=="legalNotice" for x in p["rules"]):return {"valid":True,"errors":[],"result":{"outcome":"requiresHumanReview","reason":"humanOnlyStatement"}}
    if p["mode"]=="closed":return {"valid":True,"errors":[],"result":{"outcome":"deny","reason":"closedPolicyDefault"}}
    return {"valid":True,"errors":[],"result":{"outcome":"indeterminate","reason":"noApplicableRule"}}

def patch(d:Any,ops:list[list[Any]])->Any:
    d=copy.deepcopy(d)
    for op,path,*rest in ops:
        t=d
        for k in path[:-1]:t=t[k]
        k=path[-1];v=rest[0] if rest else None
        if op=="set":t[k]=copy.deepcopy(v)
        elif op=="remove":t.pop(k,None) if isinstance(t,dict) else t.pop(k)
        elif op=="append":t[k].append(copy.deepcopy(v))
        else:raise ValueError(op)
    return d
def contains(a:Any,x:Any)->bool:
    if isinstance(x,dict):return isinstance(a,dict) and all(k in a and contains(a[k],v) for k,v in x.items())
    return a==x
def materialize(ref:dict,c:dict)->dict:return patch(ref["base"],c.get("patch",[]))
def run(rp:Path,ip:Path)->dict:
    ref,inv=load(rp),load(ip);reg,errs=registry(ref.get("registry"),rp.parent)
    if not reg:return {"ok":False,"referenceAccepted":0,"invalidRejected":0,"failures":errs}
    by={c["id"]:materialize(ref,c) for c in ref["cases"]};fail=[];ok=bad=0
    for c in ref["cases"]:
        a=evaluate(by[c["id"]],reg)
        if contains(a,c["expect"]):ok+=1
        else:fail.append({"id":c["id"],"actual":a,"expected":c["expect"]})
    for c in inv["cases"]:
        a=evaluate(patch(by[c["base"]],c["patch"]),reg);codes={x["code"] for x in a.get("errors",[])}
        if not a["valid"] and c["code"] in codes:bad+=1
        else:fail.append({"id":c["id"],"actual":a,"expectedCode":c["code"]})
    return {"ok":not fail,"referenceAccepted":ok,"invalidRejected":bad,"failures":fail}
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("reference",nargs="?",type=Path,default=DEFAULT/"reference-cases.json");p.add_argument("invalid",nargs="?",type=Path,default=DEFAULT/"invalid-cases.json");p.add_argument("--format",choices=["text","json"],default="text")
    a=p.parse_args();r=run(a.reference,a.invalid)
    print(json.dumps(r,indent=2,sort_keys=True) if a.format=="json" else f"Accepted {r['referenceAccepted']} reference cases.\nRejected {r['invalidRejected']} invalid cases.")
    return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
