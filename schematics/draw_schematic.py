#!/usr/bin/env python3
"""
Vollständiger Punkt-zu-Punkt Schaltplan — Biomimetic Shark Robot
Jede Verbindung geht von einem konkreten Pin zu einem anderen Pin.
KiCad-ähnlicher Stil mit Power-Symbolen und Net-Labels.
"""

lines = []

def svg_start(w=1600, h=1000):
    lines.append(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
  * {{ font-family: "Courier New", monospace; }}
  .comp  {{ fill:#F0F4FF; stroke:#1133AA; stroke-width:1.5; }}
  .power {{ fill:#FFF0E8; stroke:#AA4400; stroke-width:1.5; }}
  .sensor{{ fill:#EFFFEF; stroke:#116611; stroke-width:1.5; }}
  .servo {{ fill:#FFF0FF; stroke:#881188; stroke-width:1.5; }}
  .motor {{ fill:#FFFAEE; stroke:#AA6600; stroke-width:1.5; }}
  .lbl   {{ font-size:12px; font-weight:bold; fill:#111; }}
  .pin   {{ font-size:9px; fill:#333; }}
  .net   {{ font-size:9px; fill:#0033AA; font-style:italic; }}
  .val   {{ font-size:8px; fill:#555; }}
  line.pwr  {{ stroke:#CC2222; stroke-width:1.8; fill:none; }}
  line.gndw {{ stroke:#226622; stroke-width:1.8; fill:none; }}
  line.bec  {{ stroke:#CC6600; stroke-width:1.8; fill:none; }}
  line.v33  {{ stroke:#EE8800; stroke-width:1.8; fill:none; }}
  line.sig  {{ stroke:#2255CC; stroke-width:1.5; fill:none; }}
  line.i2c  {{ stroke:#AA6600; stroke-width:1.5; fill:none; stroke-dasharray:6,3; }}
  line.mot  {{ stroke:#CC4400; stroke-width:2; fill:none; }}
  line.srv  {{ stroke:#881188; stroke-width:1.5; fill:none; }}
  circle.junc{{ fill:#222; stroke:none; }}
</style>
<rect width="{w}" height="{h}" fill="#FDFCF8"/>''')

def svg_end():
    lines.append('</svg>')

def rect(x, y, w, h, cls='comp', rx=4):
    lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{cls}" rx="{rx}"/>')

def text(x, y, txt, cls='lbl', anchor='middle', size=None):
    sattr = f' font-size="{size}px"' if size else ''
    lines.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}"{sattr}>{txt}</text>')

def line(x1, y1, x2, y2, cls='sig'):
    lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"/>')

def wire(pts, cls='sig'):
    """Draw orthogonal wire through list of (x,y) points"""
    for i in range(len(pts)-1):
        line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], cls)

def junc(x, y, r=4):
    lines.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="junc"/>')

def gnd_sym(x, y, label='GND'):
    """GND symbol pointing down from pin (x,y)"""
    lines.append(f'''<g>
  <line x1="{x}" y1="{y}" x2="{x}" y2="{y+14}" class="gndw"/>
  <line x1="{x-12}" y1="{y+14}" x2="{x+12}" y2="{y+14}" class="gndw"/>
  <line x1="{x-7}"  y1="{y+20}" x2="{x+7}"  y2="{y+20}" class="gndw"/>
  <line x1="{x-3}"  y1="{y+26}" x2="{x+3}"  y2="{y+26}" class="gndw"/>
</g>''')

def vcc_sym(x, y, label='+5V', cls='bec'):
    """VCC symbol pointing up from pin (x,y)"""
    lines.append(f'''<g>
  <line x1="{x}" y1="{y}" x2="{x}" y2="{y-14}" class="{cls}"/>
  <line x1="{x-14}" y1="{y-14}" x2="{x+14}" y2="{y-14}" class="{cls}"/>
  <text x="{x}" y="{y-18}" text-anchor="middle" class="net" font-size="9">{label}</text>
</g>''')

def pin_stub(x, y, dx, label, cls='pin', anchor=None):
    """Draw a short pin stub and label"""
    x2 = x + dx
    line(x, y, x2, y, 'sig' if 'sig' not in cls else cls)
    anch = anchor or ('end' if dx < 0 else 'start')
    offset = -3 if dx < 0 else 3
    lines.append(f'<text x="{x2+offset}" y="{y+4}" text-anchor="{anch}" class="pin">{label}</text>')

def net_label(x, y, label, anchor='start'):
    lines.append(f'<rect x="{x-2}" y="{y-10}" width="{len(label)*7+4}" height="13" '
                 f'fill="white" stroke="#0033AA" stroke-width="0.5" rx="2"/>')
    lines.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
                 f'class="net" font-size="9">{label}</text>')

def box_comp(x, y, w, h, title, subtitle='', cls='comp'):
    rect(x, y, w, h, cls)
    text(x+w//2, y+16, title, 'lbl')
    if subtitle:
        text(x+w//2, y+28, subtitle, 'val')

# ════════════════════════════════════════════════════════════════════════
svg_start(1600, 1000)

# ────────────────────────────────────────────────────────────────────────
# KOMPONENTEN definieren (x, y, w, h)
# ────────────────────────────────────────────────────────────────────────

# 1. LiPo 3S  (40, 80, 90, 110)
LX,LY = 40, 80
box_comp(LX,LY,90,110,'LiPo 3S','11.1V 2200mAh','power')
text(LX+45, LY+45, 'XT60', 'val')
# Pins right side
# B+
LP_BPLUS = (LX+90, LY+30)
text(LP_BPLUS[0]-5, LP_BPLUS[1]+4, 'B+', 'pin', 'end')
# B-
LP_BMINUS = (LX+90, LY+80)
text(LP_BMINUS[0]-5, LP_BMINUS[1]+4, 'B−', 'pin', 'end')

# 2. ESC 20A  (200, 50, 160, 170)
EX,EY = 200, 50
box_comp(EX,EY,160,170,'ESC 20A','Hobbywing Platinum','comp')
text(EX+80, EY+43, 'BEC 5V/3A', 'val')
# Pins left
EP_VPLUS  = (EX,     EY+40)   # VIN+
EP_GNDIN  = (EX,     EY+70)   # GND in
EP_PWMIN  = (EX,     EY+130)  # PWM in
# Pins right
EP_BEC5V  = (EX+160, EY+40)   # BEC 5V out
EP_BECGND = (EX+160, EY+70)   # BEC GND
EP_PHA    = (EX+160, EY+100)  # Phase A
EP_PHB    = (EX+160, EY+120)  # Phase B
EP_PHC    = (EX+160, EY+140)  # Phase C

for (px,py),lbl in [(EP_VPLUS,'VIN+'),(EP_GNDIN,'GND'),(EP_PWMIN,'PWM IN')]:
    lines.append(f'<line x1="{px}" y1="{py}" x2="{px-18}" y2="{py}" class="sig"/>')
    lines.append(f'<text x="{px-20}" y="{py+4}" text-anchor="end" class="pin">{lbl}</text>')
for (px,py),lbl in [(EP_BEC5V,'BEC 5V'),(EP_BECGND,'BEC GND'),
                     (EP_PHA,'Ph A'),(EP_PHB,'Ph B'),(EP_PHC,'Ph C')]:
    lines.append(f'<line x1="{px}" y1="{py}" x2="{px+18}" y2="{py}" class="sig"/>')
    lines.append(f'<text x="{px+20}" y="{py+4}" text-anchor="start" class="pin">{lbl}</text>')

# 3. BL Motor  (500, 60, 130, 100)
MX,MY = 500, 60
box_comp(MX,MY,130,100,'BL Motor','KV=900 Outrunner','motor')
text(MX+65, MY+55, 'Getriebe 40:1', 'val')
MP_PHA = (MX, MY+30)
MP_PHB = (MX, MY+50)
MP_PHC = (MX, MY+70)
for (px,py),lbl in [(MP_PHA,'Ph A'),(MP_PHB,'Ph B'),(MP_PHC,'Ph C')]:
    lines.append(f'<line x1="{px}" y1="{py}" x2="{px-18}" y2="{py}" class="mot"/>')
    lines.append(f'<text x="{px-20}" y="{py+4}" text-anchor="end" class="pin">{lbl}</text>')
# Shaft out right
lines.append(f'<line x1="{MX+130}" y1="{MY+50}" x2="{MX+165}" y2="{MY+50}" stroke="#666" stroke-width="3" fill="none"/>')
text(MX+170, MY+46, '→ Nocken- welle', 'val', 'start', 8)

# 4. ESP32  (600, 280, 180, 300)
ESP_X, ESP_Y = 600, 280
box_comp(ESP_X, ESP_Y, 180, 300, 'ESP32 DevKit V1','240MHz WiFi/BT','comp')
# Left pins
ESPP_VIN   = (ESP_X,     ESP_Y+40)
ESPP_GND   = (ESP_X,     ESP_Y+70)
ESPP_G25   = (ESP_X,     ESP_Y+140)  # GPIO25 PWM
ESPP_G21   = (ESP_X,     ESP_Y+200)  # GPIO21 SDA
ESPP_G22   = (ESP_X,     ESP_Y+230)  # GPIO22 SCL
# Right pins
ESPP_3V3   = (ESP_X+180, ESP_Y+40)
for (px,py),lbl in [(ESPP_VIN,'VIN'),(ESPP_GND,'GND'),
                     (ESPP_G25,'GPIO25'),(ESPP_G21,'GPIO21 SDA'),(ESPP_G22,'GPIO22 SCL')]:
    lines.append(f'<line x1="{px}" y1="{py}" x2="{px-18}" y2="{py}" class="sig"/>')
    lines.append(f'<text x="{px-20}" y="{py+4}" text-anchor="end" class="pin">{lbl}</text>')
lines.append(f'<line x1="{ESPP_3V3[0]}" y1="{ESPP_3V3[1]}" x2="{ESPP_3V3[0]+18}" y2="{ESPP_3V3[1]}" class="sig"/>')
lines.append(f'<text x="{ESPP_3V3[0]+20}" y="{ESPP_3V3[1]+4}" text-anchor="start" class="pin">3V3</text>')

# 5. PCA9685  (250, 330, 160, 220)
PCA_X, PCA_Y = 250, 330
box_comp(PCA_X, PCA_Y, 160, 220, 'PCA9685', 'I2C 0x40', 'comp')
# Right pins (toward ESP32)
PCAP_VCC  = (PCA_X+160, PCA_Y+40)
PCAP_GND  = (PCA_X+160, PCA_Y+70)
PCAP_SDA  = (PCA_X+160, PCA_Y+110)
PCAP_SCL  = (PCA_X+160, PCA_Y+140)
PCAP_VPWR = (PCA_X+160, PCA_Y+180)  # V+ servo power
# Left pins (to servos)
PCAP_CH2  = (PCA_X,     PCA_Y+120)
PCAP_CH3  = (PCA_X,     PCA_Y+150)
PCAP_CH4  = (PCA_X,     PCA_Y+180)
for (px,py),lbl in [(PCAP_VCC,'VCC'),(PCAP_GND,'GND'),
                     (PCAP_SDA,'SDA'),(PCAP_SCL,'SCL'),(PCAP_VPWR,'V+')]:
    lines.append(f'<line x1="{px}" y1="{py}" x2="{px+18}" y2="{py}" class="sig"/>')
    lines.append(f'<text x="{px+20}" y="{py+4}" text-anchor="start" class="pin">{lbl}</text>')
for (px,py),lbl in [(PCAP_CH2,'CH2'),(PCAP_CH3,'CH3'),(PCAP_CH4,'CH4')]:
    lines.append(f'<line x1="{px}" y1="{py}" x2="{px-18}" y2="{py}" class="sig"/>')
    lines.append(f'<text x="{px-20}" y="{py+4}" text-anchor="end" class="pin">{lbl}</text>')

# 6. MS5837  (860, 200, 160, 120)
MS_X, MS_Y = 860, 200
box_comp(MS_X, MS_Y, 160, 120, 'MS5837-30BA', 'Depth 0x76', 'sensor')
MSP_VCC = (MS_X, MS_Y+30)
MSP_GND = (MS_X, MS_Y+55)
MSP_SDA = (MS_X, MS_Y+80)
MSP_SCL = (MS_X, MS_Y+100)
for (px,py),lbl in [(MSP_VCC,'VCC'),(MSP_GND,'GND'),(MSP_SDA,'SDA'),(MSP_SCL,'SCL')]:
    lines.append(f'<line x1="{px}" y1="{py}" x2="{px-18}" y2="{py}" class="sig"/>')
    lines.append(f'<text x="{px-20}" y="{py+4}" text-anchor="end" class="pin">{lbl}</text>')

# 7. MPU-6050  (860, 390, 160, 120)
MPU_X, MPU_Y = 860, 390
box_comp(MPU_X, MPU_Y, 160, 120, 'MPU-6050', 'IMU 0x68', 'sensor')
MPUP_VCC = (MPU_X, MPU_Y+30)
MPUP_GND = (MPU_X, MPU_Y+55)
MPUP_SDA = (MPU_X, MPU_Y+80)
MPUP_SCL = (MPU_X, MPU_Y+100)
for (px,py),lbl in [(MPUP_VCC,'VCC'),(MPUP_GND,'GND'),(MPUP_SDA,'SDA'),(MPUP_SCL,'SCL')]:
    lines.append(f'<line x1="{px}" y1="{py}" x2="{px-18}" y2="{py}" class="sig"/>')
    lines.append(f'<text x="{px-20}" y="{py+4}" text-anchor="end" class="pin">{lbl}</text>')

# 8-10. Servos  (bottom row)
def servo_comp(sx, sy, title, sub, ch_label):
    box_comp(sx, sy, 130, 90, title, sub, 'servo')
    # Signal top
    SP_SIG = (sx+40, sy)
    SP_VCC = (sx+80, sy)
    SP_GND = (sx+115, sy+90)
    lines.append(f'<line x1="{SP_SIG[0]}" y1="{SP_SIG[1]}" x2="{SP_SIG[0]}" y2="{SP_SIG[1]-18}" class="srv"/>')
    lines.append(f'<text x="{SP_SIG[0]}" y="{SP_SIG[1]-22}" text-anchor="middle" class="pin">SIG</text>')
    lines.append(f'<line x1="{SP_VCC[0]}" y1="{SP_VCC[1]}" x2="{SP_VCC[0]}" y2="{SP_VCC[1]-18}" class="bec"/>')
    lines.append(f'<text x="{SP_VCC[0]}" y="{SP_VCC[1]-22}" text-anchor="middle" class="pin">VCC</text>')
    gnd_sym(SP_GND[0], SP_GND[1])
    return SP_SIG, SP_VCC, SP_GND

S1X,S1Y = 50,  700
S2X,S2Y = 250, 700
S3X,S3Y = 450, 700
S1_SIG, S1_VCC, _ = servo_comp(S1X,S1Y,'Servo BFL','MG90S IP67','CH2')
S2_SIG, S2_VCC, _ = servo_comp(S2X,S2Y,'Servo BFR','MG90S IP67','CH3')
S3_SIG, S3_VCC, _ = servo_comp(S3X,S3Y,'Servo BAL','MG996R IP67','CH4')

# ════════════════════════════════════════════════════════════════════════
# VERBINDUNGEN (alle Punkt zu Punkt!)
# ════════════════════════════════════════════════════════════════════════

# ── 11.1V: LiPo B+ → ESC VIN+ ─────────────────────────────────────────
wire([LP_BPLUS, (180,LP_BPLUS[1]), (180,EP_VPLUS[1]), EP_VPLUS], 'pwr')

# ── GND: LiPo B− → ESC GND_in ─────────────────────────────────────────
wire([LP_BMINUS, (185,LP_BMINUS[1]), (185,EP_GNDIN[1]), EP_GNDIN], 'gndw')
gnd_sym(LP_BMINUS[0]+0, LP_BMINUS[1]+5)

# ── GND: ESC BEC_GND → GND symbol ─────────────────────────────────────
wire([EP_BECGND, (EP_BECGND[0]+30, EP_BECGND[1])], 'gndw')
gnd_sym(EP_BECGND[0]+30, EP_BECGND[1])

# ── BEC 5V rail: ESC BEC5V → junction → ESP32 VIN ─────────────────────
# Horizontal bus at y=20
BEC_BUS_Y = 22
wire([EP_BEC5V, (EP_BEC5V[0]+30, EP_BEC5V[1]), (EP_BEC5V[0]+30, BEC_BUS_Y),
     (ESPP_VIN[0]-40, BEC_BUS_Y)], 'bec')
# ESP32 VIN branch
wire([(ESPP_VIN[0]-40, BEC_BUS_Y), (ESPP_VIN[0]-40, ESPP_VIN[1]), ESPP_VIN], 'bec')
junc(ESPP_VIN[0]-40, BEC_BUS_Y)

# BEC 5V → PCA9685 VCC
BEC_J1 = (PCA_X+200, BEC_BUS_Y)  # junction on BEC bus
wire([(PCA_X+200, BEC_BUS_Y), (PCA_X+200, PCAP_VCC[1]), PCAP_VCC], 'bec')
junc(PCA_X+200, BEC_BUS_Y)

# BEC 5V → Servo VCC bus (vertical down left side)
SRV_VCC_BUS_X = 40
wire([(SRV_VCC_BUS_X, BEC_BUS_Y), (SRV_VCC_BUS_X, S1_VCC[1])], 'bec')
junc(SRV_VCC_BUS_X, BEC_BUS_Y)
# Servo VCC branches
wire([(SRV_VCC_BUS_X, S1_VCC[1]), (S1_VCC[0], S1_VCC[1])], 'bec')
wire([(SRV_VCC_BUS_X, S1_VCC[1]), (SRV_VCC_BUS_X, S2_VCC[1]), (S2_VCC[0], S2_VCC[1])], 'bec')
wire([(SRV_VCC_BUS_X, S1_VCC[1]), (SRV_VCC_BUS_X, S3_VCC[1]), (S3_VCC[0], S3_VCC[1])], 'bec')
junc(SRV_VCC_BUS_X, S1_VCC[1])

# PCA9685 V+ (servo power) → same BEC rail
wire([PCAP_VPWR, (PCAP_VPWR[0]+30, PCAP_VPWR[1]), (PCAP_VPWR[0]+30, BEC_BUS_Y)], 'bec')
junc(PCAP_VPWR[0]+30, BEC_BUS_Y)

# BEC bus label
net_label(300, BEC_BUS_Y+8, '+5V BEC')

# ── GND: ESP32 → GND symbol ────────────────────────────────────────────
gnd_sym(ESPP_GND[0]-18, ESPP_GND[1])
lines.append(f'<line x1="{ESPP_GND[0]}" y1="{ESPP_GND[1]}" x2="{ESPP_GND[0]-18}" y2="{ESPP_GND[1]}" class="gndw"/>')

# ── GND: PCA9685 GND → GND symbol ──────────────────────────────────────
wire([PCAP_GND, (PCAP_GND[0]+40, PCAP_GND[1])], 'gndw')
gnd_sym(PCAP_GND[0]+40, PCAP_GND[1])

# ── GND: MS5837 GND → symbol ───────────────────────────────────────────
wire([MSP_GND, (MSP_GND[0]-30, MSP_GND[1])], 'gndw')
gnd_sym(MSP_GND[0]-30, MSP_GND[1])

# ── GND: MPU6050 GND → symbol ──────────────────────────────────────────
wire([MPUP_GND, (MPUP_GND[0]-30, MPUP_GND[1])], 'gndw')
gnd_sym(MPUP_GND[0]-30, MPUP_GND[1])

# ── 3.3V: ESP32 3V3 → MS5837 VCC and MPU6050 VCC ──────────────────────
V33_BUS_X = 845
# ESP32 3V3 → horizontal to MS5837
wire([ESPP_3V3, (V33_BUS_X, ESPP_3V3[1]), (V33_BUS_X, MSP_VCC[1]), MSP_VCC], 'v33')
# Branch to MPU6050
wire([(V33_BUS_X, MPUP_VCC[1]), MPUP_VCC], 'v33')
junc(V33_BUS_X, MPUP_VCC[1])
vcc_sym(V33_BUS_X, MSP_VCC[1], '+3.3V', 'v33')

# ── PWM: ESP32 GPIO25 → ESC PWM_IN ─────────────────────────────────────
PWM_ROUTE_Y = 490
wire([ESPP_G25, (ESPP_G25[0]-40, ESPP_G25[1]), (ESPP_G25[0]-40, PWM_ROUTE_Y),
     (EP_PWMIN[0]-40, PWM_ROUTE_Y), (EP_PWMIN[0]-40, EP_PWMIN[1]), EP_PWMIN], 'sig')
net_label(ESPP_G25[0]-100, PWM_ROUTE_Y-3, 'GPIO25 PWM 50Hz')

# ── I2C SDA: ESP32 GPIO21 → PCA9685 SDA, MS5837 SDA, MPU6050 SDA ───────
SDA_BUS_X = 550
SDA_BUS_Y_L = 620  # bottom horizontal bus

# ESP32 GPIO21 → left → SDA bus node
wire([ESPP_G21, (SDA_BUS_X, ESPP_G21[1]), (SDA_BUS_X, SDA_BUS_Y_L)], 'i2c')

# SDA bus → PCA9685 SDA (go right from bus, then up to PCA)
PCA_SDA_J = (SDA_BUS_X, PCAP_SDA[1])
wire([(SDA_BUS_X, PCAP_SDA[1]), PCAP_SDA], 'i2c')
junc(SDA_BUS_X, PCAP_SDA[1])

# SDA bus bottom → MS5837 SDA (right)
SDA_RIGHT_X = 855
wire([(SDA_BUS_X, SDA_BUS_Y_L), (SDA_RIGHT_X, SDA_BUS_Y_L),
     (SDA_RIGHT_X, MSP_SDA[1]), MSP_SDA], 'i2c')
# Branch MPU6050 SDA from right bus
wire([(SDA_RIGHT_X, MPUP_SDA[1]), MPUP_SDA], 'i2c')
junc(SDA_RIGHT_X, MPUP_SDA[1])
junc(SDA_BUS_X, SDA_BUS_Y_L)
net_label(SDA_BUS_X+5, SDA_BUS_Y_L-3, 'SDA')

# ── I2C SCL: ESP32 GPIO22 → PCA9685 SCL, MS5837 SCL, MPU6050 SCL ───────
SCL_BUS_X = 540
SCL_BUS_Y_L = 645

wire([ESPP_G22, (SCL_BUS_X, ESPP_G22[1]), (SCL_BUS_X, SCL_BUS_Y_L)], 'i2c')

# SCL → PCA9685
wire([(SCL_BUS_X, PCAP_SCL[1]), PCAP_SCL], 'i2c')
junc(SCL_BUS_X, PCAP_SCL[1])

# SCL bottom → MS5837 and MPU6050
SCL_RIGHT_X = 854
wire([(SCL_BUS_X, SCL_BUS_Y_L), (SCL_RIGHT_X, SCL_BUS_Y_L),
     (SCL_RIGHT_X, MSP_SCL[1]), MSP_SCL], 'i2c')
wire([(SCL_RIGHT_X, MPUP_SCL[1]), MPUP_SCL], 'i2c')
junc(SCL_RIGHT_X, MPUP_SCL[1])
junc(SCL_BUS_X, SCL_BUS_Y_L)
net_label(SCL_BUS_X+5, SCL_BUS_Y_L-3, 'SCL')

# ── Motor phases: ESC → BL Motor ───────────────────────────────────────
wire([EP_PHA, (480, EP_PHA[1]), MP_PHA], 'mot')
wire([EP_PHB, (480, EP_PHB[1]), MP_PHB], 'mot')
wire([EP_PHC, (480, EP_PHC[1]), MP_PHC], 'mot')

# ── Servo signals: PCA9685 CH2/3/4 → Servos ────────────────────────────
# CH2 → Servo BFL
SRV_SIG_BUS_X = 30
# Route: PCA CH2 left → bus → down → servo SIG up
wire([PCAP_CH2, (SRV_SIG_BUS_X, PCAP_CH2[1]), (SRV_SIG_BUS_X, S1_SIG[1]), S1_SIG], 'srv')
# CH3 → Servo BFR
wire([PCAP_CH3, (SRV_SIG_BUS_X-5, PCAP_CH3[1]),
     (SRV_SIG_BUS_X-5, S2_SIG[1]), (S2_SIG[0], S2_SIG[1])], 'srv')
# CH4 → Servo BAL
wire([PCAP_CH4, (SRV_SIG_BUS_X-10, PCAP_CH4[1]),
     (SRV_SIG_BUS_X-10, S3_SIG[1]), (S3_SIG[0], S3_SIG[1])], 'srv')

# ────────────────────────────────────────────────────────────────────────
# TITLE + LEGENDE
# ────────────────────────────────────────────────────────────────────────
rect(1050, 150, 520, 480, 'comp')
text(1310, 175, 'LEGENDE', 'lbl')

legend_items = [
    ('pwr',  '#CC2222', '11.1V (LiPo)'),
    ('bec',  '#CC6600', '+5V BEC (ESC out)'),
    ('v33',  '#EE8800', '+3.3V (ESP32)'),
    ('gndw', '#226622', 'GND'),
    ('sig',  '#2255CC', 'Signal / PWM'),
    ('i2c',  '#AA6600', 'I2C (SDA/SCL) gestrichelt'),
    ('mot',  '#CC4400', 'Motor 3-Phasen'),
    ('srv',  '#881188', 'Servo-Signal (PCA9685)'),
]
for i,(cls,color,lbl) in enumerate(legend_items):
    y = 205 + i*30
    lines.append(f'<line x1="1070" y1="{y}" x2="1130" y2="{y}" stroke="{color}" '
                 f'stroke-width="1.8" fill="none" '
                 + ('stroke-dasharray="6,3"' if cls=='i2c' else '') + '/>')
    text(1140, y+4, lbl, 'pin', 'start')

# I2C addresses
text(1060, 460, 'I2C Adressen:', 'lbl', 'start', 11)
for i,(addr,name) in enumerate([('0x40','PCA9685'),('0x68','MPU-6050'),('0x76','MS5837')]):
    text(1060, 480+i*16, f'{addr}  {name}', 'pin', 'start')

text(1060, 548, 'GPIO Belegung:', 'lbl', 'start', 11)
gpios = [('GPIO21','SDA I2C'),('GPIO22','SCL I2C'),('GPIO25','PWM ESC 50Hz'),
         ('VIN','5V von BEC'),('GND','Masse'),('3V3','→ Sensoren')]
for i,(g,d) in enumerate(gpios):
    text(1060, 566+i*16, f'{g}  →  {d}', 'pin', 'start')

# GND symbol in legend
gnd_sym(1100, 568+len(gpios)*16+10)
text(1130, 568+len(gpios)*16+24, 'GND Symbol', 'pin', 'start')
# VCC symbol in legend
vcc_sym(1100, 568+len(gpios)*16+60, '+VCC', 'bec')
text(1130, 568+len(gpios)*16+46, 'VCC Symbol', 'pin', 'start')

# Title block
rect(0, 960, 1600, 40, 'comp')
text(800, 984, 'Biomimetic Shark Robot — Schaltplan v2.0  |  Alle Verbindungen Punkt-zu-Punkt  |  Fritzing-kompatibel  |  Rev 2.0 · 2026-06', 'lbl')

svg_end()

svg_content = '\n'.join(lines)
out = '/home/claude/shark/schematics/schaltplan_v2_vollstaendig.svg'
with open(out, 'w') as f:
    f.write(svg_content)
print(f"✓ {out} ({len(svg_content)//1024} KB, {svg_content.count('<line')} Leitungen)")
