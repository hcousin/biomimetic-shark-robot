/*
 * ============================================================
 *  SHARK ROBOT — RS485 TETHER ERWEITERUNG
 *  Ergänzungs-Code für shark_single_motor_firmware.ino
 * ============================================================
 *
 *  Füge dieses Modul hinzu wenn ein Tether-Kabel verwendet wird.
 *
 *  Hardware:
 *    MAX485 Transceiver (TTL <-> RS485)
 *    GPIO 16 = RX (UART2)
 *    GPIO 17 = TX (UART2)
 *    GPIO 4  = DE/RE Control (HIGH=Send, LOW=Receive)
 *
 *  Protokoll (einfaches ASCII):
 *    T1.5\n   → Tiefe setzen: 1.5m
 *    F0.6\n   → Throttle 60%
 *    S\n      → STOP
 *    G\n      → GO
 *    ?\n      → Status abfragen
 *
 *  Antwort:
 *    D:1.23,P:-2.1,T:18.5,F:0.60\n
 *    (Tiefe, Pitch, Temperatur, Throttle)
 *
 *  Kabel-Spezifikation:
 *    4-adrig, 0.5mm², max. 5m Länge
 *    Ader 1+2: GND, +5V (Stromversorgung optional)
 *    Ader 3+4: RS485 A, RS485 B (Daten)
 * ============================================================
 */

#define TETHER_RX   16
#define TETHER_TX   17
#define TETHER_DE   4    // Driver Enable / Receiver Enable

HardwareSerial tetherSerial(2);  // UART2

char tetherBuf[64];
uint8_t tetherIdx = 0;
bool useTether = false;

void tether_init() {
  tetherSerial.begin(115200, SERIAL_8N1, TETHER_RX, TETHER_TX);
  pinMode(TETHER_DE, OUTPUT);
  digitalWrite(TETHER_DE, LOW);  // Receive-Modus
  useTether = true;
  Serial.println("✓ RS485 Tether initialisiert (GPIO16/17, DE=GPIO4)");
}

void tether_send(const char* msg) {
  digitalWrite(TETHER_DE, HIGH);  // Send-Modus
  delayMicroseconds(100);
  tetherSerial.print(msg);
  tetherSerial.print('\n');
  tetherSerial.flush();
  delayMicroseconds(100);
  digitalWrite(TETHER_DE, LOW);   // Receive-Modus
}

void tether_send_telemetry() {
  char buf[64];
  snprintf(buf, sizeof(buf), "D:%.2f,P:%.1f,T:%.1f,F:%.2f",
           depthM, pitchDeg, tempC, motor.throttle);
  tether_send(buf);
}

void tether_parse(const char* cmd) {
  if (cmd[0] == 'T') {
    // Tiefe setzen
    float depth_target = atof(cmd + 1);
    depthPID.setpoint = constrain(depth_target, 0.0f, 10.0f);
    if (depth_target > 0.1f) {
      pectoral.dive_offset = -15.0f;
    }
    Serial.printf("[TETHER] Zieltiefe: %.2fm\n", depthPID.setpoint);
  }
  else if (cmd[0] == 'F') {
    // Throttle setzen
    motor.throttle_set = constrain(atof(cmd + 1), 0.0f, 1.0f);
    Serial.printf("[TETHER] Throttle: %.0f%%\n", motor.throttle_set * 100);
  }
  else if (cmd[0] == 'S') {
    // STOP
    motor.throttle_set = 0.0f;
    depthPID.setpoint = depthM;
    emergencyStop = true;
    Serial.println("[TETHER] STOP");
  }
  else if (cmd[0] == 'G') {
    // GO
    emergencyStop = false;
    Serial.println("[TETHER] GO");
  }
  else if (cmd[0] == '?') {
    // Status-Abfrage
    tether_send_telemetry();
  }
  else if (cmd[0] == 'L') {
    // Links lenken (L15 = 15° offset)
    cpg.steer = constrain(atof(cmd + 1), -20.0f, 20.0f);
  }
  else if (cmd[0] == 'R') {
    // Rechts lenken
    cpg.steer = -constrain(atof(cmd + 1), -20.0f, 20.0f);
  }
}

void tether_read() {
  if (!useTether) return;
  
  while (tetherSerial.available()) {
    char c = tetherSerial.read();
    if (c == '\n' || c == '\r') {
      if (tetherIdx > 0) {
        tetherBuf[tetherIdx] = 0;
        tether_parse(tetherBuf);
        tetherIdx = 0;
      }
    } else if (tetherIdx < sizeof(tetherBuf) - 1) {
      tetherBuf[tetherIdx++] = c;
    }
  }
}

// ─── Hybrid Modus: WiFi + Autonomes Programm ─────────────────────────
// Wird aktiv wenn WiFi-Verbindung verloren geht (Tiefe > 20cm)

struct Mission {
  float depth;        // Zieltiefe [m]
  float throttle;     // Throttle [0-1]
  float steer;        // Lenkoffset [Grad]
  uint32_t duration;  // Dauer [ms]
};

// Beispiel-Mission: Vorwärts, tauchen, kreisen, auftauchen
const Mission DEMO_MISSION[] = {
  {0.0f, 0.4f,  0.0f, 3000},   // Anlaufen an Oberfläche
  {0.8f, 0.5f,  0.0f, 5000},   // Tauchen auf 0.8m
  {0.8f, 0.5f, 10.0f, 4000},   // Linkskurve
  {0.8f, 0.5f,  0.0f, 3000},   // Geradeaus
  {0.0f, 0.3f,  0.0f, 4000},   // Auftauchen
  {0.0f, 0.0f,  0.0f, 0},      // ENDE (duration=0)
};

uint8_t  mission_step = 0;
uint32_t mission_start = 0;
bool     mission_active = false;

void mission_start_demo() {
  mission_step = 0;
  mission_start = millis();
  mission_active = true;
  Serial.println("[MISSION] Demo-Mission gestartet");
}

void mission_update() {
  if (!mission_active) return;
  
  const Mission& m = DEMO_MISSION[mission_step];
  if (m.duration == 0) {
    // Mission beendet
    mission_active = false;
    motor.throttle_set = 0.0f;
    depthPID.setpoint = 0.0f;
    Serial.println("[MISSION] Abgeschlossen");
    return;
  }
  
  // Aktuellen Schritt ausführen
  depthPID.setpoint = m.depth;
  motor.throttle_set = m.throttle;
  cpg.steer = m.steer;
  
  // Zum nächsten Schritt wechseln?
  if (millis() - mission_start >= m.duration) {
    mission_step++;
    mission_start = millis();
    Serial.printf("[MISSION] Schritt %d\n", mission_step);
  }
}

// Aufruf in loop() hinzufügen:
// tether_read();
// mission_update();
// Alle 500ms: if(millis()%500<10) tether_send_telemetry();
