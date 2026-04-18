"""
PHANTASMA — Editor Cinematografico
Canal: Sinais do Fim
Video: video-014-arrebatamento — ARREBATAMENTO: O QUE MATEUS 24:36 PROIBE REVELAR
Gerado por: Phantasma | 2026-04-17

Arquitetura:
  - 60 quadros divididos em 5 batches de 12 quadros
  - Ken Burns (zoom_in / zoom_out / pan_left / pan_right) por quadro
  - Color grading: grade_biblical / grade_apocalypse / grade_revelation
  - Render em subprocesso isolado por batch (--only-batch N)
  - Mix ffmpeg: narracao (vol 1.0) + trilha (vol 0.22 se existir)

Parte 1: Q01-Q12  | BLOCO 0 — Gancho: O Pastor que Enganou 300 Mil
Parte 2: Q13-Q24  | BLOCO 1 — O Versiculo que Todos Ignoram
Parte 3: Q25-Q37  | BLOCO 2 — O que a Biblia Realmente Diz (13 quadros)
Parte 4: Q38-Q50  | BLOCO 3 — Os Sinais sao Reais (13 quadros)
Parte 5: Q51-Q60  | BLOCO 4 — Urgencia Real + CTA (10 quadros)

QUADROS FALTANTES em 6-assets (usar text_screen com titulo da cena):
  Q24 — Ladrão de noite
  Q42 — Relogio do Juizo
  Q43 — 2 Timoteo 3
  Q50 — Proximidade real
  Q55 — Dois tipos de cristao
  Q56 — Sinais reais, volta certa

ADR-008: video_parteNN.mp4 DEVE ser >= PARTEN.mp3
"""

import gc
import os
import sys
import subprocess
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from moviepy.editor import VideoClip, concatenate_videoclips

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
ROOT   = Path(__file__).resolve().parent.parent
CANAL  = ROOT / "canais/sinais-do-fim"
VIDEO  = CANAL / "videos/video-014-arrebatamento"
ASSETS = VIDEO / "6-assets"
AUDIO  = VIDEO / "5-audio"
OUT    = VIDEO / "7-edicao"
OUT.mkdir(exist_ok=True)

W, H, FPS = 1920, 1080, 30

# ---------------------------------------------------------------------------
# PARTE_DUR — duracao em segundos por parte de audio
# Distribuicao storyboard:
#   Parte 1: Q01-Q12  | 0:00–2:30 = 150s
#   Parte 2: Q13-Q24  | 2:30–5:00 = 150s (12 quadros)
#   Parte 3: Q25-Q37  | 5:00–7:30 = 150s (13 quadros)
#   Parte 4: Q38-Q50  | 7:30–10:00 = 150s (13 quadros)
#   Parte 5: Q51-Q60  | 10:00–12:00 = 120s (10 quadros)
# ---------------------------------------------------------------------------
PARTE_DUR = {
    1: 150.0,
    2: 150.0,
    3: 150.0,
    4: 150.0,
    5: 120.0,
}

# ---------------------------------------------------------------------------
# AUDIO
# ---------------------------------------------------------------------------
PARTES_AUDIO = [AUDIO / f"parte{n}.mp3" for n in range(1, 6)]
TRILHA       = AUDIO / "trilha.MP3"

# ---------------------------------------------------------------------------
# WRITE OPTIONS
# ---------------------------------------------------------------------------
WRITE_OPTS = dict(
    codec="libx264",
    audio=False,
    fps=FPS,
    preset="ultrafast",
    threads=1,
    bitrate="5000k",
    ffmpeg_params=["-refs", "1", "-bf", "0"],
)

# ---------------------------------------------------------------------------
# QUADROS FALTANTES — usar text_screen com titulo da cena
# ---------------------------------------------------------------------------
QUADROS_FALTANTES = {24, 42, 43, 50, 55, 56}

# ---------------------------------------------------------------------------
# BATCHES
# ---------------------------------------------------------------------------
BATCHES = [
    {"id": 1, "quadros": list(range(1,  13)), "audio_parts": [1]},   # Q01-Q12 (12)
    {"id": 2, "quadros": list(range(13, 25)), "audio_parts": [2]},   # Q13-Q24 (12)
    {"id": 3, "quadros": list(range(25, 38)), "audio_parts": [3]},   # Q25-Q37 (13)
    {"id": 4, "quadros": list(range(38, 51)), "audio_parts": [4]},   # Q38-Q50 (13)
    {"id": 5, "quadros": list(range(51, 61)), "audio_parts": [5]},   # Q51-Q60 (10)
]

