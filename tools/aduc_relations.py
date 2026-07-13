#!/usr/bin/env python3
"""Reference evaluator for ADUC Relation Profile 0.1."""

from __future__ import annotations
import argparse, copy, hashlib, json, re, sys
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
DEFAULT=ROOT/"examples"/"relations"
HEX=re.compile(r"^[0-9a-f]{64}$")
AUTH={"inferred":0,"reviewed":1,"verified":2,"canonical":3}
KINDS={"resource","field","concept","entity","assertion","activity","version","result"}
RDF="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
ADUC="urn:aduc:term:"

def load(p:Path)->Any:return json.loads(p.read_text(encoding="utf-8"))
def iri(v:Any)->bool:return isinstance(v,str) and bool(urlparse(v).scheme)
def error(c:str,m:str)->dict[str,str]:return {"code":c,"message":m}
def time(v:str)->datetime:
    x=v[:-1]+"+00:00" if isinstance(v,str) and v.endswith("Z") else v
    d=datetime.fromisoformat(x)
    if d.tzinfo is None:raise ValueError("offset required")
    return d.astimezone(timezone.utc)

def registry(ref:Any,base:Path)->tuple[dict[str,Any]|None,list[dict[str,str]]]:
    if not isinstance(ref,dict) or not isinstance(ref.get("path"),str) or not HEX.fullmatch(str(ref.get("sha256",""))):
        return None,[error("ADUC-REL-VOCAB-001","pinned registry reference required")]
    p=(base/ref["path"]).resolve()
    try:p.relative_to(base.resolve())
    except ValueError:return None,[error("ADUC-REL-VOCAB-001","unsafe registry path")]
    if not p.exists():return None,[error("ADUC-REL-VOCAB-001","registry unavailable")]
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    if actual!=ref["sha256"]:return None,[error("ADUC-REL-VOCAB-001","registry digest mismatch")]
    r=load(p)
    if r.get("registryId")!=ref.get("registryId") or r.get("registryVersion")!=ref.get("registryVersion"):
        return None,[error("ADUC-REL-VOCAB-001","registry identity mismatch")]
    return r,[]

def expand(a:dict[str,Any],defaults:dict[str,Any])->dict[str,Any]:
    d={**defaults,**a}
    return {
      "relationId":d.get("id"),"subject":{"binding":d.get("s")},"predicate":d.get("p"),
      "object":{"literal":d["lit"]} if "lit" in d else {"binding":d.get("o")},
      "polarity":d.get("pol","positive"),"method":d.get("method"),"provenanceActivity":d.get("prov"),
      "authorityLevel":d.get("auth"),"assertedBy":d.get("by"),"evidence":d.get("evidence"),
      "conflictState":d.get("conflict","clear"),"lifecycleState":d.get("life","active"),
      **({"validDuring":d["valid"]} if "valid" in d else {}),
      **({"contexts":d["ctx"]} if "ctx" in d else {}),
      **({"uncertaintyRef":d["u"]} if "u" in d else {}),
      **({"identityProfileRef":d["identity"]} if "identity" in d else {}),
      **({"epistemicConfidence":d.get("confidence",0.8),"confidenceMethod":d.get("confidenceMethod","urn:aduc:method:calibrated-relation-v1")} if d.get("auth")=="inferred" else {})
    }

