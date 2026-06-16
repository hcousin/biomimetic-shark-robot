# Biomimetic Haifisch — Single Brushless Motor + Variable Hebelarm-Design

## Konzept-Übersicht

```
Brushless Outrunner Motor (KV=900, 20 A ESC)
        ↓
Planetarisches Getriebe 1:10 (RPM reduziert)
        ↓
Exzentrische Nockenwelle (Ø 12 mm Achse, Standard e=3 mm)
        ↓
4 × Zug-Stoß-Stangen (Cam Follower)
        ↓
4 × Schwanzgelenke mit VARIABLEN HEBELARMEN (J1, J2, J3, J4)
        ↓
Biologisch authentische Haifisch-Körperwelle
(Amplituden nehmen zum Schwanz hin zu!)
```

**Physikalisches Prinzip:**
- Motor rotiert kontinuierlich mit variabler RPM
- Standard-exzentrische Nocke erzeugt überall gleichen linearen Hub (±6 mm)
- 4 unterschiedlich dimensionierte Gelenk-Flansche wandeln diesen Hub in **progressive Winkel** um
- 4 Gleitschuh-Positionen (0°, 90°, 180°, 270°) → automatische Phasenversätze
- Keine digitale CPG nötig — rein mechanisch! ✓

---

## Exzentrische Nockenwelle: Design

### Geometrie (Standard, einfach zu drehen!)

```
Nocken-Profil (axialer Querschnitt):
  
  Radius-Variation:  R(θ) = R₀ + e·cos(θ)
  
  Wobei:
    R₀ = 8 mm    (Mittlerer Radius)
    e  = 3 mm    (Exzentrizität — STANDARD!)
    θ  = Winkel auf Nocke (0–360°)
    
  → Max-Radius = 11 mm (bei θ=0°)
  → Min-Radius = 5 mm  (bei θ=180°)
  → Hub pro Schubstange = 2·e = 6 mm linear (ÜBERALL GLEICH!)
```

### Linearer Hub → Gelenkwinkel via Hebelarm

Die Innovation: **Unterschiedliche Hebellängen an jedem Gelenk** verwandeln den gleichen linearen Hub in progressive Winkelausschläge:

```
Alle Gelenke bekommen:  h_linear = ±6 mm (von Standard-Nocke)

Aber unterschiedliche Hebellängen:

θ_gelenk = atan(h_linear / L_hebel)

J1 (Kopf-nah):       L₁ = 30 mm  →  θ₁ ≈ ±11.3°  (klein)
J2 (Mitte-vorne):    L₂ = 25 mm  →  θ₂ ≈ ±13.5°  
J3 (Mitte-hinten):   L₃ = 18 mm  →  θ₃ ≈ ±18.4°  
J4 (Schwanz):        L₄ = 12 mm  →  θ₄ ≈ ±26.6°  (maximal!)

Resultat: Körperwelle breitet sich mit zunehmender Amplitude aus!
```

### Material & Fertigung

| Komponente | Material | Abmessungen | Notizen |
|---|---|---|---|
| **Nockenwelle** | Edelstahl 1.4104 | Ø 12 mm × 120 mm | **Standard-Exzentrizität e=3 mm** — billiger! |
| Nocken-Gewicht | 150–200 g | — | Ausbalancierung wichtig! |
| Gleitschuh (×4) | Nylon/Teflon | 12×8 mm Fläche | Low-friction bearing |
| Zug-Stoß-Stangen (×4) | Aluminium 7075 | Ø 6 mm × variable Länge | Leicht, steif |
| Achsen-Lager | Ø 12 mm Kugellager | — | 6001-2RS (wasserdicht) |

---

## Phasenversätze — Automatische Wellenerzeugung

```
Gleitschuh-Positionen auf Nockenwelle (Aufsicht):

        0°
         │
     4   │    1
      \  │   /
       \ │ /
   180° ─X─ 0°  ← Nockenwelle-Achse
       / │ \
      /  │   \
     3   │    2
         │
        180°

Alle Gelenke bekommen GLEICHEN LINEAREN HUB (±6 mm):

J1 (Position 0°):    θ₁(t) = 11.3° · sin(2πf·t + 0°)
J2 (Position 90°):   θ₂(t) = 13.5° · sin(2πf·t − π/2)  ← 90° Phasenverzug
J3 (Position 180°):  θ₃(t) = 18.4° · sin(2πf·t − π)    ← 180° Phasenverzug
J4 (Position 270°):  θ₄(t) = 26.6° · sin(2πf·t − 3π/2) ← 270° Phasenverzug

RESULTAT: Kontinuierliche, rückwärts laufende Körperwelle
          mit biologisch authentischer Progressive (Kopf → Schwanz)
          wie bei echtem Hai! ✓
```

