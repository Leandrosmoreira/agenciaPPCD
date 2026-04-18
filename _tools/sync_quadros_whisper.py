"""
sync_quadros_whisper.py — Alinha quadros do storyboard ao áudio real via Whisper.

Uso:
  python _tools/sync_quadros_whisper.py --canal sinais-do-fim --video video-015-economist-manipulacao --partes 1 2 --quadros-range 2-18

Saida:
  Imprime dict {quadro: duracao_segundos} pronto para colar no edicao.py
  Salva em: canais/{canal}/videos/{video}/4-storyboard/durations_sync.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def clean_text(s: str) -> str:
    s = re.sub(r"[^\wáéíóúâêôãõçÁÉÍÓÚÂÊÔÃÕÇ ]", " ", s.lower())
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_quadro_narrations(storyboard_path: Path, q_start: int, q_end: int) -> dict:
    """Extrai NARRAÇÃO de cada quadro Q{q_start} até Q{q_end}."""
    text = storyboard_path.read_text(encoding="utf-8")
    result = {}
    for q in range(q_start, q_end + 1):
        tag = f"Q{q:02d}"
        # Regex: encontra o bloco do quadro
        pattern = rf"### {tag}[^\n]*\n(.*?)(?=### Q\d+|\Z)"
        m = re.search(pattern, text, re.DOTALL)
        if not m:
            print(f"[WARN] {tag} nao encontrado no storyboard", flush=True)
            result[q] = ""
            continue
        block = m.group(1)
        # Dentro do bloco, pegar linha NARRAÇÃO
        narr_match = re.search(r"\*\*NARRAÇÃO:\*\*\s*(.+?)(?=\n- \*\*|\n\n|\Z)", block, re.DOTALL)
        if narr_match:
            result[q] = clean_text(narr_match.group(1))
        else:
            # Tenta "- **NARRAÇÃO:**"
            narr2 = re.search(r"NARRAÇÃO[:\s]*[\"']?(.+?)[\"']?\s*\n", block)
            result[q] = clean_text(narr2.group(1)) if narr2 else ""
    return result


def align_quadros_to_words(quadro_narrations: dict, words_with_ts: list) -> dict:
    """
    Estrategia proporcional: cada quadro consome N palavras da transcricao proporcional
    ao tamanho da narracao do quadro. Menos preciso mas robusto.
    Retorna {q: (start_ts, end_ts, score)}
    """
    results = {}
    total_words = len(words_with_ts)
    if total_words == 0:
        return {q: None for q in quadro_narrations}

    # Conta palavras-target totais
    sorted_qs = sorted(quadro_narrations.keys())
    word_counts = {q: len(quadro_narrations[q].split()) for q in sorted_qs}
    total_target = sum(word_counts.values())

    if total_target == 0:
        # Distribuicao uniforme
        per_q = total_words // len(sorted_qs)
        word_counts = {q: per_q for q in sorted_qs}
        total_target = per_q * len(sorted_qs)

    # Distribui palavras do whisper proporcionalmente
    cursor = 0
    for q in sorted_qs:
        if total_target == 0:
            results[q] = None
            continue
        share = word_counts[q] / total_target
        n_take = max(1, int(round(share * total_words)))
        start_idx = cursor
        end_idx = min(cursor + n_take - 1, total_words - 1)
        if start_idx >= total_words:
            results[q] = None
            continue
        start_ts = words_with_ts[start_idx]["start"]
        end_ts = words_with_ts[end_idx]["end"]
        results[q] = (start_ts, end_ts, 1.0)
        cursor = end_idx + 1

    # Se sobraram palavras, estica o ultimo quadro
    if cursor < total_words and sorted_qs:
        last_q = sorted_qs[-1]
        if results[last_q]:
            s, _, sc = results[last_q]
            results[last_q] = (s, words_with_ts[-1]["end"], sc)

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--canal", required=True)
    ap.add_argument("--video", required=True)
    ap.add_argument("--partes", nargs="+", type=int, required=True, help="Numeros das partes de audio")
    ap.add_argument("--quadros-range", required=True, help="Ex: 2-18")
    ap.add_argument("--model", default="base", help="Modelo whisper (tiny/base/small/medium)")
    args = ap.parse_args()

    video_dir = ROOT / "canais" / args.canal / "videos" / args.video
    audio_dir = video_dir / "5-audio"
    sb_path = video_dir / "4-storyboard" / "storyboard.md"

    if not sb_path.exists():
        # tentar storyboard.txt
        sb_path = video_dir / "4-storyboard" / "storyboard.txt"

    q_start, q_end = map(int, args.quadros_range.split("-"))

    # 1. Extrai narracoes
    print(f"[1/3] Extraindo narracoes Q{q_start:02d}-Q{q_end:02d} de {sb_path.name}", flush=True)
    narrations = extract_quadro_narrations(sb_path, q_start, q_end)
    for q, t in narrations.items():
        print(f"  Q{q:02d}: {t[:80]}...", flush=True)

    # 2. Whisper transcribe concatenando partes
    print(f"\n[2/3] Carregando whisper model={args.model}...", flush=True)
    import whisper
    model = whisper.load_model(args.model)

    all_words = []
    time_offset = 0.0
    for p in args.partes:
        audio_path = audio_dir / f"parte{p}.mp3"
        if not audio_path.exists():
            print(f"[ERRO] audio nao encontrado: {audio_path}", flush=True)
            sys.exit(1)
        print(f"  Transcrevendo parte{p}.mp3...", flush=True)
        # word_timestamps=True retorna segments com 'words'
        result = model.transcribe(str(audio_path), language="pt", word_timestamps=True, verbose=False)
        for seg in result.get("segments", []):
            for w in seg.get("words", []):
                all_words.append({
                    "word": w["word"].strip(),
                    "start": w["start"] + time_offset,
                    "end": w["end"] + time_offset,
                })
        # Incrementa offset com duracao real do arquivo via ffprobe
        import subprocess
        r = subprocess.run(
            ["ffprobe","-v","quiet","-show_entries","format=duration","-of","csv=p=0", str(audio_path)],
            capture_output=True, text=True
        )
        try:
            file_dur = float(r.stdout.strip())
        except Exception:
            file_dur = result["segments"][-1]["end"] if result.get("segments") else 0
        time_offset += file_dur
        print(f"    {len(result.get('segments',[]))} segments, offset agora {time_offset:.1f}s", flush=True)

    print(f"  Total words: {len(all_words)}", flush=True)

    # 3. Alinhar
    print(f"\n[3/3] Alinhando quadros a palavras...", flush=True)
    alignments = align_quadros_to_words(narrations, all_words)

    # Computa duracoes
    durations = {}
    prev_end = 0.0
    for q in sorted(alignments.keys()):
        if alignments[q] is None:
            durations[q] = 5.0  # fallback
            continue
        start_ts, end_ts, score = alignments[q]
        # duracao = do prev_end ate end_ts
        dur = max(2.0, end_ts - prev_end)
        durations[q] = round(dur, 2)
        print(f"  Q{q:02d}: start={start_ts:.2f}s end={end_ts:.2f}s dur={dur:.2f}s score={score:.2f}", flush=True)
        prev_end = end_ts

    # Salvar
    out_path = video_dir / "4-storyboard" / "durations_sync.json"
    out_path.write_text(json.dumps(durations, indent=2), encoding="utf-8")
    print(f"\n[OK] Salvo: {out_path}", flush=True)
    print(f"\nDict pronto para colar no edicao.py:")
    print("DURATIONS_OVERRIDE = {")
    for q, d in durations.items():
        print(f"    {q}: {d},")
    print("}")


if __name__ == "__main__":
    main()
