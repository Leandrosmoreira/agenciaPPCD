#!/usr/bin/env python3
"""
PROMETHEUS — video-010-biblia-etiope
Gera um MP4 por parte de narração usando ffmpeg puro.
Ken Burns (zoompan) + xfade transitions.
Padrao da agencia Abismo Criativo.

Uso:
  cd C:\\Users\\Leandro\\Downloads\\agencia
  python _tools/prometheus_010.py
"""

import json
import random
import subprocess
import sys
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR   = Path(__file__).resolve().parent.parent
VIDEO_DIR  = BASE_DIR / "canais/sinais-do-fim/videos/video-010-biblia-etiope"
IMG_DIR    = VIDEO_DIR / "7-imagens"
AUDIO_DIR  = VIDEO_DIR / "5-audio"
OUTPUT_DIR = VIDEO_DIR / "7-edicao" / "partes"

WIDTH, HEIGHT = 1920, 1080
FPS = 30
TRANSITION_DURATION = 0.6

TRANSITIONS = ["fade", "fadeblack", "wipeleft", "wiperight", "slideleft",
               "slideright", "dissolve", "zoomin"]
KEN_BURNS   = ["zoom_in", "zoom_out", "pan_left", "pan_right", "pan_up", "pan_down"]

TRILHA_VOLUME = 0.20  # volume da trilha de fundo

# Ordem exata dos arquivos de audio
AUDIO_FILES = [
    "PARTE1.mp3",
    "PARTE2.mp3",
    "PARTE3.mp3",
    "PARTE4.mp3",
    "PARTE5.mp3",
    "PARTE6.mp3",
    "PARTE7.mp3",
]


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


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


def build_zoompan(effect: str, duration: float) -> str:
    frames = int(duration * FPS)
    w, h = WIDTH, HEIGHT
    if effect == "zoom_in":
        return f"zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={FPS}"
    elif effect == "zoom_out":
        return f"zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={FPS}"
    elif effect == "pan_left":
        return f"zoompan=z='1.12':x='iw*0.12*(on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={FPS}"
    elif effect == "pan_right":
        return f"zoompan=z='1.12':x='iw*0.12*(1-on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={FPS}"
    elif effect == "pan_up":
        return f"zoompan=z='1.12':x='iw/2-(iw/zoom/2)':y='ih*0.12*(on/{frames})':d={frames}:s={w}x{h}:fps={FPS}"
    elif effect == "pan_down":
        return f"zoompan=z='1.12':x='iw/2-(iw/zoom/2)':y='ih*0.12*(1-on/{frames})':d={frames}:s={w}x{h}:fps={FPS}"
    else:
        return f"zoompan=z='1':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={FPS}"


def generate_clip(img_path: Path, duration: float, effect: str, out: Path):
    zp = build_zoompan(effect, duration)
    vf = f"scale={WIDTH*2}:{HEIGHT*2},format=yuv420p,{zp},scale={WIDTH}:{HEIGHT},setsar=1"
    result = subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(img_path),
        "-vf", vf, "-t", str(duration),
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-an", str(out)
    ], capture_output=True)
    if result.returncode != 0:
        log(f"  ERRO clip: {result.stderr.decode(errors='replace')[-200:]}")
        raise RuntimeError(f"ffmpeg clip failed: {img_path.name}")


def apply_xfade(clip_a: Path, clip_b: Path, transition: str, td: float, out: Path):
    dur_a = get_duration(clip_a)
    offset = max(0.01, dur_a - td)
    result = subprocess.run([
        "ffmpeg", "-y",
        "-i", str(clip_a), "-i", str(clip_b),
        "-filter_complex",
        f"[0:v][1:v]xfade=transition={transition}:duration={td}:offset={offset:.3f}[v]",
        "-map", "[v]",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-an", str(out)
    ], capture_output=True)
    if result.returncode != 0:
        log(f"  ERRO xfade: {result.stderr.decode(errors='replace')[-200:]}")
        raise RuntimeError("ffmpeg xfade failed")


def build_trilha_loop(trilha_files: list, target_dur: float, out: Path):
    """Concatena e/ou corta trilhas para cobrir target_dur segundos."""
    if not trilha_files:
        return None
    concat_list = out.parent / f"trilha_concat_{out.stem}.txt"
    # Calcular quantas repeticoes sao necessarias
    total_trilha = sum(get_duration(t) for t in trilha_files)
    reps = max(1, int(target_dur / total_trilha) + 2)
    entries = []
    for _ in range(reps):
        for t in trilha_files:
            entries.append(f"file '{str(t).replace(chr(92), '/')}'\n")
    concat_list.write_text("".join(entries), encoding="utf-8")
    result = subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-t", str(target_dur),
        "-c:a", "aac", "-b:a", "192k",
        str(out)
    ], capture_output=True)
    if result.returncode != 0:
        return None
    return out


MAX_IMG_DURATION = 6.0  # maximo 6s por imagem — mantém ritmo dinamico
MIN_IMG_DURATION = 3.0  # minimo 3s por imagem


