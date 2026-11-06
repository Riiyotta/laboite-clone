#!/usr/bin/env python3
"""Content hash of the files the design policy is enforced by (R15).

    python3 extraction/policy_hash.py        # prints sha256:<hex>

verify_all.py recomputes this and fails when registry.manifest.json / policy/design-policy.json
carry a different value.
"""
import hashlib, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENFORCED_BY = ["tokens/llm/token-policy.json", "compatibility/graph.json", "schema/pagespec.schema.json", "schema/semantic_validate.py"]


def compute(repo=REPO):
    h = hashlib.sha256()
    for rel in ENFORCED_BY:
        h.update(rel.encode() + b"\0")
        with open(os.path.join(repo, rel), "rb") as f:
            h.update(f.read().replace(b"\r\n", b"\n"))
        h.update(b"\0")
    return "sha256:" + h.hexdigest()


if __name__ == "__main__":
    print(compute())
