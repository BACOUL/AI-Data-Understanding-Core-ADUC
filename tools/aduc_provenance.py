#!/usr/bin/env python3
"""Validate ADUC provenance bundles and deterministic transformation-lineage claims."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLES = ROOT / "examples" / "provenance"

HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
AGENT_TYPES = {"person", "organization", "softwareAgent", "modelAgent"}
EXECUTION_MODES = {"deterministic", "nondeterministic", "manual", "externalAttestation", "reconstructed"}
LINEAGE_STATES = {"observed", "attested", "inferred", "partial", "redacted"}
AUTHORITY_LEVELS = {"inferred", "reviewed", "verified", "canonical"}
REPRO_CLAIMS = {"notClaimed", "deterministic", "replayable", "notReproducible"}
DISCLOSURE_STATES = {"complete", "partial", "redacted", "unknown"}
LIFECYCLE_STATES = {"active", "deprecated"}
CONFLICT_STATES = {"clear", "contested"}
DERIVATION_KINDS = {
    "derivation",
    "primarySource",
    "revision",
    "quotation",
    "aggregation",
    "normalization",
    "conversion",
    "resolution",
    "comparison",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def error(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def is_iri(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and bool(urlparse(value).scheme)


def valid_hash(value: Any) -> bool:
    return isinstance(value, str) and HASH_RE.fullmatch(value) is not None


def parse_instant(value: Any) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError("RFC 3339 instant is required")
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        result = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"invalid RFC 3339 instant: {value}") from exc
    if result.tzinfo is None:
        raise ValueError(f"timezone offset is required: {value}")
    return result.astimezone(timezone.utc)


def validate_authority(record: dict[str, Any], family: str = "ADUC-PROV-003") -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    authority = record.get("authorityLevel")
    if authority not in AUTHORITY_LEVELS:
        errors.append(error(family, "unsupported authorityLevel"))
    if not is_iri(record.get("assertedBy")):
        errors.append(error(family, "assertedBy must be an absolute IRI"))
    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(is_iri(item) for item in evidence):
        errors.append(error(family, "non-empty IRI evidence array is required"))
    if authority == "inferred":
        confidence = record.get("confidence")
        if (
            not isinstance(confidence, (int, float))
            or isinstance(confidence, bool)
            or not 0 <= confidence <= 1
        ):
            errors.append(error("ADUC-PROV-009", "inferred lineage requires confidence between 0 and 1"))
        if not is_iri(record.get("confidenceMethod")):
            errors.append(error("ADUC-PROV-009", "inferred lineage requires confidenceMethod"))
    elif record.get("confidence") is not None and authority == "canonical":
        errors.append(error("ADUC-PROV-009", "canonical lineage must not include numeric confidence"))
    return errors


def validate_disclosure(value: Any) -> tuple[dict[str, Any], list[dict[str, str]]]:
    if not isinstance(value, dict):
        return {}, [error("ADUC-DISC-001", "disclosure object is required")]
    errors: list[dict[str, str]] = []
    state = value.get("disclosureState")
    missing = value.get("missingSegments", [])
    redacted = value.get("redactedSegments", [])
    if state not in DISCLOSURE_STATES:
        errors.append(error("ADUC-DISC-001", "unsupported disclosureState"))
    if not isinstance(missing, list) or not all(isinstance(item, str) and item for item in missing):
        errors.append(error("ADUC-DISC-001", "missingSegments must be an array of non-empty strings"))
        missing = []
    if not isinstance(redacted, list) or not all(isinstance(item, str) and item for item in redacted):
        errors.append(error("ADUC-DISC-001", "redactedSegments must be an array of non-empty strings"))
        redacted = []
    if state == "complete" and (missing or redacted):
        errors.append(error("ADUC-DISC-001", "complete disclosure cannot contain missing or redacted segments"))
    if state == "partial" and not missing:
        errors.append(error("ADUC-DISC-001", "partial disclosure requires missingSegments"))
    if state == "redacted":
        if not redacted:
            errors.append(error("ADUC-DISC-001", "redacted disclosure requires redactedSegments"))
        if not is_iri(value.get("redactionPolicy")):
            errors.append(error("ADUC-DISC-002", "redacted disclosure requires redactionPolicy"))
    return value, errors


def validate_entities(value: Any) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    entities: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []
    if not isinstance(value, list):
        return entities, [error("ADUC-PROV-001", "entities must be an array")]
    for item in value:
        if not isinstance(item, dict):
            errors.append(error("ADUC-PROV-001", "entity must be an object"))
            continue
        entity_id = item.get("entityId")
        if not is_iri(entity_id) or not is_iri(item.get("entityType")):
            errors.append(error("ADUC-PROV-001", "entityId and entityType must be absolute IRIs"))
            continue
        if entity_id in entities:
            errors.append(error("ADUC-PROV-001", f"duplicate entityId: {entity_id}"))
            continue
        if not valid_hash(item.get("contentHash")):
            errors.append(error("ADUC-PROV-002", f"entity {entity_id} requires sha256 contentHash"))
        if not is_iri(item.get("sourceBinding")):
            errors.append(error("ADUC-PROV-002", f"entity {entity_id} requires sourceBinding"))
        if item.get("lifecycleState", "active") not in LIFECYCLE_STATES:
            errors.append(error("ADUC-PROV-001", f"unsupported lifecycleState for {entity_id}"))
        entities[entity_id] = item
    return entities, errors


def validate_agents(value: Any) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    agents: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []
    if not isinstance(value, list):
        return agents, [error("ADUC-PROV-001", "agents must be an array")]
    for item in value:
        if not isinstance(item, dict):
            errors.append(error("ADUC-PROV-001", "agent must be an object"))
            continue
        agent_id = item.get("agentId")
        agent_type = item.get("agentType")
        if not is_iri(agent_id) or agent_type not in AGENT_TYPES:
            errors.append(error("ADUC-PROV-001", "agentId must be an IRI and agentType must be supported"))
            continue
        if agent_id in agents:
            errors.append(error("ADUC-PROV-001", f"duplicate agentId: {agent_id}"))
            continue
        if not isinstance(item.get("name"), str) or not item.get("name"):
            errors.append(error("ADUC-PROV-003", f"agent {agent_id} requires name"))
        if agent_type in {"softwareAgent", "modelAgent"}:
            if not isinstance(item.get("version"), str) or not item.get("version"):
                errors.append(error("ADUC-REPRO-001", f"agent {agent_id} requires version"))
            if not valid_hash(item.get("buildDigest")):
                errors.append(error("ADUC-REPRO-001", f"agent {agent_id} requires buildDigest"))
        agents[agent_id] = item
    return agents, errors


def ref_list(value: Any, field: str, entities: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    errors: list[dict[str, str]] = []
    if not isinstance(value, list):
        return [], [error("ADUC-PROV-005", f"{field} must be an array")]
    result: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict) or item.get("entityId") not in entities:
            errors.append(error("ADUC-PROV-005", f"{field} references an unknown entity"))
            continue
        if not isinstance(item.get("role"), str) or not item.get("role"):
            errors.append(error("ADUC-PROV-003", f"{field} entry requires role"))
        result.append(item)
    return result, errors


def validate_activity(
    record: Any,
    entities: dict[str, dict[str, Any]],
    agents: dict[str, dict[str, Any]],
    disclosure_state: str | None,
) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    if not isinstance(record, dict):
        return None, [error("ADUC-PROV-001", "activity must be an object")]
    errors: list[dict[str, str]] = []
    activity_id = record.get("activityId")
    if not is_iri(activity_id):
        errors.append(error("ADUC-PROV-001", "activityId must be an absolute IRI"))
    if not isinstance(record.get("activityType"), str) or not record.get("activityType"):
        errors.append(error("ADUC-PROV-001", "activityType is required"))
    if not is_iri(record.get("method")):
        errors.append(error("ADUC-PROV-003", "activity method must be an absolute IRI"))
    try:
        started = parse_instant(record.get("startedAt"))
        ended = parse_instant(record.get("endedAt"))
        if ended < started:
            errors.append(error("ADUC-PROV-004", "activity end precedes start"))
    except ValueError as exc:
        errors.append(error("ADUC-PROV-004", str(exc)))

    mode = record.get("executionMode")
    state = record.get("lineageState")
    if mode not in EXECUTION_MODES:
        errors.append(error("ADUC-PROV-001", "unsupported executionMode"))
    if state not in LINEAGE_STATES:
        errors.append(error("ADUC-PROV-001", "unsupported lineageState"))
    errors.extend(validate_authority(record))
    if state == "inferred" and record.get("authorityLevel") != "inferred":
        errors.append(error("ADUC-PROV-009", "inferred lineage must use inferred authority"))
    if state == "attested" and mode != "externalAttestation":
        errors.append(error("ADUC-PROV-009", "attested lineage requires externalAttestation mode"))
    if mode == "reconstructed" and state not in {"inferred", "partial", "redacted"}:
        errors.append(error("ADUC-PROV-009", "reconstructed mode cannot claim observed lineage"))
    if record.get("conflictState", "clear") not in CONFLICT_STATES:
        errors.append(error("ADUC-PROV-001", "unsupported conflictState"))
    if record.get("lifecycleState", "active") not in LIFECYCLE_STATES:
        errors.append(error("ADUC-PROV-001", "unsupported lifecycleState"))

    associations = record.get("associatedAgents")
    associated: list[dict[str, Any]] = []
    if not isinstance(associations, list) or not associations:
        errors.append(error("ADUC-PROV-003", "activity requires at least one associated agent"))
    else:
        for association in associations:
            if (
                not isinstance(association, dict)
                or association.get("agentId") not in agents
                or not isinstance(association.get("role"), str)
                or not association.get("role")
            ):
                errors.append(error("ADUC-PROV-003", "invalid agent association or role"))
                continue
            associated.append(association)

    used, used_errors = ref_list(record.get("used", []), "used", entities)
    generated, generated_errors = ref_list(record.get("generated", []), "generated", entities)
    errors.extend(used_errors)
    errors.extend(generated_errors)
    if record.get("activityType") != "invalidation":
        if not used:
            errors.append(error("ADUC-PROV-005", "material activity requires at least one used entity"))
        if not generated:
            errors.append(error("ADUC-PROV-005", "material activity requires at least one generated entity"))

    claim = record.get("reproducibilityClaim", "notClaimed")
    if claim not in REPRO_CLAIMS:
        errors.append(error("ADUC-REPRO-001", "unsupported reproducibilityClaim"))

    if mode == "manual":
        manual = record.get("manualIntervention")
        if not isinstance(manual, dict) or not isinstance(manual.get("description"), str) or not manual.get("description"):
            errors.append(error("ADUC-REPRO-003", "manual activity requires disclosed manualIntervention"))
        if not any(agents[a["agentId"]].get("agentType") in {"person", "organization"} for a in associated):
            errors.append(error("ADUC-REPRO-003", "manual activity requires person or organization responsibility"))

    execution = record.get("execution")
    if claim == "deterministic":
        if mode != "deterministic":
            errors.append(error("ADUC-REPRO-001", "deterministic claim requires deterministic execution mode"))
        if state not in {"observed", "attested"}:
            errors.append(error("ADUC-REPRO-001", "deterministic claim requires observed or attested lineage"))
        if disclosure_state != "complete":
            errors.append(error("ADUC-REPRO-001", "deterministic claim requires complete disclosure"))
        if not isinstance(execution, dict):
            errors.append(error("ADUC-REPRO-001", "deterministic claim requires execution evidence"))
        else:
            software_id = execution.get("softwareAgent")
            if software_id not in agents or agents.get(software_id, {}).get("agentType") != "softwareAgent":
                errors.append(error("ADUC-REPRO-001", "deterministic execution requires softwareAgent"))
            for field in ("environmentDigest", "parametersDigest"):
                if not valid_hash(execution.get(field)):
                    errors.append(error("ADUC-REPRO-001", f"deterministic execution requires {field}"))
        if mode == "manual":
            errors.append(error("ADUC-REPRO-003", "manual activity cannot claim deterministic reproduction"))

    if record.get("activityType") == "modelInference" or claim == "replayable":
        ai = record.get("aiExecution")
        if not isinstance(ai, dict):
            errors.append(error("ADUC-REPRO-004", "model inference requires aiExecution evidence"))
        else:
            model_agent = ai.get("modelAgent")
            if model_agent not in agents or agents.get(model_agent, {}).get("agentType") != "modelAgent":
                errors.append(error("ADUC-REPRO-004", "aiExecution requires modelAgent"))
            if not is_iri(ai.get("modelIdentifier")):
                errors.append(error("ADUC-REPRO-004", "modelIdentifier must be an absolute IRI"))
            if not isinstance(ai.get("modelVersion"), str) or not ai.get("modelVersion"):
                errors.append(error("ADUC-REPRO-004", "modelVersion is required"))
            if not is_iri(ai.get("provider")):
                errors.append(error("ADUC-REPRO-004", "provider must be an absolute IRI"))
            prompt_entity = ai.get("promptEntity")
            if prompt_entity not in entities:
                errors.append(error("ADUC-REPRO-004", "promptEntity must reference a bound entity"))
            for field in ("parametersDigest", "environmentDigest"):
                if not valid_hash(ai.get(field)):
                    errors.append(error("ADUC-REPRO-004", f"aiExecution requires {field}"))
            if ai.get("toolsUsed") is True and not valid_hash(ai.get("toolConfigurationDigest")):
                errors.append(error("ADUC-REPRO-004", "toolsUsed requires toolConfigurationDigest"))
            if claim == "replayable" and not isinstance(ai.get("seed"), int):
                errors.append(error("ADUC-REPRO-002", "replayable model execution requires integer seed"))
        if claim == "replayable":
            if mode != "nondeterministic":
                errors.append(error("ADUC-REPRO-002", "replayable claim requires nondeterministic execution mode"))
            if disclosure_state != "complete":
                errors.append(error("ADUC-REPRO-002", "replayable claim requires complete disclosure"))

    if state in {"partial", "redacted"} and claim in {"deterministic", "replayable"}:
        errors.append(error("ADUC-DISC-001", "partial or redacted lineage cannot claim reproduction"))

    return record, errors


def detect_cycle(edges: dict[str, set[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for nxt in edges.get(node, set()):
            if visit(nxt):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in list(edges))


def evaluate_case(case: Any) -> dict[str, Any]:
    if not isinstance(case, dict):
        return {"valid": False, "traceable": False, "reproducibility": [], "errors": [error("ADUC-PROV-001", "case must be an object")], "warnings": []}

    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    if case.get("profileVersion") != "0.1" or not is_iri(case.get("bundleId")):
        errors.append(error("ADUC-PROV-001", "profileVersion 0.1 and bundleId IRI are required"))
    try:
        evaluation_at = parse_instant(case.get("evaluationAt"))
    except ValueError as exc:
        evaluation_at = datetime.min.replace(tzinfo=timezone.utc)
        errors.append(error("ADUC-PROV-004", str(exc)))

    disclosure, disclosure_errors = validate_disclosure(case.get("disclosure"))
    errors.extend(disclosure_errors)
    disclosure_state = disclosure.get("disclosureState")

    entities, entity_errors = validate_entities(case.get("entities"))
    agents, agent_errors = validate_agents(case.get("agents"))
    errors.extend(entity_errors)
    errors.extend(agent_errors)

    activities: dict[str, dict[str, Any]] = {}
    raw_activities = case.get("activities")
    if not isinstance(raw_activities, list):
        raw_activities = []
        errors.append(error("ADUC-PROV-001", "activities must be an array"))

    generated_by: dict[str, str] = {}
    activity_times: dict[str, tuple[datetime, datetime]] = {}
    edges: dict[str, set[str]] = {}
    reproduction: list[dict[str, str]] = []

    for raw in raw_activities:
        activity, activity_errors = validate_activity(raw, entities, agents, disclosure_state)
        errors.extend(activity_errors)
        if not activity or not isinstance(activity.get("activityId"), str):
            continue
        activity_id = activity["activityId"]
        if activity_id in activities:
            errors.append(error("ADUC-PROV-001", f"duplicate activityId: {activity_id}"))
            continue
        activities[activity_id] = activity
        try:
            start = parse_instant(activity.get("startedAt"))
            end = parse_instant(activity.get("endedAt"))
            activity_times[activity_id] = (start, end)
        except ValueError:
            pass
        used_ids = [item.get("entityId") for item in activity.get("used", []) if isinstance(item, dict)]
        generated_ids = [item.get("entityId") for item in activity.get("generated", []) if isinstance(item, dict)]
        for output in generated_ids:
            if output in generated_by and generated_by[output] != activity_id:
                errors.append(error("ADUC-PROV-007", f"entity {output} generated by multiple activities"))
            elif isinstance(output, str):
                generated_by[output] = activity_id
        for input_id in used_ids:
            if not isinstance(input_id, str):
                continue
            for output_id in generated_ids:
                if isinstance(output_id, str):
                    edges.setdefault(input_id, set()).add(output_id)
        reproduction.append({"activityId": activity_id, "claim": activity.get("reproducibilityClaim", "notClaimed")})

    raw_derivations = case.get("derivations", [])
    if not isinstance(raw_derivations, list):
        errors.append(error("ADUC-PROV-001", "derivations must be an array"))
        raw_derivations = []
    derivation_ids: set[str] = set()
    for record in raw_derivations:
        if not isinstance(record, dict):
            errors.append(error("ADUC-PROV-001", "derivation must be an object"))
            continue
        derivation_id = record.get("derivationId")
        if not is_iri(derivation_id) or derivation_id in derivation_ids:
            errors.append(error("ADUC-PROV-001", "derivationId must be unique absolute IRI"))
            continue
        derivation_ids.add(derivation_id)
        used = record.get("usedEntity")
        generated = record.get("generatedEntity")
        activity_id = record.get("activityId")
        if used not in entities or generated not in entities:
            errors.append(error("ADUC-PROV-005", "derivation endpoints must exist"))
            continue
        if record.get("kind") not in DERIVATION_KINDS:
            errors.append(error("ADUC-PROV-005", "unsupported derivation kind"))
        errors.extend(validate_authority(record))
        edges.setdefault(used, set()).add(generated)
        if activity_id is not None:
            activity = activities.get(activity_id)
            if activity is None:
                errors.append(error("ADUC-PROV-005", "derivation activity does not exist"))
            else:
                used_set = {item.get("entityId") for item in activity.get("used", []) if isinstance(item, dict)}
                generated_set = {item.get("entityId") for item in activity.get("generated", []) if isinstance(item, dict)}
                if used not in used_set or generated not in generated_set:
                    errors.append(error("ADUC-PROV-005", "derivation endpoints disagree with activity usage/generation"))

    if detect_cycle(edges):
        errors.append(error("ADUC-PROV-006", "provenance graph contains a cycle"))

    invalidated_at: dict[str, datetime] = {}
    raw_invalidations = case.get("invalidations", [])
    if not isinstance(raw_invalidations, list):
        errors.append(error("ADUC-PROV-001", "invalidations must be an array"))
        raw_invalidations = []
    invalidation_ids: set[str] = set()
    for record in raw_invalidations:
        if not isinstance(record, dict):
            errors.append(error("ADUC-PROV-008", "invalidation must be an object"))
            continue
        inv_id = record.get("invalidationId")
        entity_id = record.get("entityId")
        activity_id = record.get("activityId")
        if not is_iri(inv_id) or inv_id in invalidation_ids:
            errors.append(error("ADUC-PROV-008", "invalidationId must be unique absolute IRI"))
            continue
        invalidation_ids.add(inv_id)
        if entity_id not in entities or activity_id not in activities:
            errors.append(error("ADUC-PROV-008", "invalidation references unknown entity or activity"))
            continue
        errors.extend(validate_authority(record, "ADUC-PROV-008"))
        try:
            instant = parse_instant(record.get("invalidatedAt"))
            invalidated_at[entity_id] = instant
        except ValueError as exc:
            errors.append(error("ADUC-PROV-008", str(exc)))
            continue
        generator = generated_by.get(entity_id)
        if generator and generator in activity_times and instant < activity_times[generator][1]:
            errors.append(error("ADUC-PROV-008", "invalidation precedes entity generation"))

    for activity_id, activity in activities.items():
        if activity_id not in activity_times:
            continue
        start = activity_times[activity_id][0]
        for used in activity.get("used", []):
            if not isinstance(used, dict):
                continue
            entity_id = used.get("entityId")
            instant = invalidated_at.get(entity_id)
            if instant is not None and start >= instant:
                errors.append(error("ADUC-PROV-008", f"activity {activity_id} uses invalidated entity {entity_id}"))

    active_errors = [item for item in errors if item["code"]]
    if disclosure_state in {"partial", "redacted", "unknown"}:
        warnings.append(error("ADUC-DISC-001", f"lineage disclosure is {disclosure_state}"))
    if any(
        activity.get("conflictState") == "contested" or activity.get("lifecycleState") == "deprecated"
        for activity in activities.values()
    ):
        warnings.append(error("ADUC-PROV-009", "contested or deprecated lineage is present"))

    return {
        "valid": not active_errors,
        "traceable": not active_errors and bool(activities) and bool(entities),
        "disclosureState": disclosure_state,
        "reproducibility": reproduction,
        "errors": active_errors,
        "warnings": warnings,
        "evaluatedAt": evaluation_at.isoformat().replace("+00:00", "Z"),
    }


def format_text(results: list[tuple[str, dict[str, Any]]]) -> str:
    lines: list[str] = []
    for name, result in results:
        status = "VALID" if result["valid"] else "INVALID"
        lines.append(f"{name}: {status}")
        for item in result["errors"]:
            lines.append(f"  {item['code']}: {item['message']}")
        for item in result["warnings"]:
            lines.append(f"  warning {item['code']}: {item['message']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_EXAMPLES / "reference-cases.json")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    document = load_json(args.path)
    cases = document if isinstance(document, list) else [document]
    results: list[tuple[str, dict[str, Any]]] = []
    for index, case in enumerate(cases):
        name = case.get("caseId", f"case-{index + 1}") if isinstance(case, dict) else f"case-{index + 1}"
        results.append((str(name), evaluate_case(case)))

    if args.format == "json":
        print(json.dumps([{"caseId": name, **result} for name, result in results], indent=2, sort_keys=True))
    else:
        print(format_text(results))
    return 0 if all(result["valid"] for _, result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
