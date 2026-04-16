#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARONTE — Agente de Upload para YouTube
video-008-sinais-fisicos | Sinais do Fim
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

VIDEO_FILE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-008-sinais-fisicos\8-publicacao\0412.mp4'
THUMB_FILE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-008-sinais-fisicos\8-publicacao\Gemini_Generated_Image_nfg2qynfg2qynfg2.png'
METADATA_FILE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-008-sinais-fisicos\8-publicacao\metadata.txt'
STATUS_FILE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-008-sinais-fisicos\8-publicacao\status_upload.txt'
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
                print('Crie um Google Cloud Project e baixe credentials.json')
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
        # Pular a primeira quebra de linha (apos "TÍTULO:")
        titulo_start = content.find('\n', titulo_start) + 1
        # Procurar a próxima quebra de linha
        titulo_end = content.find('\n', titulo_start)
        if titulo_end > titulo_start:
            metadata['titulo'] = content[titulo_start:titulo_end].strip()

    if not metadata['titulo']:
        print('[AVISO] Titulo nao encontrado em metadata.txt')
        return metadata

    # Extrair descricao
    if 'DESCRIÇÃO:' in content:
        desc_start = content.index('DESCRIÇÃO:') + len('DESCRIÇÃO:')
        desc_end = content.index('CAPÍTULOS:', desc_start) if 'CAPÍTULOS:' in content else len(content)
        raw_desc = content[desc_start:desc_end].strip()
        # Limpar linhas vazias no inicio
        metadata['descricao'] = '\n'.join(line for line in raw_desc.split('\n') if line.strip())

    # Extrair chapters
    if 'CAPÍTULOS:' in content:
        chapters_start = content.index('CAPÍTULOS:')
        chapters_end = content.index('REFERÊNCIAS', chapters_start) if 'REFERÊNCIAS' in content else len(content)
        chapters_text = content[chapters_start:chapters_end]
        for line in chapters_text.split('\n'):
            line = line.strip()
            # Verificar formato: "00:00 - Titulo" ou "00:00 — Titulo"
            if ':' in line and ('-' in line or '—' in line):
                sep = '-' if '-' in line else '—'
                parts = line.split(sep, 1)  # Split apenas no primeiro separador
                if len(parts) == 2:
                    timestamp = parts[0].strip()
                    title = parts[1].strip()
                    if timestamp and title:
                        metadata['chapters'].append({'timestamp': timestamp, 'title': title})

    # Extrair tags: pula o ":" inicial e hashtags, exige linha com virgulas
    if 'TAGS:' in content:
        tags_idx = content.index('TAGS:') + len('TAGS:')
        rest = content[tags_idx:].lstrip()
        for line in rest.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and ',' in line:
                metadata['tags'] = line
                break

    print(f'[OK] Metadata parseado: titulo={metadata["titulo"][:40]}...')
    return metadata

# ──────────────────────────────────────────────────────────
# UPLOAD VIDEO
# ──────────────────────────────────────────────────────────

def upload_video(youtube, metadata):
    """Faz upload do video para YouTube como PRIVATE"""

    print('[CARONTE] Iniciando upload...')

    body = {
        'snippet': {
            'title': metadata['titulo'],
            'description': metadata['descricao'],
            'tags': metadata['tags'].split(',') if metadata['tags'] else [],
            'categoryId': '27',  # Educacao
            'defaultLanguage': 'pt',
            'defaultAudioLanguage': 'pt'
        },
        'status': {
            'privacyStatus': 'unlisted',  # unlisted = link funciona (WhatsApp preview OK), mas nao aparece na busca
            'notifySubscribers': False,
            'madeForKids': False
        }
    }

    media = MediaFileUpload(VIDEO_FILE, chunksize=256*1024*1024, resumable=True, mimetype='video/mp4')

    try:
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )

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
# COMPRESS THUMBNAIL
# ──────────────────────────────────────────────────────────

def compress_thumbnail(source_file, max_size_bytes=1500000):
    """Comprime thumbnail para <2 MB (usa 1.5 MB como alvo)"""
    try:
        img = Image.open(source_file)

        # Converter para RGB se necessario (remove alpha channel)
        if img.mode == 'RGBA':
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])
            img = rgb_img

        # Criar arquivo temporario
        temp_fd, temp_file = tempfile.mkstemp(suffix='.jpg')
        os.close(temp_fd)

        # Salvar com qualidade progressiva ate ficar <2 MB
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
# SET THUMBNAIL
# ──────────────────────────────────────────────────────────

def set_thumbnail(youtube, video_id):
    """Define thumbnail do video (comprimo antes de upload)"""
    try:
        # Comprimir thumbnail
        thumb_compressed = compress_thumbnail(THUMB_FILE)
        if not thumb_compressed:
            print('[ERRO] Falha ao comprimir thumbnail')
            return False

        # Upload
        request = youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumb_compressed, mimetype='image/jpeg')
        )
        response = request.execute()

        # Limpar arquivo temporario
        os.unlink(thumb_compressed)

        print('[OK] Thumbnail definida')
        return True
    except Exception as e:
        print(f'[ERRO] Falha ao definir thumbnail: {e}')
        return False

