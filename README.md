# Biomimetic Shark Robot — Hybrid Passive Tail Edition

**Naturgetreuer Haifisch-Roboter mit exzentrischer Nockenwelle (J1/J2 aktiv) + passiven TPU-Federgelenken (J3/J4)**

> 🌿 **Branch:** `dev/hybrid-passive-tail` — Hybrid-Design
> 📦 **main:** 4× aktive Gelenke (älteres Design)

---

## 📋 Projektübersicht

Ein biomimetischer Unterwasser-Roboter in Haiform (60 cm Länge), der mit **nur 1 Brushless-Motor** eine natürliche Schwimmbewegung erzeugt. Die kurze exzentrische Nockenwelle (60mm) treibt J1+J2 aktiv an — J3+J4 sind passive TPU-Federgelenke, die durch Trägheit und Wasserkräfte natürlich nachschwingen. Biologisch authentischer als 4× aktive Gelenke!

**Kernfeatures:**
- ✅ Hybrid-Antrieb: J1/J2 aktiv (Nockenwelle) + J3/J4 passiv (TPU-Feder)
- ✅ 1× Brushless Motor KV=900 (effizient, wasserdicht)
- ✅ Kurze Nockenwelle 60mm (günstiger, kompakter)
- ✅ Progressive Amplituden: J1 ±5.7° → J2 ±6.9° → J3 ~±10° → J4 ~±15°
- ✅ Passive Resonanz: J3 ≈ 1.0 Hz, J4 ≈ 0.8 Hz
- ✅ Tiefenregelung (PID + Ballast)
- ✅ IMU-Feedback (Brustflossen-Pitch)
- ✅ WiFi + Serial-Steuerung
- ✅ Fusion 360 Workflow: Haifisch-Körperhülle + Verbindungsflansch

---

## 📁 Dateistruktur

```
biomimetic-shark-robot/
├── README.md                                   ← Du bist hier
├── firmware/
│   ├── shark_single_motor_firmware.ino         ← ESP32 Hauptcode
│   └── nocke_kinematik.py                      ← Hybrid-Kinematik-Simulator
├── mechanics/
│   ├── hybrid_passive_tail_mechanics.md        ← Hybrid-Design Dokumentation ★
│   └── single_motor_mechanics.md               ← Referenz (4× aktiv, älter)
├── hardware/
│   └── bom_complete.csv                        ← Stückliste (Hybrid-Design)
├── cad/
│   ├── body_to_j1_flange.scad                  ← Verbindung Körper → J1 ★
│   ├── tail_link_parametric.scad               ← Gelenk-Flansche J1/J2 ★
│   ├── tpu_joint_j3.scad                       ← Passiver Federblock J3 ★
│   ├── tpu_joint_j4.scad                       ← Passiver Federblock J4 ★
│   ├── tail_link_j1.scad                       ← J1 OpenSCAD (Referenz)
│   ├── body_front.scad                         ← Hauptgehäuse
│   ├── silikon_form_flosse.scad                ← Silikonform Schwanzflosse
│   └── stl/                                    ← Exportierte STL-Dateien
├── docs/
│   ├── 3d_print_structure.md                   ← 3D-Druck Parameter (Hybrid)
│   ├── rf_underwater/rf_physics.md             ← RF-Physik Unterwasser
│   ├── silicone_molding_guide.md               ← Silikonabguss-Anleitung
│   └── strouhal_optimizer.py                   ← Hydrodynamik-Optimierer
├── schematics/
│   └── schaltplan_v2.svg                       ← Schaltplan ESP32
└── LICENSE
```

---

## 🚀 Schnelleinstieg

### Hardware-Voraussetzungen
- ESP32 DevKit v1
- Brushless Outrunner Motor (KV=900) + ESC 20A
- Nockenwelle Edelstahl Ø12×**60mm**, e=3mm (Dreherei ~20 CHF)
- 2× Gelenk-Flansche J1/J2 (PETG, aus `tail_link_parametric.scad`)
- 2× TPU-Federblöcke J3/J4 (TPU 95A + 85A, aus `tpu_joint_j3/j4.scad`)
- Verbindungsflansch Körper→J1 (`body_to_j1_flange.scad`)
- Wasserdichte Sensoren (MS5837, MPU6050)
- LiPo 3S Akku