def validate_assertion(a:dict[str,Any],objects:dict[str,str],r:dict[str,Any])->tuple[dict[str,Any]|None,list[dict[str,str]]]:
    e=[]
    if not iri(a.get("relationId")):e.append(error("ADUC-REL-DOC-001","relationId must be IRI"))
    p=a.get("predicate")
    if not iri(p):return None,e+[error("ADUC-REL-PRED-001","predicate must be IRI")]
    definition=r.get("predicates",{}).get(p)
    if not definition:return None,e+[error("ADUC-REL-PRED-002","predicate absent from registry")]
    if definition.get("assertionUse")=="inferenceOnly":e.append(error("ADUC-REL-PRED-003","inference-only predicate asserted"))
    s=a.get("subject",{}).get("binding")
    if not iri(s) or s not in objects:e.append(error("ADUC-REL-ENDPOINT-001","subject not bound"))
    elif objects[s] not in definition.get("subjectKinds",[]):e.append(error("ADUC-REL-ENDPOINT-002","subject kind not allowed"))
    raw_o=a.get("object",{}); o=None; lit=None
    if "binding" in raw_o:
        o=raw_o["binding"]
        if definition.get("objectMode")!="resource":e.append(error("ADUC-REL-ENDPOINT-003","resource used for literal property"))
        if not iri(o) or o not in objects:e.append(error("ADUC-REL-ENDPOINT-001","object not bound"))
        elif objects[o] not in definition.get("objectKinds",[]):e.append(error("ADUC-REL-ENDPOINT-002","object kind not allowed"))
    elif "literal" in raw_o:
        lit=raw_o["literal"]
        if definition.get("objectMode")!="literal":e.append(error("ADUC-REL-ENDPOINT-003","literal used for object relation"))
        if not isinstance(lit,dict) or "value" not in lit or bool(lit.get("datatype"))==bool(lit.get("language")):
            e.append(error("ADUC-REL-LIT-001","literal requires exactly one datatype or language"))
        elif lit.get("datatype") and not iri(lit["datatype"]):e.append(error("ADUC-REL-LIT-001","datatype must be IRI"))
    else:e.append(error("ADUC-REL-ENDPOINT-001","object missing"))
    auth=a.get("authorityLevel")
    if auth not in AUTH:e.append(error("ADUC-REL-AUTH-001","invalid authority"))
    for k in ("method","provenanceActivity","assertedBy"):
        if not iri(a.get(k)):e.append(error("ADUC-REL-AUTH-001",f"{k} must be IRI"))
    if not isinstance(a.get("evidence"),list) or not a["evidence"] or not all(iri(x) for x in a["evidence"]):
        e.append(error("ADUC-REL-AUTH-001","evidence required"))
    if auth=="inferred" and (not isinstance(a.get("epistemicConfidence"),(int,float)) or not iri(a.get("confidenceMethod"))):
        e.append(error("ADUC-REL-AUTH-002","inferred relation requires calibrated confidence"))
    minimum=definition.get("minimumAuthority")
    if minimum and auth in AUTH and AUTH[auth]<AUTH[minimum]:e.append(error("ADUC-REL-ID-001","insufficient identity authority"))
    if definition.get("requiresIdentityProfile") and not iri(a.get("identityProfileRef")):
        e.append(error("ADUC-REL-ID-001","identity profile required"))
    if a.get("polarity","positive") not in {"positive","negative"}:e.append(error("ADUC-REL-DOC-001","invalid polarity"))
    valid=a.get("validDuring")
    if valid:
        try:
            if time(valid["start"])>=time(valid["end"]):raise ValueError("invalid bounds")
        except Exception:e.append(error("ADUC-REL-SCOPE-002","invalid temporal scope"))
    ctx=a.get("contexts",[])
    if ctx and (not isinstance(ctx,list) or not all(iri(x) for x in ctx)):e.append(error("ADUC-REL-SCOPE-002","invalid contexts"))
    n={"id":a.get("relationId"),"s":s,"p":p,"o":o if o is not None else lit,"pol":a.get("polarity","positive"),
       "auth":auth,"conflict":a.get("conflictState","clear"),"life":a.get("lifecycleState","active"),
       "valid":valid,"ctx":ctx,"def":definition,"raw":a}
    return n,e

def usable(a:dict[str,Any],at:str|None=None,ctx:str|None=None)->list[dict[str,str]]:
    e=[]
    if a["conflict"]!="clear" or a["life"]!="active":e.append(error("ADUC-REL-LIFE-001","contested or deprecated relation"))
    if at and a["valid"]:
        try:
            if not time(a["valid"]["start"])<=time(at)<time(a["valid"]["end"]):e.append(error("ADUC-REL-SCOPE-001","outside temporal scope"))
        except Exception:e.append(error("ADUC-REL-SCOPE-001","invalid evaluation instant"))
    if ctx and a["ctx"] and ctx not in a["ctx"]:e.append(error("ADUC-REL-SCOPE-001","outside contextual scope"))
    return e

