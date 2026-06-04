# 3D-Druckdateien-Struktur: Biomimetischer Haifisch-Roboter

## Gesamtübersicht der Druckteile (Stufe 2, 60 cm)

```
shark_robot/
├── body/
│   ├── body_front.stl          ← Vorderer Elektronikrumpf
│   ├── body_mid.stl            ← Mittelteil (Verbindungsstück)
│   ├── body_lid_front.stl      ← Deckel vorne (O-Ring-Flansch)
│   └── ballast_cylinder.stl    ← Ballastzylinder Ø 30 mm
├── tail/
│   ├── tail_link1.stl          ← Gelenk J1-Halter (Peduncle)
│   ├── tail_link2.stl          ← Gelenk J2-Halter
│   ├── tail_link3_passive.stl  ← Passives Federgelenk-Halter
│   ├── servo_horn_J1.stl       ← Angepasstes Servo-Horn J1
│   └── servo_horn_J2.stl       ← Angepasstes Servo-Horn J2
├── fins/
│   ├── pectoral_mount_L.stl    ← Brustflosse Links, Montage
│   ├── pectoral_mount_R.stl    ← Brustflosse Rechts, Montage
│   └── dorsal_fin.stl          ← Rückenflosse (dekorativ, keine Funktion)
├── molds/
│   ├── caudal_fin_mold_A.stl   ← Negativform Schwanzflosse Hälfte A
│   ├── caudal_fin_mold_B.stl   ← Negativform Schwanzflosse Hälfte B
│   ├── pect_fin_mold_A.stl     ← Negativform Brustflosse
│   └── pect_fin_mold_B.stl     ← Negativform Brustflosse
└── misc/
    ├── cable_guide.stl         ← Kabelführung durch Gelenke
    ├── imu_mount.stl           ← IMU-Halterung (innen, kalibriert)
    └── depth_sensor_port.stl   ← MS5837-Durchführung (Rohr)
```

---

## Detailspezifikationen pro Teil

### body_front.stl
```
Beschreibung : Hauptelektronikgehäuse, torpedoförmig
Aussenmasse  : 200 mm L × Ø 80 mm
Innenmasse   : Ø 74 mm × 185 mm (nutzbar)
Material     : PETG (chemisch beständiger als PLA)
Infill       : 30% Gyroid
Wandstärke   : 3 Perimeter à 0.4 mm = 1.2 mm
Besonderheit : O-Ring-Nut Ø 80 × 3 mm an beiden Flanschen
               4× M3-Schraublöcher (90° versetzt)
               Kabelkanal Ø 8 mm links (mit MS5837-Port)
               Ballastschacht 30 mm Ø (längs, hinten)
Stützstruktur: Ja (nur für O-Ring-Nut-Überhang)
Druckzeit    : ~4–5 h (0.2 mm Layer, Prusa MK4)
```

### tail_link1.stl (Peduncle-Gelenk)
```
Beschreibung : Halter für Servo J1, dreht um vertikale Achse
Masse        : 50 × 35 × 25 mm
Material     : PETG oder PLA+ (Festigkeit ausreichend)
Infill       : 50% (höhere Beanspruchung durch Servo-Drehmoment)
Lager        : 2× Ø 6/12/4 mm Kugellager (Flanschseiten)
Servo-Sitz   : MG995-kompatibel (24×23 mm Ausschnitt, 2× M2)
Achse        : Ø 6 mm Edelstahlstab (kommt nicht mit Druckteil)
Besonderheit : Asymmetrische Ausrundungen für Kabelführung
```

### tail_link3_passive.stl (Federgelenk)
```
Beschreibung : Passives Endgelenk mit Federstahl-Einlage
Masse        : 35 × 28 × 18 mm
Material     : TPU 95A (flexibel, dämpft Schwingungen)
Infill       : 25% (weicher durch geringe Dichte)
Federstahl   : 0.5 mm × 10 mm Federstahl-Streifen (eingedruckt)
               → durch Druckpause bei 8 mm Z-Höhe einlegen
Druckhinweis : TPU braucht Direct Drive Extruder; kein Bowden
```

### caudal_fin_mold_A/B.stl (Negativform)
```
Beschreibung : Zweiteilige Form für Silikon-Schwanzflosse
Gesamtmasse  : 140 × 95 × 30 mm (je Hälfte)
Material     : PLA (günstiger, ausreichend formstabil)
Infill       : 60% (Formstabilität unter Silikondruck)
Oberfläche   : Schleifen nach Druck! 120er → 240er → 400er
               Dann 2× dünn Epoxy-Coating, schleifen (400er)
Passstifte   : 4× Ø 4 mm Löcher (M4-Schraube als Stift nutzen)
Angusskanal  : Ø 8 mm, oben mittig
Entlüftung   : 2× Ø 2 mm diagonal an Flossenwurzeln
CFK-Kanal    : Ø 3.5 mm Tunnel, 30% Chord, horizontal
```

---

## Druckparameter-Tabelle

| Teil | Material | Layer [mm] | Infill | Wände | Stützen | Zeit ~h |
|---|---|---|---|---|---|---|
| body_front | PETG | 0.20 | 30% | 3 | Ja | 5 |
| body_mid | PETG | 0.20 | 25% | 3 | Nein | 2 |
| body_lid | PETG | 0.15 | 40% | 4 | Nein | 1 |
| tail_link 1+2 | PLA+ | 0.20 | 50% | 4 | Ja | 1.5 |
| tail_link3 | TPU 95A | 0.25 | 25% | 3 | Nein | 1 |
| servo_horns | PLA+ | 0.15 | 60% | 5 | Nein | 0.5 |
| fin_molds | PLA | 0.20 | 60% | 4 | Ja | 3 |
| pect_mounts | PETG | 0.20 | 40% | 4 | Ja | 1 |
| dorsal_fin | PLA+ | 0.20 | 15% | 3 | Nein | 0.5 |

Gesamtdruckzeit (Schätzung): **~16–18 Stunden**

---

## Montagereihenfolge

1. `body_front` + `body_mid` via M3×12 Schrauben verbinden (O-Ring einlegen)
2. Elektronik in `body_front` montieren (PCB-Halterung mit M2)
3. `tail_link1` über M3-Achse an `body_mid` befestigen, Servo J1 einbauen
4. `tail_link2` ketteartig folgen, Servo J2
5. `tail_link3` (TPU) als passives Endgelenk
6. Silikonflossen aufstecken + fixieren (Schrumpfschlauch oder Silikonkleber)
7. Kabel durch `cable_guide` führen, mit Kabelbinder sichern
8. `body_lid_front` als letztes schliessen

---

## FreeCAD / OpenSCAD Quellen
Die Parametrische Basisform des Körpers ist als OpenSCAD-Skript definierbar:
```scad
// body_front.scad — parametrisch
length = 200;
outer_r = 40;
wall = 3;
oring_r = 3;
oring_depth = 2;

difference() {
  // Hauptkörper
  union() {
    cylinder(h=length, r=outer_r, $fn=64);
    // Bugkegel
    translate([0,0,length]) sphere(r=outer_r, $fn=64);
  }
  // Innenhohlraum
  cylinder(h=length-wall, r=outer_r-wall, $fn=64);
  // O-Ring-Nut (beide Flansche)
  translate([0,0,wall])
    rotate_extrude($fn=64)
    translate([outer_r-oring_r/2, 0])
    circle(r=oring_r/2, $fn=16);
}
```
