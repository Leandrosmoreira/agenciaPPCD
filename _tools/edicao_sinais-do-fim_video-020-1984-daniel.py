"""
PHANTASMA — Editor Cinematográfico
Vídeo: video-020-1984-daniel
Canal: Sinais do Fim — Passagens do Apocalipse
Título: "1984 É ASSUSTADOR... Mas Daniel 7:25 Descreveu o Grande Irmão 2.500 Anos Antes"
Gerado por: Phantasma (MoviePy + Ken Burns + Color Grading)
Data: 2026-04-17

Blocos:
  PARTE 1 — GANCHO + PROMESSA       (Q01–Q12)
  PARTE 2 — A QUARTA BESTA          (Q13–Q24)
  PARTE 3 — OPERAÇÃO DE ERRO        (Q25–Q36)
  PARTE 4 — CHINA E A MARCA         (Q37–Q48)
  PARTE 5 — O'BRIEN E A ESPERANÇA   (Q49–Q60)

Grade dominante: grade_apocalypse (tom orwelliano/dessaturado)
Toque de: grade_biblical (dourado sagrado nos momentos proféticos)
"""

import gc, os, sys, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from moviepy.editor import VideoClip, VideoFileClip, concatenate_videoclips

ROOT   = Path(__file__).resolve().parent.parent
CANAL  = ROOT / "canais/sinais-do-fim"
VIDEO  = CANAL / "videos/video-020-1984-daniel"
ASSETS = VIDEO / "6-assets"
AUDIO  = VIDEO / "5-audio"
OUT    = VIDEO / "7-edicao"
OUT.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1920, 1080, 30

# Duração de cada parte em segundos (baseado em 12min total / 5 partes)
# Parte 1: Q01–Q12 (gancho 20s + promessa 80s = ~100s + margem) → 150s
# Parte 2: Q13–Q24 (~90s bloco quarta besta + transição) → 150s
# Parte 3: Q25–Q36 (~120s operação de erro) → 150s
# Parte 4: Q37–Q48 (~150s china e marca) → 150s
# Parte 5: Q49–Q60 (~120s o'brien + esperança + CTA) → 150s
PARTE_DUR = {1: 150.0, 2: 150.0, 3: 150.0, 4: 150.0, 5: 150.0}

PARTES_AUDIO = [AUDIO / f"parte{n}.mp3" for n in range(1, 6)]
TRILHA = AUDIO / "trilha.MP3"

# Clips Veo3 — quadros com vídeo animado em 6-assets/veo3/
VEO_DIR    = ASSETS / "veo3"
VEO_QUADROS = {3, 4, 5, 6}   # VEO_Q03–Q06 gerados (Q02 Ken Burns zoom_in)

# Trilhas por batch (Trilha1→partes 1-2, Trilha2→partes 3-4, Trilha3→parte 5)
TRILHAS_POR_BATCH = {
    1: AUDIO / "Trilha1.mp3",
    2: AUDIO / "Trilha1.mp3",
    3: AUDIO / "Trilha2.mp3",
    4: AUDIO / "Trilha2.mp3",
    5: AUDIO / "Trilha3.mp3",
}

# Override de efeito para Q02 (Snayder: zoom_in)
EFFECT_OVERRIDE = {2: "zoom_in"}

WRITE_OPTS = dict(
    codec="libx264", audio=False,
    fps=FPS, preset="ultrafast",
    threads=1, bitrate="5000k",
    ffmpeg_params=["-refs", "1", "-bf", "0"]
)

# ---------------------------------------------------------------------------
# TÍTULOS DOS BLOCOS — extraídos do storyboard (Nyx 2026-04-17)
# Usados nas telas de texto de abertura de cada parte
# ---------------------------------------------------------------------------
PARTE_TITULOS = {
    1: "GANCHO · PROMESSA",
    2: "A QUARTA BESTA",
    3: "OPERAÇÃO DE ERRO",
    4: "CHINA E A MARCA",
    5: "O'BRIEN E A ESPERANÇA",
}

# Subtítulos descritivos para contexto na tela
PARTE_SUBTITULOS = {
    1: "Daniel 7:25 × George Orwell",
    2: "Três ações do sistema final",
    3: "Energeia Planes — atividade ativa de engano",
    4: "Setecentos milhões de olhos",
    5: "Não existe — e o que vem depois",
}

