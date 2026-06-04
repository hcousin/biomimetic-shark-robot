# Biomimetic Haifisch — Single Brushless Motor + Exzentrische Nockenwelle

## Konzept-Übersicht

```
Brushless Outrunner Motor (KV=900, 20 A ESC)
        ↓
Planetengetriebe 1:3 (RPM reduziert)
        ↓
Exzentrische Nockenwelle (Ø 12 mm Achse)
        ↓
4 × Schubstangen (Cam Follower)
        ↓
4 × Schwanzgelenke (J1, J2, J3, J4)
        ↓
Kontinuierliche Haifisch-Körperwelle
```

**Physikalisches Prinzip:**
- Motor rotiert kontinuierlich mit variabler RPM
- Exzentrische Nocke erzeugt sinusoidale Bewegung jedes Gleiters
- 4 Gleitschuh-Positionen (0°, 90°, 180°, 270°) → automatische Phasenversätze
- Keine digitale CPG nötig — rein mechanisch!

---

## Exzentrische Nockenwelle: Design

### Geometrie

```
Nocken-Profil (axialer Querschnitt):
  
  Radius-Variation:  R(θ) = R₀ + e·cos(θ)
  
  Wo:
    R₀ = 8 mm    (Mittlerer Radius)
    e  = 3 mm    (Exzentrizität)
    θ  = Winkel auf Nocke (0–360°)
    
  → Max-Radius = 11 mm (bei θ=0°)
  → Min-Radius = 5 mm  (bei θ=180°)
  → Hub pro Schubstange = 2·e = 6 mm linear
```

### Schubstangen-Hube in Winkel umrechnen

Jede Schubstange sitzt auf einer Gleitschuh-Führung und wandelt lineare Bewegung in Gelenkwinkel um:

```
L_crank = Länge Schubstange = 25 mm (von Nockenwelle-Achse zu Gelenk-Achse)
h_linear = 6 mm  (max. linearer Hub auf Nocke)

θ_joint = atan(h_linear / L_crank) = atan(6/25) ≈ 13.5° linear → ±27° mit Hebel

Besser: Exzenter + 25mm Schubstange erzeugt sinusoidales Gelenk-Ausgangssignal
der Form:  θ(t) = Θ_max · sin(2πf·t + φ_i)
```

### Material & Fertigung

| Komponente | Material | Abmessungen | Notizen |
|---|---|---|---|
| Nockenwelle | Edelstahl 1.4104 | Ø 12 mm × 120 mm | Exzentrizität 3 mm |
| Nocken-Gewicht | 150–200 g | — | Ausbalancierung wichtig! |
| Gleitschuh (×4) | Nylon/Teflon | 12×8 mm Fläche | Low-friction bearing |
| Schubstangen (×4) | Aluminium 7075 | Ø 6 mm × 25 mm | Leicht, steif |
| Achsen-Lager | Ø 12 mm Kugellager | — | 6001-2RS (wasserdicht) |

---

## Phasenversätze — Automatische Wellenerzeugung

```
Gleitschuh-Positionen auf Nockenwelle (Aufsicht):

        0°
         │
    4    │    1
     \   │   /
      \ │ /
  180° ─X─ 0°  ← Nockenwelle-Achse
      / │ \
     /   │   \
    3    │    2
         │
        180°

J1 (Position 0°):    θ₁(t) = 25° · sin(2πf·t)
J2 (Position 90°):   θ₂(t) = 20° · sin(2πf·t − π/2)  ← 90° Phasenlag
J3 (Position 180°):  θ₃(t) = 15° · sin(2πf·t − π)    ← 180° Phasenlag
J4 (Position 270°):  θ₄(t) = 10° · sin(2πf·t − 3π/2) ← 270° Phasenlag

RESULTAT: Kontinuierliche, rückwärts laufende Körperwelle
          wie bei echtem Haifisch! ✓
```

---

## Brushless Motor & ESC

### Motor-Auswahl
```
Typ:           Outrunner Brushless (KV = 900)
Leistung:      20–30 W nominal
Lagerung:      Kugellager (wasserdicht)
Rotor-Größe:   Ø 35 mm × 25 mm
Gewicht:       ~60 g
Größe:         60 × 40 × 20 mm
Spannung:      3S LiPo 11.1V nominal
Strom:         2.5–3.5 A nominal (5 A Peak bei Anfahrt)

Drehzahl-Bereich:
  KV = 900  →  U[V] × KV = RPM
  11.1V × 900 = 9990 RPM (Vollgas)
  
Getriebe 1:3  →  9990 / 3 ≈ 3330 RPM
            ÷ 60 ≈ 55.5 Hz Nockenwellen-Drehzahl
            ÷ 1 Umdrehung = 1 Schwimmzyklus
            → f_swim = 55.5 Hz Maximal ❌ Viel zu schnell!
```

