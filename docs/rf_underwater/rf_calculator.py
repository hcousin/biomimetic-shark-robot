#!/usr/bin/env python3
"""
RF Signaldämpfung Unterwasser — Rechner und Visualisierung
Basierend auf der Skin-Tiefe (Skin Depth) Formel

Verwendung:
  python3 rf_calculator.py
  python3 rf_calculator.py --depth 1.5 --water freshwater
"""
import math
import argparse

WATER_TYPES = {
    "freshwater":  100,    # Süsswasser [Ω·m]
    "brackish":    10,     # Brakwasser
    "seawater":    0.2,    # Meerwasser
    "distilled":   10000,  # Destilliertes Wasser
}

FREQUENCIES = [
    ("WiFi 2.4 GHz",    2.4e9),
    ("WiFi 5 GHz",      5.0e9),
    ("433 MHz (LoRa)",  433e6),
    ("868 MHz (LoRa)",  868e6),
    ("27 MHz (RC)",     27e6),
    ("3.5 MHz (HF)",    3.5e6),
    ("300 kHz (LF)",    300e3),
    ("40 kHz (LF)",     40e3),
]

def skin_depth(rho_ohm_m: float, freq_hz: float) -> float:
    """Skin-Tiefe δ = 503 × sqrt(ρ/f)"""
    return 503.0 * math.sqrt(rho_ohm_m / freq_hz)

def attenuation_db(depth_m: float, skin_d_m: float) -> float:
    """Dämpfung in dB bei Tiefe d: L = 20*log10(e^(-d/δ))"""
    if skin_d_m <= 0:
        return -999.0
    return 20.0 * math.log10(math.exp(-depth_m / skin_d_m))

def usable(att_db: float) -> str:
    if att_db > -6:
        return "✓ Brauchbar"
    elif att_db > -20:
        return "~ Grenzwertig"
    else:
        return "✗ Unbrauchbar"

def print_table(rho: float, depths: list):
    print(f"\n{'─'*80}")
    header = f"  {'Frequenz':<22}"
    for d in depths:
        header += f"  {f'@{d}m [dB]':>12}"
    header += f"  {'δ [m]':>8}  Empfehlung"
    print(header)
    print(f"{'─'*80}")
    
    for fname, f in FREQUENCIES:
        d_skin = skin_depth(rho, f)
        row = f"  {fname:<22}"
        last_att = 0
        for d in depths:
            att = attenuation_db(d, d_skin)
            last_att = att
            row += f"  {att:>12.1f}"
        row += f"  {d_skin:>8.3f}  {usable(last_att)}"
        print(row)
    print(f"{'─'*80}\n")

def ascii_depth_chart(rho: float, freq_hz: float, fname: str, max_depth=3.0):
    d_skin = skin_depth(rho, freq_hz)
    print(f"\n  Signalstärke vs. Tiefe: {fname}")
    print(f"  Skin-Tiefe δ = {d_skin:.3f} m")
    print(f"  {'Tiefe':>6}  {'dB':>7}  Balken")
    print(f"  {'─'*50}")
    
    for d_i in range(0, int(max_depth*10)+1, 2):
        d = d_i / 10.0
        att = attenuation_db(d, d_skin)
        bar_len = max(0, int((att + 80) / 80 * 40))
        bar = "█" * bar_len
        marker = " ← MIN BRAUCHBAR" if abs(att - (-8.686)) < 0.5 else ""
        print(f"  {d:>5.1f}m  {att:>6.1f}  {bar}{marker}")

def recommend(rho: float, target_depth: float) -> str:
    usable_freqs = []
    for fname, f in FREQUENCIES:
        d_skin = skin_depth(rho, f)
        att = attenuation_db(target_depth, d_skin)
        if att > -8.7:
            usable_freqs.append((fname, f, d_skin, att))
    
    water_name = {100:"Süsswasser", 10:"Brakwasser", 0.2:"Meerwasser"}.get(rho, f"ρ={rho}Ω·m")
    
    print(f"\n{'═'*60}")
    print(f"  EMPFEHLUNG: {target_depth}m Tiefe in {water_name}")
    print(f"{'═'*60}")
    
    if not usable_freqs:
        print(f"  ✗ Kein Standard-RF-System brauchbar!")
        print(f"  → TETHER-KABEL (RS485 4-adrig, ~CHF 15)")
        print(f"  → HYBRID: WiFi an Oberfläche + Autonomer Modus")
        print(f"  → AKUSTISCH: Piezo-Wandler 20-200 kHz")
    else:
        print(f"  RF brauchbar bei {target_depth}m:")
        for fname, f, d_skin, att in usable_freqs:
            print(f"  ✓ {fname} — δ={d_skin:.2f}m, {att:.1f}dB")
    
    if target_depth >= 0.8:
        print(f"\n  Für dieses Projekt (Shark Robot @ {target_depth}m):")
        print(f"  1. TETHER RS485 (sofort, CHF 15, zuverlässig)")
        print(f"  2. HYBRID (WiFi Oberfläche + autonom bei Tiefe)")
        print(f"  3. AKUSTISCH DIY (Piezo + HC-SR04 Schaltung)")
    print()

def main():
    parser = argparse.ArgumentParser(description="RF Unterwasser Rechner")
    parser.add_argument("--depth", type=float, default=1.5, help="Zieltiefe in Metern")
    parser.add_argument("--water", choices=list(WATER_TYPES.keys()), default="freshwater")
    parser.add_argument("--chart", action="store_true", help="ASCII-Chart anzeigen")
    args = parser.parse_args()
    
    rho = WATER_TYPES[args.water]
    
    print(f"\n╔══════════════════════════════════════════════════════════════╗")
    print(f"║  RF Unterwasser Rechner — Shark Robot Projekt               ║")
    print(f"║  Skin-Tiefe: δ = 503 × √(ρ/f)                             ║")
    print(f"╚══════════════════════════════════════════════════════════════╝")
    print(f"\n  Wasser: {args.water} (ρ={rho} Ω·m)")
    
    print_table(rho, [0.3, 0.5, 1.0, 1.5, 2.0])
    recommend(rho, args.depth)
    
    if args.chart:
        ascii_depth_chart(rho, 433e6, "433 MHz (aktuell)")
        ascii_depth_chart(rho, 27e6,  "27 MHz (Empfehlung)")

if __name__ == "__main__":
    main()
