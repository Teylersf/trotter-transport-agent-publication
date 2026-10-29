## Proposed revision appendix: numerical provenance

This appendix is prepared for the invited revision. It is not part of the frozen v1.0.0 manuscript. All values below come from the already released scientific snapshot `1fb4be68eecce95b93adb8026c4e3d29fb442583`; no new data or fitted constants are introduced.

### Matrix and state norms

Vector errors use the Euclidean norm of the entire normalized amplitude array, equivalently its Frobenius norm when stored as a two-dimensional array. Matrix operator norms are spectral norms, computed as the largest singular value. They are not entrywise maximum norms or unnormalized physical-density errors. Samples are normalized by the square root of the sum of their squared magnitudes; there is no extra cell-volume factor after normalization.

For the coefficient-aware comparison, let $B$ be the centered fourth-order derivative on an $N$-point periodic grid, $C=\operatorname{diag}(\sin(2\pi j/N))$, and take the unit input $u\otimes v$, where $u_j=\sqrt{2/N}\sin(2\pi j/N)$ and $v_j=1/\sqrt N$. The two directional generators are, up to tensor ordering, $B\otimes C$ and $I\otimes B$. Their commutator factorizes as $B\otimes(CB-BC)$. Consequently its exact spectral norm is $\|B\|_2\|CB-BC\|_2$, and its norm on the specified state is $\|Bu\|_2\|(CB-BC)v\|_2$. This computes the full two-dimensional norm without constructing a matrix with $N^4$ entries.

For $p=2$, the two-sided coefficient sums are $A_p=3/2$ and $M_p=5/3$. The coefficient-aware upper bound (12) is $A_pM_p(2\pi)N=5\pi N$. The crude commutator upper bound in this table is $2\|B\|_2^2$. Both are bounds on the operator norm itself.

| Points per coordinate | Exact operator commutator norm | Coefficient-aware upper bound | Crude commutator upper bound | Action on specified smooth state |
|---:|---:|---:|---:|---:|
| 8 | 67.8300282 | 125.6637061 | 227.5555556 | 27.2613756 |
| 16 | 175.7092095 | 251.3274123 | 932.6922058 | 27.8720208 |
| 32 | 405.4070263 | 502.6548246 | 3852.2809509 | 27.9127034 |
| 64 | 863.5486624 | 1005.3096491 | 15409.1238036 | 27.9152841 |
| 128 | 1782.5930041 | 2010.6192983 | 61676.6654424 | 27.9154460 |

Provenance: `experiments/reproduce.py`, the `comm` loop in `main`; output `results/commutators.csv`. Coefficients, periodic shift matrix, state and singular-value norm are all constructed in that loop or its `derivative` helper. The bound is asserted with an absolute roundoff allowance of $10^{-8}$. The continuum smooth-state limit is $2\sqrt2\pi^2=27.9154568\ldots$.

### Independent smooth periodic splitting experiment

The input is the normalized sampled amplitude $1+0.2\sin(2\pi x)+0.2\cos(2\pi y)$; the coefficients are $c_1(y)=0.4+0.1\sin(2\pi y)$ and $c_2(x)=0.3+0.1\cos(2\pi x)$. Final time is $0.2$, stencil order is four, and the Lie product takes 32 steps. Each directional exponential is applied through an FFT, multiplication by the exact finite-grid phase, and inverse FFT. The reference is a 2,048-step Strang product with ordering $U_x(\Delta t/2)U_y(\Delta t)U_x(\Delta t/2)$; a 1,024-step calculation checks its convergence.

| Points per coordinate | Initial commutator action | Paper-style product-norm coefficient | Lie versus 2,048-step Strang state error | Difference of 1,024/2,048-step Strang references |
|---:|---:|---:|---:|---:|
| 8 | 0.1946117382 | 22.75555556 | 0.0001224076209 | 2.1127351e-10 |
| 16 | 0.1989709727 | 93.26922058 | 0.0001251702637 | 2.1910907e-10 |
| 32 | 0.1992613948 | 385.22809509 | 0.0001253543060 | 2.1965448e-10 |
| 64 | 0.1992798178 | 1540.91238036 | 0.0001253659811 | 2.1968886e-10 |

The product-norm coefficient in this table is $\|c_1\|_\infty\|c_2\|_\infty\|D\|_2^2$, matching the paper's leading first-order time-error coefficient. It is half the corresponding crude commutator bound because the local double integral contributes a factor $1/2$. It must not be confused with the full operator commutator norm in the previous table. The initial commutator action is an instantaneous diagnostic, not an error certificate; the fourth column is computed separately. Reference agreement supplies an internal convergence check rather than a rigorous error bar.

Provenance: `experiments/resource_counterchecks.py`, function `smooth_trotter_diagnostic`; JSON key `smooth_periodic_trotter_diagnostic` in `results/resource-counterchecks.json`. The computed reference norms differ from one by less than $1.3\times10^{-14}$ over the tested grids. The functions and all numerical parameters above are fixed before grid refinement. This is a new, fully specified periodic diagnostic, not a reproduction of the original Figure 5.

### Reproduced eight-point discretization magnitudes

For the initial vector $(1/2,1/\sqrt2,1/2,0,0,0,0,0)^T$, take $N=8$, $p=10$, $v=1$. Construct the circulant matrix from the source's stated coefficients, coordinate the sign for positive advection, diagonalize the Hermitian Hamiltonian and apply its unitary exponential. At times $1/4$ and $1/2$, the exact PDE samples are cyclic shifts of the input by respectively two and four indices. This comparison is independent of any choice of continuous interpolation between the initial sample points.

| Time | Calculated normalized state error | Rounded value reported in Figure 7 |
|---:|---:|---:|
| 0.25 | 0.0003586742105130 | 0.00036 |
| 0.50 | 0.0007173483287404 | 0.00072 |

Provenance: `hardware_grid_shift_check` in `experiments/resource_counterchecks.py`; JSON key `hardware_error_magnitudes`. NumPy Hermitian diagonalization is used, and the evolved norm differs from one by less than $10^{-14}$. These values confirm the reported deterministic magnitudes under the intended advection convention. They are not new quantum processor outcomes. At time $1/2$, the positive and negative shifts coincide on this periodic grid; time $1/4$ is the informative directional check.

### Error and software qualifications

The calculations use Python 3.12.14 and NumPy 2.3.5 in double precision. Values are tabulated to expose their provenance, not to imply experimental precision. Elementary identities and the exact shear quadrature use explicit assertion tolerances in the released code. The positive smooth-state experiment reports its reference-refinement difference separately, and the main consistency script checks the corrected translation convergence ratios lie between 15 and 17 under mesh halving. Every released numerical and figure file is bound by `results/artifact-sha256.json`; `data/reproducibility.json` verifies those bytes against the frozen Git commit. A DOI archive, if later obtained, must contain that same verified snapshot rather than a mutable working directory.
