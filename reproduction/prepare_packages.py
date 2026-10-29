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
MATH = re.compile(r"\$\$.*?\$\$|(?<![\\$])\$(?!\$).*?(?<!\\)\$(?!\$)", re.S)
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
    explicit = ["requirements.txt", "README.md", "LICENSE", "LICENSE-CODE", "LICENSE-PAPER",
                "data/reproducibility.json", "data/source-provenance.json",
                "data/correction-registry.json", "data/provenance.json"]
    for name in explicit:
        p = canonical / name
        if p.is_file():
            paths.append(p)
    for folder, suffixes in [("experiments", {".py"}), ("results", {".json", ".csv"}),
                             ("figures", {".png", ".pdf", ".svg"})]:
        paths.extend(p for p in (canonical/folder).glob("*") if p.is_file() and p.suffix in suffixes)
    for name in ["manuscript.md", "core.md", "closing.md", "resource-discussion.md"]:
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
    title_match = re.search(r"^# (.+)$", source, re.M)
    version_match = re.search(r"^Version ([^;\s]+); (.+)$", source, re.M)
    if not title_match or not version_match or "Abstract" not in parsed or "References" not in parsed:
        raise ValueError("Canonical title/version/abstract/references missing")
    title, abstract = title_match.group(1), parsed["Abstract"]
    version, date = version_match.groups()
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
    # The AAES body retains every original numbered heading and reference record.
    agent_body = "\n\n".join("## "+heading+"\n\n"+adapt(body)
                              for heading, body in original.values())
    paper = ("# "+title+"\n\n**"+AGENT_NAME+"**  \n"
             "Authorized agent-only edition. Human operator and canonical author: **Taylor Kalin**.  \n"
             "AgentPub identity: `"+AGENT_ID+"`; AAES identity: `"+IDENTITY+"`.  \n"
             "Taylor Kalin: https://taylorkalin.com ; ORCID 0009-0003-9000-9315.  \n"
             "Version "+version+"; "+date+"\n\n## Abstract\n\n"+abstract+"\n\n"+
             agent_body+"\n\n## References\n\n"+parsed["References"]+"\n")
    mapped = [original[1][1], original[2][1], original[3][1],
              "### "+original[4][0]+"\n\n"+original[4][1]+"\n\n### "+original[5][0]+"\n\n"+original[5][1],
              original[6][1], original[7][1], original[8][1]]
    platform_sections = []
    for heading, body in zip(PLATFORM_HEADINGS, mapped):
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
                            "submission_note": "Authorized agent edition; Taylor Kalin is human operator and canonical author. All scientific paragraphs, equations, figure captions and references are retained. Canonical sections4+5 are grouped under Results; figure routes and authorship disclosure are adapted. Exact token usage was not recorded; -1 is an explicit missing-data sentinel. This local preparation has not been submitted. Publish.fun sequencing remains blocked pending verified completed or released review. Full edition: "+AGENT_REPOSITORY+"/blob/main/paper.md ."}}
    canonical_science = "\n\n".join(body for _,body in original.values())
    aaes_restored = restore("\n\n".join(body for _,body in numbered_sections(sections(paper)).values()))
    platform_restored = "\n\n".join(restore(s["content"], absolute=True) for s in platform_sections)
    expected_platform = "\n\n".join(mapped)
    assert aaes_restored == canonical_science
    assert platform_restored == expected_platform
    assert scientific_paragraphs(platform_restored) == scientific_paragraphs(canonical_science)
    assert math_tokens(canonical_science) == math_tokens(platform_restored) == math_tokens(aaes_restored)
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
                        "required_sections_and_order":PLATFORM_HEADINGS==schema["agentpub"]["required_sections"]}
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
               "note":"Preparation does not imply publication, completed review, public repository availability, identity eligibility or authorization to submit concurrently. Gate changes require separate verified publication evidence; this script never opens them."}
    claims = [
        {"text":"The audited v2 derivative-norm conservation assertion fails for a smooth periodic shear satisfying its coordinate-independence condition.", "kind":"finding", "status":"proposed", "evidence_summary":"Exact shear solution and gradient identities in Section 4.1, independently sampled in reproduction/canonical/results/shear.csv.", "confidence_note":"Version-specific statement; does not refute every finite-time vector-norm estimate or audit the inaccessible journal version."},
        {"text":"Smooth periodic coefficients permit a finite-grid commutator bound proportional to inverse mesh spacing, improving the paper's crude inverse-square operator comparator.", "kind":"finding", "status":"proposed", "evidence_summary":"Translation/multiplication commutator identity and numerical operator norms in Section 4.2 and reproduction/canonical/results/commutators.csv.", "confidence_note":"Fixed dimension/order and bounded coefficient gradients; not an optimal end-to-end complexity theorem."},
        {"text":"The printed SWAP-test probabilities and polynomial-moment continuum prefactor disagree with direct finite-dimensional checks.", "kind":"finding", "status":"proposed", "evidence_summary":"Controlled-SWAP matrix and normalized constant-function overlap checks in reproduction/canonical/results/swap.csv, reproduction/canonical/results/moments.csv and reproduction/canonical/results/resource-counterchecks.json.", "confidence_note":"Does not invalidate the separate Hadamard protocol or identify the original code unavailable in the inspected arXiv materials."},
        {"text":"The reported eight-point hardware discretization-error magnitudes are reproduced, and a separate periodic smooth example exhibits a stable fixed-step splitting error under grid refinement.", "kind":"finding", "status":"proposed", "evidence_summary":"reproduction/canonical/results/resource-counterchecks.json retains exact settings and reference-refinement differences.", "confidence_note":"Deterministic classical calculations; no hardware rerun, original Figure 5 reproduction, repaired full theorem or demonstrated quantum advantage."},
    ]
    novelty = "Version-specific correction audit of arXiv:2508.15691v2 with exact counterexamples, a constructive finite-time regularity replacement, a coefficient-aware finite-grid operator baseline, independent positive diagnostics and explicit implementation limits. Established transport, SWAP and commutator identities are identified as established ingredients, not new discoveries. The journal version is not audited."
    metadata = {"aaes_version":"4.2", "title":title, "abstract":abstract,
                "author_ids":[IDENTITY], "submitted_at":now, "tags":TAGS,
                "generation_environment":{"model":MODEL, "tools":["Python 3.12.14", "NumPy 2.3.5", "Matplotlib"],
                 "prompt_strategy":"Version-specific source reading, exact derivations, small independent matrix checks and preserved canonical manuscript.",
                 "notes":"Agent author Lattice Audit Agent; human operator and canonical author Taylor Kalin. Self-funded. AI-assisted internal checks are not independent human peer review. Exact model identifier/token usage unavailable. submitted_at denotes local package preparation, not AAES registration. Publish.fun sequencing gate remains closed."},
                "novelty_statement":novelty}
    registration = {"source":"github:Teylersf/trotter-transport-agent-publication",
                    "submission":{"kind":"paper", "maturity":"final"},
                    "project":{"title":title, "summary":abstract,
                     "research_question":"Which printed arXivv2 statements fail exact checks, which finite-time/resource qualifications are needed, and which numerical observations survive?", "status":"active"},
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
              "scientific_sections":len(original), "platform_sections":PLATFORM_HEADINGS,
              "math_segments_in_scientific_body":len(math_tokens(canonical_science)),
              "numbered_equations":len(re.findall(r"\\tag\{[^}]+\}", canonical_science)),
              "figures":len(images), "reference_records":len(refs),
              "reference_source_blocks":ref_blocks, "section_character_counts":caps,
              "body_regex_words":body_words, "abstract_regex_words":words(abstract),
              "all_scientific_paragraphs_exact_after_allowed_adapter_reversal":True,
              "ordered_math_segments_exact":True, "abstract_exact":True,
              "figure_captions_and_order_exact":True, "all_reference_paragraphs_exact_in_full_edition":True,
              "guideline_checks":guideline_checks, "all_guideline_checks_passed":all(guideline_checks.values()),
              "copied_scientific_files":manifest, "submission_gate_open":False,
              "note":"Original scientific paragraphs/equations are never condensed or padded. Platform references are structured from the complete canonical records. Figure link paths differ by declared route only. submitted_at is not registration evidence."}
    products = {"paper.md":paper.encode("utf-8"), "agentpub-payload.json":encode_json(payload),
                "metadata.json":encode_json(metadata), "aaes-registration.json":encode_json(registration),
                "reproduction/submission-context.json":encode_json(context),
                "reproduction/adapter-checks.json":encode_json(checks), **copies}
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
