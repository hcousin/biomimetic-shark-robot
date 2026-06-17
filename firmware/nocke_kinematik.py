"""
Exzentrische Nockenwelle — Kinematik & Visualisierung

Berechnet die Gelenk-Winkel in Echtzeit basierend auf
Nocken-Geometrie und variablen Schubstangen-Längen (J1–J4).
"""

import math
import numpy as np

# Variable Hebelarm-Längen pro Gelenk (progressive Amplituden)
LEVER_LENGTHS = {
    'J1': 30,  # mm — Kopf-nah, kleine Amplitude (±11.3°)
    'J2': 25,  # mm — Vordermitte         (±13.5°)
    'J3': 18,  # mm — Hintermitte         (±18.4°)
    'J4': 12,  # mm — Schwanz, max. Amplitude (±26.6°)
}

class NockeKinematics:
    def __init__(self, R0=8, e=3, lever_lengths=None):
        """
        R0:            Mittlerer Radius Nocke (mm)
        e:             Exzentrizität (mm)
        lever_lengths: Dict mit Hebellängen pro Gelenk (mm)
                       Standard: LEVER_LENGTHS (progressive)
        """
        self.R0 = R0
        self.e = e
        self.levers = lever_lengths if lever_lengths is not None else LEVER_LENGTHS.copy()

    def nocke_radius(self, theta_deg):
        """R(θ) = R₀ + e·cos(θ) — Polarradius der Nocke"""
        theta = math.radians(theta_deg)
        return self.R0 + self.e * math.cos(theta)

    def gleitschuh_hub(self, theta_deg):
        """
        Linearer Hub des Gleitschuhs an Schubstangen-Halter.

        Geometrie: Nocke rotiert um Achse. Gleitschuh sitzt auf
        radialer Linie und kann linear bewegt werden.

        Hub = R(θ) - R₀ = e·cos(θ)  [in mm, bezogen auf Mittellage]
        """
        return self.e * math.cos(math.radians(theta_deg))

    def gelenk_winkel(self, linear_hub_mm, joint_key):
        """
        Wandelt linearen Hub in Gelenk-Winkel um.

        Crank-Slider-Mechanismus:
        θ_joint [deg] = arcsin(hub / L)

        Args:
            linear_hub_mm: Linearer Hub vom Gleitschuh (mm)
            joint_key:     'J1', 'J2', 'J3' oder 'J4'
        """
        L = self.levers[joint_key]
        if abs(linear_hub_mm) >= L:
            return math.copysign(90.0, linear_hub_mm)
        return math.degrees(math.asin(linear_hub_mm / L))

    def schwimmzyklus(self, theta_nocke_deg, gleitschuh_position, joint_key):
        """
        Berechnet Gelenk-Winkel für gegebene Nocken-Position,
        Gleitschuh-Position und Gelenk-Schlüssel.

        Args:
            theta_nocke_deg:    Aktuelle Rotation Nockenwelle (0–360°)
            gleitschuh_position: 0, 90, 180 oder 270 Grad
            joint_key:          'J1', 'J2', 'J3' oder 'J4'

        Returns:
            theta_joint: Gelenk-Auslenkung in Grad (±)
        """
        theta_eff = theta_nocke_deg - gleitschuh_position
        hub = self.gleitschuh_hub(theta_eff)
        return self.gelenk_winkel(hub, joint_key)

    def vier_gelenke(self, theta_nocke_deg):
        """Berechnet alle 4 Gelenk-Winkel für gegebene Nocken-Position."""
        j1 = self.schwimmzyklus(theta_nocke_deg,   0, 'J1')
        j2 = self.schwimmzyklus(theta_nocke_deg,  90, 'J2')
        j3 = self.schwimmzyklus(theta_nocke_deg, 180, 'J3')
        j4 = self.schwimmzyklus(theta_nocke_deg, 270, 'J4')
        return j1, j2, j3, j4

    def amplitude_maximal(self, joint_key):
        """Maximum mögliche Amplitude für ein bestimmtes Gelenk."""
        return self.gelenk_winkel(self.e, joint_key)

    def print_zyklus(self, steps=9):
        """Tabelle eines kompletten Zyklus."""
        amps = {k: self.amplitude_maximal(k) for k in self.levers}
        print("╔════════════════════════════════════════════════════════════════════╗")
        print("║ NOCKENWELLE KINEMATIK — VARIABLE HEBELARME                       ║")
        print("║ R₀={}mm, e={}mm".format(self.R0, self.e).ljust(69) + "║")
        print("║ L₁={L1}mm(J1) | L₂={L2}mm(J2) | L₃={L3}mm(J3) | L₄={L4}mm(J4)".format(
            L1=self.levers['J1'], L2=self.levers['J2'],
            L3=self.levers['J3'], L4=self.levers['J4']).ljust(69) + "║")
        print("║ Amp: J1=±{a1:.1f}° | J2=±{a2:.1f}° | J3=±{a3:.1f}° | J4=±{a4:.1f}°".format(
            a1=amps['J1'], a2=amps['J2'], a3=amps['J3'], a4=amps['J4']).ljust(69) + "║")
        print("╚════════════════════════════════════════════════════════════════════╝")
        print()
        print(" θ_Nocke  │    J1(L=30)  │    J2(L=25)  │    J3(L=18)  │    J4(L=12)  ")
        print("──────────┼──────────────┼──────────────┼──────────────┼──────────────")

        for step in range(steps + 1):
            theta = (step / steps) * 360
            j1, j2, j3, j4 = self.vier_gelenke(theta)
            print(f"  {theta:6.1f}°  │   {j1:+7.2f}°   │   {j2:+7.2f}°   │   {j3:+7.2f}°   │   {j4:+7.2f}°")

        print()
        print("BEOBACHTUNG: Progressive Amplituden J1 < J2 < J3 < J4")
        print("→ Kontinuierliche Körperwelle mit wachsender Amplitude Richtung Schwanz!")
        print()

    def phasenverlauf(self):
        """Berechne Phasenverlauf für alle Gelenke."""
        angles = np.linspace(0, 360, 361)
        j1_vals, j2_vals, j3_vals, j4_vals = [], [], [], []

        for theta in angles:
            j1, j2, j3, j4 = self.vier_gelenke(theta)
            j1_vals.append(j1)
            j2_vals.append(j2)
            j3_vals.append(j3)
            j4_vals.append(j4)

        return angles, j1_vals, j2_vals, j3_vals, j4_vals


