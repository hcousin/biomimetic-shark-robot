"""
Exzentrische Nockenwelle — Kinematik & Visualisierung
Hybrid-Design: J1/J2 aktiv (Nockenwelle), J3/J4 passiv (TPU-Federgelenke)

Branch: dev/hybrid-passive-tail
"""

import math
import numpy as np

# ─── Aktive Gelenke (Nockenwelle, e=3mm) ────────────────────
ACTIVE_LEVERS = {
    'J1': 30,  # mm → arcsin(3/30) ≈ ±5.7°
    'J2': 25,  # mm → arcsin(3/25) ≈ ±6.9°
}

# ─── Passive Gelenke (TPU-Federblöcke) ──────────────────────
# Steifigkeit k [N·mm/°], Dämpfung d, Trägheit m [kg·mm²]
PASSIVE_JOINTS = {
    'J3': {'k': 39.5, 'd': 4.0, 'm': 1.0, 'shore': '95A'},
    'J4': {'k': 25.3, 'd': 2.5, 'm': 1.0, 'shore': '85A'},
}


class NockeKinematics:
    def __init__(self, R0=8, e=3, active_levers=None, passive_joints=None):
        """
        R0:             Mittlerer Radius Nocke (mm)
        e:              Exzentrizität (mm) — kurze Welle, nur J1+J2
        active_levers:  Dict Hebellängen aktive Gelenke
        passive_joints: Dict Federparameter passive Gelenke
        """
        self.R0 = R0
        self.e  = e
        self.active  = active_levers  if active_levers  is not None else ACTIVE_LEVERS.copy()
        self.passive = passive_joints if passive_joints is not None else PASSIVE_JOINTS.copy()

        # Zustand der passiven Gelenke (für Simulation)
        self._passive_state = {k: {'theta': 0.0, 'omega': 0.0} for k in self.passive}

    # ── Nocken-Grundfunktionen ───────────────────────────────
    def gleitschuh_hub(self, theta_nocke_deg, gleitschuh_pos_deg):
        """Linearer Hub des Gleitschuhs: h = e·cos(θ_nocke - θ_pos)"""
        theta_eff = math.radians(theta_nocke_deg - gleitschuh_pos_deg)
        return self.e * math.cos(theta_eff)

    def aktiv_winkel(self, hub_mm, joint_key):
        """θ = arcsin(h / L) für aktive Gelenke"""
        L = self.active[joint_key]
        hub_clamped = max(-L + 0.001, min(L - 0.001, hub_mm))
        return math.degrees(math.asin(hub_clamped / L))

    # ── Aktive Gelenke ───────────────────────────────────────
    def aktive_gelenke(self, theta_nocke_deg):
        """Berechnet J1 und J2 aus Nocken-Position."""
        h1 = self.gleitschuh_hub(theta_nocke_deg,  0)
        h2 = self.gleitschuh_hub(theta_nocke_deg, 90)
        j1 = self.aktiv_winkel(h1, 'J1')
        j2 = self.aktiv_winkel(h2, 'J2')
        return j1, j2

    # ── Passive Gelenke (Feder-Dämpfer-Simulation) ───────────
    def passive_step(self, j2_winkel, dt_s):
        """
        Simuliert die passiven TPU-Gelenke J3 + J4.

        J3 wird durch J2 angetrieben (Trägheit + Feder):
          m·θ̈ + d·θ̇ + k·(θ - θ_input) = 0

        J4 wird durch J3 angetrieben (gleiche Logik).

        Args:
            j2_winkel: Aktueller Winkel J2 [°] — treibt J3 an
            dt_s:      Zeitschritt [s]

        Returns:
            (j3, j4) Winkel in Grad
        """
        # J3: angetrieben durch J2
        s3 = self._passive_state['J3']
        p3 = self.passive['J3']
        torque3 = p3['k'] * (j2_winkel - s3['theta']) - p3['d'] * s3['omega']
        alpha3 = torque3 / p3['m']
        s3['omega'] += alpha3 * dt_s
        s3['theta'] += s3['omega'] * dt_s

        # J4: angetrieben durch J3
        s4 = self._passive_state['J4']
        p4 = self.passive['J4']
        torque4 = p4['k'] * (s3['theta'] - s4['theta']) - p4['d'] * s4['omega']
        alpha4 = torque4 / p4['m']
        s4['omega'] += alpha4 * dt_s
        s4['theta'] += s4['omega'] * dt_s

        return s3['theta'], s4['theta']

    def reset_passive(self):
        """Setzt Zustand der passiven Gelenke zurück."""
        for k in self._passive_state:
            self._passive_state[k] = {'theta': 0.0, 'omega': 0.0}

    # ── Vollständiger Zyklus ─────────────────────────────────
    def simulate(self, freq_hz=1.0, duration_s=3.0, dt_s=0.005):
        """
        Simuliert den kompletten Roboter über mehrere Zyklen.

        Args:
            freq_hz:    Schwimmfrequenz [Hz]
            duration_s: Simulationsdauer [s]
            dt_s:       Zeitschritt [s]

        Returns:
            Dict mit Zeitreihen für J1–J4
        """
        self.reset_passive()
        t_vals  = np.arange(0, duration_s, dt_s)
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
            't':  t_vals,
            'J1': np.array(j1_vals),
            'J2': np.array(j2_vals),
            'J3': np.array(j3_vals),
            'J4': np.array(j4_vals),
        }

    # ── Ausgaben ────────────────────────────────────────────
    def amplitude_aktiv(self, joint_key):
        """Max. Amplitude aktives Gelenk."""
        L = self.active[joint_key]
        return math.degrees(math.asin(self.e / L))

    def resonanzfrequenz(self, joint_key):
        """Resonanzfrequenz des passiven Gelenks [Hz]."""
        p = self.passive[joint_key]
        return (1 / (2 * math.pi)) * math.sqrt(p['k'] / p['m'])

    def print_info(self):
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  HYBRID-DESIGN: Aktive Nockenwelle + Passive TPU-Gelenke   ║")
        print("║  R₀={}mm, e={}mm (kurze Welle, nur J1+J2)".format(self.R0, self.e).ljust(63) + "║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║  AKTIVE GELENKE (Nockenwelle)                               ║")
        for key, L in self.active.items():
            amp = self.amplitude_aktiv(key)
            print(f"║    {key} (L={L}mm) → ±{amp:.1f}°".ljust(63) + "║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║  PASSIVE GELENKE (TPU-Feder)                                ║")
        for key, p in self.passive.items():
            f_res = self.resonanzfrequenz(key)
            print(f"║    {key} (Shore {p['shore']}, k={p['k']}) → f_res={f_res:.2f} Hz".ljust(63) + "║")
        print("╚══════════════════════════════════════════════════════════════╝\n")

    def print_zyklus(self, freq_hz=1.0, steps=8):
        """Tabelle eines kompletten Zyklus bei gegebener Frequenz."""
        self.reset_passive()
        dt = 1.0 / (freq_hz * steps * 10)  # fein auflösen, dann samplen
        result = self.simulate(freq_hz=freq_hz, duration_s=2.0/freq_hz, dt_s=dt)

        # Sample an steps+1 gleichmäßigen Punkten im letzten Zyklus
        n = len(result['t'])
        cycle_start = n // 2  # zweite Hälfte (eingeschwungen)
        indices = [cycle_start + int(i * (n - 1 - cycle_start) / steps) for i in range(steps + 1)]

        print(f" θ_Nocke  │   J1(aktiv) │   J2(aktiv) │  J3(passiv) │  J4(passiv)")
        print("──────────┼─────────────┼─────────────┼─────────────┼─────────────")
        for idx in indices:
            theta = (result['t'][idx] * freq_hz * 360) % 360
            print(f"  {theta:5.1f}°  │  {result['J1'][idx]:+7.2f}°  │  {result['J2'][idx]:+7.2f}°  │  {result['J3'][idx]:+7.2f}°  │  {result['J4'][idx]:+7.2f}°")
        print()


# ─── Hauptprogramm ───────────────────────────────────────────
if __name__ == "__main__":
    k = NockeKinematics()
    k.print_info()

    print("=== Zyklus bei 1.0 Hz ===")
    k.print_zyklus(freq_hz=1.0)

    print("=== Zyklus bei 1.5 Hz ===")
    k.print_zyklus(freq_hz=1.5)

    # Resonanzcheck
    print("[Resonanz-Abstimmung]")
    for key in PASSIVE_JOINTS:
        f_res = k.resonanzfrequenz(key)
        print(f"  {key}: f_resonanz = {f_res:.2f} Hz → optimal bei {f_res:.1f} Hz schwimmen")
    print()

    print("[RPM → Schwimmfrequenz (Getriebe 40:1)]")
    for pct in [10, 25, 50, 75]:
        rpm_motor = pct / 100 * 9990
        rpm_nocke = rpm_motor / 40
        f_hz = rpm_nocke / 60
        print(f"  {pct:3d}% Throttle → {f_hz:.2f} Hz")