---

## Brushless Motor & ESC

### Motorauswahl
```
Typ:           Outrunner Brushless (KV = 900)
Leistung:      20–30 W nominal
Lagerung:      Kugellager (wasserdicht)
Rotor-Größe:   Ø 35 mm × 25 mm
Gewicht:       ~60 g
Größe:         60 × 40 × 20 mm
Spannung:      3S LiPo 11.1 V nominal
Strom:         2.5–3.5 A nominal (5 A Peak bei Anfahrt)

Drehzahl-Bereich:
  KV = 900  →  U[V] × KV = RPM
  11.1 V × 900 = 9990 RPM (Vollgas)
  
Getriebe 1:40  →  9990 / 40 ≈ 250 RPM Nockenwelle
              ÷ 60 ≈ 4.2 Hz Nockenwellen-Drehzahl maximal
              → Aber: PWM-Steuerung reduziert dies auf sinnvolle Werte!
```

### RPM-Steuerung via PWM

Für natürliche Schwimmfrequenzen (0.5–2.0 Hz) nutzen wir **PWM-Steuerung**:

```
PWM Duty Cycle [%] → ESC → Motor RPM → Nockenwelle RPM → f_swim [Hz]

PWM        ESC     Motor     Nocken-RPM  Freq.   Geschw. Est.
────────────────────────────────────────────────────────
  10 %  →  1000 V  →   900 RPM →  22.5   0.38 Hz   0.08 m/s
  25 %  →  2775 V  →  2500 RPM →  62.5   1.04 Hz   0.22 m/s
  50 %  →  5550 V  →  5000 RPM →  125    2.08 Hz   0.44 m/s  ← Standard
  75 %  →  8325 V  →  7500 RPM →  187.5  3.13 Hz   0.66 m/s
 100 %  →  11.1 V  → 10000 RPM →  250    4.17 Hz   0.88 m/s

Anmerkung: RPM ÷ 60 ÷ Getriebe (40) = Nockenwellen-Hz
           Nockenwellen-Umdrehung pro Sekunde = Schwimmzyklus-Frequenz
```

### ESC-Spezifikation

```
Typ:            Brushless ESC (20 A kontinuierlich)
Frequenz:       8 kHz PWM
Spannung:       3S LiPo (11.1 V) + 1S Safe
Programmierbar: Throttle-Kurve, Bremsart
Gehäuse:        Aluminiumgehäuse mit Kühlrippen
Wasserdichtheit: Potting vollständig oder teilweise (prüfen!)
Verkabelung:    2 mm Goldstecker (Motor) + JST-SM (BEC out)

Empfehlung: Hobbywing Platinum 20 A oder ähnlich
```

---

## Elektronik-Layout (Vereinfacht)

```
LiPo 3S 11.1 V
    │
    ├─→ [BEC 5 V/3 A] ──→ ESP32 VIN + PCA9685
    │
    ├─→ [ESC 20 A] ←──── PWM-Signal (ESP32 Pin 25)
         │
         └─→ Brushless Motor (3 Phasen)
              │
              └─→ Planetengetriebe 10:1
                   │
                   └─→ Externe Schnecke 4:1
                        │
                        └─→ Standard Exzentrische Nockenwelle
                             │
                             ├─→ Gleitschuh 1 → Zug-Stoß-Stange → Gelenk-Flansch J1 (L₁=30mm)
                             ├─→ Gleitschuh 2 → Zug-Stoß-Stange → Gelenk-Flansch J2 (L₂=25mm)
                             ├─→ Gleitschuh 3 → Zug-Stoß-Stange → Gelenk-Flansch J3 (L₃=18mm)
                             └─→ Gleitschuh 4 → Zug-Stoß-Stange → Gelenk-Flansch J4 (L₄=12mm)
                              
Servo-Kanäle frei:
  PCA9685 CH0 → Brustflosse links (unverändert)
  PCA9685 CH1 → Brustflosse rechts
  PCA9685 CH2 → Ballast-Kolben
  (Rest frei für Sensoren, Lichter etc.)
```

---

## Gelenk-Längsschnitt (Variable Hebel-Längen)

