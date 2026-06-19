// ============================================================
//  body_to_j1_flange.scad
//  Verbindungsflansch: Haifisch-Körper → Schwanzsegment J1
//
//  Zweck:
//    Schnittstelle zwischen dem importierten Hai-Körper (Fusion 360)
//    und dem ersten aktiven Gelenk-Flansch J1 (tail_link_j1.stl).
//
//  Workflow Fusion 360:
//    1. Dieses SCAD als STL exportieren (OpenSCAD → F6 → Export)
//    2. In Fusion 360: Insert → Insert Mesh → body_to_j1_flange.stl
//    3. Mit dem Hai-Körper (nach Shell) an der Schnittfläche ausrichten
//    4. Combine → Join
//    5. Gesamtes Modell als STEP exportieren (für Dreherei/Dokumentation)
//
//  Koordinatensystem:
//    +X = Schwanzrichtung (hinten)
//    -X = Kopfrichtung (vorne)
//    Z  = vertikal (oben)
// ============================================================

// ── Parameter ────────────────────────────────────────────────

// Körper-Querschnitt an der Schnittstelle (Hai-Rumpf, ~60% Länge)
body_w      = 55;    // mm Breite des Rumpfs an Schnittstelle
body_h      = 45;    // mm Höhe des Rumpfs an Schnittstelle
body_wall   = 3;     // mm Wandstärke Rumpf (aus Fusion 360 Shell)

// Flansch-Geometrie
flange_len  = 30;    // mm Länge des Übergangsstücks
flange_r    = 22;    // mm Aussenradius zylindrischer Zapfen (für J1)
j1_bore_r   = 4.1;  // mm Innenbohrung für M8-Achse (Gelenk J1)
j1_w        = 65;    // mm Breite J1-Flansch (aus tail_link_j1.stl)
j1_h        = 40;    // mm Höhe J1-Flansch

// Kabeldurchführung
cable_r     = 5;     // mm Radius Kabelkanal (ESP32-Kabel durch Gelenk)

// Schraubenlöcher (Flansch → Körper, M3)
screw_r     = 1.6;   // mm
screw_ring  = 28;    // mm Teilkreisradius der M3-Schrauben

// Fase / Übergang
fase        = 2.0;

// ── Hauptkörper ──────────────────────────────────────────────
module body_querschnitt(w, h, r=5) {
    // Abgerundetes Rechteck (Rumpf-Querschnitt)
    hull() {
        for (x = [-w/2+r, w/2-r])
        for (z = [-h/2+r, h/2-r])
            translate([x, 0, z]) circle(r=r, $fn=24);
    }
}

module flansch() {
    difference() {
        union() {
            // ① Übergangs-Extrusion: Rumpf-Querschnitt → Zylinder
            //    Linearer Übergang über flange_len
            hull() {
                // Rumpf-Seite (vorne, -Y)
                translate([0, 0, 0])
                    linear_extrude(height=1)
                        body_querschnitt(body_w, body_h);

                // Zapfen-Seite (hinten, +Y)
                translate([0, flange_len-1, 0])
                    linear_extrude(height=1)
                        circle(r=flange_r, $fn=48);
            }

            // ② Zylindrischer Zapfen für J1-Aufnahme
            translate([0, flange_len, 0])
                cylinder(h=18, r=flange_r, $fn=48);
        }

        // ── Subtraktionen ────────────────────────────────────

        // Innenhohlraum (Wandstärke body_wall)
        translate([0, -1, 0])
            linear_extrude(height=flange_len+2)
                body_querschnitt(body_w - 2*body_wall,
                                 body_h - 2*body_wall, r=3);

        // Zapfen-Innenbohrung (Kabelkanal + Achsbohrung)
        translate([0, flange_len-1, 0])
            cylinder(h=22, r=cable_r, $fn=24);

        // M8-Achsen-Bohrung für J1 (quer, X-Richtung)
        translate([0, flange_len+9, 0])
            rotate([0, 90, 0])
                cylinder(h=flange_r*3, r=j1_bore_r, $fn=24, center=true);

        // M3-Schrauben-Kranz (Flansch → Körper, 6× gleichmäßig)
        for (i = [0:5])
            rotate([0, 0, i*60])
                translate([screw_ring, 0, 0])
                    rotate([90, 0, 0])
                        cylinder(h=flange_len+5, r=screw_r, $fn=16);

        // Kabelkanal längs (ESP32-Kabel, Ø10mm)
        translate([0, -2, body_h/2 - body_wall - cable_r])
            rotate([-90, 0, 0])
                cylinder(h=flange_len+20, r=cable_r, $fn=24);
    }
}

// ── Render ───────────────────────────────────────────────────
flansch();

// ── Info ─────────────────────────────────────────────────────
echo("=== body_to_j1_flange.scad ===");
echo(str("Rumpf-Querschnitt: ", body_w, "×", body_h, "mm"));
echo(str("Zapfen-Radius:     ", flange_r, "mm (passt zu tail_link_j1.stl)"));
echo(str("M8-Achsbohrung:    Ø", j1_bore_r*2, "mm (quer, für Gelenk J1)"));
echo(str("Kabelkanal:        Ø", cable_r*2, "mm längs + quer"));
echo(str("M3-Schrauben:      6× auf Ø", screw_ring*2, "mm Teilkreis"));
echo("");
echo("Fusion 360 Workflow:");
echo("  1. OpenSCAD: F6 → Export als STL");
echo("  2. Fusion: Insert → Insert Mesh → body_to_j1_flange.stl");
echo("  3. Hai-Körper (nach Shell) an -Y-Fläche ausrichten");
echo("  4. Modify → Combine → Join");
echo("  5. File → Export → STEP (.step)");
