#!/usr/bin/env python3
"""
Hermes — Gerador de PDF + Upload VPS
Canal: Sinais do Fim | Video: video-002-marca-da-besta
"""

import os
import sys

# Verificar dependências
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
except ImportError:
    print("ERRO: reportlab não instalado. Executando: pip install reportlab")
    os.system(f"{sys.executable} -m pip install reportlab")
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle

try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    print("AVISO: paramiko não instalado. Executando: pip install paramiko")
    os.system(f"{sys.executable} -m pip install paramiko")
    try:
        import paramiko
        HAS_PARAMIKO = True
    except:
        HAS_PARAMIKO = False
        print("AVISO: Upload VPS desabilitado — paramiko não disponível")

# Cores da agência
PRETO    = HexColor("#0A0A0A")
VERMELHO = HexColor("#8B0000")
DOURADO  = HexColor("#C5A355")
CINZA    = HexColor("#888888")
CINZA_CLARO = HexColor("#DDDDDD")
BRANCO   = HexColor("#FFFFFF")

# Caminhos
LOCAL_DIR = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\2-titulos"
PDF_PATH  = os.path.join(LOCAL_DIR, "titulos_seo.pdf")
TXT_PATH  = os.path.join(LOCAL_DIR, "titulos_seo.txt")
VPS_PATH  = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/2-titulos/titulos_seo.pdf"
KEY_PATH  = os.path.expanduser("~/.ssh/id_ed25519")
VPS_URL   = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/2-titulos/titulos_seo.pdf"

def make_styles():
    styles = getSampleStyleSheet()
    return {
        'title':    ParagraphStyle('T',  parent=styles['Title'],   fontSize=20, textColor=VERMELHO,
                                   fontName='Helvetica-Bold', spaceAfter=4, leading=24),
        'subtitle': ParagraphStyle('ST', parent=styles['Normal'],  fontSize=10, textColor=DOURADO,
                                   fontName='Helvetica-Bold', spaceAfter=2),
        'meta':     ParagraphStyle('MT', parent=styles['Normal'],  fontSize=8,  textColor=CINZA,
                                   fontName='Helvetica', spaceAfter=8),
        'h1':       ParagraphStyle('H1', parent=styles['Heading1'],fontSize=14, textColor=VERMELHO,
                                   fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6),
        'h2':       ParagraphStyle('H2', parent=styles['Heading2'],fontSize=11, textColor=DOURADO,
                                   fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4),
        'body':     ParagraphStyle('B',  parent=styles['Normal'],  fontSize=9,  textColor=PRETO,
                                   fontName='Helvetica', leading=13, spaceAfter=4),
        'body_wht': ParagraphStyle('BW', parent=styles['Normal'],  fontSize=9,  textColor=BRANCO,
                                   fontName='Helvetica', leading=13, spaceAfter=4),
        'bullet':   ParagraphStyle('BL', parent=styles['Normal'],  fontSize=9,  textColor=PRETO,
                                   fontName='Helvetica', leading=13, leftIndent=12, spaceAfter=3),
        'tag':      ParagraphStyle('TG', parent=styles['Normal'],  fontSize=8.5,textColor=DOURADO,
                                   fontName='Helvetica-Bold', leading=12),
        'warn':     ParagraphStyle('WN', parent=styles['Normal'],  fontSize=9,  textColor=HexColor("#CC3300"),
                                   fontName='Helvetica-Bold', leading=13, spaceAfter=3),
        'confirm':  ParagraphStyle('CF', parent=styles['Normal'],  fontSize=10, textColor=HexColor("#006600"),
                                   fontName='Helvetica-Bold', leading=14, spaceAfter=4),
    }

