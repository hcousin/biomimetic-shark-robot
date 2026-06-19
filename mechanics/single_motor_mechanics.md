# Biomimetic Haifisch — Hybrid-Antrieb: Aktive Nockenwelle (J1/J2) + Passive TPU-Gelenke (J3/J4)

> **Aktuelles Design** (Branch: `dev/hybrid-passive-tail`)
> Für das ältere 4× aktive Design: siehe Git-History

---

## Konzept-Übersicht

```
Brushless Outrunner Motor (KV=900, 20A ESC)
        ↓
Planetengetriebe 10:1 + Schneckengetriebe 4:1 = 40:1 total
        ↓
Kurze exzentrische Nockenwelle (Ø12mm × 60mm, e=3mm)
        ↓
2× Gleitschuh (0° und 90° versetzt)
        ↓
2× Zug-Stoß-Stange (Aluminium Ø6mm)
        ↓
J1 (aktiv, L=30mm) ──→ J2 (aktiv, L=25mm)
                               ↓
                         J3 (TPU 95A, passiv) ──→ J4 (TPU 85A, passiv)
                         [Feder + Dämpfung]         [Feder + Dämpfung]
                               ↓
                         Schwanzflosse (Silikon)
```

**Kernprinzip:**
- J1 + J2 werden **aktiv** durch die Nockenwelle angetrieben (kontrollierte Sinusbewegung)
- J3 + J4 sind **passive TPU-Federblöcke** — sie schwingen durch Trägheit und Wasserkräfte nach
- Progressive Amplituden entstehen automatisch: J1 < J2 < J3 < J4

---

## Nockenwelle: Design

### Geometrie

```
Nockenwelle (kurz, nur J1+J2):

  Länge:          60mm  (statt 120mm beim 4× aktiven Design)
  Außendurchm.:   Ø12mm
  Exzentrizität:  e = 3mm
  Gleitschuhe:    2× (bei 0° und 90°)

  Radius-Variation: R(θ) = R₀ + e·cos(θ)
    R₀ = 8mm (mittlerer Radius)
    e  = 3mm (Exzentrizität)
    → Max: 11mm, Min: 5mm
    → Linearer Hub: ±3mm
```

### Hebelarm → Gelenkwinkel

```
Gelenk-Formel: θ = arcsin(e / L)

J1: L=30mm → arcsin(3/30) ≈ ±5.7°   (Kopf-nah, sanfte Bewegung)
J2: L=25mm → arcsin(3/25) ≈ ±6.9°   (Vordermitte)

Phasenversatz J1→J2: 90° (durch Gleitschuh-Position)
```

### Material & Fertigung

| Komponente | Material | Abmessungen | Kosten |
|---|---|---|---|
| Nockenwelle | Edelstahl 1.4104 | Ø12mm × 60mm, e=3mm | ~20 CHF (Dreherei) |
| Gleitschuh ×2 | PETG/Nylon | 12×8mm | 3D-Druck |
| Zug-Stoß-Stangen ×2 | Alu 7075 | Ø6mm × 25mm | ~3 CHF |
| Kugellager 6001-2RS ×2 | Stahl | Ø12×28×8mm | ~6 CHF |

---

## Passive TPU-Gelenke (J3 + J4)

### Feder-Dämpfer-Modell

```
Jedes passive Gelenk verhält sich wie ein gedämpfter Schwinger:

  m·θ̈ + d·θ̇ + k·(θ - θ_input) = 0

  m = Trägheitsmoment Schwanzsegment
  d = Dämpfung (TPU-Material + Wasser)
  k = Federsteifigkeit (TPU-Infill + Shore)

Resonanzfrequenz: f_res = (1/2π) · √(k/m)
  J3 (TPU 95A, 25% Infill): f_res ≈ 1.0 Hz
  J4 (TPU 85A, 20% Infill): f_res ≈ 0.8 Hz
```

### Erwartete Amplituden im Betrieb

| Frequenz | J1 (aktiv) | J2 (aktiv) | J3 (passiv) | J4 (passiv) |
|---|---|---|---|---|
| 0.4 Hz | ±5.7° | ±6.9° | ~±4° | ~±6° |
| 0.8 Hz | ±5.7° | ±6.9° | ~±8° | **~±15°** ← J4 Resonanz! |
| 1.0 Hz | ±5.7° | ±6.9° | **~±10°** ← J3 Resonanz! | ~±12° |
| 1.5 Hz | ±5.7° | ±6.9° | ~±7° | ~±9° |

### TPU-Spezifikationen

```
J3 (tpu_joint_j3.scad):
  Material:   TPU 95A
  Maße:       20 × 15 × 10mm
  Infill:     25% Gyroid
  Federstahl: 0.3mm × 8mm Einlage bei Z=5mm

J4 (tpu_joint_j4.scad):
  Material:   TPU 85A  ← weicher!
  Maße:       15 × 12 × 8mm
  Infill:     20% Gyroid
  Federstahl: 0.3mm × 6mm Einlage, 3mm nach hinten versetzt
              → gibt Schwanzflosse natürlichen Anstellwinkel
```

