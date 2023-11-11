import numpy as np
import matplotlib.pyplot as plt
import control

if __name__ == '__main__':
    # Process Parameters
    Kh = 3.5
    theta_t = 22
    theta_d = 2

    # Transfer Function Process
    num_p = np.array([Kh])
    den_p = np.array([theta_t, 1])
    Hp1 = control.tf(num_p, den_p)
    print('Process transfer function: Hp1(s) =', Hp1)

    # Transfer Function Delay
    N = 5  # Order of Pade approximation
    [num_pade, den_pade] = control.pade(theta_d, N)
    Hp2 = control.tf(num_pade, den_pade)
    print('Delay transfer function: Hp2(s) =', Hp2)

    # Transfer Function Open Loop
    Hp = control.series(Hp1, Hp2)
    print('Open loop transfer function: Hp(s) =', Hp)

    # Transfer Function PI Controller
    # Marginally stable
    Kp = 4.38  # = Kc
    Ti = 99999999999999 # = Inf
    # Stable (Ziegler-Nichols result)
    # Kp = 1.97
    # Ti = 7.93
    # Stable (second Ziegler-Nichols result)
    # Kp = 1.84
    # Ti = 19.75

    Hc = control.tf([Kp * Ti, Kp], [Ti, 0])
    print('Controller transfer function: Hc(s) =', Hc)

    # Transfer Function Low Pass Filter
    Tf = 0.5
    Hf = control.tf(1, [Tf, 1])
    print('Filter transfer function: Hf(s) =', Hf)

    # Transfer Function Loop
    L = control.series(Hc, Hp, Hf)
    print('Loop transfer function: L(s) =', L)

    # Transfer Function Closed Loop
    T = control.feedback(L, 1)
    print('Closed loop transfer function: T(s) =', T)

    # Step Response Feedback System
    t, y = control.step_response(T, T=200)
    plt.figure(1)
    plt.plot(t, y)
    plt.xlabel('Time [s]')
    plt.ylabel('Step response')
    plt.grid()
    plt.show()

    # Bode Plot with stability margins
    plt.figure(2)
    control.bode_plot(L, dB=True, deg=True, margins=True)
    plt.show()

    # Pole Zero Map
    plt.figure(3)
    control.pzmap(T, grid=True)
    plt.show()

    p = control.poles(T)
    z = control.zeros(T)
    print("poles = ", p)

    # Stability margins and crossover frequency
    gm, pm, wg, wp = control.margin(L)

    gm_db = 20 * np.log10(gm)

    print(f"Gain margin: GM = {gm_db:.2f} dB")
    print(f"Phase margin: PM = {pm:.2f} deg")
    print(f"Gain crossover frequency: WG = {wg:.2f} rad/s")
    print(f"Phase crossover frequency: WP = {wp:.2f} rad/s")

    # Critical Gain
    Kc = Kp * gm
    Tc = 2 * np.pi / wp
    print(f"Critical gain: Kc = {Kc:.2f}")
    print(f"Critical period: Tc = {Tc:.2f}")

    # Ziegler-Nichols Tuning
    Kp_zn = 0.45 * Kc
    Ti_zn = Tc / 1.2
    print(f"Ziegler-Nichols: Kp = {Kp_zn:.2f}, Ti = {Ti_zn:.2f}")
