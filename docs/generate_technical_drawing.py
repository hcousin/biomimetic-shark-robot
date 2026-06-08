#!/usr/bin/env python3
"""
Biomimetic Shark Robot — Technische Zeichnung (SVG Generator)
Erzeugt vollständige Konstruktionszeichnung mit:
  - Seitenriss (Side Elevation)
  - Draufsicht (Top View)
  - Querschnitt Rumpf (Cross-Section)
  - Detailansicht Nockenwelle
  - Komponenten-Legende
  - Massblatt / Bemaßung
"""

import math

W, H = 1200, 900
lines = []

def a(s): lines.append(s)

def line(x1,y1,x2,y2,stroke='#222',sw=0.8,dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    a(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

def path(d,stroke='#222',sw=1,fill='none',dash=''):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    a(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}"{da}/>')

def txt(x,y,t,sz=10,col='#111',anchor='middle',weight='normal',dy=0):
    dy_s = f' dy="{dy}"' if dy else ''
    a(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{sz}" fill="{col}" font-weight="{weight}" font-family="monospace"{dy_s}>{t}</text>')

def dim_horiz(x1,x2,y,label,col='#555',ext=15):
    """Horizontale Bemaßungslinie"""
    line(x1,y-ext,x1,y+2,col,0.5,'3,2')
    line(x2,y-ext,x2,y+2,col,0.5,'3,2')
    line(x1,y-ext+5,x2,y-ext+5,col,0.6)
    # Pfeilspitzen
    a(f'<polygon points="{x1},{y-ext+5} {x1+6},{y-ext+2} {x1+6},{y-ext+8}" fill="{col}"/>')
    a(f'<polygon points="{x2},{y-ext+5} {x2-6},{y-ext+2} {x2-6},{y-ext+8}" fill="{col}"/>')
    txt((x1+x2)/2, y-ext-2, label, 9, col)

def dim_vert(x,y1,y2,label,col='#555',ext=15):
    """Vertikale Bemaßungslinie"""
    line(x-2,y1,x+ext,y1,col,0.5,'3,2')
    line(x-2,y2,x+ext,y2,col,0.5,'3,2')
    line(x+ext-5,y1,x+ext-5,y2,col,0.6)
    a(f'<polygon points="{x+ext-5},{y1} {x+ext-2},{y1+6} {x+ext-8},{y1+6}" fill="{col}"/>')
    a(f'<polygon points="{x+ext-5},{y2} {x+ext-2},{y2-6} {x+ext-8},{y2-6}" fill="{col}"/>')
    txt(x+ext+8, (y1+y2)/2, label, 9, col, 'start')

def leader(x1,y1,x2,y2,label,side='right',col='#334',sz=9):
    line(x1,y1,x2,y2,'#888',0.5)
    a(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="2" fill="#888"/>')
    anchor = 'start' if side=='right' else 'end'
    txt(x2+(5 if side=='right' else -5), y2+3, label, sz, col, anchor)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
a(f'<?xml version="1.0" encoding="UTF-8"?>')
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a(f'<rect width="{W}" height="{H}" fill="white"/>')
# Rahmen
a(f'<rect x="10" y="10" width="{W-20}" height="{H-20}" fill="none" stroke="#222" stroke-width="1.5"/>')
a(f'<rect x="15" y="15" width="{W-30}" height="{H-30}" fill="none" stroke="#aaa" stroke-width="0.5"/>')

# Schriftfeld (Titelblock unten rechts)
a(f'<rect x="{W-420}" y="{H-75}" width="410" height="65" fill="#f5f5f3" stroke="#555" stroke-width="0.8"/>')
line(W-420, H-50, W-10, H-50, '#555', 0.5)
line(W-280, H-75, W-280, H-10, '#555', 0.5)
line(W-140, H-75, W-140, H-10, '#555', 0.5)
txt(W-210, H-60, 'Biomimetic Shark Robot', 11, '#111', 'middle', 'bold')
txt(W-210, H-42, 'Konstruktionszeichnung Rev.1.0', 9, '#444', 'middle')
txt(W-210, H-26, 'Länge: 600mm | Ø80mm | 4 Gelenke', 8, '#666', 'middle')
txt(W-350, H-60, 'Erstellt:', 8, '#666', 'start')
txt(W-350, H-45, '2026-06', 9, '#333', 'start')
txt(W-350, H-30, 'hcousin', 9, '#333', 'start')
txt(W-75, H-60, 'Massstab', 8, '#666', 'middle')
txt(W-75, H-45, '1:3', 10, '#111', 'middle', 'bold')
txt(W-75, H-28, 'Einheit: mm', 8, '#666', 'middle')

# Titel oben
txt(W//2, 35, 'BIOMIMETISCHER HAIFISCH-ROBOTER — VOLLSTÄNDIGE TECHNISCHE ZEICHNUNG', 13, '#111', 'middle', 'bold')

# ─────────────────────────────────────────────────────────────────────────────
# SEITENRISS (SIDE ELEVATION)  — y_center = 180
# ─────────────────────────────────────────────────────────────────────────────
txt(30, 58, 'A — SEITENRISS (1:3)', 10, '#333', 'start', 'bold')
line(30, 62, 750, 62, '#bbb', 0.4)

CY = 185    # Zentralachse y
SC = 0.333  # Massstab: 1px = 3mm
# Roboter: 600mm lang → 200px; Ø80mm → 26px halber Durchmesser

# Helfer: mm → px (ab linkem Rand x0=50)
X0 = 50
def mx(mm): return X0 + mm * SC
def my(mm): return CY + mm * SC

# Achsenlinie (gestrichelt)
line(X0-10, CY, mx(650), CY, '#aaa', 0.5, '6,3')

# ── Rumpf-Silhouette ──
# Nase: Parabolische Spitze von x=0 bis x=80mm
nose_pts = []
for i in range(20):
    t = i / 19
    xn = mx(t * 80)
    yn_top = CY - (13.3 * (t**0.5)) * SC * 3
    nose_pts.append((xn, yn_top))
nose_path_top = 'M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x,y in nose_pts)

nose_bot = []
for i in range(20):
    t = i / 19
    xn = mx(t * 80)
    yn_bot = CY + (13.3 * (t**0.5)) * SC * 3
    nose_bot.append((xn, yn_bot))
nose_path_bot = ' '.join(f'L {x:.1f},{y:.1f}' for x,y in reversed(nose_bot))

# Hauptkörper: x=80–380mm, Ø=80mm → r=26.7px
r_body = 80/2 * SC
# Peduncle: x=380–480mm, verjüngt von r=26.7 auf r=15
# Schwanzwurzel: x=480–600mm

# Vollständiger Körperumriss als Path
body_d = f'M {mx(0):.1f},{CY:.1f}'
body_d += ' ' + nose_path_top[2:]  # Nase oben
body_d += f' L {mx(380):.1f},{CY-r_body:.1f}'  # Rücken gerade
# Schwanzansatz (verjüngt)
body_d += f' C {mx(440):.1f},{CY-r_body:.1f} {mx(480):.1f},{CY-r_body*0.55:.1f} {mx(510):.1f},{CY-r_body*0.45:.1f}'
# Schwanzflosse oben
body_d += f' L {mx(570):.1f},{CY-r_body*1.6:.1f}'
body_d += f' C {mx(595):.1f},{CY-r_body*1.9:.1f} {mx(610):.1f},{CY-r_body*0.5:.1f} {mx(580):.1f},{CY:.1f}'
body_d += f' C {mx(610):.1f},{CY+r_body*0.5:.1f} {mx(595):.1f},{CY+r_body*1.9:.1f} {mx(570):.1f},{CY+r_body*1.6:.1f}'
# Bauch Schwanz
body_d += f' L {mx(510):.1f},{CY+r_body*0.45:.1f}'
body_d += f' C {mx(480):.1f},{CY+r_body*0.55:.1f} {mx(440):.1f},{CY+r_body:.1f} {mx(380):.1f},{CY+r_body:.1f}'
body_d += f' L {mx(80):.1f},{CY+r_body:.1f}'
body_d += ' ' + nose_path_bot + ' Z'

path(body_d, '#334', 1.2, '#ECF3FA')

# Haut-Textur (subtile Linie entlang Rücken)
path(f'M {mx(80):.1f},{CY-r_body:.1f} L {mx(380):.1f},{CY-r_body:.1f}', '#7aabcc', 0.4)

# ── Rückenflosse ──
rf_x = mx(220); rf_y = CY - r_body
rf_d = f'M {rf_x:.1f},{rf_y:.1f} C {mx(200):.1f},{CY-r_body-36:.1f} {mx(240):.1f},{CY-r_body-40:.1f} {mx(290):.1f},{CY-r_body-18:.1f} L {mx(310):.1f},{rf_y:.1f} Z'
path(rf_d, '#334', 1, '#D0E4F0')

# ── Brustflossen ──
pf_x = mx(145); pf_y = CY
# Links (sichtbar von oben): Brustflosse als NACA-Profil-Silhouette
bf_d = f'M {pf_x:.1f},{CY-r_body:.1f} C {pf_x-18:.1f},{CY-r_body-22:.1f} {pf_x+15:.1f},{CY-r_body-32:.1f} {pf_x+30:.1f},{CY-r_body-8:.1f} L {pf_x+15:.1f},{CY-r_body:.1f} Z'
path(bf_d, '#334', 0.8, '#C8DCEA')

# ── Gelenk-Segmente sichtbar machen ──
joint_colors = ['#E8F4FC','#D5EAF7','#C0DEF0','#A8CEEA']
joint_xmm = [380, 420, 460, 500]
joint_w = 35
for i,jx in enumerate(joint_xmm):
    rx = mx(jx); rw = joint_w * SC
    rh = (r_body * 0.9 - i * r_body*0.07) * 2
    ry = CY - rh/2
    a(f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" rx="2" fill="{joint_colors[i]}" stroke="#556" stroke-width="0.6"/>')

# Gelenk-Achsen (Punkte)
for jx in joint_xmm:
    a(f'<circle cx="{mx(jx+joint_w/2):.1f}" cy="{CY:.1f}" r="2.5" fill="#334"/>')
    a(f'<circle cx="{mx(jx+joint_w/2):.1f}" cy="{CY:.1f}" r="1" fill="white"/>')

# ── Interne Baugruppen (gestrichelt) ──
# Elektronik-Sektion: 0–280mm
a(f'<rect x="{mx(15):.1f}" y="{CY-r_body+3:.1f}" width="{mx(265)-mx(0):.1f}" height="{(r_body-3)*2:.1f}" rx="3" fill="none" stroke="#2266aa" stroke-width="0.7" stroke-dasharray="4,2"/>')
txt(mx(140), CY-r_body+14, 'Elektronik + Akku', 8, '#2266aa', 'middle')

# Nockenwelle/Motor: 20–140mm
a(f'<rect x="{mx(20):.1f}" y="{CY-8:.1f}" width="{mx(130)-mx(20):.1f}" height="16" rx="2" fill="#FFF0DD" stroke="#CC6600" stroke-width="0.7"/>')
txt(mx(75), CY+3, 'Motor + Nocke', 7, '#884400', 'middle')

# Ballast: 280–360mm
a(f'<rect x="{mx(285):.1f}" y="{CY-9:.1f}" width="{mx(72)-1:.1f}" height="18" rx="2" fill="#E0FFE8" stroke="#226622" stroke-width="0.7"/>')
txt(mx(321), CY+3.5, 'Ballast', 7, '#115511', 'middle')

# ── Bemaßungen Seitenriss ──
dim_horiz(X0, mx(600), CY+r_body+20, '600 mm (Gesamtlänge)', '#555', 25)
dim_horiz(X0, mx(380), CY+r_body+40, '380 mm (Rumpf)', '#777', 45)
dim_vert(mx(600)+5, CY-r_body, CY+r_body, 'Ø 80', '#555', 20)
dim_vert(mx(570)+5, CY-r_body*1.6, CY+r_body*1.6, '100', '#777', 35)

# ── Leader Labels ──
leader(pf_x+10, CY-r_body-20, pf_x-25, CY-r_body-45, 'Brustflosse (NACA0010)', 'left', '#334', 8)
leader(mx(255), CY-r_body-30, mx(255)+5, CY-r_body-55, 'Rückenflosse', 'right', '#334', 8)
leader(mx(580), CY-r_body*1.4, mx(640), CY-r_body*1.2, 'Schwanzflosse (lunate)', 'right', '#334', 8)
leader(mx(75), CY-8, mx(20), CY-35, 'BL-Motor KV=900', 'left', '#334', 8)
leader(mx(321), CY-9, mx(321), CY-38, 'Ballast 20ml', 'right', '#334', 8)

# Gelenk-Labels
for i,jx in enumerate(joint_xmm):
    txt(mx(jx+joint_w/2), CY-r_body*0.9+i*r_body*0.07-8, f'J{i+1}', 8, '#445566', 'middle')

# ─────────────────────────────────────────────────────────────────────────────
# DRAUFSICHT (TOP VIEW) — y_center = 390
# ─────────────────────────────────────────────────────────────────────────────
TY = 390   # Zentrum Draufsicht
txt(30, 290, 'B — DRAUFSICHT (1:3)', 10, '#333', 'start', 'bold')
line(30, 294, 750, 294, '#bbb', 0.4)

# Achsenlinie
line(X0-10, TY, mx(650), TY, '#aaa', 0.5, '6,3')

# Rumpf (oben gesehen — Ellipse)
top_d = f'M {mx(0):.1f},{TY:.1f}'
# Nase
for i in range(20):
    t = i/19
    xn = mx(t*80)
    wn = 26.7 * (t**0.5) * SC
    top_d += f' L {xn:.1f},{TY-wn:.1f}'
top_d += f' L {mx(380):.1f},{TY-r_body:.1f}'
# Peduncle
top_d += f' C {mx(440):.1f},{TY-r_body:.1f} {mx(490):.1f},{TY-8:.1f} {mx(510):.1f},{TY-7:.1f}'
# Schwanzflosse links
top_d += f' C {mx(540):.1f},{TY-7:.1f} {mx(570):.1f},{TY-r_body*1.5:.1f} {mx(598):.1f},{TY-r_body*0.3:.1f}'
top_d += f' L {mx(600):.1f},{TY:.1f}'
# Rechte Seite gespiegelt
top_d += f' L {mx(598):.1f},{TY+r_body*0.3:.1f}'
top_d += f' C {mx(570):.1f},{TY+r_body*1.5:.1f} {mx(540):.1f},{TY+7:.1f} {mx(510):.1f},{TY+7:.1f}'
top_d += f' C {mx(490):.1f},{TY+8:.1f} {mx(440):.1f},{TY+r_body:.1f} {mx(380):.1f},{TY+r_body:.1f}'
top_d += f' L {mx(80):.1f},{TY+r_body:.1f}'
for i in range(20):
    t = (19-i)/19
    xn = mx(t*80)
    wn = 26.7 * (t**0.5) * SC
    top_d += f' L {xn:.1f},{TY+wn:.1f}'
top_d += ' Z'
path(top_d, '#334', 1.2, '#ECF3FA')

# Brustflossen (Draufsicht — beide sichtbar)
for sign,lbl in [(-1,'Links'),( 1,'Rechts')]:
    bx = mx(120); by = TY + sign*r_body
    bfd = f'M {bx:.1f},{by:.1f} C {mx(100):.1f},{TY+sign*(r_body+25):.1f} {mx(155):.1f},{TY+sign*(r_body+32):.1f} {mx(175):.1f},{TY+sign*(r_body+10):.1f} L {mx(165):.1f},{by:.1f} Z'
    path(bfd, '#334', 0.8, '#C8DCEA')
    leader(mx(137), TY+sign*(r_body+16), mx(80), TY+sign*(r_body+30), f'Brustflosse {lbl}', 'left' if sign>0 else 'right', '#334', 7)

# Rückenflosse (Draufsicht — Linie)
line(mx(220), TY-r_body, mx(310), TY-r_body, '#334', 0.6, '2,2')

# Gelenke Draufsicht
for i,jx in enumerate(joint_xmm):
    jw = (joint_w-i*2)*SC
    jd = (r_body*0.88 - i*r_body*0.07)*2
    ry = TY - jd/2
    a(f'<rect x="{mx(jx):.1f}" y="{ry:.1f}" width="{jw:.1f}" height="{jd:.1f}" rx="1" fill="{joint_colors[i]}" stroke="#556" stroke-width="0.5"/>')

# Schwimmwellen andeuten
for phase in [0, 90, 180, 270]:
    xw = joint_xmm[phase//90]
    amp = (r_body*0.4) * math.sin(math.radians(phase+45))
    a(f'<circle cx="{mx(xw+joint_w/2):.1f}" cy="{TY+amp:.1f}" r="1.5" fill="#99BBDD" opacity="0.7"/>')

# ─────────────────────────────────────────────────────────────────────────────
# QUERSCHNITT RUMPF A-A — rechts oben, x_center=900
# ─────────────────────────────────────────────────────────────────────────────
QX = 900; QY = 175; QR = 70
txt(790, 58, 'C — QUERSCHNITT A-A (1:2)', 10, '#333', 'start', 'bold')
line(790, 62, 1170, 62, '#bbb', 0.4)

# Schnittlinie in Seitenriss
line(mx(100), CY-r_body-35, mx(100), CY+r_body+15, '#CC3333', 0.8, '5,3')
txt(mx(100), CY+r_body+22, 'A–A', 8, '#CC3333', 'middle')

# Aussenring
a(f'<circle cx="{QX}" cy="{QY}" r="{QR}" fill="#EDF6FC" stroke="#334" stroke-width="1.5"/>')
# Wandstärke
a(f'<circle cx="{QX}" cy="{QY}" r="{QR-10}" fill="white" stroke="#556" stroke-width="0.5"/>')

# Innenkomponenten
# ESP32 PCB
a(f'<rect x="{QX-28}" y="{QY-18}" width="56" height="36" rx="3" fill="#E8F0FF" stroke="#2255CC" stroke-width="0.8"/>')
txt(QX, QY-4, 'ESP32', 8, '#2255CC', 'middle')
txt(QX, QY+8, 'PCB', 7, '#2255CC', 'middle')

# Akku (links)
a(f'<rect x="{QX-58}" y="{QY-15}" width="24" height="30" rx="2" fill="#FFF3CC" stroke="#BB8800" stroke-width="0.8"/>')
txt(QX-46, QY+4, 'BAT', 7, '#885500', 'middle')

# Motor/Nocke (Kreis)
a(f'<circle cx="{QX+42}" cy="{QY}" r="12" fill="#FFE8CC" stroke="#CC5500" stroke-width="0.8"/>')
txt(QX+42, QY+4, 'M', 8, '#884400', 'middle')

# O-Ring
a(f'<circle cx="{QX}" cy="{QY}" r="{QR-1}" fill="none" stroke="#CC3333" stroke-width="2.5" stroke-dasharray="3,4" opacity="0.5"/>')
txt(QX+QR+12, QY-12, 'O-Ring', 7, '#CC3333', 'start')
line(QX+QR-2, QY-8, QX+QR+10, QY-14, '#CC3333', 0.5)

# Wandstärke bemaßen
line(QX-QR-20, QY, QX-QR-5, QY, '#555', 0.5,'3,2')
line(QX-QR+10, QY, QX-QR+25, QY, '#555', 0.5,'3,2')
txt(QX-QR-22, QY-4, '3', 8, '#555', 'end')
txt(QX-QR-22, QY+8, 'mm', 7, '#777', 'end')

# Durchmesser-Bemaßung
line(QX, QY-QR-25, QX, QY+QR+5, '#555', 0.5, '3,2')
txt(QX+5, QY-QR-10, 'Ø80', 9, '#555', 'start')

# ─────────────────────────────────────────────────────────────────────────────
# DETAIL NOCKENWELLE — rechts mitte
# ─────────────────────────────────────────────────────────────────────────────
NX = 900; NY = 390
txt(790, 290, 'D — DETAIL NOCKENWELLE (1:1)', 10, '#333', 'start', 'bold')
line(790, 294, 1170, 294, '#bbb', 0.4)

# Welle (120mm × Ø12mm)
# Maßstab 1:1 → 120mm = 120px, Ø12 = 12px
NW = 120; ND = 12; NE = 3  # Länge, Durchmesser, Exzentrizität
line(NX-70, NY, NX+70, NY, '#aaa', 0.3, '4,2')  # Achslinie

# Hauptkörper Welle
a(f'<rect x="{NX-NW//2}" y="{NY-ND//2}" width="{NW}" height="{ND}" rx="2" fill="#E8F0F8" stroke="#334" stroke-width="1"/>')

# Exzentrische Nocken-Profile (4 Positionen)
nocke_positions = [20, 45, 75, 100]  # x-Positionen auf Welle
phase_angles = [0, 90, 180, 270]
ncols = ['#C0D8F0', '#A8C8E8', '#90B8E0', '#78A8D8']
for xi, angle, col in zip(nocke_positions, phase_angles, ncols):
    cx = NX - NW//2 + xi
    cy = NY
    # Exzentrische Scheibe
    offset = NE * math.cos(math.radians(angle))
    a(f'<ellipse cx="{cx:.1f}" cy="{cy+offset:.1f}" rx="8" ry="5" fill="{col}" stroke="#445" stroke-width="0.8" opacity="0.9"/>')
    # Gleitschuh
    gx = cx; gy = cy + NE + 5 + abs(math.cos(math.radians(angle)))*2
    a(f'<rect x="{gx-5:.1f}" y="{gy:.1f}" width="10" height="6" rx="1" fill="#FFE0A0" stroke="#886600" stroke-width="0.7"/>')
    # Schubstange
    line(gx, gy, gx, gy+18, '#334', 0.8)
    # Gelenk unten
    a(f'<circle cx="{gx:.1f}" cy="{gy+18:.1f}" r="3" fill="white" stroke="#334" stroke-width="0.8"/>')
    txt(gx, gy+35, f'J{phase_angles.index(angle)+1}\n{angle}°', 7, '#334', 'middle')

# Bemaßungen Nockenwelle
line(NX-NW//2, NY+22, NX+NW//2, NY+22, '#555', 0.6)
a(f'<polygon points="{NX-NW//2},{NY+22} {NX-NW//2+5},{NY+19} {NX-NW//2+5},{NY+25}" fill="#555"/>')
a(f'<polygon points="{NX+NW//2},{NY+22} {NX+NW//2-5},{NY+19} {NX+NW//2-5},{NY+25}" fill="#555"/>')
txt(NX, NY+32, '120 mm', 8, '#555', 'middle')
txt(NX-NW//2-18, NY+3, 'e=3mm', 7, '#CC5500', 'end')
txt(NX-NW//2-18, NY-3, 'R₀=8mm', 7, '#2255CC', 'end')

# ─────────────────────────────────────────────────────────────────────────────
# LEGENDE / KOMPONENTENLISTE — rechts unten
# ─────────────────────────────────────────────────────────────────────────────
LX = 800; LY = 500
txt(LX-10, LY-15, 'E — KOMPONENTENLISTE', 10, '#333', 'start', 'bold')
line(LX-10, LY-11, 1175, LY-11, '#bbb', 0.4)
a(f'<rect x="{LX-10}" y="{LY}" width="375" height="310" fill="#FAFAF8" stroke="#CCC" stroke-width="0.5"/>')

headers = ['Nr.', 'Bezeichnung', 'Material / Typ', 'Menge']
hx = [LX, LX+30, LX+175, LX+330]
for i,(h,x) in enumerate(zip(headers, hx)):
    txt(x+2, LY+14, h, 8, '#444', 'start', 'bold')
line(LX-10, LY+18, LX+365, LY+18, '#CCC', 0.5)

components = [
    ('1','Hauptgehäuse','PETG 3D-Druck','1'),
    ('2','Elektronik-Deckel','PETG + O-Ring','2'),
    ('3','Brushless Motor','KV=900, 20W','1'),
    ('4','Nockenwelle','Edelstahl 1.4104','1'),
    ('5','Gelenk J1-J4','PETG 50% Infill','4'),
    ('6','Passivgelenk J4','TPU 95A','1'),
    ('7','Schwanzflosse','Silikon DS10+CFK','1'),
    ('8','Brustflossen','Silikon DS10 Slow','2'),
    ('9','Rückenflosse','PLA+ (dekorativ)','1'),
    ('10','Kugellager 626-ZZ','Ø6/19/6mm','8'),
    ('11','ESP32 DevKit','WiFi/BT, 240MHz','1'),
    ('12','MS5837-30BA','Tiefensensor 0x76','1'),
    ('13','MPU-6050','IMU 6-DOF 0x68','1'),
    ('14','PCA9685','I2C Servo Driver','1'),
    ('15','ESC 20A','Hobbywing + BEC','1'),
    ('16','LiPo 3S','11.1V 2200mAh','1'),
    ('17','Ballast','Spritze 20ml','1'),
]
for i,row in enumerate(components):
    yy = LY + 28 + i*17
    bg = '#F5F5F3' if i%2==0 else 'white'
    a(f'<rect x="{LX-10}" y="{yy-10}" width="375" height="17" fill="{bg}"/>')
    for val,x in zip(row, hx):
        txt(x+2, yy+1, val, 8, '#222', 'start')

a('</svg>')

out = '/home/claude/shark/docs/technical_drawing.svg'
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f"✓ {out}")
print(f"  Größe: {len('\n'.join(lines))//1024} KB, {len(lines)} Elemente")
