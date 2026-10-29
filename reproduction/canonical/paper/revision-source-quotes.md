# Source quotations and equation concordance for the revision

This is a separate revision working sheet. It is not incorporated into the published manuscript and does not change version 1.0.0, its numerical code or its publication record. Finding IDs refer to the existing C1–C10 correction registry.

**Audited source only:** J. Zylberman, T. Fredon, N. F. Loureiro and F. Debbasch, *Trotter-based quantum algorithm for solving transport equations with exponentially fewer time-steps*, arXiv:2508.15691v2. [Versioned record](https://arxiv.org/abs/2508.15691v2), [PDF](https://arxiv.org/pdf/2508.15691v2), [official source archive](https://arxiv.org/src/2508.15691v2). No finding below asserts anything about the later journal text.

The supplied/official v2 PDF has SHA-256 `8c3e5bf0c6c063bb96f383066c8a5640659e6a69a40a4d990e90901dd56d0fd2`; the extracted official `main.tex` has SHA-256 `6557fa20db60f5fb3edbcb2dc9ca94b080bcfb1f5072c066e6d2fe75c5efca1e`. Page references below are printed PDF pages; they also equal the one-based PDF page positions. TeX line numbers apply to that exact source file.

**Reading convention.** Blockquotes marked *verbatim text* retain the source's words; inline mathematical notation is typeset from its TeX. Displays marked *source equation reproduction* reproduce the specified mathematics, including the disputed signs, bounds and index ranges. They are newly typeset expressions rather than a claim of byte-for-byte TeX quotation. Displays marked *audit contrast* are our deductions or corrections and are not attributed to the source. An excerpt of a long display is identified as an excerpt.

**Visual verification.** Each quoted passage and disputed expression was independently checked against rendered source PDF pages 4, 8, 9, 11, 12, 15, 17, 24, 25, 27, 28, 29 and 33, in addition to the TeX. In particular, neither an OCR omission of an inverse nor a lost absolute-value bar is being inferred solely from extracted text.

**Third-party material.** These brief attributed excerpts are included for the specific correction discussion. The source PDF, TeX, figures and other third-party material are excluded from any CC BY or MIT license covering our own manuscript, figures or code; their rights and any applicable source license remain with their respective holders. This sheet does not republish the source archive or its figures or imply endorsement by its authors or publisher.

## C1. Spatial-derivative norm conservation

**Locator:** p.12, footnote 10 and the paragraph following Theorem III.4; p.29, Appendix B, paragraph between Eq. (B2) and “Proof of Lemma III.1”. TeX lines 495 and 1100.

**Verbatim text, footnote 10:**

> The $L^2$ norm of any derivative of $f$ is constant over time, equal to its initial value at time $t=0$.

**Verbatim text, Appendix B fragment:**

> then any derivative of $f$ is solution of the same PDE

**Source equation reproduction, the equality used in the p.12 paragraph:**

$$
\frac{\|\partial_{x_m}f_t\|_{L^2}}{\|f_0\|_{L^2}}
=\frac{\|\partial_{x_m}f_0\|_{L^2}}{\|f_0\|_{L^2}}.
$$

**Audit contrast:** differentiating the source transport equation produces

$$
(\partial_t+c\cdot\nabla)\partial_\ell f
=-\sum_j(\partial_\ell c_j)\partial_j f.
$$

The issue is the displayed replacement of time-dependent derivative norms by their initial values. It does not establish that every finite-time smooth-state estimate fails. The source theorem's longer leading coefficient already contains maxima over the time interval; that fact must remain visible when explaining the correction.

## C2. Controlled-SWAP output and the phase claim

**Locator:** p.27, Appendix A.3.b, Eqs. (A15)–(A16) and the paragraph immediately after (A16); p.28, Figure 14 and its caption. TeX lines 993–1009 and 1025. The paragraph belongs to the SWAP subsection, not the preceding Hadamard subsection.

**Verbatim text, the sentence following Eq. (A16):**

> and the difference $P(0)-P(1)$ gives the value $\Re(\braket{\phi|\psi})$.

**Source equation reproduction, the final state in Eq. (A15):**

$$
\frac{|\psi\rangle|\phi\rangle+|\phi\rangle|\psi\rangle}{2}|0\rangle
+\frac{|\psi\rangle|\phi\rangle-|\phi\rangle|\psi\rangle}{2}|1\rangle.
$$

**Source equation reproduction, Eq. (A16):**

$$
P(0)=\frac{1+\Re\langle\phi|\psi\rangle}{2},\qquad
P(1)=\frac{1-\Re\langle\phi|\psi\rangle}{2}.
$$

The following source prose and Figure 14 caption also propose adding the control phase

$$
\hat P=|0\rangle\langle0|+i|1\rangle\langle1|
$$

between the two Hadamards to infer the imaginary overlap. That is a description of the source's proposal, not an additional validated protocol.

**Audit contrast:** the state in (A15) gives

$$
P(0)=\frac{1+|\langle\phi|\psi\rangle|^2}{2},\qquad
P(1)=\frac{1-|\langle\phi|\psi\rangle|^2}{2}.
$$

Both are invariant under a global phase of either independently prepared register. This corrects this SWAP route; it does not invalidate the separate coherent Hadamard-test route.

## C3. Polynomial-moment normalization

**Locator:** p.8, last line of Eq. (17) and the immediately following definitions of $\mathcal N_{\vec k}$ and $C_{\vec k}$. TeX lines 325 and 330.

**Verbatim text fragment describing $C_{\vec k}$:**

> is a constant coming from the term $\mathcal{N}_{\vec{k}}$

**Source equation reproduction, the relevant moment and definitions:**

$$
\sum_{\vec X}X_1^{k_1}\cdots X_d^{k_d}
\frac{f(\vec X,T)}{\mathcal N_{\vec k}\|f_0\|_{2,N}}
\overset{N\to+\infty}{=}
C_{\vec k}\frac{\int_{[0,1]^d}x_1^{k_1}\cdots x_d^{k_d}f(\vec x,T)\,dV}
{\|f_0\|_{L^2}},
$$

$$
\mathcal N_{\vec k}
=\sqrt{\sum_{\vec X}\bigl(X_1^{k_1}\cdots X_d^{k_d}\bigr)^2},
\qquad
C_{\vec k}=\frac{1}{\sqrt{(2k_1+1)\cdots(2k_d+1)}}.
$$

**Audit contrast:** with the source's definition of $\mathcal N_{\vec k}$, the required factor in that limit is $\sqrt{(2k_1+1)\cdots(2k_d+1)}$. The finite-grid normalized overlap is not the erroneous part. The $d=1,k=1,f=1$ example distinguishes $\sqrt3/2$ from the source's $1/(2\sqrt3)$.

## C4. Ket-shift direction and the derivative sign

**Locator:** p.4, the shift definition immediately before Eq. (5), Eqs. (5)–(6); p.9, Lemma III.1, Eq. (20). TeX lines 150–163 and 374. Eq. (B4) repeats the derivative claim on p.30, but this finding does not require using that additional passage.

**Verbatim text fragment introducing the convention:**

> is defined using the shift operators

**Source equation reproduction:**

$$
\hat S_j=\sum_{X_j}|X_j+\Delta x_j\rangle\langle X_j|,
$$

$$
\hat D_j=\hat I_1\otimes\cdots\otimes\hat I_{j-1}
\otimes\left(-i\frac{\sum_{k=-p}^{p}a_k(\hat S_j)^k}{\Delta x_j}\right)
\otimes\hat I_{j+1}\otimes\cdots\otimes\hat I_d,
\qquad\text{source Eq. (5)},
$$

$$
\frac{d|\widetilde f\rangle_t}{dt}
=-i\left(\sum_{j=1}^{d}\hat c_j(t)\hat D_j\right)|\widetilde f\rangle_t,
\qquad\text{source Eq. (6)},
$$

$$
i\hat D_j|g\rangle=|\partial_{x_j}g\rangle+O((\Delta x_j)^{2p}),
\qquad\text{source Eq. (20)}.
$$

**Audit contrast:** the stated forward ket shift has coefficient action $(\hat S_jg)(X_j)=g(X_j-\Delta x_j)$. With the source's centered coefficients, $i\hat D_jg$ therefore approaches $-\partial_jg$. Reversing a shift convention or the derivative prefactor can resolve the inconsistency; no conclusion about the unavailable original implementation follows from choosing one repair.

## C5. Two forward QFTs in the one-dimensional propagator

**Locator:** p.15, Eq. (39), immediately after Eq. (38); compare p.6, Eq. (14), which uses opposite-side QFTs as inverses. TeX line 625; comparison Eq. (14) at line 260. The disputed Eq. (39) itself was visually checked on p.15.

**Verbatim text fragment introducing Eq. (39):**

> After the space discretization

**Source equation reproduction, Eq. (39), including both forward transforms:**

$$
|\widetilde f\rangle_t
=\widehat{QFT}\,
\exp\!\left[-i\frac{2vt}{\Delta x}
\sum_{q=0}^{p}a_q\sin(2\pi q\hat X)\right]
\widehat{QFT}\,|f_0\rangle.
$$

**Audit contrast:** at $t=0$ this is $F^2|f_0\rangle$, not the identity for a general Fourier-encoded state. One outside transform must be the inverse of the other. This is separate from, and does not negate, the reproduced numerical discretization-error magnitudes in Figure 7.

## C6. Lotka–Volterra Liouville coefficient

**Locator:** p.17, Eqs. (42)–(43), Section IV.C. TeX lines 698–707.

**Verbatim text introducing Eq. (43):**

> for which the associated Liouville equation can be written as:

**Source equation reproduction:**

$$
\dot q=-\alpha+\beta e^{-p},\qquad
\dot p=\delta-\gamma e^{-q},
\qquad\text{source Eq. (42)},
$$

$$
\partial_t\rho(q,p,t)
=(-\delta+\gamma e^{-q})\,\partial_p\rho
+(-\alpha+\beta e^{-p})\,\partial_q\rho,
\qquad\text{source Eq. (43)}.
$$

**Audit contrast:** for that divergence-free characteristic flow,

$$
\partial_t\rho=-\dot q\,\partial_q\rho-\dot p\,\partial_p\rho
=(\alpha-\beta e^{-p})\partial_q\rho
+(-\delta+\gamma e^{-q})\partial_p\rho.
$$

Only the $q$ coefficient differs between this deduction and printed (43). This is not a claim about which equation generated the source's figures.

## C7. Signed rather than absolute stencil constant

**Locator:** p.11, first paragraph below Eq. (26); compare the absolute-value definition after Eq. (B20) on p.33. TeX lines 460 and 1260.

**Verbatim text fragment describing the bound:**

> Notice that the definition of the discrete derivative operator implies

**Source equation reproduction, p.11:**

$$
\|\hat D_j\|_2\leq\frac{2C_p}{\Delta x_j},
\qquad C_p=\sum_{q=0}^{p}a_q.
$$

**Source equation reproduction, p.33 comparison definition:**

$$
C_p=\sum_{q=0}^{p}|a_q|.
$$

**Audit contrast:** the latter definition supplies the ordinary triangle-inequality bound. For $p=2$, the signed p.11 prescription gives $2C_p=7/6$, whereas the dimensionless symbol maximum at $N=32$ is approximately $1.37149428$. This is a correction to a local constant, not a change to its inverse-mesh order.

## C8. One orientation omitted from the compact maximum

**Locator:** p.11, unnumbered coefficient display inside Theorem III.4 immediately after Eq. (28). TeX lines 484–485. This is not Eq. (26)'s operator-norm coefficient.

**Verbatim text identifying the theorem:**

> Vector norm inequality

**Source equation reproduction, the full pair sum followed by its compact bound:**

$$
\begin{aligned}
\alpha'_g={1\over2}\sum_{j=1}^{d-1}\sum_{m=j+1}^{d}
\Bigg(&\|c_j\|_\infty\|\partial_{x_j}c_m\|_\infty
\max_{t\in[0,T]}\frac{\|\partial_{x_m}f_t\|_{2,N}}{\|f_0\|_{2,N}}
\\
&+\|c_m\|_\infty\|\partial_{x_m}c_j\|_\infty
\max_{t\in[0,T]}\frac{\|\partial_{x_j}f_t\|_{2,N}}{\|f_0\|_{2,N}}\Bigg)
\\
\leq {d(d-1)\over2}
\max_{\substack{1\leq m<j\leq d\\t\in[0,T]}}
&\|c_j\|_\infty\|\partial_{x_j}c_m\|_\infty
\frac{\|\partial_{x_m}f_t\|_{2,N}}{\|f_0\|_{2,N}}.
\end{aligned}
$$

**Audit contrast:** the full pair expression contains both ordered orientations. The compact maximum as printed retains only one. Replacing its index set by all $j\ne m$ covers both orientations with the displayed prefactor. The finding concerns the compact inequality, not an assertion that its preceding pair sum has the same omission.

## C9. Walsh index range and multivariate error allocation

**Locators:** p.24, Eqs. (A5)–(A7) and the sentence immediately after (A6); p.25, Eq. (A10) and its following prescription. TeX lines 847–855 and 878–880.

**Verbatim text fragment, p.24:**

> is an exact representation of $f$

**Source equation reproduction, Eqs. (A5)–(A6):**

$$
S_{f,M}=\sum_{j=0}^{M}a_j^f w_j,
\qquad
a_j^f={1\over M}\sum_{k=0}^{M-1}f(k/M)w_j(k/M).
$$

The accompanying exactness statement uses $\mathcal X_m=\{0,1/M,\ldots,(M-1)/M\}$ and $M=2^m$.

**Source equation reproduction, Eq. (A10) and the stated choice:**

$$
\|f-S_{f,\vec M}\|_\infty
\leq\sum_{i=1}^{d}{\|\partial_{x_i}f\|_\infty\over M_i},
\qquad
M_i=\left\lceil{\|\partial_{x_i}f\|_\infty\over\epsilon}\right\rceil.
$$

**Audit contrast:** an $M$-point Walsh representation has indices $0,\ldots,M-1$. The stated per-axis choice in the second display only bounds the sum by $d\epsilon$. An allocation $\epsilon_i>0$ with $\sum_i\epsilon_i\leq\epsilon$, and suitable dyadic $M_i\geq\|\partial_i f\|_\infty/\epsilon_i$, supplies the desired sufficient bound. A constant axis needs at least one term, rather than a zero-size grid. These local corrections do not disprove the availability of approximate diagonal circuits.

## C10. Coupled exponent after Eq. (B20)

**Correct locator:** p.33, Appendix B.0.c, the paragraph immediately after Eq. (B20), before Eq. (B21); TeX line 1260. The published registry's p.32 locator is one page early and should be corrected in a revision, without changing the archived version-1 record.

**Verbatim text fragment introducing the arithmetic:**

> In other words, when the discretization error

**Source equation reproduction, the following asymptotic assertion:**

$$
O\!\left(L{T^2\over L^2\Delta x^2}\epsilon\right)
=O\!\left(\epsilon^{\,2-1/(2p)}\right).
$$

**Source equation reproduction, only the right-hand bound in Eq. (B20):**

$$
\widetilde K\,d(d-1)h^2T
\max_j\|c_j\|_\infty^3
\max_{j,j',m}{(\Delta x_j)^{2p}\over\Delta x_{j'}\Delta x_m}.
$$

Here the left side of (B20) is the preceding double time integral of a commutator operator norm multiplied by $\||\widetilde f\rangle_t-|f\rangle_t\|_{2,N}$; no equality for that full integral is being introduced by quoting its right-hand bound.

**Audit contrast:** with the matched scales used in the argument, $L\propto T^2/\epsilon$ and $\Delta x\propto(\epsilon/T)^{1/(2p)}$, the expression on the left is proportional to

$$
{\epsilon^2\over\Delta x^2}
\propto\epsilon^{\,2-1/p}T^{1/p}.
$$

For fixed $T$, the exponent is $2-1/p$, not $2-1/(2p)$. It remains greater than one for $p\geq2$, so correcting this exponent does not by itself reverse the stated negligibility conclusion.

## Integration boundary

The exact quotations and source-equation reproductions above can be placed adjacent to the corresponding corrected expressions in a revised manuscript. Any revision should continue to distinguish literal printed-equation failures, typographical/convention repairs, resource qualifications and unavailable implementation evidence. No additional numerical experiment or journal-version inspection is claimed by this quotation sheet.