def graph_errors(items:list[dict[str,Any]],r:dict[str,Any])->list[dict[str,str]]:
    e=[]; ids=[x["id"] for x in items]
    if len(ids)!=len(set(ids)):e.append(error("ADUC-REL-DOC-001","duplicate relationId"))
    live=[x for x in items if x["conflict"]=="clear" and x["life"]=="active" and isinstance(x["o"],str)]
    byp=defaultdict(list)
    for x in live:byp[x["p"]].append(x)
    for p,xs in byp.items():
        c=r["predicates"][p].get("characteristics",{})
        if c.get("functional"):
            m=defaultdict(set)
            for x in xs:
                if x["pol"]=="positive":m[x["s"]].add(x["o"])
            if any(len(v)>1 for v in m.values()):e.append(error("ADUC-REL-CONFLICT-001","functional conflict"))
        if c.get("inverseFunctional"):
            m=defaultdict(set)
            for x in xs:
                if x["pol"]=="positive":m[x["o"]].add(x["s"])
            if any(len(v)>1 for v in m.values()):e.append(error("ADUC-REL-CONFLICT-002","inverse-functional conflict"))
        if c.get("acyclic"):
            g=defaultdict(list)
            for x in xs:
                if x["pol"]=="positive":g[x["s"]].append(x["o"])
            visiting=set(); done=set()
            def cyc(n):
                if n in visiting:return True
                if n in done:return False
                visiting.add(n)
                if any(cyc(z) for z in g[n]):return True
                visiting.remove(n);done.add(n);return False
            if any(cyc(n) for n in list(g)):e.append(error("ADUC-REL-CYCLE-001","cycle in acyclic predicate"))
    pairs=defaultdict(set)
    for x in live:
        if x["pol"]=="positive":pairs[(x["s"],x["o"])].add(x["p"])
    for pair,ps in pairs.items():
        if any(set(r["predicates"][p].get("disjointWith",[]))&ps for p in ps):
            e.append(error("ADUC-REL-CONFLICT-003","disjoint predicates on same pair"));break
    return e

def path(items,p,start,end):
    g=defaultdict(list)
    for x in items:
        if x["p"]==p and x["pol"]=="positive" and isinstance(x["o"],str) and not usable(x):g[x["s"]].append(x["o"])
    q=deque([(start,[start])]);seen={start}
    while q:
        n,trail=q.popleft()
        if n==end:return trail
        for z in sorted(g[n]):
            if z not in seen:seen.add(z);q.append((z,trail+[z]))
    return None

def export(items):
    graph=[];triples=0
    for x in sorted(items,key=lambda a:a["id"]):
        st={"@id":x["id"],"@type":RDF+"Statement",RDF+"subject":{"@id":x["s"]},RDF+"predicate":{"@id":x["p"]},
            ADUC+"authorityLevel":x["auth"],ADUC+"polarity":x["pol"],ADUC+"provenanceActivity":{"@id":x["raw"]["provenanceActivity"]}}
        if isinstance(x["o"],str):st[RDF+"object"]={"@id":x["o"]}
        else:
            v={"@value":x["o"]["value"]}
            v["@type" if "datatype" in x["o"] else "@language"]=x["o"].get("datatype",x["o"].get("language"))
            st[RDF+"object"]=v
        graph.append(st)
        if x["pol"]=="positive" and not usable(x):triples+=1
    return {"@graph":graph,"statements":len(items),"triples":triples}

