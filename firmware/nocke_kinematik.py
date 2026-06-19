"""
Exzentrische Nockenwelle — Kinematik & Visualisierung
Hybrid-Design: J1/J2 aktiv (Nockenwelle), J3/J4 passiv (TPU-Federgelenke)

Branch: dev/hybrid-passive-tail
Stand: Juni 2026
Dokumentation: mechanics/hybrid_passive_tail_mechanics.md
"""

import math
import numpy as np

# KONSTANTEN: Hybrid-Design (aus mechanics/hybrid_passive_tail_mechanics.md)
ACTIVE_LEVERS = {
    'J1': 30,   # mm -> arcsin(3/30) = ±5.7° (Kopf-nah)
    'J2': 25,   # mm -> arcsin(3/25) = ±6.9° (Vordermitte)
}

PASSIVE_JOINTS = {
    'J3': {
        'k': 39.5,
        'd': 4.0,
        'm': 1.0,
        'shore': '95A',
        'expected_amp': (8, 12),
        'resonance_hz': 1.0,
    },
    'J4': {
        'k': 25.3,
        'd': 2.5,
        'm': 1.0,
        'shore': '85A',
        'expected_amp': (12, 18),
        'resonance_hz': 0.8,
    },
}

GEAR_RATIO = 40.0
MOTOR_MAX_RPM = 9990.0


