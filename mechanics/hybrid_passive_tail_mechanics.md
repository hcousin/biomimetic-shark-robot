# Hybrid-Antrieb: Aktive Nockenwelle (J1/J2) + Passive TPU-Gelenke (J3/J4)

## Konzept-Übersicht

```
Brushless Motor (KV=900)
        ↓
Getriebe 40:1
        ↓
Kurze Nockenwelle (nur ~60mm, 2 Gleitschuhe)
        ↓
2 Zug-Stoß-Stangen
        ↓
J1 (L=30mm, aktiv) ──→ J2 (L=25mm, aktiv)
                              ↓
                        J3 (TPU, passiv) ──→ J4 (TPU, passiv)
                        [Federeffekt]         [Federeffekt]
```

**Prinzip:**
- J1 + J2 werden **aktiv** von der Nockenwelle angetrieben
- J3 + J4 sind **passive TPU-Federgelenke** — sie schwingen durch die
  Trägheit und Wasserkräfte natürlich nach, wie der echte Schwanzbereich
  eines Hais

---

## Warum das biologisch überzeugend ist

Echte Haie (Carangiform/Thunniform-Schwimmer) haben:
- **Vorderkörper:** Aktive Muskulatur, kontrollierte Bewegung
- **Peduncle (Schwanzstiel):** Steife Sehnen, passive Kraftübertragung
- **Schwanzflosse:** Passiv elastisch, schwingt durch Hydrodynamik nach

→ Unser Hybrid-Design imitiert genau das:

| Bereich | Natur | Unser Roboter |
|---|---|---|
| Vorderkörper | Aktive Muskeln | Nockenwelle J1/J2 |
| Schwanzstiel | Steife Sehnen | TPU J3 (mittelharte Feder) |
| Schwanzflosse | Passiv elastisch | TPU J4 (weiche Feder) |

---

## Mechanik-Details

### Aktive Nockenwelle (J1 + J2)

```
Nockenwelle: Edelstahl, Ø12mm × 60mm (NUR 60mm — viel kürzer!)
Exzentrizität: e = 3mm
Gleitschuhe: 2 Stück (0° und 90° versetzt)

J1 @ 0°:  Hebel L₁ = 30mm → Amplitude arcsin(3/30) ≈ ±5.7°
J2 @ 90°: Hebel L₂ = 25mm → Amplitude arcsin(3/25) ≈ ±6.9°

Phasenversatz J1→J2: 90° (mechanisch durch Gleitschuh-Position)
```

**Vorteile kurze Nockenwelle:**
- Nur 60mm statt 120mm → passt leichter in den Rumpf
- Leichter, günstiger zu drehen (~20–25 CHF)
- Weniger Vibration
- Einfachere Lagerung (nur 2 Lagerbuchsen nötig)

### Passive TPU-Gelenke (J3 + J4)

```
Material:    TPU 95A (J3, mittelharte Feder)
             TPU 85A (J4, weiche Feder — mehr Nachschwingen)

Geometrie:   Kein separater Gelenk-Flansch mit Hebel!
             Stattdessen: Direkte TPU-Verbindung zwischen Segmenten

             Segment 2 ──[TPU-Block J3]── Segment 3
             Segment 3 ──[TPU-Block J4]── Schwanzflosse

TPU-Block-Maße:
  J3: 20 × 15 × 10mm, Shore 95A → ca. ±8–12° bei Wasserlast
  J4: 15 × 12 × 8mm,  Shore 85A → ca. ±12–18° bei Wasserlast

Federstahl-Einlage (optional):
  0.3mm × 8mm Federstahl-Streifen durch J4-Mitte
  → Gibt definierte Steifigkeit, verhindert zu weiches "Schlabbern"
```

**Passive Bewegung entsteht durch:**
1. Trägheit des Schwanzsegments bei Richtungsumkehr
2. Hydrodynamische Kräfte (Wasser drückt Flosse)
3. Rückstellkraft des TPU (Federwirkung)

→ Resultat: Natürlich ausschwingender Schwanz, ähnlich echtem Hai!

---

## Vergleich: Altes vs. neues Design

| Merkmal | Altes Design (4× aktiv) | Neues Design (2× aktiv + 2× passiv) |
|---|---|---|
| Nockenwellen-Länge | 120mm | **60mm** |
| Nockenwellen-Kosten | ~35 CHF | **~20 CHF** |
| Anzahl Gleitschuhe | 4 | **2** |
| Anzahl Zug-Stoß-Stangen | 4 | **2** |
| Gelenk-Flansche (komplex) | 4 | **2** |
| TPU-Blöcke (einfach) | 0 | **2** |
| Montage-Komplexität | ★★★★☆ | **★★☆☆☆** |
| Biologische Authentizität | ★★★★☆ | **★★★★★** |
| Kontrollierbarkeit | ★★★★★ | ★★★☆☆ |

