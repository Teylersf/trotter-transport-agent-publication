## Journal edition and statement concordance

The version comparison now includes the published article [2] as well as the previously audited arXiv:2508.15691v2 [1]. The official publisher PDF was obtained through an unauthenticated request initiated on 29 October 2026 at 15:57:49 UTC; it is available through the PDF download action on the [article's DOI landing page](https://doi.org/10.1088/2058-9565/ae488e). It has 2,014,929 bytes and SHA-256 `1b8f24ed2bcd4979526977581fc795f80d90a6efeacfbe28e65339cf8b4803e1`. Its 34 PDF pages comprise an unnumbered publisher cover followed by printed article pages 1-33. The article identifies its publication as *Quantum Science and Technology* **11**, 025015, DOI [10.1088/2058-9565/ae488e](https://doi.org/10.1088/2058-9565/ae488e), published 3 March 2026 under CC BY 4.0. The title, four authors, DOI, dates and license were checked on its first printed page.

Version 1 of this audit accurately recorded the access challenges encountered in its available sessions and restricted its conclusions to the supplied preprint. The subsequent successful retrieval makes a direct journal comparison possible. The comparison below uses the downloaded PDF, extracted text and direct inspection of the relevant rendered formulas. Its conclusions do not rely on the publisher's open-access label or search-index excerpts. The public machine-readable record is `data/journal-comparison.json`.

The table retains the correction IDs used in the original registry. An arXiv page is the page printed in that preprint; a journal page is the printed article page, followed by its one-based PDF page in parentheses. Journal equation numbering is given as printed. The status **persists** means the specified printed discrepancy remains in this obtained journal edition. It does not establish which formulas were used in the authors' unavailable implementation code or how the published figures were generated.

| ID | arXiv v2 locator | Journal locator: printed page (PDF page), label | Status | Description |
|---|---|---|---|---|
| C1 | p.12, paragraph after Theorem III.4 and footnote 10; p.29, Appendix B opening | p.11 (12), paragraph after Theorem 3.4 and footnote 13; p.26 (27), Appendix B after Eq. (65) | Persists | The assertion that all spatial derivative norms are conserved remains. Cross-coordinate velocity gradients supply the omitted forcing. |
| C2 | pp.27-28, Eqs. (A15)-(A16) and Fig.14 | pp.24-25 (25-26), Appendix A.3.2, Eqs. (58)-(59) and Fig.13 | Persists | The standard controlled-SWAP circuit still has a real-overlap probability and an imaginary-overlap phase-gate claim. |
| C3 | p.8, Eq. (17) and the following coefficient definition | p.7 (8), Eq. (17) and the following coefficient definition | Persists | The finite-grid normalization is paired with the same reciprocal continuum prefactor. |
| C4 | p.4, Eqs. (5)-(6); p.9, Eq. (20); p.30, Eq. (B4) | p.4 (5), Eqs. (5)-(6); p.9 (10), Eq. (20); p.26 (27), Eq. (67) | Persists | The forward ket shift and stencil retain an amplitude derivative opposite to the derivative lemma. |
| C5 | p.15, Eq. (39) | p.14 (15), Eq. (39); compare p.6 (7), Eq. (14) | Persists | Both displayed QFTs remain forward transforms, producing the wrong zero-time identity. |
| C6 | p.17, Eqs. (42)-(43) | p.15 (16), Eqs. (42)-(43) | Persists | The density equation still uses the wrong sign for its $q$-derivative coefficient. |
| C7 | p.11, paragraph below Eq. (26) | p.10 (11), below Eq. (26); compare p.30 (31), Eq. (83) | Persists | The main-text stencil constant still uses signed coefficients; the appendix already uses absolute values. |
| C8 | p.11, compact maximum in Theorem III.4 | p.11 (12), compact maximum in Theorem 3.4 | Persists | The maximum still omits one ordered orientation present in the preceding pair sum. |
| C9 | p.24, Eq. (A5); p.25, Eq. (A10) and following size choice | p.21 (22), Eq. (48); p.22 (23), Eq. (53) and following size choice | Persists | The inclusive Walsh endpoint and the per-axis rather than shared error allocation both remain. |
| C10 | p.33, paragraph after Eq. (B20) | p.30 (31), paragraph after Eq. (83) | Persists | The printed exponent is $2-1/(2p)$; balanced refinement gives $2-1/p$ at fixed final time. |

For C1, the first sentence of journal footnote 13, printed p.11 (PDF p.12), states verbatim [2]:

> The $L^2$ norm of any derivative of $f$ is constant over time, equal to its initial value at time $t=0$.

The remainder of the footnote refers to Appendix B. The opening of that appendix, printed p.26 (PDF p.27) immediately after Eq. (65), repeats the homogeneous derivative-equation argument. The same smooth periodic shear counterexample therefore applies to the journal statement. This does not remove the need to keep the time-dependent derivative maxima already present in Theorem 3.4, nor does replacing the conservation claim alone prove the entire vector-norm theorem.

For C2, journal Eq. (58), printed p.24 (PDF p.25), and Fig.13, printed p.25 (PDF p.26), retain the controlled-SWAP circuit. Immediately after Eq. (58), journal Eq. (59), printed p.24 (PDF p.25), reads [2]:

$$
P(0)=\frac{1+\Re(\langle\phi|\psi\rangle)}{2},\qquad
P(1)=\frac{1-\Re(\langle\phi|\psi\rangle)}{2}.
$$

The circuit instead returns the absolute square of the overlap in these expressions. Its phase-gate modification also cannot recover the imaginary overlap. The journal's separate Hadamard-test construction remains a possible coherent route to signed matrix elements. For C3, the definition following journal Eq. (17) still gives $C_{\vec k}=1/\sqrt{\prod_j(2k_j+1)}$; the normalization in the same equation requires its reciprocal. The finite-grid checks in the audit apply unchanged.

The remaining rows preserve the original qualifications. C7 is a local inconsistency between main text and appendix. C10 corrects an arithmetic exponent while leaving that term higher order than $\epsilon$ for fixed $T$ and $p\geq2$. The table records ten persistent printed discrepancies, with differing mathematical consequences, rather than ten independent demonstrations that the algorithm or its numerical implementation fails.

### Added qualifications in the journal discussion

The journal has substantive additions that affect how the resource critique should be framed. Section 5.2, printed p.18 (PDF p.19), explicitly discusses dependence on a Gaussian localization width $\sigma$. The authors report a vector-bound step scale $L=O(\sigma^{-2})$ and an operator comparator $O(\sigma^{-(4+2/p)})$, explain how narrowing the packet changes predicted resources, and warn that other initial functions may behave differently. The present concordance records this added analysis without independently certifying the tightness of its new width exponents. The revised audit should credit the discussion of initial-function dependence. Its separate questions about propagated derivative growth and state-preparation success probability remain specific claims requiring their own evidence.

The same printed p.18 adds a conditional comparison with alternative Hamiltonian simulation methods. It discusses replacing the relevant contribution $O(T^2(C_{\rm diag}+2C_{\rm QFT})/\epsilon^2)$ by $O(T(C_{\rm diag}+C_{\rm derivative})\log(1/\epsilon)/\epsilon)$ under suitable assumptions. Coefficient and derivative block-encoding costs are identified separately, and the remaining measurement factor is retained. The journal also discusses non-unitary block encodings and their success probabilities. These passages acknowledge implementation and output costs; they should be cited when delimiting the present audit's narrower resource qualifications.

Section 5.2, printed p.19 (PDF p.20), explicitly identifies periodic boundaries as a strong assumption. It sketches extensions through nonperiodic block encodings, linear combinations of Hamiltonian simulations, or boundary penalties, and identifies further analysis needed to recover vector-norm scaling. This is an acknowledged research direction in the journal. The audited theorem still uses its stated periodic setting; the extension discussion supplies no completed nonperiodic replacement theorem.

Together, the direct concordance and these additions replace the earlier unresolved journal-version boundary. The corrected audit can now state precisely which printed findings survive publication while engaging with the journal's expanded treatment of input dependence, alternative simulation costs and boundaries. It continues to distinguish equation-level corrections from claims about unavailable software, hardware outcomes or an end-to-end quantum advantage.
