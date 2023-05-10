import numpy as np
import matplotlib.pyplot as plt


def neuron_func_7():
    '''
    NOTE: Full HH
    '''

    # NOTE: n gating variables
    def n_inf(v):
        return alpha_func_n(v) / (alpha_func_n(v) + beta_func_n(v))

    def n_tau(v):
        return 1.0 / (alpha_func_n(v) + beta_func_n(v))

    def alpha_func_n(v):
        return 0.01 * (10.0 - v) / (np.exp((10.0 - v) / 10.0) - 1.0)

    def beta_func_n(v):
        return 0.125 * np.exp(-v / 80.0)

    # NOTE: m gating variables
    def m_inf(v):
        return alpha_func_m(v) / (alpha_func_m(v) + beta_func_m(v))

    def m_tau(v):
        return 1.0 / (alpha_func_m(v) + beta_func_m(v))

    def alpha_func_m(v):
        return 0.1 * (25.0 - v) / (np.exp((25.0 - v) / 10.0) - 1.0)

    def beta_func_m(v):
        return 4.0 * np.exp(-v / 18.0)

    # NOTE: h gating variables
    def h_inf(v):
        return alpha_func_h(v) / (alpha_func_h(v) + beta_func_h(v))

    def h_tau(v):
        return 1.0 / (alpha_func_h(v) + beta_func_h(v))

    def alpha_func_h(v):
        return 0.07 * np.exp(-v / 20.0)

    def beta_func_h(v):
        return 1.0 / (np.exp((30.0 - v) / 10.0) + 1.0)

    # NOTE: simulation parameter etc
    tau = 0.01
    T = 15
    t = np.arange(0, T, tau)
    nn = t.shape[0]

    I = np.zeros(nn)
    v = np.zeros(nn)
    n = np.zeros(nn)
    m = np.zeros(nn)
    h = np.zeros(nn)

    vr = -65.0

    v[0] = vr
    n[0] = n_inf(vr * 0)
    m[0] = m_inf(vr * 0)
    h[0] = h_inf(vr * 0)

    g_k = 36.0
    g_na = 120.0
    g_leak = 0.30

    E_k = -12 + vr
    E_na = 120 + vr
    E_leak = 10.6 + vr

    C = 1.0

    I[:] = 5.0

    # NOTE: Euler's method simulation
    for i in range(1, nn):
        delta_t = t[i] - t[i - 1]

        I_k = g_k * (n[i - 1]**4) * (v[i - 1] - E_k)
        I_na = g_na * (m[i - 1]**3) * (h[i - 1]) * (v[i - 1] - E_na)
        I_leak = g_leak * (v[i - 1] - E_leak)

        dvdt = (I[i - 1] - (I_k + I_na + I_leak)) / C

        dndt = (n_inf(v[i - 1] - vr) - n[i - 1]) / n_tau(v[i - 1] - vr)
        dmdt = (m_inf(v[i - 1] - vr) - m[i - 1]) / m_tau(v[i - 1] - vr)
        dhdt = (h_inf(v[i - 1] - vr) - h[i - 1]) / h_tau(v[i - 1] - vr)

        v[i] = v[i - 1] + dvdt * delta_t
        n[i] = n[i - 1] + dndt * delta_t
        m[i] = m[i - 1] + dmdt * delta_t
        h[i] = h[i - 1] + dhdt * delta_t

    # NOTE: inspect gating functions
    fig, ax = plt.subplots(5, 1, squeeze=False)

    v_range = np.arange(-40, 100, 0.01)

    ax[0, 0].plot(v_range, n_inf(v_range), label='n: k activation')
    ax[0, 0].plot(v_range, m_inf(v_range), label='m: Na activation')
    ax[0, 0].plot(v_range, h_inf(v_range), label='h: Na inactivation')
    ax[1, 0].plot(v_range, n_tau(v_range), label='n: k activation')
    ax[1, 0].plot(v_range, m_tau(v_range), label='m: Na activation')
    ax[1, 0].plot(v_range, h_tau(v_range), label='h: Na inactivation')
    ax[2, 0].plot(t, I, label='I')
    ax[3, 0].plot(t, v, label='v')
    ax[4, 0].plot(t, n, label='n: k activation')
    ax[4, 0].plot(t, m, label='m: Na activation')
    ax[4, 0].plot(t, h, label='h: Na inactivation')
    [x.legend() for x in ax.flatten()]
    plt.tight_layout()
    plt.show()

    fig, ax = plt.subplots(1, 2, squeeze=False)
    ax[0, 0].plot(t, v)
    ax_twin = ax[0, 0].twinx()
    ax_twin.plot(t, n)
    ax_twin.plot(t, m)
    ax_twin.plot(t, h)
    ax[0, 1].plot(t, v)
    ax_twin = ax[0, 1].twinx()
    ax_twin.plot(t, g_k * n**4)
    ax_twin.plot(t, g_na * m**3 * h)
    plt.show()


neuron_func_7()
