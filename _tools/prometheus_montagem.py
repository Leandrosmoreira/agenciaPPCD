#!/usr/bin/env python3
"""
PROMETHEUS — Montador Automático de Vídeo
Agência Abismo Criativo

Gera slideshow profissional com Ken Burns + transições + áudio.
Uso: python prometheus_montagem.py --canal sinais-do-fim --video video-007-falsa-paz
"""

import argparse
import glob
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# Constantes
# ─────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent
CANAIS_DIR = BASE_DIR / "canais"

KEN_BURNS_EFFECTS = ["zoom_in", "zoom_out", "pan_left", "pan_right", "pan_up", "pan_down"]
TRANSITIONS = ["crossfade", "fade_black", "dissolve"]
TRANSITION_DURATIONS = {"crossfade": 0.5, "fade_black": 0.3, "dissolve": 0.7}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg"}

# Detecção de silêncio — pausas na narração viram pontos de transição
SILENCE_THRESHOLD_DB = -35  # dB abaixo do qual é considerado silêncio
SILENCE_MIN_DURATION = 0.8  # segundos mínimos de silêncio para contar como pausa


# ─────────────────────────────────────────────
# Utilidades
# ─────────────────────────────────────────────

def log(msg: str):
    """Imprime mensagem com timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] PROMETHEUS — {msg}")


def check_ffmpeg():
    """Verifica se ffmpeg está instalado."""
    if not shutil.which("ffmpeg"):
        print("=" * 60)
        print("ERRO: ffmpeg não encontrado no PATH.")
        print()
        print("Instale ffmpeg antes de usar este script:")
        print("  Windows:  winget install ffmpeg")
        print("  macOS:    brew install ffmpeg")
        print("  Ubuntu:   sudo apt install ffmpeg")
        print("=" * 60)
        sys.exit(1)
    if not shutil.which("ffprobe"):
        print("ERRO: ffprobe não encontrado no PATH (vem junto com ffmpeg).")
        sys.exit(1)


def run_cmd(cmd: list[str], desc: str = "", check: bool = True) -> subprocess.CompletedProcess:
    """Executa comando subprocess com log."""
    if desc:
        log(desc)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"ERRO ao executar: {' '.join(cmd[:5])}...")
        print(f"stderr: {result.stderr[:500]}")
        sys.exit(1)
    return result


def get_audio_duration(filepath: str) -> float:
    """Retorna duração em segundos de um arquivo de áudio/vídeo."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(filepath)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        log(f"AVISO: não conseguiu ler duração de {filepath}")
        return 0.0
    try:
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
    except (KeyError, json.JSONDecodeError, ValueError):
        return 0.0


