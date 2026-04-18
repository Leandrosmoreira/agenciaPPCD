"""
PHANTASMA — Editor Cinematográfico
video-017 "SKYNET é CLAUDE AI? O que Apocalipse 13 avisou em 95 d.C."
Canal: Sinais do Fim — Passagens do Apocalipse
Tema: IA/tecnologia — grade fria com tom azul tecnológico (grade_tech)
Gerado por: Phantasma — Abismo Criativo
"""

import gc, os, sys, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from moviepy.editor import VideoClip, concatenate_videoclips

ROOT   = Path(__file__).resolve().parent.parent
CANAL  = ROOT / "canais/sinais-do-fim"
VIDEO  = CANAL / "videos/video-017-claude-skynet"
ASSETS = VIDEO / "6-assets"
AUDIO  = VIDEO / "5-audio"
OUT    = VIDEO / "7-edicao"
OUT.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1920, 1080, 30

# Storyboard: 5 partes — distribuição irregular (2+10+12+13+13+8 = 60 quadros, 5 batches)
# Batch 1: Q01-Q12 (gancho + julgamento automático)
# Batch 2: Q13-Q24 (a máquina que já existe)
# Batch 3: Q25-Q37 (o que João viu em Patmos)
# Batch 4: Q38-Q50 (o nome que você usa todo dia)
# Batch 5: Q51-Q60 (o que fazer com isso)
PARTE_DUR = {1: 150.0, 2: 150.0, 3: 150.0, 4: 150.0, 5: 150.0}
PARTES_AUDIO = [AUDIO / f"parte{n}.mp3" for n in range(1, 6)]
TRILHA = AUDIO / "trilha.MP3"

WRITE_OPTS = dict(
    codec="libx264", audio=False,
    fps=FPS, preset="ultrafast",
    threads=1, bitrate="5000k",
    ffmpeg_params=["-refs", "1", "-bf", "0"]
)

# Títulos reais dos blocos extraídos do storyboard
TITULOS_PARTES = {
    1: "GANCHO: O ALGORITMO DA MORTE",
    2: "A MÁQUINA QUE JÁ EXISTE",
    3: "O QUE JOÃO VIU EM PATMOS",
    4: "O NOME QUE VOCÊ USA TODO DIA",
    5: "O QUE FAZER COM ISSO",
}


def ken_burns(img_path, duration, effect="zoom_in", fps=30):
    _cache = [None]

    def make_frame(t):
        if _cache[0] is None:
            _cache[0] = np.array(
                Image.open(img_path).convert("RGB").resize((W, H), Image.LANCZOS)
            ).astype(np.float32)
        f = _cache[0].copy()
        progress = t / max(duration, 0.001)
        if effect == "zoom_in":
            scale = 1.0 + 0.08 * progress
        elif effect == "zoom_out":
            scale = 1.08 - 0.08 * progress
        else:
            scale = 1.04
        if scale != 1.0:
            nw, nh = int(W * scale), int(H * scale)
            img_big = cv2.resize(_cache[0].astype(np.uint8), (nw, nh))
            ox = (nw - W) // 2
            oy = (nh - H) // 2
            if effect == "pan_left":
                ox = int((nw - W) * progress)
            elif effect == "pan_right":
                ox = int((nw - W) * (1 - progress))
            f = img_big[oy:oy + H, ox:ox + W].astype(np.float32)
        return np.clip(f, 0, 255).astype(np.uint8)

    clip = VideoClip(make_frame, duration=duration)
    clip.fps = fps
    return clip


def grade_biblical(frame):
    """Tom quente dourado-vermelho — cenas bíblicas/proféticas"""
    f = frame.astype(np.float32)
    np.multiply(f[:, :, 0], 1.15, out=f[:, :, 0])
    np.multiply(f[:, :, 1], 0.92, out=f[:, :, 1])
    np.multiply(f[:, :, 2], 0.85, out=f[:, :, 2])
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)


def grade_apocalypse(frame):
    """Tom dessaturado cinza-avermelhado — tema apocalíptico"""
    f = frame.astype(np.float32)
    gray = 0.299 * f[:, :, 0] + 0.587 * f[:, :, 1] + 0.114 * f[:, :, 2]
    for c in range(3):
        f[:, :, c] = f[:, :, c] * 0.3 + gray * 0.7
    np.multiply(f[:, :, 0], 1.1, out=f[:, :, 0])
    np.multiply(f[:, :, 2], 0.8, out=f[:, :, 2])
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)


