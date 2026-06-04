"""
═══════════════════════════════════════════════════════════════
 HAIFISCH-ROBOTER: Strouhal-Zahl & Hydrodynamik-Optimierer
 Basierend auf: Triantafyllou et al. (1993), Taylor et al. (2003)
═══════════════════════════════════════════════════════════════

Optimale Strouhal-Zahl für Haifische: St = 0.25 – 0.35
St = f * A / U    (f=Frequenz, A=Schwanzschlag-Amplitude, U=Geschwindigkeit)

Verwendung:
  python strouhal_optimizer.py
  → Gibt optimale Parameter für Zielgeschwindigkeit aus
"""

import math

# ─── Roboter-Parameter ───────────────────────────────────────
BODY_LENGTH   = 0.60   # m (Gesamtlänge des Roboters)
TAIL_SPAN     = 0.12   # m (Spannweite der Schwanzflosse, lunate)
TAIL_CHORD    = 0.06   # m (Chord der Schwanzflosse)

# CPG-Grenzwerte
FREQ_MIN, FREQ_MAX = 0.3, 2.5   # Hz
AMP_MIN,  AMP_MAX  = 0.05, 0.25 # m (Schwanzspitzenbewegung, nicht Winkel)

# Optimaler Strouhal-Bereich (Haifische): 0.25–0.35
ST_OPT_LOW  = 0.25
ST_OPT_HIGH = 0.35
ST_OPT      = 0.30   # Zielwert (Mitte des Bandes)

# Schubkoeffizient (empirisch, 3-Gelenk-Roboter)
THRUST_ETA   = 0.65  # Propulsionseffizienz (~65% für BCF carangiform)


def amp_deg_to_m(amp_deg: float, link_length: float = 0.15) -> float:
    """Winkelamplitude (Grad) → lineare Schwanzspitzen-Amplitude (m)"""
    return 2 * link_length * math.sin(math.radians(amp_deg))


def m_to_amp_deg(amp_m: float, link_length: float = 0.15) -> float:
    """Lineare Amplitude (m) → Winkel (Grad)"""
    ratio = amp_m / (2 * link_length)
    ratio = min(ratio, 0.99)
    return math.degrees(math.asin(ratio))


def strouhal(freq: float, amp_m: float, speed: float) -> float:
    """St = f * A / U"""
    if speed < 1e-6: return 0.0
    return freq * amp_m / speed


def speed_from_st(freq: float, amp_m: float, st: float) -> float:
    """U = f * A / St"""
    return freq * amp_m / st


def drag_power(speed: float, cd: float = 0.08, frontal_area: float = 0.005) -> float:
    """Schätzung Widerstandsleistung [W] (Wasser ρ=1000 kg/m³)"""
    rho = 1000.0
    return 0.5 * rho * cd * frontal_area * speed**3


def thrust_power(freq: float, amp_m: float) -> float:
    """Grobe Schätzung Vortriebsleistung [W]"""
    # Schub ~ ρ·A_fin·(2·f·amp)²·TAIL_SPAN
    rho = 1000.0
    v_tail = 2 * freq * amp_m
    return THRUST_ETA * 0.5 * rho * TAIL_CHORD * TAIL_SPAN * v_tail**2


