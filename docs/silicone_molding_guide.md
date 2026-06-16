# Silikonabguss-Anleitung: Haifisch-Haut & Schwanzflosse

## Überblick
Zwei separate Abgüsse:
1. **Schwanzflosse** (lunate, 12×8 cm) aus Dragon Skin 10 über CFK-Kern
2. **Körperhaut** (optionale Oberfläche) aus Dragon Skin 10 Slow, eingefärbt

---

## Teil 1: Schwanzflosse

### Materialien
| Material | Menge | Bezugsquelle |
|---|---|---|
| Dragon Skin 10 Fast (2-Komponenten) | 250 g Kit | Smooth-On / Amazon |
| Trennmittel (Mann 200) | 1 Dose | Smooth-On |
| CFK-Stab Ø 3 mm, 15 cm | 1 Stk. | Modellbauhandel |
| PLA-Filament (für Negativform) | ~50 g | — |
| Vakuumpumpe (optional) | — | Leihbar |
| Silikon-Pigment blau-grau | 2 ml | Smooth-On |

### Schritt 1: Negativform (3D-Druck)
Die Negativform wird in 2 Hälften gedruckt (Parting-Line entlang der Mittelebene der Flosse).

**Flosse Querschnitt (NACA-0010-Profil):**
- Gesamtspannweite: 120 mm (2× 60 mm Halbspannweite)
- Max. Chord: 80 mm
- Max. Dicke: 12 mm (10 % von 120 mm — NACA 0010)
- Lunate-Form: geschwungene Vorderkante, konkave Hinterkante

**STL-Form-Einstellungen:**
```
Layer Height:  0.2 mm (PETG)
Infill:        40 % (genug Steifigkeit gegen Silikondruck)
Walls:         4 Perimeter
Supports:      nein (Form muss aus 2 trennbaren Hälften bestehen)
Finish:        120er + 240er Schleifpapier, dann Epoxy-Coating
```

**CFK-Kern-Kanal:** Ø 3.5 mm Kanal entlang der Neutralachse, leicht nach vorne versetzt (30 % Chord) — wie bei echten Flossen-Calcifications.

### Schritt 2: Mischen & Einfärben
```
Dragon Skin 10 Fast:
  Part A : Part B = 1:1 nach Gewicht (z. B. 60 g : 60 g)
  Topf-Leben: ~3 Minuten (schnell arbeiten!)
  Aushärtung: 75 Minuten bei 23 °C

Pigmentierung (Blauhai-Grau):
  - 2 % Silikon-Pigment Blau: ~2.4 g auf 120 g Total
  - 0.5 % Schwarz: ~0.6 g
  → Ergibt: CMYK approx (85, 60, 30, 10) — typisches Haifisch-Rückengrau
```

### Schritt 3: Guss
1. Beide Formhälften mit Mann 200 Trennmittel einsprühen, 5 Min. trocknen lassen. Zweimal wiederholen.
2. CFK-Stab mit Klebeband temporär in Kanalposition halten.
3. Silikon mischen (s. o.), sofort in untere Formhälfte gießen — von einer Ecke aus, als Faden gießen, um Blasen zu vermeiden.
4. Obere Formhälfte auflegen, Schrauben M4 gleichmäßig anziehen (max. 2 N·m).
5. Optional: Vakuumkammer 2 Minuten bei −0.8 bar für blasenfreies Silikon.
6. 90 Minuten warten (Dragon Skin 10 Fast).
7. Vorsichtig öffnen — zuerst Schrauben, dann Formhälften auseinanderdrücken (nicht hebeln).
8. Flosse 24 Stunden nachaushärten lassen.

### Qualitätskontrolle
- Keine sichtbaren Blasen (bei Licht halten)
- CFK-Kern sitzt bei 25–35 % Chord
- Flossenflex-Test: leichtes Biegen ±30° ohne Delaminierung
- Wanddicke: 2–3 mm gleichmäßig

---

## Teil 2: Körperhaut (optional)

Die Körperhaut ist ein 2–3 mm dünner Silikonüberzug über dem 3D-gedruckten Rumpf. Sie verbessert die Optik und reduziert leicht die Grenzschichtstörung.

### Materialien
| Material | Menge |
|---|---|
| Dragon Skin 10 Slow | 500 g |
| Silikon-Pigmente (blau, grau, weiß) | je 5 ml |
| Slacker Softener (für Bauch-Region) | 50 ml |
| Pinsel 2 cm, Spachtel | — |

### Methode: Brush-On Skin
Statt Abguss wird die Haut direkt auf den Rumpf aufgepinselt (einfacher, weniger Abfall).

**Farbschema Weißer Hai / Blauhai:**
```
Rücken (dorsal):   DS10 + 3 % blau + 1 % schwarz + 0.5 % grün-grau
Flanke (lateral):  Übergangszone, trocken gemischt aus beiden
Bauch (ventral):   DS10 Slow + 20 % Slacker + 1 % weiß (leicht weicher)
```

**Aufbau (3 Schichten):**
1. Schicht: 1:1 mit Silikon-Thinner verdünnt → Grundierung, dünn aufpinseln. 30 Min.
2. Schicht: Unverdünnt, Rückenfarbe, 2–3 mm. 90 Min.
3. Schicht (Bauch): Verdünnte Weißmischung, weich überpinseln. 60 Min.

**Trennlinie**: Mit Klebeband entlang der Lateral-Linie abkleben vor Schicht 2/3.

**Oberflächenstruktur (optional):**
Durch Abrollen einer strukturierten PETG-Rolle (Haizahn-ähnliches Muster, 3D-gedruckt) auf der noch nicht ausgehärteten Schicht 2 lässt sich eine grobe Dentikel-Textur eindrücken.

---

## Teil 3: Brustflossen
Identische Methode wie Schwanzflosse, aber:
- Profil: NACA 0010, Spannweite 40 mm, Chord 25 mm
- CFK-Stab Ø 2 mm, leicht zur Hinterkante hin gebogen (5°)
- Material: DS10 Slow (flexibler, für Brustflosse wichtig)
- Einbettung: 2× M2-Messing-Insert für Servo-Verbindung an der Wurzel

---

## Sicherheitshinweise
- Dragon Skin Part A + B nie unvermischt auf die Haut bringen — Latexhandschuhe tragen
- Trennmittel gut belüften
- Vakuumpumpe: nie über −0.9 bar (Formverformung)
- Ausgussmaterial: Schwindung ~0 %, keine Nachkalibrierung nötig
