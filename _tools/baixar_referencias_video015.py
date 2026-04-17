"""
Baixa capas da Economist (2021-2026) + fotos das pessoas do video-015.
Usa múltiplas fontes com fallback.

Uso:
  python _tools/baixar_referencias_video015.py
"""
import urllib.request
import time
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT  = BASE / "canais/sinais-do-fim/videos/video-015-economist-manipulacao/6-assets/referencias"
OUT_CAPAS   = OUT / "capas"
OUT_PESSOAS = OUT / "pessoas"
OUT_CAPAS.mkdir(parents=True, exist_ok=True)
OUT_PESSOAS.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Referer": "https://www.google.com/",
}

SOURCES = {
    # ── CAPAS THE ECONOMIST ──────────────────────────────────────────
    "capas/economist_2021.jpg": [
        "https://golden-mart.com/wp-content/uploads/2025/12/economist-2021-cover.jpg",
        "https://magazine.digitalslrphoto.com/wp-content/uploads/economist-2021.jpg",
        "https://images.squarespace-cdn.com/content/economist-world-ahead-2021.jpg",
    ],
    "capas/economist_2022.jpg": [
        "https://golden-mart.com/wp-content/uploads/2025/12/economist-2022-cover.jpg",
        "https://cdn.vocal.media/economist-2022-world-ahead.jpg",
    ],
    "capas/economist_2023.jpg": [
        "https://golden-mart.com/wp-content/uploads/2025/12/economist-2023-cover.jpg",
        "https://images.squarespace-cdn.com/content/economist-world-ahead-2023.jpg",
    ],
    "capas/economist_2024.jpg": [
        "https://golden-mart.com/wp-content/uploads/2025/12/economist-2024-cover.jpg",
        "https://andreabelvedere.medium.com/economist-2024-cover.jpg",
    ],
    "capas/economist_2025.jpg": [
        "https://golden-mart.com/wp-content/uploads/2025/12/economist-2025-cover.jpg",
        "https://miro.medium.com/v2/resize:fit:1400/economist-2025.jpg",
    ],
    "capas/economist_2026.jpg": [
        "https://golden-mart.com/wp-content/uploads/2025/12/economist-2026-cover.jpg",
        "https://miro.medium.com/v2/resize:fit:1400/format:webp/1*economist-world-ahead-2026.jpg",
        "https://tagstrading.com/wp-content/uploads/economist-2026.jpg",
    ],

    # ── FOTOS PESSOAS ────────────────────────────────────────────────
    "pessoas/maria_ressa.jpg": [
        # JÁ BAIXADO — este é fallback
        "https://www.nobelprize.org/uploads/2021/10/ressa_photo-980x1386.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9d/Maria_Ressa_%28cropped%29.jpg",
    ],
    "pessoas/lynn_rothschild.jpg": [
        "https://www.weforum.org/wp-content/uploads/2023/01/lynn-forester-de-rothschild.jpg",
        "https://live.worldbank.org/sites/default/files/people/lynn-forester-de-rothschild.jpg",
        "https://www.inclusivecapitalism.com/wp-content/uploads/lynn-rothschild.jpg",
    ],
    "pessoas/stephen_smith.jpg": [
        "https://www.theglobeandmail.com/resizer/stephen-smith-economist.jpg",
        "https://static.ffnimg.com/photos/stephen-smith-first-national.jpg",
        "https://smith.queensu.ca/about/advisory_board/img/Stephen_Smith.jpg",
    ],
    "pessoas/tom_standage.jpg": [
        "https://www.niemanlab.org/wp-content/uploads/tom-standage-economist.jpg",
        "https://media.licdn.com/dms/image/tom-standage-linkedin.jpg",
    ],
    "pessoas/zanny_beddoes.jpg": [
        "https://www.alamy.com/stock-image-zanny-minton-beddoes-165323004.jpg",
        "https://pbs.twimg.com/profile_images/zannymb_400x400.jpg",
    ],
    "pessoas/zanny_bilderberg.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Zanny_Minton_Beddoes_%282014%29.jpg/440px-Zanny_Minton_Beddoes_%282014%29.jpg",
    ],
}


def try_download(dest: Path, urls: list) -> bool:
    if dest.exists() and dest.stat().st_size > 20000:
        print(f"  SKIP (já existe) {dest.name} ({dest.stat().st_size//1024}KB)")
        return True

    for url in urls:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as r:
                data = r.read()
            if len(data) < 10000:
                continue  # provavelmente HTML de erro
            dest.write_bytes(data)
            print(f"  OK  {dest.name} ({len(data)//1024}KB) ← {url[:60]}...")
            return True
        except Exception as e:
            pass  # tenta próxima URL
        time.sleep(0.5)

    print(f"  FAIL {dest.name} — nenhuma fonte funcionou")
    return False


def main():
    print("Baixando referências video-015...\n")
    ok, fail = 0, 0

    for rel_path, urls in SOURCES.items():
        dest = OUT / rel_path
        if try_download(dest, urls):
            ok += 1
        else:
            fail += 1
        time.sleep(0.8)

    print(f"\nResultado: {ok} OK | {fail} falhas")

    # Gera manifesto com o que faltou
    if fail > 0:
        manifest = OUT / "DOWNLOAD_MANUAL.md"
        lines = ["# Imagens para baixar manualmente\n\n"]
        for rel_path, urls in SOURCES.items():
            dest = OUT / rel_path
            if not dest.exists() or dest.stat().st_size < 10000:
                lines.append(f"## {rel_path}\n")
                for u in urls:
                    lines.append(f"- {u}\n")
                lines.append(f"\nSalvar em: `{dest}`\n\n")
        manifest.write_text("".join(lines), encoding="utf-8")
        print(f"\nManifesto gerado: {manifest}")

    print(f"\nAssets em: {OUT}")


if __name__ == "__main__":
    main()