# ---------------------------------------------------------------------------
# TITULOS DAS CENAS — extraidos do storyboard
# ---------------------------------------------------------------------------
TITULOS_CENAS = {
    # Batch 1 — Gancho
    1:  "GANCHO — TELA PRETA",
    2:  "O PASTOR NA TRIBUNA",
    3:  "A VENDA — CARROS E CASAS",
    4:  "A PORTA DESTRANCADA",
    5:  "O NOME — JOSHUA MHLAKELA",
    6:  "A DATA CRAVADA — 23 SET 2025",
    7:  "VIRAL — RAPTURETOK 300 MIL",
    8:  "A LUA DE SANGUE",
    9:  "A CONTAGEM REGRESSIVA",
    10: "O DIA QUE CHEGOU",
    11: "OS ARRUINADOS",
    12: "A REGRA QUE ELE QUEBROU",
    # Batch 2 — O Versiculo que Todos Ignoram
    13: "ABERTURA — MATEUS 24:36",
    14: "JESUS FALANDO",
    15: "A TRINDADE",
    16: "NINGUEM SABE — A CITACAO",
    17: "NEM OS ANJOS",
    18: "DUAS OPCOES",
    19: "WILLIAM MILLER — 1844",
    20: "O GRANDE DESAPONTAMENTO",
    21: "HAROLD CAMPING — RADIO",
    22: "WHISENANT — 88 RAZOES",
    23: "DOIS MIL ANOS DE ERROS",
    24: "LADRAO DE NOITE",           # FALTANTE — text_screen
    # Batch 3 — O que a Biblia Realmente Diz
    25: "O ANJO COM TROMBETA",
    26: "1 TESSALONICENSES — PAULO",
    27: "O SENHOR DESCE",
    28: "ALARIDO — SOM SOBRENATURAL",
    29: "VOZ DE ARCANJO MIGUEL",
    30: "TROMBETA DE DEUS",
    31: "MORTOS RESSUSCITANDO",
    32: "OS VIVOS ARREBATADOS",
    33: "EVENTO FISICO GLOBAL",
    34: "DIAS DE NOE",
    35: "NORMALIDADE — FESTA",
    36: "A PERGUNTA SILENCIOSA",
    37: "DECISAO JA TOMADA",
    # Batch 4 — Os Sinais sao Reais
    38: "SINAIS EXISTEM — ROLO",
    39: "SINAIS VS DATAS — BUSSOLA",
    40: "LUA VERMELHA — SETEMBRO",
    41: "JOEL 2:31",
    42: "RELOGIO DO JUIZO FINAL",    # FALTANTE — text_screen
    43: "2 TIMOTEO 3",               # FALTANTE — text_screen
    44: "FEED MODERNO — REDES SOCIAIS",
    45: "NACAO CONTRA NACAO",
    46: "RUSSIA UCRANIA — ISRAEL",
    47: "FOME E PESTE",
    48: "TERREMOTOS",
    49: "JANELA ABERTA",
    50: "PROXIMIDADE REAL",          # FALTANTE — text_screen
    # Batch 5 — Urgencia Real + CTA
    51: "A ARMADILHA DAS DATAS",
    52: "CALENDARIO VS ALMA",
    53: "MATEUS 24:42 — VELAI",
    54: "VELAR NAO E CALCULAR",
    55: "DOIS TIPOS DE CRISTAO",     # FALTANTE — text_screen
    56: "SINAIS REAIS — VOLTA CERTA", # FALTANTE — text_screen
    57: "TEASER — CAVALO VERMELHO",
    58: "O CAVALO CAVALGA",
    59: "CTA — DEIXE UM COMENTARIO",
    60: "FECHAMENTO — TELA PRETA",
}

