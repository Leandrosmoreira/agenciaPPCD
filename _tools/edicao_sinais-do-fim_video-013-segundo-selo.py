"""
PHANTASMA — Editor Cinematografico
Canal: Sinais do Fim
Video: video-013-segundo-selo — O CAVALO VERMELHO JA CAVALGA — 2o Selo Aberto
Gerado por: Phantasma | 2026-04-17

Arquitetura:
  - 60 quadros divididos em 5 batches de 12 quadros
  - Ken Burns (zoom_in / zoom_out / pan_left / pan_right) por quadro
  - Color grading: grade_biblical / grade_apocalypse / grade_revelation
  - Render em subprocesso isolado por batch (--only-batch N)
  - Mix ffmpeg: narração (vol 1.0) + trilha (vol 0.22 se existir)

Parte 1: Q01-Q12  | BLOCO 0 + 0.5 + 1 — Gancho + Profecia
Parte 2: Q13-Q25  | BLOCO 2 — O Versiculo e o Grego (13 quadros)
Parte 3: Q26-Q38  | BLOCO 3 — Quando a Paz Foi Tirada (13 quadros)
Parte 4: Q39-Q51  | BLOCO 4 — Gog e Magog em Tempo Real (13 quadros)
Parte 5: Q52-Q60  | BLOCO 5 — Voce Esta na Tribulacao + CTA (9 quadros)

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
VIDEO  = CANAL / "videos/video-013-segundo-selo"
ASSETS = VIDEO / "6-assets"
AUDIO  = VIDEO / "5-audio"
OUT    = VIDEO / "7-edicao"
OUT.mkdir(exist_ok=True)

W, H, FPS = 1920, 1080, 30

# ---------------------------------------------------------------------------
# PARTE_DUR — duracao em segundos por parte de audio
# Valores reais: substituir apos ter os MP3 finais.
# Parte 1: 0:00-2:30 = 150s | Parte 2: 2:30-5:00 = 150s | ...
# Parte 5: 10:00-12:00 = 120s
# ---------------------------------------------------------------------------
PARTE_DUR = {
    1: 150.0,   # 0:00–2:30
    2: 150.0,   # 2:30–5:00
    3: 150.0,   # 5:00–7:30
    4: 150.0,   # 7:30–10:00
    5: 120.0,   # 10:00–12:00
}

# ---------------------------------------------------------------------------
# AUDIO
# ---------------------------------------------------------------------------
PARTES_AUDIO = [AUDIO / f"parte{n}.mp3" for n in range(1, 6)]
TRILHA       = AUDIO / "trilha.MP3"

# ---------------------------------------------------------------------------
# WRITE OPTIONS (sem audio — ffmpeg mixa depois)
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
# BATCHES — 60 quadros em 5 grupos
# Parte 2 tem 13 quadros (Q13-Q25), partes 3 e 4 tambem 13 quadros cada
# Parte 5 tem 9 quadros (Q52-Q60)
# ---------------------------------------------------------------------------
BATCHES = [
    {"id": 1, "quadros": list(range(1,  13)), "audio_parts": [1]},   # Q01-Q12 (12)
    {"id": 2, "quadros": list(range(13, 26)), "audio_parts": [2]},   # Q13-Q25 (13)
    {"id": 3, "quadros": list(range(26, 39)), "audio_parts": [3]},   # Q26-Q38 (13)
    {"id": 4, "quadros": list(range(39, 52)), "audio_parts": [4]},   # Q39-Q51 (13)
    {"id": 5, "quadros": list(range(52, 61)), "audio_parts": [5]},   # Q52-Q60 (9)
]

# ---------------------------------------------------------------------------
# TITULOS DAS CENAS — extraidos do storyboard para text_screen de fallback
# ---------------------------------------------------------------------------
TITULOS_CENAS = {
    # Batch 1 — Gancho + Profecia Revelada + As Tres Promessas
    1:  "GANCHO — TELA PRETA",
    2:  "O ATAQUE",
    3:  "O PALACIO ATINGIDO",
    4:  "MORTE DO LIDER",
    5:  "O MUNDO ASSISTE",
    6:  "O LIVRO DE DOIS MIL ANOS",
    7:  "O CAVALO VERMELHO",
    8:  "A GRANDE ESPADA",
    9:  "PRIMEIRO SELO — DATA VERIFICAVEL",
    10: "A ESPADA TEM NOME",
    11: "VOCE VIVE A TRIBULACAO",
    12: "FICA AI",
    # Batch 2 — O Versiculo e o Grego
    13: "PERGAMINHO GREGO",
    14: "PYRROS — COR DE FOGO",
    15: "A FORJA",
    16: "CIDADE EM CHAMAS",
    17: "O CAVALO DE FOGO",
    18: "O VERBO TIRAR",
    19: "PRIMEIRO SELO — CAVALO BRANCO",
    20: "MACHAIRA MEGALE",
    21: "O ARSENAL NUCLEAR",
    22: "INVENTARIO DAS OGIVAS",
    23: "NUNCA UMA ESPADA MAIOR",
    24: "PUTIN E A DOUTRINA",
    25: "A ESPADA FOI ENTREGUE",
    # Batch 3 — Quando a Paz Foi Tirada
    26: "MAPA DO ORIENTE MEDIO",
    27: "RUSSIA INVADE UCRANIA",
    28: "QUINHENTOS MIL MORTOS",
    29: "7 DE OUTUBRO — HAMAS",
    30: "ESTADO DE GUERRA ISRAEL",
    31: "SETENTA E DUAS HORAS",
    32: "PRIMEIRO ATAQUE DIRETO IRA",
    33: "FRONTEIRA QUEBRADA",
    34: "SEGUNDA SALVA — 180 MISSEIS",
    35: "ISRAEL RESPONDE",
    36: "GUERRA DOS DOZE DIAS",
    37: "KHAMENEI MORRE",
    38: "FOI TIRADA OU NAO FOI?",
    # Batch 4 — Gog e Magog em Tempo Real
    39: "PROFETA EZEQUIEL",
    40: "EZEQUIEL 38 — GOG",
    41: "GANCHOS NOS QUEIXOS",
    42: "MESEQUE E TUBAL = RUSSIA",
    43: "PERSIA = IRA",
    44: "GOMER, PUTE, CUXE",
    45: "JOEL ROSENBERG",
    46: "BEIRA DA GUERRA DE GOG",
    47: "NAO E PASTOR EMOCIONAL",
    48: "TRATADO RUSSIA-IRA",
    49: "TURQUIA SE AFASTA DA OTAN",
    50: "A COALIZAO ESTA FORMADA",
    51: "COINCIDENCIA?",
    # Batch 5 — Voce Esta na Tribulacao + CTA
    52: "SETE SELOS — SEQUENCIA",
    53: "CAVALO BRANCO RESUMO",
    54: "CAVALO VERMELHO RESUMO",
    55: "CAVALO PRETO NO HORIZONTE",
    56: "CAVALEIRO DA FOME",
    57: "PRECO DO TRIGO +35%",
    58: "APOCALIPSE 7 — RESGATE",
    59: "O CORDEIRO ABRE OS SELOS",
    60: "TELA FINAL — ENCERRAMENTO",
}

# ---------------------------------------------------------------------------
# EFEITOS KEN BURNS por quadro — baseados no storyboard
# ---------------------------------------------------------------------------
# q: numero do quadro (1-60)
EFFECTS_MAP = {
    1:  "zoom_in",    # tela preta — abertura
    2:  "pan_left",   # rastros de missel diagonal
    3:  "zoom_in",    # palacio atingido — push-in
    4:  "zoom_in",    # morte do lider — push-in lento
    5:  "zoom_in",    # celular — zoom in
    6:  "zoom_in",    # codice — push-in
    7:  "zoom_in",    # cavalo vermelho — zoom in no olho
    8:  "zoom_out",   # espada — zoom out revelando
    9:  "zoom_in",    # pergaminho selado — zoom in
    10: "zoom_in",    # missel — push-in
    11: "zoom_out",   # vitral sete selos — zoom out
    12: "zoom_in",    # biblia e cruz — zoom in
    13: "zoom_in",    # pergaminho grego — push-in
    14: "zoom_in",    # pyrros — zoom in lento
    15: "zoom_in",    # forja — pulse no metal
    16: "pan_right",  # cidade em chamas — pan direita
    17: "zoom_in",    # cavalo de fogo — push-in
    18: "zoom_in",    # PAX rasgando — zoom in
    19: "zoom_out",   # cavalo branco — zoom out revelando
    20: "zoom_in",    # machaira megale — zoom in
    21: "zoom_out",   # cogumelo atomico — zoom out revelando escala
    22: "pan_right",  # mapa com pilhas — pan direita
    23: "zoom_in",    # espada cravada — push-in
    24: "zoom_in",    # Putin assinando — zoom in
    25: "zoom_in",    # entrega da espada — zoom in
    26: "zoom_in",    # mapa Oriente Medio — zoom in
    27: "zoom_in",    # tanque — zoom in na flor
    28: "pan_right",  # cemiterio militar — pan direita
    29: "zoom_in",    # cerca rasgada — push-in
    30: "zoom_in",    # rolo Tora — zoom in letras
    31: "zoom_out",   # regiao em chamas — zoom out
    32: "pan_left",   # rastros de missel — pan esquerda
    33: "zoom_in",    # fronteira rachada — zoom in
    34: "pan_right",  # ceu com misseis — pan direita
    35: "pan_right",  # caca F-35 — pan direita
    36: "zoom_in",    # instalacao nuclear — zoom in
    37: "zoom_in",    # pena sobre apocalipse — zoom in
    38: "zoom_in",    # cavalo vermelho disparando — push-in
    39: "zoom_in",    # Ezequiel — zoom in no rosto
    40: "zoom_in",    # GOG — zoom in
    41: "zoom_in",    # ganchos — push-in
    42: "pan_right",  # mapa russo — pan direita
    43: "zoom_in",    # imperador persa — push-in
    44: "zoom_in",    # triptico — pan circular
    45: "zoom_in",    # Joel Rosenberg — push-in
    46: "zoom_in",    # linha no deserto — zoom in
    47: "pan_right",  # placas institucionais — pan direita
    48: "zoom_in",    # apertao de maos — zoom in
    49: "pan_left",   # bandeira turca — pan esquerda
    50: "zoom_in",    # coalizao — zoom in no pergaminho
    51: "zoom_in",    # balanca — zoom in muito lento
    52: "pan_right",  # sete selos — pan direita
    53: "zoom_in",    # cavalo branco — push-in
    54: "zoom_in",    # cavalo vermelho — zoom in
    55: "zoom_out",   # cavalo preto no horizonte — zoom out
    56: "zoom_in",    # balanca desnivelada — zoom in
    57: "pan_right",  # celeiro — pan direita
    58: "zoom_in",    # Cordeiro — zoom in lento
    59: "zoom_in",    # maos do Cordeiro — zoom in
    60: "zoom_out",   # tela final — fade
}

# ---------------------------------------------------------------------------
# GRADE por quadro — baseado no tema da cena do storyboard
# ---------------------------------------------------------------------------
# biblical: julgamento, fogo, guerra, cavalos, misseis
# apocalypse: desolacao, fim do mundo, cemiterio, devastacao
# revelation: visao profetica, luz divina, anjos, profetas, Cordeiro
GRADE_MAP = {
    # Batch 1
    1:  "biblical",     # tela preta / gancho
    2:  "biblical",     # rastros de missel — fogo
    3:  "biblical",     # palacio em chamas
    4:  "revelation",   # morte do lider — peso profetico
    5:  "apocalypse",   # alienacao cotidiana
    6:  "revelation",   # codice medieval — revelacao
    7:  "biblical",     # cavalo vermelho — central
    8:  "biblical",     # espada — sagrado inevitavel
    9:  "revelation",   # selo rachado
    10: "biblical",     # missel — terror tecnologico
    11: "revelation",   # vitral sete selos
    12: "revelation",   # biblia e cruz
    # Batch 2
    13: "revelation",   # pergaminho grego — estudo reverente
    14: "biblical",     # pyrros — cor de fogo
    15: "biblical",     # forja — trabalho infernal
    16: "biblical",     # cidade em chamas — devastacao epica
    17: "biblical",     # cavalo de fogo — visao apocaliptica
    18: "biblical",     # PAX rasgado — violacao deliberada
    19: "apocalypse",   # cavalo branco — paz enganosa
    20: "biblical",     # machaira megale — terminologia
    21: "apocalypse",   # cogumelo atomico — escala aterradora
    22: "apocalypse",   # mapa ogivas — registro do fim
    23: "apocalypse",   # espada cravada — monumento de terror
    24: "apocalypse",   # Putin — autoridade fria
    25: "biblical",     # entrega da espada — transferencia sinistra
    # Batch 3
    26: "apocalypse",   # mapa Oriente Medio — analise forense
    27: "apocalypse",   # tanque — invasao historica
    28: "apocalypse",   # cemiterio — luto industrial
    29: "biblical",     # 7 outubro — violacao sagrada
    30: "revelation",   # rolo Tora — antiguidade em guerra
    31: "biblical",     # regiao em chamas — combustao
    32: "biblical",     # 300 rastros missel — fronteira cruzada
    33: "biblical",     # fronteira rachada — violacao historica
    34: "biblical",     # ceu com 180 misseis — retaliacao
    35: "apocalypse",   # caca F-35 — precedente cruzado
    36: "biblical",     # instalacao nuclear — destruicao cirurgica
    37: "revelation",   # pena sobre Apocalipse — peso profetico
    38: "biblical",     # cavalo vermelho disparando — acusacao profetica
    # Batch 4
    39: "revelation",   # Ezequiel — profeta antigo
    40: "revelation",   # GOG — profecia escrita
    41: "biblical",     # ganchos — arrasto profetico
    42: "apocalypse",   # mapa russo — geografia profetica
    43: "biblical",     # imperador persa — identidade atemporal
    44: "apocalypse",   # triptico coalizao — coalizao ancestral
    45: "revelation",   # Joel Rosenberg — credibilidade
    46: "revelation",   # limiar apocaliptico — encruzilhada
    47: "revelation",   # placas institucionais — credibilidade
    48: "biblical",     # tratado Russia-Ira — alianca selada
    49: "apocalypse",   # bandeira turca — realinhamento
    50: "revelation",   # coalizao formada — profecia cumprida
    51: "revelation",   # balanca — julgamento pessoal
    # Batch 5
    52: "revelation",   # sete selos — contabilidade apocaliptica
    53: "apocalypse",   # cavalo branco resumo — paz que foi
    54: "biblical",     # cavalo vermelho resumo — selo em execucao
    55: "apocalypse",   # cavalo preto — proxima onda
    56: "apocalypse",   # cavaleiro da fome — escassez iminente
    57: "apocalypse",   # celeiro em ruinas — economia fameliaca
    58: "revelation",   # Cordeiro — esperanca teologica
    59: "revelation",   # maos do Cordeiro — ato cosmico
    60: "apocalypse",   # tela final — encerramento
}


# ---------------------------------------------------------------------------
# COLOR GRADING
# ---------------------------------------------------------------------------

def grade_biblical(frame):
    """Quente, carmesim profundo — julgamento, fogo, guerra."""
    f = frame.astype(np.float32)
    np.multiply(f[:, :, 0], 1.15, out=f[:, :, 0])   # R +
    np.multiply(f[:, :, 1], 0.92, out=f[:, :, 1])   # G -
    np.multiply(f[:, :, 2], 0.85, out=f[:, :, 2])   # B -
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
    """Sombras profundas, realce dourado em altas luzes — visoes, profetas."""
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
    """Ken Burns + color grading aplicado frame a frame."""
    base = ken_burns(img_path, duration, effect)

    def make_frame_graded(t):
        return grade_fn(base.make_frame(t))

    clip = VideoClip(make_frame_graded, duration=duration)
    clip.fps = FPS
    return clip


# ---------------------------------------------------------------------------
# TELA DE TEXTO (PIL)
# ---------------------------------------------------------------------------

def text_screen(text, duration, bg=(0, 0, 0), color=(197, 163, 85), fontsize=72):
    """Gera tela preta com texto centralizado — usado como fallback e separador."""
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


# ---------------------------------------------------------------------------
# RENDER BATCH
# ---------------------------------------------------------------------------

def render_batch(batch):
    bid        = batch["id"]
    quadros    = batch["quadros"]
    audio_part = batch["audio_parts"][0]
    dur_total  = PARTE_DUR[audio_part]

    # Numero de quadros de imagem = total - 1 (Q01 de cada batch vira text_screen 2.5s)
    n_img_quadros = len(quadros) - 1
    dur_per_q = max(5.0, (dur_total - 2.5) / max(n_img_quadros, 1))

    print(
        f"[BATCH {bid}] {len(quadros)} quadros | {dur_total}s total | "
        f"{dur_per_q:.1f}s/quadro",
        flush=True,
    )

    clips = []

    # Tela de abertura do batch com titulo da cena real (Q01 do batch)
    q_first = quadros[0]
    titulo_abertura = TITULOS_CENAS.get(q_first, f"PARTE {bid}")
    clips.append(text_screen(titulo_abertura, 2.5))

    # Demais quadros
    for q in quadros[1:]:
        img_path = ASSETS / f"Q{q:02d}.png"
        titulo_q = TITULOS_CENAS.get(q, f"Q{q:02d}")

        if not img_path.exists():
            print(f"  [AVISO] {img_path.name} nao encontrado — usando text_screen", flush=True)
            clips.append(text_screen(titulo_q, dur_per_q))
            continue

        effect   = EFFECTS_MAP.get(q, "zoom_in")
        grade_key = GRADE_MAP.get(q, "biblical")
        grade_fn = GRADE_FNS[grade_key]

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
    print("PHANTASMA — video-013-segundo-selo", flush=True)
    print(f"Assets: {ASSETS}", flush=True)
    print(f"Output: {OUT}", flush=True)
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
