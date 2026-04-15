#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARGOS — Twitter OAuth 2.0 com Authorization Code Flow
Autentica uma vez via navegador, salva token, renova automaticamente.
"""

import json
import os
import sqlite3
import secrets
import webbrowser
import requests
import threading
import time
from datetime import datetime, timedelta
from flask import Flask, request
from urllib.parse import urlencode

CREDS_FILE = os.path.expanduser('~/.claude/twitter_creds.json')
DB_FILE    = os.path.expanduser('~/.claude/twitter_oauth.db')
PORT       = 5001
CALLBACK   = f'http://localhost:{PORT}/callback'

SCOPES = 'tweet.read tweet.write users.read offline.access'

# ──────────────────────────────────────────────────────────

def load_creds():
    with open(CREDS_FILE, encoding='utf-8') as f:
        return json.load(f)

# ── DB ────────────────────────────────────────────────────

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY,
        access_token TEXT,
        refresh_token TEXT,
        expires_at TEXT
    )''')
    conn.commit()
    conn.close()

def save_token(access_token, refresh_token, expires_in):
    expires_at = (datetime.now() + timedelta(seconds=expires_in)).isoformat()
    conn = sqlite3.connect(DB_FILE)
    conn.execute('DELETE FROM tokens')
    conn.execute('INSERT INTO tokens (access_token, refresh_token, expires_at) VALUES (?,?,?)',
                 (access_token, refresh_token, expires_at))
    conn.commit()
    conn.close()
    print(f'[OK] Token salvo. Expira em: {expires_at}')

def load_token():
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute('SELECT access_token, refresh_token, expires_at FROM tokens').fetchone()
    conn.close()
    return row  # (access_token, refresh_token, expires_at) ou None

# ── REFRESH ───────────────────────────────────────────────

def refresh_access_token(refresh_token):
    creds = load_creds()
    resp = requests.post(
        'https://api.twitter.com/2/oauth2/token',
        auth=(creds['oauth2_client_id'], creds['oauth2_client_secret']),
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': creds['oauth2_client_id']
        }
    )
    if resp.status_code == 200:
        data = resp.json()
        save_token(data['access_token'], data.get('refresh_token', refresh_token), data.get('expires_in', 7200))
        print('[OK] Token renovado automaticamente')
        return data['access_token']
    else:
        print(f'[ERRO] Falha ao renovar token: {resp.text}')
        return None

# ── GET ACCESS TOKEN ──────────────────────────────────────

def get_access_token():
    init_db()
    row = load_token()

    if row:
        access_token, refresh_token, expires_at = row
        if datetime.now() < datetime.fromisoformat(expires_at):
            print('[OK] Token válido, usando do DB')
            return access_token
        else:
            print('[INFO] Token expirado, renovando...')
            return refresh_access_token(refresh_token)

    # Nenhum token — fazer autorização manual
    print('[INFO] Nenhum token encontrado. Iniciando autorização OAuth 2.0...')
    return authorize()

# ── AUTORIZAÇÃO MANUAL (uma vez) ─────────────────────────

def authorize():
    creds = load_creds()
    state = secrets.token_urlsafe(16)
    code_verifier = secrets.token_urlsafe(43)

    import base64, hashlib
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode()

    auth_url = 'https://twitter.com/i/oauth2/authorize?' + urlencode({
        'response_type': 'code',
        'client_id': creds['oauth2_client_id'],
        'redirect_uri': CALLBACK,
        'scope': SCOPES,
        'state': state,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    })

    # Flask server para capturar callback
    app = Flask(__name__)
    auth_code = {}

    @app.route('/callback')
    def callback():
        auth_code['code'] = request.args.get('code')
        auth_code['state'] = request.args.get('state')
        shutdown = request.environ.get('werkzeug.server.shutdown')
        if shutdown:
            threading.Thread(target=shutdown).start()
        return '<h2>Autorização OK! Pode fechar esta janela.</h2>'

    server = threading.Thread(target=lambda: app.run(port=PORT, debug=False, use_reloader=False))
    server.daemon = True
    server.start()

    print(f'\n[ARGOS] Abrindo navegador para autorizar...')
    print(f'URL: {auth_url}\n')
    webbrowser.open(auth_url)

    # Aguardar callback (120 segundos)
    for _ in range(120):
        if auth_code.get('code'):
            break
        time.sleep(1)

    if not auth_code.get('code'):
        print('[ERRO] Timeout aguardando autorização')
        return None

    # Trocar code por access token
    resp = requests.post(
        'https://api.twitter.com/2/oauth2/token',
        auth=(creds['oauth2_client_id'], creds['oauth2_client_secret']),
        data={
            'code': auth_code['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': CALLBACK,
            'code_verifier': code_verifier
        }
    )

    if resp.status_code == 200:
        data = resp.json()
        save_token(data['access_token'], data.get('refresh_token', ''), data.get('expires_in', 7200))
        return data['access_token']
    else:
        print(f'[ERRO] Falha ao obter token: {resp.text}')
        return None

# ── SEARCH ────────────────────────────────────────────────

def search_tweets(query, access_token, max_results=10):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'query': f'{query} -is:retweet lang:pt',
        'max_results': max_results,
        'tweet.fields': 'public_metrics,created_at'
    }
    resp = requests.get(
        'https://api.twitter.com/2/tweets/search/recent',
        headers=headers,
        params=params,
        timeout=10
    )
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f'[ERRO] {resp.status_code}: {resp.text[:200]}')
        return None

# ── MAIN ──────────────────────────────────────────────────

def main():
    print('='*60)
    print('ARGOS — Twitter OAuth 2.0')
    print('='*60)

    token = get_access_token()
    if not token:
        print('[ERRO] Sem token de acesso')
        return

    topics = ['apocalipse profecia', 'fim dos tempos', 'CBDC moeda digital', 'inteligência artificial perigo']

    print('\n[ARGOS] Buscando trending topics...\n')
    for topic in topics:
        result = search_tweets(topic, token)
        if result and result.get('data'):
            tweets = result['data']
            total_eng = sum(
                t.get('public_metrics', {}).get('like_count', 0) +
                t.get('public_metrics', {}).get('retweet_count', 0)
                for t in tweets
            )
            print(f'{topic}: {len(tweets)} tweets | engagement total: {total_eng}')
            for t in tweets[:2]:
                print(f"  - {t['text'][:80]}")
        else:
            print(f'{topic}: sem resultados')
        print()

if __name__ == '__main__':
    main()
