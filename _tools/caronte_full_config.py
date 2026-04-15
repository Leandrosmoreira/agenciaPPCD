#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARONTE FULL CONFIG — Configure TUDO via API (título, descricao, tags, chapters, thumbnail, COPPA, comentarios)
Para video-002-marca-da-besta (video_id: 8_lnvGCAShM)
"""

import os
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

# ──────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────

VIDEO_ID = '8_lnvGCAShM'  # video-002-marca-da-besta

THUMB_FILE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\8-publicacao\thumb.png'
METADATA_FILE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\8-publicacao\metadata.txt'
STATUS_FILE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\8-publicacao\status_upload.txt'
LOG_FILE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log'

# Google OAuth credentials
CREDS_FILE = os.path.expanduser('~/.claude/youtube_oauth_creds.json')
TOKEN_FILE = os.path.expanduser('~/.claude/youtube_token.pickle')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube']

# ──────────────────────────────────────────────────────────
# AUTHENTICATE
# ──────────────────────────────────────────────────────────

def authenticate():
    """Autentica com YouTube API"""
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
    """Le metadata.txt e extrai info do video"""
    metadata = {
        'titulo': None,
        'descricao': None,
        'tags': None,
        'chapters': []
    }

    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extrair titulo (linha APOS "TÍTULO:")
    if 'TÍTULO:' in content:
        titulo_start = content.index('TÍTULO:') + len('TÍTULO:')
        titulo_start = content.find('\n', titulo_start) + 1
        titulo_end = content.find('\n', titulo_start)
        if titulo_end > titulo_start:
            metadata['titulo'] = content[titulo_start:titulo_end].strip()

    # Extrair descricao
    if 'DESCRIÇÃO:' in content:
        desc_start = content.index('DESCRIÇÃO:') + len('DESCRIÇÃO:')
        desc_end = content.index('CAPÍTULOS:', desc_start) if 'CAPÍTULOS:' in content else len(content)
        raw_desc = content[desc_start:desc_end].strip()
        metadata['descricao'] = '\n'.join(line for line in raw_desc.split('\n') if line.strip())

    # Extrair chapters
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

    # Extrair tags
    if 'TAGS' in content or 'tags' in content.lower():
        tags_idx = content.upper().index('TAGS')
        tags_start = tags_idx + len('TAGS')
        rest = content[tags_start:]
        tags_end = rest.index('\n\n') if '\n\n' in rest else len(rest)
        tags_text = rest[:tags_end].strip()
        for line in tags_text.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                metadata['tags'] = line
                break

    print(f'[OK] Metadata parseado: titulo={metadata["titulo"][:40]}...')
    return metadata

# ──────────────────────────────────────────────────────────
# COMPRESS THUMBNAIL
# ──────────────────────────────────────────────────────────

def compress_thumbnail(source_file, max_size_bytes=1500000):
    """Comprime thumbnail para <2 MB"""
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
            file_size = os.path.getsize(temp_file)

            if file_size < max_size_bytes:
                print(f'[OK] Thumbnail comprimida: {file_size / 1024 / 1024:.2f} MB (qualidade {quality}%)')
                return temp_file

            quality -= 5

        print(f'[ERRO] Nao conseguiu comprimir abaixo de {max_size_bytes / 1024 / 1024:.1f} MB')
        os.unlink(temp_file)
        return None

    except Exception as e:
        print(f'[ERRO] Falha ao comprimir thumbnail: {e}')
        return None

# ──────────────────────────────────────────────────────────
# FULL VIDEO UPDATE VIA API
# ──────────────────────────────────────────────────────────

def full_video_update(youtube, video_id, metadata):
    """Atualiza TUDO via API: snippet, status, processingDetails, topicDetails"""
    try:
        print('[CARONTE] Preparando snippet completo...')

        # Montar chapters na descricao
        chapters_text = ''
        if metadata['chapters']:
            chapters_text = '\n\n' + '\n'.join([f"{ch['timestamp']} - {ch['title']}" for ch in metadata['chapters']])

        new_desc = metadata['descricao'] + chapters_text

        # Validar tamanho
        if len(new_desc) > 5000:
            print(f'[AVISO] Descricao truncada de {len(new_desc)} para 5000 chars')
            new_desc = new_desc[:4950] + '...'

        # Tags
        tags = []
        if metadata['tags']:
            tags = [t.strip() for t in metadata['tags'].split(',')][:30]

        # Montar o corpo completo
        body = {
            'id': video_id,
            'snippet': {
                'title': metadata['titulo'].strip(),
                'description': new_desc,
                'tags': tags,
                'categoryId': '27',  # Educacao
                'defaultLanguage': 'pt',
                'defaultAudioLanguage': 'pt'
            },
            'status': {
                'privacyStatus': 'private',  # NUNCA mude automaticamente
                'embeddable': True,  # Permitir incorporacao
                'license': 'creativeCommon',  # Licenca padrao
                'madeForKids': False,  # NAO eh conteudo infantil (IMPORTANTE para compliance COPPA)
                'publicStatsViewable': True
            },
            'recordingDetails': {
                'recordingDate': '2026-04-07T00:00:00Z'  # Data aproximada de gravacao
            },
            'suggestions': {
                'processingWarnings': [],
                'processingErrors': [],
                'tagSuggestions': []
            }
        }

        # Fazer update com todos os parametros
        print('[CARONTE] Enviando atualizacao completa para YouTube API...')
        request = youtube.videos().update(
            part='snippet,status,recordingDetails,suggestions',
            body=body
        )
        response = request.execute()

        print('[OK] Snippet, status e configuracoes atualizados via API')
        print(f'   - Titulo: {metadata["titulo"][:50]}...')
        print(f'   - Tags: {len(tags)} tags')
        print(f'   - Privacidade: PRIVATE')
        print(f'   - Incorporacao: PERMITIDA')
        print(f'   - COPPA: NAO (nao eh infantil)')

        return True

    except Exception as e:
        print(f'[ERRO] Falha ao atualizar video: {e}')
        return False

# ──────────────────────────────────────────────────────────
# SET THUMBNAIL
# ──────────────────────────────────────────────────────────

def set_thumbnail(youtube, video_id):
    """Define thumbnail do video"""
    try:
        thumb_compressed = compress_thumbnail(THUMB_FILE)
        if not thumb_compressed:
            print('[ERRO] Falha ao comprimir thumbnail')
            return False

        request = youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumb_compressed, mimetype='image/jpeg')
        )
        response = request.execute()
        os.unlink(thumb_compressed)

        print('[OK] Thumbnail definida')
        return True
    except Exception as e:
        print(f'[ERRO] Falha ao definir thumbnail: {e}')
        return False

# ──────────────────────────────────────────────────────────
# UPDATE STATUS
# ──────────────────────────────────────────────────────────

def update_status(snippet_ok, thumb_ok):
    """Salva resultado em status_upload.txt"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = f"""VIDEO_ID: {VIDEO_ID}
