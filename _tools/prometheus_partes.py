#!/usr/bin/env python3
"""
Prometheus Partes — Gera um MP4 por parte de narração
Cada parte usa suas imagens correspondentes + Ken Burns + transições xfade
Resultado: video_parte1.mp4, video_parte2.mp4... prontos para juntar no CapCut

Uso:
  python prometheus_partes.py --canal sinais-do-fim --video video-007-falsa-paz
  python prometheus_partes.py --canal sinais-do-fim --video video-007-falsa-paz --transition slideleft
"""

import argparse
import json
import random
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg"}
WIDTH, HEIGHT = 1920, 1080
FPS = 30

TRANSITIONS = ["fade", "fadeblack", "wipeleft", "wiperight", "slideleft", "slideright", "dissolve", "zoomin"]
KEN_BURNS = ["zoom_in", "zoom_out", "pan_left", "pan_right", "pan_up", "pan_down"]


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] > {msg}", flush=True)


def get_duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json",
                        "-show_streams", str(path)], capture_output=True, text=True)
    try:
        for s in json.loads(r.stdout).get("streams", []):
            if "duration" in s:
                return float(s["duration"])
    except:
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
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(img_path),
        "-vf", vf, "-t", str(duration),
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
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
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-an", str(out)
    ], capture_output=True, check=True)


MAX_IMG_DURATION = 6.0  # maximo de segundos por imagem — mais dinamico
MIN_IMG_DURATION = 3.0  # minimo de segundos por imagem


def gerar_parte(images: list, audio_path: Path, parte_num: int,
                transition: str, td: float, output_path: Path, tmp_dir: Path):
    """Gera um único vídeo para uma parte.

    REGRA ADR-008: video_duration >= audio_duration + SAFETY_BUFFER
    Garantia: nenhum áudio é cortado pelo -shortest no final.
    """
    SAFETY_BUFFER = 1.0  # 1 segundo de sobra para permitir fade de saida

    audio_dur = get_duration(audio_path)
    n = len(images)

    # Cap de duracao por imagem: max 6s para manter dinamismo
    dur_each = max(MIN_IMG_DURATION, min(MAX_IMG_DURATION, audio_dur / n))

    # ── CALCULO CORRETO DO NUMERO DE SLOTS (ADR-008) ─────────────────────
    # xfade sobrepõe td segundos entre cada par de clips consecutivos.
    # Duracao real do merge: total = n_slots * dur_each - (n_slots - 1) * td
    # Queremos: total >= audio_dur + SAFETY_BUFFER
    # => n_slots >= (audio_dur + SAFETY_BUFFER - td) / (dur_each - td)
    import math
    target = audio_dur + SAFETY_BUFFER
    if dur_each > td:
        n_slots = math.ceil((target - td) / (dur_each - td))
    else:
        n_slots = math.ceil(target / dur_each)
    n_slots = max(n_slots, n)  # nunca menos que as imagens disponiveis

    images_loop = [images[i % n] for i in range(n_slots)]

    # Validacao final: calcular duracao real do merge
    video_dur_real = n_slots * dur_each - (n_slots - 1) * td
    log(f"  Parte {parte_num}: {n} img → {n_slots} slots × {dur_each:.1f}s "
        f"= video {video_dur_real:.1f}s / audio {audio_dur:.1f}s "
        f"(margem {video_dur_real - audio_dur:.1f}s)")

    if video_dur_real < audio_dur:
        log(f"  [ERRO CRITICO] Video ({video_dur_real:.1f}s) MENOR que audio ({audio_dur:.1f}s)!")
        raise RuntimeError(f"ADR-008 violado: parte {parte_num} dessincronizada")

    # Gerar clips Ken Burns
    kb_paths = []
    for i, img in enumerate(images_loop):
        effect = KEN_BURNS[i % len(KEN_BURNS)]
        kb = tmp_dir / f"p{parte_num}_kb{i:03d}.mp4"
        generate_clip(img, dur_each, effect, kb)
        kb_paths.append(kb)

    # Aplicar transições xfade
    merged = kb_paths[0]
    for i in range(1, len(kb_paths)):
        t_type = transition if transition != "random" else random.choice(TRANSITIONS)
        out_m = tmp_dir / f"p{parte_num}_merged{i:02d}.mp4"
        apply_xfade(merged, kb_paths[i], t_type, td, out_m)
        merged = out_m

    # Combinar vídeo + áudio + comprimir
    # NAO usar -shortest aqui: ja garantimos video >= audio acima (ADR-008).
    # Usar -t audio_dur + 0.5 para forcar o vídeo a cobrir o audio completo + fade.
    final_dur = audio_dur + 0.5
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(merged),
        "-i", str(audio_path),
        "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-r", str(FPS),
        "-t", f"{final_dur:.3f}",
        str(output_path)
    ], capture_output=True, check=True)

    # Validacao pos-renderizacao (ADR-008)
    final_video_dur = get_duration(output_path)
    if final_video_dur < audio_dur - 0.1:  # tolerancia 100ms
        log(f"  [ERRO CRITICO] Video final ({final_video_dur:.2f}s) < audio ({audio_dur:.2f}s)")
        raise RuntimeError(f"ADR-008 violado apos render: parte {parte_num}")

    size_mb = output_path.stat().st_size / 1024 / 1024
    log(f"  OK -> {output_path.name} ({size_mb:.0f} MB) "
        f"| video {final_video_dur:.2f}s / audio {audio_dur:.2f}s [OK sync]")