def grade_revelation(frame):
    """Tom contrastado dourado — tema revelacional"""
    f = frame.astype(np.float32)
    mask = f > 128
    f[mask] *= 1.05
    np.multiply(f[:, :, 0], 1.08, out=f[:, :, 0])
    np.multiply(f[:, :, 2], 0.88, out=f[:, :, 2])
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)


def grade_tech(frame):
    """
    Tom tecnológico/frio — exclusivo video-017 (IA/Skynet).
    Dessatura com leve viragem azul fria:
    R×0.90 (reduz calor), B×1.15 (acentua azul digital).
    Inspira monitor de terminal, datacenter, frieza algorítmica.
    """
    f = frame.astype(np.float32)
    # Leve dessaturação para dar aspecto digital
    gray = 0.299 * f[:, :, 0] + 0.587 * f[:, :, 1] + 0.114 * f[:, :, 2]
    for c in range(3):
        f[:, :, c] = f[:, :, c] * 0.55 + gray * 0.45
    # Viragem azul fria: reduzir vermelho, elevar azul
    np.multiply(f[:, :, 0], 0.90, out=f[:, :, 0])
    np.multiply(f[:, :, 2], 1.15, out=f[:, :, 2])
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)


def kb_with_grade(img_path, duration, effect, grade_fn):
    base = ken_burns(img_path, duration, effect)

    def make_frame_graded(t):
        return grade_fn(base.make_frame(t))

    clip = VideoClip(make_frame_graded, duration=duration)
    clip.fps = FPS
    return clip