# ---------------------------------------------------------------------------
# EFEITOS KEN BURNS por quadro
# ---------------------------------------------------------------------------
EFFECTS_MAP = {
    # Batch 1
    1:  "zoom_in",    # brasa — push-in
    2:  "zoom_in",    # pastor — zoom in no pulpito
    3:  "zoom_out",   # mesa overhead — zoom out revelando
    4:  "zoom_in",    # porta destrancada — push-in
    5:  "zoom_in",    # silhueta microfone — zoom in
    6:  "zoom_in",    # calendario 23 SET — zoom in circulo
    7:  "zoom_out",   # parede celulares — zoom out
    8:  "zoom_in",    # lua de sangue — push-in lentissimo
    9:  "zoom_in",    # relogio de bolso — zoom in ponteiro
    10: "zoom_out",   # calendario arrancado — zoom out
    11: "zoom_in",    # familia arruinada — push-in Biblia
    12: "zoom_in",    # Biblia Mateus 24 — zoom in versiculo
    # Batch 2
    13: "zoom_in",    # Biblia monumental — push-in
    14: "zoom_in",    # Cristo — zoom in rosto
    15: "zoom_in",    # tres velas — zoom in
    16: "zoom_in",    # NINGUEM — zoom in palavra
    17: "pan_right",  # coro de anjos — pan direita
    18: "zoom_in",    # balanca — zoom in desequilibrando
    19: "zoom_out",   # multidao 1844 — zoom out
    20: "pan_right",  # jornais — pan direita
    21: "zoom_in",    # microfone radio — zoom in
    22: "zoom_in",    # livro 88 — push-in capa
    23: "pan_right",  # galeria pergaminhos — pan direita
    24: "zoom_in",    # ladrao de noite — zoom in chave (FALTANTE)
    # Batch 3
    25: "zoom_out",   # anjo com trombeta — zoom out asas
    26: "zoom_in",    # Paulo escrevendo — push-in mao
    27: "zoom_in",    # Cristo descendo — pull-up
    28: "zoom_in",    # boca do arcanjo — zoom in ondas
    29: "zoom_out",   # arcanjo Miguel — zoom out asas
    30: "zoom_in",    # trombeta — zoom in abertura
    31: "pan_right",  # cemiterio aberto — pan esquerda-direita
    32: "zoom_in",    # silhuetas ascendendo — pull-up
    33: "zoom_in",    # planeta Terra — rotacao sutil
    34: "pan_right",  # arca de Noe — pan direita
    35: "zoom_out",   # banquete tsunami — zoom out revelando onda
    36: "zoom_in",    # espelho — push-in
    37: "zoom_in",    # caminho bifurcado — zoom in cruzamento
    # Batch 4
    38: "pan_right",  # rolo sinais — pan direita
    39: "zoom_in",    # bussola — zoom in agulha
    40: "zoom_in",    # lua vermelha Brasil — push-in lento
    41: "zoom_in",    # Joel 2 — zoom in versiculo
    42: "zoom_in",    # relogio 85s — zoom in ponteiro (FALTANTE)
    43: "pan_right",  # 2 Timoteo — pan lenta (FALTANTE)
    44: "zoom_out",   # feed celulares — zoom out
    45: "pan_right",  # tres silhuetas — pan entre elas
    46: "pan_right",  # tanque + pergaminho — pan direita
    47: "zoom_in",    # mesa vazia fome — zoom in tigela
    48: "zoom_in",    # rachadura magma — zoom in
    49: "zoom_in",    # janela gotica — push-in
    50: "zoom_in",    # ampulheta — zoom in graos (FALTANTE)
    # Batch 5
    51: "zoom_in",    # armadilha — push-in
    52: "zoom_in",    # split calendario/coracao — push-in coracao
    53: "zoom_in",    # Mateus 24:42 — zoom in versiculo
    54: "zoom_out",   # sentinela — zoom out torre
    55: "pan_right",  # split dois cristos — pan esquerda-direita (FALTANTE)
    56: "zoom_in",    # altar tres elementos — rotacao (FALTANTE)
    57: "zoom_in",    # cavaleiro vermelho — push-in
    58: "zoom_in",    # cascos em movimento — zoom in
    59: "zoom_in",    # mao escrevendo — zoom in pena
    60: "zoom_out",   # brasa final — zoom out
}