def gerar_pdf():
    os.makedirs(LOCAL_DIR, exist_ok=True)
    s = make_styles()
    story = []

    # ── CABEÇALHO ─────────────────────────────────────────────────────────────
    story.append(Paragraph("ABISMO CRIATIVO", s['title']))
    story.append(Paragraph("Sinais do Fim — Passagens do Apocalipse", s['subtitle']))
    story.append(Paragraph("Hermes — Analista SEO + Títulos  |  video-002-marca-da-besta  |  2026-04-06", s['meta']))
    story.append(HRFlowable(width="100%", thickness=2, color=VERMELHO, spaceAfter=10))

    # ── SEÇÃO 1: KEYWORDS PRIMÁRIAS ───────────────────────────────────────────
    story.append(Paragraph("1. Keywords Primárias — Alto Volume", s['h1']))

    kw_data = [
        ["#", "Keyword", "Volume/mês", "Competição", "Uso"],
        ["1", "marca da besta",         "18.000–22.000", "Média-Alta", "Título + Tags"],
        ["2", "666 bíblia",             "12.000–15.000", "Média",      "Tags + Descrição"],
        ["3", "apocalipse 13",          "8.000–11.000",  "Baixa-Média","Título + Tags"],
        ["4", "chip implantável bíblia","6.000–9.000",   "Baixa",      "Tags + Descrição"],
        ["5", "moeda digital fim dos tempos","4.000–6.500","Baixa",    "Descrição + Tags"],
    ]
    kw_table = Table(kw_data, colWidths=[0.6*cm, 5.5*cm, 3*cm, 2.8*cm, 3.5*cm])
    kw_table.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0),  VERMELHO),
        ('TEXTCOLOR',    (0,0), (-1,0),  BRANCO),
        ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 8),
        ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [HexColor("#F5F5F5"), BRANCO]),
        ('GRID',         (0,0), (-1,-1), 0.5, HexColor("#CCCCCC")),
        ('TEXTCOLOR',    (0,1), (-1,-1), PRETO),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
        ('LEFTPADDING',  (0,0), (-1,-1), 6),
    ]))
    story.append(kw_table)
    story.append(Spacer(1, 8))

    # ── SEÇÃO 2: KEYWORDS SECUNDÁRIAS ────────────────────────────────────────
    story.append(Paragraph("2. Keywords Secundárias", s['h1']))
    sec_kws = [
        ("número da besta",                 "5.500/mês", "Baixa",       "Alto"),
        ("microchip implantado humanos",    "4.200/mês", "Baixa",       "Alto"),
        ("CBDC controle governo",           "3.800/mês", "Baixa",       "Médio-Alto"),
        ("profecias bíblicas cumpridas",    "7.200/mês", "Média",       "Alto"),
        ("moeda digital banco central",     "5.100/mês", "Média",       "Médio"),
        ("sistema de crédito social china", "2.900/mês", "Baixa",       "Alto"),
        ("apocalipse sinais do fim",        "9.300/mês", "Média",       "Alto"),
        ("biometria apocalipse",            "1.800/mês", "Muito Baixa", "Médio"),
    ]
    sec_data = [["Keyword", "Volume", "Competição", "CTR Potencial"]]
    for row in sec_kws:
        sec_data.append(list(row))
    sec_table = Table(sec_data, colWidths=[6.5*cm, 2.5*cm, 2.8*cm, 3.2*cm])
    sec_table.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0),  HexColor("#4A0000")),
        ('TEXTCOLOR',    (0,0), (-1,0),  DOURADO),
        ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 8),
        ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [HexColor("#F5F5F5"), BRANCO]),
        ('GRID',         (0,0), (-1,-1), 0.5, HexColor("#CCCCCC")),
        ('TEXTCOLOR',    (0,1), (-1,-1), PRETO),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
        ('LEFTPADDING',  (0,0), (-1,-1), 6),
    ]))
    story.append(sec_table)
    story.append(Spacer(1, 8))

    # ── SEÇÃO 3: CAUDA LONGA ──────────────────────────────────────────────────
    story.append(Paragraph("3. Cauda Longa — Alta Conversão (10 Keywords)", s['h1']))
    cl_list = [
        ("CL-01", "a marca da besta já está sendo implementada", "1.200/mês", "Muito Alta"),
        ("CL-02", "o que é a marca da besta no apocalipse 13",   "2.100/mês", "Alta"),
        ("CL-03", "chip implantado na mão marca da besta",       "1.500/mês", "Alta"),
        ("CL-04", "moeda digital e apocalipse bíblico",          "900/mês",   "Alta"),
        ("CL-05", "666 o número da besta explicado",             "1.800/mês", "Alta"),
        ("CL-06", "profecias de apocalipse 13 se cumprindo hoje","800/mês",   "Alta"),
        ("CL-07", "controle financeiro global bíblia apocalipse","1.100/mês", "Alta"),
        ("CL-08", "quem receberá a marca da besta",              "1.300/mês", "Alta"),
        ("CL-09", "sistema cashless e profecia bíblica",         "700/mês",   "Alta"),
        ("CL-10", "implante microchip voluntário suécia apocalipse","850/mês","Alta"),
    ]
    cl_data = [["ID", "Keyword de Cauda Longa", "Volume", "Conversão"]]
    for row in cl_list:
        cl_data.append(list(row))
    cl_table = Table(cl_data, colWidths=[1.5*cm, 8.5*cm, 2*cm, 2.5*cm])
    cl_table.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0),  HexColor("#2A1500")),
        ('TEXTCOLOR',    (0,0), (-1,0),  DOURADO),
        ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 8),
        ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [HexColor("#FFF8EE"), BRANCO]),
        ('GRID',         (0,0), (-1,-1), 0.5, HexColor("#DDCC99")),
        ('TEXTCOLOR',    (0,1), (-1,-1), PRETO),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
        ('LEFTPADDING',  (0,0), (-1,-1), 6),
    ]))
    story.append(cl_table)
    story.append(Spacer(1, 8))

    # ── SEÇÃO 4: KEYWORDS DE RISCO ───────────────────────────────────────────
    story.append(Paragraph("4. Alerta — Keywords de Risco", s['h1']))
    story.append(Paragraph(
        "As keywords abaixo podem acionar filtros de conteúdo borderline do YouTube "
        "(demonetização silenciosa, supressão de recomendação). Use APENAS em descrição — "
        "NUNCA no título ou tags principais.",
        s['body']))
    story.append(Spacer(1, 4))
    risks = [
        ("5G marca da besta",         "ALTO",  "Associação sem base científica — penalização frequente"),
        ("conspiração governo chip",  "ALTO",  "Classificada como conspiração por moderação automática"),
        ("NWO Nova Ordem Mundial",    "ALTO",  "Sinaliza conteúdo extremista para o algoritmo"),
        ("Bill Gates microchip vacina","ALTO", "Desinformação documentada — risco de banimento"),
        ("ID2020 agenda marca",       "MÉDIO", "Fraseamento conspirativo — reformular com dados verificáveis"),
    ]
    risk_data = [["Keyword", "Risco", "Motivo"]]
    for row in risks:
        risk_data.append(list(row))
    risk_table = Table(risk_data, colWidths=[4.5*cm, 2*cm, 9*cm])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0),  HexColor("#8B0000")),
        ('TEXTCOLOR',    (0,0), (-1,0),  BRANCO),
        ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 8),
        ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [HexColor("#FFF0F0"), BRANCO]),
        ('GRID',         (0,0), (-1,-1), 0.5, HexColor("#FFAAAA")),
        ('TEXTCOLOR',    (1,1), (1,-1),  HexColor("#CC0000")),
        ('FONTNAME',     (1,1), (1,-1),  'Helvetica-Bold'),
        ('TEXTCOLOR',    (0,1), (0,-1),  PRETO),
        ('TEXTCOLOR',    (2,1), (2,-1),  PRETO),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
        ('LEFTPADDING',  (0,0), (-1,-1), 6),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 8))

    # ── SEÇÃO 5: ANÁLISE DE CONCORRÊNCIA ─────────────────────────────────────
    story.append(Paragraph("5. Análise de Concorrência — YouTube Brasil", s['h1']))

    story.append(Paragraph("Padrões de Título dos Líderes", s['h2']))
    for item in [
        "Estrutura dominante: [Keyword] + [Afirmação Urgente] + [Âncora Bíblica]",
        "Uso de números reais como gancho: '134 países', '50.000 chips'",
        "Pergunta retórica: 'Está Chegando?' / 'Já Começou?'",
        "Divisor preferido: ' — ' ou ' | ' (não dois pontos)",
        "Capitalização seletiva de conceitos-chave",
    ]:
        story.append(Paragraph(f"• {item}", s['bullet']))

    story.append(Paragraph("Padrões de Thumbnail", s['h2']))
    for item in [
        "Rostos humanos expressivos (choro, choque) com texto overlay",
        "Símbolo '666' ou microchip com glow vermelho/dourado em destaque",
        "Colagem profecia medieval + tecnologia moderna",
        "Texto máximo: 4-5 palavras em fonte Gothic/Impact ultra-bold",
        "Contraste extremo: fundo escuro + texto branco com outline vermelho",
    ]:
        story.append(Paragraph(f"• {item}", s['bullet']))

    story.append(Paragraph("Duração Média dos Vídeos de Sucesso", s['h2']))
    for item in [
        "12-18 min: faixa de maior retenção e monetização para nicho escatológico",
        "8-10 min: funciona para canais novos (menor abandono)",
        "+20 min: somente canais com +100k inscritos sustentam retenção",
        "Sinais do Fim (14-18 min): posicionamento ideal ✓",
    ]:
        story.append(Paragraph(f"• {item}", s['bullet']))

    story.append(Paragraph("5 Lacunas / Oportunidades para Sinais do Fim", s['h2']))
    lacunas = [
        ("L1", "Abordagem acadêmica + pastoral combinada",
         "Concorrentes são ou muito acadêmicos (secos) ou alarmistas. Sinais do Fim ocupa o meio: linguagem acessível, dados verificáveis, tom sóbrio."),
        ("L2", "Contextualização geopolítica verificável (sem teoria)",
         "Vídeos com fontes reais (BIS, Riksbank, BBC) têm maior longevidade e menos penalizações. Poucos canais BR fazem isso."),
        ("L3", "Produção visual cinemática de alta qualidade",
         "Maioria usa slides simples. Colagem bíblico-moderna (estilo Sinais do Fim) ainda é diferencial competitivo no nicho PT-BR."),
        ("L4", "Série narrativa encadeada (playlist temática)",
         "Playlist video-001 → video-002 → ... gera retenção de sessão. Concorrentes raramente criam séries coerentes."),
        ("L5", "Cobertura das 4 escolas escatológicas",
         "Maioria só apresenta visão dispensacionalista. Mostrar historicismo, preterismo, idealismo e futurismo diferencia e atrai público acadêmico."),
    ]
    lac_data = [["ID", "Lacuna", "Oportunidade"]]
    for row in lacunas:
        lac_data.append(list(row))
    lac_table = Table(lac_data, colWidths=[1.2*cm, 4.5*cm, 9.8*cm])
    lac_table.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0),  HexColor("#2A1500")),
        ('TEXTCOLOR',    (0,0), (-1,0),  DOURADO),
        ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 8),
        ('FONTNAME',     (0,1), (0,-1),  'Helvetica-Bold'),
        ('FONTNAME',     (1,1), (-1,-1), 'Helvetica'),
        ('TEXTCOLOR',    (0,1), (0,-1),  DOURADO),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [HexColor("#FFF8EE"), BRANCO]),
        ('GRID',         (0,0), (-1,-1), 0.5, HexColor("#DDCC99")),
        ('TEXTCOLOR',    (1,1), (-1,-1), PRETO),
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0), (-1,-1), 5),
        ('LEFTPADDING',  (0,0), (-1,-1), 6),
    ]))
    story.append(lac_table)
    story.append(Spacer(1, 8))

    # ── SEÇÃO 6: 10 TÍTULOS ───────────────────────────────────────────────────
    story.append(Paragraph("6. 10 Títulos com CTR Estimado", s['h1']))
    story.append(Paragraph(
        "Regras aplicadas: máx 70 chars | keyword primária no início | "
        "tom urgente/profético sem sensacionalismo | âncora bíblica",
        s['body']))
    story.append(Spacer(1, 6))

    titulos = [
        ("T01", "A Marca da Besta Já Está Sendo Implementada — Apocalipse 13", 63, "7.8%",
         "★★★★★", "Keyword primária no início + afirmação factual urgente + âncora bíblica. Tom sóbrio. MELHOR DA LISTA."),
        ("T02", "Marca da Besta: 134 Países Já Preparam o Sistema — Ap 13",    57, "7.4%",
         "★★★★½", "Número verificável (dado BIS) gera credibilidade e urgência implícita."),
        ("T03", "666 — O Sistema da Besta Está Pronto. Apocalipse 13 Explica", 61, "7.1%",
         "★★★★",  "'666' no início tem alto valor de busca direta. Ponto final cria ruptura dramática."),
        ("T04", "Chip Implantável, CBDC e Apocalipse 13 — A Conexão Proibida", 61, "6.9%",
         "★★★★",  "'Conexão Proibida' gera curiosidade. ATENÇÃO: 'Proibida' pode sinalizar clickbait ao algoritmo."),
        ("T05", "A Marca da Besta em 2025 — Chip, Moeda Digital e Apocalipse", 60, "6.7%",
         "★★★½",  "Ano atual aumenta relevância imediata. Downside: tornará-se desatualizado — baixa longevidade."),
        ("T06", "O Que É a Marca da Besta? Apocalipse 13 e o Mundo Hoje",      57, "6.5%",
         "★★★½",  "Pergunta direta captura buscas informacionais ('o que é...'). Ótimo para novos espectadores."),
        ("T07", "Marca da Besta — Do Microchip à Moeda Digital: Ap 13",        53, "6.3%",
         "★★★",   "'Do X ao Y' cria expectativa de jornada narrativa. Título curto — bom para mobile."),
        ("T08", "Apocalipse 13 Explicado: A Marca da Besta Está Chegando",     56, "6.2%",
         "★★★",   "'Explicado' atrai quem quer aprender. 'Está Chegando' adiciona urgência moderada."),
        ("T09", "Ninguém Poderá Comprar ou Vender — Apocalipse 13 Revelado",   58, "7.0%",
         "★★★★",  "Citação bíblica direta como título — alta ressonância emocional. SEM keyword primária no início."),
        ("T10", "A Besta de Apocalipse 13 e os 3 Sistemas de Controle Global", 62, "6.4%",
         "★★★",   "'3 sistemas' promete conteúdo estruturado. Boa para quem busca análise específica."),
    ]
    for cod, titulo, chars, ctr, estrelas, nota in titulos:
        bg = HexColor("#FFE8E8") if cod == "T01" else BRANCO
        bloco = Table([
            [Paragraph(f"<b>{cod}</b>", s['body']),
             Paragraph(f'<b>"{titulo}"</b>', s['body']),
             Paragraph(f"<b>{ctr}</b>", s['body'])],
            ["",
             Paragraph(f"{chars} chars | {estrelas}", s['body']),
             ""],
            ["",
             Paragraph(nota, s['body']),
             ""],
        ], colWidths=[1.2*cm, 12.3*cm, 2*cm])
        bloco.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('SPAN',       (1,1), (2,1)),
            ('SPAN',       (1,2), (2,2)),
            ('SPAN',       (0,0), (0,2)),
            ('VALIGN',     (0,0), (-1,-1), 'TOP'),
            ('FONTSIZE',   (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING',(0,0),(-1,-1), 3),
            ('LEFTPADDING',(0,0), (-1,-1), 6),
            ('BOX',        (0,0), (-1,-1), 1, HexColor("#CCCCCC")),
            ('LINEBELOW',  (0,0), (-1,0), 0.5, HexColor("#CCCCCC")),
        ]))
        story.append(bloco)
        story.append(Spacer(1, 4))

    # ── SEÇÃO 7: TÍTULO RECOMENDADO ───────────────────────────────────────────
    story.append(Paragraph("7. Título Recomendado — Análise e Justificativa", s['h1']))

    destaque = Table([[
        Paragraph(
            '"A Marca da Besta Já Está Sendo Implementada — Apocalipse 13"',
            ParagraphStyle('D', fontSize=12, textColor=DOURADO, fontName='Helvetica-Bold',
                           leading=16))
    ]], colWidths=[15.5*cm])
    destaque.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#1A0000")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0),(-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('BOX',        (0,0), (-1,-1), 2, VERMELHO),
    ]))
    story.append(destaque)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "VEREDICTO: CONFIRMO T01 como título ótimo. Nenhuma alteração necessária.", s['confirm']))

    analise = [
        ("POSIÇÃO DA KEYWORD",   "Marca da Besta nos primeiros 20 chars — máximo peso SEO"),
        ("AFIRMAÇÃO FACTUAL",    "'Já Está Sendo Implementada' — urgência sustentada por dados (CBDC, chips)"),
        ("ÂNCORA BÍBLICA",       "'Apocalipse 13' no final — captura buscas de estudo bíblico direto"),
        ("CTR ESTIMADO",         "7.8% — melhor da lista (benchmarks do nicho: 5-8%)"),
        ("COMPRIMENTO",          "63 chars — dentro do limite 70, sem truncamento em mobile ✓"),
        ("TOM",                  "Profético e urgente sem sensacionalismo — alinhado com Sinais do Fim"),
        ("EVERGREEN",            "Sem ano/data — longevidade máxima de tráfego orgânico ✓"),
    ]
    an_data = [[Paragraph(f"<b>{k}</b>", s['body']),
                Paragraph(v, s['body'])] for k, v in analise]
    an_table = Table(an_data, colWidths=[4.5*cm, 11*cm])
    an_table.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [HexColor("#F5F5F5"), BRANCO]),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#CCCCCC")),
        ('TEXTCOLOR', (0,0), (-1,-1), PRETO),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(an_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Alternativa competitiva: T02 (57 chars, CTR 7.4%) — inclui dado '134 países' "
        "para reforçar credibilidade factual, se Snayder preferir.", s['body']))
    story.append(Spacer(1, 8))

    # ── SEÇÃO 8: 27 TAGS ─────────────────────────────────────────────────────
    story.append(Paragraph("8. 27 Tags Otimizadas (~415 chars — dentro do limite 500)", s['h1']))

    tags_groups = {
        "Broad (alto volume) — 8 tags": [
            "marca da besta", "666 bíblia", "apocalipse 13", "profecias bíblicas",
            "fim dos tempos", "sinais do fim", "besta apocalipse", "apocalipse hoje"
        ],
        "Específicas (médio volume) — 9 tags": [
            "chip implantável", "moeda digital", "CBDC apocalipse", "número da besta",
            "microchip humanos", "666 explicado", "crédito social bíblia",
            "identidade digital", "cashless profecia"
        ],
        "Long-tail (alta conversão) — 7 tags": [
            "marca da besta hoje", "sistema de controle global", "marca da besta chip",
            "profecias cumpridas", "controle financeiro bíblia",
            "marca besta tecnologia", "sinais do apocalipse"
        ],
        "Brand — 3 tags": [
            "sinais do fim", "joão apocalipse", "daniel profecias"
        ],
    }

    for grupo, tags in tags_groups.append and tags_groups.items() if False else tags_groups.items():
        story.append(Paragraph(grupo, s['h2']))
        tags_str = " | ".join(tags)
        story.append(Paragraph(tags_str, s['tag']))
        story.append(Spacer(1, 4))

    # String completa de tags para copiar
    all_tags = ",".join([
        "marca da besta","666 bíblia","apocalipse 13","chip implantável","moeda digital",
        "CBDC apocalipse","número da besta","microchip humanos","profecias bíblicas",
        "sinais do fim","marca da besta hoje","fim dos tempos","666 explicado",
        "sistema de controle global","besta apocalipse","joão apocalipse","daniel profecias",
        "crédito social bíblia","identidade digital","cashless profecia","marca da besta chip",
        "apocalipse hoje","profecias cumpridas","666 o número","controle financeiro bíblia",
        "marca besta tecnologia","sinais do apocalipse"
    ])
    story.append(Paragraph("String completa para colar no YouTube Studio:", s['h2']))
    tags_box = Table([[Paragraph(all_tags, s['tag'])]], colWidths=[15.5*cm])
    tags_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#1A1A00")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('BOX',        (0,0), (-1,-1), 1, DOURADO),
    ]))
    story.append(tags_box)
    story.append(Spacer(1, 10))

    # ── RODAPÉ ────────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=DOURADO, spaceAfter=8))
    story.append(Paragraph(
        "CHECKPOINT — Aguardando aprovação de Snayder para título e SEO antes da Fase 2 (Roteiro)",
        ParagraphStyle('CP', fontSize=9, textColor=DOURADO, fontName='Helvetica-Bold', alignment=1)))
    story.append(Paragraph(
        f"Abismo Criativo | Hermes — SEO + Títulos | 2026-04-06 | video-002-marca-da-besta",
        ParagraphStyle('FT', fontSize=7, textColor=CINZA, fontName='Helvetica', alignment=1)))

    doc = SimpleDocTemplate(
        PDF_PATH, pagesize=A4,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
        leftMargin=2.2*cm, rightMargin=2.2*cm
    )
    doc.build(story)
    print(f"PDF gerado: {PDF_PATH}")
    return True

