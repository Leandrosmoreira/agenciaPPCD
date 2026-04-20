#!/usr/bin/env python3
"""
veo3_oneshot.py — Gera UM clip Veo3 a partir de qualquer imagem local.

Uso:
  python _tools/veo3_oneshot.py --image caminho/para/imagem.png --out saida.mp4

Exemplo:
  python _tools/veo3_oneshot.py --image _tools/mascots.png --out _tools/mascots_5s.mp4

Modelo: veo-3.1-fast-generate-preview | 5s | 1080p | 16:9 | sem audio
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

API_KEY   = os.getenv("GEMINI_API_KEY", "")
MODEL     = "veo-3.1-fast-generate-preview"
BASE_URL  = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predictLongRunning"

PROMPT = (
    "Hyper-realistic 3D animation. Slow motion camera zooming out. "
    "In the foreground, three mascots (a moose in red outfit, a jaguar in green outfit, "
    "and an eagle in blue outfit) are jumping joyfully with raised arms and spread wings. "
    "In the midground, the FIFA World Cup 2026 logo with stylized trophy and country flags. "
    "In the background, a massive nuclear explosion with a glowing orange-yellow-white "
    "mushroom cloud and dark smoky sky, visible shockwaves radiating outward. "
    "Dramatic shadows and warm orange light from the explosion reflecting on the characters, "
    "contrasting their joy with the apocalyptic background. "
    "Cinematic depth of field, no dialogue, no text overlay, no watermark."
)


def strip_audio(mp4_path: Path) -> None:
    tmp = mp4_path.with_suffix(".noaudio.mp4")
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", str(mp4_path), "-c:v", "copy", "-an", str(tmp)],
        capture_output=True, text=True
    )
    if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
        mp4_path.unlink()
        tmp.rename(mp4_path)
    else:
        print(f"  [WARN] strip_audio falhou: {r.stderr[:200]}")
        if tmp.exists():
            tmp.unlink()


def poll_operation(op_name: str, max_wait_s: int = 600) -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/{op_name}?key={API_KEY}"
    elapsed = 0
    while elapsed < max_wait_s:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if data.get("done"):
            return data
        print(f"  Aguardando... {elapsed + 10}s", flush=True)
        time.sleep(10)
        elapsed += 10
    raise TimeoutError(f"Timeout em {max_wait_s}s")


def extract_video_uri(result: dict) -> str:
    try:
        r = result.get("response", {})
        return r["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
    except (KeyError, IndexError, TypeError):
        pass
    try:
        r = result.get("response", {})
        return r["generatedSamples"][0]["video"]["uri"]
    except (KeyError, IndexError, TypeError):
        pass
    raise ValueError(f"URI nao encontrada:\n{json.dumps(result, indent=2)[:800]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True, help="Caminho da imagem de entrada (PNG/JPG)")
    ap.add_argument("--out",   default="_tools/mascots_5s.mp4", help="Arquivo de saida MP4")
    ap.add_argument("--dur",   type=int, default=5, help="Duracao em segundos (5 ou 8)")
    ap.add_argument("--prompt", default=None, help="Prompt customizado (opcional)")
    args = ap.parse_args()

    if not API_KEY:
        print("[ERRO] GEMINI_API_KEY nao encontrada em .env")
        sys.exit(1)

    img_path = Path(args.image)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not img_path.exists():
        print(f"[ERRO] Imagem nao encontrada: {img_path}")
        sys.exit(1)

    prompt = args.prompt or PROMPT

    # Detectar mime type
    suffix = img_path.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg"

    print(f"\nVEO3 ONE-SHOT")
    print(f"  Imagem : {img_path} ({img_path.stat().st_size/1024:.0f} KB)")
    print(f"  Output : {out_path}")
    print(f"  Model  : {MODEL}")
    print(f"  Duracao: {args.dur}s | 1080p | 16:9 | sem audio")
    print(f"  Prompt : {prompt[:120]}...")
    print()

    # 1. Encode base64
    img_data = base64.b64encode(img_path.read_bytes()).decode("utf-8")

    # 2. Payload
    payload = {
        "instances": [{
            "prompt": prompt,
            "image": {
                "bytesBase64Encoded": img_data,
                "mimeType": mime
            }
        }],
        "parameters": {
            "resolution":      "1080p",
            "durationSeconds": args.dur,
            "aspectRatio":     "16:9",
        }
    }

    # 3. Chamar API
    print("Chamando Veo3 API...", flush=True)
    resp = requests.post(f"{BASE_URL}?key={API_KEY}", json=payload, timeout=60)
    if resp.status_code != 200:
        print(f"[ERRO HTTP {resp.status_code}]\n{resp.text[:600]}")
        sys.exit(1)

    op_name = resp.json().get("name", "")
    if not op_name:
        print(f"[ERRO] Sem operation name: {resp.text[:400]}")
        sys.exit(1)

    print(f"Operation: {op_name}", flush=True)

    # 4. Polling
    print("Aguardando geracao (2-5 min)...", flush=True)
    result = poll_operation(op_name)

    # 5. Extrair URI e baixar
    video_uri = extract_video_uri(result)
    print(f"  URI: {video_uri[:80]}...", flush=True)

    if video_uri.startswith("gs://"):
        dl_url = video_uri.replace("gs://", "https://storage.googleapis.com/")
    else:
        dl_url = f"{video_uri}&key={API_KEY}" if "?" not in video_uri else f"{video_uri}&key={API_KEY}"

    print(f"  Baixando...", flush=True)
    dl_resp = requests.get(dl_url, timeout=120, stream=True)
    dl_resp.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in dl_resp.iter_content(chunk_size=8192):
            f.write(chunk)

    # 6. Remove audio
    print("  Removendo audio...", flush=True)
    strip_audio(out_path)

    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"\n[OK] {out_path} ({size_mb:.1f} MB)")
    print(f"[CUSTO ESTIMADO] ~$0.08 (5s Fast)")


if __name__ == "__main__":
    main()