def detect_silences(audio_path: Path) -> list[float]:
    """
    Detecta pausas/silêncios no áudio usando ffmpeg silencedetect.
    Retorna lista de timestamps (em segundos) onde há pausas na narração.
    Esses timestamps são usados como pontos de transição entre imagens.
    """
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", f"silencedetect=noise={SILENCE_THRESHOLD_DB}dB:d={SILENCE_MIN_DURATION}",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    stderr = result.stderr

    # Extrair silence_start e silence_end do stderr do ffmpeg
    silence_starts = re.findall(r"silence_start:\s*([\d.]+)", stderr)
    silence_ends = re.findall(r"silence_end:\s*([\d.]+)", stderr)

    # Usar o ponto médio de cada silêncio como timestamp de transição
    cut_points = []
    for i in range(min(len(silence_starts), len(silence_ends))):
        start = float(silence_starts[i])
        end = float(silence_ends[i])
        midpoint = (start + end) / 2.0
        cut_points.append(midpoint)

    log(f"Silêncios detectados no áudio: {len(cut_points)} pausas")
    for j, cp in enumerate(cut_points):
        mins = int(cp // 60)
        secs = cp % 60
        log(f"  Pausa {j+1}: {mins}:{secs:05.2f}")

    return cut_points


def timestamps_to_durations(cut_points: list[float], total_duration: float, n_images: int) -> list[float]:
    """
    Converte pontos de corte (pausas) em durações por imagem.
    Se há mais imagens que pausas, distribui igualmente entre as pausas.
    Se há mais pausas que imagens, usa as N-1 pausas mais espaçadas.
    """
    if not cut_points or n_images <= 1:
        return [total_duration / max(n_images, 1)] * n_images

    # Precisamos de n_images - 1 pontos de corte
    needed = n_images - 1

    if len(cut_points) >= needed:
        # Selecionar pausas mais espaçadas (amostragem uniforme)
        indices = [int(i * len(cut_points) / needed) for i in range(needed)]
        selected = [cut_points[idx] for idx in indices]
    else:
        # Menos pausas que imagens — subdividir os segmentos maiores
        selected = list(cut_points)
        # Adicionar pontos intermediários nos segmentos mais longos
        all_boundaries = [0.0] + selected + [total_duration]
        while len(selected) < needed:
            # Encontrar o maior segmento
            segments = []
            for i in range(len(all_boundaries) - 1):
                segments.append((all_boundaries[i+1] - all_boundaries[i], i))
            segments.sort(reverse=True)
            # Dividir o maior ao meio
            biggest_dur, biggest_idx = segments[0]
            midpoint = all_boundaries[biggest_idx] + biggest_dur / 2
            all_boundaries.insert(biggest_idx + 1, midpoint)
            selected = all_boundaries[1:-1]

    # Converter pontos de corte em durações
    boundaries = [0.0] + sorted(selected) + [total_duration]
    durations = []
    for i in range(len(boundaries) - 1):
        dur = boundaries[i+1] - boundaries[i]
        durations.append(max(dur, 0.5))  # mínimo 0.5s por imagem

    # Ajustar se temos mais/menos durações que imagens
    if len(durations) > n_images:
        durations = durations[:n_images]
    while len(durations) < n_images:
        durations.append(total_duration / n_images)

    return durations


def sort_natural(paths: list[Path]) -> list[Path]:
    """Ordenação natural (Q01, Q02... ou parte1, parte2...)."""
    def extract_num(p: Path) -> int:
        nums = re.findall(r"\d+", p.stem)
        return int(nums[-1]) if nums else 0
    return sorted(paths, key=extract_num)


# ─────────────────────────────────────────────
# Parser de storyboard
# ─────────────────────────────────────────────

def parse_storyboard(storyboard_path: Path) -> dict:
    """
    Lê storyboard.md e extrai mapeamento de quadros.
    Retorna dict: {indice_quadro: {"timestamp_s": float, "ken_burns": str, "transition": str}}
    """
    if not storyboard_path.exists():
        log("Storyboard não encontrado — usando distribuição automática")
        return {}

    text = storyboard_path.read_text(encoding="utf-8")
    mapping = {}
    current_index = 0

    # Regex para capturar quadros no formato: QUADRO NN — [M:SS]
    quadro_pattern = re.compile(
        r"QUADRO\s+(\d+)\s*[—\-]+\s*\[(\d+):(\d+)\]", re.IGNORECASE
    )
    # Regex para Ken Burns na NOTA EDIÇÃO
    ken_burns_pattern = re.compile(
        r"(?:ken\s*burns|efeito|zoom|pan)[:\s]*(zoom[_ ]?in|zoom[_ ]?out|pan[_ ]?left|pan[_ ]?right|pan[_ ]?up|pan[_ ]?down)",
        re.IGNORECASE,
    )
    # Regex para transição
    transition_pattern = re.compile(
        r"TRANSI[ÇC][ÃA]O[:\s]*(fade\s*lento|corte\s*seco|dissolve|flash\s*branco|crossfade|fade\s*to\s*black)",
        re.IGNORECASE,
    )

    blocks = re.split(r"(?=QUADRO\s+\d+)", text, flags=re.IGNORECASE)

    for block in blocks:
        match_q = quadro_pattern.search(block)
        if not match_q:
            continue

        idx = int(match_q.group(1))
        minutes = int(match_q.group(2))
        seconds = int(match_q.group(3))
        timestamp_s = minutes * 60 + seconds

        # Detectar Ken Burns
        kb_match = ken_burns_pattern.search(block)
        ken_burns = None
        if kb_match:
            ken_burns = kb_match.group(1).lower().replace(" ", "_")

        # Detectar transição
        tr_match = transition_pattern.search(block)
        transition = None
        if tr_match:
            tr_raw = tr_match.group(1).lower().strip()
            if "dissolve" in tr_raw:
                transition = "dissolve"
            elif "fade" in tr_raw and "black" in tr_raw:
                transition = "fade_black"
            elif "fade" in tr_raw:
                transition = "crossfade"
            elif "crossfade" in tr_raw:
                transition = "crossfade"

        mapping[idx] = {
            "timestamp_s": timestamp_s,
            "ken_burns": ken_burns,
            "transition": transition,
        }
        current_index += 1

    log(f"Storyboard parseado: {len(mapping)} quadros encontrados")
    return mapping


# ─────────────────────────────────────────────
# Ken Burns — gerar clip individual
# ─────────────────────────────────────────────

def build_zoompan_filter(effect: str, duration_frames: int, width: int, height: int, intensity: float) -> str:
    """
    Gera filtro zoompan do ffmpeg para o efeito Ken Burns.
    intensity: 1.2 = 20% de zoom máximo.
    """
    d = duration_frames
    # Velocidade de zoom por frame
    zoom_step = (intensity - 1.0) / d

    if effect == "zoom_in":
        # Zoom de 1.0 até intensity, centralizado
        z = f"min(zoom+{zoom_step:.6f},{intensity})"
        x = f"iw/2-(iw/zoom/2)"
        y = f"ih/2-(ih/zoom/2)"

    elif effect == "zoom_out":
        # Zoom de intensity até 1.0, centralizado
        z = f"max(zoom-{zoom_step:.6f},1.0)"
        x = f"iw/2-(iw/zoom/2)"
        y = f"ih/2-(ih/zoom/2)"

    elif effect == "pan_left":
        # Zoom fixo em intensity, pan horizontal direita→esquerda
        pan_total = f"(iw-iw/zoom)"
        z = str(intensity)
        x = f"{pan_total}*(1-on/{d})"
        y = f"ih/2-(ih/zoom/2)"

    elif effect == "pan_right":
        # Zoom fixo em intensity, pan horizontal esquerda→direita
        pan_total = f"(iw-iw/zoom)"
        z = str(intensity)
        x = f"{pan_total}*(on/{d})"
        y = f"ih/2-(ih/zoom/2)"

    elif effect == "pan_up":
        # Zoom fixo em intensity, pan vertical baixo→cima
        pan_total = f"(ih-ih/zoom)"
        z = str(intensity)
        x = f"iw/2-(iw/zoom/2)"
        y = f"{pan_total}*(1-on/{d})"

    elif effect == "pan_down":
        # Zoom fixo em intensity, pan vertical cima→baixo
        pan_total = f"(ih-ih/zoom)"
        z = str(intensity)
        x = f"iw/2-(iw/zoom/2)"
        y = f"{pan_total}*(on/{d})"

    else:
        # Fallback: zoom_in
        z = f"min(zoom+{zoom_step:.6f},{intensity})"
        x = f"iw/2-(iw/zoom/2)"
        y = f"ih/2-(ih/zoom/2)"

    return f"zoompan=z='{z}':x='{x}':y='{y}':d={d}:s={width}x{height}:fps=30"


def generate_clip(
    image_path: Path,
    output_path: Path,
    duration: float,
    effect: str,
    fps: int,
    width: int,
    height: int,
    intensity: float,
):
    """Gera um clip MP4 a partir de uma imagem com efeito Ken Burns."""
    duration_frames = int(duration * fps)
    if duration_frames < 1:
        duration_frames = 1

    zoompan = build_zoompan_filter(effect, duration_frames, width, height, intensity)

    # Primeiro: escalar/pad a imagem para garantir 16:9 na resolução alvo
    # Usamos scale + pad para lidar com qualquer aspect ratio
    scale_pad = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black"
    )

    vf = f"{scale_pad},{zoompan}"

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-vf", vf,
        "-t", f"{duration:.2f}",
        "-c:v", "libx264",
        "-preset", "medium",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-an",
        str(output_path),
    ]

    run_cmd(cmd)


