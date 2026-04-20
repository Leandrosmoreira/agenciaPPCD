#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARONTE — Agente de Upload para YouTube
video-015-economist-manipulacao | Sinais do Fim
NOTA: Video editado no CapCut (nao MoviePy) — ADR-008 sync guard desativado.
"""

import os
import json
import pickle
import sys
import tempfile
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import Image

# ──────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────

BASE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-015-economist-manipulacao'

VIDEO_FILE    = os.path.join(BASE, r'8-publicacao\0418.mp4')
THUMB_FILE    = os.path.join(BASE, r'8-publicacao\Antichrist – Daniel 927 (6).png')
METADATA_FILE = os.path.join(BASE, r'8-publicacao\metadata.txt')
STATUS_FILE   = os.path.join(BASE, r'8-publicacao\status_upload.txt')
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

    # Título
    if 'TÍTULO:' in content:
        start = content.index('TÍTULO:') + len('TÍTULO:')
        start = content.find('\n', start) + 1
        end   = content.find('\n', start)
        metadata['titulo'] = content[start:end].strip()

    # Descrição
    if 'DESCRIÇÃO:' in content:
        desc_start = content.index('DESCRIÇÃO:') + len('DESCRIÇÃO:')
        desc_end   = content.index('CAPÍTULOS:', desc_start) if 'CAPÍTULOS:' in content else len(content)
        raw = content[desc_start:desc_end].strip()
        metadata['descricao'] = '\n'.join(l for l in raw.split('\n') if l.strip())

    # Chapters
    if 'CAPÍTULOS:' in content:
        ch_start = content.index('CAPÍTULOS:')
        ch_end   = content.index('REFERÊNCIAS', ch_start) if 'REFERÊNCIAS' in content else len(content)
        for line in content[ch_start:ch_end].split('\n'):
            line = line.strip()
            if ':' in line and ('-' in line or '—' in line):
                sep   = '-' if '-' in line else '—'
                parts = line.split(sep, 1)
                if len(parts) == 2:
                    ts, title = parts[0].strip(), parts[1].strip()
                    if ts and title:
                        metadata['chapters'].append({'timestamp': ts, 'title': title})

    # Tags
    if 'TAGS:' in content:
        idx  = content.index('TAGS:') + len('TAGS:')
        rest = content[idx:].lstrip()
        for line in rest.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and ',' in line:
                metadata['tags'] = line
                break

    print(f'[OK] Metadata: {metadata["titulo"][:50] if metadata["titulo"] else "ERRO"}')
    return metadata

# ──────────────────────────────────────────────────────────
# UPLOAD VIDEO
# ──────────────────────────────────────────────────────────

def upload_video(youtube, metadata):
    print('[CARONTE] Iniciando upload (2.88 GB — pode demorar)...')
    # Sanitizar tags: strip, normalizar Unicode→ASCII, total ≤ 500 chars
    import unicodedata, re as _re
    def _ascii_tag(t):
        t = unicodedata.normalize('NFKD', t)
        t = t.encode('ascii', 'ignore').decode('ascii')
        t = _re.sub(r'[^\w\s]', '', t).strip()
        return t
    raw_tags = [_ascii_tag(t.strip()) for t in (metadata['tags'] or '').split(',') if t.strip()]
    raw_tags = [t for t in raw_tags if t and len(t) <= 100]
    safe_tags, total = [], 0
    for t in raw_tags:
        if total + len(t) + 1 <= 500:
            safe_tags.append(t)
            total += len(t) + 1
        else:
            break
    print(f'[OK] Tags: {len(safe_tags)} tags ({total} chars) | ex: {safe_tags[:3]}')

    body = {
        'snippet': {
            'title':                metadata['titulo'],
            'description':          metadata['descricao'],
            'tags':                 [],  # enviado vazio no upload; adicionado via update()

            'categoryId':           '27',
            'defaultLanguage':      'pt',
            'defaultAudioLanguage': 'pt'
        },
        'status': {
            'privacyStatus':    'private',
            'notifySubscribers': False,
            'madeForKids':       False
        }
    }
    media = MediaFileUpload(VIDEO_FILE, chunksize=256*1024*1024, resumable=True, mimetype='video/mp4')
    try:
        request  = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
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
# SET THUMBNAIL
# ──────────────────────────────────────────────────────────

def compress_thumbnail(source, max_bytes=1_500_000):
    try:
        img = Image.open(source)
        if img.mode == 'RGBA':
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        fd, tmp = tempfile.mkstemp(suffix='.jpg')
        os.close(fd)
        for q in range(95, 19, -5):
            img.save(tmp, 'JPEG', quality=q, optimize=True)
            if os.path.getsize(tmp) < max_bytes:
                print(f'[OK] Thumb comprimida ({os.path.getsize(tmp)/1024/1024:.2f} MB, q={q}%)')
                return tmp
        os.unlink(tmp)
        return None
    except Exception as e:
        print(f'[ERRO] Compress thumb: {e}')
        return None

def set_thumbnail(youtube, video_id):
    try:
        tmp = compress_thumbnail(THUMB_FILE)
        if not tmp:
            return False
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(tmp, mimetype='image/jpeg')
        ).execute()
        os.unlink(tmp)
        print('[OK] Thumbnail definida')
        return True
    except Exception as e:
        print(f'[ERRO] Set thumbnail: {e}')
        return False

# ──────────────────────────────────────────────────────────
# UPDATE DESCRIPTION + CHAPTERS
# ──────────────────────────────────────────────────────────

def update_description(youtube, video_id, metadata):
    try:
        chapters_text = ''
        if metadata['chapters']:
            chapters_text = '\n\n' + '\n'.join(f"{c['timestamp']} - {c['title']}" for c in metadata['chapters'])
        desc = metadata['descricao'] + chapters_text
        if len(desc) > 5000:
            desc = desc[:4950] + '...'

        snippet = {
            'title':           metadata['titulo'].strip(),
            'description':     desc,
            'categoryId':      '27',
            'defaultLanguage': 'pt'
        }
        if metadata.get('_safe_tags'):
            snippet['tags'] = metadata['_safe_tags']
        elif metadata['tags']:
            snippet['tags'] = [t.strip() for t in metadata['tags'].split(',')][:30]

        youtube.videos().update(
            part='snippet',
            body={'id': video_id, 'snippet': snippet}
        ).execute()
        print('[OK] Descricao e chapters atualizados')
        return True
    except Exception as e:
        print(f'[ERRO] Update descricao: {e}')
        return False

# ──────────────────────────────────────────────────────────
# SAVE STATUS
# ──────────────────────────────────────────────────────────

def save_status(video_id, thumb_ok, desc_ok):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = f"""VIDEO_ID: {video_id}
URL: https://youtube.com/watch?v={video_id}
STATUS: private (aguardando aprovacao de Snayder para publicar)
UPLOAD_TIME: {now}
THUMBNAIL: {'OK' if thumb_ok else 'ERRO'}
CHAPTERS: {'OK' if desc_ok else 'ERRO'}
PRIVACY: private — NUNCA automaticamente public
NOTA: Caronte aguarda confirmacao explicita de Snayder para tornar publico
"""
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(LOG_FILE, 'a', encoding='utf-8') as lf:
        lf.write(f'[{now}] CARONTE -- video-015 upload OK (PRIVATE) -> {video_id}\n')
        lf.write(f'[{now}] CHECKPOINT -- Aguardando aprovacao de Snayder para publicar\n')
    print(f'[OK] Status salvo')

# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

def main():
    print('='*60)
    print('CARONTE — Upload video-015-economist-manipulacao')
    print('='*60)

    # Validar arquivos
    for label, path in [('Video', VIDEO_FILE), ('Metadata', METADATA_FILE), ('Thumbnail', THUMB_FILE)]:
        if not os.path.exists(path):
            print(f'[ERRO] {label} nao encontrado: {path}')
            return False
        size = os.path.getsize(path) / 1024 / 1024
        print(f'[OK] {label}: {size:.1f} MB — {os.path.basename(path)}')

    # ADR-008 desativado: video editado no CapCut (arquivo unico, nao partes MoviePy)
    print('[INFO] ADR-008 sync guard: N/A (CapCut edit)')

    metadata = parse_metadata()
    if not metadata['titulo']:
        print('[ERRO] Titulo vazio em metadata.txt')
        return False

    creds = authenticate()
    if not creds:
        return False
    youtube = build('youtube', 'v3', credentials=creds)
    print('[OK] Autenticado no YouTube')

    video_id = upload_video(youtube, metadata)
    if not video_id:
        return False

    thumb_ok = set_thumbnail(youtube, video_id)
    # Passa safe_tags para update_description adicionar via API separada
    metadata['_safe_tags'] = safe_tags
    desc_ok  = update_description(youtube, video_id, metadata)
    save_status(video_id, thumb_ok, desc_ok)

    print('='*60)
    print(f'[SUCESSO] https://youtube.com/watch?v={video_id}')
    print('[PRIVADO] Aguardando aprovacao de Snayder para publicar')
    print('='*60)
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
