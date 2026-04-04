#!/usr/bin/env python3
"""Gerador de PDFs para Abismo Criativo - Estilo visual da agencia."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable
)
from reportlab.lib.enums import TA_CENTER

# Cores Abismo Criativo
PRETO = HexColor("#0A0A0A")
VERMELHO = HexColor("#8B0000")
DOURADO = HexColor("#C5A355")
BRANCO_SUJO = HexColor("#E8E0D0")
CINZA = HexColor("#666666")

styles = getSampleStyleSheet()

style_title = ParagraphStyle('AbismoTitle', parent=styles['Title'],
    fontSize=22, textColor=VERMELHO, spaceAfter=6, fontName='Helvetica-Bold')
style_subtitle = ParagraphStyle('AbismoSubtitle', parent=styles['Normal'],
    fontSize=12, textColor=DOURADO, spaceAfter=12, fontName='Helvetica-Bold')
style_h1 = ParagraphStyle('AbismoH1', parent=styles['Heading1'],
    fontSize=16, textColor=VERMELHO, spaceBefore=16, spaceAfter=8, fontName='Helvetica-Bold')
style_h2 = ParagraphStyle('AbismoH2', parent=styles['Heading2'],
    fontSize=13, textColor=DOURADO, spaceBefore=12, spaceAfter=6, fontName='Helvetica-Bold')
style_body = ParagraphStyle('AbismoBody', parent=styles['Normal'],
    fontSize=10, textColor=PRETO, spaceAfter=6, leading=14, fontName='Helvetica')
style_quote = ParagraphStyle('AbismoQuote', parent=styles['Normal'],
    fontSize=10, textColor=CINZA, spaceAfter=6, leading=14, fontName='Helvetica-Oblique',
    leftIndent=20, rightIndent=20)
style_footer = ParagraphStyle('AbismoFooter', parent=styles['Normal'],
    fontSize=8, textColor=CINZA, alignment=TA_CENTER)

def make_hr():
    return HRFlowable(width="100%", thickness=1, color=VERMELHO, spaceAfter=12, spaceBefore=12)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_DIR = os.path.join(BASE, "canais", "sinais-do-fim", "videos", "video-001-armagedom")


def gerar_pesquisa_pdf():
    path = os.path.join(VIDEO_DIR, "1-pesquisa", "pesquisa.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4,
        topMargin=2*cm, bottomMargin=2*cm, leftMargin=2.5*cm, rightMargin=2.5*cm)
    story = []

    story.append(Paragraph("PESQUISA ARGOS", style_title))
    story.append(Paragraph("Sinais do Fim - Video-001-Armagedom", style_subtitle))
    story.append(Paragraph("Data: 2026-04-04 | Pesquisador: Argos | Status: APROVADO", style_body))
    story.append(make_hr())

    story.append(Paragraph("TOPICO SELECIONADO", style_h1))
    story.append(Paragraph("Sinais de Guerra no Oriente Medio e Profecia de Armagedom", style_h2))
    story.append(Paragraph("Viral Score: 87.3/100 (Altissimo engajamento)", style_body))
    story.append(make_hr())

    story.append(Paragraph("JUSTIFICATIVA", style_h1))
    for j in [
        "Trending Global - Conflito Israel-Gaza em alta em YouTube, X e News",
        "Conexao Profetica Clara - Apocalipse 16:16, Zacarias 14, Mateus 24:6-7",
        "Publico Evangelico Engajado - Tema evergreen com pico em momentos de conflito",
        "Verificabilidade - Eventos reais + interpretacao profetica"
    ]:
        story.append(Paragraph("* " + j, style_body))
    story.append(make_hr())

    story.append(Paragraph("FONTES DE PESQUISA", style_h1))
    fontes = [
        ("YouTube (Peso: 3.0x)", "Busca por Armagedom subiu 45%. Videos sobre Oriente Medio x Profecia tem 200k+ views."),
        ("Google Trends (Peso: 2.5x)", "Termos: profecia Armagedom, terceira guerra mundial profecia. Pico recente."),
        ("X/Twitter (Peso: 2.0x)", "22 mil mencoes. Hashtags: #Armagedom #SinaisDosTempos"),
        ("Reddit (Peso: 1.8x)", "r/Escatologia: 15+ posts por dia. Engajamento: 3-5k upvotes."),
        ("News (Peso: 1.5x)", "G1, UOL, Folha: cobertura diaria. Conexao profetica em blogs evangelicos."),
        ("TikTok (Peso: 1.4x)", "#Armagedom: 5M+ views. Crescimento exponencial.")
    ]
    for titulo, desc in fontes:
        story.append(Paragraph(titulo, style_h2))
        story.append(Paragraph(desc, style_body))
    story.append(make_hr())

    story.append(Paragraph("TOP 10 TOPICOS VIRAIS", style_h1))
    topicos = [
        ["#", "Topico", "Score"],
        ["1", "Sinais de Guerra - Profecia de Armagedom", "87.3"],
        ["2", "Eclipse Solar - Sinal do Apocalipse?", "84.5"],
        ["3", "IA - O Sinal da Besta Moderna", "83.2"],
        ["4", "Terceiro Templo - Profecia Cumprida", "81.6"],
        ["5", "Grande Reset - Agenda 2030", "79.8"],
        ["6", "Lua de Sangue - Fenomenos Astronomicos", "78.4"],
        ["7", "CBDC - Fim do Dinheiro Fisico", "75.2"],
        ["8", "Falso Messias - Anticristo na Politica", "72.9"],
        ["9", "Perseguicao Crista Global", "71.3"],
        ["10", "Nephilim Modernos", "68.7"],
    ]
    t = Table(topicos, colWidths=[30, 330, 50])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), VERMELHO),
        ('TEXTCOLOR', (0, 0), (-1, 0), BRANCO_SUJO),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, CINZA),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#FFFFFF"), HexColor("#F5F0E8")]),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
    ]))
    story.append(t)
    story.append(make_hr())
    story.append(Paragraph("Assinado: Argos, Pesquisador de Nicho | Abismo Criativo", style_footer))
    doc.build(story)
    print(f"[OK] {path}")


def gerar_titulos_pdf():
    path = os.path.join(VIDEO_DIR, "2-titulos", "titulos_seo.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4,
        topMargin=2*cm, bottomMargin=2*cm, leftMargin=2.5*cm, rightMargin=2.5*cm)
    story = []

    story.append(Paragraph("TITULOS SEO - HERMES", style_title))
    story.append(Paragraph("Sinais do Fim - Video-001-Armagedom", style_subtitle))
    story.append(Paragraph("Data: 2026-04-04 | Analista: Hermes | Status: TITULO #1 APROVADO", style_body))
    story.append(make_hr())

    story.append(Paragraph("KEYWORDS PRIMARIAS", style_h1))
    kw = [
        ["Keyword", "Buscas/mes", "Tendencia"],
        ["Armagedom", "28k", "Crescente"],
        ["Profecia Armagedom", "12k", "Crescente"],
        ["Terceira Guerra Mundial", "18k", "Estavel"],
        ["Sinais do Apocalipse", "22k", "Crescente"],
        ["Oriente Medio profecia", "8k", "Crescente"],
    ]
    t = Table(kw, colWidths=[180, 100, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), VERMELHO),
        ('TEXTCOLOR', (0, 0), (-1, 0), BRANCO_SUJO),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, CINZA),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#FFFFFF"), HexColor("#F5F0E8")]),
    ]))
    story.append(t)
    story.append(make_hr())

    story.append(Paragraph("5 TITULOS RANKEADOS POR CTR", style_h1))
    titulos = [
        ("#1 - CTR: 7.2% [APROVADO]", "Armagedom: O Fim Comecou? Profecia Biblica Cumprida", "55 chars | Pergunta provocadora + validacao profetica"),
        ("#2 - CTR: 6.8%", "Sinais de Armagedom - Guerra e Profecia", "57 chars | Atualidade + conexao profetica"),
        ("#3 - CTR: 6.4%", "Profecia Armagedom: O Que a Biblia Prediz", "50 chars | Educacional + autoridade biblica"),
        ("#4 - CTR: 6.1%", "Guerra no Oriente Medio: Sinais do Apocalipse?", "52 chars | Noticia atual + interpretacao"),
        ("#5 - CTR: 5.9%", "Armagedom Esta Acontecendo Agora? Analise Profetica", "53 chars | Investigacao + credibilidade"),
    ]
    for rank, titulo, desc in titulos:
        story.append(Paragraph(rank, style_h2))
        story.append(Paragraph(titulo, style_quote))
        story.append(Paragraph(desc, style_body))

    story.append(make_hr())
    story.append(Paragraph("TAGS YOUTUBE", style_h1))
    story.append(Paragraph("Armagedom, Profecia Biblica, Sinais do Apocalipse, Terceira Guerra Mundial, Escatologia, Fim dos Tempos, Guerra Oriente Medio, Profecia Cumprida, Sinais dos Tempos, Livro do Apocalipse, Zacarias 14, Mateus 24", style_body))
    story.append(make_hr())
    story.append(Paragraph("Assinado: Hermes, Analista SEO | Abismo Criativo", style_footer))
    doc.build(story)
    print(f"[OK] {path}")


def gerar_roteiro_pdf():
    path = os.path.join(VIDEO_DIR, "3-roteiro", "roteiro.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4,
        topMargin=2*cm, bottomMargin=2*cm, leftMargin=2.5*cm, rightMargin=2.5*cm)
    story = []

    story.append(Paragraph("ROTEIRO COMPLETO", style_title))
    story.append(Paragraph("Sinais do Fim - Video-001-Armagedom", style_subtitle))
    story.append(Paragraph("Data: 2026-04-04 | Roteirista: Morrigan | Duracao: 12 min | 9.847 chars | Evergreen", style_body))
    story.append(make_hr())

    roteiro_path = os.path.join(VIDEO_DIR, "3-roteiro", "roteiro.txt")
    with open(roteiro_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("ROTEIRO COMPLETO") or line.startswith("Canal:") or line.startswith("Narrador:") or line.startswith("Tipo:"):
            continue
        if "=" * 10 in line:
            story.append(make_hr())
            continue
        if line.startswith("FASE"):
            story.append(Paragraph(line, style_h1))
            continue
        if line.startswith("NOTAS"):
            story.append(Paragraph(line, style_h1))
            continue
        if line.startswith("[EFEITO:") or line.startswith("[PAUSA"):
            story.append(Paragraph("<i>" + line + "</i>", style_quote))
            continue
        if line.startswith("- "):
            story.append(Paragraph(line, style_body))
            continue
        if line.startswith('"'):
            clean = line.strip('"')
            story.append(Paragraph(clean, style_body))
            continue
        story.append(Paragraph(line, style_body))

    story.append(make_hr())
    story.append(Paragraph("Assinado: Morrigan, Roteirista | Abismo Criativo", style_footer))
    doc.build(story)
    print(f"[OK] {path}")


def upload_to_vps(local_path, remote_path):
    """Upload PDF para VPS e retorna link HTTP."""
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key_path = os.path.expanduser("~/.ssh/id_ed25519")
    ssh.connect('31.97.165.64', username='root', key_filename=key_path)

    # Criar diretorio remoto
    remote_dir = os.path.dirname(remote_path)
    ssh.exec_command(f'mkdir -p {remote_dir}')

    # Upload
    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()
    ssh.close()

    # Gerar link HTTP
    rel = remote_path.replace('/opt/agencia/', '')
    url = f"http://31.97.165.64:3456/{rel}"
    print(f"[LINK] {url}")
    return url


def sync_all_to_vps():
    """Sincroniza todos os PDFs gerados para a VPS."""
    pdfs = [
        (os.path.join(VIDEO_DIR, "1-pesquisa", "pesquisa.pdf"),
         "/opt/agencia/canais/sinais-do-fim/videos/video-001-armagedom/1-pesquisa/pesquisa.pdf"),
        (os.path.join(VIDEO_DIR, "2-titulos", "titulos_seo.pdf"),
         "/opt/agencia/canais/sinais-do-fim/videos/video-001-armagedom/2-titulos/titulos_seo.pdf"),
        (os.path.join(VIDEO_DIR, "3-roteiro", "roteiro.pdf"),
         "/opt/agencia/canais/sinais-do-fim/videos/video-001-armagedom/3-roteiro/roteiro.pdf"),
    ]
    for local, remote in pdfs:
        if os.path.exists(local):
            upload_to_vps(local, remote)


if __name__ == "__main__":
    gerar_pesquisa_pdf()
    gerar_titulos_pdf()
    gerar_roteiro_pdf()
    print("\n[DONE] 3 PDFs gerados!")
    print("\n[SYNC] Enviando para VPS...")
    sync_all_to_vps()
    print("\n[DONE] PDFs sincronizados com VPS!")
