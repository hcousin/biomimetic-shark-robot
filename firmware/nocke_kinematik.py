"""
Exzentrische Nockenwelle — Kinematik & Visualisierung

Berechnet die Gelenk-Winkel in Echtzeit basierend auf
Nocken-Geometrie und Schubstangen-Längen.
"""

import math
import numpy as np

class NockeKinematics:
    def __init__(self, R0=8, e=3, crank_length=25):
        """
        R0: Mittlerer Radius Nocke (mm)
        e:  Exzentrizität (mm)
        crank_length: Schubstangen-Länge (mm)
        """
        self.R0 = R0
        self.e = e
        self.L = crank_length
        
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
    
    def gelenk_winkel(self, linear_hub_mm):
        """
        Wandelt linearen Hub in Gelenk-Winkel um.
        
        Vereinfachtes Modell: Crank-Slider-Mechanismus
        θ_joint [rad] ≈ arcsin(hub / L)
        
        Konservativ: θ_joint [deg] ≈ (hub / L) × (180/π)
        """
        if abs(linear_hub_mm) > self.L:
            return max(-90, min(90, linear_hub_mm / self.L * 90))
        return math.degrees(math.asin(linear_hub_mm / self.L))
    
    def schwimmzyklus(self, theta_nocke_deg, gleitschuh_position=0):
        """
        Berechnet Gelenk-Winkel für gegeben Nocken-Position
        und Gleitschuh-Position (0°, 90°, 180°, 270°).
        
        Args:
            theta_nocke_deg: Aktuelle Rotation Nockenwelle (0–360°)
            gleitschuh_position: 0, 90, 180, oder 270 Grad
        
        Returns:
            theta_joint: Gelenk-Auslenkung in Grad (±)
        """
        # Effektive Nocken-Position relativ zu Gleitschuh
        theta_eff = theta_nocke_deg - gleitschuh_position
        
        # Linearer Hub
        hub = self.gleitschuh_hub(theta_eff)
        
        # Zu Gelenk-Winkel konvertieren
        theta_j = self.gelenk_winkel(hub)
        return theta_j
    
    def vier_gelenke(self, theta_nocke_deg):
        """Berechnet alle 4 Gelenk-Winkel für gegeben Nocken-Position."""
        j1 = self.schwimmzyklus(theta_nocke_deg, 0)
        j2 = self.schwimmzyklus(theta_nocke_deg, 90)
        j3 = self.schwimmzyklus(theta_nocke_deg, 180)
        j4 = self.schwimmzyklus(theta_nocke_deg, 270)
        return j1, j2, j3, j4
    
    def amplitude_maximal(self):
        """Maximum mögliche Amplitude."""
        return self.gelenk_winkel(self.e)
    
    def print_zyklus(self, steps=9):
        """Tabelle eines kompletten Zyklus."""
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║ NOCKENWELLE KINEMATIK — SCHWIMMZYKLUS                   ║")
        print("║ R₀={}mm, e={}mm, L={}mm → Amplitude=±{:.1f}°".format(
              self.R0, self.e, self.L, self.amplitude_maximal()))
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
        print(" θ_Nocke  │    J1    │    J2    │    J3    │    J4    │ Phase")
        print("──────────┼──────────┼──────────┼──────────┼──────────┼──────────")
        
        for step in range(steps+1):
            theta = (step / steps) * 360
            j1, j2, j3, j4 = self.vier_gelenke(theta)
            
            # Phasenbestimmung
            phase = "Start"
            if 80 < theta < 100: phase = "J1 max+"
            elif 170 < theta < 190: phase = "J1 max-"
            elif 80 < (theta-90) % 360 < 100: phase = "J2 max+"
            
            print(f"  {theta:6.1f}°  │  {j1:+6.1f}° │  {j2:+6.1f}° │  {j3:+6.1f}° │  {j4:+6.1f}° │ {phase}")
        
        print()
        print("BEOBACHTUNG: Alle 4 Gelenke schwingen sinusförmig mit 90° Phasenversatz")
        print("→ Kontinuierliche Körperwelle in beide Richtungen!")
        print()
    
    def phasenverlauf(self):
        """Berechne Phasenverlauf für alle Gelenke."""
        angles = np.linspace(0, 360, 361)
        j1_vals = []
        j2_vals = []
        j3_vals = []
        j4_vals = []
        
        for theta in angles:
            j1, j2, j3, j4 = self.vier_gelenke(theta)
            j1_vals.append(j1)
            j2_vals.append(j2)
            j3_vals.append(j3)
            j4_vals.append(j4)
        
        return angles, j1_vals, j2_vals, j3_vals, j4_vals

# ─── Beispiel: Standard-Hai-Roboter ─────────────────────────
if __name__ == "__main__":
    # Typische Parameter
    k = NockeKinematics(R0=8, e=3, crank_length=25)
    
    print("\n=== HAIFISCH-ROBOTER NOCKENWELLE ===\n")
    k.print_zyklus(steps=12)
    
    # Detaillierte Analyse
    print("\n[Detailanalyse]")
    theta_test = 90  # Nocke bei 90°
    j1, j2, j3, j4 = k.vier_gelenke(theta_test)
    print(f"Bei Nocken-Position θ={theta_test}°:")
    print(f"  J1 = {j1:+.1f}°  (Peduncle)")
    print(f"  J2 = {j2:+.1f}°  (Mid-body)")
    print(f"  J3 = {j3:+.1f}°  (Caudal-base)")
    print(f"  J4 = {j4:+.1f}°  (Tail-tip)")
    print()
    
    # Amplitude
    amp = k.amplitude_maximal()
    print(f"Maximale Amplitude pro Gelenk: ±{amp:.1f}°")
    print(f"Geschätzte Gesamtkörperwelle-Amplitude: ~{amp*0.8:.1f}°")
    print()
    
    # Frequenz-Mapping
    print("[RPM → Frequenz]")
    for rpm in [50, 100, 150, 250]:
        f_hz = rpm / 60
        print(f"  {rpm:3d} RPM → {f_hz:.2f} Hz → {f_hz*0.6:.2f} m/s (geschätzt)")
    print()
    
    # Alternative Nocke (größere Exzentrizität)
    print("\n[Vergleich: Verschiedene Exzentrizitäten]")
    for e_test in [2, 3, 4, 5]:
        k_test = NockeKinematics(R0=8, e=e_test, crank_length=25)
        amp_test = k_test.amplitude_maximal()
        print(f"  e={e_test}mm → Amplitude ±{amp_test:.1f}°")
    print()