# ---------------------------------------------------------------------------
# MAPEAMENTO Q → descrição curta (fallback quando imagem ausente)
# ---------------------------------------------------------------------------
QUADRO_DESCRICAO = {
    1:  "A máquina de escrever tuberculosa",
    2:  "O túmulo de Eric Arthur Blair",
    3:  "Bíblia + Daniel 7 + A pergunta",
    4:  "Ilha de Jura — Orwell escreve",
    5:  "Guerra Civil Espanhola",
    6:  "A GUERRA É PAZ · A LIBERDADE É ESCRAVIDÃO · A IGNORÂNCIA É FORÇA",
    7:  "Isaías 5:20 — Profeta hebreu",
    8:  "Dois eixos temporais — Isaías e Orwell",
    9:  "Daniel jovem em cativeiro — Babilônia",
    10: "Visões da noite — as quatro bestas",
    11: "Dentes de ferro — Daniel 7:7",
    12: "Quatro impérios em miniatura",
    13: "Três ações específicas — PALAVRAS · TEMPOS · LEI",
    14: "Ministério do Amor — câmara de interrogatório",
    15: "Crimidéia — crime de pensamento",
    16: "Ministério da Verdade — memory hole",
    17: "Não-pessoas — rostos apagados",
    18: "Mudar a lei — balança enferrujada",
    19: "Culpa permanente — figura isolada",
    20: "A pergunta ao espectador",
    21: "Paulo escreve — cela romana",
    22: "Energeia planes — pergaminho grego",
    23: "Duplipensar — dois cérebros",
    24: "Ministério da Verdade exterior",
    25: "Ministério da Paz — mesa de guerra",
    26: "Ministério da Abundância — RAÇÃO VITÓRIA",
    27: "Ministério do Amor — porta de ferro",
    28: "Ministério da Verdade — impressora rotativa",
    29: "Isaías ecoa — quatro placas em pergaminho",
    30: "Dois homens, dois milênios",
    31: "A engrenagem — dois mil e quinhentos anos",
    32: "Transição — anjo sobre a cidade vigiada",
    33: "Setecentos milhões de câmeras",
    34: "Uma câmera para cada dois habitantes",
    35: "Sistema de Crédito Social — pontuação 350",
    36: "Não embarca — portão bloqueado",
    37: "Telão de desconfiáveis — praça chinesa",
    38: "Apocalipse 13 — marca na palma",
    39: "Comprar e vender — scanner vermelho",
    40: "CBDC — cento e trinta países",
    41: "Moeda programável — código com validade",
    42: "Qumran — fragmento de Daniel",
    43: "Antes de tudo — linha do tempo profética",
    44: "Arquitetura de controle — pirâmide de três níveis",
    45: "Winston sem conta — GIN VITÓRIA",
    46: "Quem pode guerrear contra ela?",
    47: "O'Brien na cela — revelação traidora",
    48: "Não existe — sentença final",
    49: "Contraste — câmara cinza × portão celestial",
    50: "Hospital de Londres — morte silenciosa",
    51: "The Last Man in Europe",
    52: "1948 invertido → 1984",
    53: "Daniel ancião — sem cor no rosto",
    54: "Cavernas de Qumran — Mar Morto",
    55: "Israel Antiquities Authority",
    56: "Quatro citações — síntese profética",
    57: "Daniel viu · Orwell nomeou · O mundo constrói",
    58: "A escolha — enquanto ainda há escolha",
    59: "Qual ministério você já vê hoje?",
    60: "Encerramento — Daniel 7, selo final",
}

# ---------------------------------------------------------------------------
# COLOR GRADING
# ---------------------------------------------------------------------------

def grade_biblical(frame):
    """Dourado sagrado — tons quentes bíblicos (vermelhos +, azuis -)"""
    f = frame.astype(np.float32)
    np.multiply(f[:, :, 0], 1.15, out=f[:, :, 0])
    np.multiply(f[:, :, 1], 0.92, out=f[:, :, 1])
    np.multiply(f[:, :, 2], 0.85, out=f[:, :, 2])
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)


def grade_apocalypse(frame):
    """Tom orwelliano — dessatura, empurra para cinza com toque sangue (dominante)"""
    f = frame.astype(np.float32)
    gray = 0.299 * f[:, :, 0] + 0.587 * f[:, :, 1] + 0.114 * f[:, :, 2]
    for c in range(3):
        f[:, :, c] = f[:, :, c] * 0.3 + gray * 0.7
    np.multiply(f[:, :, 0], 1.1,  out=f[:, :, 0])
    np.multiply(f[:, :, 2], 0.8,  out=f[:, :, 2])
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)


