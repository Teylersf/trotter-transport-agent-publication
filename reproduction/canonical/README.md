# Corrections and resource bounds for the arXiv v2 Trotter transport algorithm

**Author: Taylor Kalin** · [taylorkalin.com](https://taylorkalin.com) · [ORCID](https://orcid.org/0009-0003-9000-9315)

A version-specific correction paper with exact counterexamples, constructive bounds and reproducible numerical checks of arXiv:2508.15691v2. The later journal article was identified but its full text could not be verified; this repository makes no claim that these errors survive there.

- [Read the full paper](paper/manuscript.md) or [typeset PDF](paper/main.pdf).
- [Source provenance](SOURCE.md), [calculated results](results/summary.json), [independent numerical evidence](results/resource-counterchecks.json).
- [Publication status](submissions/publication-status.json). A preprint, review submission and accepted article are different states.

The main corrections concern derivative-norm conservation, controlled-SWAP readout, shift/Fourier conventions, moment normalization and the Lotka-Volterra Liouville sign. A coefficient-aware operator bound sharpens the comparison baseline. The reported eight-point discretization error magnitudes reproduce, and an independent smooth periodic example supports the qualitative benefit of smooth-state analysis.

## Reproduce

Python 3.12 was used. From this directory:

```powershell
python -m pip install -r requirements.txt
python experiments/resource_counterchecks.py
python experiments/reproduce.py
```

The first script emits independent measurement, hardware-magnitude and periodic-evolution checks. The second runs ten assertion groups and regenerates its CSVs, figures, environment report and SHA-256 manifest. No GPU, author implementation, quantum account or paid service is needed. These are algebraic and numerical checks, not a quantum-hardware rerun.

`experiments/build_paper.py` assembles the Markdown and LaTeX body using Pandoc. Compile `paper/latex/main.tex` with a LaTeX engine providing its listed packages. The self-contained LaTeX project includes its figure copies. Release provenance pins the exact scientific code snapshot; the manifest excludes itself.

## Authorship, support and licenses

Taylor Kalin self-funded the study. AI assistance is disclosed in the paper separately from the author byline; no independent human peer review is asserted. Separately authorized agent editions name Lattice Audit Agent with Taylor Kalin as human operator when a venue requires an agent author.

Original audit code: [MIT](LICENSE-CODE). Manuscript and newly created figures: [CC BY 4.0](LICENSE-MANUSCRIPT). The original third-party paper is linked, not republished. No credentials are stored in this public repository.
