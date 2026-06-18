# 3D-Druckdateien-Struktur: Hybrid-Design (Aktive J1/J2 + Passive J3/J4)

> **Branch:** `dev/hybrid-passive-tail`
> **Design:** Kurze Nockenwelle (60mm) für J1+J2 aktiv, TPU-Federblöcke für J3+J4 passiv

---

## Dateistruktur

```
shark_robot/
├── body/
│   ├── body_front.stl             ← Vorderer Elektronikrumpf (unverändert)
│   ├── body_mid.stl               ← Mittelteil (unverändert)
│   ├── body_lid_front.stl         ← Deckel vorne (unverändert)
│   └── ballast_cylinder.stl       ← Ballastzylinder (unverändert)
├── tail/
│   ├── tail_link_j1.stl           ← Aktiver Gelenk-Flansch J1 (L=30mm)
│   ├── tail_link_j2.stl           ← Aktiver Gelenk-Flansch J2 (L=25mm)
│   ├── tpu_joint_j3.stl           ← Passiver TPU-Federblock J3 (Shore 95A)
│   ├── tpu_joint_j4.stl           ← Passiver TPU-Federblock J4 (Shore 85A)
│   ├── cam_follower.stl           ← Gleitschuh (×2 identisch, nicht ×4!)
│   └── crank_rod.stl              ← Zug-Stoß-Stange (×2 identisch)
├── fins/                          ← Unverändert
├── molds/                         ← Unverändert
└── misc/
    ├── nocken_halter_kurz.stl     ← NEU: Motorhalter für 60mm Nockenwelle
    ├── cable_guide.stl            ← Unverändert
    ├── imu_mount.stl              ← Unverändert
    └── depth_sensor_port.stl      ← Unverändert
```

---

## 🔴 Aktive Gelenke (Nockenwelle)

### tail_link_j1.stl — Aktives Gelenk J1 (Hebel L₁ = 30mm)

```yaml
Funktion:        Kopfnahes Gelenk, aktiv von Nockenwelle angetrieben
Hebel-Länge:     L₁ = 30mm → arcsin(3/30) ≈ ±5.7°
Maße:            65 × 40 × 20mm
Material:        PETG, 50% Infill
Achse:           Ø8mm Edelstahl-Bolzen (M8), 2× Kugellager 626-ZZ
Zug-Stoß-Punkt:  30mm von Gelenkachse
Montage:         An body_mid mit 2× M3-Schrauben
Druckzeit:       ~35 Min
```

### tail_link_j2.stl — Aktives Gelenk J2 (Hebel L₂ = 25mm)

```yaml
Funktion:        Zweites aktives Gelenk, 90° Phasenversatz zu J1
Hebel-Länge:     L₂ = 25mm → arcsin(3/25) ≈ ±6.9°
Maße:            60 × 38 × 20mm
Material:        PETG, 50% Infill
Achse:           Ø8mm Edelstahl-Bolzen (M8), 2× Kugellager 626-ZZ
Zug-Stoß-Punkt:  25mm von Gelenkachse
Montage:         Kettenartig nach J1
Druckzeit:       ~30 Min
```

---

## 🟢 Passive Gelenke (TPU-Federblöcke)

> Keine separaten Flansche mit Hebeln! Die Bewegung entsteht durch
> Trägheit + Wasserkräfte + TPU-Rückstellkraft — wie bei echten Haifischen.

### tpu_joint_j3.stl — Passiver Federblock J3

```yaml
Funktion:        Elastisches Verbindungsstück zwischen Segment 2 und 3
Material:        TPU 95A (mittelharte Feder)
Maße:            20 × 15 × 10mm
Infill:          25% Gyroid (weich, gleichmäßig)
Wandstärke:      1.2mm (3 Perimeter à 0.4mm)
Federstahl:      EMPFOHLEN: 0.3mm × 8mm Streifen bei Z=5mm einlegen
                 → Verhindert Überdehnung, definiert Mindeststeifigkeit
Montage:         Mit Silikonkleber zwischen Segment 2 + 3 einkleben
                 ODER 2× M2-Schrauben (Bohrungen im Block vorhanden)
Resonanz:        f_res ≈ 1.0 Hz → optimal bei ~25% Throttle
Erwartete Amp.:  ±8–10° bei 1.0 Hz Schwimmfrequenz
Druckzeit:       ~8 Min
Drucker:         ⚠️ Nur Direct-Drive-Extruder (kein Bowden für TPU!)
```

### tpu_joint_j4.stl — Passiver Federblock J4

```yaml
Funktion:        Elastisches Verbindungsstück zwischen Segment 3 und Schwanzflosse
Material:        TPU 85A (weicher als J3 — mehr Nachschwingen!)
Maße:            15 × 12 × 8mm
Infill:          20% Gyroid (sehr weich)
Wandstärke:      0.8mm (2 Perimeter à 0.4mm)
Federstahl:      EMPFOHLEN: 0.3mm × 6mm Streifen, leicht zur Hinterkante gebogen
                 → Gibt Schwanzflosse einen natürlichen Anstellwinkel
Montage:         Direkt an Schwanzflosse angeklebt (Epoxy oder Silikonkleber)
Resonanz:        f_res ≈ 0.8 Hz → leichtes Nachschwingen bei allen Frequenzen
Erwartete Amp.:  ±12–18° (Resonanzverstärkung bei ~0.8 Hz!)
Druckzeit:       ~5 Min
Drucker:         ⚠️ Nur Direct-Drive-Extruder (kein Bowden für TPU!)
```