# ─────────────────────────────────────────────
# Concatenação com transições
# ─────────────────────────────────────────────

def concatenate_clips_with_transitions(
    clip_paths: list[Path],
    output_path: Path,
    transition_duration: float,
):
    """
    Concatena clips. Para muitos clips (>15), usa concat demuxer (rápido e estável).
    Para poucos clips (<=15), usa xfade para transições suaves.
    """
    if len(clip_paths) == 0:
        log("ERRO: nenhum clip para concatenar")
        sys.exit(1)

    if len(clip_paths) == 1:
        shutil.copy2(clip_paths[0], output_path)
        return

    n = len(clip_paths)

    # Para muitos clips, usar concat demuxer (estável, sem limite)
    concat_file = output_path.parent / "concat_list.txt"
    with open(concat_file, "w") as f:
        for cp in clip_paths:
            f.write(f"file '{cp}'\n")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264", "-preset", "medium", "-pix_fmt", "yuv420p",
        str(output_path),
    ]
    run_cmd(cmd, f"Concatenando {n} clips")
    concat_file.unlink(missing_ok=True)


# ─────────────────────────────────────────────
# Áudio — juntar partes + mixar trilha
# ─────────────────────────────────────────────

def merge_narration_parts(audio_parts: list[Path], output_path: Path):
    """Junta partes de narração em sequência."""
    if len(audio_parts) == 0:
        return None

    if len(audio_parts) == 1:
        shutil.copy2(audio_parts[0], output_path)
        return output_path

    # Criar arquivo de concat
    concat_file = output_path.parent / "audio_concat.txt"
    with open(concat_file, "w") as f:
        for ap in audio_parts:
            f.write(f"file '{ap}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:a", "aac", "-b:a", "192k",
        str(output_path),
    ]
    run_cmd(cmd, f"Juntando {len(audio_parts)} partes de narração")
    concat_file.unlink(missing_ok=True)
    return output_path


