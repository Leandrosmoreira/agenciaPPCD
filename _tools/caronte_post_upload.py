#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARONTE — Post Upload
Aplica configuracoes obrigatorias pos-upload:
  1. Adiciona video a playlist "Apocalipse"
  2. Marca "Conteudo alterado/sintetico" = Sim
  3. Valida tags (deve ter >= 10)

Uso:
  python _tools/caronte_post_upload.py <video_id> [<video_id>...]
  python _tools/caronte_post_upload.py --all   (aplica nos videos 009 e 010)
"""

import os
import sys
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

CREDS_FILE = os.path.expanduser('~/.claude/youtube_oauth_creds.json')
TOKEN_FILE = os.path.expanduser('~/.claude/youtube_token.pickle')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube']

PLAYLIST_NAME = 'Apocalipse'

DEFAULT_VIDEOS = [
    'wEJELnPzP-I',  # video-009-anticristo
    'tlQMToRLywU',  # video-010-biblia-etiope
]


def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def find_playlist(youtube, playlist_name):
    """Busca playlist pelo nome no canal autenticado."""
    next_page = None
    while True:
        kwargs = {'part': 'snippet', 'mine': True, 'maxResults': 50}
        if next_page:
            kwargs['pageToken'] = next_page
        resp = youtube.playlists().list(**kwargs).execute()
        for item in resp.get('items', []):
            if item['snippet']['title'].lower() == playlist_name.lower():
                return item['id']
        next_page = resp.get('nextPageToken')
        if not next_page:
            break
    return None


def video_in_playlist(youtube, playlist_id, video_id):
    """Verifica se video ja esta na playlist."""
    next_page = None
    while True:
        kwargs = {'part': 'contentDetails', 'playlistId': playlist_id, 'maxResults': 50}
        if next_page:
            kwargs['pageToken'] = next_page
        resp = youtube.playlistItems().list(**kwargs).execute()
        for item in resp.get('items', []):
            if item['contentDetails']['videoId'] == video_id:
                return True
        next_page = resp.get('nextPageToken')
        if not next_page:
            break
    return False


def add_to_playlist(youtube, playlist_id, video_id):
    """Adiciona video a playlist."""
    body = {
        'snippet': {
            'playlistId': playlist_id,
            'resourceId': {
                'kind': 'youtube#video',
                'videoId': video_id,
            }
        }
    }
    return youtube.playlistItems().insert(part='snippet', body=body).execute()


def mark_synthetic_media(youtube, video_id):
    """Marca video como conteudo alterado/sintetico (IA)."""
    # Busca status atual para nao sobrescrever outros campos
    resp = youtube.videos().list(part='status', id=video_id).execute()
    if not resp['items']:
        return False
    current_status = resp['items'][0]['status']

    # Monta novo status preservando campos existentes
    new_status = {
        'privacyStatus': current_status.get('privacyStatus', 'private'),
        'selfDeclaredMadeForKids': current_status.get('selfDeclaredMadeForKids', False),
        'containsSyntheticMedia': True,
    }
    if 'license' in current_status:
        new_status['license'] = current_status['license']
    if 'embeddable' in current_status:
        new_status['embeddable'] = current_status['embeddable']
    if 'publicStatsViewable' in current_status:
        new_status['publicStatsViewable'] = current_status['publicStatsViewable']

    return youtube.videos().update(
        part='status',
        body={'id': video_id, 'status': new_status}
    ).execute()


def validate_tags(youtube, video_id):
    resp = youtube.videos().list(part='snippet', id=video_id).execute()
    if not resp['items']:
        return None
    return resp['items'][0]['snippet'].get('tags', [])


def process_video(youtube, playlist_id, video_id):
    print(f'=== {video_id} ===')

    # 1. Tags
    tags = validate_tags(youtube, video_id)
    n_tags = len(tags) if tags else 0
    marker = 'OK' if n_tags >= 10 else 'WARN'
    print(f'  [{marker}] Tags: {n_tags}')

    # 2. Playlist
    if video_in_playlist(youtube, playlist_id, video_id):
        print(f'  [OK] Ja esta na playlist "{PLAYLIST_NAME}"')
    else:
        try:
            add_to_playlist(youtube, playlist_id, video_id)
            print(f'  [OK] Adicionado a playlist "{PLAYLIST_NAME}"')
        except Exception as e:
            print(f'  [ERRO] Falha ao adicionar a playlist: {e}')

    # 3. Synthetic media
    try:
        result = mark_synthetic_media(youtube, video_id)
        if result:
            flag = result.get('status', {}).get('containsSyntheticMedia', False)
            print(f'  [OK] containsSyntheticMedia = {flag}')
        else:
            print(f'  [ERRO] Video nao encontrado ao marcar sintetico')
    except Exception as e:
        print(f'  [ERRO] Falha ao marcar sintetico: {e}')

    print()


def main():
    print('=' * 60)
    print(f'CARONTE — Post Upload (playlist + synthetic + tags)')
    print('=' * 60)

    if len(sys.argv) < 2:
        print('Uso: python caronte_post_upload.py <video_id> [<video_id>...]')
        print('     python caronte_post_upload.py --all')
        sys.exit(1)

    if sys.argv[1] == '--all':
        videos = DEFAULT_VIDEOS
    else:
        videos = sys.argv[1:]

    creds = authenticate()
    youtube = build('youtube', 'v3', credentials=creds)
    print('[OK] Autenticado')

    playlist_id = find_playlist(youtube, PLAYLIST_NAME)
    if not playlist_id:
        print(f'[ERRO] Playlist "{PLAYLIST_NAME}" nao encontrada no canal')
        sys.exit(1)
    print(f'[OK] Playlist "{PLAYLIST_NAME}" ID: {playlist_id}')
    print()

    for vid in videos:
        process_video(youtube, playlist_id, vid)

    print('=' * 60)
    print('CONCLUIDO')
    print('=' * 60)


if __name__ == '__main__':
    main()
