#!/usr/bin/env python3
"""Proves that verify_all.py catches drift: copies the repo to a scratch dir, injects one defect per case,
runs verify_all there and requires a FAIL mentioning the expected text; the untouched copy must pass.

    python3 extraction/prove_drift.py

The scratch copy gets symlinks to the sibling source (src/, public/, CLONE_SPEC_*.md, ...) when it exists,
so citation / copy-fidelity cases run too; without a sibling source those cases are reported SKIPPED.
Uses the OS temp directory (tempfile), never a hardcoded path.
"""
import json, os, re, shutil, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(REPO)
HAVE_SRC = os.path.isdir(os.path.join(ROOT, "src"))
LINK = ["src", "public", "CLONE_SPEC_A.md", "CLONE_SPEC_B.md", "CLONE_SPEC_A_ASSETS.md", "ia.json", "index.html", "README.md", "tailwind.config.js", "package.json"]


def jedit(rel, fn):
    def apply(repo):
        p = os.path.join(repo, rel)
        d = json.load(open(p, encoding="utf-8"))
        fn(d)
        json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return apply


def tedit(rel, old, new, count=1):
    def apply(repo):
        p = os.path.join(repo, rel)
        s = open(p, encoding="utf-8").read()
        assert old in s, f"{rel}: {old!r} not found"
        open(p, "w", encoding="utf-8").write(s.replace(old, new, count))
    return apply


def first_cite(d):
    for t in d["tokens"].values():
        return t["evidence"][0]


def set_cite(rel, value):
    return jedit(rel, lambda d: first_cite(d).update(cite=value))


def dup_template(d):
    d["templates"]["template.home2"] = json.loads(json.dumps(d["templates"]["template.home"]))


CASES = [
    # (id, needs_source, mutation, expected text in verify_all output)
    ("allowlist/phantom-entry", False, jedit("tokens/llm/component-allowlist.json", lambda d: d["sections"].update({"proof.ghost": d["sections"]["proof.works"]})), "phantom section proof.ghost"),
    ("allowlist/orphan-contract", False, jedit("tokens/llm/component-allowlist.json", lambda d: d["sections"].pop("proof.works")), "orphan contract proof.works"),
    ("allowlist/phantom-primitive", False, jedit("tokens/llm/component-allowlist.json", lambda d: d["primitives"].append("primitive.divider")), "phantom primitive"),
    ("citation/out-of-range", True, set_cite("tokens/00-foundation/radius.json", "src/components/hero/hero.css:9999"), "out of range"),
    ("citation/in-range-wrong-lines", True, set_cite("tokens/00-foundation/radius.json", "src/components/hero/hero.css:1-3"), "does not contain its needle"),
    ("citation/section-source-shifted", True, jedit("sections/proof.works.json", lambda d: d["source"].update(lines="1-5", citation=d["source"]["file"] + ":1-5")), "tag"),
    ("copy/fabricated-reference-string", True, jedit("schema/example.pagespec.json", lambda d: d["nodes"][6]["content"].update(body="Une phrase inventée qui n'existe nulle part dans la source.")), "not found in src"),
    ("manifest/count-drift", False, jedit("registry.manifest.json", lambda d: d["counts"].update(sections=20)), "manifest vs disk"),
    ("readme/count-drift", False, tedit("README.md", "| sections | 19 |", "| sections | 18 |"), "README.sections"),
    ("manifest/allowlist-version-drift", False, jedit("registry.manifest.json", lambda d: d.update(allowlistVersion="0.9.0")), "allowlistVersion"),
    ("catalog/token-value-edited-without-catalog", False, jedit("tokens/00-foundation/color.json", lambda d: d["tokens"]["color.prm1"].update(value="#7700ff")), "catalog drift"),
    ("policy/category-not-in-catalog", False, jedit("tokens/llm/token-policy.json", lambda d: d["rawValueRestrictions"].update(typography="x")), "not a catalog category"),
    ("assets/registry-availability-loosened", False, jedit("assets/asset-roles.json", lambda d: d["roles"]["brand.wordmark"].update(availability="generation-safe")), "registry generation-safe != pinned"),
    ("assets/substitute-not-generation-safe", False, jedit("assets/asset-roles.json", lambda d: d["roles"]["brand.wordmark"].update(generationSafeSubstitutes=["case.photo"])), "substitute case.photo"),
    ("assets/pin-removed-in-validator", False, tedit("schema/semantic_validate.py", '"brand.wordmark": "blocked-for-generation", ', ""), "PINNED_AVAILABILITY differs"),
    ("assets/contract-generated-role-unsafe", False, jedit("sections/proof.works.json", lambda d: d["generatedAssetRoles"].append("case.photo")), "not generation-safe"),
    ("retrieval/contract-and-allowlist-flipped-together", False,
     lambda r: (jedit("sections/chrome.loader.json", lambda d: (d.update(retrievalEligible=True), d.pop("retrievalIneligibleReason")))(r),
                jedit("tokens/llm/component-allowlist.json", lambda d: d["sections"]["chrome.loader"].update(retrievalEligible=True))(r)), "contradicts pin"),
    ("retrieval/pin-removed-in-validator", False, tedit("schema/semantic_validate.py", 'RETRIEVAL_INELIGIBLE = {"backdrop.webgl-scene", "chrome.loader", ', 'RETRIEVAL_INELIGIBLE = {"backdrop.webgl-scene", '), "RETRIEVAL_INELIGIBLE differs"),
    ("graph/rule-without-implementation", False, jedit("compatibility/graph.json", lambda d: d["rules"].append({"id": "NO_TWO_CTAS", "severity": "error", "description": "x"})), "mismatch ['NO_TWO_CTAS']"),
    ("schema/content-drift-from-contract", False, jedit("schema/pagespec.schema.json", lambda d: d["definitions"]["content.story.tagline"]["properties"]["statement"].update(maxWords=99)), "drift"),
    ("policy/hash-drift", False, jedit("tokens/llm/token-policy.json", lambda d: d["nodeSlots"]["blockGap"]["allowed"].append("space.40")), "recomputed"),
    ("policy/self-ratified", False, jedit("policy/design-policy.json", lambda d: d["approval"].update(status="approved", architectureDecisionRecorded=True)), "approval_ok=False"),
    ("gate/measurement-removed", False, jedit("extraction/measured-values.json", lambda d: d["sectionHeights"]["routes"]["/"]["sections"].pop("story.tagline")), "missing measurement"),
    ("gate/whitelist-justification-removed", False, jedit("extraction/measured-values.json", lambda d: d["wrapperGate"]["whitelist"][0].update(justification="ok")), "justification"),
    ("gate/viewport-changed", False, jedit("extraction/measured-values.json", lambda d: d["sectionHeights"].update(viewport="1280x800")), "gate requires 1440x900"),
    ("gate/hero-height-above-whitelist-cap", False, jedit("extraction/measured-values.json", lambda d: d["sectionHeights"]["routes"]["/"]["sections"]["hero.statement"].update(heightPx=7000)), "not above the measured"),
    ("gate/threshold-loosened-in-code", False, tedit("extraction/wrapper_gate.py", "HERO_FAIL_PX = 3000", "HERO_FAIL_PX = 9000"), "stale"),
    ("parity/exception-self-approved", False, jedit("extraction/measured-values.json", lambda d: d["parity"]["exceptions"][0].update(approvedBy="Claude", status="approved")), "pending human approval"),
    ("approval/owner-decision-record-removed", False, jedit("extraction/human-decisions.json", lambda d: d["decisions"].clear()), "approval_ok=False"),
    ("approval/whitelist-approver-not-in-record", False, jedit("extraction/measured-values.json", lambda d: d["wrapperGate"]["whitelist"][0].update(approvedBy="Someone Else")), "recorded human owner decision"),
    ("approval/agent-recorded-as-owner", False, (lambda r: (jedit("extraction/human-decisions.json", lambda d: d["decisions"][0].update(decidedBy="Claude (AI agent)"))(r),
                                                          jedit("extraction/measured-values.json", lambda d: d["parity"]["exceptions"][0].update(approvedBy="Claude (AI agent)"))(r))), "recorded human owner decision"),
    ("parity/sub-gate-section-without-exception", False, jedit("extraction/measured-values.json", lambda d: d["parity"].update(exceptions=[])), "without a recorded exception"),
    ("paths/absolute-machine-path", False, jedit("registry.manifest.json", lambda d: d["sourceProject"].update(location="/" + "Users/someone/projects/clone")), "paths"),
    ("paths/entrypoint-outside-repo", False, jedit("registry.manifest.json", lambda d: d["entryPoints"].update(ia="../ia.json")), "entryPoint outside repo"),
    ("templates/route-mapped-twice", False, jedit("templates/templates.json", dup_template), "mapped 2 times"),
]


