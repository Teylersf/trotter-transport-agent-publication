"""Prepare an offline, explicitly credited agent edition of the canonical audit.

Only owned local files are written. No network, Git, credentials, registration,
submission, review, or eligibility-check code is present. Every preparation
retains a closed Publish.fun sequencing gate. Run again after canonical fixes.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PREPARER_BYTES = Path(__file__).read_bytes()
CANONICAL = ROOT.parent / "trotter-transport-audit"
AGENT_REPOSITORY = "https://github.com/Teylersf/trotter-transport-agent-publication"
CANONICAL_REPOSITORY = "https://github.com/Teylersf/trotter-transport-audit"
AGENT_ID = "agent_29b9bf7a"
AGENT_NAME = "Lattice Audit Agent"
IDENTITY = "gist:7c74312cf47dcc31c789a8b1c3dedd25"
MODEL = "OpenAI Codex; exact underlying model identifier not recorded"
TAGS = ["quantum-algorithms", "numerical-analysis", "transport-equations",
        "Trotterization", "reproducibility"]
PLATFORM_HEADINGS = ["Introduction", "Related Work", "Methodology", "Results",
                     "Discussion", "Limitations", "Conclusion"]
MATH = re.compile(r"\\\[.*?\\\]|\\\(.*?\\\)|\$\$.*?\$\$|(?<![\\$])\$(?!\$).*?(?<!\\)\$(?!\$)", re.S)
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
DISCLOSURE = (
    "**Authorship and assistance.** Lattice Audit Agent is the authorized agent "
    "author of this venue-specific edition. Human operator and canonical author: "
    "Taylor Kalin. The canonical Taylor Kalin manuscript is available at "
    + CANONICAL_REPOSITORY + "/blob/main/paper/manuscript.md . "
    "The scientific text, equations, references and figures are retained; only "
    "the byline, this disclosure and figure-link routes are adapted. AI tools "
    "assisted with literature retrieval, derivation checks, code, internal reviews "
    "and manuscript drafting. These checks are not independent human peer review. "
    "The platform agent byline does not replace Taylor Kalin's canonical authorship."
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode_json(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n").encode("utf-8")


def utf16_length(text):
    return len(text.encode("utf-16-le")) // 2


def words(text):
    return len(re.findall(r"\b[\w'-]+\b", text))


def sections(text):
    matches = list(re.finditer(r"^## (.+)$", text, re.M))
    out = {}
    for i, m in enumerate(matches):
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        if m.group(1) in out:
            raise ValueError("Duplicate canonical section heading")
        out[m.group(1)] = text[m.end():end].strip()
    return out


def numbered_sections(parsed):
    out = {}
    for heading, body in parsed.items():
        m = re.fullmatch(r"([1-8])\. (.+)", heading)
        if m:
            if int(m.group(1)) in out:
                raise ValueError("Duplicate canonical numbered section")
            out[int(m.group(1))] = (heading, body)
    if sorted(out) != list(range(1, 9)):
        raise ValueError("Expected exactly canonical numbered sections 1 through 8")
    return out


def appendix_sections(parsed):
    """Keep optional top-level appendices in source order; never discard one."""
    numbered = numbered_sections(parsed)
    keys = list(parsed)
    out = {}
    if list(numbered) != list(range(1,9)):
        raise ValueError("Required scientific sections must remain in order 1 through 8")
    for heading, body in parsed.items():
        match = re.fullmatch(r"Appendix ([A-Z])(?:[.:]\s*|\s+|$)(.*)", heading)
        if match:
            letter = match.group(1)
            if letter in out:
                raise ValueError("Duplicate canonical appendix letter")
            out[letter] = (heading, body)
    expected = [chr(ord('A')+i) for i in range(len(out))]
    if list(out) != expected:
        raise ValueError("Appendices must be contiguous and ordered A, B, ...")
    permitted = {"Abstract", "References", *(h for h,_ in numbered.values()),
                 *(h for h,_ in out.values())}
    if set(parsed) != permitted:
        raise ValueError("Unrecognized top-level scientific heading; refuse to omit it")
    conclusion = keys.index(numbered[8][0])
    reference = keys.index("References")
    if conclusion >= reference or any(not conclusion < keys.index(h) < reference
                                     for h,_ in out.values()):
        raise ValueError("Appendices must follow Conclusion and precede References")
    if keys != ["Abstract", *(h for h,_ in numbered.values()),
                *(h for h,_ in out.values()), "References"]:
        raise ValueError("Canonical top-level section order is inconsistent")
    return out


def protected_blocks(text):
    """Full text equality is primary; these independent inventories aid review."""
    return {
        "math": math_tokens(text),
        "tables": re.findall(r"(?m)^(?:[ \t]*\|[^\n]*\|[ \t]*(?:\n|$))+", text),
        "quotations": re.findall(r"(?m)^(?:>[^\n]*(?:\n|$))+", text),
        "code_fences": re.findall(r"(?ms)^```[^\n]*\n.*?^```[ \t]*$", text),
        "proof_markers": re.findall(r"(?m)^(?:#{3,6}\s+)?(?:\*\*)?Proof\b[^\n]*", text),
    }


def platform_arrangement(numbered, appendices):
    """Return unchanged bodies in the required seven-plus-optional order."""
    mapped = [numbered[1][1], numbered[2][1], numbered[3][1],
              "### "+numbered[4][0]+"\n\n"+numbered[4][1]+"\n\n### "+numbered[5][0]+"\n\n"+numbered[5][1],
              numbered[6][1], numbered[7][1], numbered[8][1]]
    headings = list(PLATFORM_HEADINGS)
    if appendices:
        mapped.append("\n\n".join("### "+heading+"\n\n"+body
                                   for heading,body in appendices.values()))
        headings.append("Appendix")
    return headings, mapped


def journal_evidence(canonical, version):
    """A revision's journal claims require the actual public concordance record."""
    if version == "1.0.0":
        return None
    path = canonical/"data"/"journal-comparison.json"
    data = path.read_bytes()
    record = json.loads(data)
    findings = record.get("findings", [])
    if ([r.get("id") for r in findings] != ["C"+str(i) for i in range(1,11)]
            or any(r.get("status") != "persists" for r in findings)
            or record.get("status_counts") != {"persists":10,"corrected":0,"altered":0}):
        raise ValueError("Journal concordance does not bind all ten persistent groups")
    edition = record.get("journal_edition", {})
    if (edition.get("doi") != "10.1088/2058-9565/ae488e"
            or not re.fullmatch(r"[0-9a-f]{64}", edition.get("sha256", ""))
            or edition.get("http_status") != 200 or edition.get("pdf_pages") != 34
            or not isinstance(edition.get("bytes"), int) or edition["bytes"] <= 0):
        raise ValueError("Incomplete actual journal-PDF provenance")
    return {"record":record, "path":"data/journal-comparison.json", "sha256":sha(data)}


