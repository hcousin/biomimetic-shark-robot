#!/usr/bin/env python3
"""
Generiert eine vollständige Fritzing-kompatible .fzz Datei
für den Biomimetic Shark Robot.

Enthält alle Komponenten und Verbindungen:
  - ESP32 DevKit V1
  - PCA9685 I2C Servo Driver
  - MS5837-30BA Tiefensensor
  - MPU-6050 IMU
  - ESC 20A (Brushless)
  - Brushless Motor
  - 3x Servos (MG90S, MG996R)
  - LiPo 3S 11.1V
  - UBEC 5V/3A
"""

import zipfile
import json
import os

# ─── Fritzing Sketch XML ──────────────────────────────────────────────────────
SKETCH_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<module fritzingVersion="0.9.10" moduleId="shark_robot_schematic">
 <title>Biomimetic Shark Robot Schematic</title>
 <author>hcousin</author>
 <date>2026-06-07</date>
 <description>Single BL Motor + ESP32 + PCA9685 + MS5837 + MPU6050 + Servos</description>
 <views>
  <schematicView>
   <layers image="schematic/shark_schematic.svg">
    <layer layerId="schematicTrace0"/>
    <layer layerId="schematicTrace1"/>
   </layers>
  </schematicView>
  <breadboardView>
   <layers image="breadboard/shark_breadboard.svg">
    <layer layerId="breadboardbreadboard"/>
   </layers>
  </breadboardView>
 </views>
 <instances>

  <!-- ESP32 DevKit V1 -->
  <instance moduleIdRef="ESP32_DevKit_V1" modelIndex="1" path="core:esp32_devkit_v1">
   <title>ESP32</title>
   <views>
    <schematicView layer="schematicTrace0">
     <geometry x="400" y="200" z="0" transform="matrix(1 0 0 1 0 0)"/>
    </schematicView>
    <breadboardView layer="breadboardbreadboard">
     <geometry x="400" y="300" z="0" transform="matrix(1 0 0 1 0 0)"/>
    </breadboardView>
   </views>
  </instance>

  <!-- PCA9685 -->
  <instance moduleIdRef="PCA9685_I2C" modelIndex="2" path="core:pca9685">
   <title>PCA9685</title>
   <views>
    <schematicView layer="schematicTrace0">
     <geometry x="150" y="350" z="0" transform="matrix(1 0 0 1 0 0)"/>
    </schematicView>
   </views>
  </instance>

  <!-- MS5837 -->
  <instance moduleIdRef="MS5837_30BA" modelIndex="3" path="core:generic_ic">
   <title>MS5837-30BA</title>
   <views>
    <schematicView layer="schematicTrace0">
     <geometry x="650" y="150" z="0" transform="matrix(1 0 0 1 0 0)"/>
    </schematicView>
   </views>
  </instance>

  <!-- MPU6050 -->
  <instance moduleIdRef="MPU6050" modelIndex="4" path="core:mpu6050">
   <title>MPU-6050</title>
   <views>
    <schematicView layer="schematicTrace0">
     <geometry x="650" y="300" z="0" transform="matrix(1 0 0 1 0 0)"/>
    </schematicView>
   </views>
  </instance>

  <!-- ESC 20A -->
  <instance moduleIdRef="ESC_20A" modelIndex="5" path="core:generic_ic">
   <title>ESC 20A</title>
   <views>
    <schematicView layer="schematicTrace0">
     <geometry x="150" y="150" z="0" transform="matrix(1 0 0 1 0 0)"/>
    </schematicView>
   </views>
  </instance>

  <!-- LiPo Battery -->
  <instance moduleIdRef="LiPo_3S" modelIndex="6" path="core:battery">
   <title>LiPo 3S 11.1V</title>
   <views>
    <schematicView layer="schematicTrace0">
     <geometry x="50" y="200" z="0" transform="matrix(1 0 0 1 0 0)"/>
    </schematicView>
   </views>
  </instance>

  <!-- Servo Brustflosse Links -->
  <instance moduleIdRef="Servo_MG90S" modelIndex="7" path="core:servo">
   <title>Servo BFL (MG90S)</title>
   <views>
    <schematicView layer="schematicTrace0">
     <geometry x="150" y="500" z="0" transform="matrix(1 0 0 1 0 0)"/>
    </schematicView>
   </views>
  </instance>

  <!-- Servo Brustflosse Rechts -->
  <instance moduleIdRef="Servo_MG90S" modelIndex="8" path="core:servo">
   <title>Servo BFR (MG90S)</title>
   <views>
    <schematicView layer="schematicTrace0">
     <geometry x="300" y="500" z="0" transform="matrix(1 0 0 1 0 0)"/>
    </schematicView>
   </views>
  </instance>

  <!-- Servo Ballast -->
  <instance moduleIdRef="Servo_MG996R" modelIndex="9" path="core:servo">
   <title>Servo Ballast (MG996R)</title>
   <views>
    <schematicView layer="schematicTrace0">
     <geometry x="450" y="500" z="0" transform="matrix(1 0 0 1 0 0)"/>
    </schematicView>
   </views>
  </instance>

 </instances>

 <wires>
  <!-- POWER: LiPo+ → ESC VIN -->
  <wire modelIndex="100">
   <views>
    <schematicView>
     <geometry x="0" y="0" z="0">
      <wireExtras mils="0"/>
     </geometry>
    </schematicView>
   </views>
   <connectors>
    <connector connectorId="vout_plus" modelIndex="6"/>
    <connector connectorId="vin_plus" modelIndex="5"/>
   </connectors>
  </wire>

  <!-- POWER: LiPo- → ESC GND -->
  <wire modelIndex="101">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="vout_minus" modelIndex="6"/>
    <connector connectorId="vin_gnd" modelIndex="5"/>
   </connectors>
  </wire>

  <!-- POWER: ESC BEC 5V → ESP32 VIN -->
  <wire modelIndex="102">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="bec_5v" modelIndex="5"/>
    <connector connectorId="vin" modelIndex="1"/>
   </connectors>
  </wire>

  <!-- POWER: ESC BEC GND → ESP32 GND -->
  <wire modelIndex="103">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="bec_gnd" modelIndex="5"/>
    <connector connectorId="gnd" modelIndex="1"/>
   </connectors>
  </wire>

  <!-- SIGNAL: ESP32 GPIO25 → ESC PWM -->
  <wire modelIndex="104">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="gpio25" modelIndex="1"/>
    <connector connectorId="pwm_in" modelIndex="5"/>
   </connectors>
  </wire>

  <!-- I2C: ESP32 GPIO21 (SDA) → PCA9685 SDA -->
  <wire modelIndex="105">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="gpio21" modelIndex="1"/>
    <connector connectorId="sda" modelIndex="2"/>
   </connectors>
  </wire>

  <!-- I2C: ESP32 GPIO22 (SCL) → PCA9685 SCL -->
  <wire modelIndex="106">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="gpio22" modelIndex="1"/>
    <connector connectorId="scl" modelIndex="2"/>
   </connectors>
  </wire>

  <!-- I2C: ESP32 GPIO21 (SDA) → MS5837 SDA -->
  <wire modelIndex="107">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="gpio21" modelIndex="1"/>
    <connector connectorId="sda" modelIndex="3"/>
   </connectors>
  </wire>

  <!-- I2C: ESP32 GPIO22 (SCL) → MS5837 SCL -->
  <wire modelIndex="108">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="gpio22" modelIndex="1"/>
    <connector connectorId="scl" modelIndex="3"/>
   </connectors>
  </wire>

  <!-- I2C: ESP32 GPIO21 (SDA) → MPU6050 SDA -->
  <wire modelIndex="109">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="gpio21" modelIndex="1"/>
    <connector connectorId="sda" modelIndex="4"/>
   </connectors>
  </wire>

  <!-- I2C: ESP32 GPIO22 (SCL) → MPU6050 SCL -->
  <wire modelIndex="110">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="gpio22" modelIndex="1"/>
    <connector connectorId="scl" modelIndex="4"/>
   </connectors>
  </wire>

  <!-- I2C: 3.3V → MS5837 VCC -->
  <wire modelIndex="111">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="3v3" modelIndex="1"/>
    <connector connectorId="vcc" modelIndex="3"/>
   </connectors>
  </wire>

  <!-- I2C: 3.3V → MPU6050 VCC -->
  <wire modelIndex="112">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="3v3" modelIndex="1"/>
    <connector connectorId="vcc" modelIndex="4"/>
   </connectors>
  </wire>

  <!-- 5V → PCA9685 VCC -->
  <wire modelIndex="113">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="bec_5v" modelIndex="5"/>
    <connector connectorId="vcc" modelIndex="2"/>
   </connectors>
  </wire>

  <!-- PCA9685 CH2 → Servo BFL Signal -->
  <wire modelIndex="114">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="ch2" modelIndex="2"/>
    <connector connectorId="signal" modelIndex="7"/>
   </connectors>
  </wire>

  <!-- PCA9685 CH3 → Servo BFR Signal -->
  <wire modelIndex="115">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="ch3" modelIndex="2"/>
    <connector connectorId="signal" modelIndex="8"/>
   </connectors>
  </wire>

  <!-- PCA9685 CH4 → Servo Ballast Signal -->
  <wire modelIndex="116">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="ch4" modelIndex="2"/>
    <connector connectorId="signal" modelIndex="9"/>
   </connectors>
  </wire>

  <!-- GND: ESP32 GND → MPU6050 GND -->
  <wire modelIndex="120">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="gnd" modelIndex="1"/>
    <connector connectorId="gnd" modelIndex="4"/>
   </connectors>
  </wire>

  <!-- GND: ESP32 GND → MS5837 GND -->
  <wire modelIndex="121">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="gnd" modelIndex="1"/>
    <connector connectorId="gnd" modelIndex="3"/>
   </connectors>
  </wire>

  <!-- GND: ESP32 GND → PCA9685 GND -->
  <wire modelIndex="122">
   <views><schematicView><geometry x="0" y="0" z="0"><wireExtras mils="0"/></geometry></schematicView></views>
   <connectors>
    <connector connectorId="gnd" modelIndex="1"/>
    <connector connectorId="gnd" modelIndex="2"/>
   </connectors>
  </wire>

 </wires>

