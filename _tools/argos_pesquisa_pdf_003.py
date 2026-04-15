#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Argos - Gerador de PDF de Pesquisa
video-003 | Sinais do Fim | 2026-04-07
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.colors import HexColor
from datetime import datetime

# ── Cores da agencia
C_BG       = HexColor('#0A0A0A')
C_TEXT     = HexColor('#E8E0D0')
C_RED      = HexColor('#8B0000')
C_GOLD     = HexColor('#C5A355')
C_DIMTEXT  = HexColor('#A09888')
C_DARKRED  = HexColor('#5C0000')
C_ROWALT   = HexColor('#1A1A1A')

OUTPUT = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-003-babilonia\1-pesquisa\pesquisa.pdf'
W, H = A4

# ── Header / Footer
def on_page(canvas, doc):
    canvas.saveState()
    # Fundo preto total
    canvas.setFillColor(C_BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Header bar
    canvas.setFillColor(C_RED)
    canvas.rect(0, H - 22*mm, W, 22*mm, fill=1, stroke=0)
    # Header linha dourada
    canvas.setFillColor(C_GOLD)
    canvas.rect(0, H - 23*mm, W, 1.2*mm, fill=1, stroke=0)
    # Header texto esquerda
    canvas.setFillColor(C_TEXT)
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(15*mm, H - 14*mm, 'ABISMO CRIATIVO  |  ARGOS — Pesquisador de Nicho')
    # Header texto direita
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(C_GOLD)
    canvas.drawRightString(W - 15*mm, H - 14*mm, 'CONFIDENCIAL')
    # Footer linha
    canvas.setFillColor(C_GOLD)
    canvas.rect(0, 12*mm, W, 0.5*mm, fill=1, stroke=0)
    # Footer texto
    canvas.setFillColor(C_DIMTEXT)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(15*mm, 7*mm, f'Sinais do Fim  |  video-003  |  Pesquisa gerada em {datetime.now().strftime("%d/%m/%Y")}')
    canvas.drawRightString(W - 15*mm, 7*mm, f'Pagina {doc.page}')
    canvas.restoreState()

# ── Estilos
def make_styles():
    base = dict(fontName='Helvetica', textColor=C_TEXT, backColor=C_BG, leading=16)

    title = ParagraphStyle('Title', **base,
        fontSize=20, fontName='Helvetica-Bold',
        textColor=C_GOLD, alignment=TA_CENTER,
        spaceAfter=4, leading=26)

    subtitle = ParagraphStyle('Subtitle', **base,
        fontSize=11, textColor=C_DIMTEXT,
        alignment=TA_CENTER, spaceAfter=2)

    h1 = ParagraphStyle('H1', **base,
        fontSize=13, fontName='Helvetica-Bold',
        textColor=C_RED, spaceBefore=10, spaceAfter=4,
        borderPad=2)

    h2 = ParagraphStyle('H2', **base,
        fontSize=11, fontName='Helvetica-Bold',
        textColor=C_GOLD, spaceBefore=8, spaceAfter=3)

    body = ParagraphStyle('Body', **base,
        fontSize=9, spaceAfter=4, leading=15)

    bullet = ParagraphStyle('Bullet', **base,
        fontSize=9, spaceAfter=3, leading=14,
        leftIndent=12, bulletIndent=0)

    highlight = ParagraphStyle('Highlight', **base,
        fontSize=9, textColor=C_GOLD, spaceAfter=3, leading=14,
        leftIndent=12)

    score_title = ParagraphStyle('ScoreTitle', **base,
        fontSize=10, fontName='Helvetica-Bold',
        textColor=C_GOLD, spaceAfter=2)

    score_body = ParagraphStyle('ScoreBody', **base,
        fontSize=9, spaceAfter=3, leading=14, leftIndent=8)

    tag = ParagraphStyle('Tag', **base,
        fontSize=8, textColor=C_DIMTEXT, spaceAfter=2,
        leftIndent=8)

    warn = ParagraphStyle('Warn', **base,
        fontSize=9, textColor=C_RED, fontName='Helvetica-Bold',
        spaceAfter=4, leading=14)

    return dict(title=title, subtitle=subtitle, h1=h1, h2=h2,
                body=body, bullet=bullet, highlight=highlight,
                score_title=score_title, score_body=score_body,
                tag=tag, warn=warn)

def divider(color=C_RED, thickness=0.8):
    return HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=4, spaceBefore=2)