def readme_documents(title, version, code_pin, checks, journal):
    """Generated only by an explicitly invoked preparation, never at import."""
    if journal:
        scope = ("The supplied arXiv v2 and the directly obtained published journal PDF "
                 "were compared. All ten registered correction groups persist in the "
                 "checked journal passages, with differing mathematical consequences. "
                 "The added journal discussions of localization width, implementation/output "
                 "costs and periodic boundaries are credited. This is not a complete audit "
                 "of every new journal passage and does not identify the equations used "
                 "by original code unavailable in the inspected materials.")
    else:
        scope = "This version audits arXiv:2508.15691v2; its journal text is not audited in that edition."
    appendix_note = ("All complete appendices remain after Conclusion in paper.md and "
                     "are grouped, without shortening, in one optional AgentPub Appendix section."
                     if checks["appendices"] else "This edition has no optional appendix.")
    root = f"""# {title}

Agent edition by **Lattice Audit Agent**. Human operator and canonical author: **Taylor Kalin**.

Version {version}; [canonical audit]({CANONICAL_REPOSITORY}). {scope}

The edition preserves all scientific paragraphs, complete proofs, source quotations, tables, ordered math tokens, reference records and figures. Only the agent byline/disclosure, declared figure routes and required platform section arrangement are adapted. {appendix_note} Numerical benefits and limits are retained; this package does not establish quantum advantage or infer fabrication or implementation failure from printed discrepancies.

- [Full agent manuscript](paper.md)
- [AgentPub payload](agentpub-payload.json) and [AAES registration](aaes-registration.json)
- [Preservation/copy checks](reproduction/adapter-checks.json)
- [Reproduction instructions](reproduction/README.md)
- [Submission context](reproduction/submission-context.json)

The current preparation records {checks['math_segments_in_scientific_body']} scientific-body math segments, {checks['figures']} figures and {checks['reference_records']} references, with {len(checks['copied_scientific_files'])} byte-exact canonical copies. The scientific numerical snapshot is `{code_pin}`; packaging and source-comparison evidence may be newer and are separately hashed. The original canonical manuscript retains Taylor Kalin's byline in `reproduction/canonical/paper/manuscript.md`.

The intended repository is `Teylersf/trotter-transport-agent-publication`. AgentPub identity: `{AGENT_ID}`. Existing AAES identity: [{IDENTITY}](https://gist.github.com/Teylersf/7c74312cf47dcc31c789a8b1c3dedd25). Preparation does not verify public availability, current identity access, GitHub eligibility or review disposition.

**Local preparation only.** Submission gates remain closed pending a final disposition ending the Publish.fun review, verified publication, or formal release. A completed round requesting revisions does not release that gate. No credential or network/submission automation is included. A venue renderer is not certified by local source-preservation checks.

Our own manuscript/figures use CC BY 4.0 and original audit code uses MIT as disclosed by the canonical author. Third-party excerpts, figures and source works retain their own rights and applicable licenses; they are not relicensed by this package.
"""
    reproduction = f"""# Reproduction and preparation of version {version}

The numerical scientific snapshot is `{code_pin}`. Exact current manuscript, concordance and copy hashes are in `adapter-checks.json`; updated manuscript/provenance packaging is distinct from unchanged numerical results.

## Numerical checks

The `canonical/` directory contains approved canonical science copied byte-for-byte. From this repository:

```console
cd reproduction/canonical
python -m pip install -r requirements.txt
python experiments/reproduce.py
python experiments/resource_counterchecks.py
```

These CPU calculations use NumPy, with Matplotlib for figures. They test specified equations and independent smooth periodic examples. They do not rerun the original hardware or reproduce the source's two-dimensional figures. {scope}

## Offline preparation

```console
python reproduction/prepare_packages.py --expected-code-commit {code_pin}
```

Keep the canonical checkout beside this repository, or supply `--canonical-root`. `--expected-manuscript-sha256` can require the exact final manuscript. Preparation performs no network or Git operations, scientific execution, credential access, registration, submission or review call. It checks current inputs before output writes. It can be repeated after authorized canonical corrections.

All required scientific sections 1–8 remain in order; nested Methods headings are retained. Canonical sections 4+5 are grouped under AgentPub Results. {appendix_note} References remain complete in paper.md and are structured outside AgentPub section contents. Every scientific paragraph and complete section body is compared after reversing only allowed authorship/figure-link adaptations; complete proofs are covered by that equality. Math, tables, source blockquotes, code fences and figure captions/order also have separate exact inventories. No scientific simplification, truncation, padding or math-whitespace compression is performed.

Every platform section, including Appendix, must fit both Unicode and UTF-16 counts within 49,000. The saved official template supplies other format checks. Any body-length/ref-count guideline shortfall is reported instead of repaired by changing science. Copied files and the source-concordance JSON have exact byte hashes. Private notes, credentials, caches, raw third-party PDFs and operational venue receipts are excluded.

Every invocation leaves all submission gates false. A later final disposition ending review, verified publication or formal release requires separately verified context; a revision request is not release. Agent-only authorship is explicit, Taylor Kalin's canonical authorship is retained, and AI-assisted checks are not independent human peer review. Token usage is unrecorded; AgentPub's `-1` integer is expressly a missing-data sentinel.
"""
    return {"README.md":root.encode("utf-8"),
            "reproduction/README.md":reproduction.encode("utf-8")}


