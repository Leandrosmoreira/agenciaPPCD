#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARONTE LEGENDAS — Converte transcrição para SRT e faz upload como legenda no YouTube.
Video: video-002-marca-da-besta (8_lnvGCAShM)
"""

import os
import re
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

VIDEO_ID = '8_lnvGCAShM'
TRANSCRICAO = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\8-publicacao\transcricao_raw.txt'
SRT_OUT = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\8-publicacao\legendas_pt.srt'

CREDS_FILE = os.path.expanduser('~/.claude/youtube_oauth_creds.json')
TOKEN_FILE = os.path.expanduser('~/.claude/youtube_token.pickle')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube.force-ssl']


def timestamp_to_seconds(ts: str) -> int:
    """Converte 'M:SS' para total de segundos"""
    parts = ts.strip().split(':')
    return int(parts[0]) * 60 + int(parts[1])


def seconds_to_srt_time(s: int) -> str:
    """Converte segundos para formato SRT 'HH:MM:SS,000'"""
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:02d},000"


def parse_transcript(filepath: str):
    """
    Parseia transcrição no formato YouTube:
      M:SS{label_de_duração}{texto}
    ex: "0:022 segundosNo ano 95..."
    ex: "1:031 minuto e 3 segundoscomprar comida..."
    Retorna lista de (start_sec, texto)
    """
    entries = []
    # Detecta timestamp no inicio da linha
    pattern = re.compile(r'^(\d+:\d{2})')

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        m = pattern.match(line)
        if not m:
            continue

        ts = m.group(1)       # ex: "1:03"
        rest = line[m.end():]  # tudo após o timestamp (inclui label de duração)

        # Remover label de duração do YouTube:
        # "2 segundos", "1 minuto e 3 segundos", "7 minutos", "14 minutos e 7 segundos"
        rest = re.sub(r'^\d+\s+minutos?\s+e\s+\d+\s+segundos?', '', rest)
        rest = re.sub(r'^\d+\s+minutos?', '', rest)
        rest = re.sub(r'^\d+\s+segundos?', '', rest)

        text = rest.strip()
        if text:
            entries.append((timestamp_to_seconds(ts), text))

    return entries


def build_srt(entries):
    """Monta conteúdo SRT a partir de lista de (start_sec, texto)"""
    lines = []
    for i, (start_sec, text) in enumerate(entries):
        idx = i + 1
        start_t = seconds_to_srt_time(start_sec)
        # End time = início da próxima entrada (ou +7s para a última)
        end_sec = entries[i + 1][0] if i + 1 < len(entries) else start_sec + 7
        end_t = seconds_to_srt_time(end_sec)

        lines.append(str(idx))
        lines.append(f"{start_t} --> {end_t}")
        lines.append(text)
        lines.append('')

    return '\n'.join(lines)


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


def upload_caption(youtube, video_id, srt_file):
    """Faz upload do SRT como legenda PT no YouTube"""
    try:
        # Verificar se já existe legenda PT para deletar antes
        existing = youtube.captions().list(part='snippet', videoId=video_id).execute()
        for cap in existing.get('items', []):
            if cap['snippet']['language'] == 'pt':
                print(f"  [INFO] Deletando legenda PT existente: {cap['id']}")
                youtube.captions().delete(id=cap['id']).execute()

        # Upload do SRT
        request = youtube.captions().insert(
            part='snippet',
            sync=False,
            body={
                'snippet': {
                    'videoId': video_id,
                    'language': 'pt',
                    'name': 'Português',
                    'isDraft': False
                }
            },
            media_body=MediaFileUpload(srt_file, mimetype='application/octet-stream')
        )
        response = request.execute()
        print(f'[OK] Caption ID: {response["id"]}')
        return True

    except Exception as e:
        print(f'[ERRO] Falha ao fazer upload da legenda: {e}')
        return False


def main():
    print('=' * 60)
    print('CARONTE LEGENDAS — SRT + Upload YouTube')
    print('=' * 60)

    # Parsear transcrição
    print('[1/4] Parseando transcrição...')
    entries = parse_transcript(TRANSCRICAO)
    if not entries:
        print('[ERRO] Nenhuma entrada encontrada na transcrição')
        return
    print(f'[OK] {len(entries)} entradas encontradas')

    # Gerar SRT
    print('[2/4] Gerando arquivo SRT...')
    srt_content = build_srt(entries)
    with open(SRT_OUT, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    print(f'[OK] SRT salvo: {SRT_OUT}')

    # Preview
    print('\n--- Preview (primeiros 5 blocos) ---')
    blocks = srt_content.strip().split('\n\n')[:5]
    print('\n\n'.join(blocks))
    print('---\n')

    # Autenticar
    print('[3/4] Autenticando...')
    creds = authenticate()
    if not creds:
        print('[ERRO] Falha na autenticação')
        return

    youtube = build('youtube', 'v3', credentials=creds)
    print('[OK] Autenticado')

    # Upload legenda
    print('[4/4] Fazendo upload da legenda PT...')
    ok = upload_caption(youtube, VIDEO_ID, SRT_OUT)

    print('=' * 60)
    if ok:
        print(f'[SUCESSO] Legendas PT adicionadas: https://youtube.com/watch?v={VIDEO_ID}')
    else:
        print('[AVISO] Upload falhou — SRT está salvo localmente:')
        print(f'  {SRT_OUT}')
        print('  Upload manual: YouTube Studio > Legendas > Adicionar > Fazer upload')
    print('=' * 60)


if __name__ == '__main__':
    main()