def gerar_parte(images, audio_path: Path, parte_num: int, output_path: Path, tmp_dir: Path, trilha_files: list = None):
    import math
    audio_dur = get_duration(audio_path)
    n = len(images)

    # Cap de 6s por imagem — sem cap = imagens estaticas de 10-13s
    dur_each = max(MIN_IMG_DURATION, min(MAX_IMG_DURATION, audio_dur / n))

    # Looping: se poucas imagens, repetir para cobrir o audio
    n_slots = math.ceil(audio_dur / dur_each)
    images = [images[i % n] for i in range(n_slots)]

    log(f"  {n} imagens -> {n_slots} slots x {dur_each:.1f}s = {audio_dur:.1f}s audio")

    # Gerar clips Ken Burns
    kb_paths = []
    for i, img in enumerate(images):
        effect = KEN_BURNS[i % len(KEN_BURNS)]
        kb = tmp_dir / f"p{parte_num}_kb{i:02d}.mp4"
        generate_clip(img, dur_each, effect, kb)
        if (i + 1) % 5 == 0:
            log(f"    [{i+1}/{len(images)}] clips gerados...")
        kb_paths.append(kb)

    # Aplicar transicoes xfade
    merged = kb_paths[0]
    for i in range(1, len(kb_paths)):
        t_type = random.choice(TRANSITIONS)
        out_m = tmp_dir / f"p{parte_num}_merged{i:02d}.mp4"
        apply_xfade(merged, kb_paths[i], t_type, TRANSITION_DURATION, out_m)
        merged = out_m

    # Combinar video + audio (com trilha de fundo se disponivel)
    if trilha_files:
        video_dur = get_duration(merged)
        trilha_loop = tmp_dir / f"p{parte_num}_trilha.aac"
        trilha_ok = build_trilha_loop(trilha_files, video_dur + 2, trilha_loop)
    else:
        trilha_ok = None

    if trilha_ok:
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", str(merged),
            "-i", str(audio_path),
            "-i", str(trilha_ok),
            "-filter_complex",
            f"[1:a]volume=1.0[narr];[2:a]volume={TRILHA_VOLUME}[music];[narr][music]amix=inputs=2:duration=shortest[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-r", str(FPS), "-shortest",
            str(output_path)
        ], capture_output=True)
    else:
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", str(merged),
            "-i", str(audio_path),
            "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-r", str(FPS), "-shortest",
            str(output_path)
        ], capture_output=True)

    if result.returncode != 0:
        log(f"  ERRO final: {result.stderr.decode(errors='replace')[-200:]}")
        raise RuntimeError("ffmpeg final merge failed")

    size_mb = output_path.stat().st_size / 1024 / 1024
    log(f"  OK -> {output_path.name} ({size_mb:.0f} MB)")


def main():
    print("=" * 60)
    print("PROMETHEUS — video-010-biblia-etiope")
    print("Abismo Criativo | Canal: Sinais do Fim")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Imagens ordenadas
    images = sorted(IMG_DIR.glob("Q*.png"), key=lambda f: f.name)
    log(f"Imagens: {len(images)}")

    # Partes de audio (na ordem exata)
    partes = []
    for nome in AUDIO_FILES:
        p = AUDIO_DIR / nome
        if p.exists():
            partes.append(p)
        else:
            log(f"[WARN] Audio nao encontrado: {nome}")

    log(f"Partes de audio: {len(partes)}")

    # Trilhas de fundo
    trilha_files = sorted(AUDIO_DIR.glob("Trilha*.mp3"), key=lambda f: f.name)
    if trilha_files:
        log(f"Trilhas: {[t.name for t in trilha_files]} (volume {TRILHA_VOLUME})")
    else:
        log("Trilhas: nenhuma encontrada")

    # Distribuir imagens proporcionalmente por duracao
    durations = [get_duration(p) for p in partes]
    total_dur = sum(durations)
    imgs_por_parte = []
    idx = 0
    for i, dur in enumerate(durations):
        proporcao = dur / total_dur
        n = max(3, round(len(images) * proporcao))
        if i == len(partes) - 1:
            n = len(images) - idx
        n = max(3, min(n, len(images) - idx))
        imgs_por_parte.append(images[idx:idx + n])
        idx += n

    log(f"Distribuicao: {[len(g) for g in imgs_por_parte]} imagens por parte")

    tmp_dir = Path(tempfile.mkdtemp(prefix="prometheus_010_"))
    try:
        for i, (audio, imgs) in enumerate(zip(partes, imgs_por_parte), 1):
            log(f"\n=== PARTE {i}/{len(partes)}: {audio.name} ===")
            out = OUTPUT_DIR / f"video_parte{i:02d}.mp4"
            gerar_parte(imgs, audio, i, out, tmp_dir, trilha_files)

        log("\n" + "=" * 60)
        log(f"CONCLUIDO! {len(partes)} videos gerados em:")
        log(f"  {OUTPUT_DIR}")
        for f in sorted(OUTPUT_DIR.glob("*.mp4")):
            mb = f.stat().st_size / 1024 / 1024
            log(f"  {f.name} — {mb:.0f} MB")
        log("=" * 60)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
