#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, re, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('_agency/competitive_intel/transcricoes_top5.json', encoding='utf-8'))

power_words_list = [
    'assustador','proibido','ninguem','ja esta','sendo ativado','nao te contaram',
    'escondido','revelado','urgente','atencao','cuidado','perigo','fim','apocalipse',
    'profecia','biblia','sinal','tribulacao','arrebatamento','destruicao','juizo',
    'sangue','fogo','guerra','morte','salvador','jesus','deus','espirito','anjo',
    'diabo','satanas','besta','falso','paz','verdade','segredo','nunca','sempre',
    'agora','hoje','ultimo','primeiro','mundo','brasil','israel','ira'
]

stop = {
    'de','a','o','e','que','em','um','uma','para','com','se','ao','no','na',
    'os','as','dos','das','do','da','por','sao','mas','ou','nao','foi','esta',
    'ser','ter','seu','sua','seus','suas','este','esta','isso','aqui','ali',
    'pela','pelo','mais','muito','bem','onde','quando','como','voce','isso',
    'esse','essa','eles','elas','nos','eles','isso','aquele','aquela','isso'
}

print('=' * 70)
print('ANALISE COMPETITIVA -- TOP 5 VIDEOS BIBLICOS')
print('=' * 70)

all_words = Counter()

for v in data:
    import unicodedata
    def norm(s):
        return unicodedata.normalize('NFKD', s.lower()).encode('ascii','ignore').decode()

    text_norm = norm(v['text'])

    print(f"\n--- {v['title']} ---")
    print(f"Views: {v['views']:,} | Duracao: {v['total_dur']//60}:{v['total_dur']%60:02d}min")

    print(f"\nHOOK (primeiros 30s):")
    hook_clean = v['hook_30s'].replace('\n', ' ')
    print(f"  {hook_clean[:220]}")

    print(f"\nCTA (ultimos 60s):")
    cta_clean = v['cta'].replace('\n', ' ')
    print(f"  {cta_clean[:180]}")

    found = [w for w in power_words_list if w in text_norm]
    print(f"\nPOWER WORDS ({len(found)}): {', '.join(found[:15])}")

    words = re.findall(r'[a-z]{4,}', text_norm)
    freq = Counter(w for w in words if w not in stop)
    top10 = freq.most_common(12)
    print(f"TOP KEYWORDS: {', '.join(f'{w}({n})' for w,n in top10)}")
    all_words.update(freq)

print(f"\n{'='*70}")
print('POWER WORDS GLOBAIS (5 videos combinados):')
global_top = [(w,n) for w,n in all_words.most_common(25) if len(w) > 4]
for w, n in global_top[:20]:
    bar = '#' * min(30, n//5)
    print(f"  {w:<22} {bar} ({n})")

# Salvar resumo em MD
output = []
output.append('# Analise Competitiva -- Top 5 Videos Biblicos\n')
output.append('_Fonte: transcricoes automaticas via youtube-transcript-api_\n\n')

for v in data:
    def norm(s):
        import unicodedata
        return unicodedata.normalize('NFKD', s.lower()).encode('ascii','ignore').decode()
    text_norm = norm(v['text'])
    words = re.findall(r'[a-z]{4,}', text_norm)
    freq = Counter(w for w in words if w not in stop)
    top_kw = [w for w,n in freq.most_common(10)]
    found_pw = [w for w in power_words_list if w in text_norm]

    output.append(f"## {v['views']:,} views | {v['title']}\n")
    output.append(f"**Duracao:** {v['total_dur']//60}:{v['total_dur']%60:02d}min\n\n")
    output.append(f"**HOOK (30s):** {v['hook_30s'][:200]}\n\n")
    output.append(f"**CTA:** {v['cta'][:150]}\n\n")
    output.append(f"**Power words:** {', '.join(found_pw[:12])}\n\n")
    output.append(f"**Keywords:** {', '.join(top_kw)}\n\n")
    output.append("---\n\n")

with open('_agency/competitive_intel/analise_top5.md', 'w', encoding='utf-8') as f:
    f.writelines(output)
print('\nSalvo: _agency/competitive_intel/analise_top5.md')