# ---------------------------------------------------------------------------
# GRADE por quadro
# ---------------------------------------------------------------------------
GRADE_MAP = {
    # Batch 1
    1:  "biblical",     # brasa — abertura ominosa
    2:  "biblical",     # pastor — manipulacao carısmatica
    3:  "apocalypse",   # mesa de venda — renúncia material
    4:  "apocalypse",   # porta destrancada — abandono
    5:  "revelation",   # silhueta microfone — suspense
    6:  "biblical",     # calendario — marcacao profetica
    7:  "apocalypse",   # viral TikTok — panico
    8:  "biblical",     # lua de sangue — presagio
    9:  "revelation",   # relogio de bolso — tempo correndo
    10: "apocalypse",   # calendario arrancado — vazio fracasso
    11: "apocalypse",   # familia arruinada — desolacao
    12: "revelation",   # Biblia Mateus 24 — revelacao iminente
    # Batch 2
    13: "revelation",   # Biblia monumental — reverente
    14: "revelation",   # Cristo — autoridade divina
    15: "revelation",   # tres velas — sacralidade trinitaria
    16: "revelation",   # NINGUEM — revelacao textual
    17: "revelation",   # coro de anjos — humildade sagrada
    18: "revelation",   # balanca — dilema teologico
    19: "apocalypse",   # multidao 1844 — expectativa frustrada
    20: "apocalypse",   # jornais — fracasso documentado
    21: "apocalypse",   # microfone radio — transmissao obsoleta
    22: "revelation",   # livro 88 — best-seller enganoso
    23: "apocalypse",   # galeria pergaminhos — historico fracassos
    24: "biblical",     # ladrao de noite — invasao silenciosa (FALTANTE)
    # Batch 3
    25: "revelation",   # anjo trombeta — solenidade doutrinaria
    26: "revelation",   # Paulo escrevendo — autoria apostolica
    27: "revelation",   # Cristo descendo — epifania
    28: "revelation",   # boca do arcanjo — explosao cosmica
    29: "revelation",   # arcanjo Miguel — majestade angelical
    30: "revelation",   # trombeta — convocacao militar divina
    31: "revelation",   # cemiterio aberto — ressurreicao gloriosa
    32: "revelation",   # silhuetas ascendendo — elevacao extatica
    33: "revelation",   # planeta Terra — dimensao planetaria
    34: "revelation",   # arca de Noe — paralelismo escatologico
    35: "apocalypse",   # banquete com tsunami — ignorancia fatal
    36: "revelation",   # espelho — auto-interrogacao
    37: "revelation",   # caminho bifurcado — encruzilhada
    # Batch 4
    38: "revelation",   # rolo sinais — revelacao profetica
    39: "revelation",   # bussola — orientacao profetica
    40: "biblical",     # lua vermelha — sinal cumprido
    41: "revelation",   # Joel 2 — autoridade profetica
    42: "biblical",     # relogio 85s — urgencia (FALTANTE)
    43: "revelation",   # 2 Timoteo — diagnostico espiritual (FALTANTE)
    44: "apocalypse",   # feed celulares — cumprimento contemporaneo
    45: "apocalypse",   # tres silhuetas — geopolitica apocaliptica
    46: "apocalypse",   # tanque — conflito atual
    47: "apocalypse",   # mesa fome — escassez global
    48: "apocalypse",   # rachadura — desastre telúrico
    49: "revelation",   # janela gotica — iminencia real
    50: "revelation",   # ampulheta — tempo esgotando (FALTANTE)
    # Batch 5
    51: "biblical",     # armadilha — advertencia
    52: "revelation",   # split calendario/coracao — dicotomia espiritual
    53: "revelation",   # Mateus 24:42 — comando direto de Cristo
    54: "revelation",   # sentinela — vigilancia fiel
    55: "revelation",   # dois tipos de cristao — contraste etico (FALTANTE)
    56: "revelation",   # sintese doutrinaria (FALTANTE)
    57: "biblical",     # cavaleiro vermelho — cliffhanger
    58: "biblical",     # cascos — profecia em movimento
    59: "revelation",   # mao escrevendo — convite direto
    60: "apocalypse",   # brasa final — encerramento
}


# ---------------------------------------------------------------------------
# COLOR GRADING
# ---------------------------------------------------------------------------

def grade_biblical(frame):
    """Quente, carmesim profundo — fogo, guerra, julgamento."""
    f = frame.astype(np.float32)
    np.multiply(f[:, :, 0], 1.15, out=f[:, :, 0])
    np.multiply(f[:, :, 1], 0.92, out=f[:, :, 1])
    np.multiply(f[:, :, 2], 0.85, out=f[:, :, 2])
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)


def grade_apocalypse(frame):
    """Desaturado 70% + dourado — desolacao, fim do mundo."""
    f = frame.astype(np.float32)
    gray = 0.299 * f[:, :, 0] + 0.587 * f[:, :, 1] + 0.114 * f[:, :, 2]
    for c in range(3):
        f[:, :, c] = f[:, :, c] * 0.3 + gray * 0.7
    np.multiply(f[:, :, 0], 1.10, out=f[:, :, 0])
    np.multiply(f[:, :, 1], 1.00, out=f[:, :, 1])
    np.multiply(f[:, :, 2], 0.80, out=f[:, :, 2])
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)


