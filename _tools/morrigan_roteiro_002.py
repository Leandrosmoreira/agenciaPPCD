#!/usr/bin/env python3
"""
Morrigan — Roteiro video-002-marca-da-besta
Gera PDF com visual da agência e faz upload para VPS via SFTP.
"""
import os
import datetime
import paramiko
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

# Cores da agência
PRETO   = HexColor("#0A0A0A")
VERMELHO = HexColor("#8B0000")
DOURADO  = HexColor("#C5A355")
CINZA    = HexColor("#666666")
BRANCO   = HexColor("#E8E0D0")

styles = getSampleStyleSheet()

style_agency = ParagraphStyle(
    'Agency',
    parent=styles['Normal'],
    fontSize=9,
    textColor=CINZA,
    fontName='Helvetica',
    spaceAfter=2,
)
style_title = ParagraphStyle(
    'T',
    parent=styles['Title'],
    fontSize=20,
    textColor=VERMELHO,
    fontName='Helvetica-Bold',
    spaceAfter=4,
    leading=24,
)
style_subtitle = ParagraphStyle(
    'S',
    parent=styles['Normal'],
    fontSize=11,
    textColor=DOURADO,
    fontName='Helvetica-Bold',
    spaceAfter=4,
)
style_meta = ParagraphStyle(
    'M',
    parent=styles['Normal'],
    fontSize=9,
    textColor=CINZA,
    fontName='Helvetica',
    spaceAfter=10,
)
style_h1 = ParagraphStyle(
    'H1',
    parent=styles['Heading1'],
    fontSize=15,
    textColor=VERMELHO,
    fontName='Helvetica-Bold',
    spaceBefore=18,
    spaceAfter=8,
    leading=18,
)
style_h2 = ParagraphStyle(
    'H2',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=DOURADO,
    fontName='Helvetica-Bold',
    spaceBefore=12,
    spaceAfter=6,
    leading=15,
)
style_h3 = ParagraphStyle(
    'H3',
    parent=styles['Heading3'],
    fontSize=10,
    textColor=DOURADO,
    fontName='Helvetica-BoldOblique',
    spaceBefore=8,
    spaceAfter=4,
    leading=13,
)
style_body = ParagraphStyle(
    'B',
    parent=styles['Normal'],
    fontSize=9,
    textColor=PRETO,
    leading=13,
    spaceAfter=4,
)
style_viral = ParagraphStyle(
    'V',
    parent=styles['Normal'],
    fontSize=9,
    textColor=VERMELHO,
    fontName='Helvetica-Bold',
    leading=13,
    spaceAfter=4,
    leftIndent=12,
    borderPad=4,
)
style_visual = ParagraphStyle(
    'Vis',
    parent=styles['Normal'],
    fontSize=8,
    textColor=CINZA,
    fontName='Helvetica-Oblique',
    leading=11,
    spaceAfter=4,
    leftIndent=12,
)
style_separator = ParagraphStyle(
    'Sep',
    parent=styles['Normal'],
    fontSize=8,
    textColor=CINZA,
    fontName='Helvetica',
    spaceAfter=2,
    spaceBefore=2,
)

LOCAL_DIR  = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\3-roteiro"
TXT_PATH   = os.path.join(LOCAL_DIR, "roteiro.txt")
PDF_PATH   = os.path.join(LOCAL_DIR, "roteiro.pdf")
LOG_PATH   = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log"

VPS_HOST   = "31.97.165.64"
VPS_PORT   = 22
VPS_USER   = "root"
KEY_PATH   = os.path.expanduser("~/.ssh/id_ed25519")
VPS_REMOTE = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/3-roteiro/roteiro.pdf"
HTTP_URL   = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/3-roteiro/roteiro.pdf"


def sanitize(text):
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;'))


