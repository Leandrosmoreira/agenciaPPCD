# video-015-economist-manipulacao — Montagem v2 (Veo3 + PNG hibrido)
# Abismo Criativo — gerado em 2026-04-18
#
# ARQUITETURA RAM-SAFE:
#   1. Para cada quadro: renderiza UM clip de 8s em arquivo temp_clip_NN.mp4
#      - Fecha TUDO e gc entre clips (nunca 2 clips abertos ao mesmo tempo)
#      - PNG -> MoviePy Ken Burns + grade + vignette
#      - Veo3 MP4 -> ffmpeg direto com scale+eq+vignette (sem MoviePy)
#   2. Concat com crossfade 0.5s via ffmpeg xfade
#   3. Mix narracao + trilha vol=0.22 via ffmpeg
#
# Uso:
#   python _tools/montagem_v2_video-015.py --parte 1

import argparse
import gc
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT       = Path(__file__).resolve().parent.parent
VIDEO_DIR  = ROOT / "canais" / "sinais-do-fim" / "videos" / "video-015-economist-manipulacao"
ASSETS     = VIDEO_DIR / "6-assets"
VEO3_DIR   = ASSETS / "veo3"
AUDIO_DIR  = VIDEO_DIR / "5-audio"
OUT_DIR    = VIDEO_DIR / "7-edicao" / "partes"

FPS         = 30
W, H        = 1920, 1080
CLIP_DUR    = 8.0
CROSSFADE   = 0.5

BRIGHTNESS = 0.90
CONTRAST   = 1.15
VIG_STR    = 0.55
TRILHA_VOL = 0.22

QUADROS_POR_PARTE = {
    1: list(range(1, 12)),    # Q01-Q11
    2: list(range(12, 23)),   # Q12-Q22
    3: list(range(23, 34)),   # Q23-Q33
    4: list(range(34, 45)),   # Q34-Q44
    5: list(range(45, 56)),   # Q45-Q55
    6: list(range(56, 67)),   # Q56-Q66
    7: list(range(67, 78)),   # Q67-Q77
    8: list(range(78, 89)),   # Q78-Q88
    9: list(range(89, 99)),   # Q89-Q98
}

KB_DIRECTIONS = [
    "zoom_in", "pan_left", "zoom_in", "zoom_in_extreme", "pan_right",
    "zoom_out", "pan_left", "zoom_in", "pan_right", "zoom_out",
    "zoom_in", "pan_left", "zoom_out",
]

# ==============================================================================
# RENDER DE 1 CLIP PNG (MoviePy isolado com close/gc ao fim)
# ==============================================================================

