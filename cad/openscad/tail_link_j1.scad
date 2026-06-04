// Tail Joint J1 — Peduncle Servo-Halter
// Material: PETG, 50% Infill

$fn = 32;

module servo_mount() {
    difference() {
        cube([35, 45, 25], center=true);
        cube([24, 23, 20], center=true);
    }
}

module bearing_pocket() {
    cylinder(h=8, r=14, $fn=$fn);
}

module shaft_hole() {
    cylinder(h=30, r=3.5, $fn=8);
}

union() {
    servo_mount();
    translate([-12, 0, 0]) bearing_pocket();
    translate([12, 0, 0]) bearing_pocket();
    shaft_hole();
}
