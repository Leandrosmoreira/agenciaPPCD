#!/usr/bin/env python3
"""
GOETIA — Gerador de PDF + Upload VPS
Canal: Sinais do Fim
Video: video-002-marca-da-besta
Agencia: Abismo Criativo
"""

import os
import sys
import paramiko
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)

# ─── Cores da agencia ────────────────────────────────────────────────────────
PRETO       = HexColor("#0A0A0A")
VERMELHO    = HexColor("#8B0000")
DOURADO     = HexColor("#C5A355")
BRANCO_SUJO = HexColor("#E8E0D0")
CINZA_ESCURO = HexColor("#1A1A1A")

# ─── Estilos ─────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    'AgTitle',
    parent=styles['Title'],
    fontSize=22,
    textColor=VERMELHO,
    fontName='Helvetica-Bold',
    spaceAfter=6,
    alignment=1,
)
style_subtitle = ParagraphStyle(
    'AgSubtitle',
    parent=styles['Normal'],
    fontSize=11,
    textColor=DOURADO,
    fontName='Helvetica-Bold',
    spaceAfter=4,
    alignment=1,
)
style_meta = ParagraphStyle(
    'AgMeta',
    parent=styles['Normal'],
    fontSize=8,
    textColor=DOURADO,
    fontName='Helvetica',
    spaceAfter=2,
    alignment=1,
)
style_section = ParagraphStyle(
    'AgSection',
    parent=styles['Heading1'],
    fontSize=13,
    textColor=VERMELHO,
    fontName='Helvetica-Bold',
    spaceBefore=16,
    spaceAfter=6,
)
style_q_header = ParagraphStyle(
    'AgQHeader',
    parent=styles['Heading2'],
    fontSize=11,
    textColor=DOURADO,
    fontName='Helvetica-Bold',
    spaceBefore=10,
    spaceAfter=4,
)
style_label = ParagraphStyle(
    'AgLabel',
    parent=styles['Normal'],
    fontSize=8,
    textColor=DOURADO,
    fontName='Helvetica-Bold',
    spaceAfter=2,
)
style_body = ParagraphStyle(
    'AgBody',
    parent=styles['Normal'],
    fontSize=8,
    textColor=PRETO,
    fontName='Helvetica',
    leading=12,
    spaceAfter=4,
)
style_prompt = ParagraphStyle(
    'AgPrompt',
    parent=styles['Normal'],
    fontSize=8,
    textColor=CINZA_ESCURO,
    fontName='Helvetica',
    leading=12,
    spaceAfter=4,
    leftIndent=12,
    borderPad=4,
)
style_negative = ParagraphStyle(
    'AgNeg',
    parent=styles['Normal'],
    fontSize=7,
    textColor=HexColor("#555555"),
    fontName='Helvetica-Oblique',
    leading=10,
    spaceAfter=4,
    leftIndent=12,
)
style_footer = ParagraphStyle(
    'AgFooter',
    parent=styles['Normal'],
    fontSize=7,
    textColor=DOURADO,
    fontName='Helvetica',
    alignment=1,
    spaceAfter=2,
)

# ─── Caminhos ────────────────────────────────────────────────────────────────
LOCAL_DIR   = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\5-prompts"
TXT_PATH    = os.path.join(LOCAL_DIR, "prompts_imagens.txt")
PDF_PATH    = os.path.join(LOCAL_DIR, "prompts_imagens.pdf")
LOG_PATH    = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log"

VPS_HOST    = "31.97.165.64"
VPS_PORT    = 22
VPS_USER    = "root"
KEY_PATH    = os.path.expanduser("~/.ssh/id_ed25519")
VPS_REMOTE  = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/prompts_imagens.pdf"
VPS_DIR     = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts"
PDF_URL     = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/prompts_imagens.pdf"


