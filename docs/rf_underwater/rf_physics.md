# RF-Signalübertragung unter Wasser — Physikalische Grundlagen

## Kernprinzip: Skin-Tiefe (Skin Depth)

Elektromagnetische Wellen werden in leitfähigen Medien (wie Wasser) exponentiell gedämpft.
Die charakteristische Eindringtiefe heißt **Skin-Tiefe δ**:

```
δ = 503 × √(ρ / f)

δ  = Skin-Tiefe [m]
ρ  = Spezifischer Widerstand des Wassers [Ω·m]
f  = Frequenz [Hz]
```

Die Signalamplitude fällt ab als:

```
A(d) = A₀ × e^(−d/δ)

Dämpfung in dB: L = 20 × log₁₀(e^(−d/δ)) = −8.686 × d/δ
```

### Wassertypen und Leitfähigkeit

| Wassertyp        | ρ [Ω·m] | σ [S/m] |
|---|---|---|
| Destilliert      | 10'000   | 0.0001  |
| Süßwasser (See)  | ~100     | ~0.01   |
| Brackwasser      | ~10      | ~0.1    |
| Meerwasser       | ~0.2     | ~5      |

---

## Frequenzvergleich (Süßwasser, ρ = 100 Ω·m)

| Frequenz | δ [m] | @0.5 m [dB] | @1.0 m [dB] | @2.0 m [dB] | Urteil |
|---|---|---|---|---|---|
| WiFi 2.4 GHz   | 0.103 | −42  | −85  | −169 | ✗ Unbrauchbar |
| 433 MHz (LoRa) | 0.242 | −18  | −36  | −72  | ✗ Unbrauchbar |
| 27 MHz (RC)    | 0.968 | −4.5 | −9   | −18  | ~ Grenzwertig |
| 3 MHz (HF)     | 2.904 | −1.5 | −3   | −6   | ✓ Brauchbar   |
| 300 kHz (LF)   | 9.183 | −0.5 | −0.9 | −1.9 | ✓ Brauchbar   |

**Faustregel:** Brauchbare Kommunikation erfordert d < 0.5 × δ (max. −8.7 dB).

---

## Warum 433 MHz für 1–2 m scheitert

Bei 433 MHz in Süßwasser: δ = 0.24 m

- Bei 1.0 m Tiefe: Dämpfung = −35.9 dB → Faktor 63× Signalverlust
- Bei 1.5 m Tiefe: Dämpfung = −53.9 dB → Faktor 500× Signalverlust

**Das Signal ist bei 1 m Tiefe praktisch nicht mehr vorhanden.**

---

## Lösungsoptionen für 1–2 m Tiefe

### Option 1: Tether-Kabel (Empfohlen ★★★★★)

```
Spezifikation:
  Kabel:      0.5 mm² 4-adrig, 5 m Länge
  Adern:      2× Strom (GND + 5 V) + 2× Daten (RS485)
  Protokoll:  RS485 / UART, 115200 Baud
  Kosten:     ~15 CHF
  Reichweite: bis 1200 m (RS485-Spezifikation)

Vorteile:
  - Zuverlässig bei jeder Tiefe
  - Niedrige Latenz (<1 ms)
  - Keine RF-Genehmigungen erforderlich
  - Stromversorgung möglich
  
Nachteil:
  - Kabel schränkt Bewegungsfreiheit ein
  - Kabelschleppwiderstand
```

### Option 2: 27-MHz-RC-Modul (Grenzwertig ★★★☆☆)

```
Frequenz:   27.095 MHz (CH1, CEPT-legal)
Skin-Tiefe: 0.97 m in Süßwasser
@1.0 m:     −9 dB → 35 % Signalstärke (grenzwertig)
@1.5 m:     −13.5 dB → 21 % Signalstärke (unzuverlässig)

Antenne:    λ/4 = 2.77 m Drahtantenne
            oder Ferritkern-Antennen (verkürzt)

Empfehlung: Nur für <0.8 m in Süßwasser zuverlässig
```

### Option 3: Hybrid WiFi + Autonomer Modus (★★★★☆)

```
Architektur:
  OBERFLÄCHE (0–0.2 m): WiFi UDP → volles Kommando
  TAUCHPHASE (>0.2 m):  Vorprogrammierte Mission
  
Ablauf:
  1. WiFi: Zieltiefe + Kurs setzen
  2. Hai taucht → WiFi-Signal reißt ab
  3. ESP32 führt gespeicherten Plan autonom aus
  4. Auftauchen → WiFi-Verbindung wiederhergestellt

Vorteil:   Kein Kabel
Nachteil:  Kein Echtzeit-Eingriff unter Wasser
```

### Option 4: Akustische Kommunikation (★★★★☆)

```
Medium:     Schallwellen (nicht RF!)
Frequenz:   20–200 kHz
@2 m:       < −1 dB (sehr gering)

Hardware:   Underwater Acoustic Modem
            z. B. Subnero M25M (~CHF 800)
            oder DIY: HC-SR04 + wasserdichte Piezo-Wandler

Vorteil:    Echtzeitkommunikation bis 100 m Tiefe
Nachteil:   Kosten, Komplexität, Latenz ~50 ms
```

---

## Empfehlung für dieses Projekt

**Für 1–2 m in Süßwasser (Pool/See):**

```
KURZFRISTIG:   Tether-Kabel (4-adrig, RS485)
               → Sofort funktionierend, CHF 15
              
MITTELFRISTIG: Hybrid-Ansatz
               → WiFi-Steuerung an Oberfläche
               → Autonome Tiefenfahrt nach Programm
               → Kein Kabel nötig
              
LANGFRISTIG:   Akustisches Modem (DIY)
               → Echte kabellose Steuerung bei Tiefe
```

---

## Anpassungen an der Firmware

Für den Hybrid-Ansatz benötigt die Firmware:
- Missionsspeicher (Tiefe + Kurs als Sequenz)
- WiFi-Verbindungsstatus-Erkennung
- Autonomen Fallback, wenn WiFi verloren

Für Tether:
- RS485-Transceiver (z. B. MAX485)
- Neuer UART-Handler in Firmware
- Einfaches ASCII-Protokoll: `T0.5` = Tiefe 0.5 m, `F0.6` = Throttle 60 %