def text_screen(text, duration, bg=(0, 0, 0), color=(197, 163, 85), fontsize=72):
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", fontsize)
    except Exception:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", fontsize)
        except Exception:
            font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((W - tw) // 2, (H - th) // 2), text, fill=color, font=font)
    arr = np.array(img)
    clip = VideoClip(lambda t: arr, duration=duration)
    clip.fps = FPS
    return clip


def _select_grade(batch_id, quadro_index):
    """
    Estratégia de grade para video-017:
    - grade_tech como padrão (tom frio tecnológico)
    - grade_biblical para cenas explicitamente bíblicas/proféticas
      (batches 3 e 4 têm muitas cenas de João/Daniel/Apocalipse)
    - grade_revelation para fechamentos (batch 5)
    - grade_apocalypse para cenas de guerra/julgamento (batch 1)
    """
    if batch_id == 1:
        # Gancho + Julgamento automático — tone frio industrial
        return grade_tech if quadro_index % 2 == 0 else grade_apocalypse
    elif batch_id == 2:
        # A Máquina que já existe — tech dominante
        return grade_tech
    elif batch_id == 3:
        # João em Patmos — alterna tech com bíblico (João é bíblico, contexto é digital)
        return grade_biblical if quadro_index < 4 else grade_tech
    elif batch_id == 4:
        # Claude/Shannon/IA — tech dominante com bíblico ocasional
        if quadro_index in (3, 4, 5):  # Q41-Q43: Shannon/Teoria da Informação
            return grade_biblical
        return grade_tech
    else:
        # Fechamento (batch 5) — revelation para dar peso de conclusão
        return grade_revelation if quadro_index >= 6 else grade_tech


def render_batch(batch):
    bid = batch["id"]
    quadros = batch["quadros"]
    audio_parts = batch["audio_parts"]

    titulo = TITULOS_PARTES.get(bid, f"PARTE {bid}")
    print(f"[PHANTASMA] Renderizando batch {bid}: {titulo} ({len(quadros)-1} quadros)", flush=True)

    clips = []
    # Tela de título com nome real do bloco — fundo preto, cor dourada
    clips.append(text_screen(titulo, 2.5))

    dur_per_q = max(5.0, PARTE_DUR[audio_parts[0]] / max(1, len(quadros) - 1))
    effects = [
        "zoom_in", "zoom_out", "pan_left", "zoom_in", "pan_right", "zoom_out",
        "zoom_in", "zoom_out", "pan_left", "zoom_in", "pan_right", "zoom_out"
    ]

    for i, q in enumerate(quadros[1:]):
        img_path = ASSETS / f"Q{q:02d}.png"
        if not img_path.exists():
            print(f"  [AVISO] {img_path.name} não encontrado — tela placeholder", flush=True)
            clips.append(text_screen(f"Q{q:02d}", dur_per_q))
            continue
        effect = effects[i % len(effects)]
        grade_fn = _select_grade(bid, i)
        clips.append(kb_with_grade(img_path, dur_per_q, effect, grade_fn))

    silent_path = OUT / f"parte_{bid:02d}_silent.mp4"
    final_path  = OUT / f"parte_{bid:02d}.mp4"

    video = concatenate_videoclips(clips, method="chain")
    video.write_videofile(str(silent_path), **WRITE_OPTS)
    video.close()
    del video, clips
    gc.collect()

    audio_file = PARTES_AUDIO[audio_parts[0] - 1]
    if not audio_file.exists():
        print(f"  [AVISO] Áudio {audio_file.name} não encontrado — copiando vídeo mudo", flush=True)
        import shutil
        shutil.copy(silent_path, final_path)
        silent_path.unlink(missing_ok=True)
        return True

    if TRILHA.exists():
        cmd = [
            "ffmpeg", "-y",
            "-i", str(silent_path),
            "-i", str(audio_file),
            "-i", str(TRILHA),
            "-filter_complex",
            "[1:a]volume=1.0[narr];[2:a]volume=0.22[music];[narr][music]amix=inputs=2:duration=first[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac",
            "-shortest", str(final_path)
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(silent_path),
            "-i", str(audio_file),
            "-filter_complex", "[1:a]volume=1.0[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac",
            "-shortest", str(final_path)
        ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERRO ffmpeg] {result.stderr[-500:]}", flush=True)
        return False

    silent_path.unlink(missing_ok=True)
    print(f"[OK] parte_{bid:02d}.mp4 → {final_path}", flush=True)
    return True


# 60 quadros, 5 grupos de 12
BATCHES = [
    {"id": 1, "quadros": list(range(1, 13)),  "audio_parts": [1]},
    {"id": 2, "quadros": list(range(13, 25)), "audio_parts": [2]},
    {"id": 3, "quadros": list(range(25, 37)), "audio_parts": [3]},
    {"id": 4, "quadros": list(range(37, 49)), "audio_parts": [4]},
    {"id": 5, "quadros": list(range(49, 61)), "audio_parts": [5]},
]


def main():
    import argparse
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--only-batch", type=int, default=None)
    args, _ = parser.parse_known_args()

    if args.only_batch is not None:
        batch = next((b for b in BATCHES if b["id"] == args.only_batch), None)
        if batch is None:
            print(f"[ERRO] Batch {args.only_batch} não encontrado.", flush=True)
            sys.exit(1)
        ok = render_batch(batch)
        sys.exit(0 if ok else 1)

    print("=" * 60, flush=True)
    print("PHANTASMA — video-017-claude-skynet", flush=True)
    print("SKYNET é CLAUDE AI? O que Apocalipse 13 avisou em 95 d.C.", flush=True)
    print(f"Assets: {ASSETS}", flush=True)
    print(f"Output: {OUT}", flush=True)
    print("Grade padrão: grade_tech (tom azul frio/tecnológico)", flush=True)
    print("=" * 60, flush=True)

    script = str(Path(__file__).resolve())
    resultados = {}

    for batch in BATCHES:
        print(f"\n[DISPATCH] Batch {batch['id']}/{len(BATCHES)}", flush=True)
        result = subprocess.run(
            [sys.executable, script, "--only-batch", str(batch["id"])]
        )
        status = "OK" if result.returncode == 0 else "ERRO"
        resultados[batch["id"]] = status
        print(f"Batch {batch['id']}: {status}", flush=True)

    print("\n" + "=" * 60, flush=True)
    print("RESUMO FINAL:", flush=True)
    for bid, status in resultados.items():
        titulo = TITULOS_PARTES.get(bid, f"Parte {bid}")
        print(f"  Parte {bid} ({titulo}): {status}", flush=True)

    erros = [bid for bid, s in resultados.items() if s == "ERRO"]
    if erros:
        print(f"\n[ATENÇÃO] Batches com erro: {erros}", flush=True)
        sys.exit(1)
    else:
        print("\n[PHANTASMA] Renderização completa. Todos os batches OK.", flush=True)
        sys.exit(0)


if __name__ == "__main__":
    main()
