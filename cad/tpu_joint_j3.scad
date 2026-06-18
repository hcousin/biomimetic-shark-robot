// ============================================================
//  tpu_joint_j3.scad — Passiver TPU-Federblock J3
//  Material: TPU 95A, 25% Gyroid Infill
//  Funktion: Elastische Verbindung Segment 2 → Segment 3
//  Resonanz: f_res ≈ 1.0 Hz
// ============================================================

// Parameter
breite     = 20;   // mm (X)
tiefe      = 15;   // mm (Y)
hoehe      = 10;   // mm (Z)
wand       = 1.2;  // mm Wandstärke (3 Perimeter à 0.4mm)
bolzen_r   = 1.1;  // mm Radius M2-Bohrung
stahl_h    = 0.5;  // mm Federstahl-Kanal Höhe
stahl_b    = 8.5;  // mm Federstahl-Kanal Breite
fase       = 1.0;  // mm Fase an Kanten (Druckbarkeit)

module tpu_federblock(b, t, h, wand, bolzen_r, stahl_h, stahl_b, fase) {
    difference() {
        // Grundkörper mit Fasen
        hull() {
            for (x = [-b/2+fase, b/2-fase])
            for (y = [-t/2+fase, t/2-fase])
            for (z = [-h/2+fase, h/2-fase])
                translate([x, y, z]) sphere(r=fase, $fn=8);
        }

        // Federstahl-Kanal (horizontal, bei Z=0)
        translate([0, 0, 0])
            cube([stahl_b, t+1, stahl_h], center=true);

        // M2-Montage-Bohrungen (2× längs, für Segmentbefestigung)
        for (x = [-b/4, b/4])
            translate([x, 0, 0])
                cylinder(h=h+1, r=bolzen_r, $fn=16, center=true);

        // Segmentverbindungs-Zapfen-Aufnahmen (vorne + hinten, Ø5mm × 3mm tief)
        for (y = [-t/2+1.5, t/2-1.5])
            translate([0, y, 0])
                cylinder(h=5, r=2.5, $fn=16, center=true);
    }
}

tpu_federblock(breite, tiefe, hoehe, wand, bolzen_r, stahl_h, stahl_b, fase);

// Info
echo(str("J3 TPU-Federblock: ", breite, "×", tiefe, "×", hoehe, "mm"));
echo(str("Material: TPU 95A | Infill: 25% Gyroid"));
echo(str("Federstahl-Kanal: ", stahl_b, "mm × ", stahl_h, "mm bei Z=0"));
echo(str("Resonanz: ~1.0 Hz | Erwartete Amplitude: ±8-10°"));