class NockeKinematics:
    def __init__(self, R0=8.0, e=3.0, active_levers=None, passive_joints=None):
        self.R0 = R0
        self.e = e
        self.active = active_levers if active_levers is not None else ACTIVE_LEVERS.copy()
        self.passive = passive_joints if passive_joints is not None else PASSIVE_JOINTS.copy()
        self._passive_state = {k: {'theta': 0.0, 'omega': 0.0} for k in self.passive}
        self.body_length_m = 0.65
        self.tail_amplitude_m = 0.03
        self.swim_speed_mps = 0.35

    def gleitschuh_hub(self, theta_nocke_deg, gleitschuh_pos_deg):
        theta_eff = math.radians(theta_nocke_deg - gleitschuh_pos_deg)
        return self.e * math.cos(theta_eff)

    def aktiv_winkel(self, hub_mm, joint_key):
        L = self.active[joint_key]
        hub_clamped = max(-L + 0.001, min(L - 0.001, hub_mm))
        return math.degrees(math.asin(hub_mm / L))

    def aktive_gelenke(self, theta_nocke_deg):
        h1 = self.gleitschuh_hub(theta_nocke_deg, 0)
        h2 = self.gleitschuh_hub(theta_nocke_deg, 90)
        return self.aktiv_winkel(h1, 'J1'), self.aktiv_winkel(h2, 'J2')

    def passive_step(self, j2_winkel, dt_s):
        s3 = self._passive_state['J3']
        p3 = self.passive['J3']
        torque3 = p3['k'] * (j2_winkel - s3['theta']) - p3['d'] * s3['omega']
        alpha3 = torque3 / p3['m']
        s3['omega'] += alpha3 * dt_s
        s3['theta'] += s3['omega'] * dt_s

        s4 = self._passive_state['J4']
        p4 = self.passive['J4']
        torque4 = p4['k'] * (s3['theta'] - s4['theta']) - p4['d'] * s4['omega']
        alpha4 = torque4 / p4['m']
        s4['omega'] += alpha4 * dt_s
        s4['theta'] += s4['omega'] * dt_s

        return s3['theta'], s4['theta']

    def reset_passive(self):
        for k in self._passive_state:
            self._passive_state[k] = {'theta': 0.0, 'omega': 0.0}

    def simulate(self, freq_hz=1.0, duration_s=3.0, dt_s=0.005):
        self.reset_passive()
        t_vals = np.arange(0, duration_s, dt_s)
        j1_vals, j2_vals, j3_vals, j4_vals = [], [], [], []
        for t in t_vals:
            theta_nocke = (t * freq_hz * 360) % 360
            j1, j2 = self.aktive_gelenke(theta_nocke)
            j3, j4 = self.passive_step(j2, dt_s)
            j1_vals.append(j1)
            j2_vals.append(j2)
            j3_vals.append(j3)
            j4_vals.append(j4)
        return {
            't': t_vals,
            'J1': np.array(j1_vals),
            'J2': np.array(j2_vals),
            'J3': np.array(j3_vals),
            'J4': np.array(j4_vals),
        }

    def strouhal_number(self, freq_hz, amplitude_m, speed_mps):
        return (freq_hz * amplitude_m * 2) / speed_mps

    def amplitude_aktiv(self, joint_key):
        L = self.active[joint_key]
        return math.degrees(math.asin(self.e / L))

    def resonanzfrequenz(self, joint_key):
        p = self.passive[joint_key]
        return (1 / (2 * math.pi)) * math.sqrt(p['k'] / p['m'])

    def print_info(self):
        print("\n" + "=" * 78)
        print(" HYBRID-DESIGN: 2 Aktive + 2 Passive Gelenke")
        print("=" * 78)
        print(f" Nockenwelle: R0={self.R0}mm, e={self.e}mm, Laenge=60mm")
        print(f" Getriebe: {GEAR_RATIO}:1 (10:1 + 4:1)")
        print(f" Gleitschuhe: 2 Stueck (nur J1+J2)")
        print("-" * 78)
        print(" AKTIVE GELENKE (Nockenwelle):")
        for key, L in self.active.items():
            amp = self.amplitude_aktiv(key)
            print(f"  {key}: L={L}mm -> +-{amp:.1f} deg")
        print("-" * 78)
        print(" PASSIVE GELENKE (TPU-Feder):")
        for key, p in self.passive.items():
            f_res = self.resonanzfrequenz(key)
            amp_range = p['expected_amp']
            print(f"  {key}: Shore {p['shore']}, f_res={f_res:.1f} Hz, Amp: +-{amp_range[0]}-{amp_range[1]} deg")
        print("=" * 78 + "\n")

    def print_zyklus(self, freq_hz=1.0, steps=8):
        self.reset_passive()
        dt = 1.0 / (freq_hz * steps * 10)
        result = self.simulate(freq_hz=freq_hz, duration_s=2.0/freq_hz, dt_s=dt)
        n = len(result['t'])
        cycle_start = n // 2
        indices = [cycle_start + int(i * (n - 1 - cycle_start) / steps) for i in range(steps + 1)]
        print(f"\n Nockenwinkel |   J1(aktiv) |   J2(aktiv) |  J3(passiv) |  J4(passiv)")
        print("-" * 65)
        for idx in indices:
            theta = (result['t'][idx] * freq_hz * 360) % 360
            print(f"  {theta:5.1f} deg   |  {result['J1'][idx]:+7.2f} deg  |  {result['J2'][idx]:+7.2f} deg  |  {result['J3'][idx]:+7.2f} deg  |  {result['J4'][idx]:+7.2f} deg")
        print()

    def print_amplitude_analysis(self, freq_hz=1.0):
        result = self.simulate(freq_hz=freq_hz, duration_s=5.0, dt_s=0.001)
        n = len(result['t'])
        half = n // 2
        amps = {}
        for key in ['J1', 'J2', 'J3', 'J4']:
            amp = np.max(np.abs(result[key][half:]))
            amps[key] = amp

        print("\n" + "=" * 70)
        print(f" AMPLITUDEN-ANALYSE bei f = {freq_hz:.2f} Hz")
        print("=" * 70)
        print("\nBiologische Referenz (echter Hai):")
        print("  Koerperwelle: Amplitude steigt exponentiell zum Schwanz")
        print("  Typisch: J1:J2:J3:J4 ~ 1 : 1.2 : 1.8 : 2.5")
        print("\nSimulierte Amplituden:")
        for key in ['J1', 'J2', 'J3', 'J4']:
            amp = amps[key]
            ratio = amp / amps['J1'] if amps['J1'] > 0 else 0
            print(f"  {key}: +-{amp:5.2f} deg (Verhaeltnis: {ratio:.2f}x)")

        speed = self.swim_speed_mps * (freq_hz / 1.0)
        st = self.strouhal_number(freq_hz, self.tail_amplitude_m, speed)
        print(f"\nStrouhal-Zahl: St = {st:.3f} (Optimal: 0.25-0.35)")
        print("\nResonanz-Check:")
        for key in ['J3', 'J4']:
            f_res = self.resonanzfrequenz(key)
            ratio = freq_hz / f_res
            status = "OK Nahe Resonanz!" if abs(ratio - 1.0) < 0.15 else "Nicht optimal"
            print(f"  {key}: f_sim={freq_hz:.2f} Hz, f_res={f_res:.2f} Hz -> {status}")
        print()

    def print_throttle_table(self):
        print("\n" + "=" * 70)
        print(" THROTTLE -> FREQUENZ -> GESCHWINDIGKEIT (Getriebe 40:1)")
        print("=" * 70)
        print(f"{'Throttle':>10} | {'Motor RPM':>10} | {'Cam RPM':>10} | {'Freq [Hz]':>10} | {'Speed [m/s]':>15}")
        print("-" * 70)
        speed_data = {0.5: 0.18, 1.0: 0.35, 1.5: 0.53, 2.0: 0.70}
        for pct in [10, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100]:
            rpm_motor = pct / 100 * MOTOR_MAX_RPM
            rpm_nocke = rpm_motor / GEAR_RATIO
            f_hz = rpm_nocke / 60
            if f_hz <= 0.5:
                speed = speed_data[0.5] * (f_hz / 0.5)
            elif f_hz >= 2.0:
                speed = speed_data[2.0] * (f_hz / 2.0)
            else:
                keys = sorted(speed_data.keys())
                for i in range(len(keys) - 1):
                    if keys[i] <= f_hz <= keys[i+1]:
                        ratio = (f_hz - keys[i]) / (keys[i+1] - keys[i])
                        speed = speed_data[keys[i]] + ratio * (speed_data[keys[i+1]] - speed_data[keys[i]])
                        break
            print(f"{pct:10.0f}% | {rpm_motor:10.0f} | {rpm_nocke:10.1f} | {f_hz:10.2f} | {speed:15.2f}")
        print()


