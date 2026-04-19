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
import subprocess
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
# Modelos image-to-video:
#   - veo-3.1-generate-preview       → standard (qualidade máxima, usado na parte 1)
#   - veo-3.1-fast-generate-preview  → fast (mais barato, usado nas partes 2-5)
MODEL_STANDARD = "veo-3.1-generate-preview"
MODEL_FAST     = "veo-3.1-fast-generate-preview"
BASE_URL_TMPL  = "https://generativelanguage.googleapis.com/v1beta/models/{model}:predictLongRunning"
#   Standard: generateAudio=False → ~50% do preço. Fast: gera áudio, stripamos via ffmpeg.
COST_STANDARD  = 0.160   # ~$0.020/s × 8s @ 1080p sem áudio (param aceito)
COST_FAST      = 0.128   # ~$0.016/s × 8s @ 1080p COM áudio (fast não aceita flag, áudio removido depois)

def model_for_parte(parte: int) -> str:
    """Fast em tudo — Snayder escolheu opção C (mais barata)."""
    return MODEL_FAST

def cost_for_parte(parte: int) -> float:
    return COST_FAST


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
        f"# Model: {MODEL_FAST} (todas as partes) | 1080p/8s | áudio removido via ffmpeg",
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
        img_path = video_dir / "6-assets" / f"Q{q:02d}.png"

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
            img_path = video_dir / "6-assets" / f"Q{q:02d}.png"

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
    estimated_cost = n_clips * COST_FAST

    plan_lines += [
        "## CUSTO ESTIMADO",
        f"  {n_clips} clips × ${COST_FAST:.3f} ({MODEL_FAST} @ 1080p/8s) = ${estimated_cost:.2f}",
        f"  Áudio gerado pela API é removido via ffmpeg -an após download.",
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
# FILES API — upload imagem → URI (exigido pelo veo-3.1-lite)
# ═══════════════════════════════════════════════════════════════════════════

def upload_to_files_api(img_path: Path) -> str:
    """
    Faz upload da imagem para a Gemini Files API.
    Retorna o fileUri (ex: 'https://generativelanguage.googleapis.com/v1beta/files/abc123').
    TTL: 48h — arquivo deletado automaticamente pela Google.
    """
    upload_url = f"https://generativelanguage.googleapis.com/upload/v1beta/files?key={API_KEY}"
    img_bytes  = img_path.read_bytes()
    metadata   = json.dumps({"file": {"display_name": img_path.name}})

    resp = requests.post(
        upload_url,
        headers={"X-Goog-Upload-Protocol": "multipart"},
        files=[
            ("metadata", (None, metadata, "application/json")),
            ("file",     (img_path.name, img_bytes, "image/png")),
        ],
        timeout=120,
    )
    resp.raise_for_status()
    data     = resp.json()
    file_uri = data["file"]["uri"]
    return file_uri


def delete_from_files_api(file_uri: str):
    """Remove arquivo da Files API após uso (opcional — TTL 48h)."""
    # URI formato: .../v1beta/files/{file_id}
    # DELETE endpoint: DELETE .../v1beta/files/{file_id}?key=...
    try:
        file_id = file_uri.rstrip("/").split("/files/")[-1]
        del_url = f"https://generativelanguage.googleapis.com/v1beta/files/{file_id}?key={API_KEY}"
        requests.delete(del_url, timeout=15)
    except Exception:
        pass  # Falha silenciosa — TTL 48h garante limpeza automática


# ═══════════════════════════════════════════════════════════════════════════
# POLLING DA OPERAÇÃO VEO3
# ═══════════════════════════════════════════════════════════════════════════

def strip_audio(mp4_path: Path) -> None:
    """Remove áudio do MP4 via ffmpeg -an. Sobrescreve o arquivo original."""
    tmp = mp4_path.with_suffix(".noaudio.mp4")
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", str(mp4_path), "-c:v", "copy", "-an", str(tmp)],
        capture_output=True, text=True
    )
    if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
        mp4_path.unlink()
        tmp.rename(mp4_path)
    else:
        print(f"  [WARN] ffmpeg -an falhou, mantendo com áudio: {r.stderr[:200]}")
        if tmp.exists():
            tmp.unlink()


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
    print(f"Clips: {len(clips)} | Model: {MODEL_FAST} | 1080p/8s | áudio removido via ffmpeg")
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

        # 1. Encode imagem base64
        print(f"  Encoding {img_path.name}...", flush=True)
        img_data = base64.b64encode(img_path.read_bytes()).decode("utf-8")

        # 2. Payload — Gemini Dev API usa bytesBase64Encoded (igual Vertex AI)
        #    Confirmado via SDK oficial googleapis/python-genai → _Image_to_mldev
        parameters = {
            "resolution":      "1080p",
            "durationSeconds": 8,
            "aspectRatio":     "16:9",
        }
        # Fast não aceita generateAudio — áudio é removido via ffmpeg após download.

        payload = {
            "instances": [{
                "prompt": c["prompt"],
                "image": {
                    "bytesBase64Encoded": img_data,
                    "mimeType":           "image/png"
                }
            }],
            "parameters": parameters
        }

        # 3. Chamar API Veo3 — modelo depende da parte (standard p/ parte 1, fast demais)
        model    = model_for_parte(c["parte"])
        base_url = BASE_URL_TMPL.format(model=model)
        print(f"  Chamando Veo3 API ({model})...", flush=True)
        try:
            resp = requests.post(
                f"{base_url}?key={API_KEY}",
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

        # Remover áudio — Snayder: vídeo mudo, narração vem do Suno/mix
        print(f"  Removendo áudio via ffmpeg...", flush=True)
        strip_audio(out_path)

        size_mb = out_path.stat().st_size / 1024 / 1024
        print(f"  [OK] {out_path.name} ({size_mb:.1f} MB, sem áudio)", flush=True)
        total_cost += cost_for_parte(c["parte"])
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