---

## 3D-Druck: Neue Teile

### tpu_joint_j3.stl
```yaml
Funktion:    Passives Federgelenk zwischen Segment 2 und 3
Material:    TPU 95A
Maße:        20 × 15 × 10mm
Infill:      25% (weicher durch geringe Dichte)
Einlage:     Optional: 0.3mm Federstahl-Streifen (einlegen bei Z=5mm)
Montage:     Direkt zwischen Segment 2 + 3 eingeklebt (Silikongeklebt)
             oder mit 2× M2-Schrauben fixiert
Steifigkeit: ~0.08 N·mm/° (Schätzung, abhängig von Infill)
```

### tpu_joint_j4.stl
```yaml
Funktion:    Passives Federgelenk zwischen Segment 3 und Schwanzflosse
Material:    TPU 85A (weicher als J3!)
Maße:        15 × 12 × 8mm
Infill:      20% (sehr weich, maximales Nachschwingen)
Einlage:     0.3mm × 8mm Federstahl EMPFOHLEN (verhindert Überdehnung)
Montage:     Direkt an Schwanzflosse angeklebt
Steifigkeit: ~0.04 N·mm/° (sehr weich)
```

### nocken_kurz_halter.stl (AKTUALISIERT)
```yaml
Funktion:    Motorhalter + Nockenwellen-Lager (nur 60mm Welle)
Material:    PETG, 60% Infill
Änderung:   Lagerbuchsen jetzt nur 60mm auseinander (statt 120mm)
             → Kompakterer Halter, leichter
```

---

## Montagereihenfolge (Vereinfacht!)

1. **Kurze Nockenwelle vorbereiten** (Dreherei, ~20 CHF)
   - Ø12mm × 60mm, e=3mm
   - 2 Lager-Bohrungen (6001-2RS)

2. **Motor + Getriebe montieren**
   - Wie bisher (unverändert)

3. **Nur 2 Gleitschuhe + 2 Zug-Stoß-Stangen**
   - J1-Gleitschuh @ 0°
   - J2-Gleitschuh @ 90°
   - Schubstangen an Gelenk-Flansche J1/J2

4. **TPU-Blöcke einsetzen**
   - J3: TPU 95A zwischen Segment 2+3 einkleben
   - J4: TPU 85A zwischen Segment 3+Flosse einkleben
   - Federstahl-Einlage optional einlegen

5. **Test im Trockenen**
   - Aktive Gelenke: gleichmäßige Bewegung J1/J2?
   - Passive Gelenke: schwingen J3/J4 frei nach? (von Hand prüfen)

6. **Wassertest**
   - Bei 0.5 Hz: Schwanz sollte elegant nachschwingen
   - Bei 1.5 Hz: Schwanz schwingt mit, Amplitude wächst durch Resonanz

---

## Abstimmung der TPU-Steifigkeit

Die optimale Steifigkeit hängt von der Schwimmfrequenz ab.
Ziel: **Resonanzfrequenz der passiven Gelenke ≈ Schwimmfrequenz**

```
f_resonanz = (1/2π) × √(k/m)

k = Federsteifigkeit TPU [N·mm/°]
m = Trägheitsmoment Schwanzsegment [kg·mm²]

Für f_resonanz ≈ 1.0–1.5 Hz:
  → TPU 85A mit 20% Infill und ~5g Schwanzsegment: gut
  → Falls zu steif: Infill reduzieren oder TPU 75A verwenden
  → Falls zu weich: Infill erhöhen oder Federstahl-Einlage hinzufügen
```

---

## Kosten-Update

| Komponente | Altes Design | Neues Design |
|---|---|---|
| Nockenwelle | 35 CHF | **20 CHF** |
| Gleitschuhe (×2 statt ×4) | 4 CHF | **2 CHF** |
| Gelenk-Flansche (×2 statt ×4) | 4 CHF | **2 CHF** |
| TPU-Blöcke J3+J4 (neu) | — | **1 CHF** |
| **Ersparnis** | — | **~18 CHF** |

**Neues Total: ~460 CHF**

---

## Status

- ✅ Konzept definiert
- ⏳ nocke_kinematik.py anpassen (nur J1/J2 aktiv)
- ⏳ 3d_print_structure.md aktualisieren
- ⏳ OpenSCAD-Skript für TPU-Blöcke