def optimize(target_speed: float) -> dict:
    """
    Findet optimale CPG-Parameter für Zielgeschwindigkeit.
    Sucht Kombination (freq, amp) die:
      1. Strouhal-Zahl im optimalen Band hält
      2. Schub >= Widerstand
      3. Frequenz und Amplitude in Hardware-Grenzen
    """
    best = None
    best_score = float('inf')

    for f in [x * 0.05 for x in range(int(FREQ_MIN/0.05), int(FREQ_MAX/0.05)+1)]:
        for a in [x * 0.005 for x in range(int(AMP_MIN/0.005), int(AMP_MAX/0.005)+1)]:
            st = strouhal(f, a, target_speed)
            v_actual = speed_from_st(f, a, ST_OPT)

            # Bewertungsfunktion: Nähe zu Zielgeschwindigkeit + St-Abweichung
            st_err = abs(st - ST_OPT)
            v_err  = abs(v_actual - target_speed)
            score  = st_err * 2.0 + v_err * 5.0

            # Feasibility-Check
            if not (FREQ_MIN <= f <= FREQ_MAX): continue
            if not (AMP_MIN  <= a <= AMP_MAX):  continue
            if st < ST_OPT_LOW * 0.8: continue  # zu weit weg

            if score < best_score:
                best_score = score
                best = {'freq': f, 'amp_m': a, 'st': st,
                        'v_est': v_actual, 'score': score}

    if best is None:
        return {'error': 'Keine Lösung gefunden'}

    best['amp_deg_j1'] = m_to_amp_deg(best['amp_m'] * 0.65)
    best['amp_deg_j2'] = m_to_amp_deg(best['amp_m'] * 0.90)
    best['drag_W']     = drag_power(target_speed)
    best['thrust_W']   = thrust_power(best['freq'], best['amp_m'])
    best['eta']        = min(best['drag_W'] / best['thrust_W'], 1.0) if best['thrust_W'] > 0 else 0
    return best


def reynolds(speed: float, length: float = BODY_LENGTH) -> float:
    """Re = U·L / ν,  Wasser ν = 1e-6 m²/s"""
    return speed * length / 1e-6


def print_header():
    print("=" * 62)
    print("  HAIFISCH-ROBOTER — HYDRODYNAMIK OPTIMIERER")
    print("  Optimales Strouhal-Band: {:.2f} – {:.2f}".format(ST_OPT_LOW, ST_OPT_HIGH))
    print("=" * 62)


def print_table():
    """Tabelle optimaler Parameter für verschiedene Geschwindigkeiten"""
    print_header()
    print(f"\n{'Geschw.':>8} {'Freq':>6} {'Amp J1':>7} {'Amp J2':>7} "
          f"{'St':>5} {'Re':>8} {'η':>5}")
    print("-" * 62)
    for v in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2]:
        r = optimize(v)
        if 'error' not in r:
            print(f"{v:>7.1f}m/s {r['freq']:>5.2f}Hz {r['amp_deg_j1']:>6.1f}°"
                  f" {r['amp_deg_j2']:>6.1f}°  {r['st']:>4.2f}"
                  f" {reynolds(v):>8.0f}  {r['eta']:>4.0%}")
    print()


def print_detail(v: float):
    """Detaillierte Ausgabe für eine Zielgeschwindigkeit"""
    r = optimize(v)
    print_header()
    print(f"\nZielgeschwindigkeit: {v:.2f} m/s ({v/BODY_LENGTH:.1f} BL/s)\n")
    if 'error' in r:
        print("  Fehler:", r['error']); return
    print(f"  Empfohlene Frequenz : {r['freq']:.2f} Hz")
    print(f"  Amplitude J1 (±)    : {r['amp_deg_j1']:.1f}°")
    print(f"  Amplitude J2 (±)    : {r['amp_deg_j2']:.1f}°")
    print(f"  Schwanz-Amplitude   : {r['amp_m']*100:.1f} cm")
    print(f"  Strouhal-Zahl       : {r['st']:.3f}  "
          f"({'optimal' if ST_OPT_LOW<=r['st']<=ST_OPT_HIGH else 'suboptimal'})")
    print(f"  Reynolds-Zahl       : {reynolds(v):.0f}")
    print(f"  Schätzung Schub     : {r['thrust_W']:.2f} W")
    print(f"  Schätzung Widerst.  : {r['drag_W']:.3f} W")
    print(f"  Schub-Effizienz η   : {r['eta']:.0%}")
    print(f"\n  → CPG Arduino-Code:")
    print(f"     float freq = {r['freq']:.2f}f;")
    print(f"     float amp1 = {r['amp_deg_j1']:.1f}f;")
    print(f"     float amp2 = {r['amp_deg_j2']:.1f}f;")
    print()


if __name__ == "__main__":
    print_table()
    print_detail(0.5)
    print_detail(0.8)
    print("\nFür beliebige Geschwindigkeit: optimize(v_m_s)")
    print("Beispiel: python -c \"from strouhal_optimizer import *; print(optimize(0.6))\"")
