"""
NYX — Gerador de PDF + Upload VPS
video-002-marca-da-besta | storyboard
Abismo Criativo | Agente: Nyx
"""

import os
import datetime

try:
    import paramiko
except ImportError:
    paramiko = None

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
    from reportlab.lib import colors
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False

# ── Cores da agência ──────────────────────────────────────────────────────────
PRETO   = HexColor("#0A0A0A") if REPORTLAB_OK else None
VERMELHO = HexColor("#8B0000") if REPORTLAB_OK else None
DOURADO  = HexColor("#C5A355") if REPORTLAB_OK else None
CINZA    = HexColor("#666666") if REPORTLAB_OK else None
BRANCO   = HexColor("#FFFFFF") if REPORTLAB_OK else None
CINZA_CLARO = HexColor("#CCCCCC") if REPORTLAB_OK else None

# ── Caminhos ──────────────────────────────────────────────────────────────────
LOCAL_DIR  = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\4-storyboard"
TXT_PATH   = os.path.join(LOCAL_DIR, "storyboard.txt")
PDF_PATH   = os.path.join(LOCAL_DIR, "storyboard.pdf")
LOG_PATH   = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log"

VPS_HOST   = "31.97.165.64"
VPS_PORT   = 22
VPS_USER   = "root"
KEY_PATH   = os.path.expanduser("~/.ssh/id_ed25519")
VPS_REMOTE = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/4-storyboard/storyboard.pdf"
URL_FINAL  = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/4-storyboard/storyboard.pdf"


def ts():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M]")


def log(msg):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{ts()} {msg}\n")
    print(f"{ts()} {msg}")


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title_ag", parent=base["Title"],
            fontSize=20, textColor=VERMELHO,
            fontName="Helvetica-Bold", spaceAfter=4, leading=24
        ),
        "subtitle": ParagraphStyle(
            "Sub_ag", parent=base["Normal"],
            fontSize=11, textColor=DOURADO,
            fontName="Helvetica-Bold", spaceAfter=10
        ),
        "meta": ParagraphStyle(
            "Meta_ag", parent=base["Normal"],
            fontSize=9, textColor=CINZA,
            fontName="Helvetica", spaceAfter=6
        ),
        "ato": ParagraphStyle(
            "Ato_ag", parent=base["Heading1"],
            fontSize=14, textColor=VERMELHO,
            fontName="Helvetica-Bold", spaceBefore=18, spaceAfter=8,
            borderPad=4
        ),
        "quadro_header": ParagraphStyle(
            "QH_ag", parent=base["Heading2"],
            fontSize=12, textColor=DOURADO,
            fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4
        ),
        "campo_label": ParagraphStyle(
            "CL_ag", parent=base["Normal"],
            fontSize=9, textColor=DOURADO,
            fontName="Helvetica-Bold", spaceAfter=1
        ),
        "campo_valor": ParagraphStyle(
            "CV_ag", parent=base["Normal"],
            fontSize=9, textColor=BRANCO,
            fontName="Helvetica", spaceAfter=4, leading=13
        ),
        "resumo_h": ParagraphStyle(
            "RH_ag", parent=base["Heading1"],
            fontSize=13, textColor=VERMELHO,
            fontName="Helvetica-Bold", spaceBefore=16, spaceAfter=8
        ),
        "resumo_item": ParagraphStyle(
            "RI_ag", parent=base["Normal"],
            fontSize=10, textColor=BRANCO,
            fontName="Helvetica", spaceAfter=4, leading=14
        ),
    }


def safe(text):
    """Escapa caracteres especiais para ReportLab."""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))