---

## Vergleich: Altes Design vs. Hybrid

| Teil | Altes Design (4× aktiv) | Hybrid (2× aktiv + 2× passiv) |
|---|---|---|
| Nockenwelle | 120mm, 4 Gleitschuhe | **60mm, 2 Gleitschuhe** |
| Gelenk-Flansche | 4× PETG (komplex) | **2× PETG + 2× TPU (einfach)** |
| Zug-Stoß-Stangen | 4 Stück | **2 Stück** |
| Druckteile total | ~13 STL | **~11 STL** |
| Montage-Komplexität | ★★★★☆ | **★★☆☆☆** |
| Bio-Authentizität | ★★★★☆ | **★★★★★** |

---

## Druckparameter-Tabelle

| Teil | Material | Layer | Infill | Wände | Stützen | Zeit |
|---|---|---|---|---|---|---|
| tail_link_j1 | PETG | 0.20mm | 50% | 3 | Ja | 35 Min |
| tail_link_j2 | PETG | 0.20mm | 50% | 3 | Ja | 30 Min |
| **tpu_joint_j3** | **TPU 95A** | **0.25mm** | **25%** | **3** | Nein | **8 Min** |
| **tpu_joint_j4** | **TPU 85A** | **0.25mm** | **20%** | **2** | Nein | **5 Min** |
| cam_follower ×2 | PETG | 0.20mm | 50% | 3 | Nein | 5 Min je |
| crank_rod ×2 | PETG | 0.20mm | 50% | 3 | Nein | 10 Min je |
| nocken_halter_kurz | PETG | 0.20mm | 60% | 4 | Ja | 45 Min |

**Gesamtdruckzeit: ~10–12 Stunden** (kürzer als vorher!)

---

## Montagereihenfolge

1. **Kurze Nockenwelle** (60mm, Dreherei ~20 CHF)
   - 2× 6001-2RS Lager in `nocken_halter_kurz` einpressen
   - Motor + Getriebe montieren

2. **Aktive Gelenke J1 + J2**
   - 2× Gleitschuh @ 0° und 90° auf Nocke
   - 2× Zug-Stoß-Stangen an J1 + J2 Flansche anschließen
   - Test: Bewegen sich J1/J2 gleichmäßig mit 90° Versatz?

3. **Passive Gelenke J3 + J4** ← NEU, einfach!
   - Federstahl-Einlage bei Z=5mm in `tpu_joint_j3` einlegen
   - `tpu_joint_j3` zwischen Segment 2 + 3 mit Silikonkleber fixieren
   - 24h aushärten lassen
   - `tpu_joint_j4` an Schwanzflosse ankleben, 24h aushärten

4. **Test im Trockenen**
   - Motor bei 10% Throttle anfahren
   - J1/J2 sollten aktiv schwingen
   - J3/J4 von Hand prüfen: leicht biegbar, kehrt selbst zurück?

5. **Wassertest**
   - Bei 25% Throttle (~1.0 Hz): J3 sollte in Resonanz mitschwingen
   - Bei 20% Throttle (~0.8 Hz): J4 schwingt stärker (Resonanz J4!)
   - Schaut es wie ein echter Hai aus? ✓

---

## Abstimmung im Betrieb

Falls J3/J4 zu steif (wenig Bewegung):
- Infill reduzieren (z.B. 15%)
- TPU mit niedrigerem Shore-Wert (85A → 75A für J3)

Falls J3/J4 zu weich (schlabbernd):
- Infill erhöhen
- Federstahl-Einlage dicker (0.5mm statt 0.3mm)
- Shore-Wert erhöhen

---

## OpenSCAD-Skizze TPU-Federblock

```scad
// tpu_joint_parametric.scad
// Für J3: breite=20, tiefe=15, hoehe=10, shore=95
// Für J4: breite=15, tiefe=12, hoehe=8,  shore=85

breite = 20;
tiefe  = 15;
hoehe  = 10;

difference() {
    // Grundkörper
    cube([breite, tiefe, hoehe], center=true);

    // Montage-Bohrungen (2× M2)
    for (x = [-breite/4, breite/4])
        translate([x, 0, 0])
            cylinder(h=hoehe+1, r=1.1, $fn=16, center=true);

    // Federstahl-Kanal (bei Z=0, horizontal)
    translate([0, 0, 0])
        cube([breite+1, 1.0, 0.5], center=true);
}

// Info
echo(str("TPU-Block: ", breite, "×", tiefe, "×", hoehe, "mm"));
echo(str("Federstahl-Kanal bei Z=0 (Mitte)"));
```

---

## ✅ Konsistenz-Checkliste (Branch: dev/hybrid-passive-tail)

- ✅ `mechanics/hybrid_passive_tail_mechanics.md` — Konzept
- ✅ `firmware/nocke_kinematik.py` — J1/J2 aktiv, J3/J4 Feder-Simulation
- ✅ `docs/3d_print_structure.md` — TPU-Blöcke J3+J4 spezifiziert
- ⏳ OpenSCAD `.scad` Dateien für tpu_joint_j3 + j4
- ⏳ BOM aktualisieren (Branch-Version)

---

**Status:** 🟢 Hybrid-Design dokumentiert