def main():
    parser = argparse.ArgumentParser(description="Prometheus Partes - Um MP4 por parte de audio")
    parser.add_argument("--canal", required=True)
    parser.add_argument("--video", required=True)
    parser.add_argument("--transition", default="random",
                        choices=TRANSITIONS + ["random"])
    parser.add_argument("--transition-duration", type=float, default=0.6)
    args = parser.parse_args()

    video_dir = BASE_DIR / "canais" / args.canal / "videos" / args.video
    img_dir = video_dir / "6-assets" / "imagens"
    audio_dir = video_dir / "6-assets" / "audio_suno"
    output_dir = video_dir / "7-edicao" / "partes"
    output_dir.mkdir(parents=True, exist_ok=True)

    log(f"Canal: {args.canal} | Video: {args.video} | Transicao: {args.transition}")

    # ── Imagens ordenadas ──────────────────────────────────────────────────
    images = sorted(
        [f for f in img_dir.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS],
        key=lambda f: f.name)
    log(f"Imagens totais: {len(images)}")

    # ── Partes de narração ─────────────────────────────────────────────────
    mk = ["trilha", "music", "instrumental"]
    partes = sorted([f for f in audio_dir.iterdir()
                     if f.suffix.lower() in AUDIO_EXTENSIONS
                     and not any(k in f.name.lower() for k in mk)],
                    key=lambda f: f.name)
    log(f"Partes de audio: {len(partes)}")

    if not partes:
        log("ERRO: Nenhuma parte de narração encontrada")
        sys.exit(1)

    # ── Distribuir imagens entre partes ───────────────────────────────────
    # Proporção baseada na duração de cada parte
    durations = [get_duration(p) for p in partes]
    total_dur = sum(durations)
    imgs_por_parte = []
    idx = 0
    for i, dur in enumerate(durations):
        proporcao = dur / total_dur
        n = max(3, round(len(images) * proporcao))
        if i == len(partes) - 1:
            n = len(images) - idx  # última parte pega o resto
        n = max(3, min(n, len(images) - idx))
        imgs_por_parte.append(images[idx:idx + n])
        idx += n

    log(f"Distribuicao: {[len(g) for g in imgs_por_parte]} imagens por parte")

    # ── Gerar um vídeo por parte ───────────────────────────────────────────
    tmp_dir = Path(tempfile.mkdtemp(prefix="prometheus_partes_"))
    try:
        for i, (parte_audio, parte_imgs) in enumerate(zip(partes, imgs_por_parte), 1):
            log(f"\n=== PARTE {i}/{len(partes)}: {parte_audio.name} ===")
            output_path = output_dir / f"video_parte{i:02d}.mp4"
            gerar_parte(
                images=parte_imgs,
                audio_path=parte_audio,
                parte_num=i,
                transition=args.transition,
                td=args.transition_duration,
                output_path=output_path,
                tmp_dir=tmp_dir
            )

        log("\n" + "=" * 50)
        log(f"CONCLUIDO! {len(partes)} videos gerados em:")
        log(f"  {output_dir}")
        for f in sorted(output_dir.iterdir()):
            mb = f.stat().st_size / 1024 / 1024
            log(f"  {f.name} — {mb:.0f} MB")
        log("=" * 50)

    finally:
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
