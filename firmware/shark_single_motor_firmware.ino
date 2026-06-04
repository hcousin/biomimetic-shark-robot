/*
 * ============================================================
 *  BIOMIMETISCHER HAIFISCH — SINGLE MOTOR VERSION
 *  Exzentrische Nockenwelle + BL Motor (ESC)
 * ============================================================
 *
 *  Hardware:
 *    - ESP32 DevKit
 *    - Brushless Outrunner Motor (KV=900)
 *    - ESC 20A mit PWM-Input
 *    - Exzentrische Nockenwelle (mechanisch 4 Gelenke)
 *    - 2× MG90S Brustflossen-Servo
 *    - 1× MG996R Ballast-Servo
 *    - MS5837-30BA Drucksensor
 *    - MPU-6050 IMU
 *
 *  Elektronik:
 *    GPIO 25 → ESC PWM Input (50 Hz, 1000–2000 µs)
 *    I²C 21/22 → Sensoren (MS5837, MPU6050)
 *    SDA/SCL → PCA9685 (optional für weitere Servos)
 *
 *  WICHTIG: Die 4 Gelenke werden REIN MECHANISCH durch
 *  die Nockenwelle angesteuert. Der Code regelt nur:
 *    - Motor-Drehzahl (via ESC PWM)
 *    - Brustflossen-Pitch (IMU-Feedback)
 *    - Tiefe (Ballast-PID)
 * ============================================================
 */

#include <Wire.h>
#include <WiFi.h>
#include <WiFiUdp.h>

// ─── Sensor-Adressen ────────────────────────────────────────
#define MPU6050_ADDR   0x68
#define MS5837_ADDR    0x76

// ─── ESC PWM Output ─────────────────────────────────────────
#define ESC_PIN        25      // PWM für ESC
#define PWM_FREQ       50      // 50 Hz Standard für ESC
#define PWM_RESOLUTION 16      // 16-bit resolution = 0–65535
#define PWM_CHANNEL    0

// PWM-Pulsbreite Grenzen (in µs):
//   1000 µs = 0% Throttle (Stop)
//   1500 µs = Neutral (für bidirektionale ESCs)
//   2000 µs = 100% Throttle (Vollgas)
//
// ESP32 PWM-Berechnung:
//   duty_cycle = (desired_µs / 20000) × 65535
//   z.B. 1500 µs: (1500 / 20000) × 65535 = 4915
#define ESC_MIN_PWM    3276    // 1000 µs
#define ESC_MID_PWM    4915    // 1500 µs (neutral, manche ESCs)
#define ESC_MAX_PWM    6553    // 2000 µs

// ─── Motorsteuerung Parameter ───────────────────────────────
struct MotorControl {
  float throttle      = 0.0f;    // 0.0 – 1.0 (0–100%)
  float throttle_set  = 0.0f;    // Sollwert
  float ramp_rate     = 0.1f;    // Sanfter Anfahrt (pro Schleife)
  uint16_t pwm_out    = ESC_MIN_PWM;
  
  // RPM-Feedback (optional mit Encoder)
  float rpm           = 0.0f;
  float freq_swim     = 0.0f;    // Berechnete Schwimmfrequenz
} motor;

// ─── Tiefenregler & Ballast ─────────────────────────────────
struct PIDState {
  float kp          = 1.4f;
  float ki          = 0.25f;
  float kd          = 0.08f;
  float setpoint    = 0.0f;
  float integral    = 0.0f;
  float prevError   = 0.0f;
  float output      = 0.0f;
} depthPID;

uint8_t ballastPos  = 90;

// ─── Sensorwerte ────────────────────────────────────────────
float depthM        = 0.0f;
float pitchDeg      = 0.0f;
float rollDeg       = 0.0f;
float tempC         = 20.0f;

// ─── MS5837 PROM ────────────────────────────────────────────
uint16_t ms5837_C[7] = {0};

// ─── Brustflossen-Pitch-Korrektur ───────────────────────────
struct PectoralControl {
  float pitch_left   = 0.0f;
  float pitch_right  = 0.0f;
  float imr_damp     = 0.3f;    // IMU Rückkopplung Faktor
  float dive_offset  = 0.0f;    // Tauchen-Offset
} pectoral;