def grade_revelation(frame):
    """Revelação — leve boost em highlights, vermelho +, azul -"""
    f = frame.astype(np.float32)
    mask = f > 128
    f[mask] *= 1.05
    np.multiply(f[:, :, 0], 1.08, out=f[:, :, 0])
    np.multiply(f[:, :, 2], 0.88, out=f[:, :, 2])
    np.clip(f, 0, 255, out=f)
    return f.astype(np.uint8)

# ---------------------------------------------------------------------------
# KEN BURNS
# ---------------------------------------------------------------------------

def ken_burns(img_path, duration, effect="zoom_in"):
    """Anima imagem estática com efeito Ken Burns (zoom / pan)."""
    _cache = [None]

    def make_frame(t):
        if _cache[0] is None:
            _cache[0] = np.array(
                Image.open(img_path).convert("RGB").resize((W, H), Image.LANCZOS)
            ).astype(np.float32)
        f = _cache[0].copy()
        progress = t / max(duration, 0.001)
        scale = 1.0

        if effect == "zoom_in":
            scale = 1.0 + 0.08 * progress
        elif effect == "zoom_out":
            scale = 1.08 - 0.08 * progress
        elif effect in ("pan_left", "pan_right"):
            scale = 1.04

        if scale != 1.0:
            nw, nh = int(W * scale), int(H * scale)
            big = cv2.resize(_cache[0].astype(np.uint8), (nw, nh))
            ox = (nw - W) // 2
            oy = (nh - H) // 2
            if effect == "pan_left":
                ox = int((nw - W) * progress)
            elif effect == "pan_right":
                ox = int((nw - W) * (1 - progress))
            f = big[oy:oy + H, ox:ox + W].astype(np.float32)

        return np.clip(f, 0, 255).astype(np.uint8)

    c = VideoClip(make_frame, duration=duration)
    c.fps = FPS
    return c


def kb_with_grade(img_path, duration, effect, grade_fn):
    """Ken Burns + color grading combinados."""
    base = ken_burns(img_path, duration, effect)

    def mf(t):
        return grade_fn(base.make_frame(t))

    c = VideoClip(mf, duration=duration)
    c.fps = FPS
    return c


def veo_with_grade(veo_path, grade_fn):
    """Carrega clip Veo3 MP4 e aplica color grading frame a frame."""
    base = VideoFileClip(str(veo_path), audio=False)
    base = base.resize((W, H))

    def mf(t):
        frame = base.get_frame(min(t, base.duration - 1 / FPS))
        return grade_fn(frame)

    c = VideoClip(mf, duration=base.duration)
    c.fps = FPS
    return c

# ---------------------------------------------------------------------------
# TELAS DE TEXTO
# ---------------------------------------------------------------------------

