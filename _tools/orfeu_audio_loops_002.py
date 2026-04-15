#!/usr/bin/env python3
"""
ORFEU — Trilha Instrumental + Loops de Atmosfera
Canal: Sinais do Fim | Video: video-002-marca-da-besta
"""

import os
import paramiko
from datetime import datetime

LOCAL_DIR = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\5-prompts"
TXT_OUT = os.path.join(LOCAL_DIR, "suno_audio_completo.txt")
LOG_PATH = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log"
VPS_REMOTE = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/suno_audio_completo.txt"
TXT_URL = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/suno_audio_completo.txt"

SEP = "=" * 80

def gerar_txt():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    linhas = [
        SEP,
        "SUNO AUDIO COMPLETO -- video-002-marca-da-besta",
        "Agente: Orfeu | Abismo Criativo | Sinais do Fim",
        f"Gerado: {now}",
        SEP,
        "",
        SEP,
        "PARTE 1 -- TRILHA INSTRUMENTAL",
        "Suno > Create > Custom mode (NAO usar aba Sounds)",
        SEP,
        "",
        "INSTRUCOES:",
        "- Suno > Create > Custom mode",
        "- Preencher os campos abaixo",
        "- Gerar 2 versoes e escolher a melhor",
        "- No CapCut: volume 10-15%, loopado por todo o video",
        "",
        "STYLE OF MUSIC:",
        "dark ambient cinematic, deep orchestral drones, low cello sustained notes, ancient strings, distant haunting choir pads, ominous reverb, slow tempo 60 BPM, prophetic biblical atmosphere, no percussion, no beats, cinematic tension, documentary score, instrumental only",
        "",
        "TITLE:",
        "Sinais do Fim -- Trilha Fundo",
        "",
        "LYRICS (copiar exatamente):",
        "[Instrumental]",
        "[No vocals]",
        "[No lyrics]",
        "[Dark ambient orchestral]",
        "[Deep drone sustained]",
        "[Low cello]",
        "[Ancient choir distant]",
        "[Prophetic atmosphere]",
        "[Slow build]",
        "[Cinematic tension]",
        "",
        SEP,
        "PARTE 2 -- LOOPS DE ATMOSFERA",
        "Suno > Sounds > Type: LOOP (nao One-Shot)",
        SEP,
        "",
        "INSTRUCOES:",
        "- Suno > Sounds > Type: LOOP",
        "- Colar cada prompt no campo 'Describe the sound you want'",
        "- Gerar 2 variacoes de cada e escolher a melhor",
        "- BPM: Auto | Key: Any",
        "",
        "-" * 80,
        "LOOP 1 -- DRONE BASE",
        "Usar: Video inteiro como camada base | Volume CapCut: 8%",
        "-" * 80,
        "dark ambient drone loop, deep ominous low frequency hum, sub-bass rumble, prophetic tension atmosphere, no melody, no rhythm, pure sustained drone, apocalyptic dread, 60 seconds seamless loop",
        "",
        "-" * 80,
        "LOOP 2 -- CATEDRAL",
        "Usar: Cenas biblicas medievais Q01-Q12 | Volume CapCut: 12%",
        "-" * 80,
        "ancient stone cathedral reverb ambience loop, distant echoing silence, faint stone drip, cold air resonance, gothic atmosphere, sacred and ominous, no music, pure environmental sound, seamless loop",
        "",
        "-" * 80,
        "LOOP 3 -- TEMPESTADE",
        "Usar: Cenas de besta e apocalipse | Volume CapCut: 15%",
        "-" * 80,
        "distant thunder rumble loop, deep low rolling thunder, wind howling through ruins, storm approaching ambience, no rain yet, ominous weather tension, prophetic storm atmosphere, seamless loop",
        "",
        "-" * 80,
        "LOOP 4 -- FOGO",
        "Usar: Cenas de julgamento e fogo | Volume CapCut: 12%",
        "-" * 80,
        "fire crackling ambience loop, embers and ash soundscape, burning wood distant, warm crackling texture, apocalyptic fire atmosphere, no wind, steady burn, seamless loop",
        "",
        "-" * 80,
        "LOOP 5 -- DIGITAL",
        "Usar: Cenas CBDC, chip, vigilancia Q19-Q32 | Volume CapCut: 10%",
        "-" * 80,
        "digital tension ambience loop, low electronic hum, server room distant buzz, surveillance atmosphere, cold mechanical drone, dystopian technology soundscape, seamless loop",
        "",
        SEP,
        "GUIA DE USO NO CAPCUT",
        SEP,
        "",
        "TRILHAS DE AUDIO (ordem de cima para baixo):",
        "  TRILHA 1: Narracao Suno (partes 1-9) -- volume 100%",
        "  TRILHA 2: Trilha Instrumental -- volume 10-15%, loop todo o video",
        "  TRILHA 3: Loop atmosfera por secao (conforme tabela abaixo)",
        "",
        "MAPA DE LOOPS POR SECAO:",
        "  [00:00 - 02:00]  Loop 2 (Catedral)    -- Introducao + base biblica",
        "  [02:00 - 04:00]  Loop 3 (Tempestade)  -- Besta + contexto historico",
        "  [04:00 - 08:00]  Loop 5 (Digital)     -- CBDC + chip + vigilancia",
        "  [08:00 - 11:00]  Loop 3 (Tempestade)  -- Exclusao + controle global",
        "  [11:00 - 13:30]  Loop 4 (Fogo)        -- Conclusao + julgamento + CTA",
        "  Loop 1 (Drone)   camada base em TODO o video no volume 8%",
        "",
        SEP,
        "ORFEU | ABISMO CRIATIVO | video-002-marca-da-besta",
        SEP,
    ]

    conteudo = "\n".join(linhas)
    with open(TXT_OUT, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"[OK] Arquivo gerado: {TXT_OUT}")
    return TXT_OUT


def upload_vps(txt_path):
    print(f"[...] Conectando VPS...")
    try:
        key = paramiko.Ed25519Key.from_private_key_file(os.path.expanduser("~/.ssh/id_ed25519"))
    except Exception as e:
        print(f"[ERRO] Chave SSH: {e}")
        return False
    transport = paramiko.Transport(("31.97.165.64", 22))
    try:
        transport.connect(username="root", pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(txt_path, VPS_REMOTE)
        sftp.close()
        transport.close()
        print(f"[OK] Upload concluido!")
        print(f"[URL] {TXT_URL}")
        return True
    except Exception as e:
        print(f"[ERRO] Upload: {e}")
        transport.close()
        return False


def registrar_log(upload_ok):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    status = f"OK -> {TXT_URL}" if upload_ok else "FALHOU"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{now}] ORFEU -- suno_audio_completo.txt gerado (1 trilha + 5 loops), upload {status}\n")
    print("[OK] pipeline.log atualizado")


if __name__ == "__main__":
    print("=" * 60)
    print("ORFEU -- Trilha + Loops | video-002-marca-da-besta")
    print("=" * 60)
    txt_path = gerar_txt()
    upload_ok = upload_vps(txt_path)
    registrar_log(upload_ok)
    print("=" * 60)
    if upload_ok:
        print(f"[CONCLUIDO] {TXT_URL}")
    else:
        print(f"[CONCLUIDO] Salvo localmente: {txt_path}")
    print("=" * 60)