def render_clip_png(png_path: Path, direction: str, out_path: Path, dur: float = CLIP_DUR):
    """Renderiza 1 PNG com Ken Burns + grade + vignette em arquivo mp4 independente."""
    from moviepy.editor import ImageClip, VideoClip

    base = ImageClip(str(png_path)).resize((W, H)).set_duration(dur)
    w, h = base.size
    zoom_ratio = 0.15

    def _make(scale_fn):
        def mf(t):
            import cv2
            p = t / dur
            s = scale_fn(p)
            nw, nh = int(w * s), int(h * s)
            img = base.get_frame(t)
            r = cv2.resize(img, (nw, nh))
            x, y = (nw - w) // 2, (nh - h) // 2
            return r[y:y+h, x:x+w]
        return mf

    def _pan(scale_fixed, x_fn):
        def mf(t):
            import cv2
            p = t / dur
            nw, nh = int(w * scale_fixed), int(h * scale_fixed)
            img = base.get_frame(t)
            r = cv2.resize(img, (nw, nh))
            xo = x_fn(p, nw, w)
            y = (nh - h) // 2
            return r[y:y+h, xo:xo+w]
        return mf

    if direction == "zoom_in":
        mf = _make(lambda p: 1.0 + zoom_ratio * p)
    elif direction == "zoom_out":
        mf = _make(lambda p: (1.0 + zoom_ratio) - zoom_ratio * p)
    elif direction == "zoom_in_extreme":
        zr = zoom_ratio * 1.5
        mf = _make(lambda p: 1.0 + zr * p)
    elif direction == "pan_left":
        sf = 1.0 + zoom_ratio * 0.5
        mf = _pan(sf, lambda p, nw, w_: int((nw - w_) * p))
    elif direction == "pan_right":
        sf = 1.0 + zoom_ratio * 0.5
        mf = _pan(sf, lambda p, nw, w_: int((nw - w_) * (1.0 - p)))
    else:
        mf = _make(lambda p: 1.0 + zoom_ratio * p)

    # LUT grade (uma vez por clip)
    idx = np.arange(256, dtype=np.float32)
    b = np.clip((idx - 128) * CONTRAST * BRIGHTNESS + 128 * BRIGHTNESS, 0, 255).astype(np.uint8)
    lr = np.clip(b.astype(np.float32) * 0.98, 0, 255).astype(np.uint8)
    lg = b
    lb = np.clip(b.astype(np.float32) * 1.01, 0, 255).astype(np.uint8)

    def final_mf(t):
        f = mf(t)
        # grade in-place via LUT uint8 — SEM float32 intermediario (RAM-safe)
        out = np.empty_like(f)
        out[:, :, 0] = lr[f[:, :, 0]]
        out[:, :, 1] = lg[f[:, :, 1]]
        out[:, :, 2] = lb[f[:, :, 2]]
        return out

    # Renderiza clip SEM vignette (evita OOM float32); vignette aplicado via ffmpeg depois
    raw_path = out_path.with_suffix(".raw.mp4")
    clip = VideoClip(final_mf, duration=dur).set_fps(FPS)
    clip.write_videofile(
        str(raw_path),
        fps=FPS, codec="libx264",
        audio=False, preset="ultrafast", bitrate="6000k",
        threads=1, ffmpeg_params=["-refs","1","-bf","0"],
        verbose=False, logger=None,
    )
    clip.close()
    base.close()
    del clip, base, mf, final_mf
    gc.collect()

    # Aplica vignette via ffmpeg (sem pressao de RAM Python)
    r = subprocess.run([
        "ffmpeg", "-y",
        "-threads", "1",        # limita decode buffers (evita get_buffer OOM)
        "-i", str(raw_path),
        "-an",
        "-vf", "vignette=angle=PI/4",
        "-c:v", "libx264", "-preset", "ultrafast", "-b:v", "5000k",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-threads", "1",
        str(out_path),
    ], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[ERRO ffmpeg vignette PNG] raw={raw_path} exists={raw_path.exists()} size={raw_path.stat().st_size if raw_path.exists() else 'N/A'}\n--- STDERR ---\n{r.stderr[-3000:]}")
        sys.exit(1)
    raw_path.unlink(missing_ok=True)


# ==============================================================================
# RENDER DE 1 CLIP VEO3 (ffmpeg direto, sem MoviePy)
# ==============================================================================

def render_clip_veo(veo_path: Path, out_path: Path, dur: float = CLIP_DUR):
    """
    Processa Veo3 via ffmpeg: trim/estende p/ dur + eq (grade) + vignette.
    Veo3 nativo = 8s. Se dur < 8: corta. Se dur > 8: congela ultimo frame.
    """
    VEO_NATIVE = 8.0
    grade = "eq=brightness=-0.10:contrast=1.15:saturation=0.95,vignette=angle=PI/4"

    if dur <= VEO_NATIVE:
        vf = grade
        t_arg = ["-t", f"{dur:.3f}"]
    else:
        # Congela ultimo frame pelo tempo extra
        pad = dur - VEO_NATIVE
        vf = f"tpad=stop_mode=clone:stop_duration={pad:.3f},{grade}"
        t_arg = ["-t", f"{dur:.3f}"]

    cmd = [
        "ffmpeg", "-y",
        "-i", str(veo_path),
        *t_arg,
        "-an",
        "-vf", vf,
        "-r", str(FPS),
        "-c:v", "libx264", "-preset", "ultrafast", "-b:v", "6000k",
        "-pix_fmt", "yuv420p",
        str(out_path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[ERRO ffmpeg Veo3]\n{r.stderr[-800:]}")
        sys.exit(1)


# ==============================================================================
# CONCAT + CROSSFADE VIA FFMPEG XFADE (lotes de 5 — RAM-safe)
# ==============================================================================

BATCH_SIZE = 5  # max clips por lote de xfade


def _xfade_cascade(clip_paths: list, clip_durs: list, out_path: Path, bv_final: str = "2000k"):
    """Une N clips com xfade em cascata par-a-par. N deve ser <= BATCH_SIZE."""
    n = len(clip_paths)
    if n == 1:
        shutil.copy(clip_paths[0], out_path)
        return clip_durs[0]

    tmp_dir = out_path.parent / f".xc_{out_path.stem}"
    tmp_dir.mkdir(exist_ok=True)

    current = Path(clip_paths[0])
    current_dur = clip_durs[0]

    for i in range(1, n):
        next_clip = Path(clip_paths[i])
        is_last = (i == n - 1)
        step_out = out_path if is_last else tmp_dir / f"step_{i:02d}.mp4"
        offset = current_dur - CROSSFADE
        bv = bv_final if is_last else "1500k"

        cmd = [
            "ffmpeg", "-y",
            "-i", str(current),
            "-i", str(next_clip),
            "-filter_complex",
            f"[0:v][1:v]xfade=transition=fade:duration={CROSSFADE}:offset={offset:.2f}[vout]",
            "-map", "[vout]",
            "-c:v", "libx264", "-preset", "ultrafast", "-b:v", bv,
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(step_out),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"[ERRO xfade i={i}] offset={offset:.2f}\n{r.stderr[-2000:]}")
            sys.exit(1)

        if current != Path(clip_paths[0]) and current.exists():
            try: current.unlink()
            except: pass
        current = step_out
        current_dur += clip_durs[i] - CROSSFADE

    shutil.rmtree(tmp_dir, ignore_errors=True)
    return current_dur


def concat_with_xfade(clip_paths: list, clip_durs: list, out_path: Path):
    """Xfade em lotes de BATCH_SIZE — suporta longas partes sem OOM."""
    n = len(clip_paths)
    if n == 1:
        shutil.copy(clip_paths[0], out_path)
        return clip_durs[0]

    # Diagnostico: verificar existencia e tamanho de cada clip
    for i, cp in enumerate(clip_paths):
        p = Path(cp)
        sz = p.stat().st_size if p.exists() else -1
        print(f"  [diag] clip_{i:02d}: exists={p.exists()} size={sz//1024}KB path={p.name}")

    if n <= BATCH_SIZE:
        return _xfade_cascade(clip_paths, clip_durs, out_path, bv_final="6000k")

    # Dividir em lotes, unir resultados dos lotes no final
    tmp_dir = out_path.parent / f".batches_{out_path.stem}"
    tmp_dir.mkdir(exist_ok=True)

    batch_files = []
    batch_durs  = []
    for start in range(0, n, BATCH_SIZE):
        end    = min(start + BATCH_SIZE, n)
        b_out  = tmp_dir / f"batch_{start:02d}.mp4"
        b_dur  = _xfade_cascade(clip_paths[start:end], clip_durs[start:end], b_out, bv_final="2000k")
        batch_files.append(str(b_out))
        batch_durs.append(b_dur)

    # Une os poucos lotes resultantes (sem OOM)
    total = _xfade_cascade(batch_files, batch_durs, out_path, bv_final="6000k")
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return total


# ==============================================================================
# MAIN POR PARTE
# ==============================================================================

def get_audio_duration(audio_path: Path) -> float:
    """Retorna duracao em segundos via ffprobe."""
    r = subprocess.run(
        ["ffprobe","-v","quiet","-show_entries","format=duration","-of","csv=p=0", str(audio_path)],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())


def distribute_durations(audio_dur: float, n_clips: int) -> list:
    """
    Distribui audio_dur entre n_clips com regra:
    - Cada clip teto 8s, minimo ok
    - Se n_clips * 8 < audio_dur: ultimos clips esticam (congelam frame final)
    - Inclui compensacao de CROSSFADE: total visivel = sum(durs) - (n-1)*CROSSFADE
    """
    if n_clips == 0:
        return []
    # total_visivel desejado = audio_dur
    # sum(durs) - (n-1)*CROSSFADE = audio_dur
    # => sum(durs) = audio_dur + (n-1)*CROSSFADE
    sum_durs = audio_dur + (n_clips - 1) * CROSSFADE
    base = sum_durs / n_clips

    if base <= CLIP_DUR:
        # Todos iguais, dentro do teto
        return [round(base, 3)] * n_clips

    # base > 8s: distribuir 8s para (n-1) clips, ultimo absorve o resto
    # Mas Snayder disse "teto 8s" — ultimo estica (congela Veo3 ou ImageClip maior)
    durs = [CLIP_DUR] * (n_clips - 1)
    last = sum_durs - CLIP_DUR * (n_clips - 1)
    durs.append(round(last, 3))
    return durs


def render_parte(parte: int):
    if parte not in QUADROS_POR_PARTE:
        print(f"[ERRO] Parte {parte} invalida. Use 1-9.")
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    quadros = QUADROS_POR_PARTE[parte]

    # Medir audio da narracao para calcular duracoes
    narr_path = AUDIO_DIR / f"parte{parte}.mp3"
    if not narr_path.exists():
        print(f"[ERRO] Narracao nao encontrada: {narr_path}")
        sys.exit(1)
    audio_dur = get_audio_duration(narr_path)
    clip_durs = distribute_durations(audio_dur, len(quadros))

    print(f"\n{'='*60}")
    print(f"MONTAGEM v2 — video-015 — PARTE {parte}")
    print(f"Quadros: Q{quadros[0]:02d}-Q{quadros[-1]:02d} ({len(quadros)} clips)")
    print(f"Audio: {narr_path.name} = {audio_dur:.2f}s")
    print(f"Duracoes por clip: {[f'{d:.2f}s' for d in clip_durs]}")
    print(f"Total visivel (com xfade): {sum(clip_durs) - (len(quadros)-1)*CROSSFADE:.2f}s")
    print(f"{'='*60}")

    tmp_dir = Path(tempfile.mkdtemp(prefix=f"montagem_p{parte}_"))
    clip_paths = []
    final_durs = []

    # 1. Render clip-a-clip em arquivos temp
    print(f"\n[1/3] Renderizando {len(quadros)} clips individuais em {tmp_dir}...")
    for i, q in enumerate(quadros):
        idx_global = sum(len(QUADROS_POR_PARTE[p]) for p in range(1, parte)) + i
        veo_path = VEO3_DIR / f"VEO_Q{q:02d}.mp4"
        png_path = ASSETS   / f"Q{q:02d}.png"
        tmp_clip = tmp_dir / f"clip_{i:02d}.mp4"
        dur = clip_durs[i]

        if veo_path.exists():
            print(f"  [{i+1}/{len(quadros)}] Q{q:02d}: VEO3 -> ffmpeg grade+vignette | {dur:.2f}s")
            render_clip_veo(veo_path, tmp_clip, dur)
        elif png_path.exists():
            direction = KB_DIRECTIONS[idx_global % len(KB_DIRECTIONS)]
            print(f"  [{i+1}/{len(quadros)}] Q{q:02d}: PNG -> KenBurns({direction}) | {dur:.2f}s")
            render_clip_png(png_path, direction, tmp_clip, dur)
        else:
            print(f"  [SKIP] Q{q:02d}: sem Veo3 e sem PNG")
            continue

        clip_paths.append(tmp_clip)
        final_durs.append(dur)
        gc.collect()

    if not clip_paths:
        print("[ERRO] Nenhum clip gerado.")
        sys.exit(1)

    # 2. Concat com xfade
    print(f"\n[2/3] Concatenando {len(clip_paths)} clips com xfade {CROSSFADE}s...")
    silent_path = OUT_DIR / f"parte_{parte:02d}_silent.mp4"
    total_dur = concat_with_xfade(clip_paths, final_durs, silent_path)
    print(f"  Duracao total do video: {total_dur:.2f}s | audio: {audio_dur:.2f}s")

    # 3. Mix audio — video ja dimensionado pelo audio, sem -shortest
    print(f"\n[3/3] Mixando audio (narracao + trilha vol={TRILHA_VOL})...")
    final_path = OUT_DIR / f"parte_{parte:02d}.mp4"
    trilha_path = AUDIO_DIR / "Trilha1.mp3"

    if trilha_path.exists():
        fade_start = max(0, audio_dur - 2)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(silent_path),
            "-i", str(narr_path),
            "-i", str(trilha_path),
            "-filter_complex",
            f"[1:a]volume=1.0[narr];"
            f"[2:a]volume={TRILHA_VOL},afade=t=out:st={fade_start}:d=2[tr];"
            f"[narr][tr]amix=inputs=2:duration=first:dropout_transition=0[mix]",
            "-map", "0:v", "-map", "[mix]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            str(final_path),
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(silent_path),
            "-i", str(narr_path),
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            str(final_path),
        ]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[ERRO ffmpeg mix]\n{r.stderr[-800:]}")
        sys.exit(1)
    silent_path.unlink(missing_ok=True)

    # Limpa temp
    shutil.rmtree(tmp_dir, ignore_errors=True)

    size_mb = final_path.stat().st_size / 1024 / 1024
    print(f"\n[OK] {final_path.name} ({size_mb:.1f} MB)")
    print(f"     Caminho: {final_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parte", type=int, required=True, help="Numero da parte (1-9)")
    args = ap.parse_args()

    if not VEO3_DIR.exists():
        print(f"[ERRO] Pasta Veo3 nao existe: {VEO3_DIR}")
        sys.exit(1)
    if not ASSETS.exists():
        print(f"[ERRO] Pasta de assets nao existe: {ASSETS}")
        sys.exit(1)

    render_parte(args.parte)


if __name__ == "__main__":
    main()