def grade_revelation(frame):
    """Sombras profundas, realce dourado — visoes, profetas, anjos."""
    f = frame.astype(np.float32)
    mask = f > 128
    f[mask] *= 1.05
    np.multiply(f[:, :, 0], 1.08, out=f[:, :, 0])
    np.multiply(f[:, :, 2], 0.88, out=f[:, :, 2])
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)


GRADE_FNS = {
    "biblical":   grade_biblical,
    "apocalypse": grade_apocalypse,
    "revelation": grade_revelation,
}


# ---------------------------------------------------------------------------
# KEN BURNS (lazy loading)
# ---------------------------------------------------------------------------

def ken_burns(img_path, duration, effect="zoom_in", fps=30):
    """Lazy: le dimensoes agora, pixels so no make_frame."""
    _cache = [None]

    def make_frame(t):
        if _cache[0] is None:
            _cache[0] = (
                np.array(
                    Image.open(img_path).convert("RGB").resize((W, H), Image.LANCZOS)
                ).astype(np.float32)
            )
        progress = t / max(duration, 0.001)

        if effect == "zoom_in":
            scale = 1.0 + 0.08 * progress
        elif effect == "zoom_out":
            scale = 1.08 - 0.08 * progress
        elif effect in ("pan_left", "pan_right"):
            scale = 1.04
        else:
            scale = 1.0

        if scale != 1.0:
            nw = int(W * scale)
            nh = int(H * scale)
            img_big = cv2.resize(_cache[0].astype(np.uint8), (nw, nh))
            ox = (nw - W) // 2
            oy = (nh - H) // 2
            if effect == "pan_left":
                ox = int((nw - W) * progress)
            elif effect == "pan_right":
                ox = int((nw - W) * (1.0 - progress))
            f = img_big[oy: oy + H, ox: ox + W].astype(np.float32)
        else:
            f = _cache[0].copy()

        return np.clip(f, 0, 255).astype(np.uint8)

    clip = VideoClip(make_frame, duration=duration)
    clip.fps = fps
    return clip


def kb_with_grade(img_path, duration, effect, grade_fn):
    """Ken Burns + color grading frame a frame."""
    base = ken_burns(img_path, duration, effect)

    def make_frame_graded(t):
        return grade_fn(base.make_frame(t))

    clip = VideoClip(make_frame_graded, duration=duration)
    clip.fps = FPS
    return clip


# ---------------------------------------------------------------------------
# TELA DE TEXTO (PIL) — fallback para quadros faltantes
# ---------------------------------------------------------------------------