---

## Brushless Motor & ESC

### Motorauswahl (unverändert)

```
Typ:        Outrunner Brushless KV=900
Leistung:   20–30W nominal
Spannung:   3S LiPo 11.1V
Strom:      2.5–3.5A nominal

Getriebe:   Planetengetriebe 10:1 + Schneckengetriebe 4:1 = 40:1 total
```

### RPM → Schwimmfrequenz

```
Nockenwellen-RPM = Motor-RPM / 40
Schwimmfrequenz  = Nockenwellen-RPM / 60

Throttle  Motor-RPM  Nocke-RPM  Frequenz  Empfehlung
  10%      ~1000       ~25       0.4 Hz    Langsam
  20%      ~2000       ~50       0.8 Hz    ← J4 Resonanz!
  25%      ~2500       ~62       1.0 Hz    ← J3 Resonanz! (Standard)
  50%      ~5000      ~125       2.1 Hz    Schnell
```

---

## Elektronik-Layout

```
LiPo 3S 11.1V
    │
    ├─→ [BEC 5V/3A] ──→ ESP32 + PCA9685 + Servos
    │
    └─→ [ESC 20A] ←──── PWM Pin 25 (ESP32)
         │
         └─→ Brushless Motor
              └─→ Getriebe 40:1
                   └─→ Nockenwelle (60mm)
                        ├─→ Gleitschuh J1 @ 0°  → Zug-Stoß-Stange → J1 (L=30mm)
                        └─→ Gleitschuh J2 @ 90° → Zug-Stoß-Stange → J2 (L=25mm)
                                                          ↓
                                                   TPU-Block J3 (95A)
                                                          ↓
                                                   TPU-Block J4 (85A)
                                                          ↓
                                                   Schwanzflosse (Silikon)

Freie Servo-Kanäle (PCA9685):
  CH0 → Brustflosse links
  CH1 → Brustflosse rechts
  CH2 → Ballast-Kolben
```

---

## Vergleich: 4× Aktiv vs. Hybrid

| Merkmal | 4× Aktiv (main) | Hybrid (dieser Branch) |
|---|---|---|
| Nockenwelle | 120mm, 35 CHF | **60mm, 20 CHF** |
| Gleitschuhe | 4× | **2×** |
| Zug-Stoß-Stangen | 4× | **2×** |
| Gelenk-Flansche (PETG) | 4× | **2×** |
| Passive Gelenke (TPU) | — | **2×** |
| Montage-Komplexität | ★★★★☆ | **★★☆☆☆** |
| Bio-Authentizität | ★★★★☆ | **★★★★★** |
| Kosten | 478 CHF | **458 CHF** |

---

## Montagereihenfolge

1. **Nockenwelle** (60mm) von Dreherei, 2× 6001-2RS Lager einpressen
2. **Motor + Getriebe** auf Motorhalter-Flansch montieren
3. **2× Gleitschuh** auf Nocke: J1 @ 0°, J2 @ 90°
4. **2× Zug-Stoß-Stange** an Gelenk-Flansche J1/J2 anschließen
5. **TPU-Block J3** zwischen Segment 2+3 einkleben (Silikonkleber, 24h)
6. **TPU-Block J4** zwischen Segment 3+Flosse einkleben (24h)
7. **Verbindungsflansch** (body_to_j1_flange) an Hai-Körperhülle anpassen
8. **Test trocken**: J1/J2 schwingen? J3/J4 nachgiebig + rückstellend?
9. **Wassertest**: Bei 25% Throttle (1.0 Hz) — J3 sollte in Resonanz mitschwingen

---

## Abstimmung TPU-Steifigkeit

Falls J3/J4 **zu steif** (kaum Bewegung):
- Infill reduzieren (15%)
- Shore-Wert senken (95A→85A für J3, 85A→75A für J4)
- Federstahl-Einlage weglassen

Falls J3/J4 **zu weich** (schlabbernd):
- Infill erhöhen (30%)
- Shore-Wert erhöhen
- Federstahl-Einlage dicker (0.5mm statt 0.3mm)

---

## CAD-Dateien

| Datei | Beschreibung |
|---|---|
| `cad/tail_link_parametric.scad` | Aktive Flansche J1 (L=30) + J2 (L=25) |
| `cad/tpu_joint_j3.scad` | Passiver Federblock J3 (TPU 95A) |
| `cad/tpu_joint_j4.scad` | Passiver Federblock J4 (TPU 85A) |
| `cad/body_to_j1_flange.scad` | Verbindung Hai-Körper → J1 |
| `cad/body_front.scad` | Hauptelektronikgehäuse |
| `cad/silikon_form_flosse.scad` | Negativform Schwanzflosse |

---

**Status:** 🟢 Konsistent mit Hybrid-Design
**Simulation:** `python3 firmware/nocke_kinematik.py`
