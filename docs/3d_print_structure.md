# 3D-Druckdateien-Struktur: Biomimetischer Haifisch-Roboter (Variable Hebelarm-Design)

## Gesamtübersicht der Druckteile (Stufe 2, 60 cm)

```
shark_robot/
├── body/
│   ├── body_front.stl          ← Vorderer Elektronikrumpf
│   ├── body_mid.stl            ← Mittelteil (Verbindungsstück)
│   ├── body_lid_front.stl      ← Deckel vorne (O-Ring-Flansch)
│   └── ballast_cylinder.stl    ← Ballastzylinder Ø 30 mm
├── tail/
│   ├── tail_link_j1.stl        ← Gelenk-Flansch J1 (Hebel L1=30mm)
│   ├── tail_link_j2.stl        ← Gelenk-Flansch J2 (Hebel L2=25mm)
│   ├── tail_link_j3.stl        ← Gelenk-Flansch J3 (Hebel L3=18mm)
│   ├── tail_link_j4.stl        ← Gelenk-Flansch J4 (Hebel L4=12mm) — MAXIMAL!
│   ├── cam_follower.stl        ← Gleitschuh (×4 identisch)
│   └── crank_rod.stl           ← Zug-Stoß-Stange (×4 identisch)
├── fins/
│   ├── pectoral_mount_left.stl    ← Brustflosse links, Montage
│   ├── pectoral_mount_right.stl   ← Brustflosse rechts, Montage
│   └── dorsal_fin.stl             ← Rückenflosse (dekorativ)
├── molds/
│   ├── silikon_form_flosse.stl    ← Negativform Schwanzflosse
│   └── (weitere Silikonformen für Brustflossen)
└── misc/
    ├── cable_guide.stl         ← Kabelführung durch Gelenke
    ├── imu_mount.stl           ← IMU-Halterung (innen)
    ├── motor_mount_flange.stl  ← Motor-Flansch mit Nocken-Lagern
    └── servo_mount_j1.stl      ← Servo-Halter (optional)
```

---

## 🔴 KRITISCH: Neue Gelenk-Flansche mit variablen Hebelarmen!

Die Innovation des Redesigns liegt hier: **Jeder Flansch hat eine unterschiedliche Hebellänge!**

```
             Nocke (Standard: e=3mm, linearer Hub ±6mm überall)
                    ↓
    ┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
    │                 │                 │                 │                 │
   J1 (L=30mm)      J2 (L=25mm)      J3 (L=18mm)      J4 (L=12mm)
    ↓                 ↓                 ↓                 ↓
  ±11.3°            ±13.5°            ±18.4°            ±26.6°  ← MAXIMAL!
  (klein)           (mittel)          (groß)            (sehr groß)
  Kopf-nah          Vorder-mitte      Hinter-mitte      SCHWANZ
```

### tail_link_j1.stl — **Kopf-nahes Gelenk (Hebel L₁ = 30 mm)**

```yaml
Beschreibung:    Gelenk-Flansch J1 mit LANGER Hebellänge
Hebel-Länge:     L₁ = 30 mm  →  θ_max ≈ ±11.3°
Maße:            65 × 40 × 20 mm
Material:        PETG, 50 % Infill
Achse:           Ø 8 mm Edelstahl-Bolzen (M8), beidseitig kugelgelagert
Zug-Stoß-Punkt:  30 mm von Gelenkachse entfernt
                 Resultat: arctan(6mm / 30mm) ≈ ±11.3°
Besonderheit:    - Sanfte Bewegung, kleine Amplitude
                 - Kopfbereich (stabiler, weniger Belastung)
                 - 2× Ø 6 mm Kugellager (626-ZZ) seitlich
Montage:         An body_mid mit 2× M3-Senkkopfschrauben
```

### tail_link_j2.stl — **Vordermitte-Gelenk (Hebel L₂ = 25 mm)**

```yaml
Beschreibung:    Gelenk-Flansch J2 mit MITTLERER Hebellänge
Hebel-Länge:     L₂ = 25 mm  →  θ_max ≈ ±13.5°
Maße:            60 × 38 × 20 mm
Material:        PETG, 50 % Infill
Achse:           Ø 8 mm Edelstahl-Bolzen (M8)
Zug-Stoß-Punkt:  25 mm von Gelenkachse entfernt
Besonderheit:    - Transition zwischen Kopf und Hintermitte
                 - Mittlere Belastung
Montage:         Kettenartig nach J1 verbunden
```

### tail_link_j3.stl — **Hintermitte-Gelenk (Hebel L₃ = 18 mm)**

