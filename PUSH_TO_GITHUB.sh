#!/bin/bash
# SICHERES PUSH-SKRIPT FÜR GITHUB
# Nutzer: hcousin
# Token wird durch SSH-Authentifizierung ersetzt (sicherer!)

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Biomimetic Shark Robot → GitHub Upload              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 1. GitHub-Repo erstellen
echo "📝 Schritt 1: Gehe zu https://github.com/new"
echo "              und erstelle ein PRIVATES Repository:"
echo "              - Name: biomimetic-shark-robot"
echo "              - Private: JA"
echo "              - Keine README/LICENSE (wir haben schon eins)"
echo ""
read -p "→ Weiter wenn Repository erstellt? (Enter)"

# 2. Repository-URL
read -p "→ Gib deine Repository-URL ein (z.B. git@github.com:hcousin/biomimetic-shark-robot.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ Keine URL eingegeben!"
    exit 1
fi

# 3. Remote hinzufügen
echo ""
echo "🔗 Verbinde mit GitHub..."
git remote add origin "$REPO_URL"

# 4. Push
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Repository ist jetzt auf GitHub:"
    echo "   $REPO_URL"
    echo ""
    echo "🔒 Sicherheit:"
    echo "   - Token wurde NICHT gespeichert"
    echo "   - SSH-Authentifizierung wird verwendet"
    echo "   - Repository ist PRIVAT"
else
    echo ""
    echo "❌ Push fehlgeschlagen!"
    echo "   Prüfe deine SSH-Keys: ssh -T git@github.com"
fi