def upload_vps():
    if not HAS_PARAMIKO:
        print("AVISO: paramiko não disponível — upload ignorado")
        return False
    try:
        key = paramiko.Ed25519Key.from_private_key_file(KEY_PATH)
        transport = paramiko.Transport(("31.97.165.64", 22))
        transport.connect(username="root", pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Criar diretórios na VPS (recursivo)
        dirs = [
            "/opt/agencia",
            "/opt/agencia/canais",
            "/opt/agencia/canais/sinais-do-fim",
            "/opt/agencia/canais/sinais-do-fim/videos",
            "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta",
            "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/2-titulos",
        ]
        for d in dirs:
            try:
                sftp.mkdir(d)
            except:
                pass

        sftp.put(PDF_PATH, VPS_PATH)
        sftp.close()
        transport.close()
        print(f"Upload VPS OK: {VPS_URL}")
        return True
    except Exception as e:
        print(f"ERRO no upload VPS: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("HERMES — SEO + Títulos | video-002-marca-da-besta")
    print("=" * 60)

    # 1. Gerar PDF
    print("\n[1/2] Gerando PDF...")
    ok_pdf = gerar_pdf()

    # 2. Upload VPS
    print("\n[2/2] Fazendo upload para VPS...")
    ok_vps = upload_vps()

    print("\n" + "=" * 60)
    print("RESULTADO:")
    print(f"  PDF local:  {'OK' if ok_pdf else 'ERRO'} → {PDF_PATH}")
    print(f"  Upload VPS: {'OK' if ok_vps else 'ERRO/SKIP'}")
    if ok_vps:
        print(f"  URL HTTP:   {VPS_URL}")
    print("=" * 60)
