import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
Phantasma NIVEL 3 -- video-015-economist-manipulacao
"ACHEI QUEM MANIPULA O MERCADO: A CAPA DA ECONOMIST 2026"

Stack: MoviePy 1.0.3 + OpenCV 4.11 + NumPy 2.2
Efeitos: Ken Burns Pro | Film Grain | Vignette | Color Grade Split-Tone |
         Burning Embers | Flicker Dramático | Parallax Simulado | Cross-Dissolve

Saída: 5 partes autocontidas (CapCut-ready) com áudio já mixado
  7-edicao/parte_01.mp4 … parte_05.mp4 | 1920×1080 | 30fps

Comando:
  python _tools/edicao_sinais-do-fim_video-015-economist-manipulacao.py > render.log 2>&1
"""

import gc
import math
import os
import random
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont

# ═══════════════════════════════════════════════════════════════════════
# CAMINHOS
# ═══════════════════════════════════════════════════════════════════════
BASE   = Path(__file__).resolve().parent.parent
CANAL  = "sinais-do-fim"
VIDEO  = "video-015-economist-manipulacao"
VD     = BASE / "canais" / CANAL / "videos" / VIDEO
ASSETS = VD / "6-assets"
AUDIO  = VD / "5-audio"
OUT    = VD / "7-edicao"
REFS   = VD / "6-assets/referencias"   # fotos reais + capas Economist
OUT.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# PARÂMETROS GLOBAIS
# ═══════════════════════════════════════════════════════════════════════
FPS  = 30
W, H = 1920, 1080
random.seed(847200)
np.random.seed(847200)

# Grids + buffers pré-alocados — apply_parallax usa ZERO alocações por frame
_Y32, _X32 = np.meshgrid(np.arange(H, dtype=np.float32),
                          np.arange(W, dtype=np.float32), indexing='ij')
_CY32, _CX32 = np.float32(H / 2), np.float32(W / 2)
_MAP_X   = np.empty((H, W), dtype=np.float32)   # buffer reutilizado
_MAP_Y   = np.empty((H, W), dtype=np.float32)   # buffer reutilizado
_SCRATCH = np.empty((H, W), dtype=np.float32)   # scratch temporário

# Durações reais por ffprobe (segundos)
PARTE_DUR = {1:77.880, 2:92.360, 3:99.600, 4:99.960,
             5:108.600, 6:108.440, 7:128.040, 8:107.720, 9:121.920}

# 5 batches de vídeo → cada um mixado com N partes de áudio
BATCHES = [
    {"id":1, "quadros":list(range( 1,19)), "audio":[1,2]},   # 170.24s
    {"id":2, "quadros":list(range(19,39)), "audio":[3,4]},   # 199.56s
    {"id":3, "quadros":list(range(39,61)), "audio":[5,6]},   # 217.04s
    {"id":4, "quadros":list(range(61,82)), "audio":[7,8]},   # 235.76s
    {"id":5, "quadros":list(range(82,99)), "audio":[9]},     # 121.92s
]

WRITE_OPTS = dict(
    fps=FPS, codec="libx264", preset="ultrafast",
    threads=1, bitrate="5000k",
    ffmpeg_params=["-refs","1","-bf","0"]
)

# Trilha offset acumulado entre batches (reaproveitamos trilha sem reiniciar)
_trilha_offset = 0.0

# ═══════════════════════════════════════════════════════════════════════
# KEN BURNS CONFIG
# ═══════════════════════════════════════════════════════════════════════
KB_OVERRIDES = {
    1:"none",    3:"pan_right",  4:"zoom_in",    7:"zoom_in",
    10:"zoom_in",12:"pan_right", 21:"zoom_in",   24:"zoom_out",
    27:"freeze", 39:"zoom_in",   40:"zoom_in",   45:"zoom_in",
    46:"zoom_in",47:"zoom_in",   56:"zoom_in",   61:"zoom_in",
    78:"pan_left",79:"zoom_in",  80:"zoom_in",   81:"zoom_out",
    94:"zoom_in",
}
KB_CYCLE = ["zoom_in","zoom_out","pan_right","pan_left","zoom_out","zoom_in","pan_left","pan_right"]

def kb_dir(q: int) -> str:
    if q in KB_OVERRIDES:
        return KB_OVERRIDES[q]
    return KB_CYCLE[q % len(KB_CYCLE)]

# ── MAPA DE FOTOS REAIS ─────────────────────────────────────────────────────
# Quando o arquivo existir em REFS, insere 2.5s de foto real ANTES da imagem MJ
# Efeito: foto real (P&B gradeada) → dissolve → imagem MJ colorida
REAL_PHOTO_MAP = {
    # Economist covers — BLOCO 2 histórico de acertos
    13: ("capas/economist_2021.jpg",  "The Economist — World Ahead 2021"),
    15: ("capas/economist_2022.jpg",  "The Economist — World Ahead 2022"),
    17: ("capas/economist_2023.jpg",  "The Economist — World Ahead 2023"),
    20: ("capas/economist_2024.jpg",  "The Economist — World Ahead 2024"),
    22: ("capas/economist_2025.jpg",  "The Economist — World Ahead 2025"),
    26: ("capas/economist_2026.jpg",  "The Economist — World Ahead 2026"),
    # Fotos de pessoas
    6:  ("pessoas/stephen_smith.jpg",    "Stephen Smith — $7B — First National Financial"),
    9:  ("pessoas/maria_ressa.jpg",       "Maria Ressa — Nobel da Paz 2021"),
    39: ("pessoas/tom_standage.jpg",      "Tom Standage — Editor The Economist"),
    78: ("pessoas/lynn_rothschild.jpg",   "Lynn Forester de Rothschild"),
    91: ("pessoas/zanny_beddoes.jpg",     "Zanny Minton Beddoes — Editora-chefe The Economist"),
}
REAL_PHOTO_DUR = 2.5   # segundos de foto real antes do dissolve

# Quadros com duração estendida (versos bíblicos e bombshell)
SLOW_QS = {45,46,47,56,61,78,79,80,81}

# Quadros com flash na transição de saída
FLASH_WHITE = {10,16,21,24,30,34,40}
FLASH_RED   = {23,78}

# Quadros com flicker dramático
FLICKER_QS = {10,17,23,45,56,61,78,79,80}

# Quadros com brasas densas
EMBERS_HEAVY = {1,2,3,10,23,45,46,47,56,61,78,79,80,81,82}

# ═══════════════════════════════════════════════════════════════════════
# COLOR GRADING
# ═══════════════════════════════════════════════════════════════════════
def get_grade(q: int) -> str:
    if q in SLOW_QS:          return "revelation"
    if q <= 11:               return "biblical"
    if q <= 25:               return "apocalypse"
    if q <= 40:               return "revelation"
    if q <= 60:               return "biblical"
    if q <= 81:               return "revelation"
    return "apocalypse"

def apply_grade(img: np.ndarray, mode: str) -> np.ndarray:
    """img: BGR uint8 1920x1080. Retorna BGR uint8 com grade aplicado."""
    f = img.astype(np.float32) / 255.0

    if mode == "biblical":
        # Quente carmesim: boost R, crush B
        f[:,:,2] = np.clip(f[:,:,2] * 1.15 + 0.03, 0, 1)
        f[:,:,1] = np.clip(f[:,:,1] * 0.93, 0, 1)
        f[:,:,0] = np.clip(f[:,:,0] * 0.82, 0, 1)
        f = np.power(f, 1.05)

    elif mode == "apocalypse":
        # 65% dessaturado + tint dourado nos highlights
        gray = (0.114*f[:,:,0] + 0.587*f[:,:,1] + 0.299*f[:,:,2])
        for c in range(3):
            f[:,:,c] = f[:,:,c] * 0.35 + gray * 0.65
        lum = np.max(f, axis=2)
        hi  = lum > 0.72
        f[:,:,2][hi] = np.clip(f[:,:,2][hi] * 1.12, 0, 1)  # R (dourado)
        f[:,:,1][hi] = np.clip(f[:,:,1][hi] * 1.06, 0, 1)  # G

    elif mode == "revelation":
        # Sombras azul-noite, highlights âmbar dourado, gamma crushado
        lum = 0.114*f[:,:,0] + 0.587*f[:,:,1] + 0.299*f[:,:,2]
        shadow_mask = lum < 0.38
        highlight_mask = lum > 0.65
        f[:,:,0][shadow_mask]    = np.clip(f[:,:,0][shadow_mask] * 1.10, 0, 1)  # B shadows +
        f[:,:,2][shadow_mask]    = np.clip(f[:,:,2][shadow_mask] * 0.72, 0, 1)  # R shadows -
        f[:,:,2][highlight_mask] = np.clip(f[:,:,2][highlight_mask] * 1.14, 0, 1)
        f[:,:,1][highlight_mask] = np.clip(f[:,:,1][highlight_mask] * 1.07, 0, 1)
        f = np.power(np.clip(f, 0, 1), 1.12)

    return (np.clip(f, 0, 1) * 255).astype(np.uint8)

# ═══════════════════════════════════════════════════════════════════════
# VIGNETTE (pré-computada)
# ═══════════════════════════════════════════════════════════════════════
def make_vignette(w=W, h=H, strength=0.65) -> np.ndarray:
    """Retorna máscara float32 [H,W,1] multiplicativa (0=borda, 1=centro)."""
    cx, cy = w/2, h/2
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt(((X-cx)/cx)**2 + ((Y-cy)/cy)**2)
    vign = 1.0 - np.clip(dist * strength, 0, 1)
    vign = np.power(vign, 1.5)
    return vign[:,:,np.newaxis].astype(np.float32)

VIGNETTE = make_vignette()

def apply_vignette(img: np.ndarray) -> np.ndarray:
    f = img.astype(np.float32)
    f = f * (0.30 + 0.70 * VIGNETTE)   # uma só multiplicação
    return np.clip(f, 0, 255).astype(np.uint8)

# ═══════════════════════════════════════════════════════════════════════
# FILM GRAIN
# ═══════════════════════════════════════════════════════════════════════
def apply_grain(img: np.ndarray, intensity: int = 10, frame_idx: int = 0) -> np.ndarray:
    """Grain orgânico por frame (seed varia com frame_idx)."""
    rng = np.random.default_rng(frame_idx * 7 + 42)
    noise = rng.integers(-intensity, intensity, img.shape, dtype=np.int16)
    out = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return out

# ═══════════════════════════════════════════════════════════════════════
# BURNING EMBERS
# ═══════════════════════════════════════════════════════════════════════
_EMBER_PALETTE = [
    (0,   140, 255),  # laranja claro  (OpenCV BGR: B=0, G=140, R=255)
    (0,   80,  220),  # laranja médio
    (0,   60,  180),  # laranja escuro
    (0,   30,  140),  # vermelho-brasa
]

def apply_embers(img: np.ndarray, n: int, frame_idx: int) -> np.ndarray:
    """Sobrepõe N brasas animadas em blend additive."""
    rng = np.random.default_rng(frame_idx * 13 + 99)
    out = img.copy()

    for _ in range(n):
        # Posição animada: flutua para cima ao longo do tempo
        base_x = int(rng.integers(0, W))
        base_y = int(rng.integers(0, H))
        # Deriva vertical (y sobe com frame_idx)
        y = (base_y - frame_idx * int(rng.integers(1, 4))) % H
        x = (base_x + int(rng.integers(-2, 3)) * (frame_idx % 7)) % W

        radius = int(rng.integers(2, 6))
        color  = _EMBER_PALETTE[rng.integers(0, len(_EMBER_PALETTE))]
        alpha  = float(rng.uniform(0.4, 0.95))

        # Desenha círculo com blend additive
        y1, y2 = max(0, y-radius), min(H, y+radius+1)
        x1, x2 = max(0, x-radius), min(W, x+radius+1)
        if y2 > y1 and x2 > x1:
            # Gaussian blob
            patch = out[y1:y2, x1:x2].astype(np.float32)
            cy_, cx_ = (y2-y1)//2, (x2-x1)//2
            for py in range(y2-y1):
                for px in range(x2-x1):
                    d = math.sqrt((py-cy_)**2 + (px-cx_)**2)
                    if d <= radius:
                        w_ = (1 - d/radius) * alpha
                        for c, vc in enumerate(color):
                            patch[py,px,c] = min(255, patch[py,px,c] + vc * w_)
            out[y1:y2, x1:x2] = np.clip(patch, 0, 255).astype(np.uint8)
    return out

# ═══════════════════════════════════════════════════════════════════════
# PARALLAX SIMULADO
# ═══════════════════════════════════════════════════════════════════════
def apply_parallax(img: np.ndarray, t: float, duration: float,
                   direction: str) -> np.ndarray:
    """
    Simula parallax: centro da imagem (foreground) se move 70% da velocidade,
    bordas (background) se movem 100%. Implementado como warp óptico suave.
    """
    global _MAP_X, _MAP_Y, _SCRATCH
    if direction == "none" or direction == "freeze":
        return img

    progress = np.float32(t / max(duration, 0.001))

    if direction in ("zoom_in", "zoom_out"):
        sc = np.float32(1.0 + (0.08 if direction == "zoom_in" else -0.08) * progress)
        sb = np.float32(1.0 + (0.12 if direction == "zoom_in" else -0.12) * progress)

        # dist_norm → _SCRATCH, zero alocações
        np.subtract(_X32, _CX32, out=_MAP_X);  np.divide(_MAP_X, _CX32, out=_MAP_X)
        np.multiply(_MAP_X, _MAP_X, out=_MAP_X)                      # ((X-cx)/cx)^2
        np.subtract(_Y32, _CY32, out=_MAP_Y);  np.divide(_MAP_Y, _CY32, out=_MAP_Y)
        np.multiply(_MAP_Y, _MAP_Y, out=_SCRATCH)                     # ((Y-cy)/cy)^2
        np.add(_MAP_X, _SCRATCH, out=_SCRATCH)
        np.sqrt(_SCRATCH, out=_SCRATCH);  np.clip(_SCRATCH, 0, 1, out=_SCRATCH)

        # scale_map → _MAP_X
        np.subtract(sb, sc, out=_MAP_X)
        np.multiply(_MAP_X, _SCRATCH, out=_MAP_X)
        _MAP_X += sc                                                   # scale_map

        # map_x final → _SCRATCH
        np.subtract(_X32, _CX32, out=_SCRATCH)
        np.divide(_SCRATCH, _MAP_X, out=_SCRATCH)
        _SCRATCH += _CX32                                              # map_x final

        # map_y final → _MAP_Y
        np.subtract(_Y32, _CY32, out=_MAP_Y)
        np.divide(_MAP_Y, _MAP_X, out=_MAP_Y)
        _MAP_Y += _CY32                                                # map_y final

        np.copyto(_MAP_X, _SCRATCH)                                    # map_x → _MAP_X

    elif direction in ("pan_left", "pan_right"):
        sign = np.float32(-1 if direction == "pan_left" else 1)
        shift_px = np.float32(W * 0.03 * progress * sign)

        # local_shift → _SCRATCH, zero alocações
        np.subtract(_X32, _CX32, out=_SCRATCH)
        np.abs(_SCRATCH, out=_SCRATCH)
        np.divide(_SCRATCH, _CX32, out=_SCRATCH)                      # dist_x
        _SCRATCH *= np.float32(0.40);  _SCRATCH += np.float32(0.60)
        _SCRATCH *= shift_px                                           # local_shift
        np.subtract(_X32, _SCRATCH, out=_MAP_X)                       # map_x
        np.copyto(_MAP_Y, _Y32)                                        # map_y

    else:
        return img

    return cv2.remap(img, _MAP_X, _MAP_Y, cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_REFLECT)

# ═══════════════════════════════════════════════════════════════════════
# FLICKER
# ═══════════════════════════════════════════════════════════════════════
def apply_flicker(img: np.ndarray, t: float, intensity: float = 0.07) -> np.ndarray:
    """Oscila luminância ±intensity usando onda senoidal rápida."""
    flicker = 1.0 + intensity * math.sin(t * 18.0 + 0.3) * math.cos(t * 7.3)
    f = img.astype(np.float32) * flicker
    return np.clip(f, 0, 255).astype(np.uint8)

# ═══════════════════════════════════════════════════════════════════════
# KEN BURNS (OpenCV — mais rápido que MoviePy nativo)
# ═══════════════════════════════════════════════════════════════════════
def ken_burns_frame(base_img: np.ndarray, t: float, duration: float,
                    direction: str) -> np.ndarray:
    """
    Aplica Ken Burns em um único frame.
    base_img: BGR 1024x576 (ou qualquer tamanho — será escalado para W×H).
    """
    h_, w_ = base_img.shape[:2]
    progress = t / max(duration, 0.001)

    # Easing suave (ease-in-out)
    ease = progress * progress * (3.0 - 2.0 * progress)

    if direction == "none" or direction == "freeze":
        scaled = cv2.resize(base_img, (W, H), interpolation=cv2.INTER_LANCZOS4)
        return scaled

    if direction == "zoom_in":
        scale = 1.0 + 0.12 * ease
    elif direction == "zoom_out":
        scale = 1.12 - 0.12 * ease
    elif direction in ("pan_left", "pan_right"):
        scale = 1.08  # fixo para pan

    # Novo tamanho mantendo aspect ratio de crop
    nw = int(W * scale)
    nh = int(H * scale)
    big = cv2.resize(base_img, (nw, nh), interpolation=cv2.INTER_LANCZOS4)

    if direction in ("zoom_in", "zoom_out"):
        x0 = (nw - W) // 2
        y0 = (nh - H) // 2
    elif direction == "pan_left":
        max_offset = nw - W
        x0 = int(max_offset * ease)
        y0 = (nh - H) // 2
    elif direction == "pan_right":
        max_offset = nw - W
        x0 = int(max_offset * (1.0 - ease))
        y0 = (nh - H) // 2
    else:
        x0 = (nw - W) // 2
        y0 = (nh - H) // 2

    x0 = max(0, min(x0, nw - W))
    y0 = max(0, min(y0, nh - H))
    return big[y0:y0+H, x0:x0+W]

# ═══════════════════════════════════════════════════════════════════════
# TELA PRETA Q01 (abertura)
# ═══════════════════════════════════════════════════════════════════════
def make_black_frame_clip(duration: float = 2.5) -> ImageClip:
    """Q01: tela preta com brasa central animada."""
    # Frame base preto
    base = np.zeros((H, W, 3), dtype=np.uint8)

    def make_frame(t):
        f = base.copy()
        # Brasa central que aparece lentamente
        alpha = min(1.0, t / 1.5)
        cx_, cy_ = W//2, int(H * 0.72)
        for r in range(12, 0, -1):
            intensity = int(255 * alpha * (12-r)/12)
            # Cores: laranja-brasa
            color_b = max(0, intensity // 4)
            color_g = max(0, intensity // 2)
            color_r = intensity
            cv2.circle(f, (cx_, cy_), r,
                      (color_b, color_g, color_r), -1)
        f = apply_grain(f, 5, int(t * FPS))
        return f

    clip = ImageClip(make_frame(0), duration=duration)
    clip.make_frame = make_frame
    return clip

# ═══════════════════════════════════════════════════════════════════════
# CLIP PRINCIPAL: carrega imagem + aplica todos os efeitos
# ═══════════════════════════════════════════════════════════════════════
def load_quadro_bgr(q: int) -> np.ndarray | None:
    """Carrega PNG do quadro em BGR. Retorna None se não encontrar."""
    path = ASSETS / f"Q{q:02d}.png"
    if not path.exists():
        print(f"  [SKIP] {path.name} não encontrado", flush=True)
        return None
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        print(f"  [ERRO] Falha ao abrir {path.name}", flush=True)
        return None
    return img

def build_real_photo_clip(img_path: Path, label: str,
                          duration: float = REAL_PHOTO_DUR) -> ImageClip:
    """
    Clip de 2.5s com foto real:
    - Escala para 1920x1080 mantendo aspect ratio (letterbox preto)
    - Grade P&B + tint frio (não mistura com o colorido do canal)
    - Lower third com label em dourado
    - Ken Burns zoom-in lento
    """
    img_bgr = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    if img_bgr is None:
        return None

    # Escala com letterbox
    ih, iw = img_bgr.shape[:2]
    scale = min(W / iw, H / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    resized = cv2.resize(img_bgr, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    canvas = np.zeros((H, W, 3), dtype=np.uint8)
    y0 = (H - nh) // 2
    x0 = (W - nw) // 2
    canvas[y0:y0+nh, x0:x0+nw] = resized

    # Grade P&B fria (marca temporal = mundo real = P&B do canal)
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    canvas_bw = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    # Leve tint azul-frio
    canvas_bw = canvas_bw.astype(np.float32)
    canvas_bw[:,:,0] = np.clip(canvas_bw[:,:,0] * 1.08, 0, 255)   # boost B
    canvas_bw[:,:,2] = np.clip(canvas_bw[:,:,2] * 0.90, 0, 255)   # crush R
    canvas_bw = canvas_bw.astype(np.uint8)

    # Lower third: label em dourado
    pil = Image.fromarray(cv2.cvtColor(canvas_bw, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil)
    # Barra escura semi-transparente
    overlay = Image.new("RGBA", pil.size, (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.rectangle([(0, H - 80), (W, H)], fill=(0, 0, 0, 160))
    pil = Image.alpha_composite(pil.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(pil)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 32)
    except:
        font = ImageFont.load_default()
    draw.text((40, H - 58), label, font=font, fill=(197, 163, 85))  # dourado #C5A355
    base_bgr = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    base_bgr = apply_vignette(base_bgr)

    def make_frame(t):
        progress = t / max(duration, 0.001)
        ease = progress * progress * (3.0 - 2.0 * progress)
        scale_f = 1.0 + 0.06 * ease  # zoom-in muito suave
        nw2 = int(W * scale_f)
        nh2 = int(H * scale_f)
        big = cv2.resize(base_bgr, (nw2, nh2), interpolation=cv2.INTER_LINEAR)
        x1 = (nw2 - W) // 2
        y1 = (nh2 - H) // 2
        frame = big[y1:y1+H, x1:x1+W]
        frame = apply_grain(frame, intensity=7, frame_idx=int(t * FPS))
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    clip = ImageClip(make_frame(0), duration=duration)
    clip.make_frame = make_frame
    return clip


def build_clip(q: int, duration: float) -> ImageClip:
    """Constrói ImageClip com todos os efeitos Nível 3."""

    if q == 1:
        return make_black_frame_clip(duration)

    base_img = load_quadro_bgr(q)
    if base_img is None:
        # Fallback: frame preto
        base_img = np.zeros((576, 1024, 3), dtype=np.uint8)

    grade   = get_grade(q)
    kb      = kb_dir(q)
    heavy   = q in EMBERS_HEAVY
    flicker = q in FLICKER_QS
    ember_n = 35 if heavy else 12

    # Pré-aplica grade na imagem base (invariante no tempo)
    base_graded = apply_grade(base_img, grade)

    # Cache de imagem pré-escalada (evita resize por frame no modo freeze)
    _cache = [None]

    def make_frame(t):
        frame_idx = int(t * FPS)

        # Ken Burns + Parallax (frame atual)
        kb_frame = ken_burns_frame(base_graded, t, duration, kb)

        # Parallax desabilitado — causava esticamento/distorção
        # if kb != "freeze":
        #     kb_frame = apply_parallax(kb_frame, t, duration, kb)

        # Vinheta
        kb_frame = apply_vignette(kb_frame)

        # Embers desabilitados — estavam aparecendo como pontos laranja/marrom visíveis
        # kb_frame = apply_embers(kb_frame, ember_n, frame_idx)

        # Flicker dramático
        if flicker:
            kb_frame = apply_flicker(kb_frame, t, intensity=0.06)

        # Film grain
        kb_frame = apply_grain(kb_frame, intensity=9, frame_idx=frame_idx)

        # MoviePy quer RGB
        return cv2.cvtColor(kb_frame, cv2.COLOR_BGR2RGB)

    clip = ImageClip(make_frame(0), duration=duration)
    clip.make_frame = make_frame
    return clip

# ═══════════════════════════════════════════════════════════════════════
# DURAÇÃO POR QUADRO (proporcional à duração total do batch)
# ═══════════════════════════════════════════════════════════════════════
# Durações whisper-aligned por quadro (override do calc_durations uniforme)
# Gerado por _tools/sync_quadros_whisper.py — cada valor = tempo real que narrador leva
DURATIONS_OVERRIDE = {
    # Whisper-aligned — gerado por sync_quadros_whisper.py 2026-04-17
    # Q01 = black frame 2.5s (handled em build_clip, nao precisa aqui)
    # Batch 1 (parte1+parte2 = 170.24s)
     2:18.44,  3: 8.14,  4:10.72,  5: 6.80,  6: 4.52,  7:15.56,  8: 6.76,
     9:15.40, 10: 6.36, 11: 7.40, 12:10.12, 13:11.82, 14: 9.20,
    15: 9.64, 16: 6.36, 17: 7.04, 18: 7.64,
    # Batch 2 (parte3+parte4 = 199.56s)
    19: 7.14, 20: 8.84, 21:11.84, 22: 8.62, 23:13.62, 24: 4.64,
    25:10.54, 26:15.60, 27: 5.86, 28:23.82, 29: 7.10, 30:13.08,
    31: 8.44, 32: 7.36, 33: 5.58, 34: 8.40, 35:11.94, 36: 7.66,
    37: 3.44, 38:12.86,
    # Batch 3 (parte5+parte6 = 217.04s)
    39:10.92, 40:14.06, 41:14.16, 42:11.82, 43: 7.08, 44: 6.72,
    45:10.30, 46:14.16, 47: 4.80, 48: 2.00, 49:17.34, 50: 5.84,
    51:10.08, 52: 5.94, 53: 4.46, 54:14.02, 55: 5.60, 56:17.28,
    57: 6.16, 58: 4.70, 59:10.84, 60:15.10,
    # Batch 4 (parte7+parte8 = 235.76s)
    61:10.68, 62:13.36, 63:16.04, 64: 7.30, 65: 7.80, 66: 9.82,
    67:15.92, 68:11.62, 69:10.16, 70: 9.42, 71:24.64, 72: 5.62,
    73: 2.00, 74:16.24, 75: 9.94, 76:13.00, 77:13.08, 78:10.10,
    79: 3.58, 80:17.58, 81: 5.74,
    # Batch 5 (parte9 = 121.92s)
    82:21.78, 83: 8.10, 84: 8.96, 85:13.56, 86: 7.20, 87: 5.72,
    88: 4.64, 89: 3.86, 90: 4.12, 91: 9.56, 92: 2.04, 93: 2.00,
    94: 3.62, 95: 6.16, 96: 4.76, 97: 4.18, 98: 5.68,
}

def calc_durations(quadros: list, audio_parts: list) -> list:
    """
    Usa DURATIONS_OVERRIDE (whisper-aligned) para cada quadro quando disponivel.
    Quadros com foto real: subtrai REAL_PHOTO_DUR (2.5s) da duracao da MJ para
    que o total com photo = valor whisper (photo substitui primeiros 2.5s da narracao).
    Quadros fora do override: fallback para distribuicao uniforme do tempo restante.
    """
    total_audio = sum(PARTE_DUR[p] for p in audio_parts)

    # Etapa 1: usa override onde disponivel
    known = {}
    unknown = []
    for q in quadros:
        if q in DURATIONS_OVERRIDE:
            d = DURATIONS_OVERRIDE[q]
            # Se for quadro com foto real, desconta photo_dur (photo substitui inicio da narracao)
            if q in REAL_PHOTO_MAP:
                d = max(2.0, d - REAL_PHOTO_DUR)
            known[q] = d
        else:
            unknown.append(q)

    # Etapa 2: Q01 black frame
    q01_dur = 2.5 if 1 in quadros else 0.0

    # Etapa 3: distribui tempo restante para quadros sem override
    used = sum(known.values()) + q01_dur
    # Adiciona tempo das fotos reais ao total esperado
    photo_total = sum(REAL_PHOTO_DUR for q in quadros if q in REAL_PHOTO_MAP)
    target = total_audio - photo_total
    remaining = max(0, target - used)

    if unknown:
        per_q = remaining / len(unknown)
        for q in unknown:
            weight = 1.4 if q in SLOW_QS else 1.0
            known[q] = max(3.0, per_q * weight)

    if 1 in quadros:
        known[1] = q01_dur

    # Retorna lista na ordem de quadros
    return [known.get(q, 5.0) for q in quadros]

# ═══════════════════════════════════════════════════════════════════════
# MIX DE ÁUDIO (ffmpeg — fora do MoviePy para evitar OOM)
# ═══════════════════════════════════════════════════════════════════════
def concat_audio_parts(audio_parts: list, out_audio: Path) -> bool:
    """Concatena N partes de áudio em um único MP3 via ffmpeg."""
    if len(audio_parts) == 1:
        import shutil
        shutil.copy(AUDIO / f"parte{audio_parts[0]}.mp3", out_audio)
        return True

    # Lista de inputs para concat
    inputs = []
    for p in audio_parts:
        ap = AUDIO / f"parte{p}.mp3"
        if not ap.exists():
            print(f"  [ERRO] Áudio não encontrado: {ap}", flush=True)
            return False
        inputs.extend(["-i", str(ap)])

    filter_complex = "".join(f"[{i}:0]" for i in range(len(audio_parts)))
    filter_complex += f"concat=n={len(audio_parts)}:v=0:a=1[out]"

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[out]",
        str(out_audio)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  [ERRO] concat_audio: {r.stderr[:300]}", flush=True)
        return False
    return True

def mix_video_audio(silent_mp4: Path, narr_mp3: Path, batch_id: int,
                    out_mp4: Path) -> bool:
    """
    Mixa vídeo silencioso + narração + trilha instrumental.
    Trilha: vol 0.22, offset acumulado, fade out 2s no fim.
    Narração: vol 1.0.
    """
    global _trilha_offset

    # Escolhe trilha com base no batch
    trilha_map = {1:"Trilha1.mp3", 2:"Trilha2.mp3", 3:"Trilha3.mp3",
                  4:"Trilha1.mp3", 5:"Trilha2.mp3"}
    trilha = AUDIO / trilha_map[batch_id]

    if not trilha.exists():
        # Sem trilha — só narração
        cmd = ["ffmpeg", "-y",
               "-i", str(silent_mp4),
               "-i", str(narr_mp3),
               "-c:v", "copy",
               "-c:a", "aac", "-b:a", "192k",
               "-shortest",
               str(out_mp4)]
    else:
        # Duração do vídeo para fade out
        probe = subprocess.run(
            ["ffprobe","-v","quiet","-show_entries","format=duration",
             "-of","csv=p=0", str(silent_mp4)],
            capture_output=True, text=True)
        try:
            vid_dur = float(probe.stdout.strip())
        except:
            vid_dur = 999.0

        fade_start = max(0, vid_dur - 2.0)

        cmd = ["ffmpeg", "-y",
               "-i", str(silent_mp4),
               "-i", str(narr_mp3),
               "-ss", str(_trilha_offset), "-i", str(trilha),
               "-filter_complex",
               f"[1:a]volume=1.0[narr];"
               f"[2:a]volume=0.22,afade=t=out:st={fade_start:.2f}:d=2[bg];"
               f"[narr][bg]amix=inputs=2:duration=first[aout]",
               "-map", "0:v",
               "-map", "[aout]",
               "-c:v", "copy",
               "-c:a", "aac", "-b:a", "192k",
               "-shortest",
               str(out_mp4)]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  [ERRO] mix_audio batch {batch_id}: {r.stderr[:400]}", flush=True)
        return False

    # Atualiza offset da trilha
    probe2 = subprocess.run(
        ["ffprobe","-v","quiet","-show_entries","format=duration",
         "-of","csv=p=0", str(out_mp4)],
        capture_output=True, text=True)
    try:
        _trilha_offset += float(probe2.stdout.strip())
    except:
        _trilha_offset += sum(PARTE_DUR[p] for p in [])
    return True

# ═══════════════════════════════════════════════════════════════════════
# RENDER PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════
def render_batch(batch: dict) -> bool:
    bid    = batch["id"]
    quadros= batch["quadros"]
    audios = batch["audio"]

    print(f"\n{'='*60}", flush=True)
    print(f"BATCH {bid}/5 — Q{quadros[0]:02d}–Q{quadros[-1]:02d} | "
          f"áudio partes {audios}", flush=True)
    print(f"{'='*60}", flush=True)

    durations = calc_durations(quadros, audios)

    # ── Constrói clips ──────────────────────────────────────────────
    clips = []
    for i, q in enumerate(quadros):
        dur = durations[i]

        # Verifica se há foto real para inserir ANTES do MJ
        if q in REAL_PHOTO_MAP:
            rel_path, label = REAL_PHOTO_MAP[q]
            ref_path = REFS / rel_path
            if ref_path.exists() and ref_path.stat().st_size > 10000:
                real_clip = build_real_photo_clip(ref_path, label, REAL_PHOTO_DUR)
                if real_clip:
                    clips.append(real_clip)
                    dur = max(dur - REAL_PHOTO_DUR, 3.0)  # desconta do MJ
                    print(f"  Q{q:02d} | FOTO_REAL+MJ | {label[:40]}", flush=True)
                else:
                    print(f"  Q{q:02d} | {kb_dir(q):<10} | {get_grade(q):<11} | "
                          f"{dur:.1f}s", flush=True)
            else:
                print(f"  Q{q:02d} | {kb_dir(q):<10} | {get_grade(q):<11} | "
                      f"{dur:.1f}s [ref não encontrada: {rel_path}]", flush=True)
        else:
            print(f"  Q{q:02d} | {kb_dir(q):<10} | {get_grade(q):<11} | "
                  f"{dur:.1f}s", flush=True)

        clip = build_clip(q, dur)
        clips.append(clip)

    # ── Concatena ───────────────────────────────────────────────────
    print(f"\n  Concatenando {len(clips)} clips...", flush=True)
    final = concatenate_videoclips(clips, method="chain")

    # ── Render silent ───────────────────────────────────────────────
    silent_path = OUT / f"parte_{bid:02d}_silent.mp4"
    print(f"  Renderizando {silent_path.name}...", flush=True)
    final.write_videofile(str(silent_path), audio=False, **WRITE_OPTS)

    # Limpa RAM imediatamente
    final.close()
    for c in clips:
        c.close()
    del clips, final
    gc.collect()

    # ── Concatena áudios ────────────────────────────────────────────
    narr_concat = OUT / f"narr_{bid:02d}.mp3"
    print(f"  Concatenando áudios partes {audios}...", flush=True)
    if not concat_audio_parts(audios, narr_concat):
        return False

    # ── Mix final ───────────────────────────────────────────────────
    out_path = OUT / f"parte_{bid:02d}.mp4"
    print(f"  Mixando → {out_path.name}...", flush=True)
    if not mix_video_audio(silent_path, narr_concat, bid, out_path):
        return False

    # Limpa temporários
    silent_path.unlink(missing_ok=True)
    narr_concat.unlink(missing_ok=True)

    # Duração real do output
    probe = subprocess.run(
        ["ffprobe","-v","quiet","-show_entries","format=duration",
         "-of","csv=p=0", str(out_path)],
        capture_output=True, text=True)
    try:
        dur_real = float(probe.stdout.strip())
        m, s = divmod(int(dur_real), 60)
        print(f"  ✅ {out_path.name} → {m}:{s:02d}", flush=True)
    except:
        print(f"  ✅ {out_path.name} gerado", flush=True)

    return True

# ═══════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════
def main():
    import argparse, time

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--only-batch', type=int, default=None,
                        help='Renderizar apenas este batch (1-5) — uso interno')
    args, _ = parser.parse_known_args()

    # ── Modo subprocesso: apenas 1 batch ────────────────────────────────
    if args.only_batch is not None:
        bid = args.only_batch
        batch = next((b for b in BATCHES if b["id"] == bid), None)
        if batch is None:
            print(f"[ERRO] Batch {bid} não encontrado", flush=True)
            sys.exit(1)
        print(f"\n{'='*50}", flush=True)
        print(f"SUBPROCESS — Batch {bid}/5", flush=True)
        ok = render_batch(batch)
        sys.exit(0 if ok else 1)

    # ── Modo principal: dispara subprocesso por batch ───────────────────
    print("PHANTASMA NÍVEL 3 — video-015-economist-manipulacao", flush=True)
    print(f"Output: {OUT}", flush=True)
    print(f"Quadros: 98 | Partes áudio: 9 | Batches: 5", flush=True)
    print(f"Resolução: {W}×{H} | FPS: {FPS}", flush=True)
    print(f"Efeitos: KenBurns+Parallax | Grain | Vignette | Grade | Embers | Flicker",
          flush=True)
    print(f"Estratégia: SUBPROCESS por batch (RAM zerada entre batches)", flush=True)

    # Verifica assets
    missing = [q for b in BATCHES for q in b["quadros"]
               if q > 1 and not (ASSETS / f"Q{q:02d}.png").exists()]
    if missing:
        print(f"\n[AVISO] {len(missing)} quadros não encontrados: {missing[:10]}...",
              flush=True)

    # Limpa arquivos parciais de runs anteriores
    for f in OUT.glob("*_silent.mp4"):
        f.unlink()
        print(f"  [limpeza] {f.name} removido", flush=True)
    for f in OUT.glob("narr_*.mp3"):
        f.unlink()
        print(f"  [limpeza] {f.name} removido", flush=True)

    script = str(Path(__file__).resolve())
    success = 0
    for batch in BATCHES:
        bid = batch["id"]
        print(f"\n{'='*60}", flush=True)
        print(f"Lançando batch {bid}/5 em subprocesso...", flush=True)
        result = subprocess.run(
            [sys.executable, script, '--only-batch', str(bid)],
            # Herda stdout/stderr do pai (vai para render.log)
        )
        if result.returncode == 0:
            success += 1
            print(f"  Batch {bid} CONCLUÍDO (exit 0)", flush=True)
        else:
            print(f"[ERRO] Batch {bid} falhou (exit {result.returncode}) — abortando",
                  flush=True)
            sys.exit(1)

        # Forçar Windows a liberar páginas de RAM antes do próximo batch
        try:
            import ctypes
            ctypes.windll.psapi.EmptyWorkingSet(
                ctypes.windll.kernel32.GetCurrentProcess())
            print(f"  [RAM] Working set liberado", flush=True)
        except Exception:
            pass
        gc.collect()
        import time as _time; _time.sleep(3)  # pausa para OS liberar páginas

    print(f"\n{'='*60}", flush=True)
    print(f"CONCLUÍDO: {success}/5 partes geradas", flush=True)
    print(f"Output: {OUT}", flush=True)
    print(f"\nOrdem para CapCut:", flush=True)
    for i in range(1, 6):
        print(f"  {i}. {OUT / f'parte_{i:02d}.mp4'}", flush=True)

    # Registra pipeline.log
    log_path = BASE / "canais" / CANAL / "_config" / "pipeline.log"
    with log_path.open("a", encoding="utf-8") as f:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{ts} | {VIDEO} | FASE 3.5 | Phantasma | "
                f"5 partes renderizadas Nível 3 (subprocess) | {OUT}\n")

if __name__ == "__main__":
    main()