// ─── Zeitsteuerung ──────────────────────────────────────────
unsigned long lastSensor  = 0;
unsigned long lastPID     = 0;
unsigned long lastTelem   = 0;
const uint32_t SENSOR_DT_MS = 50;   // 20 Hz
const uint32_t PID_DT_MS    = 50;   // 20 Hz
const uint32_t TELEM_DT_MS  = 500;  // 2 Hz Telemetrie

bool emergencyStop = false;

// ─── WiFi UDP ───────────────────────────────────────────────
const char* WIFI_SSID  = "SharkControl";
const char* WIFI_PASS  = "haifisch2024";
WiFiUDP udp;
char udpBuf[256];

// ════════════════════════════════════════════════════════════
//  MPU-6050
// ════════════════════════════════════════════════════════════
void mpu_init() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x6B); Wire.write(0x00);   // Wake up
  Wire.endTransmission();
}

void mpu_read() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x3B); Wire.endTransmission(false);
  Wire.requestFrom(MPU6050_ADDR, 6, true);
  int16_t ax = (Wire.read()<<8)|Wire.read();
  int16_t ay = (Wire.read()<<8)|Wire.read();
  int16_t az = (Wire.read()<<8)|Wire.read();
  
  pitchDeg = atan2f((float)ay, (float)az) * 57.296f;
  rollDeg  = atan2f((float)ax, (float)az) * 57.296f;
}

// ════════════════════════════════════════════════════════════
//  MS5837-30BA Drucksensor
// ════════════════════════════════════════════════════════════
void ms5837_init() {
  Wire.beginTransmission(MS5837_ADDR);
  Wire.write(0x1E); Wire.endTransmission();
  delay(10);
  
  for (uint8_t i = 1; i <= 6; i++) {
    Wire.beginTransmission(MS5837_ADDR);
    Wire.write(0xA0 + i * 2);
    Wire.endTransmission();
    Wire.requestFrom(MS5837_ADDR, 2, true);
    ms5837_C[i] = ((uint16_t)Wire.read() << 8) | Wire.read();
  }
}

uint32_t ms5837_readADC(uint8_t cmd) {
  Wire.beginTransmission(MS5837_ADDR);
  Wire.write(cmd); Wire.endTransmission();
  delay(3);
  Wire.beginTransmission(MS5837_ADDR);
  Wire.write(0x00); Wire.endTransmission();
  Wire.requestFrom(MS5837_ADDR, 3, true);
  return ((uint32_t)Wire.read()<<16)|((uint32_t)Wire.read()<<8)|Wire.read();
}

void ms5837_read() {
  uint32_t D1 = ms5837_readADC(0x40);
  uint32_t D2 = ms5837_readADC(0x50);
  
  int32_t dT   = (int32_t)D2 - ((int32_t)ms5837_C[5] << 8);
  tempC        = 20.0f + dT * ms5837_C[6] / 8388608.0f;
  int64_t OFF  = ((int64_t)ms5837_C[2] << 16) + ((int64_t)ms5837_C[4] * dT >> 7);
  int64_t SENS = ((int64_t)ms5837_C[1] << 15) + ((int64_t)ms5837_C[3] * dT >> 8);
  float pressureMbar = ((D1 * SENS / 2097152.0f - OFF) / 32768.0f) / 100.0f;
  depthM = (pressureMbar - 1013.25f) / (1025.0f * 9.80665f / 100.0f);
  depthM = max(depthM, 0.0f);
}

