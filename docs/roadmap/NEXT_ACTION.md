# Next Action

## Single active task

Define and accept the ADUC policy and permitted-use profile before freezing the normative full-Core object model.

Create:

```text
docs/decisions/ADR-0013-policy-and-permitted-use.md
spec/POLICY_PROFILE_0_1.md
examples/policy/
tools/aduc_policy.py
tests/policy/
```

## Objective

Define how an ADUC contract communicates machine-readable use conditions without pretending that the Core can determine legal validity, consent, ownership, jurisdiction, fairness, or regulatory compliance by itself.

The profile must allow a consumer to answer:

```text
Is this requested purpose permitted?
Is the requester or recipient allowed?
Is a required duty satisfied?
Has the permission expired?
Does a prohibition or conflict block use?
Is the policy complete enough for automatic reliance?
```

## Completed dependencies

```text
ADR-0005  epistemic lifecycle
ADR-0006  source description and immutable binding
ADR-0007  units and deterministic conversion
ADR-0008  temporal semantics and timezone alignment
ADR-0009  entity identity and safe equivalence
ADR-0010  provenance and transformation lineage
ADR-0011  uncertainty and data quality
ADR-0012  general relation semantics
```

Every policy must bind its target through ADR-0006, identify parties through ADR-0009, use ADR-0008 for temporal validity, retain ADR-0010 provenance, preserve ADR-0005 authority/conflict/lifecycle, and avoid inventing relation semantics contrary to ADR-0012.

## Required decisions

1. reuse ODRL and relevant established vocabularies instead of creating a competing rights language;
2. distinguish permission, prohibition, duty, constraint, recommendation, legal notice, and descriptive classification;
3. define policy, rule, target, assigner, assignee, action, purpose, recipient, spatial scope, temporal scope, duty, remedy, consequence, evidence, provenance, authority, conflict, and lifecycle;
4. distinguish a machine-evaluable rule from a human-only legal statement;
5. define deterministic precedence and conflict behavior without claiming universal legal interpretation;
6. require explicit purpose identifiers instead of free-text purpose matching;
7. define recipient and requester identity requirements;
8. define temporal, territorial, organizational, and environment constraints;
9. define pre-use and post-use duties and how satisfaction evidence is linked;
10. preserve unknown, partial, redacted, contested, deprecated, and externally governed policy states;
11. define policy inheritance, composition, versioning, replacement, and target scope;
12. define safe consumer outcomes such as `permit`, `deny`, `notApplicable`, `indeterminate`, and `requiresHumanReview`;
13. ensure that absence of a permission does not automatically mean permission or prohibition unless the governing profile explicitly declares a closed policy mode;
14. define deterministic JSON-LD/RDF export and an offline evaluation subset.

## Required counterexamples

The specification must reject or block:

- treating a descriptive `public` classification as permission for every purpose;
- matching a free-text purpose to a controlled purpose identifier;
- allowing use after policy expiry;
- allowing an unidentified requester when a named assignee is required;
- ignoring a prohibition because a permission also exists;
- claiming consent without evidence and provenance;
- treating a legal notice as an executable permission;
- silently dropping attribution, deletion, reporting, or downstream-use duties;
- considering a duty satisfied without bound evidence;
- evaluating a redacted or incomplete policy as fully permissive;
- applying a policy to the wrong resource version;
- inventing jurisdictional or regulatory compliance;
- treating absence of a rule as permission in open policy mode;
- automatically using contested or deprecated policies;
- accepting local action or purpose labels as global identifiers.

## Scope boundary

Do not implement the normative full-Core object model, full-Core JSON Schema, compiler, review UI, registry service, MCP adapter, extensions, anticipation engine, or legal-advice system in this task.

## Completion test

An independent implementer must be able to:

1. represent a permission, prohibition, and duty for an exactly bound resource;
2. evaluate a request with purpose, requester, recipient, time, place, and environment;
3. return a deterministic permit, deny, indeterminate, not-applicable, or human-review outcome;
4. prove that required duties are or are not satisfied using bound evidence;
5. block expired, contested, incomplete, redacted, or misbound policies;
6. preserve provenance, authority, lifecycle, versioning, and replacement;
7. export qualifying policy records deterministically to JSON-LD/RDF.

## Cross-cutting adoption constraint

[`ADOPTION_AND_VALUE_VALIDATION.md`](ADOPTION_AND_VALUE_VALIDATION.md) remains mandatory. Do not implement the JSON/CSV compiler now.