def references(text):
    matches = list(re.finditer(r"^\[(\d+)\] (.+?)(?=\n\n\[\d+\] |\Z)", text, re.M | re.S))
    if not matches:
        raise ValueError("No canonical reference records found")
    result, originals = [], []
    for match in matches:
        number, record = match.group(1), match.group(2).strip()
        originals.append(match.group(0).strip())
        explicit = re.search(r"(?<!\*)\*([^*]+)\*(?!\*)", record)
        if "same title" in record:
            if not result:
                raise ValueError("Unresolved 'same title' reference")
            title = result[-1]["title"]
            author_part = record.split(", same title", 1)[0]
        elif explicit:
            title = explicit.group(1)
            author_part = record[:explicit.start()].rstrip(", ")
        else:
            raise ValueError("Reference requires an explicit verified canonical title")
        authors = [s.strip() for s in re.split(r",\s*|\s+and\s+", author_part) if s.strip()]
        urls = [u.rstrip(".;,") for u in re.findall(r"https?://[^\s]+", record)]
        years = re.findall(r"\b(?:19|20)\d{2}\b", record)
        if not authors or not urls or not years:
            raise ValueError("Reference lacks canonical authors, year or URL")
        item = {"ref_id": number, "type": "external",
                "source": "arxiv" if "arxiv.org" in urls[0] else "doi" if "doi.org" in urls[0] else "url",
                "title": title, "authors": authors, "year": int(years[0]), "url": urls[0]}
        doi = next((u.split("doi.org/", 1)[1] for u in urls if "doi.org/" in u), None)
        if doi:
            item["doi"] = doi
        result.append(item)
    if [int(x["ref_id"]) for x in result] != list(range(1, len(result)+1)):
        raise ValueError("Reference numbering must be contiguous")
    return result, originals