// ════════════════════════════════════════════════════════════
//  Motor ESC PWM Control
// ════════════════════════════════════════════════════════════
void motor_init() {
  ledcSetup(PWM_CHANNEL, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(ESC_PIN, PWM_CHANNEL);
  ledcWrite(PWM_CHANNEL, ESC_MIN_PWM);  // Start at 0%
  delay(500);
}

void motor_update(float dt_s) {
  // Sanfte Beschleunigung (Ramping)
  float diff = motor.throttle_set - motor.throttle;
  if (abs(diff) > 0.01f) {
    motor.throttle += constrain(diff, -motor.ramp_rate * dt_s, motor.ramp_rate * dt_s);
  } else {
    motor.throttle = motor.throttle_set;
  }
  
  // Throttle [0,1] → PWM Duty
  // Linear Mapping: 0% → ESC_MIN_PWM, 100% → ESC_MAX_PWM
  motor.pwm_out = (uint16_t)(ESC_MIN_PWM + motor.throttle * (ESC_MAX_PWM - ESC_MIN_PWM));
  
  // Berechne geschätzte Schwimmfrequenz
  // Motor RPM = throttle × max_rpm = throttle × 9990
  // Mit Getriebe 40:1 → Nockenwellen-RPM = Motor_RPM / 40
  // Frequenz = Nockenwellen-RPM / 60
  float motor_rpm = motor.throttle * 9990.0f;
  float nocke_rpm = motor_rpm / 40.0f;
  motor.freq_swim = nocke_rpm / 60.0f;
  
  // PWM Ausgabe
  ledcWrite(PWM_CHANNEL, motor.pwm_out);
}

// ════════════════════════════════════════════════════════════
//  PID Tiefenregler
// ════════════════════════════════════════════════════════════
void runDepthPID(float dt_s) {
  float error = depthPID.setpoint - depthM;
  depthPID.integral  += error * dt_s;
  depthPID.integral   = constrain(depthPID.integral, -5.0f, 5.0f);
  float derivative    = (error - depthPID.prevError) / dt_s;
  depthPID.prevError  = error;
  depthPID.output     = depthPID.kp * error
                      + depthPID.ki * depthPID.integral
                      + depthPID.kd * derivative;
  
  ballastPos = (int)constrain(90.0f + depthPID.output * 8.0f, 70.0f, 110.0f);
}

// ════════════════════════════════════════════════════════════
//  Brustflossen-Steuerung (IMU-Feedback)
// ════════════════════════════════════════════════════════════
void updatePectoralFins() {
  // Pitch-Korrektur: Wenn Hai zu steil (Pitch > 10°), Brustflossen korrigieren
  float pitch_corr = pitchDeg * pectoral.imr_damp;
  
  pectoral.pitch_left  = -pitch_corr + pectoral.dive_offset;
  pectoral.pitch_right = -pitch_corr + pectoral.dive_offset;
  
  // Grenzen
  pectoral.pitch_left  = constrain(pectoral.pitch_left, -25.0f, 25.0f);
  pectoral.pitch_right = constrain(pectoral.pitch_right, -25.0f, 25.0f);
}

// ════════════════════════════════════════════════════════════
//  UDP Kommando-Parser
// ════════════════════════════════════════════════════════════
void parseUDP() {
  int len = udp.parsePacket();
  if (!len) return;
  
  udp.read((uint8_t*)udpBuf, sizeof(udpBuf)-1);
  udpBuf[len] = 0;
  
  // Einfacher Text-Parser (kein JSON nötig für Single Motor)
  // Format: "THROTTLE 0.5"  oder "DEPTH 1.0"  oder "STOP"
  
  String s(udpBuf);
  s.toUpperCase();
  
  if (s.startsWith("THROTTLE ")) {
    motor.throttle_set = constrain(s.substring(9).toFloat(), 0.0f, 1.0f);
    Serial.print("Throttle set to: "); Serial.println(motor.throttle_set);
  }
  else if (s.startsWith("DEPTH ")) {
    depthPID.setpoint = constrain(s.substring(6).toFloat(), 0.0f, 10.0f);
    pectoral.dive_offset = -15.0f;  // Brustflossen für Tauchen
    Serial.print("Target depth: "); Serial.println(depthPID.setpoint);
  }
  else if (s == "SURFACE") {
    depthPID.setpoint = 0.0f;
    pectoral.dive_offset = 0.0f;
    Serial.println("Ascending...");
  }
  else if (s == "STOP") {
    motor.throttle_set = 0.0f;
    depthPID.setpoint = depthM;
    emergencyStop = true;
    Serial.println("EMERGENCY STOP");
  }
  else if (s == "GO") {
    emergencyStop = false;
    Serial.println("Resume");
  }
  
  // Telemetrie-Rückmeldung
  char reply[128];
  snprintf(reply, sizeof(reply),
    "DEPTH:%.2f,PITCH:%.1f,MOTOR:%.1f%%,FREQ:%.2fHz",
    depthM, pitchDeg, motor.throttle*100.0f, motor.freq_swim);
  udp.beginPacket(udp.remoteIP(), udp.remotePort());
  udp.print(reply);
  udp.endPacket();
}

// ════════════════════════════════════════════════════════════
//  Serial Debug Interface
// ════════════════════════════════════════════════════════════
void parseSerial() {
  if (!Serial.available()) return;
  String s = Serial.readStringUntil('\n');
  s.trim();
  
  if (s == "status") {
    Serial.printf("DEPTH: %.2f m | PITCH: %.1f° | TEMP: %.1f°C\n", depthM, pitchDeg, tempC);
    Serial.printf("MOTOR: %.0f%% Throttle | Freq: %.2f Hz | RPM: %.0f\n",
                  motor.throttle*100.0f, motor.freq_swim, motor.throttle * 9990.0f);
    Serial.printf("Ballast: %d | Pect-L: %.1f° | Pect-R: %.1f°\n",
                  ballastPos, pectoral.pitch_left, pectoral.pitch_right);
  }
  else if (s.startsWith("throttle ")) {
    motor.throttle_set = constrain(s.substring(9).toFloat(), 0.0f, 1.0f);
    Serial.println("Throttle OK");
  }
  else if (s.startsWith("depth ")) {
    depthPID.setpoint = s.substring(6).toFloat();
    pectoral.dive_offset = -15.0f;
    Serial.println("Diving...");
  }
  else if (s == "?") {
    Serial.println("Commands: status | throttle X(0-1) | depth X(m) | stop | go");
  }
}

// ════════════════════════════════════════════════════════════
//  SETUP
// ════════════════════════════════════════════════════════════
void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  Wire.setClock(400000);
  
  Serial.println("\n╔═══════════════════════════════════════════╗");
  Serial.println("║  HAIFISCH-ROBOTER — SINGLE MOTOR v1.0   ║");
  Serial.println("║  Exzentrische Nockenwelle                ║");
  Serial.println("╚═══════════════════════════════════════════╝\n");
  
  motor_init();
  Serial.println("✓ ESC PWM initialized (Pin 25)");
  
  mpu_init();
  Serial.println("✓ MPU-6050 OK");
  
  ms5837_init();
  Serial.println("✓ MS5837 OK");
  
  // WiFi
  WiFi.softAP(WIFI_SSID, WIFI_PASS);
  udp.begin(4210);
  Serial.print("✓ WiFi AP: "); Serial.print(WIFI_SSID);
  Serial.print(" | IP: "); Serial.println(WiFi.softAPIP());
  
  Serial.println("\n[Ready] Tippe '?' für Befehle.\n");
}