# ─── Beispiel: Standard-Hai-Roboter ─────────────────────────────────────────
if __name__ == "__main__":
    k = NockeKinematics(R0=8, e=3)  # lever_lengths = LEVER_LENGTHS (Standard)

    print("\n=== HAIFISCH-ROBOTER NOCKENWELLE — VARIABLE HEBELARME ===\n")
    k.print_zyklus(steps=12)

    # Detaillierte Analyse
    print("\n[Detailanalyse bei θ_Nocke = 90°]")
    theta_test = 90
    j1, j2, j3, j4 = k.vier_gelenke(theta_test)
    print(f"  J1 = {j1:+.2f}°  (Peduncle,   L={k.levers['J1']}mm)")
    print(f"  J2 = {j2:+.2f}°  (Mid-body,   L={k.levers['J2']}mm)")
    print(f"  J3 = {j3:+.2f}°  (Caudal-base,L={k.levers['J3']}mm)")
    print(f"  J4 = {j4:+.2f}°  (Tail-tip,   L={k.levers['J4']}mm)")
    print()

    # Amplituden-Übersicht
    print("[Maximale Amplituden pro Gelenk]")
    for key in ['J1', 'J2', 'J3', 'J4']:
        amp = k.amplitude_maximal(key)
        L = k.levers[key]
        print(f"  {key} (L={L:2d}mm) → ±{amp:.1f}°")
    print()

    # Frequenz-Mapping
    print("[RPM → Schwimmfrequenz]")
    for rpm in [50, 100, 150, 250]:
        f_hz = rpm / 60
        print(f"  {rpm:3d} RPM → {f_hz:.2f} Hz → {f_hz * 0.6:.2f} m/s (geschätzt)")
    print()

    # Vergleich: Einheitliche vs. variable Hebelarme
    print("\n[Vergleich: Einheitliche (L=25mm) vs. Variable Hebelarme]")
    k_uniform = NockeKinematics(R0=8, e=3,
                                lever_lengths={'J1': 25, 'J2': 25, 'J3': 25, 'J4': 25})
    print(f"  {'Gelenk':<6} {'Einheitlich (L=25mm)':>22} {'Variable Hebelarme':>22}")
    print(f"  {'------':<6} {'--------------------':>22} {'------------------':>22}")
    for key in ['J1', 'J2', 'J3', 'J4']:
        a_uni = k_uniform.amplitude_maximal(key)
        a_var = k.amplitude_maximal(key)
        print(f"  {key:<6}  ±{a_uni:>5.1f}°{' ':>14}  ±{a_var:>5.1f}°")
    print()