def parse_storyboard(txt_path):
    """
    Lê o storyboard.txt e retorna lista de seções e quadros estruturados.
    """
    with open(txt_path, encoding="utf-8") as f:
        lines = f.readlines()

    sections = []  # [{"type": "ato"|"quadro"|"resumo", "content": ...}]
    current_quadro = None
    current_ato = None
    resumo_lines = []
    in_resumo = False

    for line in lines:
        line_s = line.rstrip()

        # Detectar início do resumo
        if "RESUMO DO STORYBOARD" in line_s:
            if current_quadro:
                sections.append({"type": "quadro", "data": current_quadro})
                current_quadro = None
            in_resumo = True
            resumo_lines = [line_s]
            continue

        if in_resumo:
            resumo_lines.append(line_s)
            continue

        # Detectar linhas de separação de ato (=====)
        if line_s.startswith("=====") and len(line_s) > 10:
            continue

        # Detectar linha de ato (ATO N, INTRODUÇÃO, CONCLUSÃO, ENCERRAMENTO)
        if any(marker in line_s for marker in ["ATO 1", "ATO 2", "ATO 3", "ATO 4",
                                                "INTRODUÇÃO —", "CONCLUSÃO —",
                                                "ENCERRAMENTO —"]):
            if current_quadro:
                sections.append({"type": "quadro", "data": current_quadro})
                current_quadro = None
            sections.append({"type": "ato", "text": line_s.strip("# ").strip()})
            continue

        # Detectar início de quadro
        if line_s.startswith("QUADRO "):
            if current_quadro:
                sections.append({"type": "quadro", "data": current_quadro})
            current_quadro = {
                "header": line_s,
                "TIPO": "",
                "DURAÇÃO": "",
                "TIMESTAMP": "",
                "DESCRIÇÃO VISUAL": "",
                "NARRAÇÃO": "",
                "EMOÇÃO": "",
                "TRANSIÇÃO": ""
            }
            continue

        # Preencher campos do quadro atual
        if current_quadro is not None:
            for campo in ["TIPO:", "DURAÇÃO:", "TIMESTAMP:",
                          "DESCRIÇÃO VISUAL:", "NARRAÇÃO:", "EMOÇÃO:", "TRANSIÇÃO:"]:
                if line_s.startswith(campo):
                    key = campo.rstrip(":")
                    current_quadro[key] = line_s[len(campo):].strip()
                    break

    # Fechar último quadro
    if current_quadro:
        sections.append({"type": "quadro", "data": current_quadro})

    # Adicionar resumo
    if resumo_lines:
        sections.append({"type": "resumo", "lines": resumo_lines})

    return sections


def render_quadro_table(quadro_data, styles, story):
    """Renderiza um quadro como tabela estilizada."""
    # Cabeçalho do quadro
    story.append(Paragraph(safe(quadro_data["header"]), styles["quadro_header"]))

    # Badge de tipo (IMAGE ou VIDEO)
    tipo = quadro_data.get("TIPO", "")
    cor_tipo = VERMELHO if tipo == "VIDEO" else DOURADO
    tipo_style = ParagraphStyle(
        "TipoBadge", fontSize=8, textColor=cor_tipo,
        fontName="Helvetica-Bold", spaceAfter=6
    )
    meta_line = (
        f"[{tipo}]  "
        f"Duração: {quadro_data.get('DURAÇÃO', '')}  |  "
        f"Timestamp: {quadro_data.get('TIMESTAMP', '')}"
    )
    story.append(Paragraph(safe(meta_line), tipo_style))

    # Campos visuais, narração, emoção, transição em tabela 2 colunas
    campos = [
        ("DESCRIÇÃO VISUAL", quadro_data.get("DESCRIÇÃO VISUAL", "")),
        ("NARRAÇÃO", quadro_data.get("NARRAÇÃO", "")),
        ("EMOÇÃO", quadro_data.get("EMOÇÃO", "")),
        ("TRANSIÇÃO", quadro_data.get("TRANSIÇÃO", "")),
    ]

    table_data = []
    for label, valor in campos:
        if valor:
            label_p = Paragraph(safe(label), styles["campo_label"])
            valor_p = Paragraph(safe(valor), styles["campo_valor"])
            table_data.append([label_p, valor_p])

    if table_data:
        col_widths = [3.5 * cm, 13.5 * cm]
        t = Table(table_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (0, -1), HexColor("#1A0000")),
            ("BACKGROUND",    (1, 0), (1, -1), HexColor("#0F0F0F")),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 6),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
            ("LINEABOVE",     (0, 0), (-1, 0), 0.5, VERMELHO),
            ("LINEBELOW",     (0, -1), (-1, -1), 0.3, CINZA),
        ]))
        story.append(t)

    story.append(Spacer(1, 4))


