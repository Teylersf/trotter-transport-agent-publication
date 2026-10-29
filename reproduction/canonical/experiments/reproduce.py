"""Independent deterministic checks of arXiv:2508.15691v2.

All results are newly calculated; no author code or quantum hardware is used.
Run from any directory with Python, NumPy and Matplotlib.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import platform
import numpy as np
from numpy.linalg import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results'
FIG = ROOT / 'figures'
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)


def expm(matrix):
    """Unitary exponential for the anti-Hermitian matrices used here."""
    values, vectors = np.linalg.eigh(1j*matrix)
    return (vectors*np.exp(-1j*values))@vectors.conj().T


def stencil(p):
    return {k: (-1)**(k+1)*math.factorial(p)**2 /
            (k*math.factorial(p-k)*math.factorial(p+k))
            for k in range(-p, p+1) if k}


def derivative(n, p=2):
    # S|j> = |j+1>; B acting on amplitudes approximates +d/dx.
    shift = np.roll(np.eye(n), 1, axis=0)
    printed_d = -1j*n*sum(a*np.linalg.matrix_power(shift, k)
                          for k, a in stencil(p).items())
    return -1j*printed_d, printed_d


def save_csv(name, rows):
    with (OUT / name).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    checks = {}
    shear = []
    x = np.arange(512)/512
    xx, yy = np.meshgrid(x, x, indexing='ij')
    for t in (0, .1, .25, .5, 1, 2):
        phase = 2*np.pi*(xx-t*np.sin(2*np.pi*yy))
        f = np.sin(phase)
        fx = 2*np.pi*np.cos(phase)
        fy = -(2*np.pi)**2*t*np.cos(2*np.pi*yy)*np.cos(phase)
        row = {'time': t, 'f_l2': float(np.sqrt(np.mean(f*f))),
               'fx_l2': float(np.sqrt(np.mean(fx*fx))),
               'fy_l2': float(np.sqrt(np.mean(fy*fy))),
               'fy_l2_exact': 2*np.pi**2*t}
        shear.append(row)
        assert abs(row['f_l2']-1/np.sqrt(2)) < 1e-12
        assert abs(row['fy_l2']-row['fy_l2_exact']) < 1e-11
    checks['shear_exact_quadrature'] = True
    save_csv('shear.csv', shear)

    translation = []
    for n in (16, 32, 64, 128):
        x = np.arange(n)/n
        f0 = np.sqrt(2/n)*np.cos(2*np.pi*x)
        b, d = derivative(n)
        t = .125
        target = np.sqrt(2/n)*np.cos(2*np.pi*(x-t))
        wrong = expm(-1j*d*t)@f0
        corrected = expm(1j*d*t)@f0
        translation.append({'N': n,
            'printed_sign_error': float(norm(wrong-target)),
            'corrected_sign_error': float(norm(corrected-target))})
        assert norm(b+b.conj().T) < 1e-11
    assert translation[-1]['printed_sign_error'] > 1.4
    assert translation[-1]['corrected_sign_error'] < 2e-7
    ratios = [a['corrected_sign_error']/b['corrected_sign_error']
              for a,b in zip(translation,translation[1:])]
    assert all(15 < ratio < 17 for ratio in ratios)
    checks['shift_sign_counterexample'] = True
    save_csv('translation.csv', translation)

    comm = []
    for n in (8, 16, 32, 64, 128):
        x = np.arange(n)/n
        b, _ = derivative(n)
        c = np.diag(np.sin(2*np.pi*x))
        cb = c@b-b@c
        bx = b@(np.sqrt(2/n)*np.sin(2*np.pi*x))
        by = cb@(np.ones(n)/np.sqrt(n))
        comm.append({'N': n, 'operator_commutator_norm': float(norm(cb, 2)*norm(b, 2)),
            'smooth_state_commutator_norm': float(norm(bx)*norm(by)),
            'crude_operator_bound': float(2*norm(b, 2)**2),
            'coefficient_aware_bound': float(1.5*(5/3)*2*np.pi*n)})
        assert comm[-1]['operator_commutator_norm'] <= comm[-1]['coefficient_aware_bound']+1e-8
    checks['coefficient_aware_commutator_bound'] = True
    save_csv('commutators.csv', comm)

    moments = []
    for n in (16, 64, 256, 1024, 4096):
        x = np.arange(n)/n
        actual = float(np.sum(x)/(np.linalg.norm(x)*np.sqrt(n)))
        moments.append({'N': n, 'normalized_overlap': actual,
                        'correct_continuum_limit': np.sqrt(3)/2,
                        'printed_continuum_limit': 1/(2*np.sqrt(3))})
    checks['moment_normalization'] = bool(abs(moments[-1]['normalized_overlap']-np.sqrt(3)/2) < 6e-5)
    save_csv('moments.csv', moments)

    swap = []
    phi = np.array([1, 0], dtype=complex)
    for label, psi in [('same', phi), ('minus', -phi), ('phase_i', 1j*phi),
                       ('plus', np.array([1, 1])/np.sqrt(2))]:
        overlap = np.vdot(phi, psi)
        joint0 = (np.kron(psi, phi)+np.kron(phi, psi))/2
        p0 = float(np.vdot(joint0, joint0).real)
        p0_phase = float(norm((np.kron(psi, phi)+1j*np.kron(phi, psi))/2)**2)
        swap.append({'state': label, 'overlap_real': float(overlap.real),
            'overlap_imag': float(overlap.imag), 'actual_p0': p0,
            'printed_p0': (1+float(overlap.real))/2,
            'p0_with_i_phase': p0_phase})
        assert abs(p0-(1+abs(overlap)**2)/2) < 1e-12
        assert abs(p0_phase-.5) < 1e-12
    checks['controlled_swap_probabilities'] = True
    save_csv('swap.csv', swap)

    n = 8
    j = np.arange(n)
    qft = np.exp(2j*np.pi*np.outer(j,j)/n)/np.sqrt(n)
    f0 = np.array([.5,1/np.sqrt(2),.5,0,0,0,0,0])
    qft_error = float(norm(qft@qft@f0-f0))
    assert abs(qft_error-np.sqrt(1.5)) < 1e-12
    symbol_n = 32
    theta = 2*np.pi*np.arange(symbol_n)/symbol_n
    symbol_max = float(np.max(np.abs(4/3*np.sin(theta)-1/6*np.sin(2*theta))))
    assert symbol_max > 7/6
    assert symbol_max <= 1.5
    alpha, beta, gamma, delta = np.exp(-1), np.exp(-.5), np.exp(1/3), np.exp(-1/6)
    fixed_q, fixed_p = np.log(gamma/delta), np.log(beta/alpha)
    assert abs(-alpha+beta*np.exp(-fixed_p)) < 1e-14
    assert abs(delta-gamma*np.exp(-fixed_q)) < 1e-14
    jac_correct = np.array([[0,-alpha],[delta,0]])
    jac_printed = np.array([[0,alpha],[delta,0]])
    omega = np.sqrt(alpha*delta)
    assert np.allclose(np.sort_complex(np.linalg.eigvals(jac_correct)), [-1j*omega,1j*omega])
    assert np.allclose(np.sort(np.linalg.eigvals(jac_printed)), [-omega,omega])
    lv = {'fixed_q': float(fixed_q), 'fixed_p': float(fixed_p),
          'physical_eigenvalues': [[float(z.real),float(z.imag)] for z in np.linalg.eigvals(jac_correct)],
          'printed_liouville_characteristic_eigenvalues': [[float(z.real),float(z.imag)] for z in np.linalg.eigvals(jac_printed)]}
    checks['lotka_volterra_local_linearization'] = True
    checks['qft_zero_time_identity_failure'] = True
    checks['signed_stencil_constant_failure'] = True
    # c1=1,c2=sin(2πx), f0=sin(2πy); evaluate both orientations at t=0.
    ratio_derivative = 2*np.pi
    pair_terms = [1*(2*np.pi)*ratio_derivative, 1*0*0]
    full_alpha_at_zero = .5*sum(pair_terms)
    printed_max_at_zero = pair_terms[1]
    assert full_alpha_at_zero > printed_max_at_zero
    checks['oriented_maximum_failure'] = True
    # Literal A5 includes index M. On an M=8 dyadic grid w_M duplicates DC.
    walsh_m = 8
    grid = np.arange(walsh_m)/walsh_m
    first_bit_beyond_grid = np.floor(grid*2**4).astype(int) % 2
    w_m = (-1.)**first_bit_beyond_grid
    a_m = np.mean(w_m)
    literal_constant_sum = 1+a_m*w_m
    assert np.all(literal_constant_sum == 2)
    # A10 axis budgets: f=x+y, M1=M2=8, epsilon=1/8.
    sample = 1-1e-9
    actual_multivariate_error = 2*(sample-np.floor(walsh_m*sample)/walsh_m)
    assert actual_multivariate_error > 1/walsh_m
    assert actual_multivariate_error < 2/walsh_m
    checks['walsh_index_and_axis_budget'] = True

    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False,
                         'figure.dpi': 140, 'savefig.dpi': 220})
    fig, axs = plt.subplots(1,2,figsize=(10,3.5),constrained_layout=True)
    axs[0].plot([r['time'] for r in shear],[r['fy_l2'] for r in shear],'o-', label='Exact shear: y derivative')
    axs[0].axhline(0, color='gray',ls='--',label='Claimed conserved value')
    axs[0].set(xlabel='Time',ylabel='L2 norm',title='Derivative growth with conserved solution norm')
    axs[0].legend(fontsize=8)
    axs[1].loglog([r['N'] for r in translation],[r['printed_sign_error'] for r in translation],'o-',label='Printed shift/sign')
    axs[1].loglog([r['N'] for r in translation],[r['corrected_sign_error'] for r in translation],'o-',label='Corrected sign')
    axs[1].set(xlabel='Grid points N',ylabel='Normalized state error',title='Advection at T = 1/8; stencil p = 2')
    axs[1].legend(fontsize=8)
    fig.savefig(FIG/'transport-checks.png'); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.8,4),constrained_layout=True)
    for key,label in [('crude_operator_bound','Crude operator bound'),('coefficient_aware_bound','Coefficient-aware bound'),('operator_commutator_norm','Exact operator commutator'),('smooth_state_commutator_norm','Smooth-state commutator')]:
        ax.loglog([r['N'] for r in comm],[r[key] for r in comm],'o-',label=label)
    ax.set(xlabel='Grid points per axis N',ylabel='Norm / bound',title='Periodic shear plus constant transverse transport')
    ax.legend(fontsize=8)
    fig.savefig(FIG/'commutator-baselines.png'); plt.close(fig)

    fig, axs = plt.subplots(1,2,figsize=(10,3.5),constrained_layout=True)
    axs[0].semilogx([r['N'] for r in moments],[r['normalized_overlap'] for r in moments],'o-',label='Finite-grid overlap')
    axs[0].axhline(np.sqrt(3)/2,color='#21825c',ls='--',label='Correct limit')
    axs[0].axhline(1/(2*np.sqrt(3)),color='#c4463a',ls=':',label='Printed limit')
    axs[0].set(xlabel='Grid points N',ylabel='Overlap',title='Linear moment of the constant function')
    axs[0].legend(fontsize=8)
    positions=np.arange(len(swap))
    axs[1].bar(positions-.16,[r['actual_p0'] for r in swap],.32,label='Controlled-SWAP')
    axs[1].bar(positions+.16,[r['printed_p0'] for r in swap],.32,label='Printed formula')
    axs[1].set(xticks=positions,xticklabels=[r['state'] for r in swap],ylabel='Probability P(0)',title='Global phase cannot change a SWAP outcome')
    axs[1].legend(fontsize=8)
    fig.savefig(FIG/'measurement-checks.png'); plt.close(fig)

    summary = {'source': 'arXiv:2508.15691v2', 'checks': checks,
        'qft_two_forward_zero_time_error': qft_error,
        'p2_N32_dimensionless_symbol_norm': symbol_max,
        'printed_p2_norm_bound': 7/6, 'corrected_p2_absolute_bound': 1.5,
        'oriented_maximum_counterexample': {'c1':'1','c2':'sin(2*pi*x)',
            'f0':'sin(2*pi*y)', 'printed_one_orientation_bound':float(printed_max_at_zero),
            'full_alpha_prime_at_t0':float(full_alpha_at_zero)},
        'walsh_local_checks': {'M':walsh_m,'literal_constant_series_values':literal_constant_sum.tolist(),
            'per_axis_target_epsilon':1/walsh_m,'actual_two_axis_error':float(actual_multivariate_error)},
        'lotka_volterra': lv,
        'gaussian_preparation': {'sigma':.02,'dimension':2,'alpha':1,
            'asymptotic_success_probability':float(np.pi*.02**2),
            'mean_trials':float(1/(np.pi*.02**2))},
        'environment': {'python':platform.python_version(),'numpy':np.__version__,
                        'matplotlib':matplotlib.__version__}}
    assert all(checks.values())
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
    manifest = {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
        for folder in (OUT,FIG) for p in sorted(folder.iterdir())
        if p.is_file() and p.name != 'artifact-sha256.json'}
    (OUT/'artifact-sha256.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
