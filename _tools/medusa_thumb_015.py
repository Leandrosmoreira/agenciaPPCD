"""
Medusa — Gerador de Thumbnails via Gemini Image API
video-015-economist-manipulacao | 3 variações | 1280x720 (16:9)
"""
import base64, json, os, sys, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent

def load_env(path):
    if not path.exists(): return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

load_env(ROOT / ".env")
API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL   = "gemini-2.5-flash-image"
URL     = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

OUT_DIR = ROOT / "canais/sinais-do-fim/videos/video-015-economist-manipulacao/8-publicacao"
OUT_DIR.mkdir(parents=True, exist_ok=True)

THUMBS = [
    {
        "id": "THUMB_A",
        "text_overlay": "ELES PLANEJARAM TUDO",
        "prompt": (
            "Close-up photo of a shocked desperate middle-aged man holding The Economist magazine "
            "with illuminati symbols on the cover, his face occupying left 45% of frame with expression "
            "of terror and disbelief, deep shadows on face, dramatic chiaroscuro lighting from above, "
            "dark crimson and black background, golden light illuminating the magazine, fire embers "
            "floating in air, 35mm film grain, photorealistic, cinematic YouTube thumbnail composition, "
            "empty dark space on right side for text overlay, 1280x720 pixels, 16:9 aspect ratio"
        ),
    },
    {
        "id": "THUMB_B",
        "text_overlay": "QUEM CONTROLA O MUNDO",
        "prompt": (
            "Dark dramatic image of a human puppet silhouette of a world leader being controlled by "
            "a shadowy hand emerging from the top with glowing golden strings, The Economist magazine "
            "logo barely visible in background, deep black background with crimson glow from below, "
            "golden threads glowing like fire, chiaroscuro dramatic lighting, floating ash embers, "
            "ornate decorative borders, aged parchment texture overlay, 35mm film grain, apocalyptic "
            "surreal atmosphere, YouTube thumbnail 16:9 1280x720, empty space on left for text overlay"
        ),
    },
    {
        "id": "THUMB_C",
        "text_overlay": "PROIBIRAM ESSA CAPA",
        "prompt": (
            "The Economist magazine cover burning with a glowing illuminati all-seeing eye pyramid "
            "visible through the flames, a shadowy hand reaching in to hide or tear the magazine, "
            "deep black background, intense crimson and gold fire, dramatic shadows, floating ash embers, "
            "anamorphic lens flares, chiaroscuro lighting, 35mm film grain, photorealistic, apocalyptic "
            "atmosphere, YouTube thumbnail 16:9 1280x720 pixels, empty dark space on left side for text"
        ),
    },
]

PRICE_USD = 0.039

def generate(thumb: dict) -> Path | None:
    print(f"\n[{thumb['id']}] Gerando: {thumb['text_overlay']}")
    payload = {
        "contents": [{"parts": [{"text": thumb["prompt"]}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]},
    }
    resp = requests.post(URL, json=payload, timeout=120)
    if resp.status_code != 200:
        print(f"  [ERRO {resp.status_code}] {resp.text[:400]}")
        return None

    data = resp.json()
    try:
        parts = data["candidates"][0]["content"]["parts"]
        for part in parts:
            if "inlineData" in part:
                img_b64 = part["inlineData"]["data"]
                out = OUT_DIR / f"{thumb['id']}.png"
                out.write_bytes(base64.b64decode(img_b64))
                sz = out.stat().st_size / 1024
                print(f"  [OK] {out.name} ({sz:.0f} KB) | ~${PRICE_USD:.3f}")
                return out
        print(f"  [ERRO] Sem inlineData na resposta")
    except (KeyError, IndexError) as e:
        print(f"  [ERRO] Parse: {e}\n  {json.dumps(data)[:300]}")
    return None

def main():
    if not API_KEY:
        print("[ERRO] GEMINI_API_KEY não encontrada em .env")
        sys.exit(1)

    print("=" * 55)
    print("MEDUSA — Thumbnails video-015-economist")
    print(f"Output: {OUT_DIR}")
    print("=" * 55)

    ok = 0
    for thumb in THUMBS:
        result = generate(thumb)
        if result: ok += 1
        time.sleep(2)

    print(f"\n[CONCLUÍDO] {ok}/{len(THUMBS)} thumbnails gerados")
    print(f"[CUSTO EST.] ~${ok * PRICE_USD:.3f} USD")
    print(f"[LOCAL] {OUT_DIR}")

if __name__ == "__main__":
    main()
