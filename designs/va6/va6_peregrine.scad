// VA-6 "Peregrine" Interceptor Drone
// Based on P1-SUN photo reference
// Dimensions in mm
// Bomb/torpedo fuselage, large cruciform fins, motor pods at fin tips

// === DESIGN PARAMETERS ===

// Fuselage - fat torpedo/bomb shape (ratio ~1:4.5)
fuse_length     = 650;
fuse_max_dia    = 140;
fuse_max_r      = fuse_max_dia / 2;

// Nose - blunt ogive (mortar-round shape)
nose_length     = 100;
nose_tip_r      = 25;

// Tail taper
tail_taper_len  = 120;
tail_end_r      = 35;

// Main body (between nose and tail taper)
body_length     = fuse_length - nose_length - tail_taper_len;

// Cruciform fins - large flat rectangular plates
fin_span        = 160;    // each fin extends this far from fuselage surface
fin_chord       = 180;    // long chord along flight axis
fin_thickness   = 8;

// Fin position (aft portion of fuselage)
fin_z_start     = fuse_length - tail_taper_len - fin_chord + 30;

// Motor pods - cylindrical nacelles at each fin tip
pod_length      = 120;    // extends forward and aft of fin
pod_dia         = 38;
pod_r           = pod_dia / 2;

// Props
prop_dia        = 150;    // 6 inch

// === MODULES ===

// Blunt ogive nose
module nose() {
    // Tip dome
    sphere(r=nose_tip_r, $fn=32);

    // Taper from tip to full body diameter
    cylinder(h=nose_length, r1=nose_tip_r, r2=fuse_max_r, $fn=48);
}

// Main cylindrical body
module body() {
    translate([0, 0, nose_length])
        cylinder(h=body_length, r=fuse_max_r, $fn=48);
}

// Tail taper
module tail() {
    translate([0, 0, fuse_length - tail_taper_len])
        cylinder(h=tail_taper_len, r1=fuse_max_r, r2=tail_end_r, $fn=48);
}

// Single rectangular fin plate
module fin() {
    translate([fuse_max_r - 2, -fin_thickness/2, fin_z_start])
        cube([fin_span + 2, fin_thickness, fin_chord]);
}

// Motor pod (nacelle) at fin tip
module motor_pod() {
    pod_x = fuse_max_r + fin_span;
    pod_z = fin_z_start + fin_chord/2;

    translate([pod_x, 0, pod_z])
        rotate([0, 0, 0])
            cylinder(h=pod_length, r=pod_r, center=true, $fn=24);
}

// Prop disk at front of motor pod
module prop(front) {
    pod_x = fuse_max_r + fin_span;
    pod_z = fin_z_start + fin_chord/2;
    offset = front ? pod_length/2 : -pod_length/2;

    translate([pod_x, 0, pod_z + offset])
        cylinder(h=2, r=prop_dia/2, center=true, $fn=24);
}

// === ASSEMBLY ===

union() {
    // Fuselage
    nose();
    body();
    tail();

    // Cruciform fins (4x at 90 degrees)
    rotate([0, 0, 0])   fin();
    rotate([0, 0, 90])  fin();
    rotate([0, 0, 180]) fin();
    rotate([0, 0, 270]) fin();

    // Motor pods at fin tips (4x)
    rotate([0, 0, 0])   motor_pod();
    rotate([0, 0, 90])  motor_pod();
    rotate([0, 0, 180]) motor_pod();
    rotate([0, 0, 270]) motor_pod();

    // Prop disks - front
    rotate([0, 0, 0])   prop(true);
    rotate([0, 0, 90])  prop(true);
    rotate([0, 0, 180]) prop(true);
    rotate([0, 0, 270]) prop(true);

    // Prop disks - rear
    rotate([0, 0, 0])   prop(false);
    rotate([0, 0, 90])  prop(false);
    rotate([0, 0, 180]) prop(false);
    rotate([0, 0, 270]) prop(false);
}

// === SPECS ===
// Overall length: 650mm
// Max fuselage diameter: 140mm
// Cruciform fin span (tip-to-tip): ~460mm
// Fin chord: 180mm
// Motor pod length: 120mm
// Motor pod diameter: 38mm
// Prop diameter: 150mm (6")
// MTOW: 3.2-4.0 kg
// Payload (warhead): 0.8 kg
