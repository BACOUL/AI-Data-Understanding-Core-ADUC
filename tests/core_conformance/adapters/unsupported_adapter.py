#!/usr/bin/env python3
import json
import sys

ADAPTER_PROTOCOL = "urn:aduc:full-core-conformance-adapter:0.1"


def emit(payload):
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")


operation = sys.argv[1] if len(sys.argv) > 1 else "declareCapabilities"
if operation == "declareCapabilities":
    emit(
        {
            "adapterProtocol": ADAPTER_PROTOCOL,
            "operation": operation,
            "implementation": {"id": "urn:aduc:test:unsupported", "kind": "external"},
            "capabilities": {"validate": False, "compare": False, "format": False, "classes": []},
        }
    )
else:
    emit(
        {
            "adapterProtocol": ADAPTER_PROTOCOL,
            "operation": operation,
            "implementation": {"id": "urn:aduc:test:unsupported", "kind": "external"},
            "status": "unsupported",
        }
    )