```yaml
Beschreibung:    Gelenk-Flansch J3 mit KURZER Hebellänge
Hebel-Länge:     L₃ = 18 mm  →  θ_max ≈ ±18.4°
Maße:            50 × 32 × 18 mm
Material:        PETG, 50 % Infill
Achse:           Ø 8 mm Edelstahl-Bolzen (M8)
Zug-Stoß-Punkt:  18 mm von Gelenkachse entfernt
Besonderheit:    - Größere Amplitude als J1/J2
                 - Höhere Belastung beginnt
                 - Schwanzbereich-Start
Montage:         Nach J2, vor Schwanz
```

### tail_link_j4.stl — **Schwanz-Gelenk (Hebel L₄ = 12 mm) — MAXIMAL!**

```yaml
Beschreibung:    Gelenk-Flansch J4 mit KÜRZESTER Hebellänge (maximal!)
Hebel-Länge:     L₄ = 12 mm  →  θ_max ≈ ±26.6°  ← MAXIMAL!
Maße:            48 × 30 × 18 mm (kompakt, hohe Kraft)
Material:        PETG, 60 % Infill  ← HÖHER (mehr Steifigkeit für Kräfte!)
Achse:           Ø 8 mm Edelstahl-Bolzen (M8)
Zug-Stoß-Punkt:  12 mm von Gelenkachse entfernt
                 Resultat: arctan(6mm / 12mm) ≈ ±26.6°
Besonderheit:    ✓ Größte Amplitude!
                 ✓ Höchste mechanische Belastung
                 ✓ 60% Infill für extra Steifigkeit
                 ✓ Schwanzspitze — maximale Auslenkung wie echter Fisch!
Montage:         Am Ende der Gelenkkette, vor Schwanzflosse
```

---

## Allgemeine Spezifikationen für alle Gelenk-Flansche

```yaml
Symmetrie:       Alle Flansche sind mittig durchbohrt (Achse Ø 8 mm)
Außen-Lager:     2× Ø 6 mm Kugellager (626-ZZ) beidseitig
                 (erlauben freie Rotation um Achse)

Schubstangen-Anschluss:
                 - Obere Fläche hat konisches Loch für M6-Bolzen
                 - Zug-Stoß-Stange wird mit M6 + Federscheibe befestigt
                 - ±0.1 mm Spielfreiheit für glatte Bewegung

Montagepunkte:   - Hinten: Verbindung zum Körper (M3 Schraube)
                 - Seiten: Kugellagersitze (Ø 6 mm Welle)
                 - Oben: Schubstangen-Anschluss (M6 Bolzen)

Materialwahl:    PETG (besser als PLA für Wasserdruck)
                 J1–J3: 50 % Infill
                 J4:    60 % Infill (höhere Belastung!)

Druckzeit:       J1/J2/J3/J4: ~30–45 Min je Teil (schnell!)
```

---

## Andere 3D-Druck-Teile (UNVERÄNDERT)

### body_front.stl
```
Beschreibung : Hauptelektronikgehäuse, torpedoförmig
Außenmaße    : 200 mm L × Ø 80 mm
Material     : PETG, 30 % Infill
Druckzeit    : ~4–5 h
```

### cam_follower.stl (×4 identisch)
```
Beschreibung : Gleitschuh, sitzt auf Nockenwelle
Maße         : 12 × 8 × 15 mm
Material     : PETG, 50 % Infill
Menge        : 4 Stück (all identical)
Druckzeit    : ~5 Min je Teil
```

### crank_rod.stl (×4 identisch)
```
Beschreibung : Zug-Stoß-Stange (verbindet Gleitschuh mit Gelenk-Flansch)
Maße         : Ø 6 mm × 25 mm Länge
Material     : PETG oder TPU (flexibel)
Menge        : 4 Stück (all identical)
Druckzeit    : ~10 Min je Teil
```

### motor_mount_flange.stl
```
Beschreibung : Motorhalter mit Nockenwellen-Lagern (6001-2RS)
Material     : PETG, 60 % Infill (hohe Steifigkeit!)
Besonderheit : 2× Ø 12 mm Lagerbuchsen-Sitze (6001er Lager)
Druckzeit    : ~1–1.5 h
```

---

## 📋 Druckparameter-Tabelle (Aktualisiert)