def mix_audio_with_music(
    narration_path: Path,
    music_path: Path | None,
    output_path: Path,
    music_volume: float,
    total_duration: float,
):
    """Mixa narração com trilha instrumental (volume reduzido, fade in/out)."""
    if music_path is None or not music_path.exists():
        # Sem trilha — copiar narração direta
        if narration_path and narration_path.exists():
            shutil.copy2(narration_path, output_path)
        return output_path

    if narration_path is None or not narration_path.exists():
        # Sem narração — usar só a trilha
        shutil.copy2(music_path, output_path)
        return output_path

    # Fade in 2s, fade out 3s na trilha
    fade_in = 2.0
    fade_out = 3.0
    fade_out_start = max(0, total_duration - fade_out)

    # Filter: ajustar volume da trilha + fade in/out, depois mixar
    filter_complex = (
        f"[1:a]volume={music_volume:.2f},"
        f"afade=t=in:st=0:d={fade_in:.1f},"
        f"afade=t=out:st={fade_out_start:.1f}:d={fade_out:.1f}[music];"
        f"[0:a][music]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(narration_path),
        "-i", str(music_path),
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{total_duration:.2f}",
        str(output_path),
    ]
    run_cmd(cmd, "Mixando narração + trilha instrumental")
    return output_path


# ─────────────────────────────────────────────
# Combinar vídeo + áudio final
# ─────────────────────────────────────────────

def combine_video_audio(video_path: Path, audio_path: Path | None, output_path: Path):
    """Combina stream de vídeo com áudio final."""
    if audio_path is None or not audio_path.exists():
        # Sem áudio — copiar vídeo mudo
        shutil.copy2(video_path, output_path)
        log("Exportado como slideshow mudo (sem áudio disponível)")
        return

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_path),
    ]
    run_cmd(cmd, "Combinando vídeo + áudio final")