def evaluate(case:dict[str,Any],reg:dict[str,Any],defaults:dict[str,Any])->dict[str,Any]:
    e=[]; objects=case.get("objects",{})
    if not isinstance(objects,dict) or not all(iri(k) and v in KINDS for k,v in objects.items()):
        return {"valid":False,"errors":[error("ADUC-REL-ENDPOINT-001","invalid object table")]}
    items=[]
    for raw in case.get("a",[]):
        n,found=validate_assertion(expand(raw,defaults),objects,reg);e+=found
        if n:items.append(n)
    e+=graph_errors(items,reg); byid={x["id"]:x for x in items}; act=case.get("act",{});t=act.get("t");result=None
    if t=="validate":
        for x in items:e+=usable(x)
        if not e:result={"usable":len(items)}
    elif t=="inverse":
        x=byid.get(act.get("id"))
        if not x:e.append(error("ADUC-REL-ACTION-001","relation missing"))
        else:
            e+=usable(x);inv=x["def"].get("inverseOf")
            if not inv:e.append(error("ADUC-REL-INF-001","no authoritative inverse"))
            elif isinstance(x["o"],str):result={"s":x["o"],"p":inv,"o":x["s"]}
    elif t=="transitive":
        p=act.get("p");d=reg["predicates"].get(p)
        out=p if d and d.get("characteristics",{}).get("transitive") else d.get("transitiveSuperproperty") if d else None
        if not out or not reg["predicates"].get(out,{}).get("characteristics",{}).get("transitive"):
            e.append(error("ADUC-REL-INF-002","no authoritative transitivity"))
        else:
            trail=path(items,p,act.get("from"),act.get("to"))
            if not trail or len(trail)<3:e.append(error("ADUC-REL-INF-002","no qualifying path"))
            else:result={"s":trail[0],"p":out,"o":trail[-1],"n":len(trail)-1}
    elif t=="exact":
        x=byid.get(act.get("id"))
        if not x or x["def"].get("exactness")!="exact":e.append(error("ADUC-REL-SEM-001","not exact"))
        else:result={"exact":True}
    elif t=="cause":e.append(error("ADUC-REL-CAUSE-001","relation does not establish causation"))
    elif t=="negativeFromAbsence":e.append(error("ADUC-REL-OPEN-001","absence is unknown, not false"))
    elif t=="evaluate":
        x=byid.get(act.get("id"))
        if not x:e.append(error("ADUC-REL-ACTION-001","relation missing"))
        else:
            e+=usable(x,act.get("at"),act.get("ctx"))
            if not e:result={"holds":True}
    elif t=="query":
        hits=[x for x in items if x["s"]==act.get("s") and x["p"]==act.get("p") and x["o"]==act.get("o") and not usable(x)]
        pol={x["pol"] for x in hits};result={"truth":"true" if pol=={"positive"} else "false" if pol=={"negative"} else "unknown"}
    elif t=="export":
        for x in items:e+=usable(x)
        if not e:
            out=export(items);result={"statements":out["statements"],"triples":out["triples"],"jsonld":out}
    else:e.append(error("ADUC-REL-ACTION-001","unsupported action"))
    out={"valid":not e,"errors":e}
    if result is not None:out["result"]=result
    if t=="validate" and not e:out["usable"]=len(items)
    return out

def patch(doc,ops):
    d=copy.deepcopy(doc)
    for operation in ops:
        op,path=operation[0],operation[1]
        val=operation[2] if len(operation)>2 else None
        target=d
        for k in path[:-1]:target=target[k]
        k=path[-1]
        if op=="set":target[k]=copy.deepcopy(val)
        elif op=="remove":target.pop(k,None) if isinstance(target,dict) else target.pop(k)
        elif op=="append":target[k].append(copy.deepcopy(val))
    return d

def contains(actual,expected):
    return all(k in actual and (contains(actual[k],v) if isinstance(v,dict) else actual[k]==v) for k,v in expected.items())

def run(reference:Path,invalid:Path)->dict[str,Any]:
    ref=load(reference); inv=load(invalid); reg,errs=registry(ref.get("registry"),reference.parent)
    if not reg:return {"ok":False,"referenceAccepted":0,"invalidRejected":0,"failures":errs}
    defaults=ref.get("defaults",{}); byid={c["id"]:c for c in ref["cases"]};fail=[];ok=bad=0
    for c in ref["cases"]:
        a=evaluate(c,reg,defaults)
        if contains(a,c["expect"]):ok+=1
        else:fail.append({"id":c["id"],"actual":a,"expected":c["expect"]})
    for s in inv["cases"]:
        c=patch(byid[s["base"]],s["patch"])
        if "registry" in c:
            r2,regerrs=registry(c["registry"],reference.parent)
            a={"valid":False,"errors":regerrs} if not r2 else evaluate(c,r2,defaults)
        else:a=evaluate(c,reg,defaults)
        if not a["valid"] and s["code"] in {x["code"] for x in a["errors"]}:bad+=1
        else:fail.append({"id":s["id"],"actual":a,"expectedCode":s["code"]})
    return {"ok":not fail,"referenceAccepted":ok,"invalidRejected":bad,"failures":fail}

def main()->int:
    p=argparse.ArgumentParser();p.add_argument("reference",nargs="?",type=Path,default=DEFAULT/"reference-cases.json")
    p.add_argument("invalid",nargs="?",type=Path,default=DEFAULT/"invalid-cases.json");p.add_argument("--format",choices=["text","json"],default="text")
    a=p.parse_args();r=run(a.reference,a.invalid)
    print(json.dumps(r,indent=2,sort_keys=True) if a.format=="json" else f"Accepted {r['referenceAccepted']} reference cases.\nRejected {r['invalidRejected']} invalid cases.")
    return 0 if r["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
