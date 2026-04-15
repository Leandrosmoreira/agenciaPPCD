#!/usr/bin/env python3
"""
GOETIA — Gera prompts_imagens_flat.txt
Formato: cada prompt como paragrafo unico, campos inline, sem markdown.
Canal: Sinais do Fim | Video: video-002-marca-da-besta
"""

import os
import paramiko
from datetime import datetime

# ─── Caminhos ────────────────────────────────────────────────────────────────
LOCAL_DIR  = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\5-prompts"
TXT_IN     = os.path.join(LOCAL_DIR, "prompts_imagens.txt")
TXT_OUT    = os.path.join(LOCAL_DIR, "prompts_imagens_flat.txt")
LOG_PATH   = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log"

VPS_HOST   = "31.97.165.64"
VPS_PORT   = 22
VPS_USER   = "root"
KEY_PATH   = os.path.expanduser("~/.ssh/id_ed25519")
VPS_REMOTE = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/prompts_imagens_flat.txt"
TXT_URL    = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/prompts_imagens_flat.txt"


# ─── Parser (mesmo do goetia_imagens_002.py) ─────────────────────────────────
def parse_all_blocks(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    all_blocks = []
    current_block = None

    for line in lines:
        line_stripped = line.strip()

        if line_stripped.startswith("## Q"):
            if current_block:
                all_blocks.append(current_block)
            current_block = {"header": line_stripped[3:].strip(), "fields": {}, "current_field": None}
            continue

        if current_block is None:
            continue

        if line_stripped.startswith("**SUBJECT:**"):
            current_block["current_field"] = "subject"
            current_block["fields"]["subject"] = line_stripped.replace("**SUBJECT:**", "").strip()
        elif line_stripped.startswith("**SETTING:**"):
            current_block["current_field"] = "setting"
            current_block["fields"]["setting"] = line_stripped.replace("**SETTING:**", "").strip()
        elif line_stripped.startswith("**MOOD:**"):
            current_block["current_field"] = "mood"
            current_block["fields"]["mood"] = line_stripped.replace("**MOOD:**", "").strip()
        elif line_stripped.startswith("**PROMPT:**"):
            current_block["current_field"] = "prompt"
            current_block["fields"]["prompt"] = ""
        elif line_stripped.startswith("**NEGATIVE PROMPT:**"):
            current_block["current_field"] = "negative"
            current_block["fields"]["negative"] = line_stripped.replace("**NEGATIVE PROMPT:**", "").strip()
        elif line_stripped.startswith("**ASPECT RATIO:**"):
            current_block["fields"]["ratio"] = line_stripped.replace("**ASPECT RATIO:**", "").strip()
            current_block["current_field"] = None
        elif line_stripped.startswith("**STYLE:**"):
            current_block["fields"]["style"] = line_stripped.replace("**STYLE:**", "").strip()
            current_block["current_field"] = None
        elif line_stripped == "---":
            all_blocks.append(current_block)
            current_block = None
        elif current_block.get("current_field") == "prompt" and line_stripped:
            existing = current_block["fields"].get("prompt", "")
            current_block["fields"]["prompt"] = (existing + " " + line_stripped).strip()

    if current_block:
        all_blocks.append(current_block)

    return all_blocks


# ─── Gerar TXT flat ───────────────────────────────────────────────────────────
def gerar_flat_txt():
    blocks = parse_all_blocks(TXT_IN)
    print(f"[PARSER] {len(blocks)} blocos encontrados")

    linhas = []
    for b in blocks:
        f = b.get("fields", {})
        subject  = f.get("subject", "").strip().rstrip(".")
        setting  = f.get("setting", "").strip().rstrip(".")
        mood     = f.get("mood", "").strip().rstrip(".")
        prompt   = f.get("prompt", "").strip().rstrip(".")
        ratio    = f.get("ratio", "16:9").strip()
        style    = f.get("style", "Cinematic surreal biblical collage").strip()

        # Montar paragrafo unico
        parts = []
        if subject:
            parts.append(f"SUBJECT: {subject}.")
        if setting:
            parts.append(f"SETTING: {setting}.")
        if mood:
            parts.append(f"MOOD: {mood}.")
        if prompt:
            parts.append(f"PROMPT: {prompt}.")
        parts.append(f"Aspect Ratio: {ratio} | Style: {style}")

        paragrafo = " ".join(parts)
        linhas.append(paragrafo)

    conteudo = "\n\n".join(linhas) + "\n"

    with open(TXT_OUT, "w", encoding="utf-8") as f:
        f.write(conteudo)

    print(f"[OK] TXT gerado: {TXT_OUT}")
    print(f"[INFO] {len(blocks)} prompts, {len(conteudo)} caracteres")
    return TXT_OUT


# ─── Upload VPS ───────────────────────────────────────────────────────────────
def upload_vps(txt_path):
    print(f"[...] Conectando VPS {VPS_HOST}...")
    try:
        key = paramiko.Ed25519Key.from_private_key_file(KEY_PATH)
    except Exception as e:
        print(f"[ERRO] Chave SSH: {e}")
        return False

    transport = paramiko.Transport((VPS_HOST, VPS_PORT))
    try:
        transport.connect(username=VPS_USER, pkey=key)
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


# ─── Registro log ─────────────────────────────────────────────────────────────
def registrar_log(upload_ok):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    status = f"OK -> {TXT_URL}" if upload_ok else "FALHOU (arquivo local salvo)"
    linha = f"[{now}] GOETIA — prompts_imagens_flat.txt gerado e upload {status}\n"
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(linha)
    print(f"[OK] pipeline.log atualizado")


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("GOETIA — Flat TXT | video-002-marca-da-besta")
    print("=" * 60)

    txt_path = gerar_flat_txt()
    upload_ok = upload_vps(txt_path)
    registrar_log(upload_ok)

    print("=" * 60)
    if upload_ok:
        print(f"[CONCLUIDO] Disponivel em:")
        print(f"  {TXT_URL}")
    else:
        print(f"[CONCLUIDO] Salvo localmente em:")
        print(f"  {txt_path}")
    print("=" * 60)
