; Ballast-Spritze — 3D-Druck Adapter (optional)
; Nicht für CNC — nur für 3D-Druck!
; Siehe stl/ballast_syringe_adapter.stl

G21
M104 S210       ; Heizblock 210°C (PETG)
M109 S60        ; Bett 60°C
G28             ; Home
G92 E0
G1 F9000 E-2    ; Retract

M109 S60        ; Temperaturwarte
M104 S0         ; Heizblock aus

M02