if __name__ == "__main__":
    k = NockeKinematics()
    k.print_info()
    k.print_throttle_table()
    for freq in [0.5, 1.0, 1.5]:
        print(f"\n--- Frequenz: {freq:.1f} Hz ---")
        k.print_zyklus(freq_hz=freq)
    k.print_amplitude_analysis(freq_hz=1.0)
    k.print_amplitude_analysis(freq_hz=1.5)
    print("\n" + "=" * 78)
    print("  RESONANZ-ABSTIMMUNG")
    print("=" * 78)
    for key in PASSIVE_JOINTS:
        f_res = k.resonanzfrequenz(key)
        print(f"  {key} (Shore {PASSIVE_JOINTS[key]['shore']}):")
        print(f"    Resonanz: {f_res:.2f} Hz")
        print(f"    Erwartete Amplitude: +-{PASSIVE_JOINTS[key]['expected_amp'][0]}-{PASSIVE_JOINTS[key]['expected_amp'][1]} deg")
    print("\n" + "=" * 78)
    print("  ANALYSE ABGESCHLOSSEN")
    print("=" * 78)
    print("\nEmpfehlungen:")
    print("  1. Bei 1.0 Hz: J3 ist in Resonanz -> maximale Amplitude!")
    print("  2. Bei 0.8 Hz: J4 ist in Resonanz -> Schwanz schwingt stark!")
    print("  3. Strouhal-Zahl bei 1.0-1.2 Hz optimal (0.25-0.35)")
    print("  4. Fuer beste biologische Authentizitaet: 1.0-1.5 Hz verwenden\n")