### Firmware flashen
```bash
# Arduino IDE, Board: ESP32 DevKit v1
# Datei: firmware/shark_single_motor_firmware.ino
```

### Kinematik simulieren
```bash
python3 firmware/nocke_kinematik.py
# Zeigt aktive J1/J2 + passive J3/J4 Simulation über mehrere Zyklen
```

### OpenSCAD → STL (für Fusion 360)
```bash
# 1. OpenSCAD installieren: openscad.org
# 2. Datei öffnen, F6 (Render), dann Export as STL
# 3. In Fusion 360: Insert → Insert Mesh
```

---

## 🔧 Mechanik-Highlights

### Aktive Nockenwelle (J1 + J2)
```
Nockenwelle: Edelstahl Ø12×60mm, e=3mm
Gleitschuhe: 2× (0° und 90° versetzt)

J1 @ 0°:  L=30mm → arcsin(3/30) ≈ ±5.7°  (Kopf-nah)
J2 @ 90°: L=25mm → arcsin(3/25) ≈ ±6.9°  (Vordermitte)
```

### Passive TPU-Gelenke (J3 + J4)
```
J3: TPU 95A, 25% Infill → f_res ≈ 1.0 Hz → ~±10° bei Resonanz
J4: TPU 85A, 20% Infill → f_res ≈ 0.8 Hz → ~±15° bei Resonanz

Federstahl-Einlage 0.3mm empfohlen (verhindert Überdehnung)
```

### Phasenversätze (automatisch, mechanisch)
```
J1: θ₁(t) = 5.7°  · sin(2πf·t)
J2: θ₂(t) = 6.9°  · sin(2πf·t − π/2)
J3: θ₃(t) ≈ 10°   · sin(2πf·t − π)      ← passiv, resonanzverstärkt
J4: θ₄(t) ≈ 15°   · sin(2πf·t − 3π/2)   ← passiv, maximale Amplitude
```

---

## 📊 Performance-Daten

| Throttle | Motor RPM | Nocken Hz | Geschw. est. |
|---|---|---|---|
| 10% | ~1000 | 0.4 Hz | ~0.08 m/s |
| 25% | ~2500 | 1.0 Hz | ~0.22 m/s ← J3 Resonanz! |
| 20% | ~2000 | 0.8 Hz | ~0.18 m/s ← J4 Resonanz! |
| 50% | ~5000 | 2.1 Hz | ~0.44 m/s |

---

## 🛠️ Montage-Reihenfolge

1. **Kurze Nockenwelle** (60mm, Dreherei)
2. **Motor + Getriebe** (unverändert)
3. **Nur 2 Gleitschuhe** @ 0° + 90°
4. **J1 + J2 Flansche** an Zug-Stoß-Stangen
5. **TPU-Blöcke J3 + J4** einkleben (Silikonkleber, 24h)
6. **Verbindungsflansch** (`body_to_j1_flange.scad`) → Fusion 360 anpassen
7. **Elektronik** + Sensoren in Gehäuse
8. **Wassertest** bei 25% Throttle

---

## 🐟 Fusion 360 Workflow (Körperhülle)

```
1. Haifisch-Körper (OBJ) laden von Free3D / GrabCAD
2. Skalieren auf 60cm Länge
3. Schwanz bei ~60% Körperlänge abschneiden (Plane Cut)
4. Shell: 3mm Wandstärke
5. body_to_j1_flange.stl importieren (aus body_to_j1_flange.scad)
6. An Schnittstelle ausrichten → Combine → Join
7. Als STEP exportieren
```

Parameter in `body_to_j1_flange.scad` anpassen:
- `body_w` / `body_h` → Rumpf-Querschnitt an Schnittstelle (in Fusion messen)

