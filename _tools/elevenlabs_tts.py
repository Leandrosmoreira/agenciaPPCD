#!/usr/bin/env python3
"""
ELEVENLABS TTS — Gerador de narracao automatizado
Abismo Criativo | Agente: Orfeu (modo ElevenLabs)

Converte parteN.txt (prompts de narracao) em MP3 via ElevenLabs API.
Limpa tags Suno automaticamente. Salva em 5-audio/PARTEN.mp3.

Uso:
  python elevenlabs_tts.py --canal rewound-america --video video-001-why-i-started
  python elevenlabs_tts.py --canal rewound-america --video video-001-why-i-started --dry-run
  python elevenlabs_tts.py --canal rewound-america --video video-001-why-i-started --parte 1

Requer:
  ELEVENLABS_API_KEY no .env
  ELEVENLABS_VOICE_ID_REWOUND ou ELEVENLABS_VOICE_ID_SINAIS no .env
"""

import argparse
import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERRO: 'requests' nao instalado. Rode: pip install requests")
    sys.exit(1)

# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CANAIS_DIR = BASE_DIR / "canais"

API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# Defaults (podem ser overridden por estilo_canal.md)
DEFAULT_MODEL = "eleven_multilingual_v2"
DEFAULT_STABILITY = 0.65
DEFAULT_SIMILARITY = 0.85
DEFAULT_STYLE = 0.3

# Tags Suno a remover
SUNO_TAG_PATTERNS = [
    r"\[Voice:.*?\]",
    r"\[Background:.*?\]",
    r"\[Style:.*?\]",
    r"\[trilha.*?\]",
    r"\[voz.*?\]",
]

# Tags de pausa — converter para marcador
PAUSE_PATTERN = r"\[pausa\s+([\d.]+)s?\]"


# ============================================================
# FUNCOES
# ============================================================

def load_env():
    """Carrega variaveis do .env se existir."""
    env_path = BASE_DIR / "_agency" / ".env"
    if not env_path.exists():
        env_path = BASE_DIR / "_agency" / ".env.template"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    key = key.strip()
                    val = val.strip()
                    if val and key not in os.environ:
                        os.environ[key] = val


def get_api_key():
    return os.environ.get("ELEVENLABS_API_KEY", "")


def get_voice_id(canal_slug: str):
    """Retorna voice_id baseado no canal."""
    slug_upper = canal_slug.replace("-", "_").upper()
    # Tenta ELEVENLABS_VOICE_ID_{CANAL} primeiro
    key = f"ELEVENLABS_VOICE_ID_{slug_upper}"
    vid = os.environ.get(key, "")
    if vid:
        return vid
    # Fallback para nomes comuns
    for suffix in ["REWOUND", "SINAIS"]:
        if suffix.lower() in canal_slug.lower():
            vid = os.environ.get(f"ELEVENLABS_VOICE_ID_{suffix}", "")
            if vid:
                return vid
    return ""


def clean_text(raw: str) -> str:
    """Remove tags Suno e limpa texto para TTS puro."""
    text = raw

    # Remover tags Suno
    for pattern in SUNO_TAG_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)

    # Converter pausas para quebras de linha (ElevenLabs respeita pontuacao)
    def pause_to_break(match):
        seconds = float(match.group(1))
        if seconds >= 3:
            return "\n\n...\n\n"
        elif seconds >= 1.5:
            return "\n\n"
        else:
            return "\n"

    text = re.sub(PAUSE_PATTERN, pause_to_break, text, flags=re.IGNORECASE)

    # Remover qualquer tag restante [...]
    text = re.sub(r"\[.*?\]", "", text)

    # Limpar espacos e linhas vazias excessivas
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    text = text.strip()

    return text


def find_parte_files(prompts_dir: Path) -> list:
    """Encontra arquivos parteN.txt ordenados."""
    patterns = [
        "parte*.txt",
        "*-parte*.txt",
        "video-*-parte*.txt",
    ]
    files = set()
    for pat in patterns:
        files.update(prompts_dir.glob(pat))

    # Ordenar por numero da parte
    def parte_num(f):
        match = re.search(r"parte(\d+)", f.name, re.IGNORECASE)
        return int(match.group(1)) if match else 999

    return sorted(files, key=parte_num)


def generate_tts(text: str, voice_id: str, api_key: str,
                 model: str = DEFAULT_MODEL,
                 stability: float = DEFAULT_STABILITY,
                 similarity: float = DEFAULT_SIMILARITY,
                 style: float = DEFAULT_STYLE) -> bytes:
    """Chama ElevenLabs API e retorna bytes do MP3."""
    url = f"{API_URL}/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": style,
            "use_speaker_boost": True,
        },
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=120)

    if resp.status_code == 200:
        return resp.content
    else:
        error_msg = resp.text[:300]
        raise RuntimeError(
            f"ElevenLabs API error {resp.status_code}: {error_msg}"
        )


