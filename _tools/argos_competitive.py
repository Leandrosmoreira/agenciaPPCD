#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Argos Competitive — Coleta semanal de inteligência competitiva
YouTube Data API v3 — Nicho Bíblico / Apocalipse

Uso:
  python argos_competitive.py
  python argos_competitive.py --dias 14        (últimos 14 dias)
  python argos_competitive.py --queries 5      (top 5 queries)
  python argos_competitive.py --dry-run        (sem salvar, só mostra)

Quota usada por execução: ~900 unidades (de 10.000/dia disponíveis)

Salva em:
  _agency/competitive_intel/semana-YYYY-WW.json   (dados brutos)
  _agency/competitive_intel/insights-YYYY-WW.md   (análise Hermes)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("ERRO: pip install google-api-python-client")
    sys.exit(1)

# ─── Config ────────────────────────────────────────────────────────────────

BASE_DIR     = Path(__file__).resolve().parent.parent
INTEL_DIR    = BASE_DIR / "_agency" / "competitive_intel"
ENV_FILE     = BASE_DIR / "_agency" / ".env"

# Canais concorrentes para monitorar diretamente
CANAIS_CONCORRENTES = {
    "Dr Éden":             "UCuWsf-qGxpMnaibrN-XUHmA",   # 216k subs — nicho idêntico
    "Fatos Desconhecidos": "UCbAiIkPobUFy71zlmwVw3jw",   # 22.8M subs — referência de formato
    "Cortes IA":           "UCd5qbAL7aV3SF1nhvlZVStg",   # Clipes virais escatologia
}

MAX_CANAL_VIDEOS = 20   # top 20 vídeos por canal

# Queries de busca — nicho bíblico/apocalipse
SEARCH_QUERIES = [
    "bíblia apocalipse",
    "sinais do fim",
    "marca da besta",
    "anticristo 2026",
    "profecias bíblicas",
    "arrebatamento",
    "fim dos tempos",
    "armagedom bíblia",
    "666 chip tecnologia",
    "grande tribulação",
]

MAX_RESULTS_PER_QUERY = 25   # 25 × 10 queries = 250 vídeos únicos
RELEVANCE_LANGUAGE   = "pt"  # prioriza conteúdo em português

# ─── 6 Layers (base de análise Hermes) ────────────────────────────────────

LAYER_PATTERNS = {
    "L1_urgencia": [
        r"\b(agora|hoje|esta semana|já|2026|2025|está acontecendo|foi ativado|começa)\b",
        r"\b(alerta|urgente|breaking|imediato|neste momento)\b",
    ],
    "L2_segredo": [
        r"\b(ninguém|proibido|escondido|não te contaram|revelado|oculto|removido)\b",
        r"\b(igrejas não|vaticano|apagado|banido|verdade que)\b",
    ],
    "L3_atual": [
        r"\b(trump|israel|irã|ucrânia|cbdc|ia |inteligência artificial|chip)\b",
        r"\b(guerra|cessar.fogo|davos|economia|tecnologia)\b",
    ],
    "L4_numero": [
        r"\b(\d+)\s*(sinais|profecias|passos|fatos|coisas|países|selos|trombetas)\b",
        r"\b(144\.?000|666|777|primeiro|sete|três|quatro)\b",
    ],
    "L5_medo_esperanca": [
        r"\b(assustador|terrível|aterrorizante|chocante|sobrevive|escapa|proteção)\b",
        r"\b(julgamento|destruição|tribulação|fim|morte|salvo|escape)\b",
    ],
    "L6_identidade": [
        r"\b(você|quem lê|quem conhece|cristão|crente|remanescente|os seus)\b",
        r"\b(sua fé|você precisa|você não sabe|nós sabemos)\b",
    ],
}

POWER_WORDS = ["assustador", "proibido", "revelado", "ninguém", "agora",
               "já está", "sendo ativado", "não te contaram", "escondido"]


# ─── Helpers ──────────────────────────────────────────────────────────────

