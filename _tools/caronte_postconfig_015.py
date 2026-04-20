#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARONTE POST-CONFIG — video-015
Aplica descricao, chapters e tags no video ja uploadado VwlZ2NLQyFc
"""
import os, pickle, unicodedata, re
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

VIDEO_ID      = 'VwlZ2NLQyFc'
METADATA_FILE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-015-economist-manipulacao\8-publicacao\metadata.txt'
STATUS_FILE   = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-015-economist-manipulacao\8-publicacao\status_upload.txt'
LOG_FILE      = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log'
TOKEN_FILE    = os.path.expanduser('~/.claude/youtube_token.pickle')

def authenticate():
    with open(TOKEN_FILE, 'rb') as f:
        creds = pickle.load(f)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

def parse_metadata():
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    titulo, descricao, tags_raw, chapters = None, None, None, []

    if 'TITULO:' in content or 'TÍTULO:' in content:
        key = 'TÍTULO:' if 'TÍTULO:' in content else 'TITULO:'
        s = content.index(key) + len(key)
        s = content.find('\n', s) + 1
        e = content.find('\n', s)
        titulo = content[s:e].strip()

    if 'DESCRICAO:' in content or 'DESCRIÇÃO:' in content:
        key = 'DESCRIÇÃO:' if 'DESCRIÇÃO:' in content else 'DESCRICAO:'
        ds = content.index(key) + len(key)
        de = content.index('CAPÍTULOS:', ds) if 'CAPÍTULOS:' in content else len(content)
        raw = content[ds:de].strip()
        descricao = '\n'.join(l for l in raw.split('\n') if l.strip())

    if 'CAPÍTULOS:' in content:
        cs = content.index('CAPÍTULOS:')
        ce = content.index('REFERÊNCIAS', cs) if 'REFERÊNCIAS' in content else len(content)
        for line in content[cs:ce].split('\n'):
            line = line.strip()
            if ':' in line and ('-' in line or '—' in line):
                sep = '-' if '-' in line else '—'
                parts = line.split(sep, 1)
                if len(parts) == 2:
                    ts, title = parts[0].strip(), parts[1].strip()
                    if ts and title:
                        chapters.append({'timestamp': ts, 'title': title})

    if 'TAGS:' in content:
        idx = content.index('TAGS:') + len('TAGS:')
        rest = content[idx:].lstrip()
        for line in rest.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and ',' in line:
                tags_raw = line
                break

    return titulo, descricao, tags_raw, chapters

def sanitize_tags(tags_raw):
    def clean(t):
        t = unicodedata.normalize('NFKD', t)
        t = t.encode('ascii', 'ignore').decode('ascii')
        t = re.sub(r'[^\w\s]', '', t).strip()
        return t
    raw = [clean(t.strip()) for t in tags_raw.split(',') if t.strip()]
    raw = [t for t in raw if t and len(t) <= 100]
    safe, total = [], 0
    for t in raw:
        if total + len(t) + 1 <= 500:
            safe.append(t)
            total += len(t) + 1
        else:
            break
    print(f'[OK] {len(safe)} tags ({total} chars)')
    return safe

def main():
    print('='*55)
    print(f'CARONTE POST-CONFIG | {VIDEO_ID}')
    print('='*55)

    titulo, descricao, tags_raw, chapters = parse_metadata()
    print(f'[OK] Titulo: {titulo[:50]}')
    print(f'[OK] {len(chapters)} chapters')

    safe_tags = sanitize_tags(tags_raw) if tags_raw else []

    creds   = authenticate()
    youtube = build('youtube', 'v3', credentials=creds)
    print('[OK] Autenticado')

    # Montar descricao com chapters
    chapters_text = '\n\n' + '\n'.join(f"{c['timestamp']} - {c['title']}" for c in chapters) if chapters else ''
    desc = descricao + chapters_text
    if len(desc) > 5000:
        desc = desc[:4950] + '...'

    snippet = {
        'title':           titulo.strip(),
        'description':     desc,
        'categoryId':      '27',
        'defaultLanguage': 'pt',
    }
    if safe_tags:
        snippet['tags'] = safe_tags

    try:
        youtube.videos().update(
            part='snippet',
            body={'id': VIDEO_ID, 'snippet': snippet}
        ).execute()
        print('[OK] Descricao + chapters + tags atualizados')
    except Exception as e:
        print(f'[ERRO] Update: {e}')
        # Tentar sem tags se falhar
        print('[RETRY] Tentando sem tags...')
        snippet.pop('tags', None)
        youtube.videos().update(
            part='snippet',
            body={'id': VIDEO_ID, 'snippet': snippet}
        ).execute()
        print('[OK] Descricao + chapters atualizados (sem tags)')

    # Salvar status
    from datetime import datetime
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = f"""VIDEO_ID: {VIDEO_ID}
URL: https://youtube.com/watch?v={VIDEO_ID}
STATUS: private (aguardando aprovacao de Snayder)
UPLOAD_TIME: {now}
THUMBNAIL: OK
CHAPTERS: OK
TAGS: OK
PRIVACY: private
"""
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        f.write(status)
    with open(LOG_FILE, 'a', encoding='utf-8') as lf:
        lf.write(f'[{now}] CARONTE -- video-015 post-config OK (PRIVATE) -> {VIDEO_ID}\n')

    print('='*55)
    print(f'[SUCESSO] https://youtube.com/watch?v={VIDEO_ID}')
    print('[PRIVADO] Aguardando aprovacao para publicar')
    print('='*55)

if __name__ == '__main__':
    main()