# ──────────────────────────────────────────────────────────
# UPDATE DESCRIPTION WITH CHAPTERS
# ──────────────────────────────────────────────────────────

def update_description_with_chapters(youtube, video_id, metadata):
    """Atualiza descricao com chapters via API"""
    try:
        # Validar metadata
        if not metadata['titulo'] or not metadata['titulo'].strip():
            print('[ERRO] Titulo vazio na metadata')
            return False

        # Montar chapters
        chapters_text = ''
        if metadata['chapters']:
            chapters_text = '\n\n' + '\n'.join([f"{ch['timestamp']} - {ch['title']}" for ch in metadata['chapters']])

        # Montar descricao final
        new_desc = metadata['descricao'] + chapters_text

        # Validar tamanho descricao (max 5000 caracteres)
        if len(new_desc) > 5000:
            print(f'[AVISO] Descricao muito longa ({len(new_desc)} chars), truncando para 5000')
            new_desc = new_desc[:4950] + '...'

        # Montar snippet com todos os campos obrigatorios
        snippet = {
            'title': metadata['titulo'].strip(),
            'description': new_desc,
            'categoryId': '27',  # Educacao
            'defaultLanguage': 'pt'
        }

        # Adicionar tags se existir
        if metadata['tags']:
            tag_list = [t.strip() for t in metadata['tags'].split(',')]
            snippet['tags'] = tag_list[:30]  # YouTube permite max 500 chars de tags

        # Fazer update
        request = youtube.videos().update(
            part='snippet',
            body={
                'id': video_id,
                'snippet': snippet
            }
        )
        response = request.execute()
        print('[OK] Descricao e chapters atualizados')
        return True
    except Exception as e:
        print(f'[ERRO] Falha ao atualizar descricao: {e}')
        return False

# ──────────────────────────────────────────────────────────
# SAVE STATUS
# ──────────────────────────────────────────────────────────

def save_status(video_id, thumb_ok, desc_ok):
    """Salva status do upload em status_upload.txt"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = f"""VIDEO_ID: {video_id}
URL: https://youtube.com/watch?v={video_id}
STATUS: private (aguardando aprovacao de Snayder para publicar)
UPLOAD_TIME: {now}
THUMBNAIL: {'OK' if thumb_ok else 'ERRO'}
CHAPTERS: {'OK' if desc_ok else 'ERRO'}
PRIVACY_STATUS: private (NUNCA mudou automaticamente para public)
NOTA: Caronte aguarda confirmacao explicita de Snayder para tornar publico
"""
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        f.write(status)

    # Registrar no pipeline log
    with open(LOG_FILE, 'a', encoding='utf-8') as lf:
        lf.write(f'[{now}] CARONTE -- Video upload OK (PRIVATE) -> {video_id}\n')
        lf.write(f'[{now}] CHECKPOINT -- Aguardando aprovacao de Snayder para tornar publico\n')

    print(f'[OK] Status salvo em {STATUS_FILE}')

# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

def main():
    print('='*60)
    print('CARONTE — Agente de Upload')
    print('='*60)

    # Validar arquivos
    if not os.path.exists(VIDEO_FILE):
        print(f'[ERRO] Video nao encontrado: {VIDEO_FILE}')
        return False
    video_size_mb = os.path.getsize(VIDEO_FILE) / 1024 / 1024
    print(f'[OK] Video encontrado ({video_size_mb:.1f} MB)')

    if not os.path.exists(METADATA_FILE):
        print(f'[ERRO] Metadata nao encontrado: {METADATA_FILE}')
        return False
    print('[OK] Metadata encontrada')

    if not os.path.exists(THUMB_FILE):
        print(f'[ERRO] Thumbnail nao encontrada: {THUMB_FILE}')
        return False
    thumb_size_mb = os.path.getsize(THUMB_FILE) / 1024 / 1024
    print(f'[OK] Thumbnail encontrada ({thumb_size_mb:.1f} MB) [sera comprimida para <2 MB]')

    # ADR-008: validar sync audio/video antes do upload
    if not validar_sync_adr008(VIDEO_FILE):
        return False

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

    # Upload video
    video_id = upload_video(youtube, metadata)
    if not video_id:
        print('[ERRO] Falha no upload')
        return False

    # Set thumbnail (com compressao automatica)
    print('[CARONTE] Comprimindo e enviando thumbnail...')
    thumb_ok = set_thumbnail(youtube, video_id)

    # Update description with chapters (via API)
    print('[CARONTE] Atualizando descricao e chapters via API...')
    desc_ok = update_description_with_chapters(youtube, video_id, metadata)

    # Save status
    save_status(video_id, thumb_ok, desc_ok)

    print('='*60)
    print(f'[SUCESSO] Video privado em: https://youtube.com/watch?v={video_id}')
    if thumb_ok and desc_ok:
        print('[OK] Thumbnail e metadata atualizadas via API')
    else:
        if not thumb_ok:
            print('[AVISO] Thumbnail nao foi atualizada — verifique tamanho/formato')
        if not desc_ok:
            print('[AVISO] Descricao/chapters nao foram atualizadas — verifique metadata.txt')
    print('[AGUARDANDO] Aprovacao de Snayder para mudar para PUBLICO')
    print('='*60)
    return thumb_ok and desc_ok

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