### RPM-Reduktion notwendig

Für natürliche Schwimmfrequenzen (0.5–2.0 Hz) brauchen wir:

```
Zielfrequenz: f = 1.5 Hz = 90 Umdrehungen/Minute

Getriebe-Verhältnis:
  3330 RPM / 90 RPM = 37:1  Gesamtreduktion nötig!
  
Lösung:
  Brushless KV=900 + Planetengetriebe 10:1 (im Motor integriert)
  + externe Schnecken-Zahnradwelle 4:1
  = 40:1 Gesamtreduktion
  
  Dann: 9990 / 40 ≈ 250 RPM Nockenwellen-Drehzahl
        250 / 60 ≈ 4.2 Hz Nockenwelle
  
  ❌ Immer noch zu schnell!
```

**Alternative: Gelöst über PWM-Duty-Cycle!**
```
ESC mit BEC (Battery Elimination Circuit) ansteuern
PWM:  0–5 V (von ESP32 GPIO)
      0% Duty = 0 RPM
      50% Duty = 5000 RPM (halb Vollgas)
      100% Duty = 10000 RPM
      
Mit 40:1 Getriebe:
  50% Duty → 5000 / 40 = 125 RPM = 2.1 Hz ✓ Perfekt!
  25% Duty → 2500 / 40 = 62.5 RPM = 1.0 Hz ✓
  10% Duty → 1000 / 40 = 25 RPM = 0.4 Hz (langsames Rückwärts)
```

### ESC-Spezifikation

```
Typ:            Brushless ESC (20A kontinuierlich)
Frequenz:       8 kHz PWM
Spannung:       3S LiPo (11.1V) + 1S Safe
Programmierbar: Throttle-Kurve, Bremsart
Gehäuse:        Aluminiumgehäuse mit Kühlriffel
Wassergehalt:   Potting-komplett oder teilweise (prüfen!)
Verkabelung:    2mm Goldstecker (Motor) + JST-SM (BEC out)

Empfehlung: Hobbywing Platinum 20A oder ähnlich
```

---

## Elektronik-Layout (Vereinfacht)

```
LiPo 3S 11.1V
    │
    ├─→ [BEC 5V/3A] ──→ ESP32 VIN + PCA9685
    │
    ├─→ [ESC 20A] ←──── PWM Signal (ESP32 Pin 25)
         │
         └─→ Brushless Motor (3 Phasen)
              │
              └─→ Planetengetriebe 10:1
                   │
                   └─→ Externe Schnecke 4:1
                        │
                        └─→ Exzentrische Nockenwelle
                             │
                             ├─→ Schubstange J1
                             ├─→ Schubstange J2
                             ├─→ Schubstange J3
                             └─→ Schubstange J4
                             
Servo-Kanäle frei:
  PCA9685 CH0 → Brustflosse Links (unverändert)
  PCA9685 CH1 → Brustflosse Rechts
  PCA9685 CH2 → Ballast-Kolben
  (Reste frei für Sensoren, Lichter, etc.)
```

---

## Gelenk-Längsschnitt (Einzelgelenk J1)

```
                   Nockenwelle
                   (rotierend)
              ┌────────•────────┐
              │                 │
         Gleitschuh         Rückenlager
         (Nylon)            (6001-2RS)
          ╔════╗
          ║ ● ║ ← Hub linear ±3mm
          ╚════╝
            │
       Schubstange
       (Al, Ø6 mm)
            │
        ╭───┴───╮
        │       │
    Gelenk-Flansch L    Gelenk-Flansch R
    (Verbindung zu       (zum nächsten
     Körper-Segment)     Segment)
        ╱───╲              ╱───╲
       /     \            /     \
   Body A   Link 1    Link 1   Link 2
   Ø8mm     Ø8mm      Ø8mm     Ø8mm
   Achsen aus Edelstahl
```

---

## CAD-Teile für 3D-Druck

### Exzentrische Nockenwelle (NICHT 3D-gedruckt!)
Muss **Edelstahl gedreht** werden bei lokaler Dreherei. Kosten: ~30–50 CHF.

Zeichnung zu bestellen:
```
- Außendurchmesser: Ø 12 mm
- Länge: 120 mm
- Exzentrizität: 3 mm
- Lagerbohrungen: Ø 6 mm an beiden Enden (6001-Lager)
- Oberflächengüte: Ra 0.8 µm (poliert)
- Ausbalancierung: Statisch (wichtig!)
```

### Gleitschuh-Halter (4× 3D-gedruckt, PETG)
```
Funktion:   Führt Schubstange linear auf Nockenwelle
Material:   PETG, 50% Infill
Maße:       12 × 8 × 15 mm
Lagerfläche: Teflon-beschichtet oder selbstschmierend
Montage:    An Schubstangen-Halter mit M3-Schraube fixiert
```