# ─────────────────────────────────────────────
# Pipeline principal
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="PROMETHEUS — Montador Automático de Vídeo (Abismo Criativo)"
    )
    parser.add_argument("--canal", required=True, help="Slug do canal (ex: sinais-do-fim)")
    parser.add_argument("--video", required=True, help="Slug do vídeo (ex: video-007-falsa-paz)")
    parser.add_argument("--fps", type=int, default=30, help="Frames por segundo (default: 30)")
    parser.add_argument(
        "--resolution", default="1920x1080",
        help="Resolução do vídeo (default: 1920x1080)",
    )
    parser.add_argument(
        "--transition-duration", type=float, default=0.5,
        help="Duração padrão das transições em segundos (default: 0.5)",
    )
    parser.add_argument(
        "--ken-burns-intensity", type=float, default=1.2,
        help="Intensidade do Ken Burns — 1.2 = 20%% zoom (default: 1.2)",
    )
    parser.add_argument(
        "--music-volume", type=float, default=0.15,
        help="Volume da trilha em relação à narração — 0.15 = 15%% (default: 0.15)",
    )
    parser.add_argument(
        "--output", default=None,
        help="Caminho de saída (default: 7-edicao/video_montagem.mp4)",
    )
    parser.add_argument(
        "--sync-pauses", action="store_true", default=True,
        help="Sincronizar transições com pausas na narração (default: ativado)",
    )
    parser.add_argument(
        "--no-sync-pauses", action="store_true", default=False,
        help="Desativar sincronização com pausas — distribuição uniforme",
    )

    args = parser.parse_args()

    # ── Validações ──────────────────────────
    check_ffmpeg()

    width, height = map(int, args.resolution.split("x"))

    video_dir = CANAIS_DIR / args.canal / "videos" / args.video
    if not video_dir.exists():
        print(f"ERRO: diretório do vídeo não encontrado: {video_dir}")
        sys.exit(1)

    images_dir = video_dir / "6-assets" / "imagens"
    audio_dir = video_dir / "6-assets" / "audio_suno"
    storyboard_path = video_dir / "4-storyboard" / "storyboard.md"
    output_dir = video_dir / "7-edicao"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = Path(args.output) if args.output else output_dir / "video_montagem.mp4"

    log(f"Canal: {args.canal}")
    log(f"Vídeo: {args.video}")
    log(f"Resolução: {width}x{height} @ {args.fps}fps")

    # ── 1. Detectar imagens ──────────────────
    images = []
    if images_dir.exists():
        for f in images_dir.iterdir():
            if f.suffix.lower() in IMAGE_EXTENSIONS:
                images.append(f)
    images = sort_natural(images)

    if not images:
        print(f"ERRO: nenhuma imagem encontrada em {images_dir}")
        sys.exit(1)

    log(f"Imagens encontradas: {len(images)}")

    # ── 2. Detectar áudios ───────────────────
    narration_parts = []
    music_parts = []
    music_path = None

    if audio_dir.exists():
        for f in audio_dir.iterdir():
            if f.suffix.lower() not in AUDIO_EXTENSIONS:
                continue
            name_lower = f.stem.lower()
            if "trilha" in name_lower or "music" in name_lower or "instrumental" in name_lower:
                music_parts.append(f)
            elif "parte" in name_lower or "part" in name_lower or "narracao" in name_lower:
                narration_parts.append(f)

    narration_parts = sort_natural(narration_parts)
    music_parts = sort_natural(music_parts)

    # Criar diretório temporário (usado por trilha concat e clips)
    tmp_dir = Path(tempfile.mkdtemp(prefix="prometheus_"))

    # Se múltiplas trilhas (trilha.mp3, trilha1.mp3, trilha2.mp3), concatenar
    if len(music_parts) == 1:
        music_path = music_parts[0]
    elif len(music_parts) > 1:
        log(f"Concatenando {len(music_parts)} trilhas: {[p.name for p in music_parts]}")
        music_concat = tmp_dir / "trilha_concat.m4a"
        merge_narration_parts(music_parts, music_concat)
        music_path = music_concat

    log(f"Partes de narração: {len(narration_parts)}")
    log(f"Trilha instrumental: {'sim' if music_path else 'não'} ({len(music_parts)} arquivo(s))")

    # ── 3. Calcular duração total ────────────
    total_duration = 0.0
    for np in narration_parts:
        total_duration += get_audio_duration(str(np))

    if music_path and total_duration == 0.0:
        total_duration = get_audio_duration(str(music_path))

    if total_duration == 0.0:
        # Sem áudio — 5 segundos por imagem
        total_duration = len(images) * 5.0
        log(f"Sem áudio detectado — usando {total_duration:.0f}s ({len(images)} imgs x 5s)")
    else:
        log(f"Duração total do áudio: {total_duration:.1f}s")

    # ── 4. Parse storyboard ──────────────────
    storyboard_map = parse_storyboard(storyboard_path)

    # ── 5. Detectar pausas e distribuir imagens ─
    n_images = len(images)
    use_pause_sync = args.sync_pauses and not args.no_sync_pauses

    if use_pause_sync and narration_parts:
        # Primeiro juntar narração para detectar pausas
        narration_for_detection = tmp_dir / "narration_detect.m4a"
        merge_narration_parts(narration_parts, narration_for_detection)
        pause_timestamps = detect_silences(narration_for_detection)

        if pause_timestamps:
            durations = timestamps_to_durations(pause_timestamps, total_duration, n_images)
            log(f"Usando {len(pause_timestamps)} pausas da narração como pontos de transição")
        else:
            durations = [total_duration / n_images] * n_images
            log("Nenhuma pausa detectada — distribuição uniforme")
    else:
        durations = [total_duration / n_images] * n_images
        log("Sincronização com pausas desativada — distribuição uniforme")

    image_configs = []
    for i, img in enumerate(images):
        quadro_idx = i + 1

        # Duração baseada nas pausas
        dur = durations[i] if i < len(durations) else total_duration / n_images

        # Ken Burns
        effect = None
        if quadro_idx in storyboard_map and storyboard_map[quadro_idx].get("ken_burns"):
            effect = storyboard_map[quadro_idx]["ken_burns"]
        if effect is None:
            effect = random.choice(KEN_BURNS_EFFECTS)

        image_configs.append({
            "path": img,
            "duration": dur,
            "effect": effect,
        })

    avg_dur = sum(d["duration"] for d in image_configs) / len(image_configs)
    log(f"Duração média por imagem: ~{avg_dur:.1f}s (min: {min(d['duration'] for d in image_configs):.1f}s, max: {max(d['duration'] for d in image_configs):.1f}s)")

    # ── 6. Gerar clips individuais ───────────
    clip_paths = []

    total_clips = len(image_configs)
    for i, cfg in enumerate(image_configs):
        clip_path = tmp_dir / f"clip_{i:03d}.mp4"
        pct = int((i + 1) / total_clips * 100)
        log(f"[{pct:3d}%] Clip {i+1}/{total_clips}: {cfg['path'].name} ({cfg['duration']:.1f}s, {cfg['effect']})")
        generate_clip(
            image_path=cfg["path"],
            output_path=clip_path,
            duration=cfg["duration"],
            effect=cfg["effect"],
            fps=args.fps,
            width=width,
            height=height,
            intensity=args.ken_burns_intensity,
        )
        clip_paths.append(clip_path)

    # ── 7. Concatenar com transições ─────────
    video_only_path = tmp_dir / "video_notrans.mp4"
    concatenate_clips_with_transitions(
        clip_paths=clip_paths,
        output_path=video_only_path,
        transition_duration=args.transition_duration,
    )

    # ── 8. Processar áudio ───────────────────
    audio_final_path = None

    if narration_parts:
        # Reusar narração já mergeada se foi criada para detecção de pausas
        narration_merged = tmp_dir / "narration_detect.m4a"
        if not narration_merged.exists():
            narration_merged = tmp_dir / "narration_merged.m4a"
            merge_narration_parts(narration_parts, narration_merged)

        audio_final_path = tmp_dir / "audio_final.m4a"
        mix_audio_with_music(
            narration_path=narration_merged,
            music_path=music_path,
            output_path=audio_final_path,
            music_volume=args.music_volume,
            total_duration=total_duration,
        )
    elif music_path:
        audio_final_path = music_path

    # ── 9. Combinar vídeo + áudio ────────────
    combine_video_audio(video_only_path, audio_final_path, output_path)

    # ── 10. Cleanup ──────────────────────────
    try:
        shutil.rmtree(tmp_dir)
    except Exception:
        log(f"AVISO: não foi possível limpar temporários em {tmp_dir}")

    # ── 11. Log no pipeline ──────────────────
    log_path = CANAIS_DIR / args.canal / "_config" / "pipeline.log"
    if log_path.parent.exists():
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = (
            f"[{ts}] PROMETHEUS — Montagem automática concluída → "
            f"7-edicao/video_montagem.mp4 "
            f"({len(images)} imgs, {total_duration:.0f}s, {width}x{height})\n"
        )
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    # ── Resultado ────────────────────────────
    print()
    print("=" * 60)
    print("  PROMETHEUS — Montagem concluída")
    print("=" * 60)
    print(f"  Output:     {output_path}")
    print(f"  Imagens:    {len(images)}")
    print(f"  Duração:    {total_duration:.1f}s")
    print(f"  Resolução:  {width}x{height} @ {args.fps}fps")
    print(f"  Narração:   {len(narration_parts)} partes")
    print(f"  Trilha:     {'sim' if music_path else 'não'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
