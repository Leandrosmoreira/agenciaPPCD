# ============================================================================
# Phantasma -- Editor Cinematografico | Abismo Criativo
# Video: video-008-sinais-fisicos | Canal: Sinais do Fim
# Gerado em: 2026-04-11 (v3 -- 5 partes com audio, para CapCut)
# Executar: python _tools/edicao_sinais-do-fim_video-008-sinais-fisicos.py
# ============================================================================

import sys, io, gc, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from moviepy.editor import (
    ImageClip, VideoClip, ColorClip,
    concatenate_videoclips
)
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── FONTES WINDOWS ────────────────────────────────────────────────────────────
def _get_font(size):
    for path in [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/verdanab.ttf",
        "C:/Windows/Fonts/verdana.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()

def _pil_text_frame(text, w, h, fontsize, color_hex, stroke_color_hex="#000000",
                    stroke_w=2, align="center", valign="center", pad_bottom=0):
    color  = tuple(int(color_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    stroke = tuple(int(stroke_color_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    font   = _get_font(fontsize)
    img    = Image.new("RGB", (w, h), (0, 0, 0))
    draw   = ImageDraw.Draw(img)
    lines  = text.split("\n")
    line_h = fontsize + 8
    total_h = len(lines) * line_h
    if valign == "center":
        y_start = (h - total_h) // 2
    else:
        y_start = int(h * 0.80) - total_h // 2 + pad_bottom
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw   = bbox[2] - bbox[0]
        x    = (w - tw) // 2 if align == "center" else 40
        y    = y_start + i * line_h
        for dx in range(-stroke_w, stroke_w + 1):
            for dy in range(-stroke_w, stroke_w + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), line, font=font, fill=stroke)
        draw.text((x, y), line, font=font, fill=color)
    return np.array(img)

# ── PATHS ─────────────────────────────────────────────────────────────────────
BASE  = Path(r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-008-sinais-fisicos")
IMG   = BASE / "6-assets" / "imagens"
AUDIO = BASE / "6-assets" / "audio_suno"
OUT   = BASE / "7-edicao"
OUT.mkdir(exist_ok=True)

W, H, FPS = 1920, 1080, 30

TRILHA = AUDIO / "trilha.MP3"
if not TRILHA.exists():
    TRILHA = AUDIO / "trilha.mp3"

# ── COLOR GRADES (float32 in-place -- sem arrays temporarios) ─────────────────
def grade_biblical(frame):
    f = frame.astype(np.float32)
    np.multiply(f[:, :, 0], np.float32(1.15), out=f[:, :, 0])
    np.clip(f[:, :, 0], 0, 255, out=f[:, :, 0])
    np.multiply(f[:, :, 2], np.float32(0.85), out=f[:, :, 2])
    np.multiply(f, np.float32(0.90), out=f)
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)

def grade_apocalypse(frame):
    f    = frame.astype(np.float32)
    gray = f.mean(axis=2, keepdims=True)
    np.multiply(f,    np.float32(0.30), out=f)
    np.multiply(gray, np.float32(0.70), out=gray)
    np.add(f, gray, out=f)
    del gray
    np.multiply(f[:, :, 0], np.float32(1.20), out=f[:, :, 0])
    np.clip(f[:, :, 0], 0, 255, out=f[:, :, 0])
    np.multiply(f, np.float32(0.85), out=f)
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)

def grade_revelation(frame):
    f = frame.astype(np.float32)
    dark = f < np.float32(80)
    f[dark] *= np.float32(0.60)
    del dark
    bright = f > np.float32(180)
    f[bright] *= np.float32(1.10)
    del bright
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)

GRADES = {
    "biblical":   grade_biblical,
    "apocalypse": grade_apocalypse,
    "revelation": grade_revelation,
}

# ── KEN BURNS (lazy loading) ──────────────────────────────────────────────────
def ken_burns(img_path, duration, zoom_type="zoom_in", grade="biblical"):
    img_path_str = str(img_path)
    with Image.open(img_path_str) as _tmp:
        iw, ih = _tmp.size
    scale = max(W / iw, H / ih) * 1.12
    if zoom_type == "zoom_in":
        s0, s1, dx, dy = scale, scale * 1.08, 0.0, 0.0
    elif zoom_type == "zoom_out":
        s0, s1, dx, dy = scale * 1.08, scale, 0.0, 0.0
    elif zoom_type == "pan_left":
        s0, s1, dx, dy = scale, scale, 0.05, 0.0
    elif zoom_type == "pan_right":
        s0, s1, dx, dy = scale, scale, -0.05, 0.0
    else:
        s0, s1, dx, dy = scale, scale * 1.05, 0.0, 0.0
    grade_fn = GRADES.get(grade, grade_biblical)
    _cache = [None]
    def make_frame(t):
        if _cache[0] is None:
            _cache[0] = np.array(Image.open(img_path_str).convert("RGB"))
        img_array = _cache[0]
        p     = t / max(duration, 0.001)
        cur_s = s0 + (s1 - s0) * p
        nw    = int(iw * cur_s)
        nh    = int(ih * cur_s)
        resized = np.array(Image.fromarray(img_array).resize((nw, nh), Image.LANCZOS))
        ox = int((nw - W) / 2 + dx * nw * p)
        oy = int((nh - H) / 2 + dy * nh * p)
        ox = max(0, min(ox, nw - W))
        oy = max(0, min(oy, nh - H))
        return grade_fn(resized[oy:oy + H, ox:ox + W])
    return VideoClip(make_frame, duration=duration).set_fps(FPS)

# ── TEXT CLIPS ────────────────────────────────────────────────────────────────
def tela_preta(duration=3.0):
    return ColorClip(size=(W, H), color=(0, 0, 0)).set_duration(duration)

def texto_pivo(text, duration=6.0, fontsize=64):
    frame = _pil_text_frame(text, W, H, fontsize, "#C5A355", stroke_w=2)
    return ImageClip(frame).set_duration(duration).fadein(0.5).fadeout(0.5)

def logo_cta(duration=35.0):
    img  = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    f_big = _get_font(80)
    f_sml = _get_font(42)
    gold  = (197, 163, 85)
    white = (255, 255, 255)
    black = (0, 0, 0)
    logo_txt = "SINAIS DO FIM"
    bb = draw.textbbox((0, 0), logo_txt, font=f_big)
    x  = (W - (bb[2] - bb[0])) // 2
    for ddx in (-3, -2, -1, 1, 2, 3):
        for ddy in (-3, -2, -1, 1, 2, 3):
            draw.text((x + ddx, 380 + ddy), logo_txt, font=f_big, fill=black)
    draw.text((x, 380), logo_txt, font=f_big, fill=gold)
    cta_txt = "INSCREVA-SE  |  SINO ATIVADO  |  COMENTE ABAIXO"
    bb2 = draw.textbbox((0, 0), cta_txt, font=f_sml)
    x2  = (W - (bb2[2] - bb2[0])) // 2
    draw.text((x2, 520), cta_txt, font=f_sml, fill=white)
    frame = np.array(img)
    return ImageClip(frame).set_duration(duration).fadein(1.0).fadeout(5.0)

# ── OVERLAY CITACAO ───────────────────────────────────────────────────────────
def add_overlay(clip, text, start_t=2.0, dur=4.0):
    def frame_with_overlay(t):
        base = clip.get_frame(t)
        if not (start_t <= t <= start_t + dur):
            return base
        img  = Image.fromarray(base)
        draw = ImageDraw.Draw(img)
        font = _get_font(42)
        gold  = (197, 163, 85)
        black = (0, 0, 0)
        bb = draw.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        x  = (W - tw) // 2
        y  = int(H * 0.82)
        for ddx in (-2, -1, 1, 2):
            for ddy in (-2, -1, 1, 2):
                draw.text((x + ddx, y + ddy), text, font=font, fill=black)
        draw.text((x, y), text, font=font, fill=gold)
        return np.array(img)
    return VideoClip(frame_with_overlay, duration=clip.duration).set_fps(FPS)


# ── STORYBOARD COMPLETO (90 imagens + especiais) ──────────────────────────────
STORYBOARD = [

    # ── ABERTURA ────────────────────────────────────────────────────────────────
    (None,      3,  None,         None,          "smash_cut",   None),

    # ── PARTE 1 — gancho | corvos + cavaleiro + anjos + profetas ────────────────
    ("img_082", 7,  "zoom_in",    "apocalypse",  "fade_black",  None),
    ("img_083", 7,  "pan_right",  "revelation",  "crossfade",   None),
    ("img_084", 7,  "zoom_out",   "apocalypse",  "smash_cut",   None),
    ("img_085", 7,  "zoom_in",    "revelation",  "crossfade",   None),
    ("img_086", 7,  "pan_left",   "apocalypse",  "crossfade",   None),
    ("img_087", 7,  "zoom_out",   "revelation",  "dissolve",    None),
    ("img_088", 7,  "zoom_in",    "apocalypse",  "crossfade",   None),
    ("img_089", 6,  "pan_right",  "revelation",  "smash_cut",   None),
    ("img_090", 6,  "zoom_in",    "apocalypse",  "crossfade",   None),
    ("img_022", 7,  "zoom_in",    "apocalypse",  "smash_cut",   None),
    ("img_023", 7,  "zoom_out",   "revelation",  "crossfade",   None),
    ("img_028", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_029", 7,  "pan_right",  "biblical",    "crossfade",   None),
    ("img_032", 6,  "zoom_out",   "revelation",  "crossfade",   None),
    ("img_033", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_034", 7,  "pan_left",   "biblical",    "crossfade",   None),
    ("img_073", 7,  "pan_right",  "apocalypse",  "crossfade",   None),
    ("img_074", 7,  "zoom_out",   "biblical",    "crossfade",   None),
    ("img_075", 7,  "zoom_in",    "apocalypse",  "crossfade",   None),
    ("img_076", 7,  "pan_left",   "biblical",    "fade_black",  None),

    # ── TEXTO PIVO 1 ─────────────────────────────────────────────────────────
    (None,      6,  None,         None,          "fade_black",  "TEXTO_PIVO_1"),

    # ── PARTE 2 — Joel + Jesus + sinais do ceu ──────────────────────────────────
    ("img_057", 8,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_058", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_053", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_054", 7,  "pan_right",  "biblical",    "crossfade",   None),
    ("img_055", 8,  "zoom_out",   "biblical",    "fade_black",  "Joel 2:30-31"),
    ("img_056", 7,  "pan_left",   "biblical",    "dissolve",    None),
    ("img_035", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_036", 7,  "pan_left",   "biblical",    "crossfade",   None),
    ("img_026", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_027", 7,  "zoom_out",   "revelation",  "crossfade",   None),
    ("img_014", 7,  "pan_left",   "biblical",    "crossfade",   None),
    ("img_015", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_016", 6,  "zoom_out",   "biblical",    "crossfade",   None),
    ("img_017", 6,  "pan_right",  "biblical",    "crossfade",   None),
    ("img_045", 7,  "zoom_in",    "apocalypse",  "crossfade",   None),
    ("img_046", 7,  "pan_right",  "apocalypse",  "crossfade",   None),
    ("img_005", 8,  "zoom_out",   "revelation",  "crossfade",   None),
    ("img_006", 7,  "zoom_in",    "revelation",  "dissolve",    None),
    ("img_007", 7,  "zoom_out",   "revelation",  "crossfade",   None),
    ("img_008", 8,  "zoom_in",    "biblical",    "fade_black",  "Mateus 16:2-3"),
    ("img_009", 7,  "pan_right",  "biblical",    "crossfade",   None),
    ("img_003", 7,  "zoom_out",   "revelation",  "crossfade",   None),
    ("img_004", 6,  "zoom_in",    "revelation",  "fade_black",  None),

    # ── PARTE 3 — Elias + chuva sangue + Moises ─────────────────────────────────
    ("img_021", 7,  "zoom_in",    "revelation",  "smash_cut",   None),
    ("img_049", 8,  "zoom_in",    "biblical",    "fade_black",  None),
    ("img_050", 8,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_051", 8,  "zoom_in",    "biblical",    "fade_black",  None),
    ("img_052", 8,  "zoom_out",   "biblical",    "crossfade",   None),
    ("img_024", 8,  "zoom_in",    "biblical",    "fade_black",  "1 Reis 17:6"),
    ("img_067", 7,  "pan_right",  "biblical",    "crossfade",   None),
    ("img_063", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_064", 7,  "pan_left",   "biblical",    "crossfade",   None),
    ("img_065", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_069", 7,  "pan_right",  "biblical",    "crossfade",   None),
    ("img_070", 7,  "zoom_out",   "biblical",    "crossfade",   None),
    ("img_030", 7,  "zoom_in",    "apocalypse",  "crossfade",   None),
    ("img_031", 7,  "zoom_out",   "revelation",  "crossfade",   None),
    ("img_010", 8,  "zoom_out",   "revelation",  "crossfade",   None),
    ("img_011", 8,  "zoom_in",    "revelation",  "crossfade",   None),
    ("img_077", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_078", 7,  "pan_left",   "biblical",    "fade_black",  "Exodo 7"),

    # ── TEXTO PIVO 2 ─────────────────────────────────────────────────────────
    (None,      6,  None,         None,          "smash_cut",   "TEXTO_PIVO_2"),

    # ── PARTE 4 — conexao presente + selos + pergunta ───────────────────────────
    ("img_001", 8,  "zoom_in",    "revelation",  "smash_cut",   None),
    ("img_002", 8,  "zoom_in",    "revelation",  "fade_black",  "Apocalipse 6:12"),
    ("img_079", 8,  "zoom_out",   "apocalypse",  "crossfade",   None),
    ("img_080", 7,  "pan_right",  "revelation",  "crossfade",   None),
    ("img_081", 7,  "zoom_in",    "revelation",  "crossfade",   None),
    ("img_012", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_013", 7,  "pan_left",   "biblical",    "crossfade",   None),
    ("img_061", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_062", 7,  "zoom_out",   "biblical",    "crossfade",   None),
    ("img_043", 7,  "zoom_in",    "apocalypse",  "crossfade",   None),
    ("img_044", 7,  "pan_right",  "apocalypse",  "crossfade",   None),
    ("img_066", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_068", 7,  "pan_left",   "biblical",    "crossfade",   None),
    ("img_071", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_072", 7,  "zoom_out",   "biblical",    "fade_black",  "Apocalipse 16:3"),

    # ── PARTE 5 — encerramento + CTA ────────────────────────────────────────────
    ("img_018", 7,  "zoom_in",    "revelation",  "crossfade",   None),
    ("img_019", 7,  "pan_right",  "revelation",  "crossfade",   None),
    ("img_020", 7,  "zoom_out",   "apocalypse",  "crossfade",   None),
    ("img_041", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_042", 7,  "pan_right",  "biblical",    "crossfade",   None),
    ("img_059", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_060", 7,  "zoom_out",   "biblical",    "crossfade",   None),
    ("img_025", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_037", 7,  "pan_left",   "biblical",    "crossfade",   None),
    ("img_038", 7,  "zoom_in",    "biblical",    "crossfade",   None),
    ("img_039", 7,  "zoom_out",   "biblical",    "crossfade",   None),
    ("img_040", 7,  "pan_right",  "biblical",    "crossfade",   None),
    ("img_047", 8,  "zoom_out",   "biblical",    "crossfade",   None),
    ("img_048", 8,  "zoom_out",   "biblical",    "dissolve",    None),

    # ── LOGO CTA FINAL ───────────────────────────────────────────────────────
    (None,     35,  None,         None,          "dissolve",    "LOGO_CTA"),
]

# ── BATCH CUTS (1 por parte de audio) ────────────────────────────────────────
BATCH_CUTS = [
    (0,  22),   # Parte 1: abertura + corvos + profetas + pivot1
    (22, 44),   # Parte 2: Joel + Jesus + sinais
    (44, 63),   # Parte 3: Elias + chuva + Moises + pivot2
    (63, 79),   # Parte 4: selos + pergunta
    (79, None), # Parte 5: encerramento + CTA
]

PARTES_AUDIO = [AUDIO / f"parte{n}.mp3" for n in range(1, 6)]

TEMP_DIR = OUT / "temp_batches"
TEMP_DIR.mkdir(exist_ok=True)

WRITE_OPTS = dict(
    fps=FPS, codec="libx264", bitrate="5000k",
    preset="ultrafast", threads=1, audio=False, logger="bar",
    ffmpeg_params=["-refs", "1", "-bf", "0"],
)

# ── BUILD CLIP ────────────────────────────────────────────────────────────────
def build_clip(entry):
    img_key, dur, zoom, grade, trans, overlay = entry
    if img_key is None:
        if overlay == "TEXTO_PIVO_1":
            return texto_pivo("MAS EXISTE UMA PERGUNTA\nQUE A CIENCIA NAO FAZ", duration=dur)
        elif overlay == "TEXTO_PIVO_2":
            return texto_pivo("E SE JA TIVER COMECADO?", duration=dur)
        elif overlay == "LOGO_CTA":
            return logo_cta(duration=dur)
        else:
            return tela_preta(duration=dur)
    img_file = IMG / f"{img_key}.png"
    if not img_file.exists():
        print(f"  AVISO: {img_file.name} nao encontrado -- tela preta")
        return tela_preta(duration=dur)
    clip = ken_burns(img_file, dur, zoom_type=zoom, grade=grade)
    if overlay and overlay not in ("TEXTO_PIVO_1", "TEXTO_PIVO_2", "LOGO_CTA"):
        clip = add_overlay(clip, overlay, start_t=2.0, dur=4.0)
    return clip

# ── PROBE DURACAO ─────────────────────────────────────────────────────────────
def probe_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True
    )
    return float(r.stdout.strip()) if r.returncode == 0 else 0.0

# ── RENDER PRINCIPAL ──────────────────────────────────────────────────────────
trilha_offset = 0.0  # posicao acumulada na trilha

for b_idx, (start, end) in enumerate(BATCH_CUTS):
    parte_num = b_idx + 1
    batch = STORYBOARD[start:end]
    print(f"\n{'='*60}")
    print(f"PARTE {parte_num}/5 — {len(batch)} clips")
    print(f"{'='*60}")

    # ── 1. Renderizar video silencioso ────────────────────────────────────────
    clips = [build_clip(e) for e in batch]
    batch_video = concatenate_videoclips(clips, method="chain")
    approx_dur  = batch_video.duration

    silent_path = TEMP_DIR / f"parte_{parte_num:02d}_silent.mp4"
    print(f"  [1/3] Renderizando {silent_path.name} ({approx_dur:.1f}s)...")
    batch_video.write_videofile(str(silent_path), **WRITE_OPTS)

    for c in clips:
        try: c.close()
        except: pass
    try: batch_video.close()
    except: pass
    gc.collect()

    # ── 2. Probe duracao real do arquivo gerado ───────────────────────────────
    batch_dur = probe_duration(silent_path)
    if batch_dur == 0.0:
        batch_dur = approx_dur
    print(f"  [2/3] Duracao real: {batch_dur:.2f}s")

    # ── 3. Mixar audio (narracao + trilha) ───────────────────────────────────
    final_path = OUT / f"parte_{parte_num:02d}.mp4"
    audio_part = PARTES_AUDIO[b_idx]

    print(f"  [3/3] Mixando audio -> {final_path.name}")

    if audio_part.exists() and TRILHA.exists():
        fo_trilha = max(batch_dur - 2.5, 0.0)
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(silent_path),
            "-ss", f"{trilha_offset:.3f}", "-i", str(TRILHA),
            "-i", str(audio_part),
            "-filter_complex",
            (f"[1:a]volume=0.22,"
             f"atrim=0:{batch_dur:.3f},"
             f"afade=t=out:st={fo_trilha:.3f}:d=2[trilha];"
             f"[2:a]volume=1.0[narracao];"
             "[trilha][narracao]amix=inputs=2:duration=shortest[audio]"),
            "-map", "0:v", "-map", "[audio]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", str(final_path)
        ], check=True)
        print(f"  OK narracao + trilha (offset={trilha_offset:.1f}s)")

    elif audio_part.exists():
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(silent_path),
            "-i", str(audio_part),
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", str(final_path)
        ], check=True)
        print(f"  OK narracao (sem trilha)")

    else:
        import shutil
        shutil.copy(str(silent_path), str(final_path))
        print(f"  AVISO sem audio -- video puro copiado")

    trilha_offset += batch_dur
    size_mb = final_path.stat().st_size / 1e6 if final_path.exists() else 0
    print(f"  => {final_path.name} | {size_mb:.1f} MB | trilha ate {trilha_offset:.1f}s")

# ── RESUMO FINAL ──────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("TODAS AS PARTES PRONTAS")
print(f"{'='*60}")
total_mb = 0.0
for i in range(1, 6):
    p = OUT / f"parte_{i:02d}.mp4"
    if p.exists():
        mb = p.stat().st_size / 1e6
        total_mb += mb
        print(f"  parte_{i:02d}.mp4  {mb:.1f} MB")
    else:
        print(f"  parte_{i:02d}.mp4  NAO GERADO")
print(f"\nTotal: {total_mb:.1f} MB")
print(f"Pasta: {OUT}")
print("\nImporte as 5 partes no CapCut e una em ordem.")
