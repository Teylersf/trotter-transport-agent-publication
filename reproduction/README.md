# Reproduction and agent-edition preparation

The canonical scientific revision is `1fb4be68eecce95b93adb8026c4e3d29fb442583`. The canonical manuscript records this immutable snapshot. The preparation checks record its exact manuscript hash and every copied file hash; rerun preparation after an authorized canonical correction.

## Reproduce the numerical checks

The directory `canonical/` holds exact copies of the approved canonical experiments, results, figures, requirements and paper sources. It excludes private working notes, venue receipts, caches and credentials. From this repository:

```console
cd reproduction/canonical
python -m pip install -r requirements.txt
python experiments/reproduce.py
python experiments/resource_counterchecks.py
```

The first script regenerates the shear, translation, commutator, moment and SWAP checks and three figures. The second emits the independent matrix checks, reported hardware-error magnitudes and separate smooth periodic evolution diagnostic. Both run on CPU with NumPy; the first also uses Matplotlib. No author simulation code, quantum hardware, credential or external dataset is required. These calculations do not reproduce the original paper's two-dimensional figures or rerun its hardware experiment. A refined Strang reference is checked by further refinement, rather than treated as an exact solution.

`canonical/data/reproducibility.json`, when present in the canonical release, supplies the parent's additional provenance. Local absence is not replaced with fabricated provenance. The copied original manuscript preserves the canonical Taylor Kalin byline. The root `paper.md` is the separately disclosed agent edition.

## Regenerate this local package

Keep the canonical `trotter-transport-audit` checkout beside this repository. Run:

```console
python reproduction/prepare_packages.py --expected-code-commit 1fb4be68eecce95b93adb8026c4e3d29fb442583
```

An explicit `--canonical-root` is supported. An optional `--expected-manuscript-sha256` requires an exact manuscript snapshot. The expected 40-character scientific pin must appear in the canonical manuscript. The script reads a sanitized snapshot of the official saved venue schemas, never credentials. It performs no network or Git operations, launches no scientific calculation, and implements no submission or review calls.

Preparation checks every scientific section against its canonical text after reversing only the declared authorship-disclosure and figure-link changes. It separately checks ordered math tokens, all scientific paragraphs, abstract, figure captions/order and complete reference paragraphs. AgentPub maps canonical sections 1, 2, 3, 4+5, 6, 7 and 8 onto Introduction, Related Work, Methodology, Results, Discussion, Limitations and Conclusion. Section 4 and 5 headings remain visible inside Results; their content is not shortened. References are structured outside the seven section contents, while the full manuscript retains every complete bibliographic paragraph.

The adapter checks both Unicode-codepoint and UTF-16-unit section lengths against a conservative 49,000-character limit. It also checks title, abstract, research-article word range, reference count and required section order against the saved official template. Scientific content is neither padded to reach a limit nor truncated to fit one. Every copied scientific file is verified byte-for-byte after writing, and changed canonical inputs cause preparation to stop.

The schema snapshot records public source URLs and raw-document hashes. Its OpenAPI metadata and prose guidance do not establish what a future venue renderer supports. Token usage is unknown: the AgentPub payload explicitly uses `total_tokens=-1` as a missing-data sentinel, not a measured value. No public article or registration ID is invented.

## Sequencing and publication limits

Every run of this preparer writes `publishfun_state=pending_review` and keeps all submission gates false. These are preparation defaults, not an assertion about a future review outcome. A later verified completed or released review requires an explicit context update before submission; this script cannot open that gate. Public repository visibility, current agent identity and AAES Discussions/category availability also remain unverified locally. The existing identity Gist is referenced, not recreated. No failed registration should be retried blindly.

Publish.fun performs AI review. Internal AI-assisted checks and an eventual automated venue review must not be described as independent human peer review. The canonical manuscript, source-version limitation and all qualifications on quantum advantage remain attached to both editions.
