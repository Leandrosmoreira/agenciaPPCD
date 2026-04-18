#!/usr/bin/env python3
"""
veo3_image_to_video.py — Gera clips Veo3 image-to-video por quadro do storyboard.

Modos:
  --plan    → Lê storyboard + durações → escreve veo3_plan_{video}.txt para aprovação
  --execute → Lê plano aprovado → chama API → baixa MP4s → reporta custo

Uso:
  python _tools/veo3_image_to_video.py --canal sinais-do-fim --video video-015-economist-manipulacao --plan
  python _tools/veo3_image_to_video.py --canal sinais-do-fim --video video-015-economist-manipulacao --execute
  python _tools/veo3_image_to_video.py --canal sinais-do-fim --video video-015-economist-manipulacao --execute --parte 1 2

Arquitetura de clips (padrão video-015):
  Parte 1 — primeiro minuto (~5-6 clips × 8s = cinematografia de abertura)
  Partes 2-5 — 2 clips cada nos quadros de maior duração (cenas mais importantes)
  Total: ~13-14 clips | Custo estimado: ~$1.66-$1.80

Saída: canais/{canal}/videos/{video}/6-assets/veo3/VEO_Q{NN}.mp4
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

API_KEY       = os.getenv("GEMINI_API_KEY", "")
MODEL         = "veo-3.1-lite-generate-preview"
BASE_URL      = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predictLongRunning"
COST_PER_CLIP = 0.128   # ~$0.016/s × 8s (veo-3.1-lite-generate-preview @ 1080p, estimativa)


# ═══════════════════════════════════════════════════════════════════════════
# UTILITÁRIOS
# ═══════════════════════════════════════════════════════════════════════════

def load_durations(video_dir: Path) -> dict:
    """Carrega durações de durations_sync.json (gerado por sync_quadros_whisper.py)."""
    p = video_dir / "4-storyboard" / "durations_sync.json"
    if p.exists():
        data = json.loads(p.read_text(encoding="utf-8"))
        return {int(k): float(v) for k, v in data.items()}
    print("[AVISO] durations_sync.json não encontrado — usando durações uniformes (7s/quadro)")
    return {}


def load_quadro_meta(video_dir: Path, q: int) -> dict:
    """Lê JSON do quadro de 6-prompts-imagem/ para obter scene_title, subject, etc."""
    p = video_dir / "6-prompts-imagem" / f"Q{q:02d}.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def build_veo3_prompt(meta: dict) -> str:
    """
    Constrói prompt Veo3 a partir do JSON do quadro.
    Combina: subject.primary + subject.secondary + style textual + shot info.
    Adiciona instrução final para cinematografia limpa.
    """
    parts = []
    subj = meta.get("subject", {})
    if subj.get("primary"):
        parts.append(subj["primary"])
    if subj.get("secondary"):
        parts.append(subj["secondary"])
    style = meta.get("style_reference", {}).get("textual_description", "")
    if style:
        parts.append(style)
    shot = meta.get("shot", {})
    shot_info = ", ".join(v for k, v in shot.items()
                         if k in ("type", "camera_angle") and v)
    if shot_info:
        parts.append(f"Camera: {shot_info}")
    env = meta.get("environment", {})
    if env.get("atmosphere"):
        parts.append(env["atmosphere"])
    parts.append(
        "Cinematic slow motion, subtle camera movement, "
        "no dialogue, no text overlay, no watermark, no people talking to camera"
    )
    return ". ".join(p for p in parts if p)


def detect_batch_ranges(video_dir: Path) -> dict:
    """
    Detecta batch ranges automaticamente contando JSONs em 6-prompts-imagem/.
    Divide em 5 grupos proporcionais.
    Retorna {1: [q1, q2, ...], 2: [...], ...}
    """
    img_dir = video_dir / "6-prompts-imagem"
    q_numbers = sorted([
        int(f.stem[1:])
        for f in img_dir.glob("Q*.json")
        if f.stem[1:].isdigit()
    ])
    if not q_numbers:
        # Fallback: Q01-Q60
        q_numbers = list(range(1, 61))

    total = len(q_numbers)
    per_parte = total // 5
    ranges = {}
    for i in range(5):
        start = i * per_parte
        end = (i + 1) * per_parte if i < 4 else total
        ranges[i + 1] = q_numbers[start:end]
    return ranges


def select_clips_parte1(durations: dict, quadros: list, max_seconds: float = 62.0) -> list:
    """
    Seleciona quadros da parte 1 dentro dos primeiros max_seconds.
    Pula Q01 (tela de abertura/gancho).
    """
    cumulative = 0.0
    selected = []
    for q in sorted(quadros):
        dur = durations.get(q, 7.0)
        if q == 1:
            cumulative += dur
            continue
        if cumulative >= max_seconds:
            break
        selected.append(q)
        cumulative += dur
    return selected


def select_clips_best(durations: dict, quadros: list, n: int = 2) -> list:
    """
    Seleciona os N quadros com maior duração de narração (cenas mais importantes).
    Pula Q01.
    """
    valid = [(q, durations.get(q, 7.0)) for q in quadros if q != 1]
    valid.sort(key=lambda x: x[1], reverse=True)
    return sorted([q for q, _ in valid[:n]])


# ═══════════════════════════════════════════════════════════════════════════
# MODO --plan
# ═══════════════════════════════════════════════════════════════════════════

def generate_plan(args, video_dir: Path):
    """
    Gera plano de clips em formato TXT + JSON para aprovação de Snayder.
    """
    durations   = load_durations(video_dir)
    batch_ranges = detect_batch_ranges(video_dir)

    plan_lines = [
        f"# Veo3 Plan — {args.video}",
        f"# Gerado: 2026-04-17",
        f"# Model: {MODEL} | Resolution: 1080p | Duration: 8s/clip",
        f"# ─────────────────────────────────────────────────────────────",
        f"# INSTRUÇÃO: Revise os prompts, edite se necessário.",
        f"# Depois rode: python _tools/veo3_image_to_video.py --canal {args.canal} --video {args.video} --execute",
        f"# Para executar só partes específicas adicione: --parte 1 2",
        "",
    ]

    clip_num  = 0
    all_clips = []

    # ── Parte 1 — primeiro minuto ────────────────────────────────────────
    p1_quadros  = batch_ranges.get(1, [])
    p1_selected = select_clips_parte1(durations, p1_quadros, max_seconds=62.0)

    plan_lines.append(
        "## PARTE 1 — Primeiro Minuto  "
        f"(~{len(p1_selected)} clips × 8s ≈ {len(p1_selected)*8}s de cinematografia)"
    )
    plan_lines.append("")

    for q in p1_selected:
        clip_num += 1
        meta  = load_quadro_meta(video_dir, q)
        title = meta.get("scene_title", f"Quadro Q{q:02d}")
        prompt = build_veo3_prompt(meta)
        img_path = video_dir / "6-assets" / "imagens" / f"Q{q:02d}.png"

        plan_lines += [
            f"CLIP_{clip_num:02d} | Q{q:02d} | parte=1 | dur_narr={durations.get(q,7):.1f}s | {title}",
            f"  IMAGE:  {img_path.relative_to(ROOT) if img_path.exists() else '⚠ IMAGEM NÃO ENCONTRADA: ' + str(img_path)}",
            f"  PROMPT: {prompt}",
            "",
        ]
        all_clips.append({
            "clip": clip_num,
            "q":    q,
            "parte": 1,
            "image": str(img_path),
            "prompt": prompt,
            "title": title,
        })

    # ── Partes 2-5 — 2 destaques cada ───────────────────────────────────
    for parte in range(2, 6):
        p_quadros  = batch_ranges.get(parte, [])
        p_selected = select_clips_best(durations, p_quadros, n=2)

        plan_lines.append(f"## PARTE {parte} — 2 Destaques Cinematográficos")
        plan_lines.append("")

        for q in p_selected:
            clip_num += 1
            meta   = load_quadro_meta(video_dir, q)
            title  = meta.get("scene_title", f"Quadro Q{q:02d}")
            prompt = build_veo3_prompt(meta)
            img_path = video_dir / "6-assets" / "imagens" / f"Q{q:02d}.png"

            plan_lines += [
                f"CLIP_{clip_num:02d} | Q{q:02d} | parte={parte} | dur_narr={durations.get(q,7):.1f}s | {title}",
                f"  IMAGE:  {img_path.relative_to(ROOT) if img_path.exists() else '⚠ IMAGEM NÃO ENCONTRADA: ' + str(img_path)}",
                f"  PROMPT: {prompt}",
                "",
            ]
            all_clips.append({
                "clip": clip_num,
                "q":    q,
                "parte": parte,
                "image": str(img_path),
                "prompt": prompt,
                "title": title,
            })

    # ── Custo estimado ───────────────────────────────────────────────────
    n_clips        = len(all_clips)
    estimated_cost = n_clips * COST_PER_CLIP

    plan_lines += [
        "## CUSTO ESTIMADO",
        f"  {n_clips} clips × ${COST_PER_CLIP:.3f}/clip (veo-3.1-lite-generate-preview @ 1080p/8s)",
        f"  Total estimado: ${estimated_cost:.2f}",
        f"  NOTA: Verifique preço atual em ai.google.dev/gemini-api/docs/pricing",
        "",
        "## STATUS",
        "  [ ] Revisado por Snayder",
        "  [ ] Prompts editados (se necessário)",
        "  [ ] Aprovado para execução",
    ]

    # ── Salvar ───────────────────────────────────────────────────────────
    assets_dir = video_dir / "6-assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    plan_txt  = assets_dir / f"veo3_plan_{args.video}.txt"
    plan_json = assets_dir / f"veo3_plan_{args.video}.json"

    plan_txt.write_text("\n".join(plan_lines), encoding="utf-8")
    plan_json.write_text(json.dumps(all_clips, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n".join(plan_lines))
    print(f"\n{'='*60}")
    print(f"[OK] Plano TXT salvo : {plan_txt}")
    print(f"[OK] Plano JSON salvo: {plan_json}")
    print(f"[CUSTO] {n_clips} clips | Estimado: ${estimated_cost:.2f}")
    print(f"{'='*60}")
    print(f"\nPRÓXIMO PASSO: Revise {plan_txt.name} e rode --execute quando aprovado.")


# ═══════════════════════════════════════════════════════════════════════════
# POLLING DA OPERAÇÃO VEO3
# ═══════════════════════════════════════════════════════════════════════════

def poll_operation(operation_name: str, max_wait_s: int = 600) -> dict:
    """
    Faz polling da operação Veo3 até completar.
    Aguarda até max_wait_s segundos (default: 10 min).
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/{operation_name}?key={API_KEY}"
    interval = 10
    elapsed  = 0
    while elapsed < max_wait_s:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if data.get("done"):
            return data
        print(f"  Aguardando... {elapsed + interval}s", flush=True)
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(
        f"Operação {operation_name} não concluiu em {max_wait_s}s. "
        f"Verifique: GET {url}"
    )


