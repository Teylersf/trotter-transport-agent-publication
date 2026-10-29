# Reproduction and preparation of version 1.1.0

The numerical scientific snapshot is `1fb4be68eecce95b93adb8026c4e3d29fb442583`. Exact current manuscript, concordance and copy hashes are in `adapter-checks.json`; updated manuscript/provenance packaging is distinct from unchanged numerical results.

## Numerical checks

The `canonical/` directory contains approved canonical science copied byte-for-byte. From this repository:

```console
cd reproduction/canonical
python -m pip install -r requirements.txt
python experiments/reproduce.py
python experiments/resource_counterchecks.py
```

These CPU calculations use NumPy, with Matplotlib for figures. They test specified equations and independent smooth periodic examples. They do not rerun the original hardware or reproduce the source's two-dimensional figures. The supplied arXiv v2 and the directly obtained published journal PDF were compared. All ten registered correction groups persist in the checked journal passages, with differing mathematical consequences. The added journal discussions of localization width, implementation/output costs and periodic boundaries are credited. This is not a complete audit of every new journal passage and does not identify the equations used by original code unavailable in the inspected materials.

## Offline preparation

```console
python reproduction/prepare_packages.py --expected-code-commit 1fb4be68eecce95b93adb8026c4e3d29fb442583
```

Keep the canonical checkout beside this repository, or supply `--canonical-root`. `--expected-manuscript-sha256` can require the exact final manuscript. Preparation performs no network or Git operations, scientific execution, credential access, registration, submission or review call. It checks current inputs before output writes. It can be repeated after authorized canonical corrections.

All required scientific sections 1–8 remain in order; nested Methods headings are retained. Canonical sections 4+5 are grouped under AgentPub Results. All complete appendices remain after Conclusion in paper.md and are grouped, without shortening, in one optional AgentPub Appendix section. References remain complete in paper.md and are structured outside AgentPub section contents. Every scientific paragraph and complete section body is compared after reversing only allowed authorship/figure-link adaptations; complete proofs are covered by that equality. Math, tables, source blockquotes, code fences and figure captions/order also have separate exact inventories. No scientific simplification, truncation, padding or math-whitespace compression is performed.

Every platform section, including Appendix, must fit both Unicode and UTF-16 counts within 49,000. The saved official template supplies other format checks. Any body-length/ref-count guideline shortfall is reported instead of repaired by changing science. Copied files and the source-concordance JSON have exact byte hashes. Private notes, credentials, caches, raw third-party PDFs and operational venue receipts are excluded.

Every invocation leaves all submission gates false. A later final disposition ending review, verified publication or formal release requires separately verified context; a revision request is not release. Agent-only authorship is explicit, Taylor Kalin's canonical authorship is retained, and AI-assisted checks are not independent human peer review. Token usage is unrecorded; AgentPub's `-1` integer is expressly a missing-data sentinel.
