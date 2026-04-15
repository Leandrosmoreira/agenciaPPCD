#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARONTE — Detector Automático de Chapters via Whisper
Transcreve os áudios de narração e detecta timestamps reais dos capítulos.
Atualiza a descrição do vídeo no YouTube com os chapters corretos.

Uso:
    python caronte_chapters.py --canal sinais-do-fim --video video-007-falsa-paz
    python caronte_chapters.py --canal sinais-do-fim --video video-007-falsa-paz --video-id djzD7YFysoU --update
"""

import os
import re
import pickle
import argparse
from pathlib import Path
from datetime import datetime

# ──────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────

BASE_DIR   = Path(r'C:\Users\Leandro\Downloads\agencia')
TOKEN_FILE = Path.home() / '.claude' / 'youtube_token.pickle'
SCOPES     = ['https://www.googleapis.com/auth/youtube']

# ──────────────────────────────────────────────────────────
# TRANSCREVER ÁUDIOS COM WHISPER
# ──────────────────────────────────────────────────────────

def transcribe_parts(audio_dir: Path, model_size: str = 'base') -> list[dict]:
    """
    Transcreve todos os parteN.mp3 com Whisper.
    Retorna lista de dicts: {part, offset_sec, text, segments}
    """
    import whisper

    parts = sorted(audio_dir.glob('parte*.mp3'))
    if not parts:
        print(f'[ERRO] Nenhum arquivo parte*.mp3 em {audio_dir}')
        return []

    print(f'[WHISPER] Carregando modelo "{model_size}"...')
    model = whisper.load_model(model_size)

    # Calcular duração de cada parte para offsets acumulados
    import subprocess, json as _json
    def get_duration(path):
        r = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
             '-of', 'json', str(path)],
            capture_output=True, text=True
        )
        return float(_json.loads(r.stdout)['format']['duration'])

    results = []
    offset = 0.0
    for part in parts:
        duration = get_duration(part)
        print(f'[WHISPER] Transcrevendo {part.name} (offset {offset:.0f}s)...')
        result = model.transcribe(str(part), language='pt', word_timestamps=True)

        # Ajustar timestamps dos segments para o offset absoluto do vídeo
        segments_abs = []
        for seg in result['segments']:
            segments_abs.append({
                'start': seg['start'] + offset,
                'end':   seg['end']   + offset,
                'text':  seg['text'].strip()
            })

        results.append({
            'part':       part.name,
            'offset_sec': offset,
            'duration':   duration,
            'text':       result['text'],
            'segments':   segments_abs
        })
        offset += duration

    print(f'[OK] {len(results)} partes transcritas | duração total: {offset:.0f}s ({int(offset//60)}:{int(offset%60):02d})')
    return results

# ──────────────────────────────────────────────────────────
# DETECTAR CHAPTERS
# ──────────────────────────────────────────────────────────

def detect_chapters(transcription: list[dict], metadata_file: Path) -> list[dict]:
    """
    Lê os chapters do metadata.txt e encontra o timestamp exato
    no áudio via matching de palavras-chave na transcrição.
    Retorna lista de {timestamp_str, title, matched_text, confidence}
    """
    # Ler chapters do metadata
    content = metadata_file.read_text(encoding='utf-8')
    chapters_raw = []
    if 'CAPÍTULOS:' in content:
        start = content.index('CAPÍTULOS:')
        end = content.index('REFERÊNCIAS', start) if 'REFERÊNCIAS' in content else len(content)
        for line in content[start:end].split('\n'):
            line = line.strip()
            if re.match(r'^\d+:\d+', line) and ' - ' in line:
                parts = line.split(' - ', 1)
                chapters_raw.append({'time_hint': parts[0].strip(), 'title': parts[1].strip()})

    if not chapters_raw:
        print('[AVISO] Nenhum chapter encontrado no metadata.txt')
        return []

    # Montar lista plana de segments para busca
    all_segments = []
    for part_data in transcription:
        all_segments.extend(part_data['segments'])

    def fmt_time(secs: float) -> str:
        m, s = divmod(int(secs), 60)
        return f'{m}:{s:02d}'

    def keywords_from_title(title: str) -> list[str]:
        """Extrai palavras-chave do título do chapter (remove stopwords)"""
        stopwords = {'o', 'a', 'os', 'as', 'de', 'do', 'da', 'dos', 'das',
                     'que', 'e', 'em', 'um', 'uma', 'por', 'para', 'com',
                     'se', 'ao', 'no', 'na', 'nos', 'nas', 'é', 'são'}
        words = re.findall(r'\w+', title.lower())
        return [w for w in words if w not in stopwords and len(w) > 3]

    def hint_to_secs(hint: str) -> float:
        parts = hint.split(':')
        return int(parts[0]) * 60 + int(parts[1])

    detected = []
    for i, chapter in enumerate(chapters_raw):
        keywords = keywords_from_title(chapter['title'])
        hint_secs = hint_to_secs(chapter['time_hint'])

        # Buscar nos segments próximos ao hint (±90s de tolerância)
        best_seg = None
        best_score = 0
        for seg in all_segments:
            # Peso: proximidade ao hint + keywords encontradas
            time_diff = abs(seg['start'] - hint_secs)
            if time_diff > 90:
                continue
            text_lower = seg['text'].lower()
            kw_hits = sum(1 for kw in keywords if kw in text_lower)
            # Score: keywords têm mais peso que proximidade
            score = kw_hits * 10 - (time_diff / 10)
            if score > best_score:
                best_score = score
                best_seg = seg

        # Se não encontrou por keywords, usa o segment mais próximo do hint
        if not best_seg:
            closest = min(all_segments, key=lambda s: abs(s['start'] - hint_secs))
            best_seg = closest
            confidence = 'baixa (sem match de keywords)'
        else:
            confidence = f'alta ({best_score:.0f}pts)'

        # Chapter 0:00 sempre fica em 0:00
        final_time = 0.0 if i == 0 else best_seg['start']

        detected.append({
            'timestamp_str': fmt_time(final_time),
            'timestamp_sec': final_time,
            'title':         chapter['title'],
            'matched_text':  best_seg['text'][:60] if best_seg else '',
            'confidence':    confidence
        })
        print(f'  Chapter {i+1}: [{fmt_time(final_time)}] "{chapter["title"]}" — {confidence}')
        print(f'             match: "{best_seg["text"][:60] if best_seg else "N/A"}"')

    return detected

# ──────────────────────────────────────────────────────────
# ATUALIZAR DESCRIÇÃO NO YOUTUBE
# ──────────────────────────────────────────────────────────

def update_youtube_chapters(video_id: str, chapters: list[dict], metadata_file: Path):
    """Atualiza a descrição do vídeo no YouTube com os chapters corrigidos."""
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print('[ERRO] Token inválido. Rode o caronte_upload.py primeiro para autenticar.')
            return False

    youtube = build('youtube', 'v3', credentials=creds)

    # Buscar descrição atual
    resp = youtube.videos().list(part='snippet', id=video_id).execute()
    if not resp['items']:
        print(f'[ERRO] Vídeo {video_id} não encontrado')
        return False

    snippet = resp['items'][0]['snippet']
    current_desc = snippet.get('description', '')

    # Remover chapters antigos (linhas que começam com timestamp)
    lines = current_desc.split('\n')
    clean_lines = [l for l in lines if not re.match(r'^\d+:\d{2}\s*[-–—]', l.strip())]
    clean_desc = '\n'.join(clean_lines).strip()

    # Montar novos chapters
    chapters_text = '\n\n' + '\n'.join(
        f"{ch['timestamp_str']} - {ch['title']}" for ch in chapters
    )
    new_desc = clean_desc + chapters_text

    if len(new_desc) > 5000:
        new_desc = new_desc[:4950] + '...'

    # Atualizar
    snippet['description'] = new_desc
    youtube.videos().update(
        part='snippet',
        body={'id': video_id, 'snippet': snippet}
    ).execute()

    print(f'[OK] Descrição atualizada com {len(chapters)} chapters corrigidos')
    return True

# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Caronte — Detector de Chapters')
    parser.add_argument('--canal', required=True)
    parser.add_argument('--video', required=True)
    parser.add_argument('--video-id', help='YouTube video ID para atualizar descrição')
    parser.add_argument('--update', action='store_true', help='Atualizar YouTube após detectar')
    parser.add_argument('--model', default='base', help='Modelo Whisper: tiny/base/small/medium')
    args = parser.parse_args()

    video_dir  = BASE_DIR / 'canais' / args.canal / 'videos' / args.video
    audio_dir  = video_dir / '6-assets' / 'audio_suno'
    meta_file  = video_dir / '8-publicacao' / 'metadata.txt'
    log_file   = BASE_DIR / 'canais' / args.canal / '_config' / 'pipeline.log'

    print('='*60)
    print(f'CARONTE CHAPTERS — {args.video}')
    print('='*60)

    # Transcrever
    transcription = transcribe_parts(audio_dir, model_size=args.model)
    if not transcription:
        return

    # Detectar chapters
    print('\n[CARONTE] Detectando chapters...')
    chapters = detect_chapters(transcription, meta_file)

    # Exibir resultado
    print('\n' + '='*60)
    print('CHAPTERS DETECTADOS (copiar para YouTube):')
    print('='*60)
    for ch in chapters:
        print(f"{ch['timestamp_str']} - {ch['title']}")

    # Atualizar YouTube se solicitado
    if args.update and args.video_id:
        print(f'\n[CARONTE] Atualizando YouTube ({args.video_id})...')
        ok = update_youtube_chapters(args.video_id, chapters, meta_file)
        if ok:
            # Log
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f'[{now}] CARONTE — Chapters atualizados via Whisper no vídeo {args.video_id}\n')
                for ch in chapters:
                    f.write(f'[{now}] CARONTE —   {ch["timestamp_str"]} - {ch["title"]}\n')

    print('='*60)

if __name__ == '__main__':
    main()
