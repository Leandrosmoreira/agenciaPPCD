#!/usr/bin/env python3
"""
Prometheus Transições — Montador com transições estilo CapCut
Usa FFmpeg puro (zoompan + xfade) — sem problemas de memória RAM

Transições disponíveis:
  fade, fadeblack, fadewhite, wipeleft, wiperight,
  slideleft, slideright, dissolve, zoomin, random

Uso:
  python prometheus_moviepy.py --canal sinais-do-fim --video video-007-falsa-paz
  python prometheus_moviepy.py --canal sinais-do-fim --video video-007-falsa-paz --transition slideleft --min-duration 7
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

# Transições FFmpeg xfade disponíveis
TRANSITIONS = ["fade", "fadeblack", "wipeleft", "wiperight", "slideleft", "slideright", "dissolve", "zoomin"]
KEN_BURNS = ["zoom_in", "zoom_out", "pan_left", "pan_right", "pan_up", "pan_down"]


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] PROMETHEUS-TR > {msg}", flush=True)


def write_log(log_path: Path, msg: str):
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {msg}\n")
    except:
        pass


# ─── FFmpeg helpers ────────────────────────────────────────────────────────

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


def merge_files(files: list, tmp_dir: Path, name: str) -> Path:
    if len(files) == 1:
        return files[0]
    lst = tmp_dir / f"{name}_list.txt"
    with open(lst, "w") as f:
        for fp in files:
            f.write(f"file '{fp.resolve()}'\n")
    out = tmp_dir / f"{name}.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(out)],
                   capture_output=True, check=True)
    return out


def detect_silences(audio_path: Path, threshold_db=-35, min_dur=0.8):
    cmd = ["ffmpeg", "-i", str(audio_path),
           "-af", f"silencedetect=noise={threshold_db}dB:d={min_dur}",
           "-f", "null", "-"]
    out = subprocess.run(cmd, capture_output=True, text=True).stderr
    pauses, start = [], None
    for line in out.split("\n"):
        if "silence_start" in line:
            try: start = float(line.split("silence_start: ")[1])
            except: pass
        elif "silence_end" in line and start is not None:
            try:
                end = float(line.split("silence_end: ")[1].split(" | ")[0])
                pauses.append((start + end) / 2)
                start = None
            except: pass
    return pauses


# ─── Ken Burns via FFmpeg zoompan ─────────────────────────────────────────

def build_zoompan_filter(effect: str, duration: float, w=WIDTH, h=HEIGHT) -> str:
    fps = FPS
    frames = int(duration * fps)

    if effect == "zoom_in":
        return (f"zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                f":d={frames}:s={w}x{h}:fps={fps}")
    elif effect == "zoom_out":
        return (f"zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                f":d={frames}:s={w}x{h}:fps={fps}")
    elif effect == "pan_left":
        return (f"zoompan=z='1.15':x='iw*0.15*(on/{frames})':y='ih/2-(ih/zoom/2)'"
                f":d={frames}:s={w}x{h}:fps={fps}")
    elif effect == "pan_right":
        return (f"zoompan=z='1.15':x='iw*0.15*(1-on/{frames})':y='ih/2-(ih/zoom/2)'"
                f":d={frames}:s={w}x{h}:fps={fps}")
    elif effect == "pan_up":
        return (f"zoompan=z='1.15':x='iw/2-(iw/zoom/2)':y='ih*0.15*(on/{frames})'"
                f":d={frames}:s={w}x{h}:fps={fps}")
    elif effect == "pan_down":
        return (f"zoompan=z='1.15':x='iw/2-(iw/zoom/2)':y='ih*0.15*(1-on/{frames})'"
                f":d={frames}:s={w}x{h}:fps={fps}")
    else:
        return (f"zoompan=z='1':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                f":d={frames}:s={w}x{h}:fps={fps}")


def generate_ken_burns_clip(img_path: Path, duration: float, effect: str, out_path: Path):
    """Gera clip Ken Burns com FFmpeg zoompan."""
    zp = build_zoompan_filter(effect, duration)
    vf = f"scale={WIDTH*2}:{HEIGHT*2},format=yuv420p,{zp},scale={WIDTH}:{HEIGHT},setsar=1"
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(img_path),
        "-vf", vf,
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-r", str(FPS), "-an",
        str(out_path)
    ], capture_output=True, check=True)


def apply_xfade(clip_a: Path, clip_b: Path, transition: str,
                td: float, out_path: Path):
    """Aplica transição xfade entre dois clips com FFmpeg."""
    dur_a = get_duration(clip_a)
    offset = max(0.01, dur_a - td)

    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(clip_a), "-i", str(clip_b),
        "-filter_complex",
        f"[0:v][1:v]xfade=transition={transition}:duration={td}:offset={offset:.3f}[v]",
        "-map", "[v]",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-r", str(FPS), "-an",
        str(out_path)
    ], capture_output=True, check=True)


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Prometheus Transicoes - Ken Burns + xfade")
    parser.add_argument("--canal", required=True)
    parser.add_argument("--video", required=True)
    parser.add_argument("--transition", default="random",
                        choices=TRANSITIONS + ["random"])
    parser.add_argument("--transition-duration", type=float, default=0.6)
    parser.add_argument("--min-duration", type=float, default=7.0,
                        help="Duracao minima por imagem em segundos (padrao: 7)")
    parser.add_argument("--music-volume", type=float, default=0.25)
    parser.add_argument("--no-sync-pauses", action="store_true")
    parser.add_argument("--output", default="video_montagem_mv.mp4")
    args = parser.parse_args()

    video_dir = BASE_DIR / "canais" / args.canal / "videos" / args.video
    img_dir = video_dir / "6-assets" / "imagens"
    audio_dir = video_dir / "6-assets" / "audio_suno"
    output_dir = video_dir / "7-edicao"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / args.output
    log_path = BASE_DIR / "canais" / args.canal / "_config" / "pipeline.log"

    log(f"Canal: {args.canal} | Video: {args.video} | Transicao: {args.transition} | Min: {args.min_duration}s")

    # ── Imagens ────────────────────────────────────────────────────────────
    images = sorted(
        [f for f in img_dir.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS],
        key=lambda f: f.name)
    if not images:
        log(f"ERRO: Nenhuma imagem em {img_dir}")
        sys.exit(1)
    log(f"Imagens disponiveis: {len(images)}")

    # ── Áudios ─────────────────────────────────────────────────────────────
    mk = ["trilha", "music", "instrumental"]
    narr = sorted([f for f in audio_dir.iterdir()
                   if f.suffix.lower() in AUDIO_EXTENSIONS
                   and not any(k in f.name.lower() for k in mk)], key=lambda f: f.name)
    music = sorted([f for f in audio_dir.iterdir()
                    if f.suffix.lower() in AUDIO_EXTENSIONS
                    and any(k in f.name.lower() for k in mk)], key=lambda f: f.name)
    log(f"Narracoes: {len(narr)} | Trilhas: {len(music)}")

    tmp_dir = Path(tempfile.mkdtemp(prefix="prometheus_tr_"))
    log(f"Temp: {tmp_dir}")

    try:
        # ── Merge narração ─────────────────────────────────────────────────
        if narr:
            merged_narr = merge_files(narr, tmp_dir, "narration")
            total_dur = get_duration(merged_narr)
            log(f"Duracao audio: {total_dur:.1f}s")
        else:
            merged_narr = None
            total_dur = 0

        # ── Pausas ─────────────────────────────────────────────────────────
        if merged_narr and not args.no_sync_pauses:
            pauses = [p for p in detect_silences(merged_narr) if p > 5.0]
            log(f"Pausas validas: {len(pauses)}")
            for i, p in enumerate(pauses):
                m, s = divmod(p, 60)
                log(f"  Pausa {i+1}: {int(m)}:{s:05.2f}")
        else:
            pauses = []

        # ── Limitar e distribuir imagens ───────────────────────────────────
        MIN_DUR = args.min_duration
        MAX_DUR = MIN_DUR + 3.0

        if total_dur > 0:
            max_imgs = int(total_dur / MIN_DUR)
            if len(images) > max_imgs:
                log(f"Selecionando {max_imgs} de {len(images)} imagens")
                step = len(images) / max_imgs
                images = [images[int(i * step)] for i in range(max_imgs)]

        if pauses and total_dur > 0:
            cut_points = [0.0] + pauses + [total_dur]
            segments = len(cut_points) - 1
            base = max(1, len(images) // segments)
            durations, idx = [], 0
            for seg in range(segments):
                seg_dur = cut_points[seg+1] - cut_points[seg]
                n = base if seg < segments - 1 else max(1, len(images) - idx)
                d = max(MIN_DUR, min(MAX_DUR, seg_dur / max(1, n)))
                for _ in range(n):
                    if idx < len(images):
                        durations.append(d)
                        idx += 1
            while idx < len(images):
                durations.append(MIN_DUR)
                idx += 1
        else:
            d = max(MIN_DUR, total_dur / len(images)) if total_dur > 0 else MIN_DUR
            durations = [d] * len(images)

        log(f"Imagens: {len(images)} | Duracao media: {sum(durations)/len(durations):.1f}s")

        # ── Gerar clips Ken Burns ──────────────────────────────────────────
        log("Gerando clips Ken Burns...")
        td = args.transition_duration
        kb_paths = []
        edit_log = []
        current_ts = 0.0

        for i, (img_path, dur) in enumerate(zip(images, durations)):
            effect = KEN_BURNS[i % len(KEN_BURNS)]
            pct = int((i + 1) / len(images) * 100)
            log(f"  [{pct:3d}%] {i+1}/{len(images)}: {img_path.name} ({dur:.1f}s, {effect})")

            kb_path = tmp_dir / f"kb_{i:03d}.mp4"
            generate_ken_burns_clip(img_path, dur, effect, kb_path)
            kb_paths.append(kb_path)

            ts_m, ts_s = divmod(current_ts, 60)
            edit_log.append({
                "index": i + 1,
                "timestamp": f"{int(ts_m):02d}:{ts_s:05.2f}",
                "image": img_path.name,
                "effect": effect,
                "duration_s": round(dur, 1),
            })
            current_ts += dur

        # ── Aplicar transições xfade sequencialmente ───────────────────────
        log(f"Aplicando transicoes xfade ({args.transition})...")
        merged = kb_paths[0]

        for i in range(1, len(kb_paths)):
            t_type = args.transition if args.transition != "random" else random.choice(TRANSITIONS)
            edit_log[i]["transition_in"] = t_type
            out_merge = tmp_dir / f"merged_{i:03d}.mp4"
            pct = int(i / (len(kb_paths) - 1) * 100)
            log(f"  [{pct:3d}%] Transicao {i}/{len(kb_paths)-1}: {t_type}")
            apply_xfade(merged, kb_paths[i], t_type, td, out_merge)
            merged = out_merge

        edit_log[0]["transition_in"] = "inicio"
        video_only = merged
        log(f"Video base: {get_duration(video_only):.1f}s")

        # ── Áudio ──────────────────────────────────────────────────────────
        if merged_narr:
            log("Mixando audio...")
            audio_out = tmp_dir / "final_audio.mp3"

            if music:
                merged_music = merge_files(music, tmp_dir, "music")
                video_dur = get_duration(video_only)
                music_dur = get_duration(merged_music)

                # Loop da trilha se necessário
                if music_dur < video_dur:
                    n = int(video_dur / music_dur) + 2
                    loop_list = tmp_dir / "loop_list.txt"
                    with open(loop_list, "w") as f:
                        for _ in range(n):
                            f.write(f"file '{merged_music.resolve()}'\n")
                    looped = tmp_dir / "music_looped.mp3"
                    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                                    "-i", str(loop_list), "-c", "copy", str(looped)],
                                   capture_output=True)
                    merged_music = looped

                # Mixar narração + trilha com volume
                subprocess.run([
                    "ffmpeg", "-y",
                    "-i", str(merged_narr),
                    "-i", str(merged_music),
                    "-filter_complex",
                    f"[1:a]volume={args.music_volume},afade=t=in:d=2,afade=t=out:st={video_dur-4}:d=4[music];"
                    f"[0:a][music]amix=inputs=2:duration=first[aout]",
                    "-map", "[aout]",
                    "-t", str(video_dur),
                    str(audio_out)
                ], capture_output=True, check=True)
            else:
                audio_out = merged_narr

            # Combinar vídeo + áudio
            log(f"Combinando video + audio -> {output_path.name}")
            subprocess.run([
                "ffmpeg", "-y",
                "-i", str(video_only),
                "-i", str(audio_out),
                "-c:v", "libx264", "-crf", "23", "-preset", "medium",
                "-c:a", "aac", "-b:a", "192k",
                "-r", str(FPS), "-shortest",
                str(output_path)
            ], check=True)
        else:
            subprocess.run([
                "ffmpeg", "-y", "-i", str(video_only),
                "-c:v", "libx264", "-crf", "23", "-preset", "medium",
                "-r", str(FPS), str(output_path)
            ], check=True)

        # ── Log detalhado de edição ────────────────────────────────────────
        size_mb = output_path.stat().st_size / 1024 / 1024
        dur_final = get_duration(output_path)

        log_edit_path = output_dir / (output_path.stem + "_edit_log.txt")
        from collections import Counter
        with open(log_edit_path, "w", encoding="utf-8") as f:
            f.write(f"PROMETHEUS — Log de Edicao Detalhado\n")
            f.write(f"Video: {args.canal}/{args.video}\n")
            f.write(f"Output: {args.output} | Duracao: {dur_final:.0f}s | Tamanho: {size_mb:.0f}MB\n")
            f.write(f"Imagens: {len(images)} | Transicao: {args.transition}\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"{'#':<4} {'TIMESTAMP':<10} {'IMAGEM':<12} {'DUR':<6} {'EFEITO KB':<16} TRANSICAO\n")
            f.write("-" * 70 + "\n")
            for e in edit_log:
                f.write(f"{e['index']:<4} {e['timestamp']:<10} {e['image']:<12} "
                        f"{str(e['duration_s'])+'s':<6} {e['effect']:<16} {e.get('transition_in','')}\n")
            f.write("\n" + "=" * 70 + "\n")
            effects_c = Counter(e["effect"] for e in edit_log)
            trans_c = Counter(e.get("transition_in") for e in edit_log if e.get("transition_in") != "inicio")
            f.write("Efeitos Ken Burns:\n")
            for k, v in sorted(effects_c.items(), key=lambda x: -x[1]):
                f.write(f"  {k}: {v}x\n")
            f.write("Transicoes:\n")
            for k, v in sorted(trans_c.items(), key=lambda x: -x[1]):
                f.write(f"  {k}: {v}x\n")

        log(f"Edit log salvo: {log_edit_path.name}")
        log("=" * 55)
        log(f"Concluido! {output_path.name}")
        log(f"Duracao: {dur_final:.0f}s | Tamanho: {size_mb:.0f} MB")
        log(f"Imagens: {len(images)} | Transicoes: {len(images)-1}")
        log("=" * 55)

        write_log(log_path, f"PROMETHEUS-TR concluido -> {args.output} ({dur_final:.0f}s, {size_mb:.0f}MB)")

    finally:
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