# ─── Parse do arquivo de prompts ─────────────────────────────────────────────
def parse_prompts(txt_path):
    """Le o arquivo .txt e extrai blocos de prompts por quadro.
    Abordagem robusta: parseia todos os ## Q blocks e agrupa por faixa de numero."""
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Passo 1: extrair todos os blocos ## Q com seus campos
    all_blocks = []
    current_block = None

    for line in lines:
        line_stripped = line.strip()

        # Detecta quadro (## Q)
        if line_stripped.startswith("## Q"):
            if current_block:
                all_blocks.append(current_block)
            current_block = {"header": line_stripped[3:].strip(), "fields": {}, "current_field": None}
            continue

        # Pula linhas fora de um bloco Q
        if current_block is None:
            continue

        # Detecta campos do bloco
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

    # Flush ultimo bloco
    if current_block:
        all_blocks.append(current_block)

    # Passo 2: agrupar blocos em secoes por faixa de numero Q
    section_ranges = [
        ("INTRODUCAO — Q01 a Q04", 1, 4),
        ("ATO 1 — BASE BIBLICA — Q05 a Q12", 5, 12),
        ("ATO 2 — CONTEXTO HISTORICO — Q13 a Q18", 13, 18),
        ("ATO 3 — CBDC + CHIP — Q19 a Q26", 19, 26),
        ("ATO 4 — VIGILANCIA — Q27 a Q32", 27, 32),
        ("CONCLUSAO — Q33 a Q35", 33, 35),
    ]

    sections = []
    for title, q_start, q_end in section_ranges:
        sec_blocks = []
        for b in all_blocks:
            header = b.get("header", "")
            # Extrair numero do Q (ex: "Q08 — Titulo" -> 8)
            try:
                q_num = int(header[1:3])
                if q_start <= q_num <= q_end:
                    sec_blocks.append(b)
            except (ValueError, IndexError):
                pass
        if sec_blocks:
            sections.append({"title": title, "blocks": sec_blocks})

    print(f"[PARSER] {len(all_blocks)} blocos parseados, {len(sections)} secoes")
    return sections


# ─── Geracao do PDF ───────────────────────────────────────────────────────────
def gerar_pdf():
    os.makedirs(LOCAL_DIR, exist_ok=True)

    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title="Prompts de Imagem — video-002-marca-da-besta",
        author="Goetia | Abismo Criativo",
    )

    story = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Capa ──
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("ABISMO CRIATIVO", style_title))
    story.append(Paragraph("Sinais do Fim — Passagens do Apocalipse", style_subtitle))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=VERMELHO, spaceAfter=6))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("PROMPTS DE IMAGEM — BANANA 2.0", style_title))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("video-002-marca-da-besta", style_subtitle))
    story.append(Paragraph(
        '"A Marca da Besta Já Está Sendo Implementada — Apocalipse 13"',
        style_subtitle
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"Agente: Goetia  |  Data: {now}  |  Total: 35 prompts", style_meta))
    story.append(HRFlowable(width="100%", thickness=1, color=DOURADO, spaceAfter=6))
    story.append(Spacer(1, 0.5*cm))

    # ── Estilo Base Global ──
    story.append(Paragraph("ESTILO BASE GLOBAL", style_section))
    story.append(Paragraph(
        "Inclua em todos os prompts:",
        style_label
    ))
    estilo_base = (
        "Create a cinematic surreal collage image about the apocalypse. "
        "Use a medieval biblical illustration style for the main subject in full color "
        "and high detail in the foreground. In the background, show a modern world in "
        "black and white or desaturated tones. Add fire, smoke, and dramatic clouds. "
        "Use strong contrast between the colorful subject and the monochrome background. "
        "Lighting: cinematic, dramatic, high contrast, glowing highlights. "
        "Feel: epic, emotional, slightly surreal, like a prophecy happening in the modern world."
    )
    story.append(Paragraph(estilo_base, style_prompt))
    story.append(HRFlowable(width="100%", thickness=0.5, color=DOURADO, spaceAfter=4))

    # ── Carregar e parsear prompts ──
    sections = parse_prompts(TXT_PATH)

    section_names = {
        "INTRODUCAO": "INTRODUÇÃO — Q01 a Q04",
        "ATO 1": "ATO 1 — BASE BÍBLICA — Q05 a Q12",
        "ATO 2": "ATO 2 — CONTEXTO HISTÓRICO — Q13 a Q18",
        "ATO 3": "ATO 3 — CBDC + CHIP — Q19 a Q26",
        "ATO 4": "ATO 4 — VIGILÂNCIA — Q27 a Q32",
        "CONCLUSAO": "CONCLUSÃO — Q33 a Q35",
    }

    for sec in sections:
        title = sec.get("title", "")
        blocks = sec.get("blocks", [])

        # Filtrar secoes que contem quadros Q
        valid_blocks = [b for b in blocks if b.get("header")]
        if not valid_blocks:
            continue

        story.append(PageBreak())
        story.append(Paragraph(title, style_section))
        story.append(HRFlowable(width="100%", thickness=1, color=VERMELHO, spaceAfter=6))

        for block in valid_blocks:
            header = block.get("header", "")
            fields = block.get("fields", {})

            story.append(Paragraph(f"## {header}", style_q_header))

            if fields.get("subject"):
                story.append(Paragraph("SUBJECT:", style_label))
                story.append(Paragraph(fields["subject"], style_body))

            if fields.get("setting"):
                story.append(Paragraph("SETTING:", style_label))
                story.append(Paragraph(fields["setting"], style_body))

            if fields.get("mood"):
                story.append(Paragraph("MOOD:", style_label))
                story.append(Paragraph(fields["mood"], style_body))

            if fields.get("prompt"):
                story.append(Paragraph("PROMPT:", style_label))
                story.append(Paragraph(fields["prompt"], style_prompt))

            if fields.get("negative"):
                story.append(Paragraph("NEGATIVE PROMPT:", style_label))
                story.append(Paragraph(fields["negative"], style_negative))

            ratio_style = fields.get("ratio", "16:9")
            style_val = fields.get("style", "Cinematic surreal biblical collage")
            story.append(Paragraph(
                f"Aspect Ratio: {ratio_style}  |  Style: {style_val}",
                style_meta
            ))
            story.append(HRFlowable(width="100%", thickness=0.3, color=CINZA_ESCURO, spaceAfter=4))

    # ── Rodape ──
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=DOURADO, spaceAfter=6))
    story.append(Paragraph(
        f"GOETIA | ABISMO CRIATIVO | {now}",
        style_footer
    ))
    story.append(Paragraph(
        "Canal: Sinais do Fim | video-002-marca-da-besta | 35 prompts para Banana 2.0",
        style_footer
    ))

    doc.build(story)
    print(f"[OK] PDF gerado: {PDF_PATH}")
    return PDF_PATH