def gerar_pdf():
    if not REPORTLAB_OK:
        print("ERRO: ReportLab não instalado. Execute: pip install reportlab")
        return False

    os.makedirs(LOCAL_DIR, exist_ok=True)

    styles = build_styles()

    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2.2 * cm,
        rightMargin=2.2 * cm,
    )

    story = []

    # ── Capa / Cabeçalho ──────────────────────────────────────────────────────
    story.append(Paragraph("ABISMO CRIATIVO — SINAIS DO FIM", styles["title"]))
    story.append(Paragraph(
        "Nyx — Storyboard Frame a Frame | video-002-marca-da-besta",
        styles["subtitle"]
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=VERMELHO, spaceAfter=4))
    story.append(Paragraph(
        "Título: A Marca da Besta Já Está Sendo Implementada — Apocalipse 13",
        styles["meta"]
    ))
    story.append(Paragraph(
        "Canal: Sinais do Fim — Passagens do Apocalipse  |  Duração: 15:30 min  |  "
        "Total: 93 quadros (56 IMAGE + 37 VIDEO)  |  Data: 2026-04-06",
        styles["meta"]
    ))
    story.append(HRFlowable(width="100%", thickness=0.5, color=CINZA, spaceAfter=12))

    # ── Parse e renderização ──────────────────────────────────────────────────
    sections = parse_storyboard(TXT_PATH)

    for sec in sections:
        if sec["type"] == "ato":
            story.append(Spacer(1, 8))
            story.append(HRFlowable(width="100%", thickness=1, color=VERMELHO, spaceAfter=4))
            story.append(Paragraph(safe(sec["text"]), styles["ato"]))
            story.append(HRFlowable(width="100%", thickness=0.3, color=CINZA, spaceAfter=8))

        elif sec["type"] == "quadro":
            render_quadro_table(sec["data"], styles, story)

        elif sec["type"] == "resumo":
            story.append(Spacer(1, 12))
            story.append(HRFlowable(width="100%", thickness=1.5, color=VERMELHO, spaceAfter=8))
            story.append(Paragraph("RESUMO DO STORYBOARD", styles["resumo_h"]))
            for rline in sec["lines"]:
                rline = rline.strip()
                if not rline or rline.startswith("===") or "RESUMO DO STORYBOARD" in rline:
                    if not rline:
                        story.append(Spacer(1, 4))
                    continue
                story.append(Paragraph(safe(rline), styles["resumo_item"]))

    # ── Rodapé de fechamento ──────────────────────────────────────────────────
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1, color=DOURADO, spaceAfter=6))
    story.append(Paragraph(
        "NYX — Abismo Criativo | Canal: Sinais do Fim | video-002-marca-da-besta",
        styles["meta"]
    ))
    story.append(Paragraph(
        f"Gerado em: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles["meta"]
    ))

    doc.build(story)
    print(f"PDF gerado: {PDF_PATH}")
    return True


def upload_vps():
    if paramiko is None:
        print("ERRO: paramiko não instalado. Execute: pip install paramiko")
        return False

    try:
        key = paramiko.Ed25519Key.from_private_key_file(KEY_PATH)
    except Exception as e:
        print(f"ERRO ao carregar chave SSH: {e}")
        return False

    try:
        t = paramiko.Transport((VPS_HOST, VPS_PORT))
        t.connect(username=VPS_USER, pkey=key)
        sftp = paramiko.SFTPClient.from_transport(t)

        # Garantir que o diretório remoto existe
        remote_dir = os.path.dirname(VPS_REMOTE)
        dirs = remote_dir.split("/")
        path_acum = ""
        for d in dirs:
            if not d:
                continue
            path_acum += "/" + d
            try:
                sftp.mkdir(path_acum)
            except Exception:
                pass  # diretório já existe

        sftp.put(PDF_PATH, VPS_REMOTE)
        sftp.close()
        t.close()
        print(f"Upload OK: {URL_FINAL}")
        return True

    except Exception as e:
        print(f"ERRO no upload: {e}")
        return False


def registrar_log(quadros_total, image_count, video_count, upload_ok):
    status_upload = "OK" if upload_ok else "FALHOU (verificar VPS)"
    log(
        f"NYX — Storyboard concluído ({quadros_total} quadros, "
        f"{image_count} IMAGE, {video_count} VIDEO) → storyboard.pdf {status_upload}"
    )
    log(f"LINK — {URL_FINAL}")


if __name__ == "__main__":
    print("=" * 60)
    print("NYX — Gerador de Storyboard PDF | video-002-marca-da-besta")
    print("=" * 60)

    # 1. Gerar PDF
    print("\n[1/3] Gerando PDF...")
    pdf_ok = gerar_pdf()

    if not pdf_ok:
        print("ABORTADO: falha na geração do PDF.")
        exit(1)

    # 2. Upload VPS
    print("\n[2/3] Fazendo upload para VPS...")
    upload_ok = upload_vps()

    # 3. Registrar no log
    print("\n[3/3] Registrando no pipeline.log...")
    registrar_log(
        quadros_total=93,
        image_count=56,
        video_count=37,
        upload_ok=upload_ok
    )

    print("\n" + "=" * 60)
    print("NYX — CONCLUÍDO")
    print(f"PDF local : {PDF_PATH}")
    print(f"URL VPS   : {URL_FINAL}")
    print("=" * 60)