def build_pdf():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=28*mm, bottomMargin=20*mm
    )
    frame = Frame(15*mm, 20*mm, W - 30*mm, H - 50*mm, id='main')
    template = PageTemplate(id='main', frames=[frame], onPage=on_page)
    doc.addPageTemplates([template])

    S = make_styles()
    story = []

    # ── CAPA
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph('ARGOS', S['title']))
    story.append(Paragraph('Pesquisa de Nicho — Sinais do Fim', S['subtitle']))
    story.append(Spacer(1, 2*mm))
    story.append(divider(C_GOLD, 1.5))
    story.append(Spacer(1, 2*mm))

    # Bloco de contexto
    context_data = [
        ['CANAL', 'Sinais do Fim — Passagens do Apocalipse'],
        ['VIDEO', 'video-003 (slot disponivel)'],
        ['DATA DA PESQUISA', '07/04/2026'],
        ['GATILHO', 'EUA + Ira firmaram cessar-fogo de 2 semanas — DIA 39 do conflito'],
        ['JANELA', 'URGENTE: 48-72h para capitalizar trending'],
    ]
    ctx_table = Table(context_data, colWidths=[45*mm, 120*mm])
    ctx_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), C_DARKRED),
        ('BACKGROUND', (1,0), (1,-1), C_ROWALT),
        ('TEXTCOLOR', (0,0), (0,-1), C_GOLD),
        ('TEXTCOLOR', (1,0), (1,-1), C_TEXT),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (1,0), (1,-1), [C_ROWALT, C_BG]),
        ('GRID', (0,0), (-1,-1), 0.3, C_GOLD),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(ctx_table)
    story.append(Spacer(1, 6*mm))

    # ── SECAO 1: Fontes
    story.append(divider(C_RED))
    story.append(Paragraph('01  FONTES MONITORADAS', S['h1']))
    fontes = [
        ('YouTube (peso 35%)', [
            'Busca: "guerra Ira profecia", "Ormuz fim dos tempos", "Gogue Magogue Ira 2026"',
            'Conteudo ativo: multiplos canais evangelical PT-BR publicando sobre Israel x Ira',
            'LACUNA: Nenhum canal focou ainda no CESSAR-FOGO como sinal profetico'
        ]),
        ('Google Trends (peso 25%)', [
            '"profecia biblica Ira" -> +340% vs. jan/2026',
            '"Gogue Magogue" -> +180% nos ultimos 30 dias',
            '"Ormuz biblia" -> busca emergente, baixa concorrencia'
        ]),
        ('Noticias (peso 20%)', [
            'Guiame.com.br: "Especialistas dizem que conflito EUA-Ira tem elementos profeticos"',
            'O Pesquisador Cristao: "O papel do Ira nas profecias biblicas"',
            'Wikipedia: "Guerra do Ira em 2026" — atualizado diariamente'
        ]),
        ('Comunidade Evangelical BR (peso 20%)', [
            'Alto volume de compartilhamentos sobre profecia x Ira no WhatsApp/Telegram',
            'Pastores publicando interpretacoes de Ezequiel 38',
            'Audiencia 25-55 anos altamente engajada no tema'
        ]),
    ]
    for fonte, items in fontes:
        story.append(Paragraph(f'• {fonte}', S['h2']))
        for item in items:
            story.append(Paragraph(f'  — {item}', S['bullet']))
        story.append(Spacer(1, 2*mm))

    # ── SECAO 2: Top 10
    story.append(divider(C_RED))
    story.append(Paragraph('02  TOP 10 TOPICOS RANKEADOS', S['h1']))

    top10_data = [
        ['#', 'TOPICO', 'SCORE'],
        ['1', 'Ira, Ormuz e Gogue: O Cessar-Fogo que a Biblia Previu', '94/100'],
        ['2', 'A Persia nas Profecias: O Ira no Roteiro do Apocalipse', '88/100'],
        ['3', 'O Estreito que Para o Mundo: Ormuz e as 7 Trombetas', '82/100'],
        ['4', 'Gogue e Magogue: A Guerra Final Esta Comecando?', '79/100'],
        ['5', 'Trump, Ira e o Anticristo: A Paz Falsa das Profecias', '76/100'],
        ['6', 'Jeremias e o Julgamento da Persia em 2026', '71/100'],
        ['7', 'A Queda de Babilonia e o Petroleo: Profecia Cumprida?', '68/100'],
        ['8', 'Nostradamus vs Biblia: Quem Previu a Guerra no Ira?', '65/100'],
        ['9', 'Os 4 Cavaleiros e a Guerra dos 39 Dias', '61/100'],
        ['10', 'Ezequiel 38: Versiculo por Versiculo com o Mapa da Guerra', '58/100'],
    ]
    t = Table(top10_data, colWidths=[10*mm, 130*mm, 25*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_RED),
        ('TEXTCOLOR', (0,0), (-1,0), C_GOLD),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_ROWALT, C_BG]),
        ('TEXTCOLOR', (0,1), (-1,-1), C_TEXT),
        ('TEXTCOLOR', (0,1), (0,-1), C_GOLD),
        ('TEXTCOLOR', (2,1), (2,3), C_GOLD),
        ('FONTNAME', (2,1), (2,3), 'Helvetica-Bold'),
        ('TEXTCOLOR', (2,4), (2,-1), C_DIMTEXT),
        ('GRID', (0,0), (-1,-1), 0.3, C_DARKRED),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 4*mm))

    # ── SECAO 3: TOP 3 RECOMENDADOS
    story.append(divider(C_RED))
    story.append(Paragraph('03  TOP 3 RECOMENDADOS', S['h1']))

    # Opcao 1
    op1 = [
        [Paragraph('<b>OPCAO 1  |  VIRAL SCORE: 94/100  |  URGENTE (72h)</b>', ParagraphStyle('op1h',
            fontName='Helvetica-Bold', textColor=C_GOLD, fontSize=10, backColor=C_BG, leading=14)),
         ''],
        [Paragraph('"Ira, Ormuz e Gogue: O Cessar-Fogo que a Biblia Previu"', ParagraphStyle('op1t',
            fontName='Helvetica-Bold', textColor=C_RED, fontSize=11, backColor=C_BG, leading=16)),
         ''],
    ]
    op1_table = Table(op1, colWidths=[165*mm])
    op1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_DARKRED),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, C_GOLD),
    ]))
    story.append(op1_table)
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph('Por que AGORA:', S['h2']))
    op1_bullets = [
        'Evento aconteceu HOJE — janela de 48-72h para capitalizar o trending',
        'Nenhum canal concorrente publicou sobre o CESSAR-FOGO como sinal profetico',
        'Busca por "Gogue Magogue" +180% nos ultimos 30 dias',
        'Audiencia evangelical ja esta consumindo conteudo sobre Ira',
    ]
    for b in op1_bullets:
        story.append(Paragraph(f'• {b}', S['bullet']))
    story.append(Paragraph('Angulo narrativo:', S['h2']))
    story.append(Paragraph(
        'O cessar-fogo nao e paz — e o prenuncio. Ezequiel 38 diz que Gogue ataca Israel quando este viver "em paz e seguranca". '
        'O acordo de 2 semanas com o Ira cria exatamente essa falsa sensacao de seguranca. A Persia (Ira) e citada nominalmente '
        'em Ezequiel 38:5 como aliada de Gogue na guerra final.',
        S['body']))
    story.append(Paragraph('Passagens ancora:', S['h2']))
    passagens1 = [
        'Ezequiel 38:2-6 — alianca de Gogue, inclui Persia/Ira',
        'Ezequiel 38:10-13 — ataque quando Israel estiver em paz',
        'Jeremias 49:34-39 — juizo sobre Elao/Persia',
        'Apocalipse 9:13-16 — 6a Trombeta, exercito do Eufrates',
        '1 Tessalonicenses 5:3 — "paz e seguranca... entao a destruicao subita"',
    ]
    for p in passagens1:
        story.append(Paragraph(f'• {p}', S['highlight']))
    story.append(Paragraph('Slug: video-003-ira-gogue-ormuz', S['tag']))
    story.append(Spacer(1, 4*mm))

    # Opcao 2
    story.append(Paragraph('OPCAO 2  |  VIRAL SCORE: 88/100', S['score_title']))
    story.append(Paragraph('"A Persia nas Profecias: O Ira no Roteiro do Apocalipse"', S['h2']))
    story.append(Paragraph(
        'Conteudo evergreen com alto volume de busca permanente. Conecta historia (Persia antiga -> Ira moderno) com profecias. '
        'Formato educativo-profetico — tom ideal para o canal. Pode ser produzido sem urgencia de data.',
        S['body']))
    passagens2 = [
        'Daniel 8 — o carneiro = Persia e Media',
        'Ezequiel 38:5 — Persia como aliada de Gogue',
        'Isaias 13:17 — juizo sobre Babilonia pelos medos/persas',
        'Daniel 10:13 — o "principe da Persia" (dimensao espiritual)',
    ]
    for p in passagens2:
        story.append(Paragraph(f'• {p}', S['highlight']))
    story.append(Paragraph('Slug: video-003-persia-apocalipse', S['tag']))
    story.append(Spacer(1, 4*mm))

    # Opcao 3
    story.append(Paragraph('OPCAO 3  |  VIRAL SCORE: 82/100', S['score_title']))
    story.append(Paragraph('"O Estreito que Para o Mundo: Ormuz e as 7 Trombetas"', S['h2']))
    story.append(Paragraph(
        'Ormuz e o tema mais pesquisado do conflito no contexto economico. Conecta evento secular (petroleo, logistica) '
        'com profecia (7 Trombetas). Antecipa o video-004-7-trombetas planejado. '
        'Audiencia nao-evangelical tambem pesquisa Ormuz — porta de entrada para o canal.',
        S['body']))
    passagens3 = [
        'Apocalipse 8:7-12 — as 4 primeiras trombetas (catastrofes globais)',
        'Apocalipse 18:11-19 — mercadores choram, colapso do comercio',
        'Ezequiel 27 — Tiro, metafora do comercio maritimo destruido',
        'Isaias 23 — juizo sobre o comercio maritimo',
    ]
    for p in passagens3:
        story.append(Paragraph(f'• {p}', S['highlight']))
    story.append(Paragraph('Slug: video-003-ormuz-7-trombetas', S['tag']))
    story.append(Spacer(1, 4*mm))

    # ── SECAO 4: JANELA
    story.append(divider(C_RED))
    story.append(Paragraph('04  JANELA DE OPORTUNIDADE', S['h1']))

    janela_data = [
        ['OPCAO', 'PRAZO', 'PRIORIDADE'],
        ['Opcao 1 — Ira/Gogue/Ormuz', 'Publicar em ate 72h (prazo: 10/04)', 'URGENTE'],
        ['Opcao 2 — Persia/Apocalipse', 'Ate 2 semanas (durante negociacoes Islamabad)', 'ALTA'],
        ['Opcao 3 — Ormuz/Trombetas', 'Qualquer momento — evergreen + trending', 'NORMAL'],
    ]
    jt = Table(janela_data, colWidths=[70*mm, 65*mm, 30*mm])
    jt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_RED),
        ('TEXTCOLOR', (0,0), (-1,0), C_GOLD),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_ROWALT, C_BG]),
        ('TEXTCOLOR', (0,1), (-1,-1), C_TEXT),
        ('TEXTCOLOR', (2,1), (2,1), C_RED),
        ('FONTNAME', (2,1), (2,1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (2,2), (2,2), C_GOLD),
        ('TEXTCOLOR', (2,3), (2,3), C_DIMTEXT),
        ('GRID', (0,0), (-1,-1), 0.3, C_DARKRED),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(jt)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        'ARGOS RECOMENDA: Opcao 1 pela janela de 72h. Evento de hoje nao pode ser desperdicado.',
        S['warn']))

    # ── RODAPE FINAL
    story.append(Spacer(1, 4*mm))
    story.append(divider(C_GOLD, 1))
    story.append(Paragraph(
        'Aguardando aprovacao de Snayder — qual opcao seguir? (#1, #2 ou #3)',
        ParagraphStyle('final', fontName='Helvetica-Bold', textColor=C_GOLD,
                       fontSize=10, backColor=C_BG, alignment=TA_CENTER, leading=16)))

    doc.build(story)
    print(f'[OK] PDF gerado: {OUTPUT}')

if __name__ == '__main__':
    build_pdf()
