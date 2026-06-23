#!/usr/bin/env python3
"""
sync_issues.py — GitHub Issues → Codeberg Sync (Stufe 2)

Synct Issues, Labels, Kommentare und Status von GitHub nach Codeberg.
Läuft als GitHub Actions Workflow bei issue/issue_comment Events.

Umgebungsvariablen (via GitHub Secrets):
  GH_PAT          GitHub Personal Access Token (repo scope)
  CODEBERG_TOKEN  Codeberg Personal Access Token
  GITHUB_REPO     z.B. "hcousin/biomimetic-shark-robot"
  CODEBERG_REPO   z.B. "hcousin/biomimetic-shark-robot"
"""

import os
import sys
import json
import time
import requests

# ── Konfiguration ────────────────────────────────────────────
GH_TOKEN  = os.environ['GH_PAT']
CB_TOKEN  = os.environ['CODEBERG_TOKEN']
GH_REPO   = os.environ.get('GITHUB_REPO',   'hcousin/biomimetic-shark-robot')
CB_REPO   = os.environ.get('CODEBERG_REPO', 'hcousin/biomimetic-shark-robot')

GH_API = 'https://api.github.com'
CB_API = 'https://codeberg.org/api/v1'

GH_HEADERS = {
    'Authorization': f'token {GH_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}
CB_HEADERS = {
    'Authorization': f'token {CB_TOKEN}',
    'Content-Type': 'application/json'
}

# ── Hilfsfunktionen ──────────────────────────────────────────
def gh_get(path, params=None):
    """GET Request gegen GitHub API."""
    r = requests.get(f'{GH_API}{path}', headers=GH_HEADERS, params=params)
    r.raise_for_status()
    return r.json()

def cb_get(path, params=None):
    """GET Request gegen Codeberg API."""
    r = requests.get(f'{CB_API}{path}', headers=CB_HEADERS, params=params)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

def cb_post(path, data):
    """POST Request gegen Codeberg API."""
    r = requests.post(f'{CB_API}{path}', headers=CB_HEADERS, json=data)
    r.raise_for_status()
    return r.json()

def cb_patch(path, data):
    """PATCH Request gegen Codeberg API."""
    r = requests.patch(f'{CB_API}{path}', headers=CB_HEADERS, json=data)
    r.raise_for_status()
    return r.json()

def rate_limit_wait():
    """Kurze Pause um Rate Limits zu vermeiden."""
    time.sleep(0.5)

# ── Labels ───────────────────────────────────────────────────
def sync_labels():
    """Synct alle Labels von GitHub nach Codeberg."""
    print('🏷️  Synce Labels...')
    gh_labels = gh_get(f'/repos/{GH_REPO}/labels')
    cb_labels = cb_get(f'/repos/{CB_REPO}/labels') or []
    cb_label_names = {l['name'] for l in cb_labels}

    for label in gh_labels:
        if label['name'] not in cb_label_names:
            cb_post(f'/repos/{CB_REPO}/labels', {
                'name':  label['name'],
                'color': label['color'],
                'description': label.get('description', '')
            })
            print(f'  + Label erstellt: {label["name"]}')
            rate_limit_wait()
        else:
            # Update falls Farbe geändert
            cb_label = next(l for l in cb_labels if l['name'] == label['name'])
            if cb_label['color'] != label['color']:
                cb_patch(f'/repos/{CB_REPO}/labels/{cb_label["id"]}', {
                    'color': label['color']
                })
                print(f'  ~ Label aktualisiert: {label["name"]}')
                rate_limit_wait()

# ── Issue-Mapping ─────────────────────────────────────────────
def get_cb_issue_by_title(gh_issue_number, gh_title):
    """
    Findet das entsprechende Codeberg-Issue anhand von Titel-Marker.
    Wir fügen [GH#N] am Anfang des Titels ein als eindeutigen Identifier.
    """
    marker = f'[GH#{gh_issue_number}]'
    page = 1
    while True:
        issues = cb_get(f'/repos/{CB_REPO}/issues',
                        params={'type': 'issues', 'state': 'open', 'page': page, 'limit': 50}) or []
        closed = cb_get(f'/repos/{CB_REPO}/issues',
                        params={'type': 'issues', 'state': 'closed', 'page': page, 'limit': 50}) or []
        all_issues = issues + closed
        if not all_issues:
            break
        for issue in all_issues:
            if issue['title'].startswith(marker):
                return issue
        if len(all_issues) < 100:
            break
        page += 1
    return None

# ── Issue-Body formatieren ────────────────────────────────────
def format_body(gh_issue):
    """Fügt GitHub-Referenz ans Ende des Issue-Body."""
    body = gh_issue.get('body') or ''
    footer = (
        f'\n\n---\n'
        f'*🔗 Gespiegelt von GitHub: '
        f'https://github.com/{GH_REPO}/issues/{gh_issue["number"]}*'
    )
    # Footer nicht doppelt hinzufügen
    if '🔗 Gespiegelt von GitHub' in body:
        return body
    return body + footer

# ── Labels für Codeberg-Issue ermitteln ───────────────────────
def get_label_ids(gh_labels):
    """Ermittelt Codeberg Label-IDs anhand der Label-Namen."""
    cb_labels = cb_get(f'/repos/{CB_REPO}/labels') or []
    cb_label_map = {l['name']: l['id'] for l in cb_labels}
    ids = []
    for label in gh_labels:
        if label['name'] in cb_label_map:
            ids.append(cb_label_map[label['name']])
    return ids

# ── Einzelnes Issue synchronisieren ──────────────────────────
def sync_issue(gh_issue_number):
    """Synchronisiert ein einzelnes GitHub-Issue nach Codeberg."""
    print(f'\n📋 Synce Issue #{gh_issue_number}...')

    # GitHub Issue holen
    gh_issue = gh_get(f'/repos/{GH_REPO}/issues/{gh_issue_number}')

    # Pull Requests überspringen
    if 'pull_request' in gh_issue:
        print(f'  (übersprungen: Pull Request)')
        return

    title   = f'[GH#{gh_issue_number}] {gh_issue["title"]}'
    body    = format_body(gh_issue)
    state   = gh_issue['state']              # 'open' oder 'closed'
    labels  = get_label_ids(gh_issue.get('labels', []))

    # Bestehendes Codeberg-Issue suchen
    cb_issue = get_cb_issue_by_title(gh_issue_number, gh_issue['title'])

    if cb_issue is None:
        # Neues Issue erstellen
        payload = {
            'title':  title,
            'body':   body,
            'labels': labels,
            'closed': state == 'closed'
        }
        cb_issue = cb_post(f'/repos/{CB_REPO}/issues', payload)
        print(f'  ✅ Issue erstellt: #{cb_issue["number"]} — {title}')
    else:
        # Bestehendes Issue aktualisieren
        payload = {
            'title':  title,
            'body':   body,
            'labels': labels,
            'state':  state
        }
        cb_patch(f'/repos/{CB_REPO}/issues/{cb_issue["number"]}', payload)
        print(f'  ~ Issue aktualisiert: #{cb_issue["number"]} — {title}')

    rate_limit_wait()

    # Kommentare synchronisieren
    sync_comments(gh_issue_number, cb_issue['number'])

# ── Kommentare synchronisieren ────────────────────────────────
def sync_comments(gh_issue_number, cb_issue_number):
    """Synchronisiert alle Kommentare eines Issues."""
    print(f'  💬 Synce Kommentare...')

    gh_comments = gh_get(f'/repos/{GH_REPO}/issues/{gh_issue_number}/comments')
    cb_comments = cb_get(f'/repos/{CB_REPO}/issues/{cb_issue_number}/comments') or []

    # Mapping: GitHub-Kommentar-ID → Codeberg-Kommentar
    # Wir speichern die GH-Comment-ID als Marker im Body
    cb_comment_map = {}
    for cc in cb_comments:
        body = cc.get('body', '')
        # Suche nach Marker "<!-- gh_comment_id:12345 -->"
        if '<!-- gh_comment_id:' in body:
            start = body.index('<!-- gh_comment_id:') + len('<!-- gh_comment_id:')
            end   = body.index(' -->', start)
            gh_id = int(body[start:end])
            cb_comment_map[gh_id] = cc

    for gc in gh_comments:
        gh_id   = gc['id']
        author  = gc['user']['login']
        body    = gc.get('body', '')
        marker  = f'<!-- gh_comment_id:{gh_id} -->'
        footer  = f'\n\n*— @{author} auf GitHub*\n{marker}'

        if gh_id not in cb_comment_map:
            # Neuen Kommentar erstellen
            cb_post(f'/repos/{CB_REPO}/issues/{cb_issue_number}/comments', {
                'body': body + footer
            })
            print(f'    + Kommentar erstellt (GH#{gh_id})')
        else:
            # Bestehenden Kommentar aktualisieren falls geändert
            cb_body = cb_comment_map[gh_id].get('body', '')
            new_body = body + footer
            # Nur aktualisieren wenn sich der Inhalt geändert hat
            if cb_body.split('\n\n*— @')[0] != body:
                cb_patch(
                    f'/repos/{CB_REPO}/issues/comments/{cb_comment_map[gh_id]["id"]}',
                    {'body': new_body}
                )
                print(f'    ~ Kommentar aktualisiert (GH#{gh_id})')

        rate_limit_wait()

# ── Alle Issues synchronisieren ───────────────────────────────
def sync_all_issues():
    """Synchronisiert alle GitHub Issues nach Codeberg."""
    print('🔄 Synce alle Issues...')
    page = 1
    while True:
        issues = gh_get(f'/repos/{GH_REPO}/issues',
                        params={'state': 'all', 'page': page, 'per_page': 50})
        if not issues:
            break
        for issue in issues:
            if 'pull_request' not in issue:
                sync_issue(issue['number'])
        if len(issues) < 50:
            break
        page += 1

# ── Hauptprogramm ─────────────────────────────────────────────
if __name__ == '__main__':
    # Modus: 'all' oder Issue-Nummer
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'

    print(f'🦈 Issue Sync: {GH_REPO} → Codeberg/{CB_REPO}')
    print(f'   Modus: {mode}')

    # Labels zuerst synchronisieren
    sync_labels()

    if mode == 'all':
        sync_all_issues()
    else:
        sync_issue(int(mode))

    print('\n✅ Sync abgeschlossen!')
