// ============================================================
//  tail_link_parametric.scad — Aktive Gelenk-Flansche J1 + J2
//  Erzeugt J1 (lever=30mm) oder J2 (lever=25mm)
//  Material: PETG, 50% Infill
// ============================================================

// ← Hier anpassen für J1 oder J2:
joint_name   = "J1";   // "J1" oder "J2"
lever_length = 30;     // J1=30mm, J2=25mm

// Berechnete Amplitude (nur Info):
// theta_max = arcsin(3mm / lever_length)
// J1: arcsin(3/30) ≈ 5.74°
// J2: arcsin(3/25) ≈ 6.89°

// Abmessungen
breite     = (lever_length == 30) ? 65 : 60;
tiefe      = (lever_length == 30) ? 40 : 38;
hoehe      = 20;
achse_r    = 4.1;   // Ø8.2mm für M8-Bolzen (leichtes Spiel)
lager_r    = 3.05;  // Ø6.1mm für 626-ZZ Kugellager
fase       = 1.5;

module gelenk_flansch(b, t, h, lever, achse_r, lager_r, fase) {
    difference() {
        // Hauptkörper
        hull() {
            for (x = [-b/2+fase, b/2-fase])
            for (y = [-t/2+fase, t/2-fase])
            for (z = [-h/2+fase, h/2-fase])
                translate([x, y, z]) sphere(r=fase, $fn=8);
        }

        // Zentrale Achsen-Bohrung (Ø8mm für M8-Bolzen)
        cylinder(h=h+1, r=achse_r, $fn=32, center=true);

        // Kugellager-Sitze beidseitig (626-ZZ, Ø6mm)
        for (y = [-t/2+2, t/2-2])
            translate([0, y, 0])
                cylinder(h=8, r=lager_r, $fn=24, center=true);

        // Zug-Stoß-Stangen-Anschluss (M6-Gewinde, am Hebelpunkt)
        translate([lever, 0, 0])
            cylinder(h=h+1, r=3.2, $fn=24, center=true);

        // Montagebohrungen zum Körper (2× M3)
        for (x = [-b/2+5, b/2-5])
            translate([x, 0, 0])
                cylinder(h=h+1, r=1.6, $fn=16, center=true);

        // Kabelkanal (Ø5mm, längs)
        translate([0, 0, 0])
            rotate([90, 0, 0])
                cylinder(h=t+1, r=2.5, $fn=16, center=true);
    }
}

gelenk_flansch(breite, tiefe, hoehe, lever_length, achse_r, lager_r, fase);

echo(str("Gelenk-Flansch ", joint_name, ": ", breite, "×", tiefe, "×", hoehe, "mm"));
echo(str("Hebel-Länge: ", lever_length, "mm"));
echo(str("Material: PETG | Infill: 50%"));
