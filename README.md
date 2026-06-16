# Biomimetic Shark Robot — Single Brushless Motor Edition

**Naturgetreuer Haifisch-Roboter mit exzentrischer Nockenwelle und kontinuierlicher Körperwelle**

---

## 📋 Projektübersicht

Ein biomimetischer Unterwasser-Roboter in Haiform (60–70 cm Länge), der mit **nur 1 Brushless-Motor** eine natürliche Schwimmbewegung erzeugt. Die exzentrische Nockenwelle treibt mechanisch 4 Gelenke mit automatischen Phasenversätzen an — keine komplexe CPG-Software nötig!

**Kernfeatures:**
- ✅ Kontinuierliche Körperwelle (wie echter Hai)
- ✅ 1× Brushless Motor KV=900 (effizient, wasserdicht)
- ✅ Mechanische Phasenversätze (Nocken-Geometrie)
- ✅ 4 Körper-Gelenke (J1–J4) mit ±6.9° Amplitude
- ✅ Tiefenregelung (PID + Ballast)
- ✅ IMU-Feedback (Brustflossen-Pitch)
- ✅ WiFi + Serial-Steuerung

---

## 📁 Dateistruktur

```
biomimetic-shark-robot/
├── README.md                              ← Du bist hier
├── firmware/
│   ├── shark_single_motor_firmware.ino   ← ESP32 Hauptcode
│   └── nocke_kinematik.py                ← Python-Kinematik-Simulator
├── mechanics/
│   └── single_motor_mechanics.md         ← Komplette Mechanik-Dokumentation
├── hardware/
│   ├── nocke_kinematics_specs.txt        ← Nockenwelle-Spezifikation
│   └── bom_single_motor.csv              ← Stückliste
├── cad/
│   └── 3d_print_parts.md                 ← STL-Teile-Beschreibung
├── docs/
│   ├── strouhal_optimization.py          ← Hydrodynamik-Optimierer
│   ├── silicone_molding_guide.md         ← Silikonabguss-Anleitung
│   └── 3d_print_structure.md             ← 3D-Druck-Parameter
└── LICENSE                               ← MIT License

```

---

## 🚀 Schnelleinstieg

### Hardware-Voraussetzungen
- ESP32 DevKit v1
- Brushless Outrunner Motor (KV=900)
- ESC 20 A mit PWM-Input
- Nockenwelle (Edelstahl gedreht, Ø12×120 mm, e=3 mm)
- 3D-Drucker (PETG/TPU)
- Wasserdichte Sensoren (MS5837, MPU6050)
- LiPo 3S Akku

### Firmware flashen
```bash
# Arduino IDE oder PlatformIO
# Board: ESP32 DevKit v1
# COM Port: /dev/ttyUSB0 (oder dein Port)
cd firmware/
# Datei: shark_single_motor_firmware.ino
# Upload!
```

### Kinematik testen
```bash
python3 firmware/nocke_kinematik.py
```
Zeigt Gelenk-Winkel über einen Schwimmzyklus.

---

## 🔧 Mechanik-Highlights

**Exzentrische Nockenwelle:**
- R₀ = 8 mm (mittlerer Radius)
- e = 3 mm (Exzentrizität)
- Hub: ±3 mm linear → ±6.9° Gelenk
- 4 Gleitschuh-Positionen @ 0°, 90°, 180°, 270°

**Automatische Phasenversätze:**
```
J1 @ 0°:   θ₁(t) = 6.9° · sin(2πf·t + 0°)
J2 @ 90°:  θ₂(t) = 6.9° · sin(2πf·t − π/2)
J3 @ 180°: θ₃(t) = 6.9° · sin(2πf·t − π)
J4 @ 270°: θ₄(t) = 6.9° · sin(2πf·t − 3π/2)
```
→ Kontinuierliche Körperwelle entsteht automatisch!

**Motor-Steuerung:**
- PWM Duty Cycle 0–100 %
- Getriebe 40:1 (10:1 intern + 4:1 extern)
- Nocken-RPM = Motor-RPM / 40
- Schwimmfrequenz = Nocken-RPM / 60

---

## 📊 Performance-Daten

| Frequenz | Motor RPM | Geschwindigkeit | Periode |
|---|---|---|---|
| 0.5 Hz | ~1800 RPM | ~0.18 m/s | 2.0 s |
| 1.0 Hz | ~3600 RPM | ~0.35 m/s | 1.0 s |
| 1.5 Hz | ~5400 RPM | ~0.53 m/s | 0.67 s |
| 2.0 Hz | ~7200 RPM | ~0.70 m/s | 0.5 s |

---

## 🛠️ Montage-Reihenfolge

