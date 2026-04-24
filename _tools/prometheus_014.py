#!/usr/bin/env python3
"""
PROMETHEUS — video-014-arrebatamento
ffmpeg puro: Ken Burns agressivo + xfade + cap 6s/imagem + loop
60 quadros estáticos. Veo3 em Q01-Q04 (gancho ~32s).
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
VIDEO_DIR  = BASE_DIR / "canais/sinais-do-fim/videos/video-014-arrebatamento"
IMG_DIR    = VIDEO_DIR / "6-assets"
VEO_DIR    = IMG_DIR / "veo3"
AUDIO_DIR  = VIDEO_DIR / "5-audio"
OUTPUT_DIR = VIDEO_DIR / "7-edicao" / "partes"

WIDTH, HEIGHT = 1920, 1080
FPS = 30
TRANSITION_DURATION = 0.6

TRANSITIONS = ["fade", "fadeblack", "wipeleft", "wiperight", "slideleft",
               "slideright", "dissolve", "zoomin"]
KEN_BURNS   = ["zoom_in", "zoom_out", "pan_left", "pan_right", "pan_up", "pan_down"]

TRILHA_VOLUME = 0.22

VEO_QUADROS = {1, 2, 3, 4}  # Clips Veo3 para gancho (primeiros ~32s)

EFFECT_OVERRIDE = {}

AUDIO_FILES = [
    "PARTE1.mp3", "PARTE2.mp3", "PARTE3.mp3", "PARTE4.mp3", "PARTE5.mp3",
]

# Trilha por parte
TRILHAS_POR_PARTE = {
    1: "Trilha1.mp3", 2: "Trilha1.mp3",
    3: "Trilha2.mp3", 4: "Trilha2.mp3",
    5: "Trilha3.mp3",
}

MAX_IMG_DURATION = 6.0
MIN_IMG_DURATION = 3.5


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


def generate_clip_img(img_path: Path, duration: float, effect: str, out: Path):
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


def generate_clip_veo(veo_path: Path, out: Path):
    """Normaliza clip Veo3 para 1920x1080@30fps, sem áudio."""
    result = subprocess.run([
        "ffmpeg", "-y", "-i", str(veo_path),
        "-vf", f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,crop={WIDTH}:{HEIGHT},setsar=1",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-an", str(out)
    ], capture_output=True)
    if result.returncode != 0:
        log(f"  ERRO veo: {result.stderr.decode(errors='replace')[-200:]}")
        raise RuntimeError(f"ffmpeg veo failed: {veo_path.name}")


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


def build_trilha_loop(trilha_file: Path, target_dur: float, out: Path):
    total = get_duration(trilha_file)
    reps = max(1, int(target_dur / max(total, 1)) + 2)
    concat_list = out.parent / f"trilha_concat_{out.stem}.txt"
    entries = [f"file '{str(trilha_file).replace(chr(92), '/')}'\n" for _ in range(reps)]
    concat_list.write_text("".join(entries), encoding="utf-8")
    result = subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-t", str(target_dur),
        "-c:a", "aac", "-b:a", "192k",
        str(out)
    ], capture_output=True)
    return out if result.returncode == 0 else None


def parse_q_num(name: str):
    """Q03.png -> (3, 0); Q02_1.png -> (2, 1)."""
    stem = Path(name).stem.upper()
    if "_" in stem:
        head, _, tail = stem.partition("_")
        base = "".join(ch for ch in head if ch.isdigit())
        var = "".join(ch for ch in tail if ch.isdigit())
        return (int(base) if base else 0, int(var) if var else 0)
    digits = "".join(ch for ch in stem if ch.isdigit())
    return (int(digits) if digits else 0, 0)


def gerar_parte(quadros, audio_path: Path, parte_num: int, output_path: Path,
                tmp_dir: Path, trilha_file: Path):
    import math
    audio_dur = get_duration(audio_path)

    veo_q_in_parte = [q for q in quadros if parse_q_num(q.name)[0] in VEO_QUADROS and q.suffix.lower() == ".mp4"]
    img_q_in_parte = [q for q in quadros if q not in veo_q_in_parte]

    veo_total = sum(get_duration(q) for q in veo_q_in_parte)
    img_available = max(1.0, audio_dur - veo_total)

    n_img = len(img_q_in_parte)
    if n_img > 0:
        dur_each = max(MIN_IMG_DURATION, min(MAX_IMG_DURATION, img_available / n_img))
        n_slots = math.ceil(img_available / dur_each)
        if n_slots > n_img:
            img_q_in_parte = [img_q_in_parte[i % n_img] for i in range(n_slots)]
            dur_each = img_available / n_slots
            dur_each = max(MIN_IMG_DURATION, min(MAX_IMG_DURATION, dur_each))
    else:
        dur_each = 0.0

    log(f"  Quadros: {len(quadros)} ({len(veo_q_in_parte)} Veo3 + {len(img_q_in_parte)} imgs x {dur_each:.1f}s)")
    log(f"  Audio: {audio_dur:.1f}s | Veo3 total: {veo_total:.1f}s | Imgs: {img_available:.1f}s")

    clips = []
    for i, q in enumerate(quadros):
        qnum_tuple = parse_q_num(q.name)
        qnum = qnum_tuple[0]
        is_variant = qnum_tuple[1] > 0
        out = tmp_dir / f"p{parte_num}_c{i:02d}.mp4"
        if qnum in VEO_QUADROS and not is_variant:
            veo_path = VEO_DIR / f"VEO_Q{qnum:02d}.mp4"
            if veo_path.exists():
                generate_clip_veo(veo_path, out)
            else:
                effect = EFFECT_OVERRIDE.get(qnum, KEN_BURNS[i % len(KEN_BURNS)])
                generate_clip_img(q, dur_each, effect, out)
        else:
            effect = EFFECT_OVERRIDE.get(qnum, KEN_BURNS[i % len(KEN_BURNS)])
            generate_clip_img(q, dur_each, effect, out)
        clips.append(out)
        if (i + 1) % 5 == 0:
            log(f"    [{i+1}/{len(quadros)}] clips gerados...")

    def _effective_dur(clip_list):
        total = sum(get_duration(c) for c in clip_list)
        return total - max(0, len(clip_list) - 1) * TRANSITION_DURATION

    target_dur = audio_dur + 0.8
    eff = _effective_dur(clips)
    loop_idx = 0
    while eff < target_dur and img_q_in_parte:
        offset = (loop_idx * 3 + len(clips)) % len(img_q_in_parte)
        extra = img_q_in_parte[offset]
        effect = KEN_BURNS[(len(clips) + loop_idx) % len(KEN_BURNS)]
        out = tmp_dir / f"p{parte_num}_cx{len(clips):02d}.mp4"
        generate_clip_img(extra, MAX_IMG_DURATION, effect, out)
        clips.append(out)
        loop_idx += 1
        eff = _effective_dur(clips)
    log(f"  Extras: {loop_idx} clips adicionais | eff_dur={eff:.1f}s >= target={target_dur:.1f}s")

    last_t = None
    merged = clips[0]
    for i in range(1, len(clips)):
        choices = [t for t in TRANSITIONS if t != last_t]
        t_type = random.choice(choices)
        last_t = t_type
        out_m = tmp_dir / f"p{parte_num}_m{i:02d}.mp4"
        apply_xfade(merged, clips[i], t_type, TRANSITION_DURATION, out_m)
        merged = out_m

    video_dur = get_duration(merged)

    if video_dur < audio_dur + 0.2:
        gap = (audio_dur + 0.3) - video_dur
        if gap > 1.0:
            log(f"  [WARN] Gap grande {gap:.1f}s — loop de clips falhou! tpad como ultima opcao")
        else:
            log(f"  [SYNC] Safety-net pad {gap:.2f}s")
        merged_padded = tmp_dir / f"p{parte_num}_padded.mp4"
        r_pad = subprocess.run([
            "ffmpeg", "-y", "-i", str(merged),
            "-vf", f"tpad=stop_mode=clone:stop_duration={gap:.2f}",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-an",
            str(merged_padded)
        ], capture_output=True)
        if r_pad.returncode == 0:
            merged = merged_padded
            video_dur = get_duration(merged)

    trilha_loop = tmp_dir / f"p{parte_num}_trilha.aac"
    trilha_ok = build_trilha_loop(trilha_file, video_dur + 2, trilha_loop)

    final_dur = max(audio_dur, video_dur)

    if trilha_ok:
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", str(merged),
            "-i", str(audio_path),
            "-i", str(trilha_ok),
            "-filter_complex",
            f"[1:a]volume=1.0[narr];[2:a]volume={TRILHA_VOLUME},afade=t=out:st={final_dur-2}:d=2[music];[narr][music]amix=inputs=2:duration=longest:dropout_transition=0[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-r", str(FPS),
            "-t", f"{final_dur:.2f}",
            str(output_path)
        ], capture_output=True)
    else:
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", str(merged),
            "-i", str(audio_path),
            "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-r", str(FPS),
            "-t", f"{final_dur:.2f}",
            str(output_path)
        ], capture_output=True)

    if result.returncode != 0:
        log(f"  ERRO final: {result.stderr.decode(errors='replace')[-200:]}")
        raise RuntimeError("ffmpeg final merge failed")

    size_mb = output_path.stat().st_size / 1024 / 1024
    log(f"  OK -> {output_path.name} ({size_mb:.0f} MB)")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--only-parte", type=int, default=None)
    ap.add_argument("--from-parte", type=int, default=1)
    args = ap.parse_args()

    print("=" * 60)
    print("PROMETHEUS — video-014-arrebatamento")
    print("Ken Burns dinâmico (cap 6s) + 4 clips Veo3 + xfade")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    images = sorted(IMG_DIR.glob("Q*.png"), key=lambda f: parse_q_num(f.name))
    log(f"Imagens: {len(images)}")

    partes_audio = [AUDIO_DIR / n for n in AUDIO_FILES if (AUDIO_DIR / n).exists()]
    log(f"Partes de áudio: {len(partes_audio)}")

    n_per_parte = len(images) // len(partes_audio)
    resto = len(images) % len(partes_audio)
    grupos = []
    idx = 0
    for i in range(len(partes_audio)):
        n = n_per_parte + (1 if i < resto else 0)
        grupos.append(images[idx:idx+n])
        idx += n
    log(f"Distribuição: {[len(g) for g in grupos]} quadros por parte")

    tmp_dir = Path(tempfile.mkdtemp(prefix="prometheus_014_"))
    try:
        for i, (audio, quadros) in enumerate(zip(partes_audio, grupos), 1):
            if args.only_parte and i != args.only_parte:
                continue
            if i < args.from_parte:
                continue
            log(f"\n=== PARTE {i}/{len(partes_audio)}: {audio.name} ===")
            trilha = AUDIO_DIR / TRILHAS_POR_PARTE.get(i, "Trilha1.mp3")
            out = OUTPUT_DIR / f"video_parte{i:02d}.mp4"
            gerar_parte(quadros, audio, i, out, tmp_dir, trilha)

        log("\n" + "=" * 60)
        log(f"CONCLUÍDO! {len(partes_audio)} vídeos em:")
        log(f"  {OUTPUT_DIR}")
        for f in sorted(OUTPUT_DIR.glob("*.mp4")):
            mb = f.stat().st_size / 1024 / 1024
            log(f"  {f.name} — {mb:.0f} MB")
        log("=" * 60)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