</module>
'''

# ─── Vollständiges SVG Schaltplan (Schematic View) ───────────────────────────
SCHEMATIC_SVG = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900">
<style>
  text { font-family: monospace; }
  .lbl { font-size: 11px; fill: #111; }
  .pin { font-size: 9px; fill: #444; }
  .net { font-size: 9px; fill: #1a1aaa; }
  .comp { fill: #f0f4ff; stroke: #2244aa; stroke-width: 1.5; }
  .power-comp { fill: #fff8ee; stroke: #cc6600; stroke-width: 1.5; }
  .sensor { fill: #efffef; stroke: #226622; stroke-width: 1.5; }
  .servo { fill: #fff0ff; stroke: #883388; stroke-width: 1.5; }
  .pwr  { stroke: #cc2222; stroke-width: 2; fill: none; }
  .gnd  { stroke: #226622; stroke-width: 2; fill: none; }
  .sig  { stroke: #2255cc; stroke-width: 1.5; fill: none; }
  .i2c  { stroke: #cc8800; stroke-width: 1.5; fill: none; stroke-dasharray: 6,2; }
  .mot  { stroke: #cc5500; stroke-width: 2; fill: none; }
  .junc { fill: #222; }
  .bus  { stroke: #888; stroke-width: 0.5; fill: none; stroke-dasharray: 2,2; }
</style>

<!-- ── TITLE BLOCK ── -->
<rect x="0" y="0" width="1400" height="900" fill="#fdfcf8"/>
<rect x="10" y="860" width="1380" height="35" fill="#eee" stroke="#999" stroke-width="0.5"/>
<text x="700" y="882" text-anchor="middle" font-size="12" font-weight="bold">
  Biomimetic Shark Robot — Vollständiger Schaltplan | ESP32 + BL-Motor + PCA9685 + MS5837 + MPU6050 | Rev 1.0
</text>

<!-- ══════════════════════════════════════════════════════════════
     KOMPONENTEN
═══════════════════════════════════════════════════════════════ -->

<!-- ── LIPO BATTERY ── -->
<g id="lipo" transform="translate(30,100)">
  <rect x="0" y="0" width="90" height="80" class="power-comp" rx="5"/>
  <text x="45" y="20" text-anchor="middle" class="lbl" font-weight="bold">LiPo 3S</text>
  <text x="45" y="34" text-anchor="middle" class="pin">11.1V 2200mAh</text>
  <text x="45" y="47" text-anchor="middle" class="pin">XT60</text>
  <!-- B+ pin right -->
  <line x1="90" y1="20" x2="110" y2="20" class="pwr"/>
  <text x="112" y="18" class="pin" fill="#cc2222">B+</text>
  <!-- B- pin right -->
  <line x1="90" y1="60" x2="110" y2="60" class="gnd"/>
  <text x="112" y="64" class="pin" fill="#226622">B−</text>
</g>

<!-- ── ESC 20A ── -->
<g id="esc" transform="translate(220,60)">
  <rect x="0" y="0" width="120" height="130" class="comp" rx="5"/>
  <text x="60" y="20" text-anchor="middle" class="lbl" font-weight="bold">ESC 20A</text>
  <text x="60" y="33" text-anchor="middle" class="pin">Hobbywing</text>
  <!-- Input pins left -->
  <line x1="-20" y1="30" x2="0" y2="30" class="pwr"/>
  <text x="-22" y="28" text-anchor="end" class="pin" fill="#cc2222">VIN+</text>
  <line x1="-20" y1="50" x2="0" y2="50" class="gnd"/>
  <text x="-22" y="54" text-anchor="end" class="pin" fill="#226622">GND</text>
  <!-- BEC 5V output -->
  <line x1="120" y1="30" x2="150" y2="30" class="pwr" stroke="#cc6600"/>
  <text x="152" y="28" class="pin" fill="#cc6600">BEC 5V</text>
  <line x1="120" y1="50" x2="150" y2="50" class="gnd"/>
  <text x="152" y="54" class="pin" fill="#226622">BEC GND</text>
  <!-- PWM input -->
  <line x1="-20" y1="80" x2="0" y2="80" class="sig"/>
  <text x="-22" y="78" text-anchor="end" class="pin" fill="#2255cc">PWM IN</text>
  <!-- Motor 3-phase output -->
  <line x1="120" y1="80" x2="150" y2="80" class="mot"/>
  <text x="152" y="78" class="pin" fill="#cc5500">Phase A</text>
  <line x1="120" y1="95" x2="150" y2="95" class="mot"/>
  <text x="152" y="93" class="pin" fill="#cc5500">Phase B</text>
  <line x1="120" y1="110" x2="150" y2="110" class="mot"/>
  <text x="152" y="108" class="pin" fill="#cc5500">Phase C</text>
</g>

<!-- ── BRUSHLESS MOTOR ── -->
<g id="motor" transform="translate(430,70)">
  <rect x="0" y="0" width="110" height="90" class="power-comp" rx="5"/>
  <text x="55" y="22" text-anchor="middle" class="lbl" font-weight="bold">BL Motor</text>
  <text x="55" y="35" text-anchor="middle" class="pin">KV=900</text>
  <text x="55" y="48" text-anchor="middle" class="pin">Outrunner 20W</text>
  <text x="55" y="61" text-anchor="middle" class="pin">Ø35mm</text>
  <!-- 3-phase input -->
  <line x1="-20" y1="30" x2="0" y2="30" class="mot"/>
  <text x="-22" y="28" text-anchor="end" class="pin" fill="#cc5500">Phase A</text>
  <line x1="-20" y1="50" x2="0" y2="50" class="mot"/>
  <text x="-22" y="48" text-anchor="end" class="pin" fill="#cc5500">Phase B</text>
  <line x1="-20" y1="70" x2="0" y2="70" class="mot"/>
  <text x="-22" y="68" text-anchor="end" class="pin" fill="#cc5500">Phase C</text>
  <!-- Shaft output -->
  <line x1="110" y1="45" x2="140" y2="45" stroke="#666" stroke-width="3"/>
  <text x="142" y="43" class="pin">Welle → Getriebe 40:1</text>
</g>

<!-- ── ESP32 DEVKIT V1 ── -->
<g id="esp32" transform="translate(580,200)">
  <rect x="0" y="0" width="160" height="340" class="comp" rx="5"/>
  <text x="80" y="22" text-anchor="middle" class="lbl" font-weight="bold">ESP32 DevKit V1</text>
  <text x="80" y="36" text-anchor="middle" class="pin">240MHz dual-core</text>
  <text x="80" y="48" text-anchor="middle" class="pin">WiFi + Bluetooth</text>

  <!-- LEFT PINS -->
  <text x="5" y="75" class="pin">3V3</text>
  <line x1="0" y1="70" x2="-20" y2="70" class="pwr" stroke="#ff6666"/>

  <text x="5" y="95" class="pin">GND</text>
  <line x1="0" y1="90" x2="-20" y2="90" class="gnd"/>

  <text x="5" y="115" class="pin">VIN</text>
  <line x1="0" y1="110" x2="-20" y2="110" class="pwr" stroke="#cc6600"/>

  <text x="5" y="155" class="pin">GPIO21 SDA</text>
  <line x1="0" y1="150" x2="-20" y2="150" class="i2c"/>

  <text x="5" y="175" class="pin">GPIO22 SCL</text>
  <line x1="0" y1="170" x2="-20" y2="170" class="i2c"/>

  <text x="5" y="215" class="pin">GPIO25 PWM</text>
  <line x1="0" y1="210" x2="-20" y2="210" class="sig"/>

  <!-- RIGHT PINS -->
  <text x="155" y="75" text-anchor="end" class="pin">EN</text>
  <text x="155" y="95" text-anchor="end" class="pin">SVP</text>
  <text x="155" y="115" text-anchor="end" class="pin">SVN</text>
  <text x="155" y="135" text-anchor="end" class="pin">GPIO34</text>
  <text x="155" y="155" text-anchor="end" class="pin">GPIO35</text>
  <text x="155" y="175" text-anchor="end" class="pin">GPIO32</text>
  <text x="155" y="195" text-anchor="end" class="pin">GPIO33</text>
  <text x="155" y="215" text-anchor="end" class="pin">GPIO27</text>
  <text x="155" y="235" text-anchor="end" class="pin">GPIO26</text>
  <text x="155" y="255" text-anchor="end" class="pin">GPIO25</text>
  <text x="155" y="275" text-anchor="end" class="pin">GPIO24</text>

  <line x1="160" y1="250" x2="180" y2="250" class="sig"/>
  <text x="182" y="254" class="pin" fill="#2255cc">→ ESC PWM</text>
</g>

<!-- ── PCA9685 ── -->
<g id="pca9685" transform="translate(200,300)">
  <rect x="0" y="0" width="150" height="200" class="comp" rx="5"/>
  <text x="75" y="22" text-anchor="middle" class="lbl" font-weight="bold">PCA9685</text>
  <text x="75" y="36" text-anchor="middle" class="pin">I2C Servo Driver</text>
  <text x="75" y="49" text-anchor="middle" class="pin">Addr: 0x40</text>

  <!-- Input pins right (to ESP32) -->
  <text x="145" y="75" text-anchor="end" class="pin">SDA</text>
  <line x1="150" y1="70" x2="175" y2="70" class="i2c"/>

  <text x="145" y="95" text-anchor="end" class="pin">SCL</text>
  <line x1="150" y1="90" x2="175" y2="90" class="i2c"/>

  <text x="145" y="115" text-anchor="end" class="pin">VCC 5V</text>
  <line x1="150" y1="110" x2="175" y2="110" class="pwr" stroke="#cc6600"/>

  <text x="145" y="135" text-anchor="end" class="pin">GND</text>
  <line x1="150" y1="130" x2="175" y2="130" class="gnd"/>

  <!-- Output channels left (to servos) -->
  <text x="5" y="155" class="pin">CH2 → BFL</text>
  <line x1="0" y1="150" x2="-20" y2="150" class="sig" stroke="#883388"/>

  <text x="5" y="175" class="pin">CH3 → BFR</text>
  <line x1="0" y1="170" x2="-20" y2="170" class="sig" stroke="#883388"/>

  <text x="5" y="195" class="pin">CH4 → BAL</text>
  <line x1="0" y1="190" x2="-20" y2="190" class="sig" stroke="#883388"/>
</g>

<!-- ── MS5837 PRESSURE SENSOR ── -->
<g id="ms5837" transform="translate(820,180)">
  <rect x="0" y="0" width="140" height="110" class="sensor" rx="5"/>
  <text x="70" y="22" text-anchor="middle" class="lbl" font-weight="bold">MS5837-30BA</text>
  <text x="70" y="36" text-anchor="middle" class="pin">Depth Sensor</text>
  <text x="70" y="49" text-anchor="middle" class="pin">I2C Addr: 0x76</text>
  <text x="70" y="62" text-anchor="middle" class="pin">0−300m / ±2mm</text>

  <!-- Pins left -->
  <text x="5" y="82" class="pin">VCC 3.3V</text>
  <line x1="0" y1="77" x2="-20" y2="77" class="pwr" stroke="#ff6666"/>

  <text x="5" y="97" class="pin">GND</text>
  <line x1="0" y1="92" x2="-20" y2="92" class="gnd"/>

  <text x="5" y="108" class="pin">SDA</text>
  <line x1="0" y1="103" x2="-20" y2="103" class="i2c"/>
  <text x="5" y="118" class="pin">SCL</text>
  <line x1="0" y1="113" x2="-20" y2="113" class="i2c"/>
</g>

<!-- ── MPU-6050 ── -->
<g id="mpu6050" transform="translate(820,340)">
  <rect x="0" y="0" width="140" height="110" class="sensor" rx="5"/>
  <text x="70" y="22" text-anchor="middle" class="lbl" font-weight="bold">MPU-6050</text>
  <text x="70" y="36" text-anchor="middle" class="pin">IMU 6-DOF</text>
  <text x="70" y="49" text-anchor="middle" class="pin">I2C Addr: 0x68</text>
  <text x="70" y="62" text-anchor="middle" class="pin">Gyro + Accel</text>

  <!-- Pins left -->
  <text x="5" y="82" class="pin">VCC 3.3V</text>
  <line x1="0" y1="77" x2="-20" y2="77" class="pwr" stroke="#ff6666"/>

  <text x="5" y="97" class="pin">GND</text>
  <line x1="0" y1="92" x2="-20" y2="92" class="gnd"/>

  <text x="5" y="108" class="pin">SDA</text>
  <line x1="0" y1="103" x2="-20" y2="103" class="i2c"/>
  <text x="5" y="118" class="pin">SCL</text>
  <line x1="0" y1="113" x2="-20" y2="113" class="i2c"/>
</g>

<!-- ── SERVO BRUSTFLOSSE LINKS ── -->
<g id="servo_bfl" transform="translate(30,540)">
  <rect x="0" y="0" width="120" height="70" class="servo" rx="5"/>
  <text x="60" y="20" text-anchor="middle" class="lbl" font-weight="bold">Servo BFL</text>
  <text x="60" y="34" text-anchor="middle" class="pin">MG90S IP67</text>
  <text x="60" y="47" text-anchor="middle" class="pin">Brustflosse L</text>
  <line x1="120" y1="20" x2="145" y2="20" class="sig" stroke="#883388"/>
  <text x="147" y="18" class="pin" fill="#883388">SIG CH2</text>
  <line x1="120" y1="40" x2="145" y2="40" class="pwr" stroke="#cc6600"/>
  <text x="147" y="38" class="pin" fill="#cc6600">+5V</text>
  <line x1="120" y1="60" x2="145" y2="60" class="gnd"/>
  <text x="147" y="64" class="pin" fill="#226622">GND</text>
</g>

<!-- ── SERVO BRUSTFLOSSE RECHTS ── -->
<g id="servo_bfr" transform="translate(30,640)">
  <rect x="0" y="0" width="120" height="70" class="servo" rx="5"/>
  <text x="60" y="20" text-anchor="middle" class="lbl" font-weight="bold">Servo BFR</text>
  <text x="60" y="34" text-anchor="middle" class="pin">MG90S IP67</text>
  <text x="60" y="47" text-anchor="middle" class="pin">Brustflosse R</text>
  <line x1="120" y1="20" x2="145" y2="20" class="sig" stroke="#883388"/>
  <text x="147" y="18" class="pin" fill="#883388">SIG CH3</text>
  <line x1="120" y1="40" x2="145" y2="40" class="pwr" stroke="#cc6600"/>
  <line x1="120" y1="60" x2="145" y2="60" class="gnd"/>
</g>

<!-- ── SERVO BALLAST ── -->
<g id="servo_bal" transform="translate(30,740)">
  <rect x="0" y="0" width="120" height="70" class="servo" rx="5"/>
  <text x="60" y="20" text-anchor="middle" class="lbl" font-weight="bold">Servo Ballast</text>
  <text x="60" y="34" text-anchor="middle" class="pin">MG996R IP67</text>
  <text x="60" y="47" text-anchor="middle" class="pin">15 kg·cm</text>
  <line x1="120" y1="20" x2="145" y2="20" class="sig" stroke="#883388"/>
  <text x="147" y="18" class="pin" fill="#883388">SIG CH4</text>
  <line x1="120" y1="40" x2="145" y2="40" class="pwr" stroke="#cc6600"/>
  <line x1="120" y1="60" x2="145" y2="60" class="gnd"/>
</g>

<!-- ══════════════════════════════════════════════════════════════
     NETS / VERBINDUNGEN
═══════════════════════════════════════════════════════════════ -->

<!-- === POWER RAILS === -->
<!-- LiPo B+ → ESC VIN+ -->
<polyline points="140,120 155,120 155,90 220,90" class="pwr"/>
<!-- LiPo B− → ESC GND -->
<polyline points="140,160 160,160 160,110 220,110" class="gnd"/>

<!-- ESC BEC 5V rail (horizontal bus at y=30) -->
<line x1="370" y1="90" x2="580" y2="90" class="pwr" stroke="#cc6600"/>
<text x="460" y="86" class="net" fill="#cc6600">+5V BEC</text>
<!-- BEC 5V → ESP32 VIN (y=310) -->
<polyline points="580,90 560,90 560,310 580,310" class="pwr" stroke="#cc6600"/>
<!-- BEC 5V → PCA9685 VCC -->
<polyline points="480,90 480,390 375,390 375,410" class="pwr" stroke="#cc6600"/>
<!-- BEC 5V → Servo VCC (bus) -->
<polyline points="370,90 175,90 175,540" class="pwr" stroke="#cc6600" stroke-dasharray="4,2"/>
<text x="177" y="420" class="net" fill="#cc6600">+5V → Servos</text>

<!-- GND common bus -->
<line x1="155" y1="160" x2="155" y2="840" class="gnd"/>
<text x="157" y="500" class="net" fill="#226622">GND Bus</text>
<!-- ESP32 GND → bus -->
<polyline points="580,290 550,290 550,840 155,840" class="gnd"/>
<!-- PCA9685 GND → bus -->
<polyline points="375,430 350,430 350,840" class="gnd"/>
<!-- Sensors GND → bus -->
<polyline points="800,272 785,272 785,840" class="gnd"/>
<polyline points="800,432 785,432 785,840" class="gnd"/>

<!-- ESC Motor phases A/B/C → BL Motor -->
<line x1="370" y1="140" x2="430" y2="140" class="mot"/>
<line x1="370" y1="155" x2="430" y2="155" class="mot"/>
<line x1="370" y1="170" x2="430" y2="170" class="mot"/>

<!-- === SIGNAL: ESP32 GPIO25 → ESC PWM === -->
<polyline points="580,410 540,410 540,210 240,210 240,140" class="sig"/>
<circle cx="540" cy="410" r="4" class="junc"/>
<text x="400" y="207" class="net" fill="#2255cc">GPIO25 PWM</text>

<!-- === I2C BUS (SDA/SCL) === -->
<!-- SDA bus: ESP32 GPIO21 left → PCA / MS5837 / MPU6050 -->
<polyline points="580,350 510,350 510,370 375,370" class="i2c"/>
<text x="430" y="346" class="net" fill="#cc8800">SDA (GPIO21)</text>
<!-- SDA → MS5837 -->
<polyline points="510,350 510,220 800,220" class="i2c"/>
<!-- SDA → MPU6050 -->
<polyline points="510,350 510,383 800,383" class="i2c"/>
<circle cx="510" cy="350" r="4" class="junc"/>

<!-- SCL bus: ESP32 GPIO22 left → PCA / MS5837 / MPU6050 -->
<polyline points="580,370 520,370 520,390 375,390" class="i2c"/>
<text x="430" y="366" class="net" fill="#cc8800">SCL (GPIO22)</text>
<!-- SCL → MS5837 -->
<polyline points="520,370 520,233 800,233" class="i2c"/>
<!-- SCL → MPU6050 -->
<polyline points="520,370 520,393 800,393" class="i2c"/>
<circle cx="520" cy="370" r="4" class="junc"/>

<!-- 3.3V → MS5837 VCC -->
<polyline points="580,270 570,270 570,200 800,200" class="pwr" stroke="#ff6666"/>
<text x="600" y="198" class="net" fill="#ff6666">3V3</text>
<!-- 3.3V → MPU6050 VCC -->
<polyline points="570,270 570,360 800,360" class="pwr" stroke="#ff6666"/>
<circle cx="570" cy="270" r="4" class="junc"/>

<!-- === PCA9685 → SERVOS === -->
<!-- CH2 → BFL -->
<polyline points="200,450 180,450 180,560 175,560" class="sig" stroke="#883388"/>
<text x="183" y="448" class="net" fill="#883388">CH2</text>
<!-- CH3 → BFR -->
<polyline points="200,470 185,470 185,660 175,660" class="sig" stroke="#883388" stroke-dasharray="5,2"/>
<text x="188" y="468" class="net" fill="#883388">CH3</text>
<!-- CH4 → BAL -->
<polyline points="200,490 190,490 190,760 175,760" class="sig" stroke="#883388" stroke-dasharray="3,3"/>
<text x="193" y="488" class="net" fill="#883388">CH4</text>

<!-- ══════════════════════════════════════════════════════════════
     LEGENDE
═══════════════════════════════════════════════════════════════ -->
<rect x="1020" y="100" width="360" height="400" fill="#fffef0" stroke="#999" stroke-width="0.5" rx="4"/>
<text x="1200" y="125" text-anchor="middle" class="lbl" font-weight="bold">LEGENDE</text>

<line x1="1040" y1="150" x2="1090" y2="150" class="pwr"/>
<text x="1095" y="154" class="lbl">+11.1V LiPo</text>

<line x1="1040" y1="175" x2="1090" y2="175" class="pwr" stroke="#cc6600"/>
<text x="1095" y="179" class="lbl">+5V BEC</text>

<line x1="1040" y1="200" x2="1090" y2="200" class="pwr" stroke="#ff6666"/>
<text x="1095" y="204" class="lbl">+3.3V (ESP32)</text>

<line x1="1040" y1="225" x2="1090" y2="225" class="gnd"/>
<text x="1095" y="229" class="lbl">GND</text>

<line x1="1040" y1="250" x2="1090" y2="250" class="sig"/>
<text x="1095" y="254" class="lbl">Signal / PWM</text>

<line x1="1040" y1="275" x2="1090" y2="275" class="i2c"/>
<text x="1095" y="279" class="lbl">I2C (SDA/SCL)</text>

<line x1="1040" y1="300" x2="1090" y2="300" class="mot"/>
<text x="1095" y="304" class="lbl">Motor-Phasen (3-Ph)</text>

<line x1="1040" y1="325" x2="1090" y2="325" class="sig" stroke="#883388"/>
<text x="1095" y="329" class="lbl">Servo-Signal (PCA9685)</text>

<text x="1040" y="360" class="lbl" font-weight="bold">I2C Adressen:</text>
<text x="1040" y="378" class="pin">PCA9685 → 0x40</text>
<text x="1040" y="393" class="pin">MPU-6050 → 0x68</text>
<text x="1040" y="408" class="pin">MS5837  → 0x76</text>
<text x="1040" y="425" class="pin">I2C: SDA=GPIO21, SCL=GPIO22</text>
<text x="1040" y="440" class="pin">PWM ESC: GPIO25 (50Hz)</text>
<text x="1040" y="455" class="pin">BEC: 5V/3A (Servos + Logic)</text>
<text x="1040" y="470" class="pin">Motor: 3-Phase BL KV=900</text>
<text x="1040" y="485" class="pin">Getriebe 40:1 → Nockenwelle</text>

</svg>'''