1. **Nockenwelle vorbereiten** (Dreherei)
   - Edelstahl, Ø12×120 mm, e=3 mm
   - Beide Enden Lager-Bohrungen (Ø6 mm für 6001-Lager)
   
2. **Motor montieren**
   - BL Outrunner auf Flansch-Halter
   - Mit 4× M2-Schrauben fixieren
   
3. **Getriebe-Assembly**
   - Planetengetriebe 10:1 (im Motor oder extern)
   - Schneckengetriebe 4:1 auf Motorwelle
   
4. **Gleitschuhe + Schubstangen**
   - 4 Gleitschuh-Paare auf Nocke (90° Versatz)
   - Schubstangen (25 mm Aluminium) anschrauben
   
5. **Gelenk-Flansche verbinden**
   - An 4 Körper-Segmente anschließen
   - Test im Trockenen (keine Interferenzen?)
   
6. **Elektronik + Sensorik**
   - ESP32 + MS5837 + MPU6050 + ESC
   - Wasserdicht abdichten (O-Ring + Epoxy)
   
7. **Ballast-System**
   - 20 ml Spritze mit M5-Kolben
   - Servo-gesteuert für Tiefenregelung

---

## 📡 Steuerung

### WiFi UDP (JSON-ähnlich)
```
"THROTTLE 0.5"      → 50 % Motor-Drehzahl
"DEPTH 1.0"         → Zieltiefe 1.0 m
"SURFACE"           → Auftauchen
"STOP"              → Notfall-Stopp
```

### Serial (115200 Baud)
```
throttle 0.5        → Drehzahl setzen
depth 1.5           → Tauchen
status              → Telemetrie anzeigen
```

---

## 💰 Kosten-Übersicht

| Komponente | Kosten |
|---|---|
| Brushless Motor | 15–20 CHF |
| ESC 20 A | 12–18 CHF |
| Getriebe (2× Set) | 35–45 CHF |
| **Nockenwelle (gedreht)** | **30–50 CHF** |
| 3D-Druck (PETG/TPU) | 20–30 CHF |
| Sensoren + Elektronik | ~100 CHF |
| Akku, Dichtung, Kleinteile | ~30 CHF |
| **TOTAL** | **~280–350 CHF** |

---

## 📚 Dokumentation

- **`single_motor_mechanics.md`** — Komplette mechanische Spezifikation
- **`nocke_kinematik.py`** — Kinematik-Simulator + Visualisierung
- **`shark_single_motor_firmware.ino`** — Produktionsreifer ESP32-Code
- **`strouhal_optimizer.py`** — Hydrodynamik-Optimierer
- **`silicone_molding_guide.md`** — Silikonabguss-Anleitung
- **`3d_print_structure.md`** — 3D-Druck-Parameter & STL-Liste

---

## 🔬 Technische Grundlagen

**BCF Carangiform Schwimmen:**
Die kontinuierliche Körperwelle breitet sich vom Kopf zur Schwanzspitze aus.
Mit 4 Gelenken bei 90° Phasenverlauf erreichen wir biologisch optimale Bewegungen.

**Strouhal-Optimierung:**
St = f·A/U ≈ 0.25–0.35 (optimal für echte Haie)
Siehe `strouhal_optimizer.py` für Parameterberechnung.

**Nockenwellen-Kinematik:**
Die exzentrische Geometrie wandelt Rotationsbewegung in sinusoidale
Gelenk-Schwingungen um — rein mechanisch, keine digitale Steuerung nötig!

---

## ⚠️ Wichtige Sicherheitshinweise

- ⚠️ **Nockenwelle rotiert mit hoher Geschwindigkeit** — vollständig abdecken!
- ⚠️ **Gelenk-Bewegungen können Finger einklemmen** — Sicherheitsschalter!
- ⚠️ **Wasserdichtheit vor dem Betrieb prüfen** — Drucktest durchführen!
- ⚠️ **Akku-Laden in feuerfester Box** — LiPo-Sicherheit!

---

## 📖 Lizenz

MIT License — Frei nutzbar, Änderungen erlaubt, Nennung erforderlich.

---

## 🤝 Kontakt & Feedback

Fragen zur Mechanik? → Siehe `single_motor_mechanics.md`
Fragen zum Code? → Siehe `shark_single_motor_firmware.ino`
Hydrodynamik-Optimierung? → Siehe `strouhal_optimizer.py`

---

**Status:** ✅ Vollständig dokumentiert (Stand: Juni 2026)
**Zielgruppe:** Maker, Robotik-Enthusiasten, Biomimetic-Forscher
**Schwierigkeitsgrad:** ⭐⭐⭐ Mittel (Mechanik-Kenntnisse hilfreich)

---

**Happy Shark Building! 🦈**
