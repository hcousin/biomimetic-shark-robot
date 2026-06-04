// Silikonform für Schwanzflosse (Lunate)
// Material: PLA (Negativform), 60% Infill
// Zwei Hälften: A und B
// Ergibt Silikonabguss nach Dragon Skin 10

$fn = 64;

// Parameter
span = 120;    // Spannweite (mm)
chord = 80;    // Chord (mm)
thickness = 12; // Max dicke (mm, NACA 0010)
cfc_hole = 3.5; // CFK-Kern-Kanal Ø

module naca_0010_profile() {
    // Approximation NACA 0010 Profil
    scale([chord, thickness/2, 1])
        circle(r=0.5, $fn=32);
}

module caudal_fin_half() {
    difference() {
        union() {
            // Halbe Form
            translate([0, 0, span/4])
                linear_extrude(height=span/2)
                    naca_0010_profile();
        }
        // CFK-Kanal
        cylinder(h=span, r=cfc_hole/2, $fn=8);
    }
}

module form_flansch() {
    // Flache Flansch-Fläche zum Zusammenfügen
    cube([chord+10, span+10, 3], center=true);
}

// ASSEMBLY
union() {
    caudal_fin_half();
    form_flansch();
}
