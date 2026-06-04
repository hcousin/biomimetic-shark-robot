; Exzentrische Nockenwelle — CNC G-Code
; Material: Edelstahl 1.4104
; Rohling: Ø15 mm × 125 mm
; Dreherei-Bearbeitung (nicht 3-Achsen Fräsen!)
; 
; Parameter:
;   R₀ = 8 mm (Mittlerer Radius)
;   e = 3 mm (Exzentrizität)
;   Länge = 120 mm

G21             ; Metrik
G40             ; Radius-Ausgleich aus
G64             ; Standard-Verarbeitung

; Sicherheitsposition
G90 G00 Z10

; Drehbearbeitung (für Drehmaschine!)
; Diese Bearbeitung MUSS auf einer Drehmaschine erfolgen
; oder numerisch gesteuerten Drehmaschine (CNC Lathe)

; Schritt 1: Grobe Bearbeitung — Zylinder Ø12mm drehen
G00 X15 Z5      ; Startposition
G01 Z-120 F100  ; Längsnut 120 mm bei Ø15mm (grob)

; Schritt 2: Exzentrische Form — Nocken-Profil
; Die exzentrische Form wird durch parametrische Drehbearbeitung erzeugt
; Formel: R(θ) = R₀ + e·cos(θ) = 8 + 3·cos(θ)
; 
; Dies erfordert ein Computerprogramm für die Drehmaschine
; oder manuelle Positionierung

; Schritt 3: Achsbohren (Lager-Sitze)
G00 X0 Z0
G01 Z-5 F50     ; Zentrierbohrer
G00 Z10
G01 Z-120 F50   ; Tiefbohrung Ø6mm

; Schritt 4: Ausbalancieren
; Nach der Bearbeitung MUSS die Welle ausbalanciert werden!
; Statisches Auswuchten erforderlich

G00 Z10         ; Sicherheitsposition
M02             ; Programmende

; HINWEIS:
; Dies ist ein VEREINFACHTES Programm!
; Eine echte exzentrische Nockenwelle erfordert:
; 
; 1. Parametrische Drehbearbeitung (CAM-Software)
; 2. Oder: Mehrteil-Nocken (Teile einzeln drehen + Montage)
; 3. Genauigkeit: ±0.1 mm
; 4. Oberflächengüte: Ra 0.8 µm (poliert)
; 5. Material: Edelstahl 1.4104 (korrosionsbeständig)
; 6. Abschluss: Dynamisches Auswuchten

; EMPFOHLENER WORKFLOW:
; → CAD-Datei als STEP exportieren
; → CAM-Software (Fusion 360, Mastercam, CATIA)
; → Post-Processing für Drehmaschinen-Steuerung
; → Bei Dreherei bestellen: "Exzentrische Nockenwelle, Ø12mm, e=3mm"
