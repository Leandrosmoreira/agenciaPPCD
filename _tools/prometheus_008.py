#!/usr/bin/env python3
"""
Prometheus 008 — ffmpeg puro, sem MoviePy
Video: video-008-sinais-fisicos | Canal: Sinais do Fim

- Ken Burns via zoompan filter nativo do ffmpeg
- xfade para transicoes entre clips
- Detecta automaticamente parte*.mp3 e Trilha*.mp3
- Concatena todas as trilhas em loop continuo
- Mix narracao (1.0) + trilha (0.22) por parte, sem corte de audio
- Output: parte_01.mp4 ... parte_05.mp4 prontos para CapCut

Uso:
  python _tools/prometheus_008.py
"""

import json
import random
import subprocess
import sys
import io
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── PATHS ──────────────────────────────────────────────────────────────────────
BASE      = Path(__file__).resolve().parent.parent
VIDEO_DIR = BASE / "canais" / "sinais-do-fim" / "videos" / "video-008-sinais-fisicos"
IMG_DIR   = VIDEO_DIR / "6-assets" / "imagens"
AUDIO_DIR = VIDEO_DIR / "6-assets" / "audio_suno"
OUT_DIR   = VIDEO_DIR / "7-edicao"
OUT_DIR.mkdir(exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 30
TRANS_DUR = 0.6   # duracao da transicao xfade em segundos
TRANSITION = "fade"  # fade | dissolve | wipeleft | slideleft | zoomin

IMG_EXTS   = {".png", ".jpg", ".jpeg", ".webp"}
AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".ogg"}

# ── LOG ────────────────────────────────────────────────────────────────────────
def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


# ── FFPROBE DURACAO ────────────────────────────────────────────────────────────
def get_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", str(path)],
        capture_output=True, text=True
    )
    try:
        for s in json.loads(r.stdout).get("streams", []):
            if "duration" in s:
                return float(s["duration"])
    except Exception:
        pass
    return 0.0


# ── KEN BURNS (zoompan nativo ffmpeg) ─────────────────────────────────────────
EFFECTS = ["zoom_in", "zoom_out", "pan_left", "pan_right", "pan_up", "pan_down"]

def build_zoompan(effect: str, duration: float) -> str:
    frames = int(duration * FPS)
    w, h = WIDTH, HEIGHT
    if effect == "zoom_in":
        return (f"zoompan=z='min(zoom+0.0015,1.5)':"
                f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                f"d={frames}:s={w}x{h}:fps={FPS}")
    elif effect == "zoom_out":
        return (f"zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':"
                f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                f"d={frames}:s={w}x{h}:fps={FPS}")
    elif effect == "pan_left":
        return (f"zoompan=z='1.12':x='iw*0.12*(on/{frames})':"
                f"y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={FPS}")
    elif effect == "pan_right":
        return (f"zoompan=z='1.12':x='iw*0.12*(1-on/{frames})':"
                f"y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={FPS}")
    elif effect == "pan_up":
        return (f"zoompan=z='1.12':x='iw/2-(iw/zoom/2)':"
                f"y='ih*0.12*(on/{frames})':d={frames}:s={w}x{h}:fps={FPS}")
    elif effect == "pan_down":
        return (f"zoompan=z='1.12':x='iw/2-(iw/zoom/2)':"
                f"y='ih*0.12*(1-on/{frames})':d={frames}:s={w}x{h}:fps={FPS}")
    else:
        return (f"zoompan=z='1.0':x='iw/2-(iw/zoom/2)':"
                f"y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={FPS}")


def render_ken_burns(img: Path, duration: float, effect: str, out: Path):
    zp = build_zoompan(effect, duration)
    vf = f"scale={WIDTH*2}:{HEIGHT*2},format=yuv420p,{zp},scale={WIDTH}:{HEIGHT},setsar=1"
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(img),
        "-vf", vf, "-t", str(duration),
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-r", str(FPS), "-an", str(out)
    ], capture_output=True, check=True)