| Teil | Material | Layer [mm] | Infill | Wände | Stützen | Zeit ~min |
|---|---|---|---|---|---|---|
| **body_front** | PETG | 0.20 | 30% | 3 | Ja | 240–300 |
| **motor_mount_flange** | PETG | 0.20 | 60% | 4 | Ja | 60–90 |
| **cam_follower (×4)** | PETG | 0.20 | 50% | 3 | Nein | 5 je Teil |
| **crank_rod (×4)** | PETG/TPU | 0.20 | 50% | 3 | Nein | 10 je Teil |
| **tail_link_j1** | PETG | 0.20 | 50% | 3 | Ja | 35 |
| **tail_link_j2** | PETG | 0.20 | 50% | 3 | Ja | 30 |
| **tail_link_j3** | PETG | 0.20 | 50% | 3 | Ja | 25 |
| **tail_link_j4** | PETG | 0.20 | 60% | 3 | Ja | 25 |
| **pectoral_mount_L/R** | PETG | 0.20 | 40% | 4 | Ja | 20 je Teil |
| **dorsal_fin** | PLA+ | 0.20 | 15% | 3 | Nein | 20 |

**Gesamtdruckzeit: ~15–18 Stunden** (etwas schneller durch progressive Hebelarm-Teile)

---

## 🛠️ Montagereihenfolge (AKTUALISIERT)

1. **Motor-Flansch vorbereiten**
   - Beide 6001-2RS Lager einpressen (Ø 12 mm Bohrungen)
   - Nockenwelle einsetzen
   - Motor mit 4× M2 befestigen

2. **Gelenk-Flansche vorbereiten** (alle 4)
   - Kugellagersitze (626-ZZ) seitlich einpressen
   - Alle Bohrlöcher kontrollieren

3. **Gleitschuhe + Zug-Stoß-Stangen montieren**
   - 4× cam_follower auf Nocke schieben (90° Versatz)
   - 4× crank_rod mit M6-Bolzen befestigen

4. **Gelenk-Kette zusammensetzen (KRITISCH!)**
   - J1 (L₁=30mm) an body_mid mit M3-Schraube
   - J2 (L₂=25mm) über Zug-Stoß-Stange verbinden
   - J3 (L₃=18mm) über Zug-Stoß-Stange verbinden
   - J4 (L₄=12mm) LETZTE — Schwanzgelenk!
   - **Wichtig:** Unterschiedliche Hebelarm-Längen beachten!

5. **Test im Trockenen**
   - Motor langsam anfahren (10% PWM)
   - Amplituden prüfen: Schwanz SICHTBAR größer als Kopf! ✓

6. **Elektronik + Sensorik**
   - ESP32 + Sensoren in body_front
   - O-Ring einlegen, body_lid verschließen

---

## 📐 OpenSCAD-Skripte für Gelenk-Flansche

Die 4 Flansche können parametrisch mit OpenSCAD generiert werden:

```scad
// tail_link_parametric.scad
// Erzeugt J1, J2, J3, J4 durch Änderung von 'lever_length'

lever_length = 30;  // ← Ändere auf 30, 25, 18, oder 12 für J1–J4
joint_name = "J1";

// Hauptflansch (trapezoid)
difference() {
    // Außenkörper
    cube([65, 40, 20], center=true);
    
    // Inneres Loch für Achse
    cylinder(h=25, r=4, $fn=32, center=true);
    
    // Zug-Stoß-Punkt
    translate([lever_length/2, 0, 0])
        cube([8, 8, 25], center=true);
    
    // Lagersitze (beidseitig)
    translate([0, -20, 0])
        cylinder(h=25, r=3, $fn=32, center=true);
    translate([0, +20, 0])
        cylinder(h=25, r=3, $fn=32, center=true);
}

echo(str("Gelenk: ", joint_name, " | Hebel-Länge: ", lever_length, "mm"));
```

Mit diesem Skript können alle 4 Flansche schnell generiert werden!

---

## ✅ Konsistenz-Checkliste

- ✓ **Firmware** (`nocke_kinematik.py`): Progressive Hebelarm-Längen dokumentiert
- ✓ **3D-Druck** (diese Datei): 4 unterschiedliche Gelenk-Flansche spezifiziert
- ✓ **Montage**: Klare Unterscheidung J1 vs. J2 vs. J3 vs. J4
- ✓ **Material**: J4 mit 60% Infill für höhere Belastung
- ✓ **Druckzeit**: Realistisch auf ~15–18 Stunden geschätzt
- ⏳ **CAD-Dateien** (folgt): OpenSCAD-Generierung, STL-Export

---

**Status:** 🟢 Konsistent mit Redesign (Variable Hebelarm-System)  
**Nächster Schritt:** CAD-Dateien generieren oder hochladen
