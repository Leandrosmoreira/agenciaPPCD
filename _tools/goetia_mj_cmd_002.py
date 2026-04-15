#!/usr/bin/env python3
"""
GOETIA — Gera prompts_imagens_mj.txt
Formato: comandos /imagine prontos para Midjourney v7.
Canal: Sinais do Fim | Video: video-002-marca-da-besta
"""

import os
import paramiko
from datetime import datetime

# ─── Caminhos ────────────────────────────────────────────────────────────────
LOCAL_DIR  = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\5-prompts"
TXT_IN     = os.path.join(LOCAL_DIR, "prompts_imagens.txt")
TXT_OUT    = os.path.join(LOCAL_DIR, "prompts_imagens_mj.txt")
LOG_PATH   = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log"

VPS_HOST   = "31.97.165.64"
VPS_PORT   = 22
VPS_USER   = "root"
KEY_PATH   = os.path.expanduser("~/.ssh/id_ed25519")
VPS_REMOTE = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/prompts_imagens_mj.txt"
TXT_URL    = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/prompts_imagens_mj.txt"

# Seed base para consistencia (mesmo seed = resultados reproduziveis)
SEED_BASE = 847200

# Style Reference aprovado por Snayder em 2026-04-06
SREF_URL = "https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png"
SREF_PARAM = f"--sref {SREF_URL} --sw 750"

# Negative prompt padrao Midjourney (via --no)
NEGATIVE_MJ = "text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors"

# Parametros fixos MJ v7
MJ_PARAMS_BASE = "--ar 16:9 --style raw --v 7 --q 2 --stylize 750"


# ─── Parser (robusto) ────────────────────────────────────────────────────────
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


# ─── Extrair numero Q do header ───────────────────────────────────────────────
def get_q_num(header):
    try:
        return int(header[1:3])
    except (ValueError, IndexError):
        return 0


# ─── Gerar arquivo MJ ─────────────────────────────────────────────────────────
def gerar_mj_txt():
    blocks = parse_all_blocks(TXT_IN)
    print(f"[PARSER] {len(blocks)} blocos encontrados")

    # Agrupamento por secao
    section_ranges = [
        ("INTRODUCAO - Q01 a Q04", 1, 4),
        ("ATO 1 - BASE BIBLICA - Q05 a Q12", 5, 12),
        ("ATO 2 - CONTEXTO HISTORICO - Q13 a Q18", 13, 18),
        ("ATO 3 - CBDC + CHIP - Q19 a Q26", 19, 26),
        ("ATO 4 - VIGILANCIA - Q27 a Q32", 27, 32),
        ("CONCLUSAO - Q33 a Q35", 33, 35),
    ]

    linhas = []
    linhas.append("PROMPTS MIDJOURNEY v7 — video-002-marca-da-besta")
    linhas.append("Canal: Sinais do Fim | Agencia: Abismo Criativo")
    linhas.append(f"Gerado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    linhas.append(f"Total: {len(blocks)} prompts")
    linhas.append("=" * 72)
    linhas.append("")
    linhas.append("ESTILO BASE GLOBAL (ja incluido em cada /imagine abaixo):")
    linhas.append("medieval illuminated manuscript style colorful vivid foreground,")
    linhas.append("monochrome desaturated modern background, cinematic dramatic lighting,")
    linhas.append("chiaroscuro shadows, fire glow and floating ash particles,")
    linhas.append("strong contrast vivid foreground vs black and white background,")
    linhas.append("epic surreal prophetic atmosphere, 35mm film grain, anamorphic lens flares")
    linhas.append("")
    linhas.append("PARAMETROS FIXOS: --ar 16:9 --style raw --v 7 --q 2 --stylize 750")
    linhas.append("SEED BASE: 847200 (incrementar +1 por quadro para variedade consistente)")
    linhas.append("")

    for (sec_title, q_start, q_end) in section_ranges:
        sec_blocks = [b for b in blocks if q_start <= get_q_num(b.get("header","")) <= q_end]
        if not sec_blocks:
            continue

        linhas.append("=" * 72)
        linhas.append(sec_title)
        linhas.append("=" * 72)
        linhas.append("")

        for b in sec_blocks:
            header = b.get("header", "")
            f = b.get("fields", {})
            q_num = get_q_num(header)
            seed = SEED_BASE + q_num

            subject = f.get("subject", "").strip().rstrip(".")
            setting = f.get("setting", "").strip().rstrip(".")
            prompt  = f.get("prompt", "").strip().rstrip(".")

            # Extrair so a parte descritiva do prompt (sem o "Create a cinematic surreal..." inicial)
            # O prompt ja contem a descricao completa da cena
            prompt_clean = prompt.replace(
                "Create a cinematic surreal collage image about the apocalypse. ", ""
            ).replace(
                "Create a cinematic surreal collage image about the apocalypse.", ""
            ).strip()

            # Montar o /imagine command
            mj_prompt = (
                f"{prompt_clean} "
                f"medieval illuminated manuscript style colorful vivid detailed foreground, "
                f"monochrome desaturated modern world background, cinematic dramatic lighting, "
                f"chiaroscuro deep shadows, fire glow and floating ash particles, "
                f"strong contrast vivid foreground vs black and white background, "
                f"epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares"
            )

            mj_cmd = (
                f"/imagine prompt: {mj_prompt} "
                f"{MJ_PARAMS_BASE} --chaos 20 --seed {seed} "
                f"{SREF_PARAM} "
                f"--no {NEGATIVE_MJ}"
            )

            linhas.append(f"Q{q_num:02d} -- {header[3:].strip() if header.startswith('Q') and len(header) > 3 else header}")
            linhas.append(mj_cmd)
            linhas.append("")

    conteudo = "\n".join(linhas)

    with open(TXT_OUT, "w", encoding="utf-8") as f:
        f.write(conteudo)

    print(f"[OK] MJ TXT gerado: {TXT_OUT}")
    print(f"[INFO] {len(blocks)} comandos /imagine, {len(conteudo)} caracteres")
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


# ─── Log ─────────────────────────────────────────────────────────────────────
def registrar_log(upload_ok):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    status = f"OK -> {TXT_URL}" if upload_ok else "FALHOU"
    linha = f"[{now}] GOETIA -- prompts_imagens_mj.txt (Midjourney v7 cmds) gerado, upload {status}\n"
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(linha)
    print(f"[OK] pipeline.log atualizado")


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("GOETIA -- Midjourney v7 Commands | video-002-marca-da-besta")
    print("=" * 60)

    txt_path = gerar_mj_txt()
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