def text_screen(text, duration, bg=(0, 0, 0), color=(197, 163, 85), fontsize=64):
    """Tela preta com texto centralizado em dourado."""
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
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((W - tw) // 2, (H - th) // 2), text, fill=color, font=font)
    arr = np.array(img)
    clip = VideoClip(lambda t: arr, duration=duration)
    clip.fps = FPS
    return clip


def text_screen_faltante(titulo, duration):
    """
    Tela especial para quadros faltantes: fundo preto, titulo em dourado,
    subtitulo em vermelho indicando que a imagem ainda nao foi gerada.
    """
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font_titulo = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 64)
        font_sub    = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 36)
    except Exception:
        font_titulo = ImageFont.load_default()
        font_sub    = font_titulo

    color_titulo = (197, 163, 85)   # dourado
    color_sub    = (139, 0, 0)      # vermelho sangue

    # Titulo
    bbox = draw.textbbox((0, 0), titulo, font=font_titulo)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((W - tw) // 2, H // 2 - th - 20), titulo, fill=color_titulo, font=font_titulo)

    # Subtitulo
    sub = "[IMAGEM NAO GERADA]"
    sbbox = draw.textbbox((0, 0), sub, font=font_sub)
    sw = sbbox[2] - sbbox[0]
    draw.text(((W - sw) // 2, H // 2 + 20), sub, fill=color_sub, font=font_sub)

    arr = np.array(img)
    clip = VideoClip(lambda t: arr, duration=duration)
    clip.fps = FPS
    return clip


# ---------------------------------------------------------------------------
# RENDER BATCH
# ---------------------------------------------------------------------------

def render_batch(batch):
    bid        = batch["id"]
    quadros    = batch["quadros"]
    audio_part = batch["audio_parts"][0]
    dur_total  = PARTE_DUR[audio_part]

    n_img_quadros = len(quadros) - 1
    dur_per_q = max(5.0, (dur_total - 2.5) / max(n_img_quadros, 1))

    print(
        f"[BATCH {bid}] {len(quadros)} quadros | {dur_total}s total | "
        f"{dur_per_q:.1f}s/quadro",
        flush=True,
    )

    clips = []

    # Tela de abertura — titulo real da cena Q01 do batch
    q_first       = quadros[0]
    titulo_abert  = TITULOS_CENAS.get(q_first, f"PARTE {bid}")
    clips.append(text_screen(titulo_abert, 2.5))

    # Demais quadros
    for q in quadros[1:]:
        titulo_q = TITULOS_CENAS.get(q, f"Q{q:02d}")

        # Quadro faltante — usar text_screen especial
        if q in QUADROS_FALTANTES:
            print(f"  [FALTANTE] Q{q:02d} — text_screen: {titulo_q}", flush=True)
            clips.append(text_screen_faltante(titulo_q, dur_per_q))
            continue

        img_path = ASSETS / f"Q{q:02d}.png"
        if not img_path.exists():
            print(f"  [AVISO] {img_path.name} nao encontrado — usando text_screen", flush=True)
            clips.append(text_screen_faltante(titulo_q, dur_per_q))
            continue

        effect    = EFFECTS_MAP.get(q, "zoom_in")
        grade_key = GRADE_MAP.get(q, "biblical")
        grade_fn  = GRADE_FNS[grade_key]

        clips.append(kb_with_grade(img_path, dur_per_q, effect, grade_fn))

    # --- render video silencioso ---
    silent_path = OUT / f"parte_{bid:02d}_silent.mp4"
    final_path  = OUT / f"parte_{bid:02d}.mp4"

    video = concatenate_videoclips(clips, method="chain")
    video.write_videofile(str(silent_path), **WRITE_OPTS)
    video.close()
    del video, clips
    gc.collect()

    # --- mix ffmpeg ---
    audio_file = PARTES_AUDIO[audio_part - 1]
    if not audio_file.exists():
        print(
            f"[AVISO] Audio nao encontrado: {audio_file.name} — copiando sem audio",
            flush=True,
        )
        import shutil
        shutil.copy(silent_path, final_path)
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
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            str(final_path),
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(silent_path),
            "-i", str(audio_file),
            "-filter_complex", "[1:a]volume=1.0[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            str(final_path),
        ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERRO ffmpeg batch {bid}]\n{result.stderr[-600:]}", flush=True)
        return False

    silent_path.unlink(missing_ok=True)
    print(f"[OK] parte_{bid:02d}.mp4 gerado em {final_path}", flush=True)
    return True


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--only-batch", type=int, default=None)
    args, _ = parser.parse_known_args()

    if args.only_batch is not None:
        batch = next((b for b in BATCHES if b["id"] == args.only_batch), None)
        if batch is None:
            print(f"[ERRO] Batch {args.only_batch} nao encontrado.", flush=True)
            sys.exit(1)
        ok = render_batch(batch)
        sys.exit(0 if ok else 1)

    print("=" * 60, flush=True)
    print("PHANTASMA — video-014-arrebatamento", flush=True)
    print(f"Assets: {ASSETS}", flush=True)
    print(f"Output: {OUT}", flush=True)
    print(
        f"Quadros faltantes: {sorted(QUADROS_FALTANTES)} "
        "(serao substituidos por tela de titulo)",
        flush=True,
    )
    print("=" * 60, flush=True)

    script = str(Path(__file__).resolve())
    resultados = {}

    for batch in BATCHES:
        bid = batch["id"]
        print(f"\n--- Iniciando Batch {bid} ---", flush=True)
        result = subprocess.run(
            [sys.executable, script, "--only-batch", str(bid)]
        )
        ok = result.returncode == 0
        resultados[bid] = ok
        print(f"Batch {bid}: {'OK' if ok else 'ERRO'}", flush=True)

    print("\n--- RESUMO ---", flush=True)
    for bid, ok in resultados.items():
        status = "OK" if ok else "ERRO"
        print(f"  Batch {bid}: {status}", flush=True)

    total_ok = sum(resultados.values())
    print(f"\n{total_ok}/{len(BATCHES)} batches concluidos.", flush=True)


if __name__ == "__main__":
    main()
