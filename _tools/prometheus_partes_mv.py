#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prometheus Partes — FFmpeg puro, crop:eval=frame
Ken Burns: crop animado por frame (sem zoompan, sem PIL, sem buffer)
Transicoes: xfade

Uso:
  python prometheus_partes_mv.py --canal sinais-do-fim --video video-007-falsa-paz
  python prometheus_partes_mv.py ... --parts 1
  python prometheus_partes_mv.py ... --transition fade
"""

import argparse
import json
import random
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

BASE_DIR        = Path(__file__).resolve().parent.parent
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg"}
WIDTH, HEIGHT   = 1920, 1080
FPS             = 30
TRANS_DUR       = 0.5   # segundos de transicao
MIN_DUR         = 7.0   # duracao minima por imagem

KEN_BURNS = ["zoom_in", "zoom_out", "pan_left", "pan_right"]

XFADE_TRANSITIONS = [
    "fade", "fadeblack", "fadewhite",
    "wipeleft", "wiperight",
    "slideleft", "slideright",
    "smoothleft", "smoothright",
    "dissolve", "pixelize",
    "radial", "circleopen", "circleclose",
    "hblur", "zoomin",
]


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] > {msg}", flush=True)


def get_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_streams", str(path)],
        capture_output=True, text=True
    )
    try:
        for s in json.loads(r.stdout).get("streams", []):
            if "duration" in s:
                return float(s["duration"])
    except Exception:
        pass
    return 0.0


def make_kb_clip(img_path: Path, duration: float, effect: str, out: Path) -> bool:
    """
    Pass 1: Ken Burns via PIL frame-a-frame -> pipe stdin -> FFmpeg.
    Zoom suave com float preciso, sem buffer, sem OOM.
    stderr=DEVNULL evita deadlock de pipe.
    """
    import gc
    try:
        from PIL import Image
    except ImportError:
        log("ERRO: pip install Pillow")
        return False

    w, h         = WIDTH, HEIGHT
    total_frames = int(duration * FPS)

    # Pre-processar imagem base
    with Image.open(img_path) as raw:
        img = raw.convert("RGB")
        iw, ih = img.size
        # crop para aspect ratio 16:9
        target = w / h
        if iw / ih > target:
            nw = int(ih * target)
            img = img.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
        elif iw / ih < target:
            nh = int(iw / target)
            img = img.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
        base = img.resize((w, h), Image.LANCZOS)

    # Pre-computar canvas largo para pan
    if effect in ("pan_left", "pan_right"):
        extra = int(w * 0.15)
        wide  = base.resize((w + extra, h), Image.BILINEAR)
    else:
        wide = None

    base_arr = None  # lazy convert

    proc = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{w}x{h}", "-pix_fmt", "rgb24",
        "-r", str(FPS), "-i", "pipe:0",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-an", str(out),
    ], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        import numpy as np
        for fn in range(total_frames):
            p = fn / max(1, total_frames - 1)  # 0.0 -> 1.0

            if effect == "zoom_in":
                scale  = 1.0 + 0.18 * p
                nw, nh = int(w * scale), int(h * scale)
                frame_img = base.resize((nw, nh), Image.BILINEAR)
                x, y  = (nw - w) // 2, (nh - h) // 2
                frame = np.array(frame_img)[y:y+h, x:x+w]

            elif effect == "zoom_out":
                scale  = 1.18 - 0.18 * p
                nw, nh = max(w, int(w * scale)), max(h, int(h * scale))
                frame_img = base.resize((nw, nh), Image.BILINEAR)
                x, y  = (nw - w) // 2, (nh - h) // 2
                frame = np.array(frame_img)[y:y+h, x:x+w]

            elif effect == "pan_left":
                ex    = wide.size[0] - w
                x     = int(ex * p)
                frame = np.array(wide)[:, x:x+w]

            elif effect == "pan_right":
                ex    = wide.size[0] - w
                x     = int(ex * (1.0 - p))
                frame = np.array(wide)[:, x:x+w]

            else:
                if base_arr is None:
                    base_arr = np.array(base)
                frame = base_arr

            proc.stdin.write(frame.tobytes())

    finally:
        proc.stdin.close()
        proc.wait()

    del wide, base, base_arr
    gc.collect()

    if proc.returncode != 0:
        log(f"    ERRO FFmpeg clip {img_path.name} (code {proc.returncode})")
        return False
    return True


def combine_xfade(clips: list, audio_path: Path, out_path: Path,
                  img_dur: float, audio_dur: float,
                  force_tr: str | None,
                  edit_log: list, part_name: str,
                  img_names: list, effects: list) -> bool:
    """Pass 2: xfade chain + audio."""
    n = len(clips)
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for clip in clips:
        cmd += ["-i", str(clip)]
    cmd += ["-i", str(audio_path)]

    if n == 1:
        fc = "[0:v]copy[vfinal]"
    else:
        parts = []
        prev  = "0:v"
        for i in range(1, n):
            tr     = force_tr if force_tr else random.choice(XFADE_TRANSITIONS)
            offset = i * img_dur
            label  = f"x{i:02d}"
            parts.append(
                f"[{prev}][{i}:v]xfade=transition={tr}"
                f":duration={TRANS_DUR}:offset={offset:.3f}[{label}]"
            )
            edit_log.append({
                "part":       part_name,
                "img_a":      img_names[i - 1],
                "img_b":      img_names[i],
                "effect_a":   effects[i - 1],
                "effect_b":   effects[i],
                "transition": tr,
                "offset_s":   round(offset, 3),
            })
            prev = label
        parts.append(f"[{prev}]copy[vfinal]")
        fc = ";".join(parts)

    cmd += [
        "-filter_complex", fc,
        "-map", "[vfinal]",
        "-map", f"{n}:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{audio_dur:.3f}",
        str(out_path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        log(f"  ERRO xfade:\n{r.stderr[-500:]}")
        return False
    return True


def build_part(images: list, audio_path: Path, out_path: Path,
               force_tr: str | None, edit_log: list) -> bool:
    n         = len(images)
    audio_dur = get_duration(audio_path)

    # Limitar imagens ao necessario
    max_imgs = max(1, int(audio_dur / MIN_DUR))
    if n > max_imgs:
        images = images[:max_imgs]
        n      = len(images)

    img_dur  = audio_dur / n
    clip_dur = img_dur + TRANS_DUR   # margem de saida para xfade

    log(f"  {n} imgs x {img_dur:.1f}s = {audio_dur:.1f}s")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp     = Path(tmpdir)
        clips   = []
        effects = []
        names   = []

        # Pass 1: clip por imagem
        for i, img in enumerate(images):
            ef  = random.choice(KEN_BURNS)
            out = tmp / f"clip_{i:03d}.mp4"
            effects.append(ef)
            names.append(img.name)
            log(f"  [{i+1}/{n}] {img.name} ({ef})")
            if not make_kb_clip(img, clip_dur, ef, out):
                return False
            clips.append(out)

        # Pass 2: xfade + audio
        log(f"  Combinando {n} clips...")
        ok = combine_xfade(
            clips, audio_path, out_path,
            img_dur, audio_dur,
            force_tr, edit_log, out_path.stem, names, effects
        )

    if ok:
        mb = out_path.stat().st_size / 1024 / 1024
        log(f"  OK -> {out_path.name} ({mb:.0f} MB)")
    return ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--canal",      required=True)
    parser.add_argument("--video",      required=True)
    parser.add_argument("--transition", default=None)
    parser.add_argument("--parts",      nargs="+", type=int)
    args = parser.parse_args()

    video_dir  = BASE_DIR / "canais" / args.canal / "videos" / args.video
    audio_dir  = video_dir / "6-assets" / "audio_suno"
    img_dir    = video_dir / "6-assets" / "imagens"
    out_dir    = video_dir / "7-edicao" / "partes"
    out_dir.mkdir(parents=True, exist_ok=True)

    audios = sorted([f for f in audio_dir.iterdir()
                     if f.suffix in AUDIO_EXTENSIONS and f.stem.startswith("parte")])
    images = sorted([f for f in img_dir.iterdir()
                     if f.suffix in IMAGE_EXTENSIONS])

    if not audios:
        log("ERRO: nenhum audio em " + str(audio_dir)); sys.exit(1)
    if not images:
        log("ERRO: nenhuma imagem em " + str(img_dir)); sys.exit(1)

    n_parts      = len(audios)
    parts_to_run = args.parts if args.parts else list(range(1, n_parts + 1))

    log(f"Canal: {args.canal} | Video: {args.video} | Transicao: {args.transition or 'random'}")
    log(f"Imagens: {len(images)} | Partes: {n_parts}")
    if args.parts:
        log(f"Gerando: partes {parts_to_run}")

    # Distribuir imagens proporcionalmente
    base, rem = divmod(len(images), n_parts)
    dist, idx = [], 0
    for p in range(n_parts):
        cnt = base + (1 if p < rem else 0)
        dist.append(images[idx:idx + cnt])
        idx += cnt
    log(f"Distribuicao: {[len(d) for d in dist]} imgs/parte\n")

    edit_log = []
    for p_idx, audio in enumerate(audios, 1):
        if p_idx not in parts_to_run:
            continue
        print(f"=== PARTE {p_idx}/{n_parts}: {audio.name} ===")
        out_path = out_dir / f"video_parte{p_idx:02d}.mp4"
        build_part(dist[p_idx - 1], audio, out_path, args.transition, edit_log)

    if edit_log:
        log_path = out_dir / "edit_log.json"
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(edit_log, f, ensure_ascii=False, indent=2)
        log(f"Log: {log_path.name}")

    print("\nCONCLUIDO!")
    for f in sorted(out_dir.glob("video_parte*.mp4")):
        mb = f.stat().st_size / 1024 / 1024
        if mb > 1:
            print(f"  {f.name} — {mb:.0f} MB")
        else:
            print(f"  {f.name} — {f.stat().st_size} bytes (ERRO)")


if __name__ == "__main__":
    main()
