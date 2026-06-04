// Biomimetic Shark Robot — Hauptelektronikgehäuse (Vorderteil)
// Material: PETG, 3D-Druck
// Parameter: 200mm Länge, Ø80mm, 3mm Wandstärke

$fn = 64;

// Parameter
length = 200;
outer_r = 40;
wall = 3;
oring_r = 3;
oring_depth = 2;
cable_hole_d = 8;

module main_body() {
    difference() {
        union() {
            cylinder(h=length-20, r=outer_r, $fn=$fn);
            translate([0, 0, length-20])
                sphere(r=outer_r, $fn=$fn);
        }
        union() {
            cylinder(h=length-wall-20, r=outer_r-wall, $fn=$fn);
            translate([0, 0, length-20])
                sphere(r=outer_r-wall, $fn=$fn);
        }
    }
}

module oring_groove() {
    rotate_extrude(angle=360, $fn=$fn)
        translate([outer_r - oring_r/2, wall + oring_depth/2])
            circle(r=oring_r/2, $fn=16);
}

module cable_port() {
    translate([outer_r-4, 0, 30])
        rotate([0, 90, 0])
            cylinder(h=10, r=cable_hole_d/2, $fn=16);
}

main_body();
oring_groove();
cable_port();
