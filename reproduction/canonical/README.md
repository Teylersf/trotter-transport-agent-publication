# Corrections and resource bounds for the Trotter quantum transport algorithm

**Author: Taylor Kalin** · [taylorkalin.com](https://taylorkalin.com) · [ORCID](https://orcid.org/0009-0003-9000-9315)

Version 1.1.0 compares arXiv:2508.15691v2 with the directly obtained *Quantum Science and Technology* 11, 025015 (2026) journal article. All ten registered correction groups persist in the checked journal PDF. Exact counterexamples, finite-grid bounds and reproducible numerical checks distinguish printed equation failures from implementation uncertainties and resource qualifications. The journal's added Gaussian-width, alternative-simulation-cost and boundary discussions are credited. The frozen [v1.0.0 release](https://github.com/Teylersf/trotter-transport-audit/releases/tag/v1.0.0) preserves the original preprint-only audit.

- [Read the full paper](paper/manuscript.md) or [typeset PDF](paper/main.pdf).
- [Source provenance](SOURCE.md), [calculated results](results/summary.json), [independent numerical evidence](results/resource-counterchecks.json).
- [Journal concordance](data/journal-comparison.json) maps the ten finding groups to both editions. The paper includes attributed source statements and numerical provenance as Appendices A and B.
- [Publication status](submissions/publication-status.json). A preprint, review submission and accepted article are different states.

The main corrections concern derivative-norm conservation, controlled-SWAP readout, shift/Fourier conventions, moment normalization and the Lotka-Volterra Liouville sign. A coefficient-aware operator bound sharpens the comparison baseline for smooth periodic coefficients; it does not cover a discontinuous periodic seam. The reported eight-point discretization error magnitudes reproduce, and an independent smooth periodic example supports the qualitative benefit of smooth-state analysis. The audit does not prove a complete repaired vector-norm theorem, an end-to-end quantum advantage, or which displayed formulas the original software used.

## Reproduce

Python 3.12 was used. From this directory:

```powershell
python -m pip install -r requirements.txt
python experiments/resource_counterchecks.py
python experiments/reproduce.py
```

The first script emits independent measurement, hardware-magnitude and periodic-evolution checks. The second runs ten assertion groups and regenerates its CSVs, figures, environment report and SHA-256 manifest. No GPU, author implementation, quantum account or paid service is needed. These are algebraic and numerical checks, not a quantum-hardware rerun.

`experiments/build_paper.py` assembles the Markdown and LaTeX body using Pandoc. It inserts the journal concordance as Section 3.1 and includes the source-statement and numerical-provenance appendices when their input files exist. Compile `paper/latex/main.tex` with a LaTeX engine providing its listed packages, including `braket`. The self-contained LaTeX project includes its figure copies. Document assembly does not rerun or alter the frozen numerical results. Release provenance pins the scientific snapshot `1fb4be68eecce95b93adb8026c4e3d29fb442583`; its numerical manifest excludes itself.

That exact code/data snapshot is archived on [Zenodo, DOI 10.5281/zenodo.23770769](https://doi.org/10.5281/zenodo.23770769), computational version 1.0.0. The expanded manuscript version 1.1.0 retains those numerical results.

## Authorship, support and licenses

Taylor Kalin self-funded the study. AI assistance is disclosed in the paper separately from the author byline; no independent human peer review is asserted. Separately authorized agent editions name Lattice Audit Agent with Taylor Kalin as human operator when a venue requires an agent author.

Original audit code: [MIT](LICENSE-CODE). Manuscript and newly created figures: [CC BY 4.0](LICENSE-MANUSCRIPT). The full third-party PDFs, source archives and figures are linked rather than republished. Brief attributed source excerpts and equation reproductions retain the applicable third-party rights and are excluded from the audit's own license grants. No credentials are stored in this public repository.
