# STEP-Format-Konvertierung

Die `.stl`-Dateien können zu echten STEP/STP-Dateien konvertiert werden mit:

## Kostenlose Tools

### FreeCAD (Empfohlen, Open Source)
1. FreeCAD installieren: https://www.freecad.org
2. Datei → Öffnen → `.stl`-Datei wählen
3. Datei → Export → `.step` wählen
4. Alle Teile als Assembly exportieren

### Online-Konverter
- https://www.freeconvert.com/stl-to-step
- https://cadexchanger.com/online/

### Python (CadQuery)
```python
import cadquery as cq
# STEP importieren/exportieren
shape = cq.importers.importStep("part.step")
cq.exporters.export(shape, "output.step")
```

## Warum STEP besser ist

| Format | Nutzen |
|---|---|
| STL | 3D-Druck, Rapid Prototyping |
| STEP/STP | CNC, Präzisionsfertigung, CAD-Austausch |
| GCODE | Direkt für 3D-Drucker/CNC |

Die Nockenwelle **muss** als STEP an die Dreherei gesendet werden!