// ════════════════════════════════════════════════════════════
//  HAUPTSCHLEIFE
// ════════════════════════════════════════════════════════════
void loop() {
  uint32_t now = millis();
  static float loop_dt = 0.01f;
  
  // 1. Sensor-Update @ 20 Hz
  if (now - lastSensor >= SENSOR_DT_MS) {
    lastSensor = now;
    mpu_read();
    ms5837_read();
  }
  
  // 2. Motor-Update (kontinuierlich, aber dt begrenzt)
  static uint32_t lastMotor = 0;
  if (now - lastMotor >= 10) {
    lastMotor = now;
    motor_update(0.01f);
  }
  
  // 3. Brustflossen-Update
  updatePectoralFins();
  
  // 4. PID @ 20 Hz
  if (now - lastPID >= PID_DT_MS) {
    lastPID = now;
    runDepthPID((float)PID_DT_MS / 1000.0f);
  }
  
  // 5. Telemetrie @ 2 Hz
  if (now - lastTelem >= TELEM_DT_MS) {
    lastTelem = now;
    Serial.printf("[%lu] T:%.0f%% f:%.2fHz D:%.2fm P:%.1f°\n",
                  now/1000, motor.throttle*100, motor.freq_swim, depthM, pitchDeg);
  }
  
  // 6. Kommunikation
  parseUDP();
  parseSerial();
  
  delay(5);
}
