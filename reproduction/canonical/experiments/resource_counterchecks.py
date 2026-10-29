"""Small independent checks of the supplied arXiv:2508.15691v2 equations.

No original author implementation or hardware data are assumed.  Uses only
NumPy.  The smooth transport experiment is a separate diagnostic, not a
reproduction of the paper's Figure 4/5 input.  Outputs numerical evidence only.
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results'


def coefficients(p):
    return {k: (-1)**(k+1) * math.factorial(p)**2 /
            (k * math.factorial(p-k) * math.factorial(p+k))
            for k in range(-p, p+1) if k}


def printed_derivative(n, p):
    # Eq.5: S|j> = |j+1>, D = -i sum_k a_k S^k / dx.
    S = np.roll(np.eye(n), 1, axis=0)
    return -1j*n*sum(a*np.linalg.matrix_power(S, k)
                    for k, a in coefficients(p).items())


def evolve_hermitian(H, state, t):
    e, v = np.linalg.eigh(H)
    return v @ (np.exp(-1j*t*e) * (v.conj().T @ state))


def sign_check():
    rows = []
    for n in (16, 32, 64):
        x = np.arange(n)/n
        f = np.sin(2*np.pi*x)
        df = 2*np.pi*np.cos(2*np.pi*x)
        D = printed_derivative(n, 2)
        rows.append({
            'N': n,
            'relative_error_iD_vs_positive_derivative': float(np.linalg.norm(1j*D@f-df)/np.linalg.norm(df)),
            'relative_error_iD_vs_negative_derivative': float(np.linalg.norm(1j*D@f+df)/np.linalg.norm(df)),
            'hermiticity_residual': float(np.linalg.norm(D-D.conj().T)),
        })
    return {'locator': 'p4 Eq5; p9 Eq20; p30 EqB4', 'rows': rows,
            'interpretation': 'With the explicitly printed forward ket shift, iD tends to minus the coefficient derivative. This diagnoses inconsistent definitions, not the unknown implementation.'}


def hardware_grid_shift_check():
    n, p = 8, 10
    f = np.array([.5, 1/np.sqrt(2), .5, 0, 0, 0, 0, 0])
    D = printed_derivative(n, p)
    rows = []
    for t, reported in ((.25, 3.6e-4), (.5, 7.2e-4)):
        # Eq38 at v=1 has an exact integer-grid shift at these two times,
        # independent of how the continuous initial function interpolates samples.
        positive = np.roll(f, round(n*t))
        negative = np.roll(f, -round(n*t))
        printed = evolve_hermitian(D, f, t)
        corrected = evolve_hermitian(-D, f, t)
        rows.append({
            't': t, 'reported_rounded_state_error': reported,
            'printed_Eq5_Eq6_vs_positive_grid_shift': float(np.linalg.norm(printed-positive)),
            'printed_Eq5_Eq6_vs_negative_grid_shift': float(np.linalg.norm(printed-negative)),
            'sign_corrected_vs_positive_grid_shift': float(np.linalg.norm(corrected-positive)),
            'sign_corrected_norm': float(np.linalg.norm(corrected)),
            'positive_and_negative_shifts_identical': bool(np.array_equal(positive, negative)),
        })
    return {'locator': 'pp15-16 Eq38, Eq39 and Figure7 caption',
            'N': n, 'p': p, 'initial_state': f.tolist(), 'rows': rows,
            'interpretation': 'The stated error magnitudes are reproduced after the intended advection sign is used. At t=.5 the two directions coincide on this periodic grid, so t=.25 is the directional diagnostic.'}


def swap_check():
    H = np.array([[1, 1], [1, -1]], complex)/np.sqrt(2)
    swap = np.array([[1, 0, 0, 0], [0, 0, 1, 0],
                     [0, 1, 0, 0], [0, 0, 0, 1]], complex)
    controlled = np.zeros((8, 8), complex)
    controlled[:4, :4] = np.eye(4)
    controlled[4:, 4:] = swap
    Had = np.kron(H, np.eye(4))
    phase = np.diag([1]*4 + [1j]*4)
    psi = np.array([1, 0], complex)
    rows = []
    for name, phi in [('positive_overlap', np.array([1, 1], complex)/np.sqrt(2)),
                      ('negative_global_phase', np.array([-1, 0], complex)),
                      ('imaginary_global_phase', np.array([1j, 0], complex))]:
        initial = np.kron([1, 0], np.kron(psi, phi))
        out = Had @ controlled @ Had @ initial
        out_phase = Had @ phase @ controlled @ Had @ initial
        overlap = np.vdot(phi, psi)
        actual = float(np.sum(abs(out[:4])**2))
        rows.append({
            'name': name, 'overlap_real': float(overlap.real),
            'overlap_imag': float(overlap.imag),
            'actual_P0': actual,
            'correct_P0_absolute_overlap_squared': float((1+abs(overlap)**2)/2),
            'printed_A16_P0_real_overlap': float((1+overlap.real)/2),
            'P0_with_claimed_imaginary_phase_gate': float(np.sum(abs(out_phase[:4])**2)),
        })
        assert abs(actual-(1+abs(overlap)**2)/2) < 1e-14
    return {'locator': 'pp27-28 EqA15, EqA16 and Figure14', 'rows': rows,
            'interpretation': 'The shown SWAP circuit measures squared overlap, which is invariant under global phase. Adding a phase to its control cannot retrieve the imaginary overlap. The distinct Hadamard-test route is not invalidated by this check.'}


def moment_check():
    n, k = 65536, 1
    x = np.arange(n)/n
    f = np.ones(n)
    overlap = float(np.dot(x, f)/(np.linalg.norm(x)*np.linalg.norm(f)))
    product = 2*k+1
    return {'locator': 'p8 Eq17 and immediately following C_k definition',
            'example': 'd=1, k=1, f(x)=1 on [0,1]', 'N': n,
            'discrete_normalized_overlap': overlap,
            'correct_continuum_overlap': math.sqrt(3)/2,
            'printed_continuum_overlap': 1/(2*math.sqrt(3)),
            'needed_C_k': math.sqrt(product),
            'printed_C_k': 1/math.sqrt(product),
            'interpretation': 'The finite-grid overlap in Eq17 is valid; the printed continuum factor is its reciprocal and predicts a factor3 error for this example.'}


def lotka_sign_check():
    alpha, beta, gamma, delta = np.exp([-1., -.5, 1/3, -1/6])
    q, p = .7, .3
    qdot = -alpha+beta*np.exp(-p)
    pdot = delta-gamma*np.exp(-q)
    return {'locator': 'p17 Eq41, Eq42, Eq43',
            'parameters': {'alpha': float(alpha), 'beta': float(beta), 'gamma': float(gamma), 'delta': float(delta)},
            'initial_qp': [q,p],
            'Eq42_characteristic_velocity_qp': [float(qdot), float(pdot)],
            'Eq43_implied_characteristic_velocity_qp': [float(-qdot), float(pdot)],
            'correct_rhs_coefficient_partial_q': float(-qdot),
            'printed_rhs_coefficient_partial_q': float(qdot),
            'interpretation': 'For divergence-free Hamiltonian flow, partial_t rho= -qdot partial_q rho -pdot partial_p rho. Eq43 reverses only the q coefficient. This is an equation inconsistency; no code is deposited to identify the equation actually evolved.'}


def gaussian_preparation():
    sigma, d, alpha = .02, 2, 1.
    success = (math.sqrt(math.pi)*sigma)**d/alpha**2
    return {'locator': 'p23 EqA2 and p18 Figure8 initial Gaussian',
            'scope': 'Continuum Gaussian sufficiently far from boundaries; EqA2 family estimate, not a measured circuit runtime.',
            'dimension': d, 'sigma': sigma, 'alpha': alpha,
            'estimated_success_probability': success,
            'estimated_expected_repeat_until_success_preparations': 1/success,
            'amplitude_amplification_scale_inverse_sqrt_probability': 1/math.sqrt(success),
            'interpretation': 'Theta(1) in EqA2 is correct for fixed f as N grows. It is not uniform in localization width or dimension, and alpha>1 decreases the probability further.'}


def smooth_trotter_diagnostic():
    rows = []
    for n in (8, 16, 32, 64):
        x = np.arange(n)/n
        c1 = .4+.1*np.sin(2*np.pi*x)[None, :]
        c2 = .3+.1*np.cos(2*np.pi*x)[:, None]
        lam = 2*n*sum(a*np.sin(2*np.pi*k*np.arange(n)/n)
                      for k,a in coefficients(2).items() if k>0)
        f = 1+.2*np.sin(2*np.pi*x)[:,None]+.2*np.cos(2*np.pi*x)[None,:]
        f = f/np.linalg.norm(f)
        def h1(u):
            return c1*np.fft.ifft(lam[:,None]*np.fft.fft(u,axis=0),axis=0)
        def h2(u):
            return c2*np.fft.ifft(lam[None,:]*np.fft.fft(u,axis=1),axis=1)
        def ux(u,dt):
            return np.fft.ifft(np.exp(-1j*dt*c1*lam[:,None])*np.fft.fft(u,axis=0),axis=0)
        def uy(u,dt):
            return np.fft.ifft(np.exp(-1j*dt*c2*lam[None,:])*np.fft.fft(u,axis=1),axis=1)
        def evolve(L,strang):
            u=f.astype(complex)
            dt=.2/L
            for _ in range(L):
                if strang:
                    u=ux(uy(ux(u,dt/2),dt),dt/2)
                else:
                    u=uy(ux(u,dt),dt)
            return u
        ref=evolve(2048,True)
        ref2=evolve(1024,True)
        rows.append({'N_per_axis':n, 'p':2,
                     'commutator_on_smooth_state_norm':float(np.linalg.norm(h2(h1(f))-h1(h2(f)))),
                     'crude_operator_product_bound':float(np.max(abs(c1))*np.max(abs(c2))*np.max(abs(lam))**2),
                     'T':.2, 'L':32,
                     'Lie_vs_refined_Strang_state_norm':float(np.linalg.norm(evolve(32,False)-ref)),
                     'reference_1024_vs_2048_Strang_difference':float(np.linalg.norm(ref2-ref)),
                     'reference_norm':float(np.linalg.norm(ref))})
    return {'scope': 'Independent periodic smooth example satisfying Eq2; not a reproduction of Figure5 or a proof of TheoremIII.4.',
            'initial_amplitude': '1+.2 sin(2 pi x)+.2 cos(2 pi y), normalized',
            'c1': '.4+.1 sin(2 pi y)', 'c2': '.3+.1 cos(2 pi x)',
            'rows': rows}


def main():
    output = {
        'source': 'User-supplied PDF byte-identical to arXiv:2508.15691v2 according to source-worker verification',
        'python_version': platform.python_version(), 'numpy_version': np.__version__,
        'producer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'sign_convention': sign_check(),
        'hardware_error_magnitudes': hardware_grid_shift_check(),
        'swap_test': swap_check(),
        'polynomial_moment_normalization': moment_check(),
        'lotka_volterra_liouville_sign': lotka_sign_check(),
        'localized_gaussian_state_preparation': gaussian_preparation(),
        'smooth_periodic_trotter_diagnostic': smooth_trotter_diagnostic(),
    }
    OUT.mkdir(exist_ok=True)
    path=OUT / 'resource-counterchecks.json'
    with path.open('w',encoding='utf-8',newline='\n') as stream:
        json.dump(output,stream,indent=2,allow_nan=False)
        stream.write('\n')
    print(json.dumps({'output':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))


if __name__=='__main__':
    main()