def math_tokens(text):
    return MATH.findall(text)


def scientific_paragraphs(text):
    return Counter(block.strip() for block in re.split(r"\n\s*\n", text.strip())
                   if block.strip() and not re.fullmatch(r"#{1,6} .+", block.strip()))


def public_copy_paths(canonical):
    paths = []
    explicit = ["requirements.txt", "README.md", "SOURCE.md", "LICENSE", "LICENSE-CODE", "LICENSE-PAPER",
                "LICENSE-MANUSCRIPT",
                "data/reproducibility.json", "data/source-provenance.json",
                "data/correction-registry.json", "data/provenance.json",
                "data/journal-comparison.json", "data/zenodo-code-archive.json"]
    for name in explicit:
        p = canonical / name
        if p.is_file():
            paths.append(p)
    for folder, suffixes in [("experiments", {".py"}), ("results", {".json", ".csv"}),
                             ("figures", {".png", ".pdf", ".svg"})]:
        paths.extend(p for p in (canonical/folder).glob("*") if p.is_file() and p.suffix in suffixes)
    for name in ["manuscript.md", "core.md", "closing.md", "resource-discussion.md",
                 "revision-journal-concordance.md", "revision-source-quotes.md",
                 "revision-numerical-provenance.md"]:
        p = canonical/"paper"/name
        if p.is_file():
            paths.append(p)
    paths.extend(p for p in (canonical/"paper"/"latex").glob("*.tex") if p.is_file())
    paths.extend(p for p in (canonical/"paper"/"latex"/"images").glob("*.png") if p.is_file())
    paths = sorted(set(paths))
    for p in paths:
        if p.is_symlink() or not p.resolve().is_relative_to(canonical.resolve()):
            raise ValueError("Public-copy input escapes canonical root")
        if any(s.lower() in {"private", "audit", "submissions", ".publishing-access", "__pycache__"}
               for s in p.relative_to(canonical).parts):
            raise ValueError("Operational/private material is not public reproduction input")
    return paths


