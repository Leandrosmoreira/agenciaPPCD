#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARONTE — Agente de Upload para YouTube
video-009-anticristo | Sinais do Fim
"""

import os
import sys
import json
import pickle
import tempfile
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from caronte_sync_guard import validar_sync_adr008  # ADR-008

# ──────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────

VIDEO_FILE    = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-009-anticristo\7-edicao\0414.mp4'
THUMB_FILE    = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-009-anticristo\8-publicacao\thumb.png'
METADATA_FILE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-009-anticristo\8-publicacao\metadata.txt'
STATUS_FILE   = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-009-anticristo\8-publicacao\status_upload.txt'
LOG_FILE      = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log'

CREDS_FILE = os.path.expanduser('~/.claude/youtube_oauth_creds.json')
TOKEN_FILE = os.path.expanduser('~/.claude/youtube_token.pickle')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube']

# ──────────────────────────────────────────────────────────
# AUTHENTICATE
# ──────────────────────────────────────────────────────────

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_FILE):
                print(f'[ERRO] Credenciais nao encontradas em {CREDS_FILE}')
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

# ──────────────────────────────────────────────────────────
# PARSE METADATA
# ──────────────────────────────────────────────────────────

def parse_metadata():
    metadata = {'titulo': None, 'descricao': None, 'tags': None, 'chapters': []}
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'TÍTULO:' in content:
        titulo_start = content.index('TÍTULO:') + len('TÍTULO:')
        titulo_start = content.find('\n', titulo_start) + 1
        titulo_end = content.find('\n', titulo_start)
        if titulo_end > titulo_start:
            metadata['titulo'] = content[titulo_start:titulo_end].strip()

    if 'DESCRIÇÃO:' in content:
        desc_start = content.index('DESCRIÇÃO:') + len('DESCRIÇÃO:')
        desc_end = content.index('CAPÍTULOS:', desc_start) if 'CAPÍTULOS:' in content else len(content)
        raw_desc = content[desc_start:desc_end].strip()
        metadata['descricao'] = '\n'.join(line for line in raw_desc.split('\n') if line.strip())

    if 'CAPÍTULOS:' in content:
        chapters_start = content.index('CAPÍTULOS:')
        chapters_end = content.index('REFERÊNCIAS', chapters_start) if 'REFERÊNCIAS' in content else len(content)
        chapters_text = content[chapters_start:chapters_end]
        for line in chapters_text.split('\n'):
            line = line.strip()
            if ':' in line and ('-' in line or '—' in line):
                sep = '-' if '-' in line else '—'
                parts = line.split(sep, 1)
                if len(parts) == 2:
                    timestamp = parts[0].strip()
                    title = parts[1].strip()
                    if timestamp and title:
                        metadata['chapters'].append({'timestamp': timestamp, 'title': title})

    # TAGS: pula o ":" inicial e hashtags, pega primeira linha com virgulas
    if 'TAGS:' in content:
        tags_idx = content.index('TAGS:') + len('TAGS:')
        rest = content[tags_idx:].lstrip()
        for line in rest.split('\n'):
            line = line.strip()
            # Linha valida: nao vazia, nao hashtag, contem virgulas (eh lista)
            if line and not line.startswith('#') and ',' in line:
                metadata['tags'] = line
                break

    print(f'[OK] Metadata: {metadata["titulo"][:50]}...')
    return metadata

# ──────────────────────────────────────────────────────────
# UPLOAD VIDEO
# ──────────────────────────────────────────────────────────

def upload_video(youtube, metadata):
    print('[CARONTE] Iniciando upload (3.5 GB — pode demorar)...')
    body = {
        'snippet': {
            'title': metadata['titulo'],
            'description': metadata['descricao'],
            'tags': metadata['tags'].split(',') if metadata['tags'] else [],
            'categoryId': '27',
            'defaultLanguage': 'pt',
            'defaultAudioLanguage': 'pt'
        },
        'status': {
            'privacyStatus': 'private',
            'notifySubscribers': False,
            'madeForKids': False
        }
    }
    media = MediaFileUpload(VIDEO_FILE, chunksize=256*1024*1024, resumable=True, mimetype='video/mp4')
    try:
        request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f'[UPLOAD] {int(status.progress() * 100)}%')
        video_id = response['id']
        print(f'[OK] Video ID: {video_id}')
        return video_id
    except Exception as e:
        print(f'[ERRO] Upload falhou: {e}')
        return None

# ──────────────────────────────────────────────────────────
# THUMBNAIL
# ──────────────────────────────────────────────────────────

def compress_thumbnail(source_file, max_size_bytes=1500000):
    try:
        img = Image.open(source_file)
        if img.mode == 'RGBA':
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])
            img = rgb_img
        temp_fd, temp_file = tempfile.mkstemp(suffix='.jpg')
        os.close(temp_fd)
        quality = 95
        while quality >= 20:
            img.save(temp_file, 'JPEG', quality=quality, optimize=True)
            if os.path.getsize(temp_file) < max_size_bytes:
                print(f'[OK] Thumb comprimida (qualidade {quality}%)')
                return temp_file
            quality -= 5
        os.unlink(temp_file)
        return None
    except Exception as e:
        print(f'[ERRO] Falha ao comprimir thumbnail: {e}')
        return None

def set_thumbnail(youtube, video_id):
    try:
        thumb_compressed = compress_thumbnail(THUMB_FILE)
        if not thumb_compressed:
            return False
        request = youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumb_compressed, mimetype='image/jpeg')
        )
        request.execute()
        os.unlink(thumb_compressed)
        print('[OK] Thumbnail definida')
        return True
    except Exception as e:
        print(f'[ERRO] Thumbnail: {e}')
        return False

# ──────────────────────────────────────────────────────────
# CHAPTERS
# ──────────────────────────────────────────────────────────

def update_description_with_chapters(youtube, video_id, metadata):
    try:
        chapters_text = ''
        if metadata['chapters']:
            chapters_text = '\n\n' + '\n'.join([f"{ch['timestamp']} - {ch['title']}" for ch in metadata['chapters']])
        new_desc = metadata['descricao'] + chapters_text
        if len(new_desc) > 5000:
            new_desc = new_desc[:4950] + '...'
        snippet = {
            'title': metadata['titulo'].strip(),
            'description': new_desc,
            'categoryId': '27',
            'defaultLanguage': 'pt'
        }
        if metadata['tags']:
            snippet['tags'] = [t.strip() for t in metadata['tags'].split(',')][:30]
        youtube.videos().update(part='snippet', body={'id': video_id, 'snippet': snippet}).execute()
        print('[OK] Descricao + chapters atualizados')
        return True
    except Exception as e:
        print(f'[ERRO] Chapters: {e}')
        return False

# ──────────────────────────────────────────────────────────
# SAVE STATUS
# ──────────────────────────────────────────────────────────

def save_status(video_id, thumb_ok, desc_ok):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = f"""VIDEO_ID: {video_id}
URL: https://youtube.com/watch?v={video_id}
STATUS: private
UPLOAD_TIME: {now}
THUMBNAIL: {'OK' if thumb_ok else 'ERRO'}
CHAPTERS: {'OK' if desc_ok else 'ERRO'}
NOTA: Aguardando aprovacao de Snayder para tornar publico
"""
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        f.write(status)
    with open(LOG_FILE, 'a', encoding='utf-8') as lf:
        lf.write(f'[{now}] CARONTE -- Upload OK (PRIVATE) -> {video_id}\n')
        lf.write(f'[{now}] CHECKPOINT -- Aguardando Snayder para publicar\n')
    print(f'[OK] Status salvo')

# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

def main():
    print('='*60)
    print('CARONTE — video-009-anticristo | Sinais do Fim')
    print('='*60)

    if not os.path.exists(VIDEO_FILE):
        print(f'[ERRO] Video nao encontrado: {VIDEO_FILE}')
        return
    print(f'[OK] Video: {os.path.getsize(VIDEO_FILE)/1024/1024:.0f} MB')

    if not os.path.exists(METADATA_FILE):
        print(f'[ERRO] Metadata nao encontrada')
        return

    if not os.path.exists(THUMB_FILE):
        print(f'[ERRO] Thumbnail nao encontrada em: {THUMB_FILE}')
        print('Salve a thumbnail como thumb.jpg na pasta 8-publicacao/')
        return

    # ADR-008: validar sync audio/video antes do upload
    if not validar_sync_adr008(VIDEO_FILE):
        return

    metadata = parse_metadata()
    if not metadata['titulo']:
        print('[ERRO] Titulo vazio')
        return

    creds = authenticate()
    if not creds:
        return
    youtube = build('youtube', 'v3', credentials=creds)
    print('[OK] Autenticado no YouTube')

    video_id = upload_video(youtube, metadata)
    if not video_id:
        return

    thumb_ok = set_thumbnail(youtube, video_id)
    desc_ok = update_description_with_chapters(youtube, video_id, metadata)
    save_status(video_id, thumb_ok, desc_ok)

    print()
    print('='*60)
    print(f'CONCLUIDO — https://youtube.com/watch?v={video_id}')
    print('STATUS: PRIVATE — aguardando Snayder para publicar')
    print('='*60)

if __name__ == '__main__':
    main()