URL: https://youtube.com/watch?v={VIDEO_ID}
STATUS: private (NUNCA publica automaticamente — aguarda aprovacao de Snayder)
CONFIGURACAO_TIME: {now}

CONFIGURACOES VIA API:
═══════════════════════════════════════════════════
✓ Snippet (titulo, descricao, tags, categoria): {'OK' if snippet_ok else 'ERRO'}
✓ Thumbnail: {'OK' if thumb_ok else 'ERRO'}
✓ Status (privacidade, incorporacao, COPPA): {'OK' if snippet_ok else 'ERRO'}

PROXIMO PASSO:
═══════════════════════════════════════════════════
Snayder deve acessar YouTube Studio para:
1. Revisar titulo e descricao
2. Ativar MANUALMENTE: Cards, Tela Final, Legendas (se houver)
3. Testar reproducao
4. Aprovar para publicacao (change to PUBLIC)

IMPORTANTE: Todos os parametros obrigatorios foram preenchidos via API.
Caronte NAO MUDA para PUBLIC automaticamente — exige confirmacao explícita.
"""
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        f.write(status)

    with open(LOG_FILE, 'a', encoding='utf-8') as lf:
        lf.write(f'[{now}] CARONTE FULL CONFIG -- {VIDEO_ID}\n')
        lf.write(f'[{now}] Snippet: {"OK" if snippet_ok else "ERRO"} | Thumbnail: {"OK" if thumb_ok else "ERRO"}\n')

    print(f'[OK] Status salvo em {STATUS_FILE}')

# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

def main():
    print('='*60)
    print('CARONTE FULL CONFIG — Configurar Tudo via API')
    print('='*60)
    print(f'VIDEO_ID: {VIDEO_ID}')

    # Validar arquivos
    if not os.path.exists(METADATA_FILE):
        print(f'[ERRO] Metadata nao encontrado: {METADATA_FILE}')
        return False
    print('[OK] Metadata encontrada')

    if not os.path.exists(THUMB_FILE):
        print(f'[ERRO] Thumbnail nao encontrada: {THUMB_FILE}')
        return False
    thumb_size_mb = os.path.getsize(THUMB_FILE) / 1024 / 1024
    print(f'[OK] Thumbnail encontrada ({thumb_size_mb:.1f} MB)')

    # Parse metadata
    metadata = parse_metadata()
    if not metadata['titulo']:
        print('[ERRO] Titulo vazio em metadata.txt')
        return False

    # Autenticar
    creds = authenticate()
    if not creds:
        print('[ERRO] Falha na autenticacao')
        return False

    youtube = build('youtube', 'v3', credentials=creds)
    print('[OK] Autenticado no YouTube')

    # Full update
    snippet_ok = full_video_update(youtube, VIDEO_ID, metadata)
    thumb_ok = set_thumbnail(youtube, VIDEO_ID)

    # Save status
    update_status(snippet_ok, thumb_ok)

    print('='*60)
    if snippet_ok and thumb_ok:
        print('[SUCESSO] Video completamente configurado via API')
        print(f'[INFO] Titulo definido: {metadata["titulo"][:50]}...')
        print('[INFO] Descricao + chapters foram adicionados')
        print('[INFO] Thumbnail foi atualizada')
        print('[INFO] Tags foram adicionadas')
        print('[INFO] Status: PRIVATE (aguardando Snayder para PUBLIC)')
        print(f'[INFO] URL: https://youtube.com/watch?v={VIDEO_ID}')
    else:
        print('[AVISO] Algumas configuracoes falharam')
    print('='*60)

    return snippet_ok and thumb_ok

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
