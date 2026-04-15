#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARGOS — Extrator de Transcrições de Concorrentes
Busca os top 10 vídeos de um tema no YouTube, baixa as transcrições
e extrai hooks, power words, estrutura e CTAs como base para a Morrigan.

Uso:
    python argos_transcricoes.py --canal sinais-do-fim --video video-008-sinais-fisicos --tema "corvos tel aviv apocalipse sinais biblicos"
"""

import os, re, sys, json, argparse, unicodedata
from pathlib import Path
from collections import Counter
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r'C:\Users\Leandro\Downloads\agencia')
API_KEY  = 'AIzaSyC6dXWuqmfnfW1GRCnVW1daSW63PyGIym8'

STOP = {
    'de','a','o','e','que','em','um','uma','para','com','se','ao','no','na',
    'os','as','dos','das','do','da','por','sao','mas','ou','nao','foi','esta',
    'ser','ter','seu','sua','seus','suas','este','esta','isso','aqui','ali',
    'pela','pelo','mais','muito','bem','onde','quando','como','voce','esse',
    'essa','eles','elas','nos','aquele','aquela','tudo','nada','cada','quem',
    'qual','porque','pois','logo','entao','assim','mesmo','outro','outra'
}

POWER_WORDS = [
    'assustador','proibido','ninguem','ja esta','sendo ativado','nao te contaram',
    'escondido','revelado','urgente','atencao','cuidado','perigo','fim','apocalipse',
    'profecia','biblia','sinal','tribulacao','arrebatamento','destruicao','juizo',
    'sangue','fogo','guerra','morte','salvador','jesus','deus','espirito','anjo',
    'diabo','satanas','besta','falso','paz','verdade','segredo','nunca','sempre',
    'agora','hoje','ultimo','primeiro','mundo','brasil','israel','ira','marca',
    'besta','numero','666','selos','trombetas','grande','final','eterno','salvo'
]

def norm(s):
    return unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode()

def fmt_time(secs):
    m, s = divmod(int(secs), 60)
    return f'{m}:{s:02d}'

# ──────────────────────────────────────────────────────────
# BUSCAR TOP 10 VÍDEOS NO YOUTUBE
# ──────────────────────────────────────────────────────────

def buscar_top10_funil(tema: str, target: int = 10, queries_tematicas: list = None) -> list[dict]:
    """
    Funil temático: usa queries alternativas relacionadas ao tema.
    Cada nível é um ângulo diferente do mesmo assunto — nunca reduz keywords mecanicamente.
    Filtra sempre por relevância temática real.
    """
    from googleapiclient.discovery import build
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Se não tiver queries temáticas, usa o tema como query única
    if not queries_tematicas:
        queries_tematicas = [tema]

    seen = set()
    videos = []

    for nivel_idx, (query, must_words) in enumerate(queries_tematicas):
        if len(videos) >= target:
            break

        faltam = target - len(videos)
        print(f'\n[FUNIL N{nivel_idx+1}] "{query}"')
        print(f'  Obrigatório no título: {must_words} | Faltam: {faltam}')

        r = youtube.search().list(
            q=query, part='snippet', type='video',
            maxResults=min(25, faltam * 3), order='viewCount'
        ).execute()

        adicionados = 0
        for item in r['items']:
            vid_id     = item['id']['videoId']
            title      = item['snippet']['title']
            title_norm = norm(title)
            # Deve ter pelo menos 1 keyword obrigatória no título
            if vid_id not in seen and any(w in title_norm for w in must_words):
                seen.add(vid_id)
                videos.append({'video_id': vid_id, 'title': title, 'channel': item['snippet']['channelTitle']})
                print(f'  + {title[:70]}')
                adicionados += 1

        if adicionados == 0:
            print(f'  (sem novos resultados relevantes)')
        print(f'  Total: {len(videos)}/{target}')

    # Buscar stats e ordenar por views
    if videos:
        ids = ','.join(v['video_id'] for v in videos[:30])
        stats = youtube.videos().list(part='statistics,snippet', id=ids).execute()
        sm = {i['id']: {'views': int(i['statistics'].get('viewCount', 0)),
                         'title': i['snippet']['title']} for i in stats['items']}
        for v in videos:
            s = sm.get(v['video_id'], {})
            v['views'] = s.get('views', 0)
            v['title']  = s.get('title', v['title'])
        videos.sort(key=lambda x: x['views'], reverse=True)

    final = videos[:target]
    print(f'\n[OK] {len(final)} vídeos relevantes:')
    for i, v in enumerate(final, 1):
        print(f'  {i:2}. {v["views"]:>8,}v | {v["title"][:70]}')
    return final


def buscar_top10(tema: str, max_results: int = 10, queries_extras: list = None) -> list[dict]:
    """
    Busca vídeos relevantes ao tema usando múltiplas queries específicas.
    Filtra por relevância de título para evitar resultados genéricos.
    """
    from googleapiclient.discovery import build
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Extrair keywords do tema para filtro de relevância
    tema_norm_words = set(norm(tema).split())
    tema_norm_words -= {'que', 'para', 'com', 'dos', 'das', 'uma', 'como', 'mais'}

    # Queries: a principal + extras se fornecidas
    all_queries = [tema]
    if queries_extras:
        all_queries.extend(queries_extras)

    seen_ids = set()
    all_videos = []

    for q in all_queries:
        print(f'[ARGOS] Query: "{q}"')
        r = youtube.search().list(
            q=q,
            part='snippet',
            type='video',
            maxResults=max_results,
            order='viewCount',
            relevanceLanguage='pt',
        ).execute()

        for item in r['items']:
            vid_id = item['id']['videoId']
            if vid_id not in seen_ids:
                seen_ids.add(vid_id)
                all_videos.append({
                    'video_id': vid_id,
                    'title':    item['snippet']['title'],
                    'channel':  item['snippet']['channelTitle'],
                })

    # Buscar stats de todos
    ids_list = [v['video_id'] for v in all_videos]
    stats_r = youtube.videos().list(
        part='snippet,statistics',
        id=','.join(ids_list[:50])
    ).execute()

    stats_map = {}
    for item in stats_r['items']:
        stats_map[item['id']] = {
            'views': int(item['statistics'].get('viewCount', 0)),
            'likes': int(item['statistics'].get('likeCount', 0)),
            'title': item['snippet']['title'],
            'channel': item['snippet']['channelTitle'],
        }

    for v in all_videos:
        s = stats_map.get(v['video_id'], {})
        v['views'] = s.get('views', 0)
        v['likes'] = s.get('likes', 0)
        v['title'] = s.get('title', v['title'])
        v['channel'] = s.get('channel', v['channel'])

    # Filtro de relevância: pontuar cada vídeo por match de keywords no título
    def relevance_score(v):
        title_norm = norm(v['title'])
        hits = sum(1 for w in tema_norm_words if w in title_norm)
        return hits

    # Separar: alta relevância (≥1 keyword) vs baixa relevância
    high = [v for v in all_videos if relevance_score(v) >= 1]
    low  = [v for v in all_videos if relevance_score(v) == 0]

    # Ordenar cada grupo por views e combinar
    high.sort(key=lambda x: x['views'], reverse=True)
    low.sort(key=lambda x: x['views'], reverse=True)

    # Pegar top N: priorizar alta relevância, completar com baixa se necessário
    final = high[:max_results]
    if len(final) < max_results:
        final += low[:max_results - len(final)]

    print(f'\n[OK] {len(final)} videos relevantes (de {len(all_videos)} encontrados)')
    print(f'     Alta relevância: {len(high)} | Baixa relevância: {len(low)}')
    for i, v in enumerate(final, 1):
        rel = relevance_score(v)
        tag = '✅' if rel >= 1 else '⚠️'
        print(f'  {tag} {i:2}. {v["views"]:>8,}v | {v["title"][:55]}')
    return final

# ──────────────────────────────────────────────────────────
# BAIXAR TRANSCRIÇÃO
# ──────────────────────────────────────────────────────────

def baixar_transcricao(video_id: str, retries: int = 3, delay_base: int = 4, ip_block_wait: int = 60) -> list | None:
    import time
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    for attempt in range(1, retries + 1):
        try:
            t = api.fetch(video_id, languages=['pt', 'pt-BR', 'en'])
            time.sleep(delay_base)  # pausa entre requests para evitar bloqueio
            return [{'start': s.start, 'text': s.text} for s in t.snippets]
        except Exception as e:
            err = str(e)[:80]
            if 'block' in err.lower() or 'ip' in err.lower() or '429' in err:
                wait = ip_block_wait * attempt
                print(f'  [IP BLOCK] Aguardando {wait}s antes de tentar novamente...')
                time.sleep(wait)
            else:
                print(f'  [ERRO] {video_id}: {err}')
                return None
    print(f'  [FALHOU] {video_id} após {retries} tentativas')
    return None

# ──────────────────────────────────────────────────────────
# ANALISAR TRANSCRIÇÃO
# ──────────────────────────────────────────────────────────

def analisar(video: dict, snippets: list) -> dict:
    full_text = ' '.join(s['text'] for s in snippets)
    text_norm = norm(full_text)
    total_dur = snippets[-1]['start'] if snippets else 0

    # Hook: primeiros 30s
    hook = ' '.join(s['text'] for s in snippets if s['start'] <= 30)

    # Estrutura: dividir em 5 blocos de 20%
    block_size = total_dur / 5 if total_dur > 0 else 60
    blocks = []
    for i in range(5):
        start = i * block_size
        end   = (i + 1) * block_size
        block_text = ' '.join(s['text'] for s in snippets if start <= s['start'] < end)
        blocks.append(block_text[:200])

    # CTA: últimos 60s
    cta = ' '.join(s['text'] for s in snippets if s['start'] >= total_dur - 60)

    # Power words encontradas
    found_pw = [w for w in POWER_WORDS if w in text_norm]

    # Keywords mais frequentes
    words = re.findall(r'[a-z]{4,}', text_norm)
    freq  = Counter(w for w in words if w not in STOP)
    top_kw = [w for w, n in freq.most_common(15)]

    # Detectar estrutura narrativa
    estrutura = []
    for i, block in enumerate(blocks):
        pct = (i + 1) * 20
        time_start = fmt_time(i * block_size)
        estrutura.append({'pct': pct, 'time': time_start, 'preview': block[:120]})

    return {
        **video,
        'total_dur':    int(total_dur),
        'total_dur_fmt': fmt_time(total_dur),
        'hook_30s':     hook[:300],
        'cta':          cta[:250],
        'estrutura':    estrutura,
        'power_words':  found_pw,
        'top_keywords': top_kw,
        'full_text':    full_text,
    }

# ──────────────────────────────────────────────────────────
# GERAR RELATÓRIO MARKDOWN
# ──────────────────────────────────────────────────────────

def gerar_relatorio(resultados: list, tema: str, output_path: Path):
    lines = []
    lines.append(f'# ARGOS — Análise de Transcrições Concorrentes\n')
    lines.append(f'**Tema:** {tema}  \n')
    lines.append(f'**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M")}  \n')
    lines.append(f'**Vídeos analisados:** {len(resultados)}\n\n')
    lines.append('---\n\n')

    # Sumário global
    all_pw = Counter()
    all_kw = Counter()
    for r in resultados:
        all_pw.update(r['power_words'])
        all_kw.update(r['top_keywords'])

    lines.append('## POWER WORDS GLOBAIS (mais usadas nos top vídeos)\n\n')
    for w, n in all_pw.most_common(15):
        bar = '█' * min(20, n)
        lines.append(f'- `{w}` {bar} ({n}x)\n')
    lines.append('\n')

    lines.append('## KEYWORDS GLOBAIS\n\n')
    lines.append(', '.join(f'`{w}`' for w, n in all_kw.most_common(20)))
    lines.append('\n\n---\n\n')

    # Padrões de hooks
    lines.append('## PADRÕES DE HOOK VALIDADOS\n\n')
    for i, r in enumerate(resultados[:5], 1):
        lines.append(f'**#{i} — {r["views"]:,} views**\n')
        lines.append(f'> {r["hook_30s"][:200]}\n\n')

    lines.append('---\n\n')

    # Cada vídeo
    lines.append('## ANÁLISE INDIVIDUAL\n\n')
    for r in resultados:
        lines.append(f'### {r["views"]:,} views | {r["title"]}\n')
        lines.append(f'**Canal:** {r["channel"]} | **Duração:** {r["total_dur_fmt"]}\n\n')

        lines.append(f'**HOOK (30s):**\n> {r["hook_30s"][:250]}\n\n')

        lines.append('**ESTRUTURA NARRATIVA:**\n')
        for blk in r['estrutura']:
            lines.append(f'- `{blk["time"]}` ({blk["pct"]}%): {blk["preview"][:100]}...\n')
        lines.append('\n')

        lines.append(f'**CTA:**\n> {r["cta"][:200]}\n\n')
        lines.append(f'**Power words:** {", ".join(r["power_words"][:12])}\n\n')
        lines.append(f'**Keywords:** {", ".join(r["top_keywords"][:10])}\n\n')
        lines.append('---\n\n')

    output_path.write_text(''.join(lines), encoding='utf-8')
    print(f'[OK] Relatorio salvo: {output_path}')

# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--canal',  required=True)
    parser.add_argument('--video',  required=True)
    parser.add_argument('--tema',   required=True, help='Tema de busca no YouTube')
    parser.add_argument('--max',    type=int, default=5)
    parser.add_argument('--delay',  type=int, default=4,   help='Segundos entre requests (default: 4)')
    parser.add_argument('--ip-wait',type=int, default=60,  help='Segundos base de espera ao IP block (default: 60)')
    args = parser.parse_args()

    video_dir  = BASE_DIR / 'canais' / args.canal / 'videos' / args.video
    output_dir = video_dir / '1-pesquisa'
    output_dir.mkdir(parents=True, exist_ok=True)

    log_file = BASE_DIR / 'canais' / args.canal / '_config' / 'pipeline.log'

    print('=' * 60)
    print(f'ARGOS TRANSCRICOES — {args.video}')
    print(f'Tema: {args.tema}')
    print('=' * 60)

    # 1. Buscar top 10 com funil temático
    # Queries temáticas: cada tupla = (query, [keywords obrigatórias no título])
    queries_tematicas = [
        # N1 — Combo exato do tema
        (args.tema, [w for w in norm(args.tema).split() if len(w) > 4][:4]),
        # N2 — Fenômenos específicos
        ('chuva de sangue profecia biblica', ['chuva','sangue','praga']),
        ('corvos israel tel aviv sinais apocalipse', ['corvo','corvos','crows']),
        ('ceu vermelho sangue biblia profecia', ['ceu','vermelho','sangue']),
        ('lua de sangue eclipse joel apocalipse profecia', ['lua','sangue','eclipse']),
        ('morte aves animais em massa sinais biblicos', ['morte','animais','aves','peixe','praga']),
        # N3 — Sinais físicos gerais (ainda específico ao tema)
        ('sinais fisicos apocalipse biblia profecias cumpridas 2024 2025 2026', ['sinal','sinais','fisico','praga']),
        ('fenomenos naturais estranhos profecias biblicas fim dos tempos', ['fenomeno','estranho','sinal','praga']),
        ('pragas biblicas acontecendo agora apocalipse 2026', ['praga','pragas','apocalipse']),
    ]
    videos = buscar_top10_funil(args.tema, target=args.max, queries_tematicas=queries_tematicas)

    # 2. Transcrever e analisar
    resultados = []
    for v in videos:
        print(f'\n[ARGOS] Transcrevendo: {v["title"][:50]}...')
        snippets = baixar_transcricao(v['video_id'], delay_base=args.delay, ip_block_wait=args.ip_wait)
        if snippets:
            r = analisar(v, snippets)
            resultados.append(r)
            print(f'  OK | {r["total_dur_fmt"]} | {len(r["power_words"])} power words')
        else:
            print(f'  PULADO (sem transcricao)')

    if not resultados:
        print('[ERRO] Nenhuma transcricao obtida')
        return

    # 3. Salvar JSON completo
    json_path = output_dir / 'transcricoes_concorrentes.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    # 4. Gerar relatório MD para Morrigan
    md_path = output_dir / 'base_roteiro_concorrentes.md'
    gerar_relatorio(resultados, args.tema, md_path)

    # 5. Log
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f'[{now}] ARGOS — {len(resultados)} transcricoes coletadas para {args.video}\n')
        f.write(f'[{now}] ARGOS — Base do roteiro salva: 1-pesquisa/base_roteiro_concorrentes.md\n')

    print('\n' + '=' * 60)
    print(f'CONCLUIDO: {len(resultados)} videos transcritos e analisados')
    print(f'Base do roteiro: {md_path}')
    print('=' * 60)

if __name__ == '__main__':
    main()