def text_screen(text, duration, bg=(0, 0, 0), color=(197, 163, 85), fontsize=72,
                subtitle=None):
    """
    Gera clipe de tela preta com texto centralizado.
    bg=(0,0,0) = preto #0A0A0A do canal
    color=(197,163,85) = dourado envelhecido #C5A355
    """
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)

    # Fonte principal
    try:
        font = ImageFont.truetype("arial.ttf", fontsize)
    except OSError:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", fontsize)
        except OSError:
            font = ImageFont.load_default()

    # Centraliza texto principal
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    y_main = (H - th) // 2 if subtitle is None else (H // 2 - th - 20)
    draw.text(((W - tw) // 2, y_main), text, fill=color, font=font)

    # Subtítulo (se fornecido)
    if subtitle:
        try:
            font_sub = ImageFont.truetype("arial.ttf", fontsize // 2)
        except OSError:
            try:
                font_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", fontsize // 2)
            except OSError:
                font_sub = ImageFont.load_default()
        bbox_s = draw.textbbox((0, 0), subtitle, font=font_sub)
        sw = bbox_s[2] - bbox_s[0]
        draw.text(((W - sw) // 2, H // 2 + 20), subtitle,
                  fill=(139, 0, 0), font=font_sub)  # vermelho sangue #8B0000

    arr = np.array(img)
    c = VideoClip(lambda t: arr, duration=duration)
    c.fps = FPS
    return c


def fallback_screen(quadro_num, duration):
    """Tela de fallback quando imagem não existe: mostra número e descrição do quadro."""
    desc = QUADRO_DESCRICAO.get(quadro_num, f"Quadro {quadro_num:02d}")
    label = f"Q{quadro_num:02d}"
    return text_screen(
        label, duration,
        bg=(10, 10, 10),
        color=(197, 163, 85),
        fontsize=80,
        subtitle=desc[:60] + ("…" if len(desc) > 60 else "")
    )

# ---------------------------------------------------------------------------
# SEQUÊNCIAS DE EFEITO E GRADE POR BLOCO
#
# Lógica temática video-020:
#   - Quadros proféticos/bíblicos (Daniel, Paulo, pergaminhos) → grade_biblical
#   - Quadros orwellianos/distópicos (Oceânia, Winston, ministérios) → grade_apocalypse (dominante)
#   - Quadros de revelação/esperança/CTA → grade_revelation
#
# Padrão de efeitos: alterna zoom_in / zoom_out / pan_left / pan_right / zoom_in…
# ---------------------------------------------------------------------------

# grade_apocalypse é a grade dominante do vídeo (tema orwelliano)
# grade_biblical aparece nos quadros proféticos
# grade_revelation aparece nos quadros de esperança e CTA

# Grade por quadro (Q01–Q60)
# B = biblical, A = apocalypse, R = revelation
QUADRO_GRADE = {
    # BLOCO 0 — GANCHO
    1:  grade_apocalypse,   # máquina de escrever — suspense terminal
    2:  grade_apocalypse,   # túmulo — elegíaco
    3:  grade_biblical,     # Bíblia aberta Daniel 7 — sagrado
    # BLOCO 1 — PROMESSA
    4:  grade_apocalypse,   # ilha isolada
    5:  grade_apocalypse,   # guerra civil
    6:  grade_apocalypse,   # lema do partido — frio, absoluto
    7:  grade_biblical,     # Isaías — oracular
    8:  grade_biblical,     # díptico Isaías × Orwell — vertigem temporal
    9:  grade_biblical,     # Daniel jovem em cativeiro
    10: grade_revelation,   # visões da noite — quatro bestas
    11: grade_apocalypse,   # dentes de ferro — visceral
    12: grade_biblical,     # quatro impérios — profético
    # BLOCO 2 — A QUARTA BESTA
    13: grade_revelation,   # três chamas — revelação tríplice
    14: grade_apocalypse,   # câmara de interrogatório — clínico
    15: grade_apocalypse,   # crimidéia — paranoia
    16: grade_apocalypse,   # memory hole — burocracia totalitária
    17: grade_apocalypse,   # não-pessoas — horror silencioso
    18: grade_apocalypse,   # mudar a lei — arbitrariedade
    19: grade_apocalypse,   # culpa permanente
    20: grade_revelation,   # pergunta ao espectador
    21: grade_biblical,     # Paulo escreve — escritor profético
    22: grade_biblical,     # energeia planes — grego sagrado
    # BLOCO 3 — OPERAÇÃO DE ERRO
    23: grade_apocalypse,   # duplipensar — abstração grotesca
    24: grade_apocalypse,   # Ministério da Verdade exterior
    25: grade_apocalypse,   # Ministério da Paz
    26: grade_apocalypse,   # Ministério da Abundância
    27: grade_apocalypse,   # Ministério do Amor — porta de ferro
    28: grade_apocalypse,   # fábrica de falsificação
    29: grade_biblical,     # Isaías ecoa — confirmação circular
    30: grade_biblical,     # dois homens, dois milênios
    31: grade_biblical,     # engrenagem profética
    32: grade_revelation,   # transição — anjo sobre cidade vigiada
    33: grade_apocalypse,   # 700 milhões de câmeras
    34: grade_apocalypse,   # uma câmera por cada dois
    # BLOCO 4 — CHINA E A MARCA
    35: grade_apocalypse,   # crédito social — julgamento algorítmico
    36: grade_apocalypse,   # não embarca — exclusão mecânica
    37: grade_apocalypse,   # telão de desconfiáveis
    38: grade_revelation,   # Apocalipse 13 — marca na palma
    39: grade_apocalypse,   # comprar e vender — scanner vermelho
    40: grade_apocalypse,   # CBDC — 130 países
    41: grade_apocalypse,   # moeda programável
    42: grade_biblical,     # Qumran — evidência arqueológica
    43: grade_biblical,     # linha do tempo profética
    44: grade_biblical,     # arquitetura de controle — pirâmide
    45: grade_apocalypse,   # Winston sem conta
    46: grade_revelation,   # quem pode guerrear — adoração apocalíptica
    # BLOCO 5 — O'BRIEN E A ESPERANÇA
    47: grade_apocalypse,   # O'Brien — traição
    48: grade_apocalypse,   # não existe — sentença final
    49: grade_revelation,   # contraste câmara cinza × portão celestial
    50: grade_apocalypse,   # hospital — morte silenciosa
    51: grade_apocalypse,   # The Last Man in Europe
    52: grade_apocalypse,   # 1948 → 1984
    53: grade_biblical,     # Daniel ancião — trauma profético
    # BLOCO 6 — PERGUNTA FINAL + CTA
    54: grade_biblical,     # Qumran + Mar Morto — descoberta monumental
    55: grade_biblical,     # Israel Antiquities Authority
    56: grade_biblical,     # quatro citações — síntese profética
    57: grade_revelation,   # Daniel viu · Orwell nomeou · o mundo constrói
    58: grade_revelation,   # a escolha — convocação moral
    59: grade_revelation,   # CTA — qual ministério você já vê hoje?
    60: grade_biblical,     # encerramento — Daniel 7, selo final
}

# Efeito Ken Burns por quadro (rotação dentro do bloco)
_EFFECTS_CYCLE = [
    "zoom_in", "zoom_out", "pan_left", "zoom_in", "pan_right",
    "zoom_out", "zoom_in", "zoom_out", "pan_left", "zoom_in",
    "pan_right", "zoom_out",
]


def effect_for_quadro(q):
    """Retorna efeito Ken Burns para o quadro (1-based), baseado em ciclo de 12."""
    return _EFFECTS_CYCLE[(q - 1) % len(_EFFECTS_CYCLE)]

# ---------------------------------------------------------------------------
# BATCHES — distribuição dos 60 quadros em 5 partes
#
# Distribuição narrativa:
#   Parte 1 (Q01–Q12): Gancho (Q01–Q03) + Promessa (Q04–Q12)
#   Parte 2 (Q13–Q24): Quarta Besta (Q11 inicia) até Operação de Erro início
#   Parte 3 (Q25–Q36): Operação de Erro (Q21 inicia, Q25–Q36 aqui)
#   Parte 4 (Q37–Q48): China e a Marca
#   Parte 5 (Q49–Q60): O'Brien + Esperança + CTA
# ---------------------------------------------------------------------------
BATCHES = [
    {"id": 1, "titulo": PARTE_TITULOS[1], "subtitulo": PARTE_SUBTITULOS[1],
     "quadros": list(range(1, 13)),   "audio_parts": [1]},
    {"id": 2, "titulo": PARTE_TITULOS[2], "subtitulo": PARTE_SUBTITULOS[2],
     "quadros": list(range(13, 25)),  "audio_parts": [2]},
    {"id": 3, "titulo": PARTE_TITULOS[3], "subtitulo": PARTE_SUBTITULOS[3],
     "quadros": list(range(25, 37)),  "audio_parts": [3]},
    {"id": 4, "titulo": PARTE_TITULOS[4], "subtitulo": PARTE_SUBTITULOS[4],
     "quadros": list(range(37, 49)),  "audio_parts": [4]},
    {"id": 5, "titulo": PARTE_TITULOS[5], "subtitulo": PARTE_SUBTITULOS[5],
     "quadros": list(range(49, 61)),  "audio_parts": [5]},
]

# ---------------------------------------------------------------------------
# RENDER DE BATCH
# ---------------------------------------------------------------------------

def render_batch(batch):
    bid        = batch["id"]
    titulo     = batch["titulo"]
    subtitulo  = batch["subtitulo"]
    quadros    = batch["quadros"]
    ap         = batch["audio_parts"]

    print(f"\n[PHANTASMA] Renderizando PARTE {bid} — {titulo}", flush=True)

    # Tela de abertura da parte (título real do bloco, não genérico)
    clips = [text_screen(titulo, 2.5, subtitle=subtitulo)]

    dur_per_q = max(5.0, PARTE_DUR[ap[0]] / max(1, len(quadros)))

    for q in quadros:
        img_path = ASSETS / f"Q{q:02d}.png"
        effect   = EFFECT_OVERRIDE.get(q, effect_for_quadro(q))
        grade_fn = QUADRO_GRADE.get(q, grade_apocalypse)

        # Veo3 clip disponível para este quadro?
        veo_path = VEO_DIR / f"VEO_Q{q:02d}.mp4"
        if q in VEO_QUADROS and veo_path.exists():
            print(f"  [VEO3] Q{q:02d} — clip animado + {grade_fn.__name__}", flush=True)
            clips.append(veo_with_grade(veo_path, grade_fn))
            continue

        if not img_path.exists():
            print(f"  [FALLBACK] Q{q:02d} — imagem ausente, usando text_screen", flush=True)
            clips.append(fallback_screen(q, dur_per_q))
            continue

        print(f"  [OK] Q{q:02d} — {effect} + {grade_fn.__name__}", flush=True)
        clips.append(kb_with_grade(img_path, dur_per_q, effect, grade_fn))

    # Renderiza vídeo silencioso
    silent = OUT / f"parte_{bid:02d}_silent.mp4"
    final  = OUT / f"parte_{bid:02d}.mp4"

    v = concatenate_videoclips(clips, method="chain")
    v.write_videofile(str(silent), **WRITE_OPTS)
    v.close()
    del v, clips
    gc.collect()

    # Mixagem de áudio com ffmpeg
    audio_file = PARTES_AUDIO[ap[0] - 1]

    if not audio_file.exists():
        print(f"  [AVISO] Audio parte{ap[0]}.mp3 não encontrado — copiando sem áudio", flush=True)
        import shutil
        shutil.copy(silent, final)
        silent.unlink(missing_ok=True)
        return True

    trilha_path = TRILHAS_POR_BATCH.get(bid, TRILHAS_POR_BATCH[1])
    if trilha_path.exists():
        cmd = [
            "ffmpeg", "-y",
            "-i", str(silent),
            "-i", str(audio_file),
            "-i", str(trilha_path),
            "-filter_complex",
            "[1:a]volume=1.0[narr];[2:a]volume=0.22[music];[narr][music]amix=inputs=2:duration=first[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            str(final),
        ]
    else:
        print(f"  [INFO] Trilha {trilha_path.name} não encontrada — narração somente", flush=True)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(silent),
            "-i", str(audio_file),
            "-filter_complex", "[1:a]volume=1.0[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            str(final),
        ]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  [ERRO ffmpeg] {r.stderr[-500:]}", flush=True)
        return False

    silent.unlink(missing_ok=True)
    print(f"  [OK] {final.name} gerado", flush=True)
    return True

# ---------------------------------------------------------------------------
# MAIN — suporte a --only-batch para paralelismo controlado
# ---------------------------------------------------------------------------

def main():
    import argparse
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--only-batch", type=int, default=None)
    args, _ = p.parse_known_args()

    if args.only_batch is not None:
        b = next((x for x in BATCHES if x["id"] == args.only_batch), None)
        if b is None:
            print(f"[ERRO] Batch {args.only_batch} não encontrado.", file=sys.stderr)
            sys.exit(1)
        sys.exit(0 if render_batch(b) else 1)

    print("=" * 70, flush=True)
    print("PHANTASMA — video-020-1984-daniel", flush=True)
    print("1984 É ASSUSTADOR... Mas Daniel 7:25 Descreveu o Grande Irmão", flush=True)
    print("2.500 Anos Antes", flush=True)
    print("=" * 70, flush=True)

    # Verifica assets antes de começar
    total_imgs = sum(1 for q in range(1, 61) if (ASSETS / f"Q{q:02d}.png").exists())
    print(f"\n[INFO] Imagens disponíveis em 6-assets/imagens: {total_imgs}/60", flush=True)
    if total_imgs == 0:
        print("[AVISO] Nenhuma imagem encontrada — todas as cenas usarão text_screen fallback",
              flush=True)

    script = str(Path(__file__).resolve())
    resultados = {}

    for b in BATCHES:
        print(f"\n{'─'*50}", flush=True)
        print(f"Despachando PARTE {b['id']} — {b['titulo']}", flush=True)
        r = subprocess.run(
            [sys.executable, script, "--only-batch", str(b["id"])]
        )
        ok = r.returncode == 0
        resultados[b["id"]] = ok
        print(f"Batch {b['id']}: {'OK' if ok else 'ERRO'}", flush=True)

    print(f"\n{'='*70}", flush=True)
    print("RESULTADO FINAL", flush=True)
    for bid, ok in resultados.items():
        status = "OK" if ok else "ERRO"
        print(f"  Parte {bid:02d} — {PARTE_TITULOS[bid]:35s} [{status}]", flush=True)

    sucessos = sum(1 for ok in resultados.values() if ok)
    print(f"\n{sucessos}/5 partes renderizadas com sucesso.", flush=True)
    print(f"Output: {OUT}", flush=True)


if __name__ == "__main__":
    main()