def main():
    if sys.flags.optimize:
        raise RuntimeError("Do not disable preparation assertions with Python -O")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=CANONICAL)
    parser.add_argument("--expected-code-commit", required=True)
    parser.add_argument("--expected-manuscript-sha256")
    args = parser.parse_args()
    canonical = args.canonical_root.resolve()
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_code_commit):
        raise ValueError("Expected code commit must be a full lowercase 40-digit SHA")
    source_path = canonical/"paper"/"manuscript.md"
    source_bytes = source_path.read_bytes()
    source = source_bytes.decode("utf-8")
    if args.expected_manuscript_sha256 and sha(source_bytes) != args.expected_manuscript_sha256:
        raise ValueError("Canonical manuscript hash differs from explicit expected bytes")
    if args.expected_code_commit not in source:
        raise ValueError("Expected immutable scientific pin is absent from canonical manuscript")
    schema_path = ROOT/"reproduction"/"venue-schema-snapshot.json"
    schema_bytes = schema_path.read_bytes()
    schema = json.loads(schema_bytes)
    parsed = sections(source)
    original = numbered_sections(parsed)
    appendices = appendix_sections(parsed)
    scientific_sections = [*original.values(), *appendices.values()]
    title_match = re.search(r"^# (.+)$", source, re.M)
    version_match = re.search(r"^Version ([^;\s]+); (.+)$", source, re.M)
    if not title_match or not version_match or "Abstract" not in parsed or "References" not in parsed:
        raise ValueError("Canonical title/version/abstract/references missing")
    title, abstract = title_match.group(1), parsed["Abstract"]
    version, date = version_match.groups()
    journal = journal_evidence(canonical, version)
    refs, ref_blocks = references(parsed["References"])
    old_disclosures = re.findall(r"^\*\*Authorship and assistance\.\*\* .+$", source, re.M)
    if len(old_disclosures) != 1:
        raise ValueError("Exactly one explicit canonical authorship disclosure is required")
    old_disclosure = old_disclosures[0]
    images = IMAGE.findall(source)
    if not images:
        raise ValueError("No canonical figure links")
    link_map = {}
    for caption, link in images:
        if not link.startswith("../figures/") or (canonical/"paper"/link).resolve().parent != canonical/"figures":
            raise ValueError("Unexpected scientific figure path; review before adapting")
        filename = Path(link).name
        if not (canonical/"figures"/filename).is_file():
            raise ValueError("Missing original figure")
        link_map[link] = "reproduction/canonical/figures/"+filename
    def adapt(body, absolute=False):
        body = body.replace(old_disclosure, DISCLOSURE)
        for old, local in link_map.items():
            new = ("https://raw.githubusercontent.com/Teylersf/trotter-transport-agent-publication/main/"+local) if absolute else local
            body = body.replace("]("+old+")", "]("+new+")")
        return body
    def restore(body, absolute=False):
        body = body.replace(DISCLOSURE, old_disclosure)
        for old, local in link_map.items():
            new = ("https://raw.githubusercontent.com/Teylersf/trotter-transport-agent-publication/main/"+local) if absolute else local
            body = body.replace("]("+new+")", "]("+old+")")
        return body
    # The AAES body retains every numbered section and every full appendix.
    agent_body = "\n\n".join("## "+heading+"\n\n"+adapt(body)
                              for heading, body in scientific_sections)
    paper = ("# "+title+"\n\n**"+AGENT_NAME+"**  \n"
             "Authorized agent-only edition. Human operator and canonical author: **Taylor Kalin**.  \n"
             "AgentPub identity: `"+AGENT_ID+"`; AAES identity: `"+IDENTITY+"`.  \n"
             "Taylor Kalin: https://taylorkalin.com ; ORCID 0009-0003-9000-9315.  \n"
             "Version "+version+"; "+date+"\n\n## Abstract\n\n"+abstract+"\n\n"+
             agent_body+"\n\n## References\n\n"+parsed["References"]+"\n")
    platform_headings, mapped = platform_arrangement(original, appendices)
    platform_sections = []
    for heading, body in zip(platform_headings, mapped):
        content = adapt(body, absolute=True)
        citations = sorted(set(re.findall(r"\[(\d+)\](?!\()", content)), key=int)
        if not set(citations) <= {r["ref_id"] for r in refs}:
            raise ValueError("Unresolved numeric citation")
        platform_sections.append({"heading": heading, "content": content, "citations": citations})
    caps = {s["heading"]: {"unicode_codepoints": len(s["content"]),
                           "utf16_code_units": utf16_length(s["content"])} for s in platform_sections}
    if any(max(v.values()) > 49000 for v in caps.values()):
        raise ValueError("AgentPub section exceeds conservative 49,000-character limit; do not truncate science")
    payload = {"title": title, "abstract": abstract, "paper_type": "research_article",
               "authors": [{"agent_id": AGENT_ID, "display_name": AGENT_NAME, "model_type": "OpenAI Codex"}],
               "sections": platform_sections, "references": refs, "tags": TAGS,
               "metadata": {"agent_model": MODEL, "agent_platform": "Codex desktop", "total_tokens": -1,
                            "submission_note": "Authorized agent edition; Taylor Kalin is human operator and canonical author. All scientific paragraphs, complete proofs, quotations, tables, equations, figure captions and references are retained. Canonical sections 4+5 are grouped under Results; any complete appendices are grouped into one optional Appendix after Conclusion. Figure routes and authorship disclosure are adapted. Exact token usage was not recorded; -1 is an explicit missing-data sentinel. This local preparation has not been submitted. Publish.fun sequencing remains blocked pending final disposition ending review, verified publication or formal release; a revision request is not release. Full edition: "+AGENT_REPOSITORY+"/blob/main/paper.md ."}}
    canonical_science = "\n\n".join(body for _,body in scientific_sections)
    parsed_agent = sections(paper)
    aaes_restored = restore("\n\n".join(body for _,body in [
        *numbered_sections(parsed_agent).values(), *appendix_sections(parsed_agent).values()]))
    platform_restored = "\n\n".join(restore(s["content"], absolute=True) for s in platform_sections)
    expected_platform = "\n\n".join(mapped)
    assert aaes_restored == canonical_science
    assert platform_restored == expected_platform
    assert scientific_paragraphs(platform_restored) == scientific_paragraphs(canonical_science)
    assert math_tokens(canonical_science) == math_tokens(platform_restored) == math_tokens(aaes_restored)
    assert protected_blocks(canonical_science) == protected_blocks(platform_restored) == protected_blocks(aaes_restored)
    assert IMAGE.findall(restore(agent_body)) == images
    assert IMAGE.findall(platform_restored) == images
    assert sections(paper)["References"] == parsed["References"]
    assert sections(paper)["Abstract"] == abstract == payload["abstract"]
    assert "??" not in paper and "TODO" not in paper
    body_words = sum(words(s["content"]) for s in platform_sections)
    constraints = schema["agentpub"]["research_article_constraints"]
    guideline_checks = {"title_limit":len(title)<=constraints["title"]["max_chars"],
                        "abstract_word_limit":words(abstract)<=constraints["abstract"]["max_words"],
                        "reference_minimum":len(refs)>=constraints["references"]["min_count"],
                        "body_word_range":constraints["body_word_count"]["min_words"]<=body_words<=constraints["body_word_count"]["max_words"],
                        "required_sections_and_order":platform_headings[:7]==schema["agentpub"]["required_sections"]
                            and platform_headings in [PLATFORM_HEADINGS, PLATFORM_HEADINGS+["Appendix"]],
                        "all_sections_allowed":all(h in constraints["sections"]["allowed"] for h in platform_headings)}
    # Keep any guideline shortfall visible rather than padding or altering science.
    now = datetime.now(timezone.utc).isoformat()
    context = {"prepared_at_utc":now, "canonical_version":version,
               "canonical_manuscript_sha256":sha(source_bytes),
               "expected_scientific_code_commit":args.expected_code_commit,
               "publication_state":"local_prepared_not_submitted", "publishfun_state":"pending_review",
               "publishfun_review_closed_verified":False, "publishfun_release_verified":False,
               "submission_gate_open":False, "agentpub_submission_gate_open":False,
               "aaes_submission_gate_open":False, "public_repository_verified":False,
               "agent_identity_verified_currently":False,
               "note":"Preparation does not imply publication, final disposition ending review, public repository availability, identity eligibility or authorization to submit concurrently. A completed round requesting revisions does not release the gate. Gate changes require separate verified publication evidence; this script never opens them."}
    claims = [
        {"text":"The audited v2 derivative-norm conservation assertion fails for a smooth periodic shear satisfying its coordinate-independence condition.", "kind":"finding", "status":"proposed", "evidence_summary":"Exact shear solution and gradient identities in Section 4.1, independently sampled in reproduction/canonical/results/shear.csv.", "confidence_note":"Version-specific statement; does not refute every finite-time vector-norm estimate or audit the inaccessible journal version."},
        {"text":"Smooth periodic coefficients permit a finite-grid commutator bound proportional to inverse mesh spacing, improving the paper's crude inverse-square operator comparator.", "kind":"finding", "status":"proposed", "evidence_summary":"Translation/multiplication commutator identity and numerical operator norms in Section 4.2 and reproduction/canonical/results/commutators.csv.", "confidence_note":"Fixed dimension/order and bounded coefficient gradients; not an optimal end-to-end complexity theorem."},
        {"text":"The printed SWAP-test probabilities and polynomial-moment continuum prefactor disagree with direct finite-dimensional checks.", "kind":"finding", "status":"proposed", "evidence_summary":"Controlled-SWAP matrix and normalized constant-function overlap checks in reproduction/canonical/results/swap.csv, reproduction/canonical/results/moments.csv and reproduction/canonical/results/resource-counterchecks.json.", "confidence_note":"Does not invalidate the separate Hadamard protocol or identify the original code unavailable in the inspected arXiv materials."},
        {"text":"The reported eight-point hardware discretization-error magnitudes are reproduced, and a separate periodic smooth example exhibits a stable fixed-step splitting error under grid refinement.", "kind":"finding", "status":"proposed", "evidence_summary":"reproduction/canonical/results/resource-counterchecks.json retains exact settings and reference-refinement differences.", "confidence_note":"Deterministic classical calculations; no hardware rerun, original Figure 5 reproduction, repaired full theorem or demonstrated quantum advantage."},
    ]
    if journal:
        claims[0]["confidence_note"] = "Applies to specified arXiv v2 and journal passages; not a complete journal error audit or a refutation of every finite-time smooth-state bound."
        claims.append({"text":"All ten registered correction groups persist in the directly obtained published journal PDF, with the mathematical and implementation qualifications retained.",
                       "kind":"finding", "status":"proposed",
                       "evidence_summary":"reproduction/canonical/data/journal-comparison.json binds C1–C10, each arXiv/journal locator, the official PDF URL and SHA-256 "+journal["record"]["journal_edition"]["sha256"]+". The full source-equation appendix remains in the manuscript.",
                       "confidence_note":"This checks the ten specified printed groups, not every new journal passage or original execution. Added Gaussian-width, simulation/readout-cost and boundary discussions are credited; local corrections have differing consequences. No fabrication, hardware rerun or original-figure failure is inferred."})
    novelty = "Version-specific correction audit of arXiv:2508.15691v2 with exact counterexamples, a constructive finite-time regularity replacement, a coefficient-aware finite-grid operator baseline, independent positive diagnostics and explicit implementation limits. Established transport, SWAP and commutator identities are identified as established ingredients, not new discoveries. "
    novelty += ("The directly obtained journal PDF is also audited for all ten registered groups, which persist with their qualifications. The journal's added localization-width, implementation/output-cost and boundary discussions are credited. This is not a complete audit of every journal addition, a new quantum algorithm, or proof of implementation failure."
                if journal else "The journal version is not audited in this edition.")
    metadata = {"aaes_version":"4.2", "title":title, "abstract":abstract,
                "author_ids":[IDENTITY], "submitted_at":now, "tags":TAGS,
                "generation_environment":{"model":MODEL, "tools":["Python 3.12.14", "NumPy 2.3.5", "Matplotlib"],
                 "prompt_strategy":"Version-specific source reading, exact derivations, small independent matrix checks and preserved canonical manuscript.",
                 "notes":"Agent author Lattice Audit Agent; human operator and canonical author Taylor Kalin. Self-funded. AI-assisted internal checks are not independent human peer review. Exact model identifier/token usage unavailable. submitted_at denotes local package preparation, not AAES registration. Publish.fun sequencing gate remains closed."},
                "novelty_statement":novelty}
    registration = {"source":"github:Teylersf/trotter-transport-agent-publication",
                    "submission":{"kind":"paper", "maturity":"final"},
                    "project":{"title":title, "summary":abstract,
                     "research_question":"Which specified arXiv v2 and journal statements fail exact checks, which finite-time/resource qualifications are needed, and which numerical observations survive?" if journal else "Which printed arXiv v2 statements fail exact checks, which finite-time/resource qualifications are needed, and which numerical observations survive?", "status":"active"},
                    "claims":claims}
    inputs = {p.relative_to(canonical).as_posix():p.read_bytes() for p in public_copy_paths(canonical)}
    if inputs.get("paper/manuscript.md") != source_bytes:
        raise ValueError("Canonical manuscript changed during preparation")
    copies = {"reproduction/canonical/"+name:data for name,data in inputs.items()}
    manifest = [{"canonical_path":name, "copy_path":"reproduction/canonical/"+name,
                 "bytes":len(data), "sha256":sha(data)} for name,data in inputs.items()]
    checks = {"canonical_version":version, "scientific_code_commit":args.expected_code_commit,
              "canonical_manuscript_sha256":sha(source_bytes),
              "preparer_sha256":sha(PREPARER_BYTES), "schema_snapshot_sha256":sha(schema_bytes),
              "scientific_sections":len(original), "appendices":[heading for heading,_ in appendices.values()],
              "platform_sections":platform_headings,
              "math_segments_in_scientific_body":len(math_tokens(canonical_science)),
              "numbered_equations":len(re.findall(r"\\tag\{[^}]+\}", canonical_science)),
              "figures":len(images), "reference_records":len(refs),
              "reference_source_blocks":ref_blocks, "section_character_counts":caps,
              "body_regex_words":body_words, "abstract_regex_words":words(abstract),
              "all_scientific_paragraphs_exact_after_allowed_adapter_reversal":True,
              "all_complete_proofs_preserved_by_full_section_equality":True,
              "full_scientific_section_bodies":[{"heading":heading,"sha256":sha(body.encode("utf-8"))}
                                               for heading,body in scientific_sections],
              "protected_block_counts":{kind:len(blocks) for kind,blocks in protected_blocks(canonical_science).items()},
              "tables_quotations_code_and_proof_markers_exact":True,
              "ordered_math_segments_exact":True, "abstract_exact":True,
              "figure_captions_and_order_exact":True, "all_reference_paragraphs_exact_in_full_edition":True,
              "guideline_checks":guideline_checks, "all_guideline_checks_passed":all(guideline_checks.values()),
              "copied_scientific_files":manifest, "submission_gate_open":False,
              "note":"Original scientific paragraphs/equations are never condensed or padded. Platform references are structured from the complete canonical records. Figure link paths differ by declared route only. submitted_at is not registration evidence."}
    if journal:
        if not any(row["canonical_path"] == journal["path"] and row["sha256"] == journal["sha256"] for row in manifest):
            raise ValueError("Journal claims are not bound to the exact copied concordance")
        checks["journal_concordance"] = {"path":journal["path"],"sha256":journal["sha256"],
                                         "specified_groups_audited":10,"persistent_groups":10,
                                         "complete_journal_audit_claimed":False}
    products = {"paper.md":paper.encode("utf-8"), "agentpub-payload.json":encode_json(payload),
                "metadata.json":encode_json(metadata), "aaes-registration.json":encode_json(registration),
                "reproduction/submission-context.json":encode_json(context),
                "reproduction/adapter-checks.json":encode_json(checks), **copies,
                **readme_documents(title, version, args.expected_code_commit, checks, journal)}
    # Refuse stale inputs before the first output write. No source is modified.
    if Path(__file__).read_bytes() != PREPARER_BYTES or schema_path.read_bytes() != schema_bytes:
        raise ValueError("Preparer or schema changed during preparation")
    for name, data in inputs.items():
        if (canonical/name).read_bytes() != data:
            raise ValueError("Canonical input changed before output write: "+name)
    for name, data in products.items():
        path = ROOT/name
        if not path.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError("Output escapes agent repository")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    for name, data in products.items():
        if (ROOT/name).read_bytes() != data:
            raise ValueError("Output byte verification failed: "+name)
    print(json.dumps({"prepared":True, "version":version, "agentpub_payload_sha256":sha(products["agentpub-payload.json"]),
                      "copied_files":len(manifest), "body_regex_words":body_words, "figures":len(images),
                      "math_segments":checks["math_segments_in_scientific_body"], "references":len(refs),
                      "guideline_checks":guideline_checks, "submission_gate_open":False}))


if __name__ == "__main__":
    main()
