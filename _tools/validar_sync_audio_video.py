#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VALIDAR SYNC AUDIO/VIDEO (ADR-008)
===================================

Valida que cada video_parteNN.mp4 em 7-edicao/partes tem duracao >= PARTE N.mp3
em 5-audio. Garante que nenhum trecho de narracao seja cortado.

Uso:
  python _tools/validar_sync_audio_video.py --canal sinais-do-fim --video video-011-nefilim
  python _tools/validar_sync_audio_video.py --canal sinais-do-fim --video video-011-nefilim --strict

Saida:
  exit 0 = tudo OK (pode fazer upload)
  exit 1 = DESSINCRONIZADO (bloqueia upload)

Tolerancia padrao: audio pode ser ate 100ms maior que video (fade)
Modo strict: audio deve ser <= video sempre (zero tolerancia)
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOLERANCE_S = 0.1  # 100ms tolerancia padrao


def log(msg):
    print(msg, flush=True)


def get_duration(path: Path) -> float:
    """Retorna duracao em segundos via ffprobe."""
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_format", str(path)],
        capture_output=True, text=True
    )
    try:
        fmt = json.loads(r.stdout).get("format", {})
        if "duration" in fmt:
            return float(fmt["duration"])
    except Exception:
        pass
    return 0.0


def fmt_time(s: float) -> str:
    """Formata segundos como MM:SS.ms"""
    m = int(s // 60)
    sec = s - m * 60
    return f"{m:02d}:{sec:05.2f}"


def validar(canal: str, video: str, strict: bool = False) -> int:
    """Valida sincronizacao audio/video. Retorna exit code (0=ok, 1=erro)."""
    video_dir = BASE_DIR / "canais" / canal / "videos" / video
    audio_dir = video_dir / "5-audio"
    edicao_dir = video_dir / "7-edicao" / "partes"

    log("=" * 60)
    log(f"VALIDAR SYNC — {canal} / {video}")
    log(f"Modo: {'STRICT' if strict else f'tolerancia {TOLERANCE_S}s'}")
    log("=" * 60)

    if not audio_dir.exists():
        log(f"[ERRO] Pasta de audio nao existe: {audio_dir}")
        return 1
    if not edicao_dir.exists():
        log(f"[ERRO] Pasta de edicao nao existe: {edicao_dir}")
        return 1

    # Coletar audios PARTE N.mp3 (ignorar trilha/music)
    skip_keywords = ["trilha", "music", "instrumental", "bg"]
    audios = sorted([
        f for f in audio_dir.iterdir()
        if f.suffix.lower() in {".mp3", ".wav", ".m4a", ".ogg"}
        and not any(k in f.name.lower() for k in skip_keywords)
    ], key=lambda f: f.name)

    videos = sorted([
        f for f in edicao_dir.iterdir()
        if f.suffix.lower() == ".mp4"
        and "parte" in f.name.lower()
    ], key=lambda f: f.name)

    if not audios:
        log(f"[ERRO] Nenhum audio de narracao encontrado em {audio_dir}")
        return 1
    if not videos:
        log(f"[ERRO] Nenhum video de parte encontrado em {edicao_dir}")
        return 1

    if len(audios) != len(videos):
        log(f"[ERRO] Numero de audios ({len(audios)}) != numero de videos ({len(videos)})")
        log(f"       Audios: {[a.name for a in audios]}")
        log(f"       Videos: {[v.name for v in videos]}")
        return 1

    log(f"Partes encontradas: {len(audios)}")
    log("")
    log(f"{'Parte':<8} {'Audio':<22} {'Video':<22} {'Delta':<10} {'Status'}")
    log("-" * 70)

    all_ok = True
    tol = 0.0 if strict else TOLERANCE_S

    for i, (a, v) in enumerate(zip(audios, videos), 1):
        a_dur = get_duration(a)
        v_dur = get_duration(v)
        delta = v_dur - a_dur

        if delta >= -tol:
            status = "[OK]"
        else:
            status = "[FAIL]"
            all_ok = False

        log(f"{i:<8} {a.name[:20]:<22} {v.name[:20]:<22} "
            f"{delta:+.2f}s    {status}")
        log(f"         audio={fmt_time(a_dur)}     video={fmt_time(v_dur)}")

    log("-" * 70)

    if all_ok:
        log("[SUCESSO] Todas as partes estao sincronizadas")
        log("         Upload LIBERADO")
        return 0
    else:
        log("[BLOQUEADO] Uma ou mais partes estao dessincronizadas")
        log("           Upload NAO PODE PROSSEGUIR")
        log("")
        log("Para corrigir: rodar novamente o prometheus:")
        log(f"  python _tools/prometheus_partes.py --canal {canal} --video {video}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Valida sincronizacao audio/video (ADR-008)"
    )
    parser.add_argument("--canal", required=True,
                        help="Ex: sinais-do-fim")
    parser.add_argument("--video", required=True,
                        help="Ex: video-011-nefilim")
    parser.add_argument("--strict", action="store_true",
                        help="Zero tolerancia (audio <= video sempre)")
    args = parser.parse_args()

    rc = validar(args.canal, args.video, args.strict)
    sys.exit(rc)


if __name__ == "__main__":
    main()