# ─── Upload VPS ───────────────────────────────────────────────────────────────
def upload_vps(pdf_path):
    print(f"[...] Conectando VPS {VPS_HOST}...")
    try:
        key = paramiko.Ed25519Key.from_private_key_file(KEY_PATH)
    except Exception as e:
        print(f"[ERRO] Nao foi possivel carregar a chave SSH: {e}")
        return False

    transport = paramiko.Transport((VPS_HOST, VPS_PORT))
    try:
        transport.connect(username=VPS_USER, pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Garantir que o diretorio remoto existe
        dirs_to_create = [
            "/opt/agencia",
            "/opt/agencia/canais",
            "/opt/agencia/canais/sinais-do-fim",
            "/opt/agencia/canais/sinais-do-fim/videos",
            "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta",
            "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts",
        ]
        for d in dirs_to_create:
            try:
                sftp.mkdir(d)
            except Exception:
                pass  # Diretorio ja existe

        print(f"[...] Enviando PDF para VPS...")
        sftp.put(pdf_path, VPS_REMOTE)
        sftp.close()
        transport.close()
        print(f"[OK] Upload concluido!")
        print(f"[URL] {PDF_URL}")
        return True
    except Exception as e:
        print(f"[ERRO] Falha no upload: {e}")
        transport.close()
        return False


# ─── Registro no pipeline.log ─────────────────────────────────────────────────
def registrar_log(upload_ok):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    status_upload = f"→ {PDF_URL}" if upload_ok else "→ ERRO NO UPLOAD (arquivo local salvo)"

    linhas = [
        f"\n[{now}] GOETIA — 35 prompts de imagem gerados → 5-prompts/prompts_imagens.txt",
        f"[{now}] GOETIA — PDF gerado → 5-prompts/prompts_imagens.pdf",
        f"[{now}] GOETIA — Upload VPS {'OK' if upload_ok else 'FALHOU'} {status_upload}",
        f"[{now}] CHECKPOINT — Aguardando aprovacao dos prompts de imagem por Snayder",
    ]

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha + "\n")

    print(f"[OK] pipeline.log atualizado")


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("GOETIA — Prompts de Imagem | video-002-marca-da-besta")
    print("=" * 60)

    # 1. Gerar PDF
    pdf_path = gerar_pdf()

    # 2. Upload VPS
    upload_ok = upload_vps(pdf_path)

    # 3. Registrar log
    registrar_log(upload_ok)

    print("=" * 60)
    if upload_ok:
        print(f"[CONCLUIDO] PDF disponivel em:")
        print(f"  {PDF_URL}")
    else:
        print(f"[CONCLUIDO] PDF salvo localmente em:")
        print(f"  {pdf_path}")
        print("  (Upload para VPS falhou — execute novamente quando a VPS estiver acessivel)")
    print("=" * 60)
