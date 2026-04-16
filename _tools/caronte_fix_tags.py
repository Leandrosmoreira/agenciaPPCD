#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARONTE — Fix Tags
Valida e atualiza tags dos videos 009 e 010 via YouTube Data API
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

CREDS_FILE = os.path.expanduser('~/.claude/youtube_oauth_creds.json')
TOKEN_FILE = os.path.expanduser('~/.claude/youtube_token.pickle')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube']

VIDEOS = [
    {
        'id': 'wEJELnPzP-I',
        'nome': 'video-009-anticristo',
        'metadata': r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-009-anticristo\8-publicacao\metadata.txt',
    },
    {
        'id': 'tlQMToRLywU',
        'nome': 'video-010-biblia-etiope',
        'metadata': r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-010-biblia-etiope\8-publicacao\metadata.txt',
    },
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


def parse_tags(metadata_file):
    with open(metadata_file, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'TAGS:' not in content:
        return []
    tags_idx = content.index('TAGS:') + len('TAGS:')
    rest = content[tags_idx:].lstrip()
    for line in rest.split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and ',' in line:
            return [t.strip() for t in line.split(',')][:30]
    return []


def get_current_video(youtube, video_id):
    response = youtube.videos().list(part='snippet,status', id=video_id).execute()
    if not response['items']:
        return None
    return response['items'][0]


def update_tags(youtube, video_id, new_tags, current_snippet):
    snippet = {
        'title': current_snippet['title'],
        'description': current_snippet['description'],
        'tags': new_tags,
        'categoryId': current_snippet.get('categoryId', '27'),
        'defaultLanguage': current_snippet.get('defaultLanguage', 'pt'),
    }
    return youtube.videos().update(
        part='snippet',
        body={'id': video_id, 'snippet': snippet}
    ).execute()


def main():
    print('=' * 60)
    print('CARONTE — Fix Tags (videos 009 + 010)')
    print('=' * 60)

    creds = authenticate()
    youtube = build('youtube', 'v3', credentials=creds)
    print('[OK] Autenticado')
    print()

    for v in VIDEOS:
        print(f'=== {v["nome"]} ({v["id"]}) ===')

        # 1. Buscar estado atual no YouTube
        current = get_current_video(youtube, v['id'])
        if not current:
            print(f'  [ERRO] Video nao encontrado')
            continue

        current_tags = current['snippet'].get('tags', [])
        print(f'  TAGS ATUAIS no YouTube ({len(current_tags)}):')
        for t in current_tags:
            print(f'    - {t}')

        # 2. Parsear tags corretas do metadata.txt
        new_tags = parse_tags(v['metadata'])
        print(f'  TAGS NOVAS do metadata.txt ({len(new_tags)}):')
        for t in new_tags:
            print(f'    - {t}')

        # 3. Atualizar se diferentes
        if current_tags == new_tags:
            print('  [OK] Ja esta correto, nada a atualizar')
        else:
            print('  [UPDATE] Atualizando tags...')
            try:
                update_tags(youtube, v['id'], new_tags, current['snippet'])
                print(f'  [OK] Tags atualizadas ({len(new_tags)} tags)')
            except Exception as e:
                print(f'  [ERRO] Falha: {e}')
        print()


if __name__ == '__main__':
    main()
