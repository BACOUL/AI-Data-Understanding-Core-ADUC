#!/usr/bin/env python3
import json
import sys

sys.stdout.write(json.dumps({"adapterProtocol": "urn:aduc:full-core-conformance-adapter:0.1"}) + "\n")
