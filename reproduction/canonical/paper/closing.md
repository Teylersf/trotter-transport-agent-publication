## 7. Limitations, reproducibility and disclosures

This audit tests the exact supplied edition. The journal version and its supplements remain unverified. The original source archive does not identify the code used to make the transport plots or provide complete hardware execution records. We consequently cannot determine which displayed mistakes were merely typesetting or convention errors and which, if any, entered a calculation. We do not infer fabrication, misconduct, intent or the failure of the authors' underlying approach from these observations.

We have not reproduced the full two-dimensional figures from the original paper. Their captions and nearby equations use different centered-coordinate conventions; some Gaussian centers are outside the displayed unit-square domain unless an unstated recentering is supplied. The coefficients linear in coordinates also need treatment at a periodic seam. These are specification gaps, not evidence that a plotted result is false. Our periodic diagnostic avoids those ambiguities by defining smooth periodic coefficients and its initial function explicitly. Original hardware outcomes were not rerun; only their claimed deterministic discretization errors were independently checked.

The constructive operator estimate is a bound, not an optimized complexity theorem. It fixes order, dimension and coefficient regularity; it does not assume these constants stay benign as a physical problem develops fine scales. Likewise, the flow estimate controls finite-time regularity but can be very pessimistic. Neither repairs all original proof constants automatically. A complete revised algorithmic theorem should present its input family, normalization lower bound on sufficiently fine grids, error allocation, time dependence, oracle or circuit access, and desired physical observable in one statement.

**Data and code availability.** All original audit code, calculated CSV/JSON outputs and newly created figures are available in the accompanying public repository, https://github.com/Teylersf/trotter-transport-audit . Run `python experiments/reproduce.py` and `python experiments/resource_counterchecks.py` after installing the listed requirements. The first regenerates its figures and records the software environment; the second emits the independent hardware-magnitude and periodic-evolution checks. The original third-party PDF and TeX are linked through their official versioned URLs rather than republished in this repository. Its scientific release records the exact code revision and file hashes; publication receipts are separate from numerical evidence.

The immutable scientific code and numerical-data snapshot is commit `1fb4be68eecce95b93adb8026c4e3d29fb442583` ([view snapshot](https://github.com/Teylersf/trotter-transport-audit/tree/1fb4be68eecce95b93adb8026c4e3d29fb442583)). Later packaging commits add this provenance statement and the compiled PDF without changing that numerical snapshot.

**Authorship and assistance.** Taylor Kalin is the author and is responsible for this audit's claims and release. AI tools assisted with literature retrieval, derivation checks, code, independent internal reviews and manuscript drafting. These checks are not represented as independent human peer review. Agent-only venues, if used, receive a separately identified agent edition with Taylor Kalin credited as the human operator; that platform requirement does not change this canonical byline.

**Funding and interests.** The author self-funded this study and reports no outside funding. No competing interests have been reported for this study. No original author, institution or publisher endorsed this audit. The manuscript and original figures are licensed CC BY 4.0; original audit code is MIT licensed. Third-party works retain their own licenses.

**Preprint and review disclosure.** The GitHub release and any AiraXiv deposit are public preprints. Publish.fun, if submitted, conducts AI review. AgentPub and AAES submissions are sequenced after a final disposition ending that review, verified publication, or formal release, consistent with its current exclusivity policy. A completed round requesting revisions is not a release. A submission receipt, a publicly visible record, or an automated review is not described as independent human peer-review acceptance. Actual venue states are recorded separately and may change after this version is frozen.

## 8. Conclusion

The supplied arXiv v2 contains concrete mathematical errors requiring correction. The most consequential are the false conservation claim for derivative norms, the controlled-SWAP readout identity, and inconsistent equations for transport direction and Liouville evolution. Several normalization and index errors can be repaired locally. These findings are supported by exact counterexamples and small reproducible matrix calculations rather than speculation about unavailable implementation code.

The central smooth-state motivation remains useful. With finite-time regularity constants retained, selected transport states can have splitting errors that remain moderate as the grid is refined, as our independent periodic example illustrates. A coefficient-aware operator analysis also improves the chosen crude comparison before vector dependence is used. A corrected paper should state both the surviving benefit and the conditions under which it holds, then account for state preparation, circuit precision and measurement of the requested physical output before asserting an overall advantage.

## References

[1] J. Zylberman, T. Fredon, N. F. Loureiro and F. Debbasch, *Trotter-based quantum algorithm for solving transport equations with exponentially fewer time-steps*, arXiv:2508.15691v2 (25 August 2025). https://arxiv.org/abs/2508.15691v2 ; versioned PDF: https://arxiv.org/pdf/2508.15691v2 ; source: https://arxiv.org/src/2508.15691v2 . **Audited edition.**

[2] J. Zylberman, T. Fredon, N. F. Loureiro and F. Debbasch, same title, *Quantum Science and Technology* **11**, 025015 (2026). https://doi.org/10.1088/2058-9565/ae488e . **Existence and bibliographic metadata verified; full journal text not audited.**

[3] D. An, D. Fang and L. Lin, *Time-dependent unbounded Hamiltonian simulation with vector norm scaling*, *Quantum* **5**, 459 (2021). https://doi.org/10.22331/q-2021-05-26-459 ; https://arxiv.org/abs/2012.13105v3 .

[4] H. Buhrman, R. Cleve, J. Watrous and R. de Wolf, *Quantum Fingerprinting*, *Physical Review Letters* **87**, 167902 (2001). https://doi.org/10.1103/PhysRevLett.87.167902 ; https://arxiv.org/abs/quant-ph/0102001v1 . The controlled-SWAP probability is derived in Section 2 of the versioned preprint.

[5] G. Brassard, P. Hoyer, M. Mosca and A. Tapp, *Quantum Amplitude Amplification and Estimation*, Contemporary Mathematics **305**, 53-74 (2002); preprint (2000). https://arxiv.org/abs/quant-ph/0005055 .

[6] A. M. Childs, Y. Su, M. C. Tran, N. Wiebe and S. Zhu, *Theory of Trotter Error with Commutator Scaling*, *Physical Review X* **11**, 011020 (2021). https://doi.org/10.1103/PhysRevX.11.011020 ; https://arxiv.org/abs/1912.08854 . The distinction between commutator-aware and crude product-norm bounds provides context for Section 4.2.

[7] J. Welch, D. Greenbaum, S. Mostame and A. Aspuru-Guzik, *Efficient quantum circuits for diagonal unitaries without ancillas*, *New Journal of Physics* **16**, 033040 (2014). https://doi.org/10.1088/1367-2630/16/3/033040 ; https://arxiv.org/abs/1306.3991 .

[8] J. Zylberman, U. Nzongani, A. Simonetto and F. Debbasch, *Efficient Quantum Circuits for Non-Unitary and Unitary Diagonal Operators with Space-Time-Accuracy Trade-Offs*, *ACM Transactions on Quantum Computing* **6**(2), Article 15 (2025). https://doi.org/10.1145/3718348 ; https://arxiv.org/abs/2404.02819 .