def extract_video_uri(result: dict) -> str:
    """
    Extrai URI do vídeo da resposta da operação Veo3.
    Tenta dois caminhos conhecidos da API.
    """
    # Caminho 1: response.generateVideoResponse.generatedSamples[0].video.uri
    try:
        r = result.get("response", {})
        # A chave pode ter @type como prefixo — não importa, tentamos os campos direto
        return r["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
    except (KeyError, IndexError, TypeError):
        pass

    # Caminho 2: response.generatedSamples[0].video.uri
    try:
        r = result.get("response", {})
        return r["generatedSamples"][0]["video"]["uri"]
    except (KeyError, IndexError, TypeError):
        pass

    raise ValueError(
        f"Não foi possível extrair URI do vídeo da resposta:\n"
        f"{json.dumps(result, indent=2, ensure_ascii=False)[:1000]}"
    )


# ═══════════════════════════════════════════════════════════════════════════
# MODO --execute
# ═══════════════════════════════════════════════════════════════════════════

def execute_plan(args, video_dir: Path):
    """
    Executa o plano aprovado: chama API Veo3 para cada clip, baixa MP4s.
    """
    if not API_KEY:
        print("[ERRO] GEMINI_API_KEY não encontrada no .env")
        print("  Adicione: GEMINI_API_KEY=sua_chave_aqui")
        sys.exit(1)

    plan_json = video_dir / "6-assets" / f"veo3_plan_{args.video}.json"
    if not plan_json.exists():
        print(f"[ERRO] Plano não encontrado: {plan_json}")
        print(f"  Rode primeiro: python _tools/veo3_image_to_video.py "
              f"--canal {args.canal} --video {args.video} --plan")
        sys.exit(1)

    clips = json.loads(plan_json.read_text(encoding="utf-8"))

    # Filtrar partes se --parte especificado
    if args.parte:
        clips = [c for c in clips if c["parte"] in args.parte]
        print(f"[INFO] Filtrando partes: {args.parte} → {len(clips)} clips")

    out_dir = video_dir / "6-assets" / "veo3"
    out_dir.mkdir(parents=True, exist_ok=True)

    total_cost = 0.0
    results    = []
    errors     = []

    print(f"\nVEO3 EXECUTE — {args.video}")
    print(f"Clips: {len(clips)} | Model: {MODEL} | 1080p/8s")
    print(f"Output: {out_dir}")
    print("=" * 60)

    for c in clips:
        img_path = Path(c["image"])
        q        = c["q"]
        clip_num = c["clip"]

        print(f"\n[CLIP_{clip_num:02d}] Q{q:02d} — {c['title']}", flush=True)

        if not img_path.exists():
            print(f"  [SKIP] Imagem não encontrada: {img_path}")
            errors.append(f"CLIP_{clip_num:02d} Q{q:02d}: imagem não encontrada")
            continue

        # Verificar se já foi gerado (skip se existir)
        out_path = out_dir / f"VEO_Q{q:02d}.mp4"
        if out_path.exists() and out_path.stat().st_size > 100_000:
            print(f"  [SKIP] Já existe: {out_path.name} ({out_path.stat().st_size/1024/1024:.1f} MB)")
            results.append({
                "q": q, "file": str(out_path),
                "size_mb": round(out_path.stat().st_size/1024/1024, 1),
                "status": "skipped"
            })
            continue

        # Encode imagem em base64
        print(f"  Encoding {img_path.name}...", flush=True)
        img_data = base64.b64encode(img_path.read_bytes()).decode("utf-8")

        # Payload da API
        payload = {
            "instances": [{
                "prompt": c["prompt"],
                "image": {
                    "inlineData": {
                        "mimeType": "image/png",
                        "data": img_data
                    }
                }
            }],
            "parameters": {
                "resolution":      "1080p",
                "durationSeconds": "8",
                "aspectRatio":     "16:9"
            }
        }

        # Chamar API
        print(f"  Chamando Veo3 API...", flush=True)
        try:
            resp = requests.post(
                f"{BASE_URL}?key={API_KEY}",
                json=payload,
                timeout=60
            )
            resp.raise_for_status()
        except requests.HTTPError as e:
            print(f"  [ERRO HTTP] {e}\n  {resp.text[:500]}")
            errors.append(f"CLIP_{clip_num:02d} Q{q:02d}: HTTP {resp.status_code}")
            continue
        except requests.RequestException as e:
            print(f"  [ERRO REQUEST] {e}")
            errors.append(f"CLIP_{clip_num:02d} Q{q:02d}: {e}")
            continue

        op_data = resp.json()
        op_name = op_data.get("name", "")
        if not op_name:
            print(f"  [ERRO] Resposta sem 'name': {op_data}")
            errors.append(f"CLIP_{clip_num:02d} Q{q:02d}: sem operation name")
            continue

        print(f"  Operation: {op_name}", flush=True)

        # Polling
        print(f"  Aguardando geração (pode levar 2-5 min)...", flush=True)
        try:
            result = poll_operation(op_name)
        except TimeoutError as e:
            print(f"  [TIMEOUT] {e}")
            errors.append(f"CLIP_{clip_num:02d} Q{q:02d}: timeout")
            continue

        # Extrair URI
        try:
            video_uri = extract_video_uri(result)
        except ValueError as e:
            print(f"  [ERRO] {e}")
            errors.append(f"CLIP_{clip_num:02d} Q{q:02d}: URI não encontrada")
            continue

        # Baixar vídeo
        print(f"  Baixando → {out_path.name}...", flush=True)
        try:
            # URI pode ser GCS (gs://) ou HTTPS
            if video_uri.startswith("gs://"):
                # Converter para URL HTTPS da Gemini API
                file_name = video_uri.replace("gs://", "").split("/", 1)[-1]
                download_url = f"https://generativelanguage.googleapis.com/v1beta/files/{file_name}?key={API_KEY}"
            else:
                sep = "&" if "?" in video_uri else "?"
                download_url = f"{video_uri}{sep}key={API_KEY}"

            dl = requests.get(download_url, stream=True, timeout=120)
            dl.raise_for_status()
            with open(out_path, "wb") as f:
                for chunk in dl.iter_content(chunk_size=65536):
                    f.write(chunk)
        except Exception as e:
            print(f"  [ERRO DOWNLOAD] {e}")
            errors.append(f"CLIP_{clip_num:02d} Q{q:02d}: download falhou — {e}")
            continue

        size_mb = out_path.stat().st_size / 1024 / 1024
        print(f"  [OK] {out_path.name} ({size_mb:.1f} MB)", flush=True)
        total_cost += COST_PER_CLIP
        results.append({
            "q": q,
            "file": str(out_path),
            "size_mb": round(size_mb, 1),
            "status": "generated"
        })

    # ── Relatório final ──────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"VEO3 CONCLUÍDO — {args.video}")
    print(f"{'='*60}")
    print(f"Gerados:  {len([r for r in results if r['status']=='generated'])}")
    print(f"Pulados:  {len([r for r in results if r['status']=='skipped'])}")
    print(f"Erros:    {len(errors)}")
    if results:
        print("\nARQUIVOS:")
        for r in results:
            print(f"  Q{r['q']:02d}: {Path(r['file']).name} ({r['size_mb']} MB) [{r['status']}]")
    if errors:
        print("\nERROS:")
        for e in errors:
            print(f"  ✗ {e}")
    print(f"\nCUSTO TOTAL ESTIMADO: ${total_cost:.2f}")
    print(f"{'='*60}")
    print(f"\nArquivos em: {out_dir}")


# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(
        description="Veo3 image-to-video para quadros do storyboard"
    )
    ap.add_argument("--canal",   required=True,  help="Nome do canal (ex: sinais-do-fim)")
    ap.add_argument("--video",   required=True,  help="Slug do vídeo (ex: video-015-economist-manipulacao)")
    ap.add_argument("--plan",    action="store_true", help="Gera plano de clips para aprovação")
    ap.add_argument("--execute", action="store_true", help="Executa plano aprovado via API")
    ap.add_argument("--parte",   nargs="+", type=int,
                    help="Filtrar partes específicas (ex: --parte 1 2)")
    args = ap.parse_args()

    if not args.plan and not args.execute:
        ap.print_help()
        sys.exit(1)

    video_dir = ROOT / "canais" / args.canal / "videos" / args.video
    if not video_dir.exists():
        print(f"[ERRO] Diretório do vídeo não encontrado: {video_dir}")
        sys.exit(1)

    if args.plan:
        generate_plan(args, video_dir)
    elif args.execute:
        execute_plan(args, video_dir)


if __name__ == "__main__":
    main()