def scratch():
    base = tempfile.mkdtemp(prefix="design-repo-drift-")
    dst = os.path.join(base, "design-repo")
    shutil.copytree(REPO, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
    if HAVE_SRC:
        for n in LINK:
            if os.path.exists(os.path.join(ROOT, n)):
                os.symlink(os.path.join(ROOT, n), os.path.join(base, n))
    return base, dst


def verify(repo):
    p = subprocess.run([sys.executable, os.path.join(repo, "extraction", "verify_all.py")], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def main():
    rows, failed = [], 0
    base, dst = scratch()
    try:
        code, out = verify(dst)
        ok = code == 0
        failed += not ok
        rows.append(("PASSES" if ok else "FAILED", "control/unmodified-copy", "verify_all exit 0" if ok else out[-400:]))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    for id_, needs_src, fn, expect in CASES:
        if needs_src and not HAVE_SRC:
            rows.append(("SKIPPED", id_, "no sibling source tree"))
            continue
        base, dst = scratch()
        try:
            fn(dst)
            code, out = verify(dst)
            fails = [l for l in out.splitlines() if l.startswith("FAIL")]
            ok = code == 1 and any(expect in l for l in fails)
            failed += not ok
            rows.append(("CAUGHT" if ok else "MISSED", id_, next((l[:150] for l in fails if expect in l), out[-300:])))
        finally:
            shutil.rmtree(base, ignore_errors=True)
    for st, id_, info in rows:
        print(f"{st:7} {id_:48} {info}")
    caught = sum(1 for r in rows if r[0] == "CAUGHT")
    skipped = sum(1 for r in rows if r[0] == "SKIPPED")
    print(f"\nprove_drift: {caught}/{len(CASES) - skipped} drift cases caught" + (f", {skipped} skipped (no source)" if skipped else "") + f"; control {'passes' if rows[0][0] == 'PASSES' else 'FAILS'}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