def load_api_key() -> str:
    """Carrega YOUTUBE_API_KEY do .env ou variável de ambiente."""
    # Tenta variável de ambiente primeiro
    key = os.environ.get("YOUTUBE_API_KEY", "")
    if key:
        return key

    # Tenta .env da agência
    env_paths = [ENV_FILE, BASE_DIR / ".env"]
    for env_path in env_paths:
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("YOUTUBE_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    # remove duplicata "YOUTUBE_API_KEY=AIza..." caso exista
                    if key.startswith("YOUTUBE_API_KEY="):
                        key = key.split("=", 1)[1].strip()
                    if key:
                        return key

    print("ERRO: YOUTUBE_API_KEY não encontrada em .env")
    sys.exit(1)


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def analyze_layers(title: str) -> dict:
    """Detecta quais dos 6 layers um título usa."""
    title_lower = title.lower()
    result = {}
    score = 0
    for layer, patterns in LAYER_PATTERNS.items():
        found = any(re.search(p, title_lower) for p in patterns)
        result[layer] = found
        if found:
            score += 1
    result["score"] = score
    result["power_words"] = [w for w in POWER_WORDS if w in title_lower]
    return result


def estimate_ctr_tier(views: int, age_days: int, layer_score: int) -> str:
    """Estima tier de CTR baseado em views por dia e layers."""
    vpd = views / max(1, age_days)
    if vpd > 5000 or (vpd > 1000 and layer_score >= 3):
        return "S"   # viral
    elif vpd > 1000 or (vpd > 300 and layer_score >= 2):
        return "A"   # alto
    elif vpd > 200:
        return "B"   # médio
    elif vpd > 50:
        return "C"   # baixo
    else:
        return "D"   # negligível


def iso_to_days(published_at: str) -> int:
    """Converte data ISO para dias desde publicação."""
    try:
        dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        return max(1, (datetime.now(timezone.utc) - dt).days)
    except:
        return 7


# ─── Coleta YouTube API ───────────────────────────────────────────────────

def search_videos(youtube, query: str, published_after: str,
                  max_results: int) -> list[str]:
    """Retorna lista de videoIds para uma query."""
    try:
        resp = youtube.search().list(
            q=query,
            type="video",
            part="id",
            publishedAfter=published_after,
            order="viewCount",
            relevanceLanguage=RELEVANCE_LANGUAGE,
            maxResults=max_results,
            regionCode="BR",
        ).execute()
        return [item["id"]["videoId"] for item in resp.get("items", [])]
    except HttpError as e:
        log(f"  AVISO search '{query}': {e}")
        return []


def get_video_details(youtube, video_ids: list[str]) -> list[dict]:
    """Busca título, views, canal e duração para lista de IDs (máx 50 por call)."""
    videos = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        try:
            resp = youtube.videos().list(
                id=",".join(batch),
                part="snippet,statistics,contentDetails",
            ).execute()
            for item in resp.get("items", []):
                snip  = item.get("snippet", {})
                stats = item.get("statistics", {})
                dur   = item.get("contentDetails", {}).get("duration", "PT0S")
                videos.append({
                    "id":           item["id"],
                    "title":        snip.get("title", ""),
                    "channel":      snip.get("channelTitle", ""),
                    "published_at": snip.get("publishedAt", ""),
                    "views":        int(stats.get("viewCount", 0)),
                    "likes":        int(stats.get("likeCount", 0)),
                    "duration":     dur,
                })
        except HttpError as e:
            log(f"  AVISO videos.list batch {i}: {e}")
    return videos


# ─── Geração de Insights ──────────────────────────────────────────────────

def generate_insights(videos: list[dict], week_label: str) -> str:
    """Gera relatório markdown de insights para Hermes."""
    # Filtra e ordena por views
    top = sorted([v for v in videos if v["views"] > 100],
                 key=lambda x: x["views"], reverse=True)[:30]

    # Conta layers mais comuns nos top 10
    layer_count = {k: 0 for k in LAYER_PATTERNS}
    power_word_count = {}
    for v in top[:10]:
        analysis = analyze_layers(v["title"])
        for layer, active in analysis.items():
            if layer in layer_count and active:
                layer_count[layer] += 1
        for pw in analysis.get("power_words", []):
            power_word_count[pw] = power_word_count.get(pw, 0) + 1

    lines = [
        f"# Insights Competitivos — {week_label}",
        f"_Gerado por Argos em {datetime.now().strftime('%d/%m/%Y %H:%M')}_",
        f"\nTotal de vídeos analisados: **{len(videos)}**",
        f"Vídeos com >100 views: **{len(top)}**",
        "",
        "## Top 10 — Views desta semana",
        "",
        "| # | Views | Tier | Layers | Título |",
        "|---|-------|------|--------|--------|",
    ]

    for i, v in enumerate(top[:10], 1):
        age  = iso_to_days(v["published_at"])
        analysis = analyze_layers(v["title"])
        tier = estimate_ctr_tier(v["views"], age, analysis["score"])
        active_layers = [k.split("_")[0] for k, a in analysis.items()
                         if k.startswith("L") and a]
        layer_str = "+".join(active_layers) if active_layers else "—"
        lines.append(
            f"| {i} | {v['views']:,} | **{tier}** | {layer_str} | {v['title'][:70]} |"
        )

    # Layers mais usados nos top 10
    lines += [
        "",
        "## Layers dominantes esta semana (top 10)",
        "",
    ]
    sorted_layers = sorted(layer_count.items(), key=lambda x: x[1], reverse=True)
    for layer, count in sorted_layers:
        bar = "█" * count + "░" * (10 - count)
        label = layer.replace("_", " ").upper()
        lines.append(f"- `{label}` {bar} {count}/10")

    # Power words
    if power_word_count:
        lines += ["", "## Power words mais frequentes", ""]
        for word, cnt in sorted(power_word_count.items(),
                                key=lambda x: x[1], reverse=True):
            lines.append(f"- **{word}** × {cnt}")

    # Fórmulas recomendadas
    top_layer = sorted_layers[0][0] if sorted_layers else "L2_segredo"
    formulas_map = {
        "L1_urgencia":      "**[TEMA] JÁ ESTÁ [ACONTECENDO]** — Bíblia Revela o Que Vem Depois",
        "L2_segredo":       "**O Que NINGUÉM Te Conta Sobre [TEMA]** (Apocalipse [X])",
        "L3_atual":         "**[EVENTO REAL] CUMPRE** a Profecia de [REFERÊNCIA BÍBLICA]",
        "L4_numero":        "**[N] Sinais de [TEMA]** que Já se Cumpriram em 2026",
        "L5_medo_esperanca":"**[TEMA] É ASSUSTADOR...** Mas ISSO Te Protege",
        "L6_identidade":    "**Quem Conhece a Bíblia JÁ SABE** — E Você?",
    }
    lines += [
        "",
        "## Fórmula recomendada para próximos títulos",
        "",
        f"> Layer dominante esta semana: `{top_layer}`",
        "",
        f"```",
        formulas_map.get(top_layer, ""),
        "```",
        "",
        "---",
        "_Use este arquivo como contexto ao invocar Hermes para gerar títulos._",
    ]

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Argos Competitive — Inteligência YouTube")
    parser.add_argument("--dias",    type=int, default=7,   help="Janela de dias (padrão: 7)")
    parser.add_argument("--queries", type=int, default=len(SEARCH_QUERIES),
                        help=f"Número de queries (padrão: {len(SEARCH_QUERIES)})")
    parser.add_argument("--dry-run", action="store_true",   help="Não salva arquivos")
    args = parser.parse_args()

    # Setup
    INTEL_DIR.mkdir(parents=True, exist_ok=True)
    week_label = datetime.now().strftime("%Y-W%W")
    published_after = (datetime.now(timezone.utc) - timedelta(days=args.dias)
                       ).strftime("%Y-%m-%dT00:00:00Z")

    log(f"Argos Competitive | Semana {week_label} | Janela: {args.dias} dias")
    log(f"Queries: {args.queries} | publishedAfter: {published_after}")

    # Build YouTube client
    api_key = load_api_key()
    youtube = build("youtube", "v3", developerKey=api_key)

    # Coleta
    all_ids: set[str] = set()
    queries = SEARCH_QUERIES[:args.queries]

    for i, query in enumerate(queries, 1):
        log(f"  [{i}/{len(queries)}] Buscando: '{query}'")
        ids = search_videos(youtube, query, published_after, MAX_RESULTS_PER_QUERY)
        new_ids = [id for id in ids if id not in all_ids]
        all_ids.update(new_ids)
        log(f"    +{len(new_ids)} vídeos únicos (total: {len(all_ids)})")

    log(f"\nBuscando detalhes de {len(all_ids)} vídeos...")
    videos = get_video_details(youtube, list(all_ids))

    # Enriquece com análise de layers
    for v in videos:
        v["layers"] = analyze_layers(v["title"])
        age = iso_to_days(v["published_at"])
        v["ctr_tier"] = estimate_ctr_tier(v["views"], age, v["layers"]["score"])

    # Ordena por views
    videos.sort(key=lambda x: x["views"], reverse=True)

    log(f"\nTop 5 vídeos desta semana:")
    for v in videos[:5]:
        log(f"  {v['views']:>8,} views | {v['ctr_tier']} | {v['title'][:60]}")

    # Gera insights
    insights_md = generate_insights(videos, week_label)

    if args.dry_run:
        log("\n[DRY RUN] Nada foi salvo.")
        print("\n" + insights_md.encode("cp1252", errors="replace").decode("cp1252"))
        return

    # Salva insights MD
    md_path = INTEL_DIR / f"insights-{week_label}.md"
    md_path.write_text(insights_md, encoding="utf-8")
    log(f"Salvo: {md_path}")

    # Atualiza symlink "latest"
    latest_json = INTEL_DIR / "latest.json"
    latest_md   = INTEL_DIR / "latest.md"
    latest_json.write_text(json_path.read_text(encoding="utf-8"), encoding="utf-8")
    latest_md.write_text(insights_md, encoding="utf-8")
    log(f"Atualizado: latest.json + latest.md")

    # ── Coleta top vídeos dos canais concorrentes ──────────────────────────
    log("\nColetando top vídeos dos canais concorrentes...")
    canal_videos = {}
    for nome, channel_id in CANAIS_CONCORRENTES.items():
        try:
            resp = youtube.search().list(
                channelId=channel_id,
                type="video",
                part="id,snippet",
                order="viewCount",
                maxResults=MAX_CANAL_VIDEOS,
            ).execute()
            ids = [item["id"]["videoId"] for item in resp.get("items", [])]
            details = get_video_details(youtube, ids)
            for v in details:
                v["layers"] = analyze_layers(v["title"])
                age = iso_to_days(v["published_at"])
                v["ctr_tier"] = estimate_ctr_tier(v["views"], age, v["layers"]["score"])
            details.sort(key=lambda x: x["views"], reverse=True)
            canal_videos[nome] = details
            log(f"  [{nome}] {len(details)} vídeos | top: {details[0]['title'][:50] if details else 'N/A'}")
        except Exception as e:
            log(f"  [{nome}] ERRO: {e}")

    # Salva canal_videos no JSON
    output_data = {
        "week":         week_label,
        "collected_at": datetime.now().isoformat(),
        "dias":         args.dias,
        "total":        len(videos),
        "videos":       videos,
        "canais_concorrentes": canal_videos,
    }

    if not args.dry_run:
        json_path = INTEL_DIR / f"semana-{week_label}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        log(f"\nTop vídeos por canal:")
        for nome, vids in canal_videos.items():
            log(f"  {nome}:")
            for v in vids[:5]:
                log(f"    {v['views']:>8,} | {v['ctr_tier']} | {v['title'][:60]}")

    log(f"\nConcluído. {len(videos)} vídeos | quota usada: ~{len(queries)*100 + len(all_ids)//50 + 10} unidades")


if __name__ == "__main__":
    main()