```
                    Nockenwelle
                    (rotierend)
               ┌────────•────────┐
               │                 │
          Gleitschuh         Rückenlager
          (Nylon)            (6001-2RS)
           ╔════╗
           ║ ● ║ ← Hub linear ±6 mm (GLEICH für alle!)
           ╚════╝
             │
        Zug-Stoß-Stange
        (Al, Ø 6 mm)
             │
        ╭────┴────╮
        │ VARIABLE │
        │ HEBEL-LÄ │  ← UNTERSCHIEDLICH!
        │  NGE L₁  │     J1: 30 mm, J2: 25 mm
        │ bis L₄   │     J3: 18 mm, J4: 12 mm
        ╭─────────╮
        │         │
    Gelenk-Flansch L    Gelenk-Flansch R
    (Verbindung zu       (zum nächsten
     Körper-Segment)     Segment)
        ╱───╲              ╱───╲
       /     \            /     \
   Body A   Link 1    Link 1   Link 2
   Ø8 mm    Ø8 mm     Ø8 mm    Ø8 mm
   Achsen aus Edelstahl
```

---

## CAD-Teile für 3D-Druck

### Exzentrische Nockenwelle (NICHT 3D-gedruckt!)
Muss **aus Edelstahl gedreht** werden bei einer lokalen Dreherei. 
**Kosten: ~30–40 CHF** (günstiger, weil STANDARD-Exzentrizität!)

Zeichnung zu bestellen:
```
- Außendurchmesser: Ø 12 mm
- Länge: 120 mm
- Exzentrizität: 3 mm (STANDARD)
- Lagerbohrungen: Ø 6 mm an beiden Enden (6001-Lager)
- Oberflächengüte: Ra 0.8 µm (poliert)
- Ausbalancierung: statisch (wichtig!)
```

### Gleitschuh-Halter (4× 3D-gedruckt, PETG)
```
Funktion:    Führt Schubstange linear auf Nockenwelle
Material:    PETG, 50 % Infill
Maße:        12 × 8 × 15 mm
Lagerfläche: Teflon-beschichtet oder selbstschmierend
Montage:     An Zug-Stoß-Stangen-Halter mit M3-Schraube fixiert
```

### Zug-Stoß-Stangen-Halter (4× 3D-gedruckt, PETG+TPU)
```
Funktion:    Verbindet Gleitschuh → variable Gelenk-Flansche
Material:    Basis PETG (oben), TPU-Puffer (unten)
Länge:       ~25–30 mm Nutzlänge (mit Spielraum für Montage)
Achsbohrung: Ø 6 mm (für M6-Stift)
Flexibilität: 1–2 mm seitwärts (Vibrationsdämpfung)
```

### Gelenk-Flansche mit VARIABLEN HEBELARMEN (4× 3D-gedruckt, PETG)

```
KRITISCH: Jeder Flansch hat eine unterschiedliche Hebel-Länge!

Flansch J1 (Kopf-nah):
  - Schubstangen-Anschluss: Hebel-Länge L₁ = 30 mm
  - Material: PETG, 50 % Infill
  - Amplitude: ±11.3° (klein)
  - Montage: An Körper-Segment 1

Flansch J2 (Mitte-vorne):
  - Schubstangen-Anschluss: Hebel-Länge L₂ = 25 mm
  - Material: PETG, 50 % Infill
  - Amplitude: ±13.5°
  - Montage: An Körper-Segment 2

Flansch J3 (Mitte-hinten):
  - Schubstangen-Anschluss: Hebel-Länge L₃ = 18 mm
  - Material: PETG, 50 % Infill
  - Amplitude: ±18.4°
  - Montage: An Körper-Segment 3

Flansch J4 (Schwanz):
  - Schubstangen-Anschluss: Hebel-Länge L₄ = 12 mm
  - Material: PETG, 60 % Infill (höhere Steifigkeit für größere Kräfte!)
  - Amplitude: ±26.6° (maximal!)
  - Montage: An Schwanz-Segment
```

### Motorhalter-Flansch (1× 3D-gedruckt, PETG)
```
Funktion:    Montiert BL-Motor zentral an Gehäuse
Material:    PETG, 60 % Infill (hohe Steifigkeit)
Befestigung: 4× M3 zum Rumpf, 4× M2 zum Motor
Axialspiel:  ≤ 0.5 mm (wichtig für Nocken-Ausrichtung)
```