def log(msg: str, pipeline_log: Path = None):
    """Print + registrar em pipeline.log."""
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    print(msg)
    if pipeline_log:
        with open(pipeline_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] ORFEU-TTS — {msg}\n")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="ElevenLabs TTS — Abismo Criativo")
    parser.add_argument("--canal", required=True, help="Slug do canal (ex: rewound-america)")
    parser.add_argument("--video", required=True, help="Slug do video (ex: video-001-why-i-started)")
    parser.add_argument("--dry-run", action="store_true", help="Mostra o que faria sem chamar API")
    parser.add_argument("--parte", type=int, help="Gerar apenas uma parte especifica")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model ID do ElevenLabs")
    parser.add_argument("--stability", type=float, default=DEFAULT_STABILITY)
    parser.add_argument("--similarity", type=float, default=DEFAULT_SIMILARITY)
    parser.add_argument("--style", type=float, default=DEFAULT_STYLE)
    args = parser.parse_args()

    load_env()

    # Paths
    canal_dir = CANAIS_DIR / args.canal
    video_dir = canal_dir / "videos" / args.video
    prompts_dir = video_dir / "5-prompts"
    audio_dir = video_dir / "5-audio"
    pipeline_log = canal_dir / "_config" / "pipeline.log"

    # Validar
    if not canal_dir.exists():
        print(f"ERRO: Canal '{args.canal}' nao encontrado em {CANAIS_DIR}")
        sys.exit(1)
    if not video_dir.exists():
        print(f"ERRO: Video '{args.video}' nao encontrado em {canal_dir / 'videos'}")
        sys.exit(1)
    if not prompts_dir.exists():
        print(f"ERRO: Pasta 5-prompts/ nao encontrada em {video_dir}")
        sys.exit(1)

    # API Key + Voice ID
    api_key = get_api_key()
    voice_id = get_voice_id(args.canal)

    if not args.dry_run:
        if not api_key:
            print("ERRO: ELEVENLABS_API_KEY nao configurado no .env")
            sys.exit(1)
        if not voice_id:
            print(f"ERRO: Voice ID nao configurado para canal '{args.canal}'")
            print(f"  Configure ELEVENLABS_VOICE_ID_{args.canal.replace('-','_').upper()} no .env")
            sys.exit(1)

    # Encontrar arquivos
    parte_files = find_parte_files(prompts_dir)
    if not parte_files:
        print(f"ERRO: Nenhum arquivo parteN.txt encontrado em {prompts_dir}")
        sys.exit(1)

    # Filtrar parte especifica
    if args.parte:
        parte_files = [f for f in parte_files
                       if re.search(rf"parte{args.parte}\b", f.name, re.IGNORECASE)]
        if not parte_files:
            print(f"ERRO: parte{args.parte} nao encontrada")
            sys.exit(1)

    audio_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f"ELEVENLABS TTS — {args.canal} / {args.video}")
    print(f"Partes: {len(parte_files)}")
    print(f"Dry-run: {'SIM' if args.dry_run else 'NAO'}")
    print(f"Voice ID: {voice_id or '(nao configurado)'}")
    print(f"Model: {args.model}")
    print("=" * 60)

    total_chars = 0
    generated = 0

    for i, parte_file in enumerate(parte_files, 1):
        # Extrair numero da parte
        match = re.search(r"parte(\d+)", parte_file.name, re.IGNORECASE)
        parte_num = int(match.group(1)) if match else i

        # Ler e limpar
        raw = parte_file.read_text(encoding="utf-8")
        clean = clean_text(raw)
        char_count = len(clean)
        total_chars += char_count

        output_path = audio_dir / f"PARTE{parte_num}.mp3"

        print(f"\n--- Parte {parte_num} ---")
        print(f"  Input: {parte_file.name} ({len(raw)} chars raw)")
        print(f"  Clean: {char_count} chars para TTS")
        print(f"  Output: {output_path.name}")

        if args.dry_run:
            print(f"  [DRY-RUN] Texto limpo (primeiros 200 chars):")
            print(f"  {clean[:200]}...")
            continue

        # Chamar API
        print(f"  Gerando audio via ElevenLabs...")
        try:
            audio_bytes = generate_tts(
                text=clean,
                voice_id=voice_id,
                api_key=api_key,
                model=args.model,
                stability=args.stability,
                similarity=args.similarity,
                style=args.style,
            )
            output_path.write_bytes(audio_bytes)
            size_kb = len(audio_bytes) / 1024
            print(f"  OK -> {output_path.name} ({size_kb:.0f} KB)")
            log(f"PARTE{parte_num}.mp3 gerado ({char_count} chars, {size_kb:.0f} KB)", pipeline_log)
            generated += 1
        except RuntimeError as e:
            print(f"  ERRO: {e}")
            log(f"ERRO parte {parte_num}: {e}", pipeline_log)

        # Rate limit (ElevenLabs Starter = ~3 req/s)
        if i < len(parte_files):
            time.sleep(1)

    print(f"\n{'=' * 60}")
    print(f"RESUMO:")
    print(f"  Total chars enviados: {total_chars:,}")
    print(f"  Partes geradas: {generated}/{len(parte_files)}")
    if not args.dry_run and generated > 0:
        print(f"  Arquivos em: {audio_dir}")
        log(f"TTS completo: {generated} partes, {total_chars:,} chars", pipeline_log)
    print("=" * 60)


if __name__ == "__main__":
    main()
