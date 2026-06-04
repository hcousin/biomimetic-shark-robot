import math

def write_stl(filename, triangles, name="Mesh"):
    with open(filename, 'w') as f:
        f.write(f"solid {name}\n")
        for tri in triangles:
            v0, v1, v2 = tri
            e1 = (v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2])
            e2 = (v2[0]-v0[0], v2[1]-v0[1], v2[2]-v0[2])
            n = (e1[1]*e2[2]-e1[2]*e2[1], e1[2]*e2[0]-e1[0]*e2[2], e1[0]*e2[1]-e1[1]*e2[0])
            L = math.sqrt(sum(x*x for x in n)) + 1e-10
            n = tuple(x/L for x in n)
            f.write(f"  facet normal {n[0]:.6e} {n[1]:.6e} {n[2]:.6e}\n    outer loop\n")
            for v in tri: f.write(f"      vertex {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            f.write("    endloop\n  endfacet\n")
        f.write(f"endsolid {name}\n")

def box(x1,y1,z1,x2,y2,z2):
    return [
        ((x1,y1,z1),(x2,y1,z1),(x2,y2,z1)), ((x1,y1,z1),(x2,y2,z1),(x1,y2,z1)),
        ((x1,y1,z2),(x2,y2,z2),(x2,y1,z2)), ((x1,y1,z2),(x1,y2,z2),(x2,y2,z2)),
        ((x1,y1,z1),(x1,y1,z2),(x2,y1,z2)), ((x1,y1,z1),(x2,y1,z2),(x2,y1,z1)),
        ((x1,y2,z1),(x2,y2,z2),(x1,y2,z2)), ((x1,y2,z1),(x2,y2,z1),(x2,y2,z2)),
        ((x1,y1,z1),(x1,y2,z2),(x1,y1,z2)), ((x1,y1,z1),(x1,y2,z1),(x1,y2,z2)),
        ((x2,y1,z1),(x2,y1,z2),(x2,y2,z2)), ((x2,y1,z1),(x2,y2,z2),(x2,y2,z1)),
    ]

def cyl(r, h, fn=16):
    tris = []
    for i in range(fn):
        a1, a2 = 2*math.pi*i/fn, 2*math.pi*(i+1)/fn
        x1,y1 = r*math.cos(a1), r*math.sin(a1)
        x2,y2 = r*math.cos(a2), r*math.sin(a2)
        tris.append(((x1,y1,0),(x2,y2,0),(0,0,0)))
        tris.append(((x1,y1,h),(x2,y2,h),(0,0,h)))
        tris.append(((x1,y1,0),(x1,y1,h),(x2,y2,h)))
        tris.append(((x1,y1,0),(x2,y2,h),(x2,y2,0)))
    return tris

# 1. Tail Link J2
tris = box(-12.5,-22,0,12.5,22,24)
write_stl('/home/claude/shark/cad/stl/tail_link_j2.stl', tris, 'TailLinkJ2')

# 2. Tail Link J3 (TPU passive)
tris = box(-10,-18,0,10,18,20)
write_stl('/home/claude/shark/cad/stl/tail_link_j3_passive.stl', tris, 'TailLinkJ3Passive')

# 3. Gleitschuh (Cam Follower)
tris = box(-6,-4,0,6,4,15)
write_stl('/home/claude/shark/cad/stl/cam_follower.stl', tris, 'CamFollower')

# 4. Motor Halter Flansch
tris = cyl(40, 8) + cyl(18, 12)
write_stl('/home/claude/shark/cad/stl/motor_mount_flange.stl', tris, 'MotorMount')

# 5. Ballast Zylinder Halter
tris = box(-15,-15,0,15,15,80)
for _ in range(8):
    tris += cyl(15, 80, fn=8)
write_stl('/home/claude/shark/cad/stl/ballast_syringe_holder.stl', tris[:80], 'BallastHolder')

# 6. Brustflosse Halter Links
tris = box(-5,-20,0,5,20,25)
write_stl('/home/claude/shark/cad/stl/pectoral_mount_left.stl', tris, 'PectoralMountLeft')

# 7. Brustflosse Halter Rechts
tris = box(-5,-20,0,5,20,25)
write_stl('/home/claude/shark/cad/stl/pectoral_mount_right.stl', tris, 'PectoralMountRight')

# 8. Rückenflosse (dekorativ)
tris = []
for i in range(12):
    x = 80*i/12
    x2 = 80*(i+1)/12
    h = 40*math.sin(math.pi*x/80)
    h2 = 40*math.sin(math.pi*x2/80)
    tris.append(((x,0,0),(x2,0,0),(x,0,h)))
    tris.append(((x2,0,0),(x2,0,h2),(x,0,h)))
write_stl('/home/claude/shark/cad/stl/dorsal_fin.stl', tris, 'DorsalFin')

# 9. Silikonform Body Lid
tris = cyl(40,8) + box(-3,-42,-5,3,42,10)
write_stl('/home/claude/shark/cad/stl/body_lid_oring.stl', tris[:50], 'BodyLidOring')

# 10. Schubstange (Crank Rod)
tris = cyl(3, 25, fn=8)
write_stl('/home/claude/shark/cad/stl/crank_rod.stl', tris, 'CrankRod')

import os
stls = [f for f in os.listdir('/home/claude/shark/cad/stl/') if f.endswith('.stl')]
print(f"✓ {len(stls)} STL-Dateien total:")
for s in sorted(stls): print(f"  {s}")