def apply_xfade(clip_a: Path, clip_b: Path, transition: str, td: float, out: Path):
    dur_a = get_duration(clip_a)
    offset = max(0.01, dur_a - td)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(clip_a), "-i", str(clip_b),
        "-filter_complex",
        f"[0:v][1:v]xfade=transition={transition}:duration={td}:offset={offset:.3f}[v]",
        "-map", "[v]",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-r", str(FPS), "-an", str(out)
    ], capture_output=True, check=True)


# ── GERAR UMA PARTE ───────────────────────────────────────────────────────────
def gerar_parte(images: list, narracao: Path, parte_num: int,
                trilha_concat: Path, trilha_offset: float,
                output_path: Path, tmp_dir: Path) -> float:
    """
    Gera um MP4 com ken burns + xfade + narracao + trilha.
    Retorna a duracao real do video gerado.
    """
    narr_dur = get_duration(narracao)
    n = len(images)
    dur_each = max(3.0, narr_dur / n)

    log(f"  {n} imagens x {dur_each:.1f}s = ~{n*dur_each:.1f}s | narracao={narr_dur:.1f}s")

    # ── Ken Burns em cada imagem ───────────────────────────────────────────────
    kb_paths = []
    for i, img in enumerate(images):
        effect = EFFECTS[i % len(EFFECTS)]
        kb = tmp_dir / f"p{parte_num}_kb{i:02d}.mp4"
        render_ken_burns(img, dur_each, effect, kb)
        kb_paths.append(kb)

    # ── Encadear com xfade ─────────────────────────────────────────────────────
    merged = kb_paths[0]
    for i in range(1, len(kb_paths)):
        out_m = tmp_dir / f"p{parte_num}_xf{i:02d}.mp4"
        apply_xfade(merged, kb_paths[i], TRANSITION, TRANS_DUR, out_m)
        merged = out_m

    video_dur = get_duration(merged)
    log(f"  Video silencioso: {video_dur:.1f}s")

    # ── Mix narracao + trilha ─────────────────────────────────────────────────
    # Trilha: pular offset acumulado, volume 0.22, fade out 3s antes do fim
    trilha_fade_st = max(narr_dur - 3.0, 0.0)
    # Narracao: volume 1.0, fade out 1s antes do fim
    narr_fade_st   = max(narr_dur - 1.5, 0.0)

    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(merged),
        "-ss", f"{trilha_offset:.3f}", "-i", str(trilha_concat),
        "-i", str(narracao),
        "-filter_complex",
        (f"[1:a]volume=0.22,"
         f"atrim=0:{narr_dur:.3f},"
         f"afade=t=in:st=0:d=2,"
         f"afade=t=out:st={trilha_fade_st:.3f}:d=3[trilha];"
         f"[2:a]volume=1.0,"
         f"afade=t=out:st={narr_fade_st:.3f}:d=1.5[narr];"
         "[trilha][narr]amix=inputs=2:duration=shortest[audio]"),
        "-map", "0:v", "-map", "[audio]",
        "-c:v", "libx264", "-crf", "23", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k",
        "-r", str(FPS),
        "-t", f"{narr_dur:.3f}",   # cortar exatamente na duracao da narracao
        str(output_path)
    ], check=True)

    final_dur = get_duration(output_path)
    mb = output_path.stat().st_size / 1e6
    log(f"  => {output_path.name} | {mb:.1f} MB | {final_dur:.1f}s")
    return narr_dur   # retorna duracao da narracao para offset da trilha


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    log("=" * 60)
    log("Prometheus 008 — ffmpeg puro")
    log("=" * 60)

    # ── Imagens ────────────────────────────────────────────────────────────────
    images = sorted(
        [f for f in IMG_DIR.iterdir() if f.suffix.lower() in IMG_EXTS],
        key=lambda f: f.name
    )
    log(f"Imagens: {len(images)}")

    # ── Narracoes (parte*.mp3) ─────────────────────────────────────────────────
    NARR_KEYWORDS = ["trilha", "trilha2", "trilha3", "music", "instrumental", "bgm"]
    partes = sorted([
        f for f in AUDIO_DIR.iterdir()
        if f.suffix.lower() in AUDIO_EXTS
        and not any(k in f.name.lower() for k in NARR_KEYWORDS)
    ], key=lambda f: f.name)
    log(f"Partes de narracao: {len(partes)} — {[p.name for p in partes]}")

    # ── Trilhas (Trilha*.mp3) ──────────────────────────────────────────────────
    trilhas = sorted([
        f for f in AUDIO_DIR.iterdir()
        if f.suffix.lower() in AUDIO_EXTS
        and any(k in f.name.lower() for k in ["trilha", "music", "instrumental", "bgm"])
    ], key=lambda f: f.name)
    log(f"Trilhas encontradas: {len(trilhas)} — {[t.name for t in trilhas]}")

    if not partes:
        log("ERRO: nenhuma parte de narracao encontrada")
        sys.exit(1)

    if not trilhas:
        log("AVISO: nenhuma trilha encontrada — vídeos apenas com narracao")

    tmp_dir = Path(tempfile.mkdtemp(prefix="prometheus_008_"))
    log(f"Temp dir: {tmp_dir}")

    try:
        # ── Concatenar trilhas em loop ─────────────────────────────────────────
        trilha_concat = None
        if trilhas:
            if len(trilhas) == 1:
                trilha_concat = trilhas[0]
                log(f"Trilha: {trilha_concat.name}")
            else:
                # Concatenar todas as trilhas em sequencia repetida (loop x3 para garantir)
                concat_list = tmp_dir / "trilhas_concat.txt"
                with open(str(concat_list), "w") as f:
                    for _ in range(3):      # 3 loops para cobrir video longo
                        for t in trilhas:
                            f.write(f"file '{t}'\n")
                trilha_concat = tmp_dir / "trilha_full.mp3"
                subprocess.run([
                    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(concat_list),
                    "-c", "copy", str(trilha_concat)
                ], check=True)
                dur_total = get_duration(trilha_concat)
                log(f"Trilha concatenada ({len(trilhas)} arquivos x3): {dur_total:.1f}s")

        # ── Distribuir imagens proporcionalmente pelas partes ─────────────────
        durations   = [get_duration(p) for p in partes]
        total_dur   = sum(durations)
        imgs_por_parte = []
        idx = 0
        for i, dur in enumerate(durations):
            if i == len(partes) - 1:
                n = len(images) - idx
            else:
                n = max(3, round(len(images) * dur / total_dur))
                n = max(3, min(n, len(images) - idx - (len(partes) - i - 1) * 3))
            imgs_por_parte.append(images[idx:idx + n])
            idx += n

        log(f"Distribuicao: {[len(g) for g in imgs_por_parte]} imagens por parte")
        log(f"Duracoes: {[f'{d:.1f}s' for d in durations]}")

        # ── Gerar partes ──────────────────────────────────────────────────────
        trilha_offset = 0.0
        for i, (parte_audio, parte_imgs) in enumerate(zip(partes, imgs_por_parte), 1):
            log(f"\n{'='*50}")
            log(f"PARTE {i}/{len(partes)}: {parte_audio.name} | {len(parte_imgs)} imagens")
            log(f"{'='*50}")
            output_path = OUT_DIR / f"parte_{i:02d}.mp4"
            parte_dur = gerar_parte(
                images=parte_imgs,
                narracao=parte_audio,
                parte_num=i,
                trilha_concat=trilha_concat,
                trilha_offset=trilha_offset,
                output_path=output_path,
                tmp_dir=tmp_dir
            )
            trilha_offset += parte_dur

        # ── Resumo ────────────────────────────────────────────────────────────
        log(f"\n{'='*60}")
        log("CONCLUIDO")
        log(f"{'='*60}")
        total_mb = 0.0
        for i in range(1, len(partes) + 1):
            p = OUT_DIR / f"parte_{i:02d}.mp4"
            if p.exists():
                mb = p.stat().st_size / 1e6
                total_mb += mb
                log(f"  parte_{i:02d}.mp4  {mb:.1f} MB")
            else:
                log(f"  parte_{i:02d}.mp4  NAO GERADO")
        log(f"\nTotal: {total_mb:.1f} MB")
        log(f"Pasta: {OUT_DIR}")
        log("Importe as partes no CapCut em ordem e una.")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
