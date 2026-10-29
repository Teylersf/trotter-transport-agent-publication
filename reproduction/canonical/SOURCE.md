# Audited editions and provenance

Version 1.1.0 compares the supplied arXiv edition with the subsequently obtained journal version. The public [journal concordance](data/journal-comparison.json) records exact printed/PDF page mappings, equation labels and statuses for all ten correction groups. All ten persist in the directly inspected journal locations. This is a comparison of printed statements, not a reconstruction of unavailable original software or hardware jobs.

## arXiv v2

Audited edition: Julien Zylberman, Thibault Fredon, Nuno F. Loureiro and Fabrice Debbasch, *Trotter-based quantum algorithm for solving transport equations with exponentially fewer time-steps*, **arXiv:2508.15691v2**, submitted 25 August 2025.

- [Versioned abstract](https://arxiv.org/abs/2508.15691v2)
- [Official PDF](https://arxiv.org/pdf/2508.15691v2)
- [Official source archive](https://arxiv.org/src/2508.15691v2)
- PDF: 34 pages; 4,798,118 bytes; SHA-256 `8c3e5bf0c6c063bb96f383066c8a5640659e6a69a40a4d990e90901dd56d0fd2`.
- Source archive: 4,057,018 bytes; SHA-256 `dd9db8768c8df20a9d27100bcddbe517af940d52a44429ebf30a186da65b44af`.

The user-supplied PDF matches the versioned official PDF byte for byte. All 34 pages and the official TeX were audited. The inspected archive contains TeX, bibliography and figure images, but no executable simulation code or raw shot records. This is an archive-specific statement. Its license is CC BY-NC-ND 4.0; the original PDF and full source are not included in this audit repository.

## Published journal article

The same four authors published the [journal article](https://doi.org/10.1088/2058-9565/ae488e) in *Quantum Science and Technology* **11**(2), 025015, online 3 March 2026. Its first article page records receipt on 2 October 2025, revision on 2 February 2026, and acceptance on 20 February 2026.

- [Official publisher PDF](https://iopscience.iop.org/article/10.1088/2058-9565/ae488e/pdf)
- Successful unauthenticated publisher request initiated 29 October 2026 at 15:57:49 UTC.
- PDF: 34 pages, comprising a publisher cover and printed article pp.1-33; 2,014,929 bytes.
- SHA-256 of the obtained copy: `1b8f24ed2bcd4979526977581fc795f80d90a6efeacfbe28e65339cf8b4803e1`.
- License on the first article page: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Initial access attempts encountered a publisher challenge; the later ordinary PDF request succeeded. The journal comparison uses its actual PDF text and direct rendered-page checks of the registered statements. It does not infer persistence from an open-access metadata label or search excerpts. Journal printed page $n$ is one-based PDF page $n+1$ because of the publisher cover.

The journal includes substantive added discussion of Gaussian-width dependence and conditional optimal-time Hamiltonian simulation costs on printed p.18, and periodic-boundary extensions on printed p.19. The audit credits these additions without treating their new scaling claims as independently established here. It also distinguishes the journal's data-availability statement from the executable author code and complete hardware records that were not obtained.

The original v1.0.0 preprint-only scope remains preserved in its immutable release. Appendix A in the revision attributes its quoted words and reproduced equations to arXiv v2 [1], while Section 3.1 provides the directly checked journal [2] correspondence. Full third-party source files and figures are not included in this repository; attributed excerpts retain their applicable source rights rather than the licenses covering the audit's own work.

The audit's exact scientific snapshot `1fb4be68eecce95b93adb8026c4e3d29fb442583` is separately archived as [computational version 1.0.0 on Zenodo](https://doi.org/10.5281/zenodo.23770769). Its ZIP has 625,315 bytes and SHA-256 `ef401c3744e4fa2ef7e9139ede5d1d6d07c077ecc513099b711b2a119a3eef68`. That archive preserves the numerical inputs, programs and outputs; the journal comparison is part of the later manuscript revision.

Primary context includes [An-Fang-Lin](https://doi.org/10.22331/q-2021-05-26-459), [Buhrman et al.](https://arxiv.org/abs/quant-ph/0102001v1), [Childs et al.](https://doi.org/10.1103/PhysRevX.11.011020), and the strong-error/no-go result of [Burgarth et al.](https://doi.org/10.1103/PhysRevResearch.6.043155). The related [anisotropic diffusion/convection preprint](https://arxiv.org/abs/2603.08799v1) and its separately identified proceedings article are distinct versioned works. See the paper's references for the full prior-art and circuit context.
