#!/usr/bin/env python3
"""
Erzeugt einen vollständigen KiCad-Stil Schaltplan als SVG.
Alle Verbindungen sind point-to-point verdrahtet.
Keine freischwebenden Drähte.
"""

W, H = 1400, 920

def svg_header():
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  text {{ font-family: monospace; }}
  .lbl  {{ font-size:11px; fill:#111; }}
  .pin  {{ font-size: 9px; fill:#333; }}
  .net  {{ font-size: 9px; fill:#003399; font-style:italic; }}
  .comp {{ fill:#EDF2FF; stroke:#2244AA; stroke-width:1.5; }}
  .pcomp{{ fill:#FFF3E0; stroke:#CC6600; stroke-width:1.5; }}
  .sens {{ fill:#E8F8F0; stroke:#1A7A40; stroke-width:1.5; }}
  .serv {{ fill:#FAF0FF; stroke:#773399; stroke-width:1.5; }}
  .mot  {{ fill:#FFF0E0; stroke:#994400; stroke-width:1.5; }}
  .pwr11{{ stroke:#CC0000; stroke-width:2.0; fill:none; }}
  .pwr5 {{ stroke:#CC6600; stroke-width:1.8; fill:none; }}
  .pwr33{{ stroke:#CC0066; stroke-width:1.5; fill:none; }}
  .gnd  {{ stroke:#006600; stroke-width:2.0; fill:none; }}
  .sig  {{ stroke:#0033CC; stroke-width:1.5; fill:none; }}
  .i2c  {{ stroke:#886600; stroke-width:1.5; fill:none; }}
  .mot3 {{ stroke:#994400; stroke-width:2.0; fill:none; }}
  .junc {{ fill:#222; stroke:none; }}
  .symv {{ fill:#CC6600; stroke:none; }}   /* +5V tri */
  .sym3 {{ fill:#CC0066; stroke:none; }}   /* +3V3 tri */
  .symg {{ fill:#006600; stroke:none; }}   /* GND tri */
  .sym1 {{ fill:#CC0000; stroke:none; }}   /* +11V tri */
</style>
'''

lines = []

def rect(x,y,w,h,cls='comp',rx=4):
    lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{cls}" rx="{rx}"/>')

def text(x,y,t,cls='lbl',anchor='middle',dy=0):
    extra = f' dy="{dy}"' if dy else ''
    lines.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}"{extra}>{t}</text>')

def wire(pts, cls='sig'):
    coords = ' '.join(f'{x},{y}' for x,y in pts)
    lines.append(f'<polyline points="{coords}" class="{cls}" fill="none"/>')

def junc(x,y,r=4):
    lines.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="junc"/>')

def pin_label(x, y, label, side='right', cls='pin'):
    if side == 'right':
        lines.append(f'<text x="{x+3}" y="{y+4}" text-anchor="start" class="{cls}">{label}</text>')
    elif side == 'left':
        lines.append(f'<text x="{x-3}" y="{y+4}" text-anchor="end" class="{cls}">{label}</text>')

# Power Symbols: GND (downward triangle), +5V / +3V3 / +11V (upward arrows)
def sym_gnd(x, y):
    lines.append(f'<polygon points="{x},{y} {x-8},{y+10} {x+8},{y+10}" class="symg"/>')
    lines.append(f'<text x="{x}" y="{y+22}" text-anchor="middle" font-size="9" fill="#006600">GND</text>')

def sym_vcc(x, y, label='+5V', cls='symv', col='#CC6600'):
    lines.append(f'<polygon points="{x},{y} {x-8},{y-10} {x+8},{y-10}" class="{cls}"/>')
    lines.append(f'<text x="{x}" y="{y-14}" text-anchor="middle" font-size="9" fill="{col}">{label}</text>')

def line(x1,y1,x2,y2,cls='sig'):
    lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"/>')

def stub(x, y, side='left', length=18):
    """Short pin stub line"""
    if side == 'left':
        line(x-length, y, x, y, 'sig')
    else:
        line(x, y, x+length, y, 'sig')

# ─────────────────────────────────────────────────────────────────────────────
# KOMPONENTEN — Positionen
# ─────────────────────────────────────────────────────────────────────────────

# LiPo Battery  (top-left)
LP = (40, 60, 100, 75)      # x,y,w,h
LP_BPLUS = (LP[0]+LP[2], LP[1]+20)    # (140, 80)
LP_BMINUS= (LP[0]+LP[2], LP[1]+55)    # (140, 115)

# ESC 20A
ES = (230, 40, 130, 155)
ES_VIN   = (ES[0],          ES[1]+30)   # (230,  70) left
ES_GND_I = (ES[0],          ES[1]+60)   # (230, 100) left
ES_PWM   = (ES[0],          ES[1]+105)  # (230, 145) left
ES_BEC5  = (ES[0]+ES[2],    ES[1]+30)   # (360,  70) right
ES_BECG  = (ES[0]+ES[2],    ES[1]+60)   # (360, 100) right
ES_PHA   = (ES[0]+ES[2],    ES[1]+105)  # (360, 145) right
ES_PHB   = (ES[0]+ES[2],    ES[1]+120)  # (360, 160) right
ES_PHC   = (ES[0]+ES[2],    ES[1]+135)  # (360, 175) right

# BL Motor
MT = (450, 55, 115, 100)
MT_PHA   = (MT[0], MT[1]+30)   # (450, 85) left
MT_PHB   = (MT[0], MT[1]+50)   # (450,105) left
MT_PHC   = (MT[0], MT[1]+70)   # (450,125) left

# ESP32
E3 = (600, 155, 155, 355)
E3_VIN   = (E3[0],          E3[1]+40)   # (600,195) left
E3_GND   = (E3[0],          E3[1]+65)   # (600,220) left
E3_3V3   = (E3[0],          E3[1]+90)   # (600,245) left
E3_21    = (E3[0],          E3[1]+150)  # (600,305) left  SDA
E3_22    = (E3[0],          E3[1]+175)  # (600,330) left  SCL
E3_25    = (E3[0]+E3[2],    E3[1]+200)  # (755,355) right GPIO25

# PCA9685
PC = (190, 335, 155, 200)
PC_VCC   = (PC[0]+PC[2], PC[1]+30)     # (345,365) right
PC_GND   = (PC[0]+PC[2], PC[1]+55)     # (345,390) right
PC_SDA   = (PC[0]+PC[2], PC[1]+80)     # (345,415) right
PC_SCL   = (PC[0]+PC[2], PC[1]+105)    # (345,440) right
PC_CH2   = (PC[0],        PC[1]+135)   # (190,470) left
PC_CH3   = (PC[0],        PC[1]+157)   # (190,492) left
PC_CH4   = (PC[0],        PC[1]+179)   # (190,514) left

# MS5837
MS = (820, 155, 145, 120)
MS_VCC   = (MS[0], MS[1]+25)   # (820,180) left
MS_GND   = (MS[0], MS[1]+50)   # (820,205) left
MS_SDA   = (MS[0], MS[1]+75)   # (820,230) left
MS_SCL   = (MS[0], MS[1]+100)  # (820,255) left

# MPU-6050
MP = (820, 335, 145, 120)
MP_VCC   = (MP[0], MP[1]+25)   # (820,360) left
MP_GND   = (MP[0], MP[1]+50)   # (820,385) left
MP_SDA   = (MP[0], MP[1]+75)   # (820,410) left
MP_SCL   = (MP[0], MP[1]+100)  # (820,435) left

# Servos (left column, stacked)
SBL = (30, 535, 125, 75)    # Brustflosse Links
SBL_SIG  = (SBL[0]+SBL[2], SBL[1]+18)  # right
SBL_VCC  = (SBL[0]+SBL[2], SBL[1]+38)
SBL_GND  = (SBL[0]+SBL[2], SBL[1]+58)

SBR = (30, 645, 125, 75)    # Brustflosse Rechts
SBR_SIG  = (SBR[0]+SBR[2], SBR[1]+18)
SBR_VCC  = (SBR[0]+SBR[2], SBR[1]+38)
SBR_GND  = (SBR[0]+SBR[2], SBR[1]+58)

SBA = (30, 755, 125, 75)    # Ballast
SBA_SIG  = (SBA[0]+SBA[2], SBA[1]+18)
SBA_VCC  = (SBA[0]+SBA[2], SBA[1]+38)
SBA_GND  = (SBA[0]+SBA[2], SBA[1]+58)

# ─────────────────────────────────────────────────────────────────────────────
# ZEICHNEN
# ─────────────────────────────────────────────────────────────────────────────

lines.append(svg_header())
lines.append('<rect width="1400" height="920" fill="#FDFCF8"/>')
# Title
lines.append('<rect x="0" y="880" width="1400" height="40" fill="#EEEEEE" stroke="#AAAAAA" stroke-width="0.5"/>')
lines.append('<text x="700" y="904" text-anchor="middle" font-size="13" font-weight="bold" font-family="monospace">'
             'Biomimetic Shark Robot — Point-to-Point Schaltplan v2.0 | Rev. 2026-06</text>')

# ─── LiPo ───
rect(*LP, cls='pcomp')
text(LP[0]+LP[2]//2, LP[1]+15, 'LiPo 3S 11.1V', 'lbl')
text(LP[0]+LP[2]//2, LP[1]+30, '2200mAh XT60', 'pin')
# stubs
line(LP_BPLUS[0], LP_BPLUS[1], LP_BPLUS[0]+15, LP_BPLUS[1], 'pwr11')
pin_label(LP_BPLUS[0]+15, LP_BPLUS[1], 'B+', 'right', 'pin')
line(LP_BMINUS[0], LP_BMINUS[1], LP_BMINUS[0]+15, LP_BMINUS[1], 'gnd')
pin_label(LP_BMINUS[0]+15, LP_BMINUS[1], 'B−', 'right', 'pin')

# ─── ESC ───
rect(*ES, cls='comp')
text(ES[0]+ES[2]//2, ES[1]+15, 'ESC 20A', 'lbl')
text(ES[0]+ES[2]//2, ES[1]+28, 'Hobbywing', 'pin')
# Left pins (stubs)
for px,lbl in [(ES_VIN,'VIN+'), (ES_GND_I,'GND'), (ES_PWM,'PWM IN')]:
    x,y = px[0],px[1]
    line(x-15, y, x, y, 'pwr11' if 'VIN' in lbl else ('gnd' if 'GND' in lbl else 'sig'))
    pin_label(x-16, y, lbl, 'left')
# Right pins
for px,lbl,cls_ in [(ES_BEC5,'BEC 5V','pwr5'),(ES_BECG,'BEC GND','gnd'),
                    (ES_PHA,'Ph.A','mot3'),(ES_PHB,'Ph.B','mot3'),(ES_PHC,'Ph.C','mot3')]:
    x,y = px[0],px[1]
    line(x, y, x+15, y, cls_)
    pin_label(x+16, y, lbl, 'right')

# ─── BL Motor ───
rect(*MT, cls='mot')
text(MT[0]+MT[2]//2, MT[1]+18, 'BL Motor', 'lbl')
text(MT[0]+MT[2]//2, MT[1]+32, 'KV=900 20W', 'pin')
for px,lbl in [(MT_PHA,'Ph.A'),(MT_PHB,'Ph.B'),(MT_PHC,'Ph.C')]:
    x,y=px[0],px[1]
    line(x-15,y,x,y,'mot3')
    pin_label(x-16,y,lbl,'left')

# ─── ESP32 ───
rect(*E3, cls='comp')
text(E3[0]+E3[2]//2, E3[1]+18, 'ESP32 DevKit V1', 'lbl')
text(E3[0]+E3[2]//2, E3[1]+32, 'WiFi / BT / 240MHz', 'pin')
# Left pins
for px,lbl,cls_ in [
    (E3_VIN, 'VIN', 'pwr5'), (E3_GND, 'GND', 'gnd'),
    (E3_3V3, '3V3', 'pwr33'), (E3_21, 'GPIO21 SDA', 'i2c'),
    (E3_22,  'GPIO22 SCL', 'i2c')]:
    x,y=px[0],px[1]
    line(x-15,y,x,y,cls_)
    pin_label(x-16,y,lbl,'left')
# Right pin GPIO25
x,y=E3_25
line(x,y,x+15,y,'sig')
pin_label(x+16,y,'GPIO25','right')

# ─── PCA9685 ───
rect(*PC, cls='comp')
text(PC[0]+PC[2]//2, PC[1]+18, 'PCA9685', 'lbl')
text(PC[0]+PC[2]//2, PC[1]+32, 'I2C Servo Driver', 'pin')
text(PC[0]+PC[2]//2, PC[1]+45, 'Addr: 0x40', 'pin')
# Right pins (toward ESP32)
for px,lbl,cls_ in [
    (PC_VCC,'VCC 5V','pwr5'),(PC_GND,'GND','gnd'),
    (PC_SDA,'SDA','i2c'),(PC_SCL,'SCL','i2c')]:
    x,y=px[0],px[1]
    line(x,y,x+15,y,cls_)
    pin_label(x+16,y,lbl,'right')
# Left pins (toward servos)
for px,lbl in [(PC_CH2,'CH2'),(PC_CH3,'CH3'),(PC_CH4,'CH4')]:
    x,y=px[0],px[1]
    line(x-15,y,x,y,'sig')
    pin_label(x-16,y,lbl,'left')

# ─── MS5837 ───
rect(*MS, cls='sens')
text(MS[0]+MS[2]//2, MS[1]+15, 'MS5837-30BA', 'lbl')
text(MS[0]+MS[2]//2, MS[1]+28, 'Depth Sensor', 'pin')
text(MS[0]+MS[2]//2, MS[1]+41, '0x76 / 0–300m', 'pin')
for px,lbl,cls_ in [(MS_VCC,'VCC 3V3','pwr33'),(MS_GND,'GND','gnd'),
                    (MS_SDA,'SDA','i2c'),(MS_SCL,'SCL','i2c')]:
    x,y=px[0],px[1]
    line(x-15,y,x,y,cls_)
    pin_label(x-16,y,lbl,'left')

# ─── MPU-6050 ───
rect(*MP, cls='sens')
text(MP[0]+MP[2]//2, MP[1]+15, 'MPU-6050', 'lbl')
text(MP[0]+MP[2]//2, MP[1]+28, 'IMU 6-DOF', 'pin')
text(MP[0]+MP[2]//2, MP[1]+41, '0x68 / Gyro+Accel', 'pin')
for px,lbl,cls_ in [(MP_VCC,'VCC 3V3','pwr33'),(MP_GND,'GND','gnd'),
                    (MP_SDA,'SDA','i2c'),(MP_SCL,'SCL','i2c')]:
    x,y=px[0],px[1]
    line(x-15,y,x,y,cls_)
    pin_label(x-16,y,lbl,'left')

# ─── Servos ───
for comp,lbl,sub in [(SBL,'Servo BFL','MG90S IP67'),(SBR,'Servo BFR','MG90S IP67'),(SBA,'Servo Ballast','MG996R IP67')]:
    x,y,w,h = comp
    rect(x,y,w,h,'serv')
    text(x+w//2, y+18, lbl, 'lbl')
    text(x+w//2, y+32, sub, 'pin')

for sig,vcc,gnd in [(SBL_SIG,SBL_VCC,SBL_GND),(SBR_SIG,SBR_VCC,SBR_GND),(SBA_SIG,SBA_VCC,SBA_GND)]:
    line(sig[0],sig[1],sig[0]+15,sig[1],'sig')
    pin_label(sig[0]+16,sig[1],'SIG','right')
    line(vcc[0],vcc[1],vcc[0]+15,vcc[1],'pwr5')
    pin_label(vcc[0]+16,vcc[1],'VCC','right')
    line(gnd[0],gnd[1],gnd[0]+15,gnd[1],'gnd')
    pin_label(gnd[0]+16,gnd[1],'GND','right')

# ═════════════════════════════════════════════════════════════════════════════
# VERBINDUNGEN — alle point-to-point, orthogonal
# ═════════════════════════════════════════════════════════════════════════════

# ── 1. LiPo B+ → ESC VIN+ ── (rot, 11V)
wire([(LP_BPLUS[0],LP_BPLUS[1]), (200,LP_BPLUS[1]), (200,ES_VIN[1]), (ES_VIN[0]-15,ES_VIN[1])], 'pwr11')

# ── 2. LiPo B- → ESC GND_IN ── (grün)
wire([(LP_BMINUS[0],LP_BMINUS[1]), (210,LP_BMINUS[1]), (210,ES_GND_I[1]), (ES_GND_I[0]-15,ES_GND_I[1])], 'gnd')

# ── 3+4+5. ESC Ph.A/B/C → Motor Ph.A/B/C ── (braun-orange)
for es_ph, mt_ph in [(ES_PHA,MT_PHA),(ES_PHB,MT_PHB),(ES_PHC,MT_PHC)]:
    x1,y1 = es_ph[0]+15, es_ph[1]   # end of ESC stub
    x2,y2 = mt_ph[0]-15, mt_ph[1]   # end of Motor stub
    jx = (x1+x2)//2
    wire([(x1,y1),(jx,y1),(jx,y2),(x2,y2)], 'mot3')

# ── 6. ESC BEC 5V → ESP32 VIN ── (orange, 5V)
# BEC_5V stub ends at (ES_BEC5[0]+15, ES_BEC5[1]) = (375, 70)
# ESP32 VIN stub ends at (E3_VIN[0]-15, E3_VIN[1]) = (585, 195)
# Route: right to x=580, then down to y=195
BEC_X = ES_BEC5[0]+15   # 375
ESP_VIN_X = E3_VIN[0]-15  # 585
V5_JUNC_X = 555          # vertical 5V bus
wire([(BEC_X, ES_BEC5[1]),
      (V5_JUNC_X, ES_BEC5[1]),
      (V5_JUNC_X, E3_VIN[1]),
      (ESP_VIN_X, E3_VIN[1])], 'pwr5')
junc(V5_JUNC_X, ES_BEC5[1])   # junction on 5V bus

# ── 7. 5V bus junction → PCA9685 VCC ──
# PCA VCC stub ends at (PC_VCC[0]+15, PC_VCC[1]) = (360, 365)
# Route from V5_JUNC_X at y=70 down to y=365 then left to 360
wire([(V5_JUNC_X, ES_BEC5[1]),
      (V5_JUNC_X, PC_VCC[1]),
      (PC_VCC[0]+15, PC_VCC[1])], 'pwr5')
junc(V5_JUNC_X, PC_VCC[1])

# ── 8. 5V bus → Servo VCC ──
# Route 5V bus down to servo area (x=V5_JUNC_X) then left along y-levels
SV_BUS_X = 170    # vertical 5V bus for servos
wire([(V5_JUNC_X, PC_VCC[1]),
      (V5_JUNC_X, SBL_VCC[1]),
      (SV_BUS_X, SBL_VCC[1])], 'pwr5')
junc(V5_JUNC_X, SBL_VCC[1])
# BFR
wire([(SV_BUS_X, SBL_VCC[1]),
      (SV_BUS_X, SBR_VCC[1]),
      (SBR_VCC[0]+15, SBR_VCC[1])], 'pwr5')
junc(SV_BUS_X, SBR_VCC[1])
# BAL
wire([(SV_BUS_X, SBR_VCC[1]),
      (SV_BUS_X, SBA_VCC[1]),
      (SBA_VCC[0]+15, SBA_VCC[1])], 'pwr5')
junc(SV_BUS_X, SBA_VCC[1])
# BFL connection to bus
line(SBL_VCC[0]+15, SBL_VCC[1], SV_BUS_X, SBL_VCC[1], 'pwr5')

# ── 9. ESC BEC GND → GND bus ──
GND_BUS_X = 215   # vertical GND bus
ES_BECG_END = (ES_BECG[0]+15, ES_BECG[1])
wire([ES_BECG_END, (GND_BUS_X, ES_BECG[1]), (GND_BUS_X, 855)], 'gnd')

# ── 10. ESP32 GND → GND bus ──
wire([(E3_GND[0]-15, E3_GND[1]),
      (GND_BUS_X, E3_GND[1])], 'gnd')
junc(GND_BUS_X, E3_GND[1])

# ── 11. PCA9685 GND → GND bus ──
wire([(PC_GND[0]+15, PC_GND[1]),
      (GND_BUS_X, PC_GND[1])], 'gnd')
junc(GND_BUS_X, PC_GND[1])

# ── 12. MS5837 GND → GND bus ──
GND_BUS_RIGHT_X = 800
wire([(MS_GND[0]-15, MS_GND[1]),
      (GND_BUS_RIGHT_X, MS_GND[1]),
      (GND_BUS_RIGHT_X, 855)], 'gnd')

# ── 13. MPU6050 GND → GND bus ──
wire([(MP_GND[0]-15, MP_GND[1]),
      (GND_BUS_RIGHT_X, MP_GND[1])], 'gnd')
junc(GND_BUS_RIGHT_X, MP_GND[1])

# ── 14. Servo GNDs → GND bus ──
SV_GND_X = 175
wire([(SBL_GND[0]+15, SBL_GND[1]), (SV_GND_X, SBL_GND[1]), (SV_GND_X, 855)], 'gnd')
junc(SV_GND_X, SBL_GND[1])
wire([(SBR_GND[0]+15, SBR_GND[1]), (SV_GND_X, SBR_GND[1])], 'gnd')
junc(SV_GND_X, SBR_GND[1])
wire([(SBA_GND[0]+15, SBA_GND[1]), (SV_GND_X, SBA_GND[1])], 'gnd')
junc(SV_GND_X, SBA_GND[1])

# GND bus bottom horizontal line
wire([(GND_BUS_X, 855), (SV_GND_X+2, 855), (SV_GND_X, 855)], 'gnd')
wire([(GND_BUS_X, 855), (GND_BUS_RIGHT_X, 855)], 'gnd')

# ── 15. ESP32 3V3 → MS5837 VCC ──
V33_BUS_X = 800
wire([(E3_3V3[0]-15, E3_3V3[1]),
      (V33_BUS_X, E3_3V3[1]),
      (V33_BUS_X, MS_VCC[1]),
      (MS_VCC[0]-15, MS_VCC[1])], 'pwr33')
junc(V33_BUS_X, MS_VCC[1])

# ── 16. 3V3 bus → MPU6050 VCC ──
wire([(V33_BUS_X, MS_VCC[1]),
      (V33_BUS_X, MP_VCC[1]),
      (MP_VCC[0]-15, MP_VCC[1])], 'pwr33')
junc(V33_BUS_X, MP_VCC[1])

# ── 17. ESP32 GPIO25 → ESC PWM_IN ──
# GPIO25 stub ends at (E3_25[0]+15, E3_25[1]) = (770, 355)
# PWM_IN stub ends at (ES_PWM[0]-15, ES_PWM[1]) = (215, 145)
# Route: right, up, left
wire([(E3_25[0]+15, E3_25[1]),
      (790, E3_25[1]),
      (790, 30),
      (215, 30),
      (215, ES_PWM[1]),
      (ES_PWM[0]-15, ES_PWM[1])], 'sig')
lines.append(f'<text x="500" y="25" text-anchor="middle" font-size="9" fill="#0033CC">GPIO25 → ESC PWM</text>')

# ── 18+19. ESP32 SDA/SCL → PCA9685 SDA/SCL ──
# SDA: ESP32 GPIO21 stub end (585, 305) → PCA SDA stub end (360, 415)
SDA_BUS_X = 575
wire([(E3_21[0]-15, E3_21[1]),
      (SDA_BUS_X, E3_21[1]),
      (SDA_BUS_X, PC_SDA[1]),
      (PC_SDA[0]+15, PC_SDA[1])], 'i2c')
junc(SDA_BUS_X, E3_21[1])

# SCL: ESP32 GPIO22 → PCA SCL
SCL_BUS_X = 570
wire([(E3_22[0]-15, E3_22[1]),
      (SCL_BUS_X, E3_22[1]),
      (SCL_BUS_X, PC_SCL[1]),
      (PC_SCL[0]+15, PC_SCL[1])], 'i2c')
junc(SCL_BUS_X, E3_22[1])

# ── 20+21. SDA bus → MS5837 + MPU6050 SDA ──
I2C_BUS_X = 808
# From SDA bus junction at (SDA_BUS_X, E3_21[1]) route right to I2C_BUS_X, then down
wire([(SDA_BUS_X, E3_21[1]),
      (I2C_BUS_X, E3_21[1]),
      (I2C_BUS_X, MS_SDA[1]),
      (MS_SDA[0]-15, MS_SDA[1])], 'i2c')
junc(I2C_BUS_X, MS_SDA[1])
wire([(I2C_BUS_X, MS_SDA[1]),
      (I2C_BUS_X, MP_SDA[1]),
      (MP_SDA[0]-15, MP_SDA[1])], 'i2c')
junc(I2C_BUS_X, MP_SDA[1])

# ── 22+23. SCL bus → MS5837 + MPU6050 SCL ──
I2C_SCL_X = 803
wire([(SCL_BUS_X, E3_22[1]),
      (I2C_SCL_X, E3_22[1]),
      (I2C_SCL_X, MS_SCL[1]),
      (MS_SCL[0]-15, MS_SCL[1])], 'i2c')
junc(I2C_SCL_X, MS_SCL[1])
wire([(I2C_SCL_X, MS_SCL[1]),
      (I2C_SCL_X, MP_SCL[1]),
      (MP_SCL[0]-15, MP_SCL[1])], 'i2c')
junc(I2C_SCL_X, MP_SCL[1])

# ── 24+25+26. PCA9685 CH2/3/4 → Servo SIG ──
CH_BUS_X = 185
# CH2 → BFL
wire([(PC_CH2[0]-15, PC_CH2[1]),
      (CH_BUS_X, PC_CH2[1]),
      (CH_BUS_X, SBL_SIG[1]),
      (SBL_SIG[0]+15, SBL_SIG[1])], 'sig')
junc(CH_BUS_X, PC_CH2[1])
# CH3 → BFR
wire([(PC_CH3[0]-15, PC_CH3[1]),
      (CH_BUS_X, PC_CH3[1]),
      (CH_BUS_X, SBR_SIG[1]),
      (SBR_SIG[0]+15, SBR_SIG[1])], 'sig')
junc(CH_BUS_X, PC_CH3[1])
# CH4 → BAL
wire([(PC_CH4[0]-15, PC_CH4[1]),
      (CH_BUS_X, PC_CH4[1]),
      (CH_BUS_X, SBA_SIG[1]),
      (SBA_SIG[0]+15, SBA_SIG[1])], 'sig')
junc(CH_BUS_X, PC_CH4[1])

# ── GND bus label ──
lines.append(f'<text x="{GND_BUS_X+3}" y="860" font-size="9" fill="#006600">GND Bus</text>')

# ─── LEGENDE ───
LG_X, LG_Y = 1020, 80
rect(LG_X, LG_Y, 360, 370, 'comp')
text(LG_X+180, LG_Y+18, 'LEGENDE', 'lbl')
entries = [
    ('pwr11','#CC0000','11.1V (LiPo/ESC)'),
    ('pwr5', '#CC6600','+5V (BEC)'),
    ('pwr33','#CC0066','+3.3V (ESP32)'),
    ('gnd',  '#006600','GND'),
    ('sig',  '#0033CC','Signal / PWM'),
    ('i2c',  '#886600','I2C (SDA/SCL)'),
    ('mot3', '#994400','Motor Phasen (3-Ph.)'),
]
for i,(cls,col,lbl) in enumerate(entries):
    y = LG_Y + 45 + i*30
    lines.append(f'<line x1="{LG_X+20}" y1="{y}" x2="{LG_X+80}" y2="{y}" class="{cls}"/>')
    lines.append(f'<text x="{LG_X+90}" y="{y+4}" font-size="10" fill="{col}" font-family="monospace">{lbl}</text>')

lines.append(f'<text x="{LG_X+20}" y="{LG_Y+265}" font-size="10" font-weight="bold" font-family="monospace">I2C Adressen:</text>')
for i,(addr,comp) in enumerate([('0x40','PCA9685'),('0x68','MPU-6050'),('0x76','MS5837')]):
    lines.append(f'<text x="{LG_X+20}" y="{LG_Y+282+i*16}" font-size="9" font-family="monospace">{addr} → {comp}</text>')
lines.append(f'<text x="{LG_X+20}" y="{LG_Y+335}" font-size="9" font-family="monospace">GPIO25 → ESC PWM (50Hz)</text>')
lines.append(f'<text x="{LG_X+20}" y="{LG_Y+352}" font-size="9" font-family="monospace">SDA=GPIO21 / SCL=GPIO22</text>')

lines.append('</svg>')

out = '/home/claude/shark/schematics/schaltplan_v2.svg'
with open(out, 'w') as f:
    f.write('\n'.join(lines))
print(f"✓ {out} ({len(lines)} Elemente)")