# ─── Netlist (für Fritzing Konsistenz) ───────────────────────────────────────
NETLIST = {
    "nets": [
        {"name": "VIN_11V", "connections": [
            {"component": "LiPo_3S", "pin": "B+"},
            {"component": "ESC_20A", "pin": "VIN+"}
        ]},
        {"name": "GND", "connections": [
            {"component": "LiPo_3S", "pin": "B-"},
            {"component": "ESC_20A", "pin": "GND"},
            {"component": "ESP32", "pin": "GND"},
            {"component": "PCA9685", "pin": "GND"},
            {"component": "MS5837", "pin": "GND"},
            {"component": "MPU6050", "pin": "GND"},
            {"component": "Servo_BFL", "pin": "GND"},
            {"component": "Servo_BFR", "pin": "GND"},
            {"component": "Servo_BAL", "pin": "GND"}
        ]},
        {"name": "BEC_5V", "connections": [
            {"component": "ESC_20A", "pin": "BEC_5V"},
            {"component": "ESP32", "pin": "VIN"},
            {"component": "PCA9685", "pin": "VCC"},
            {"component": "Servo_BFL", "pin": "VCC"},
            {"component": "Servo_BFR", "pin": "VCC"},
            {"component": "Servo_BAL", "pin": "VCC"}
        ]},
        {"name": "3V3", "connections": [
            {"component": "ESP32", "pin": "3V3"},
            {"component": "MS5837", "pin": "VCC"},
            {"component": "MPU6050", "pin": "VCC"}
        ]},
        {"name": "I2C_SDA", "connections": [
            {"component": "ESP32", "pin": "GPIO21"},
            {"component": "PCA9685", "pin": "SDA"},
            {"component": "MS5837", "pin": "SDA"},
            {"component": "MPU6050", "pin": "SDA"}
        ]},
        {"name": "I2C_SCL", "connections": [
            {"component": "ESP32", "pin": "GPIO22"},
            {"component": "PCA9685", "pin": "SCL"},
            {"component": "MS5837", "pin": "SCL"},
            {"component": "MPU6050", "pin": "SCL"}
        ]},
        {"name": "ESC_PWM", "connections": [
            {"component": "ESP32", "pin": "GPIO25"},
            {"component": "ESC_20A", "pin": "PWM_IN"}
        ]},
        {"name": "SERVO_CH2_BFL", "connections": [
            {"component": "PCA9685", "pin": "CH2"},
            {"component": "Servo_BFL", "pin": "SIGNAL"}
        ]},
        {"name": "SERVO_CH3_BFR", "connections": [
            {"component": "PCA9685", "pin": "CH3"},
            {"component": "Servo_BFR", "pin": "SIGNAL"}
        ]},
        {"name": "SERVO_CH4_BAL", "connections": [
            {"component": "PCA9685", "pin": "CH4"},
            {"component": "Servo_BAL", "pin": "SIGNAL"}
        ]},
        {"name": "MOTOR_PHASE_A", "connections": [
            {"component": "ESC_20A", "pin": "Phase_A"},
            {"component": "BL_Motor", "pin": "Phase_A"}
        ]},
        {"name": "MOTOR_PHASE_B", "connections": [
            {"component": "ESC_20A", "pin": "Phase_B"},
            {"component": "BL_Motor", "pin": "Phase_B"}
        ]},
        {"name": "MOTOR_PHASE_C", "connections": [
            {"component": "ESC_20A", "pin": "Phase_C"},
            {"component": "BL_Motor", "pin": "Phase_C"}
        ]}
    ]
}

# ─── Build .fzz file (ZIP containing XML + SVG) ──────────────────────────────
out_path = '/home/claude/shark/schematics/shark_robot_schematic.fzz'

with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('shark_robot_schematic.fz', SKETCH_XML)
    zf.writestr('schematic/shark_schematic.svg', SCHEMATIC_SVG)
    zf.writestr('netlist.json', json.dumps(NETLIST, indent=2))

print(f"✓ {out_path} ({os.path.getsize(out_path)//1024} KB)")

# Also save standalone SVG for direct viewing
with open('/home/claude/shark/schematics/schaltplan_vollstaendig.svg', 'w') as f:
    f.write(SCHEMATIC_SVG)

print(f"✓ schaltplan_vollstaendig.svg")
