"""
Goetia Nano Banana — gerador de imagens via Gemini 2.5 Flash Image (Nano Banana)
Usa REST API direto (evita google-genai que trava no import no Windows).

Uso:
  python _tools/goetia_nano_banana.py --canal sinais-do-fim --video video-015-economist-manipulacao --quadro Q01
  python _tools/goetia_nano_banana.py --canal sinais-do-fim --video video-015-economist-manipulacao --all
  python _tools/goetia_nano_banana.py --canal sinais-do-fim --video video-015-economist-manipulacao --quadro Q01 --dry-run
"""
import argparse
import base64
import io
import json
import os
import sys
import time
from pathlib import Path

import requests

try:
    from PIL import Image
    import numpy as np
    HAS_PIL = True
except Exception:
    HAS_PIL = False

ROOT = Path(__file__).resolve().parent.parent


def load_env(path: Path):
    """Carrega .env simples sem dotenv."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


load_env(ROOT / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

# Flash (padrao) e Pro (para quadros com texto critico / api_call_hints.model_override=pro)
MODEL_FLASH = os.getenv("NANO_BANANA_FLASH_MODEL", "gemini-2.5-flash-image")
MODEL_PRO = os.getenv("NANO_BANANA_PRO_MODEL", "gemini-3-pro-image-preview")

ENDPOINT_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# Precos oficiais Google (USD por imagem)
PRICE_FLASH_USD = 0.039   # Nano Banana Flash: 1290 tokens * $30/1M
PRICE_PRO_USD = 0.120     # Nano Banana Pro (estimativa conservadora)

COST_LOG = ROOT / "_tools" / "nano_banana_costs.log"

# Auto-crop: linhas com media de luminancia acima deste valor = letterbox branco
CROP_WHITE_THRESHOLD = 240

# Dimensoes alvo 16:9 (saida final de todos os quadros)
TARGET_W = 1024
TARGET_H = 576  # 1024 * 9 / 16 = 576


def _shot_to_verb(shot_type: str) -> str:
    """Converte tipo de shot em verbo forte Nano Banana."""
    st = (shot_type or "").lower()
    if "extreme close" in st:
        return "Render a photorealistic extreme close-up of"
    if "close" in st:
        return "Capture a cinematic close-up of"
    if "medium wide" in st or "medium-wide" in st:
        return "Compose a medium-wide cinematic shot of"
    if "medium" in st:
        return "Frame a photorealistic medium shot of"
    if "extreme wide" in st or "extra wide" in st:
        return "Render an epic extreme-wide establishing shot of"
    if "wide" in st:
        return "Render a wide cinematic establishing shot of"
    if "overhead" in st or "top-down" in st:
        return "Capture a top-down overhead shot of"
    return "Render a photorealistic cinematic image of"


def _negative_to_positive(neg_items: list) -> list:
    """Converte 'no X' em frases positivas descrevendo ausencia.
    Nano Banana NAO tem --no. Frases negativas podem gerar o oposto.
    """
    conversions = {
        "no people": "completely empty of human figures, deserted scene",
        "no visible faces": "faces hidden in shadow or turned away",
        "no person": "empty composition without human presence",
        "no text": "clean surface without any visible text",
        "no watermark": "clean photograph without watermarks or logos",
        "no watermarks": "clean photograph without watermarks",
        "no logo": "unmarked surface",
        "no cartoon": "photorealistic documentary photography",
        "no anime": "photorealistic live-action cinematography",
        "no illustration": "photographic realism, not illustrated",
        "no digital art": "analog film photography aesthetic",
        "no modern tech": "19th century period setting only",
        "no modern objects": "antique period-accurate setting only",
        "no modern currency design": "vintage period-accurate currency textures",
        "no modern watch design": "antique analog timepiece only",
        "no digital clock": "classical analog clock with Roman numerals only",
        "no bright daylight": "low-light chiaroscuro atmosphere",
        "no daylight": "night or interior low-light scene",
        "no bright light": "dim moody lighting, deep shadows",
        "no daylight outdoor": "interior or night exterior only",
        "no saturated modern colors": "muted desaturated period palette",
        "no neon colors": "warm analog color palette only",
        "no blurry": "tack-sharp focus on focal point",
        "no low quality": "high-resolution photographic detail",
        "no oversaturated": "naturalistic color grading",
    }

    out = []
    for item in neg_items:
        key = item.strip().lower()
        if key in conversions:
            out.append(conversions[key])
        elif key.startswith("no "):
            # Fallback generico
            subject = key[3:]
            out.append(f"scene without {subject}, composition avoiding {subject}")
        else:
            # Ja eh positivo ou forma nao reconhecida
            out.append(item)
    return out


def _format_in_scene_text(ist: dict) -> str:
    """Aplica regra Text-First: aspas literais + fonte descrita."""
    if not ist or not ist.get("enabled"):
        return ""
    content = ist.get("content") or ist.get("content_primary") or ""
    content2 = ist.get("content_secondary", "")
    font = ist.get("font_style", "")
    medium = ist.get("medium", "")
    placement = ist.get("placement", "")

    pieces = []
    if content:
        pieces.append(f'displaying the exact text "{content}"')
    if content2:
        pieces.append(f'with secondary text "{content2}"')
    if font:
        pieces.append(f"rendered in {font}")
    if medium:
        pieces.append(f"as {medium}")
    if placement:
        pieces.append(f"positioned {placement}")
    pieces.append("with crisp legible typography")

    return ", ".join(pieces)


def serialize_json_to_prompt(d: dict) -> str:
    """Serializa JSON seguindo formula Nano Banana:
    [Verbo] + [Sujeito] + [Acao] + [Local] + [Composicao] + [Estilo]
    Com enquadramento positivo e text-first.
    """
    sections = []

    # === LINHA 1: Verbo + Sujeito + Text-first ===
    shot = d.get("shot", {})
    sub = d.get("subject", {})
    verb = _shot_to_verb(shot.get("type", ""))

    subject_line = f"{verb} {sub.get('primary','the scene')}"
    if sub.get("focal_point"):
        subject_line += f", with focal point on {sub['focal_point']}"

    # Text-first: se houver texto na cena, integrar AQUI no sujeito
    ist = d.get("in_scene_text", {})
    ist_phrase = _format_in_scene_text(ist)
    if ist_phrase:
        subject_line += f", {ist_phrase}"

    sections.append(subject_line)

    # === LINHA 2: Ação/contexto do sujeito (secondary + props) ===
    action_bits = []
    if sub.get("secondary"):
        action_bits.append(sub["secondary"])
    if sub.get("props"):
        action_bits.append("surrounded by " + ", ".join(sub["props"]))
    if action_bits:
        sections.append(". ".join(action_bits) + ".")

    # === LINHA 3: Local/Ambiente ===
    env = d.get("environment", {})
    env_bits = []
    if env.get("location"):
        env_bits.append(f"Set in {env['location']}")
    if env.get("time_of_day"):
        env_bits.append(f"during {env['time_of_day']}")
    if env.get("atmosphere"):
        env_bits.append(f"with {env['atmosphere']} atmosphere")
    if env_bits:
        sections.append(", ".join(env_bits) + ".")

    # === LINHA 4: Composição + aspect ratio ===
    comp = d.get("composition", {})
    comp_bits = []
    if shot.get("type"):
        comp_bits.append(shot["type"])
    if shot.get("camera_angle"):
        comp_bits.append(shot["camera_angle"])
    if shot.get("focal_length_mm"):
        comp_bits.append(f"{shot['focal_length_mm']}mm lens")
    if shot.get("aperture"):
        comp_bits.append(f"aperture {shot['aperture']}")
    if shot.get("depth_of_field"):
        comp_bits.append(f"{shot['depth_of_field']} depth of field")
    ar = shot.get("aspect_ratio", "16:9")
    comp_bits.append(f"{ar} widescreen cinematic framing")
    if comp.get("rule"):
        comp_bits.append(comp["rule"])
    if comp_bits:
        sections.append("Composition: " + ", ".join(comp_bits) + ".")

    # Foreground/midground/background (materialidade)
    fg_mg_bg = []
    if comp.get("foreground"):
        fg_mg_bg.append(f"foreground: {comp['foreground']}")
    if comp.get("midground"):
        fg_mg_bg.append(f"midground: {comp['midground']}")
    if comp.get("background"):
        fg_mg_bg.append(f"background: {comp['background']}")
    if fg_mg_bg:
        sections.append("; ".join(fg_mg_bg) + ".")

    # === LINHA 5: Iluminação ===
    light = d.get("lighting", {})
    light_bits = []
    if light.get("key_light"):
        light_bits.append(f"key light: {light['key_light']}")
    if light.get("fill_light"):
        light_bits.append(f"fill: {light['fill_light']}")
    if light.get("rim_light"):
        light_bits.append(f"rim: {light['rim_light']}")
    if light.get("shadow_quality"):
        light_bits.append(f"shadows: {light['shadow_quality']}")
    if light.get("mood"):
        light_bits.append(f"lighting mood: {light['mood']}")
    if light_bits:
        sections.append("Lighting — " + "; ".join(light_bits) + ".")

    # === LINHA 6: Estilo (film stock + post + style_reference description) ===
    style = d.get("style", {})
    style_bits = []
    if style.get("film_stock"):
        style_bits.append(f"shot on {style['film_stock']}")
    if style.get("post_processing"):
        style_bits.append(f"post-processing: {style['post_processing']}")
    if style.get("texture_detail"):
        style_bits.append(f"textures: {style['texture_detail']}")

    sr = d.get("style_reference", {})
    if sr.get("textual_description"):
        style_bits.append(sr["textual_description"])

    if style_bits:
        sections.append("Style — " + ". ".join(style_bits) + ".")

    # === LINHA 7: Mood + Symbolism ===
    mood = d.get("mood", {})
    if mood.get("emotion"):
        mood_line = f"Emotional tone: {mood['emotion']}"
        if mood.get("tension"):
            mood_line += f", tension level {mood['tension']}"
        sections.append(mood_line + ".")

    sym = d.get("symbolism", {})
    if sym.get("primary"):
        sections.append(f"Symbolic intent: {sym['primary']}.")

    # === LINHA 8: Enquadramento positivo (ex-negative prompt) ===
    # Suporta tanto `negative_prompt` (legado) quanto `negative_as_positive` (novo)
    neg_items = d.get("negative_as_positive") or d.get("negative_prompt") or []
    if neg_items:
        positive_constraints = _negative_to_positive(neg_items)
        sections.append("Scene constraints: " + "; ".join(positive_constraints) + ".")

    # === LINHA 9: Critical note ===
    hints = d.get("api_call_hints", {})
    if hints.get("critical_note_for_gemini"):
        sections.append(f"CRITICAL REQUIREMENT: {hints['critical_note_for_gemini']}")

    return "\n\n".join(sections)


def force_16x9(img_bytes: bytes, threshold: int = CROP_WHITE_THRESHOLD) -> tuple:
    """Pipeline de normalizacao 16:9 em duas etapas:

    1. Remove letterbox branco no topo/base (se existir)
    2. Crop central para TARGET_W x TARGET_H (1024x576 = 16:9 exato)

    Retorna (novos_bytes, (w, h), descricao_operacao).
    """
    if not HAS_PIL:
        return img_bytes, (0, 0), "PIL indisponivel"

    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        arr = np.array(img)
        orig_w, orig_h = img.size

        # --- PASSO 1: remover letterbox branco ---
        row_lum = arr.mean(axis=(1, 2))
        top = 0
        for i in range(orig_h):
            if row_lum[i] < threshold:
                top = i
                break
        bottom = orig_h
        for i in range(orig_h - 1, -1, -1):
            if row_lum[i] < threshold:
                bottom = i + 1
                break
        cropped_px = top + (orig_h - bottom)
        if cropped_px >= 16:
            img = img.crop((0, top, orig_w, bottom))
            op = f"letterbox removido ({cropped_px}px)"
        else:
            op = "sem letterbox"

        # --- PASSO 2: crop central para 1024x576 ---
        w, h = img.size
        # Se menor que alvo, usa Lanczos para escalar (fallback raro)
        if w < TARGET_W or h < TARGET_H:
            scale = max(TARGET_W / w, TARGET_H / h)
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
            w, h = img.size
            op += f" | escalado para {w}x{h}"

        left = (w - TARGET_W) // 2
        top2 = (h - TARGET_H) // 2
        img = img.crop((left, top2, left + TARGET_W, top2 + TARGET_H))
        op += f" | crop central {TARGET_W}x{TARGET_H}"

        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        return buf.getvalue(), img.size, op

    except Exception as e:
        print(f"[WARN] force_16x9 falhou: {e}", flush=True)
        return img_bytes, (0, 0), f"ERRO: {e}"


def download_style_ref(url: str):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.content
    except Exception as e:
        print(f"[WARN] Falha ao baixar style_reference: {e}", flush=True)
        return None


def call_gemini(prompt_text: str, sref_bytes, out_path: Path, model: str, do_crop: bool = True) -> bool:
    parts = []
    if sref_bytes:
        parts.append({
            "inline_data": {
                "mime_type": "image/png",
                "data": base64.b64encode(sref_bytes).decode("ascii"),
            }
        })
    parts.append({"text": prompt_text})

    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    }

    endpoint = ENDPOINT_TEMPLATE.format(model=model)

    try:
        r = requests.post(endpoint, headers=headers, json=body, timeout=180)
    except Exception as e:
        print(f"[ERRO] Request falhou: {e}", flush=True)
        return False

    if r.status_code != 200:
        print(f"[ERRO] HTTP {r.status_code} ({model}): {r.text[:500]}", flush=True)
        # Fallback automatico: se Pro nao estiver disponivel, tenta Flash
        if model != MODEL_FLASH and r.status_code in (400, 404):
            print(f"[FALLBACK] Tentando {MODEL_FLASH}...", flush=True)
            return call_gemini(prompt_text, sref_bytes, out_path, MODEL_FLASH, do_crop)
        return False

    data = r.json()
    saved = False
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inline_data") or part.get("inlineData")
            if inline and inline.get("data"):
                img_bytes = base64.b64decode(inline["data"])
                orig_size = len(img_bytes)

                if do_crop:
                    img_bytes, (w, h), op = force_16x9(img_bytes)
                    print(f"[16:9] {op} -> {w}x{h}", flush=True)

                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(img_bytes)
                print(f"[OK] Salvo: {out_path} ({len(img_bytes)} bytes, modelo {model})", flush=True)
                saved = True
                break
            elif part.get("text"):
                print(f"[TEXTO] {part['text'][:200]}", flush=True)
        if saved:
            break

    if not saved:
        print("[ERRO] Nenhuma imagem retornada", flush=True)
        print(f"Resposta bruta: {json.dumps(data)[:500]}", flush=True)
    return saved


def log_cost(canal: str, video: str, quadro: str, model: str, price: float, ok: bool):
    COST_LOG.parent.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    status = "OK" if ok else "FAIL"
    line = f"{ts} | {canal} | {video} | {quadro} | {model} | ${price:.4f} | {status}\n"
    with COST_LOG.open("a", encoding="utf-8") as f:
        f.write(line)


def pick_model(data: dict) -> tuple:
    """Seleciona modelo baseado em api_call_hints.model_override. Retorna (model_id, price)."""
    hints = data.get("api_call_hints", {}) or {}
    override = (hints.get("model_override") or "").lower().strip()
    if override in ("pro", "nano-banana-pro", "gemini-pro-image"):
        return MODEL_PRO, PRICE_PRO_USD
    return MODEL_FLASH, PRICE_FLASH_USD


def process_quadro(canal: str, video: str, quadro: str, dry_run: bool, force_flash: bool = False) -> tuple:
    """Retorna (ok, model, price)."""
    video_dir = ROOT / "canais" / canal / "videos" / video
    json_path = video_dir / "6-prompts-imagem" / f"{quadro}.json"
    if not json_path.exists():
        print(f"[ERRO] JSON nao encontrado: {json_path}", flush=True)
        return False, MODEL_FLASH, 0.0

    data = json.loads(json_path.read_text(encoding="utf-8"))
    prompt = serialize_json_to_prompt(data)

    model, price = (MODEL_FLASH, PRICE_FLASH_USD) if force_flash else pick_model(data)

    print(f"\n=== {quadro} — {data.get('scene_title','')} ===", flush=True)
    print(f"Modelo: {model} (${price:.4f}) | Prompt chars: {len(prompt)}", flush=True)

    if dry_run:
        print("--- PROMPT ---", flush=True)
        print(prompt, flush=True)
        print("--- END ---", flush=True)
        return True, model, 0.0

    sref_url = data.get("style_reference", {}).get("primary_image_url")
    sref_bytes = download_style_ref(sref_url) if sref_url else None
    if sref_bytes:
        print(f"[OK] style_reference baixado ({len(sref_bytes)} bytes)", flush=True)

    out_path = video_dir / "6-assets" / f"{quadro}.png"
    ok = call_gemini(prompt, sref_bytes, out_path, model=model, do_crop=True)
    log_cost(canal, video, quadro, model, price, ok)
    return ok, model, price


def crop_existing_assets(canal: str, video: str, quadros: list) -> None:
    """Aplica force_16x9 em PNGs ja geradas, sem chamar API."""
    video_dir = ROOT / "canais" / canal / "videos" / video
    assets_dir = video_dir / "6-assets"
    total_ok = 0
    for q in quadros:
        png = assets_dir / f"{q}.png"
        if not png.exists():
            print(f"[SKIP] {q}.png nao existe", flush=True)
            continue
        orig = png.read_bytes()
        new_bytes, (w, h), op = force_16x9(orig)
        png.write_bytes(new_bytes)
        print(f"[16:9] {q}.png: {op} -> {w}x{h}", flush=True)
        total_ok += 1
    print(f"\nTotal processadas: {total_ok}/{len(quadros)}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--canal", required=True)
    ap.add_argument("--video", required=True)
    ap.add_argument("--quadro", help="Ex: Q01")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--range", help="Intervalo de quadros, ex: Q02-Q06")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force-flash", action="store_true", help="Ignora model_override=pro e usa Flash")
    ap.add_argument("--crop-existing", action="store_true", help="So aplica auto-crop em PNGs ja geradas, sem API")
    ap.add_argument("--skip-existing", action="store_true", help="Pula quadros cuja PNG ja existe em 6-assets/")
    args = ap.parse_args()

    if not (args.quadro or args.all or args.range):
        print("[ERRO] informe --quadro QXX, --range Q02-Q06 ou --all", flush=True)
        sys.exit(1)

    video_dir = ROOT / "canais" / args.canal / "videos" / args.video
    prompts_dir = video_dir / "6-prompts-imagem"

    # Resolve lista de quadros
    if args.all:
        quadros = sorted(p.stem for p in prompts_dir.glob("Q*.json"))
    elif args.range:
        try:
            start, end = args.range.split("-")
            start_n = int(start.lstrip("Q"))
            end_n = int(end.lstrip("Q"))
            quadros = [f"Q{n:02d}" for n in range(start_n, end_n + 1)]
        except Exception as e:
            print(f"[ERRO] --range invalido ({e}). Formato esperado: Q02-Q06", flush=True)
            sys.exit(1)
    else:
        quadros = [args.quadro]

    # Modo crop-only (nao chama API)
    if args.crop_existing:
        if not HAS_PIL:
            print("[ERRO] PIL/numpy nao disponiveis. pip install pillow numpy", flush=True)
            sys.exit(1)
        crop_existing_assets(args.canal, args.video, quadros)
        return

    if not API_KEY and not args.dry_run:
        print("[ERRO] GEMINI_API_KEY ausente no .env", flush=True)
        sys.exit(1)

    if not HAS_PIL:
        print("[WARN] PIL/numpy ausentes — auto-crop 16:9 desabilitado", flush=True)

    total_cost = 0.0
    ok_count = 0
    assets_dir = video_dir / "6-assets"
    by_model = {MODEL_FLASH: 0, MODEL_PRO: 0}

    for q in quadros:
        if args.skip_existing and (assets_dir / f"{q}.png").exists():
            print(f"[SKIP] {q}.png ja existe", flush=True)
            continue
        ok, model, price = process_quadro(args.canal, args.video, q, args.dry_run, force_flash=args.force_flash)
        if ok and not args.dry_run:
            ok_count += 1
            total_cost += price
            by_model[model] = by_model.get(model, 0) + 1

    print(f"\n=== RESUMO ===", flush=True)
    print(f"Sucesso: {ok_count}/{len(quadros)}", flush=True)
    if not args.dry_run:
        print(f"  Flash: {by_model.get(MODEL_FLASH, 0)} x ${PRICE_FLASH_USD:.3f}", flush=True)
        print(f"  Pro:   {by_model.get(MODEL_PRO, 0)} x ${PRICE_PRO_USD:.3f}", flush=True)
        print(f"Custo total: ${total_cost:.4f}", flush=True)


if __name__ == "__main__":
    main()