---

## Frequenzsteuerung

### Mapping RPM → Schwimmfrequenz

```
PWM Duty Cycle [%] → ESC → Motor RPM → Nockenwelle RPM → f_swim [Hz]

PWM        ESC     Motor     Nocken-RPM  Freq.   Geschw. Est.
────────────────────────────────────────────────────────
  10 %  →  1000 V  →   900 RPM →  22.5   0.38 Hz   0.08 m/s
  25 %  →  2775 V  →  2500 RPM →  62.5   1.04 Hz   0.22 m/s
  50 %  →  5550 V  →  5000 RPM →  125    2.08 Hz   0.44 m/s  ← Standard
  75 %  →  8325 V  →  7500 RPM →  187.5  3.13 Hz   0.66 m/s
 100 %  →  11.1 V  → 10000 RPM →  250    4.17 Hz   0.88 m/s  ← Max

Anmerkung: RPM ÷ 60 ÷ Getriebe (40) = Nockenwellen-Hz
           Nockenwellen-Umdrehung pro Sekunde = Schwimmzyklus-Frequenz
```

### Drehzahl-Feedback (optional, für konstante Frequenz)

Magnetischer Encoder auf Nockenwellen-Achse:
- AS5600 12-bit Rotations-Encoder
- I²C-Schnittstelle zu ESP32
- Ermöglicht konstante Frequenz bei variabler Last (Wasserwiderstand)

---

## Montagereihenfolge

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

4. **Gleitschuh + Zug-Stoß-Stangen**
   - 4 Gleitschuh-Paare auf Nocke schieben (90° Versatz)
   - Zug-Stoß-Stangen an Gleitschuhe anschrauben
   - Bewegungsfreiheit testen (kein Klemmen)

5. **Variable Gelenk-Flansche verbinden**
   - Zug-Stoß-Stangen an **unterschiedlich langen** Gelenk-Flanschen anbringen:
     - J1 (L=30 mm) → Körper-Segment 1
     - J2 (L=25 mm) → Körper-Segment 2
     - J3 (L=18 mm) → Körper-Segment 3
     - J4 (L=12 mm) → Schwanz-Segment
   - M6-Bolzen mit Unterlegscheibe + Federscheibe + Mutter
   - Spielfreiheit: ±0.1 mm Axialspiel zulässig

6. **Test im Trockenen**
   - Motor langsam mit PWM-Signal anfahren (10 % DC)
   - Bewegung sollte glatt sein, keine Interferenzen
   - Schwingen alle 4 Gelenke phasenverschoben?
   - **Amplituden prüfen:** Schwanz sollte deutlich größer ausschlagen als Kopf! ✓

---

## Sicherheit & Wartung

⚠️ **Wichtig:**
- Nockenwelle ist **Hochgeschwindigkeitskomponente** — vollständig abdecken
- Gelenk-Bewegung kann bei Vollgas Finger einklemmen → Sicherheitsschalter
- Motordrehrichtung: Gegen den Uhrzeigersinn = Vorwärts (kalibrieren!)
- Schmierung: TL-Gemisch auf Gleitschuh-Nockenwelle, alle 2 Betriebsstunden

---

## Ersatzteile & Kosten

| Komponente | Material | Kosten |
|---|---|---|
| BL Outrunner Motor 20 W | Fertig | 15–20 CHF |
| ESC 20 A + BEC | Fertig | 12–18 CHF |
| Planetengetriebe 10:1 | Fertig | 20–25 CHF |
| Schneckenrad 4:1 | Fertig/Gedreht | 15–20 CHF |
| **Nockenwelle Edelstahl (Standard)** | Bestellung Dreherei | **30–40 CHF** |
| **Variable 3D-Druck-Gelenk-Flansche** | PETG | **25–35 CHF** |
| Kugellager + Kleinteile | — | 15 CHF |
| **Total Antrieb** | — | **~140–160 CHF** |

---

## Vorteile des Variable Hebelarm-Designs

✅ **Standard-Nockenwelle** — billiger zu drehen, einfacher zu bestellen  
✅ **Progressive Amplituden** — biologisch authentisch wie echter Hai  
✅ **Flexibel nachzujustieren** — nur Flansche wechseln bei Bedarf  
✅ **Einfacher zu montieren** — keine komplexe exzentrische Geometrie nötig  
✅ **Schnellerer Prototyp-Durchlauf** — Standard-Teile, weniger Fehlerrisiko