---

## 📡 Steuerung

```
WiFi UDP:   "THROTTLE 0.25"  → 25% (J3-Resonanz!)
            "DEPTH 1.0"      → Tauchen auf 1m
            "SURFACE"        → Auftauchen
            "STOP"           → Notfall-Stopp

Serial:     throttle 0.25 | depth 1.0 | status | ?
```

---

## 💰 Kosten (Hybrid-Design)

| Kategorie | Kosten |
|---|---|
| Motor + ESC + Getriebe | ~73 CHF |
| Nockenwelle (kurz, 60mm) | ~20 CHF |
| Elektronik + Sensoren | ~74 CHF |
| 3D-Druck Material | ~66 CHF |
| Silikon + Formen | ~103 CHF |
| Dichtung + Kleinteile | ~65 CHF |
| **TOTAL** | **~458 CHF** |

---

## 📚 Dokumentation

| Datei | Inhalt |
|---|---|
| `mechanics/hybrid_passive_tail_mechanics.md` | Vollständige Mechanik-Spezifikation |
| `docs/3d_print_structure.md` | 3D-Druck Parameter + STL-Liste |
| `docs/silicone_molding_guide.md` | Silikonabguss-Anleitung |
| `firmware/nocke_kinematik.py` | Hybrid-Kinematik-Simulator |
| `docs/rf_underwater/rf_physics.md` | RF-Physik + Tether-Empfehlung |

---

## ⚠️ Sicherheitshinweise

- ⚠️ **Nockenwelle rotiert schnell** — vollständig abdecken!
- ⚠️ **TPU-Blöcke vor Wassertest** auf Klebefestigkeit prüfen
- ⚠️ **Wasserdichtheit prüfen** vor dem Eintauchen (Drucktest)
- ⚠️ **LiPo in feuerfester Box** laden

---

## 📖 Lizenz

MIT License — Frei nutzbar, Änderungen erlaubt, Nennung erforderlich.

---

**Status:** ✅ Hybrid-Design vollständig dokumentiert (Stand: Juni 2026)
**Branch:** `dev/hybrid-passive-tail` | PR #2 offen
**Schwierigkeitsgrad:** ⭐⭐☆☆☆ Einfacher als 4× aktives Design!

---

**Happy Shark Building! 🦈**


---

## 🔬 Acknowledgements & Related Work

Dieses Projekt ist eine unabhängige Reimplementierung, inspiriert durch folgende Open-Source-Arbeiten:

### OpenFish (TU Delft, 2022)
> van den Berg, S.C., Scharff, R.B.N., Rusák, Z., Wu, J. (2022).
> *OpenFish: Biomimetic Design of a Soft Robotic Fish for High Speed Locomotion.*
> HardwareX. https://doi.org/10.17605/OSF.IO/FB5VH
> **Lizenz: CC-BY-SA 4.0**

Konzeptuelle Inspiration: Kombination aus aktivem und passivem Schwanzsegment
für Thunniform-Schwimmen — in diesem Projekt neu implementiert mit
exzentrischer Nockenwelle + TPU-Federgelenken.

⚠️ **Hinweis:** Es wurden **keine Designdateien von OpenFish direkt übernommen**.
Dieses Projekt ist eine eigenständige Neuentwicklung mit anderer Hardware
(Brushless-Motor, exzentrische Nockenwelle, TPU-Gelenke, ESP32).
Die MIT-Lizenz dieses Projekts gilt daher uneingeschränkt.

### FISHR — Erweiterung von OpenFish (2025)
> *Fluid interaction study: Hydrodynamic robot (FISHR) —
> Expansion of bioinspired soft robotic fish.*
> HardwareX. https://www.hardware-x.com/article/S2468-0672(25)00052-5
> **Lizenz: CC BY 4.0**

Referenz für Validierungsmethodik (Tail-Kinematik-Vergleich, Strouhal-Optimierung).
