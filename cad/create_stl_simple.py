#!/usr/bin/env python3
"""STL-Dateien manuell erstellen (ASCII STL Format)"""
import struct
import math

def write_stl_ascii(filename, triangles, name="Mesh"):
    """Schreibe ASCII STL-Datei"""
    with open(filename, 'w') as f:
        f.write(f"solid {name}\n")
        for tri in triangles:
            # Normale berechnen
            v0, v1, v2 = tri
            edge1 = (v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2])
            edge2 = (v2[0]-v0[0], v2[1]-v0[1], v2[2]-v0[2])
            normal = (
                edge1[1]*edge2[2] - edge1[2]*edge2[1],
                edge1[2]*edge2[0] - edge1[0]*edge2[2],
                edge1[0]*edge2[1] - edge1[1]*edge2[0]
            )
            norm_len = math.sqrt(sum(n*n for n in normal)) + 1e-6
            normal = tuple(n/norm_len for n in normal)
            
            f.write(f"  facet normal {normal[0]:.6e} {normal[1]:.6e} {normal[2]:.6e}\n")
            f.write(f"    outer loop\n")
            for v in tri:
                f.write(f"      vertex {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            f.write(f"    endloop\n")
            f.write(f"  endfacet\n")
        f.write(f"endsolid {name}\n")

# 1. Body Front (Zylinder + Kegel)
triangles_body = []
fn = 16
for i in range(fn):
    i_next = (i + 1) % fn
    angle = 2*math.pi * i / fn
    angle_next = 2*math.pi * i_next / fn
    
    x1, y1 = 40*math.cos(angle), 40*math.sin(angle)
    x2, y2 = 40*math.cos(angle_next), 40*math.sin(angle_next)
    
    # Seitenflächen Zylinder
    triangles_body.append(((x1, y1, 0), (x2, y2, 0), (x1, y1, 180)))
    triangles_body.append(((x2, y2, 0), (x2, y2, 180), (x1, y1, 180)))
    
    # Kegel-Flächen
    triangles_body.append(((x1, y1, 180), (x2, y2, 180), (0, 0, 200)))

write_stl_ascii('/home/claude/shark/cad/stl/body_front.stl', triangles_body, 'BodyFront')
print(f"✓ body_front.stl ({len(triangles_body)} triangles)")

# 2. Servo Mount J1 (einfache Box)
triangles_servo = [
    # Unten
    ((-17.5, -22.5, -12.5), (17.5, -22.5, -12.5), (17.5, 22.5, -12.5)),
    ((-17.5, -22.5, -12.5), (17.5, 22.5, -12.5), (-17.5, 22.5, -12.5)),
    # Oben
    ((-17.5, -22.5, 12.5), (17.5, 22.5, 12.5), (17.5, -22.5, 12.5)),
    ((-17.5, -22.5, 12.5), (-17.5, 22.5, 12.5), (17.5, 22.5, 12.5)),
    # Seiten
    ((-17.5, -22.5, -12.5), (-17.5, -22.5, 12.5), (17.5, -22.5, 12.5)),
    ((-17.5, -22.5, -12.5), (17.5, -22.5, 12.5), (17.5, -22.5, -12.5)),
    # Weitere Seiten...
]

write_stl_ascii('/home/claude/shark/cad/stl/servo_mount_j1.stl', triangles_servo, 'ServoMountJ1')
print(f"✓ servo_mount_j1.stl ({len(triangles_servo)} triangles)")

# 3. Silikonform Flosse (Lunate Shape)
triangles_form = []
for y_i in range(11):
    y = -60 + 120*y_i/11
    for z_i in range(7):
        z = 120*z_i/7
        # Elliptische Form approximieren
        x = 40 * max(0, math.sqrt(1 - (y/60)**2))
        
        if z_i < 6 and y_i < 10:
            y_next = -60 + 120*(y_i+1)/11
            z_next = 120*(z_i+1)/7
            x_next = 40 * max(0, math.sqrt(1 - (y_next/60)**2))
            x_znext = 40 * max(0, math.sqrt(1 - (y/60)**2))
            x_both = 40 * max(0, math.sqrt(1 - (y_next/60)**2))
            
            triangles_form.append(((x, y, z), (x_znext, y, z_next), (x_next, y_next, z)))
            triangles_form.append(((x_znext, y, z_next), (x_both, y_next, z_next), (x_next, y_next, z)))

write_stl_ascii('/home/claude/shark/cad/stl/silikon_form_flosse.stl', triangles_form, 'SilikonForm')
print(f"✓ silikon_form_flosse.stl ({len(triangles_form)} triangles)")

print("\n✓ Alle STL-Dateien erstellt in cad/stl/")