def build_story(content):
    story = []

    # Cabeçalho
    story.append(Paragraph("ABISMO CRIATIVO", style_agency))
    story.append(Paragraph("A Marca da Besta Já Está Sendo Implementada — Apocalipse 13", style_title))
    story.append(Paragraph("Morrigan — Criadora de Roteiro  |  video-002-marca-da-besta", style_subtitle))
    story.append(Paragraph("Canal: Sinais do Fim — Passagens do Apocalipse  |  Data: 2026-04-06", style_meta))
    story.append(HRFlowable(width="100%", thickness=2, color=VERMELHO, spaceAfter=14))

    lines = content.split('\n')
    i = 0
    skip_header = True  # pular bloco de cabeçalho do .txt (já reproduzido acima)
    header_end = 0

    # Detectar fim do cabeçalho (linha de ===)
    for idx, line in enumerate(lines):
        if line.startswith('====') and idx > 2:
            header_end = idx + 1
            break

    for idx in range(header_end, len(lines)):
        line = lines[idx]
        stripped = line.strip()

        if not stripped:
            story.append(Spacer(1, 4))
            continue

        if stripped.startswith('===='):
            story.append(HRFlowable(width="100%", thickness=0.5, color=CINZA, spaceAfter=6, spaceBefore=6))
            continue

        if stripped.startswith('## '):
            story.append(Paragraph(sanitize(stripped[3:]), style_h1))
            continue

        if stripped.startswith('### '):
            story.append(Paragraph(sanitize(stripped[4:]), style_h2))
            continue

        if stripped.startswith('[VIRAL]'):
            text = stripped[7:].strip()
            story.append(Paragraph(sanitize(text), style_viral))
            continue

        if stripped.startswith('[VISUAL:'):
            text = stripped  # mantém o marcador
            story.append(Paragraph(sanitize(text), style_visual))
            continue

        if stripped.startswith('[PAUSA'):
            story.append(Paragraph(sanitize(stripped), style_visual))
            continue

        if stripped.startswith('ROTEIRO —') or stripped.startswith('Canal:') or stripped.startswith('Agência:') or stripped.startswith('Vídeo:') or stripped.startswith('Duração') or stripped.startswith('Data:'):
            continue  # já no cabeçalho

        # corpo normal
        story.append(Paragraph(sanitize(stripped), style_body))

    # Rodapé
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=VERMELHO, spaceAfter=8))
    story.append(Paragraph(
        f"Gerado em: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}  |  "
        f"Agência Abismo Criativo  |  Morrigan  |  {HTTP_URL}",
        style_agency
    ))

    return story


def gerar_pdf():
    os.makedirs(LOCAL_DIR, exist_ok=True)
    with open(TXT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
    )
    story = build_story(content)
    doc.build(story)
    size_kb = os.path.getsize(PDF_PATH) // 1024
    print(f"[OK] PDF gerado: {PDF_PATH} ({size_kb} KB)")
    return size_kb


def upload_vps():
    print(f"[INFO] Conectando a {VPS_HOST}...")
    try:
        key = paramiko.Ed25519Key.from_private_key_file(KEY_PATH)
    except Exception as e:
        print(f"[ERRO] Chave SSH nao encontrada: {e}")
        return False

    try:
        transport = paramiko.Transport((VPS_HOST, VPS_PORT))
        transport.connect(username=VPS_USER, pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Garantir que o diretório remoto existe
        remote_dir = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/3-roteiro"
        dirs_to_create = []
        path = remote_dir
        while path not in ('/', ''):
            dirs_to_create.insert(0, path)
            path = path.rsplit('/', 1)[0]

        for d in dirs_to_create:
            try:
                sftp.mkdir(d)
            except Exception:
                pass  # já existe

        sftp.put(PDF_PATH, VPS_REMOTE)
        sftp.close()
        transport.close()
        print(f"[OK] Upload concluido: {HTTP_URL}")
        return True
    except Exception as e:
        print(f"[ERRO] Upload falhou: {e}")
        return False


def registrar_log(size_kb, upload_ok):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    chars = os.path.getsize(TXT_PATH)
    status_upload = "enviado para VPS" if upload_ok else "ERRO no upload — arquivo local disponivel"

    entry = (
        f"\n[{now}] MORRIGAN — Roteiro concluido "
        f"(15:30 min est., {chars} chars, {size_kb} KB PDF) "
        f"→ roteiro.pdf {status_upload}\n"
        f"[{now}] LINK — {HTTP_URL}\n"
        f"[{now}] CHECKPOINT — Aguardando aprovacao do roteiro por Snayder\n"
    )

    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(entry)
        print(f"[OK] Log registrado: {LOG_PATH}")
    except Exception as e:
        print(f"[AVISO] Nao foi possivel escrever no log: {e}")


if __name__ == '__main__':
    print("=" * 60)
    print("MORRIGAN — Roteiro video-002-marca-da-besta")
    print("=" * 60)
    size_kb = gerar_pdf()
    upload_ok = upload_vps()
    registrar_log(size_kb, upload_ok)
    print("=" * 60)
    print(f"ROTEIRO CONCLUIDO")
    print(f"Local : {PDF_PATH}")
    print(f"VPS   : {HTTP_URL}")
    print("=" * 60)
