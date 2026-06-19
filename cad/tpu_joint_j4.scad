// ============================================================
//  tpu_joint_j4.scad — Passiver TPU-Federblock J4
//  Material: TPU 85A (WEICHER als J3!), 20% Gyroid Infill
//  Funktion: Elastische Verbindung Segment 3 → Schwanzflosse
//  Resonanz: f_res ≈ 0.8 Hz — maximales Nachschwingen!
// ============================================================

// Parameter (kompakter als J3)
breite     = 15;   // mm (X)
tiefe      = 12;   // mm (Y)
hoehe      = 8;    // mm (Z)
wand       = 0.8;  // mm Wandstärke (2 Perimeter à 0.4mm — sehr weich!)
bolzen_r   = 1.1;  // mm Radius M2-Bohrung
stahl_h    = 0.5;  // mm Federstahl-Kanal Höhe
stahl_b    = 6.5;  // mm Federstahl-Kanal Breite (kürzer als J3)
fase       = 0.8;  // mm Fase
anstell    = 3;    // mm Federstahl leicht nach hinten versetzt
               //    → gibt Schwanzflosse natürlichen Anstellwinkel

module tpu_federblock_j4(b, t, h, bolzen_r, stahl_h, stahl_b, fase, anstell) {
    difference() {
        // Grundkörper mit Fasen
        hull() {
            for (x = [-b/2+fase, b/2-fase])
            for (y = [-t/2+fase, t/2-fase])
            for (z = [-h/2+fase, h/2-fase])
                translate([x, y, z]) sphere(r=fase, $fn=8);
        }

        // Federstahl-Kanal (leicht nach hinten versetzt → Anstellwinkel)
        translate([anstell, 0, 0])
            cube([stahl_b, t+1, stahl_h], center=true);

        // M2-Montage-Bohrung (1× zentral — kleinerer Block)
        translate([0, 0, 0])
            cylinder(h=h+1, r=bolzen_r, $fn=16, center=true);

        // Schwanzflosse-Verbindungs-Nut (hinten, für CFK-Stab Ø3mm)
        translate([b/4, 0, 0])
            cylinder(h=h+1, r=1.6, $fn=16, center=true);

        // Segment-Zapfen-Aufnahme (vorne)
        translate([-b/4, 0, 0])
            cylinder(h=5, r=2.0, $fn=16, center=true);
    }
}

tpu_federblock_j4(breite, tiefe, hoehe, bolzen_r, stahl_h, stahl_b, fase, anstell);

echo(str("J4 TPU-Federblock: ", breite, "×", tiefe, "×", hoehe, "mm"));
echo(str("Material: TPU 85A | Infill: 20% Gyroid"));
echo(str("Federstahl-Kanal: ", stahl_b, "mm, versetzt ", anstell, "mm → Anstellwinkel"));
echo(str("Resonanz: ~0.8 Hz | Erwartete Amplitude: ±12-18°"));
