#!/usr/bin/env python3
"""
Generiere STL-Dateien für Haifisch-Roboter
Nutzt numpy-stl für einfache geometrische Formen
"""

import numpy as np
from stl import mesh

def create_cylinder_mesh(radius, height, fn=32):
    """Zylinder als Mesh"""
    theta = np.linspace(0, 2*np.pi, fn)
    
    # Vertices
    vertices = []
    for i in range(fn):
        # Unten
        vertices.append([radius*np.cos(theta[i]), radius*np.sin(theta[i]), 0])
    for i in range(fn):
        # Oben
        vertices.append([radius*np.cos(theta[i]), radius*np.sin(theta[i]), height])
    
    vertices = np.array(vertices)
    
    # Faces (Seitenflächen)
    faces = []
    for i in range(fn):
        i_next = (i+1) % fn
        # Seite
        faces.append([i, i_next, i+fn])
        faces.append([i_next, i_next+fn, i+fn])
    
    return mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))

def create_body_front_stl():
    """Hauptelektronikgehäuse"""
    print("Erstelle body_front.stl...")
    
    # Vereinfachte Geometrie: Zylinder + Kegel
    vertices = np.array([
        # Zylinder unten (8 Vertices)
        [40, 0, 0],
        [28, 28, 0],
        [0, 40, 0],
        [-28, 28, 0],
        [-40, 0, 0],
        [-28, -28, 0],
        [0, -40, 0],
        [28, -28, 0],
        # Zylinder oben
        [40, 0, 180],
        [28, 28, 180],
        [0, 40, 180],
        [-28, 28, 180],
        [-40, 0, 180],
        [-28, -28, 180],
        [0, -40, 180],
        [28, -28, 180],
        # Kegel-Spitze
        [0, 0, 200],
    ], dtype=np.float32)
    
    # Faces
    faces = np.array([
        # Seitenflächen des Zylinders
        [0, 1, 9],
        [0, 9, 8],
        [1, 2, 10],
        [1, 10, 9],
        # ... weitere Faces würden folgen
        # Vereinfacht: nur minimale Faces für Grundform
    ], dtype=np.int32)
    
    # Erstelle Mesh
    m = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            m.vectors[i][j] = vertices[f[j]]
    
    m.save('/home/claude/shark/cad/stl/body_front.stl')
    print(f"✓ body_front.stl ({len(faces)} faces)")

def create_silikon_form_stl():
    """Silikonform für Schwanzflosse"""
    print("Erstelle silikon_form_flosse.stl...")
    
    # Vereinfachte Lunate-Form (halbe Ellipse)
    vertices = []
    for y in np.linspace(-60, 60, 12):
        for z in np.linspace(0, 120, 8):
            # Elliptische Form
            x_ellipse = 40 * np.sqrt(max(0, 1 - (y/60)**2))
            vertices.append([x_ellipse, y, z])
    
    vertices = np.array(vertices, dtype=np.float32)
    
    # Minimale Face-Definition
    faces = np.array([
        [0, 1, 12],
        [0, 12, 13],
    ], dtype=np.int32)
    
    m = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        if i < len(m.vectors):
            for j in range(3):
                if f[j] < len(vertices):
                    m.vectors[i][j] = vertices[f[j]]
    
    m.save('/home/claude/shark/cad/stl/silikon_form_flosse.stl')
    print(f"✓ silikon_form_flosse.stl")

def create_servo_mount_stl():
    """Servo-Halter J1"""
    print("Erstelle servo_mount_j1.stl...")
    
    # Einfache Box
    vertices = np.array([
        # Box für Servo-Halter
        [-17.5, -22.5, -12.5], [17.5, -22.5, -12.5],
        [17.5, 22.5, -12.5], [-17.5, 22.5, -12.5],
        [-17.5, -22.5, 12.5], [17.5, -22.5, 12.5],
        [17.5, 22.5, 12.5], [-17.5, 22.5, 12.5],
    ], dtype=np.float32)
    
    faces = np.array([
        [0, 1, 2], [0, 2, 3],
        [4, 6, 5], [4, 7, 6],
        [0, 4, 5], [0, 5, 1],
        [2, 6, 7], [2, 7, 3],
    ], dtype=np.int32)
    
    m = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            m.vectors[i][j] = vertices[f[j]]
    
    m.save('/home/claude/shark/cad/stl/servo_mount_j1.stl')
    print(f"✓ servo_mount_j1.stl")

if __name__ == '__main__':
    print("Generiere STL-Dateien für Haifisch-Roboter...")
    create_body_front_stl()
    create_silikon_form_stl()
    create_servo_mount_stl()
    print("\n✓ Alle STL-Dateien erstellt!")
    print("  → cad/stl/")