### Schubstangen-Halter (4× 3D-gedruckt, PETG+TPU)
```
Funktion:   Verbindet Gleitschuh → Gelenk-Flansch
Material:   Basis PETG (oben), TPU-Puffer (unten)
Länge:      ~25 mm Nutzlänge
Achsbohrung: Ø 6 mm (für M6 Stift)
Flexibilität: 1–2 mm seitwärts (Vibration-Dämpfung)
```

### Motorhalter-Flansch (1× 3D-gedruckt, PETG)
```
Funktion:   Montiert BL-Motor zentral an Gehäuse
Material:   PETG, 60% Infill (hohe Steifigkeit)
Befestigung: 4× M3 zum Rumpf, 4× M2 zum Motor
Axialspiel: ≤ 0.5 mm (wichtig für Nocken-Ausrichtung)
```

---

## Frequenz-Steuerung

### Mapping RPM → Schwimmfrequenz

```
PWM Duty Cycle [%] → ESC → Motor RPM → Nockenwelle RPM → f_swim [Hz]

PWM        ESC     Motor   Nocken-RPM  Freq.   Geschw. Est.
────────────────────────────────────────────────────────
  10%  →  1000V  →  900 RPM   →  22.5   0.38 Hz   0.08 m/s
  25%  →  2775V  →  2500 RPM  →  62.5   1.04 Hz   0.22 m/s
  50%  →  5550V  →  5000 RPM  →  125    2.08 Hz   0.44 m/s  ← Standard
  75%  →  8325V  →  7500 RPM  →  187.5  3.13 Hz   0.66 m/s
 100%  →  11.1V  →  10000 RPM →  250    4.17 Hz   0.88 m/s  ← Max (zu schnell)

Anmerkung: RPM ÷ 60 ÷ Getriebe(40) = Nockenwellen-Hz
           Nockenwellen-Umdrehung pro Sekunde = Schwimmzyklus-Frequenz
```

### Drehzahl-Feedback (optional, für konstante Freq.)

Magnetischer Encoder auf Nockenwellen-Achse:
- AS5600 12-bit Rotations-Encoder
- I²C interface zu ESP32
- Ermöglicht konstante f bei variabler Last (Wasser-Widerstand)

---

## Montage-Reihenfolge

1. **Nockenwelle vorbereiten**
   - Beide Lagerbuchsen in Halter-Flansch einpressen (6001-2RS)
   - Ausbalancierung prüfen (auf Ausgleichsbank testen)

2. **Motor montieren**
   - BL-Motor auf Flansch mit 4× M2 befestigen
   - Ausrichtung kontrollieren: Welle konzentrisch zur Nockenwelle

3. **Getriebe/Zahnrad**
   - Wenn intern im Motor: fertig
   - Wenn extern: Schneckengetriebe 4:1 auf Motorwelle
   - Ausrichtung justieren, TL-Gemisch (leichte Schmierung)

4. **Gleitschuh + Schubstangen**
   - 4 Gleitschuh-Paare auf Nocke schieben (90° Versatz)
   - Schubstangen an Gleitschuhe anschrauben
   - Bewegungsfreiheit testen (kein Klemmen)

5. **Gelenk-Flansche verbinden**
   - Schubstangen an Gelenk-Flansche der 4 Körpersegmente anschließen
   - M6-Bolzen mit Unterlegscheibe + Federscheibe + Mutter
   - Spielfreiheit: ±0.1 mm Axialspiel zulässig

6. **Test im Trockenen**
   - Motor langsam mit PWM-Signal anfahren (10% DC)
   - Bewegung sollte glatt sein, keine Interferenzen
   - Alle 4 Gelenke phasenverschoben schwingen?

---

## Sicherheit & Wartung

⚠️ **Wichtig:**
- Nockenwelle ist **Hochgeschwindigkeits-Komponente** — vollständig abdecken
- Gelenk-Bewegung kann bei Vollgas Finger einklemmen → Sicherheitsschalter
- Motor-Drehrichtung: Gegen den Uhrzeiger = Vorwärts (kalibrieren!)
- Schmierung: TL-Gemisch auf Gleitschuh-Nockenwelle, alle 2 Betriebsstunden

---

## Ersatzteile & Kosten

| Komponente | Material | Kosten |
|---|---|---|
| BL Outrunner Motor 20W | Fertig | 15–20 CHF |
| ESC 20A + BEC | Fertig | 12–18 CHF |
| Planetengetriebe 10:1 | Fertig | 20–25 CHF |
| Schneckenrad 4:1 | Fertig/Gedreht | 15–20 CHF |
| Nockenwelle Edelstahl (gedreht) | Bestellung Dreherei | 30–50 CHF |
| 3D-Druck-Teile | PETG/TPU | 20–30 CHF |
| Kugellager + Kleinteile | — | 15 CHF |
| **Total Antrieb** | — | **~150 CHF** |

