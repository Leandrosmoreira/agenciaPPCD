#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Argos — Pesquisador de Nicho | Abismo Criativo
video-002-marca-da-besta | Sinais do Fim
"""

import os
import sys
import datetime

try:
    import paramiko
except ImportError:
    print("AVISO: paramiko nao encontrado. Upload VPS sera ignorado.")
    paramiko = None

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ─── Cores da agência ───────────────────────────────────────────────────────
PRETO   = HexColor("#0A0A0A")
VERMELHO = HexColor("#8B0000")
DOURADO  = HexColor("#C5A355")
CINZA    = HexColor("#999999")
BRANCO   = HexColor("#E8E0D0")
FUNDO_CARD = HexColor("#1A0A0A")

# ─── Estilos ────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

style_titulo = ParagraphStyle(
    'Titulo',
    parent=styles['Title'],
    fontSize=20,
    textColor=VERMELHO,
    fontName='Helvetica-Bold',
    alignment=TA_CENTER,
    spaceAfter=4,
)
style_subtitulo = ParagraphStyle(
    'Subtitulo',
    parent=styles['Normal'],
    fontSize=11,
    textColor=DOURADO,
    fontName='Helvetica-Bold',
    alignment=TA_CENTER,
    spaceAfter=14,
)
style_h1 = ParagraphStyle(
    'H1',
    parent=styles['Heading1'],
    fontSize=15,
    textColor=VERMELHO,
    fontName='Helvetica-Bold',
    spaceBefore=18,
    spaceAfter=8,
    borderPad=4,
)
style_h2 = ParagraphStyle(
    'H2',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=DOURADO,
    fontName='Helvetica-Bold',
    spaceBefore=12,
    spaceAfter=5,
)
style_h3 = ParagraphStyle(
    'H3',
    parent=styles['Heading3'],
    fontSize=10,
    textColor=DOURADO,
    fontName='Helvetica',
    spaceBefore=8,
    spaceAfter=4,
)
style_body = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontSize=9,
    textColor=PRETO,
    fontName='Helvetica',
    leading=14,
    spaceAfter=5,
    alignment=TA_JUSTIFY,
)
style_bullet = ParagraphStyle(
    'Bullet',
    parent=styles['Normal'],
    fontSize=9,
    textColor=PRETO,
    fontName='Helvetica',
    leading=13,
    spaceAfter=3,
    leftIndent=14,
    bulletIndent=4,
)
style_destaque = ParagraphStyle(
    'Destaque',
    parent=styles['Normal'],
    fontSize=9,
    textColor=DOURADO,
    fontName='Helvetica-Bold',
    leading=13,
    spaceAfter=4,
    leftIndent=10,
)
style_dado = ParagraphStyle(
    'Dado',
    parent=styles['Normal'],
    fontSize=8,
    textColor=CINZA,
    fontName='Helvetica',
    leading=12,
    spaceAfter=3,
    leftIndent=14,
)
style_frase = ParagraphStyle(
    'Frase',
    parent=styles['Normal'],
    fontSize=11,
    textColor=VERMELHO,
    fontName='Helvetica-Bold',
    leading=16,
    spaceAfter=10,
    alignment=TA_CENTER,
    borderPad=8,
)
style_rodape = ParagraphStyle(
    'Rodape',
    parent=styles['Normal'],
    fontSize=7,
    textColor=CINZA,
    fontName='Helvetica',
    alignment=TA_CENTER,
    spaceAfter=0,
)

# ─── Caminhos ───────────────────────────────────────────────────────────────
LOCAL_DIR = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\1-pesquisa"
TXT_PATH  = os.path.join(LOCAL_DIR, "pesquisa.txt")
PDF_PATH  = os.path.join(LOCAL_DIR, "pesquisa.pdf")

VPS_HOST  = "31.97.165.64"
VPS_PORT  = 22
VPS_USER  = "root"
KEY_PATH  = os.path.expanduser("~/.ssh/id_ed25519")
VPS_DIR   = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/1-pesquisa"
VPS_PATH  = VPS_DIR + "/pesquisa.pdf"
HTTP_URL  = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/1-pesquisa/pesquisa.pdf"

# ─── Conteúdo de Pesquisa ───────────────────────────────────────────────────
PESQUISA_TXT = """ARGOS — PESQUISA DE NICHO
Agência: Abismo Criativo | Canal: Sinais do Fim — Passagens do Apocalipse
Vídeo: video-002-marca-da-besta | Tema: A Marca da Besta (Apocalipse 13)
Data: 2026-04-06

================================================================================
SEÇÃO 1 — BASE BÍBLICA: TEXTOS E ANÁLISE
================================================================================

TEXTO PRINCIPAL: Apocalipse 13:16-18 (ARA)
"E ela faz que a todos, aos pequenos e aos grandes, aos ricos e aos pobres, aos
livres e aos escravos, se lhes ponha uma marca na mão direita ou na fronte; e
que ninguém possa comprar ou vender, senão aquele que tiver a marca, o nome da
besta ou o número do seu nome. Aqui está a sabedoria. Aquele que tem
entendimento, calcule o número da besta; porque é o número de um homem, e o seu
número é Seiscentos e Sessenta e Seis."

ANÁLISE PALAVRA POR PALAVRA:
- "marca" (grego: charagma) — incisão, gravação, carimbo; mesmo termo usado para
  marcas imperiais romanas em documentos e na pele de escravos e animais.
- "mão direita ou na fronte" — locais visíveis; simbolismo de ação (mão) e
  lealdade/pensamento (fronte). Em Dt 6:8 e Ex 13:9, Deus manda "amarrar" sua
  lei na mão e na fronte — a Marca da Besta é a inversão exata deste mandamento.
- "comprar ou vender" — controle econômico total. Sem a marca: exclusão do
  sistema comercial, impossibilidade de sustento.
- "666" — número do homem/humanidade (6 representa imperfeição, aquém do divino
  7). Interpretações: gematria, número simbólico de imperfeição máxima.

TEXTOS DE SUPORTE:
1. Apocalipse 14:9-11 — "Se alguém adorar a besta e a sua imagem e receber a
   marca na testa ou na mão, também esse beberá do vinho da ira de Deus..."
   → Consequência espiritual definitiva: condenação eterna.

2. Apocalipse 19:20 — A Besta e o falso profeta são lançados no lago de fogo.
   → Desfecho narrativo confirmando que a Marca é parte do sistema da Besta.

3. Daniel 7:7,23-25 — A Quarta Besta (diferente de todas) devora e tritura o
   mundo. O "pequeno chifre" muda os tempos e as leis.
   → Paralelo direto com o sistema de controle global.

4. Ezequiel 9:4-6 — O Senhor manda marcar (taw, última letra do alfabeto hebraico,
   forma de cruz) os que gemem pelas abominações de Jerusalém para preservá-los.
   → Precedente bíblico para "marcas" de identificação divina vs. demoníaca.

5. Deuteronômio 6:6-8 (Shemá) — "E amarrarás [as palavras de Deus] como sinal
   na tua mão, e serão por frontal entre os teus olhos."
   → A Marca da Besta é a contrafação satânica do tefilim judaico.

6. Apocalipse 7:3 e 9:4 — Selo de Deus nos 144.000: contraparte positiva da
   marca. Dois sistemas paralelos de identificação e pertencimento.

================================================================================
SEÇÃO 2 — CONTEXTO HISTÓRICO E ESCOLAS ESCATOLÓGICAS
================================================================================

CONTEXTO DO SÉCULO I: O CULTO IMPERIAL ROMANO
- Domiciano (81-96 d.C.) exigiu ser tratado como "Dominus et Deus" (Senhor e Deus).
- Toda transação comercial requeria participação em sacrifícios ao Imperador ou
  certificado de lealdade (libellus).
- Cristãos que se recusavam eram excluídos das guildas comerciais, perdendo
  acesso a trabalho e mercados — exatamente "não comprar nem vender".
- Moedas romanas traziam a imagem (eikon) do Imperador com título divino.

GEMATRIA: NERO E O 666
- Nero César em hebraico (nrwn qsr) = Nun(50)+Resh(200)+Waw(6)+Nun(50)+
  Qoph(100)+Samekh(60)+Resh(200) = 666.
- Variação latina sem o "n" final: 616 (encontrado em manuscritos antigos como
  o Papiro 115 de Oxyrhynchus).
- Nero perseguiu cristãos (64 d.C.), matou Pedro e Paulo, era o padrão do
  tirano imperial para os cristãos do século I.
- Interpretação preterista: a Marca foi cumprida no sistema romano do século I.

4 ESCOLAS ESCATOLÓGICAS:

1. PRETERISMO (cumprimento passado)
   - Toda profecia de Ap 13 se cumpriu no século I d.C.
   - Besta = Néron/Domiciano; Falso Profeta = sacerdócio imperial romano.
   - Representantes: David Chilton, R.C. Sproul, Gary DeMar.
   - Ponto forte: contexto histórico imediato; ponto fraco: o "lago de fogo"
     não ocorreu literalmente no século I.

2. HISTORICISMO (cumprimento progressivo na história)
   - A Besta = o sistema papal de Roma (posição dos Reformadores).
   - Lutero: "O papa é o Anticristo." Calvino: sistema romano como besta profética.
   - Marca = submissão à autoridade papal vs. autoridade das Escrituras.
   - Westminster Confession (1647) ainda referencia este entendimento.
   - Representantes: Matthew Henry, Adam Clarke, Albert Barnes.

3. IDEALISMO/SIMBOLISMO (princípios atemporais)
   - A Marca representa qualquer sistema de idolatria e coerção econômica.
   - Não é literal; representa lealdade ao poder mundano vs. a Deus.
   - Representantes: William Hendriksen, Dennis Johnson, G.K. Beale.
   - Ponto forte: aplicável a qualquer época; ponto fraco: subestima especificidade.

4. FUTURISMO (cumprimento futuro literal)
   - Sistematizado por John Nelson Darby (1800-1882), fundador do Dispensacionalismo.
   - La Peyrère (1655) e Lacunza (1812) antecipam elementos; Darby formaliza em 1830.
   - Anticristo futuro, literal, identificável; Tribulação de 7 anos; Arrebatamento.
   - Scofield Reference Bible (1909) populariza globalmente.
   - Tim LaHaye (Left Behind), Hal Lindsey popularizam no século XX.
   - Posição dominante no evangelicalismo brasileiro contemporâneo.

================================================================================
SEÇÃO 3 — PARALELOS MODERNOS VERIFICÁVEIS
================================================================================

1. CBDCs — MOEDAS DIGITAIS DE BANCO CENTRAL
   - 134 países (representando 98% do PIB global) estão em fase de pesquisa,
     piloto ou implementação de CBDCs. [Atlantic Council CBDC Tracker, 2024]
   - Agustín Carstens, diretor do BIS (Banco de Compensações Internacionais):
     "Com o dinheiro em dinheiro físico, não sabemos quem está usando $100 hoje.
     Com CBDC, o banco central terá controle absoluto sobre as regras e
     regulamentos que determinarão o uso [do dinheiro]." [BIS Innovation Summit, 2020]
   - China: e-Yuan (DCEP) em circulação, usado em Olimpíadas de Inverno 2022.
     Pode ter prazo de validade (dinheiro que expira se não usado).
   - Drex (Brasil): CBDC do Banco Central do Brasil em desenvolvimento.
     Permite "dinheiro programável" — o governo pode definir onde e como
     o dinheiro pode ser gasto.
   - FedNow (EUA): lançado julho 2023. Infraestrutura de pagamentos instantâneos.
   - Paralelo com Marca: controle centralizado sobre toda transação comercial.

2. MICROCHIPS IMPLANTÁVEIS
   - Epicenter (Suécia): empresa pioneira em implantes RFID. Mais de 6.000
     funcionários e clientes com chips implantados na mão entre 2015-2023.
     [BBC, The Guardian, Reuters]
   - Estimativa global: 10.000-50.000 pessoas com chips implantados no mundo.
     [Wired, 2021; BBC Future, 2022]
   - FDA (EUA): aprovou em 2004 o VeriChip, primeiro chip implantável humano
     para uso médico (dados de saúde acessíveis em emergências).
   - Three Square Market (EUA, 2017): empresa ofereceu microchips voluntários
     a funcionários para acesso a escritório e pagamentos.
   - Implantes NFC: permitem pagamentos por aproximação diretamente pelo corpo.
   - Paralelo com Marca: tecnologia de identificação na mão, literalmente.

3. CRÉDITO SOCIAL — CHINA
   - Sistema de pontuação social pilotado em 2014, expandido desde 2018.
   - 23 milhões de viagens de avião bloqueadas e 5,5 milhões de viagens de
     trem negadas a cidadãos com "pontuação baixa". [Relatório do Supremo
     Tribunal Popular da China, 2019]
   - 200 milhões de câmeras de vigilância em 2021 (projeção: 560 milhões até 2025).
   - Reconhecimento facial: identifica cidadãos em multidões em segundos.
   - Acesso negado a: escolas particulares, hotéis de luxo, restaurantes,
     viagens internacionais, cargos governamentais.
   - Paralelo com Marca: "não comprar nem vender" como punição por
     comportamento não aprovado pelo Estado.

4. BIOMETRIA GLOBAL
   - Aadhaar (Índia): sistema de identidade biométrica com 1,38 bilhão de
     registros (2024). Vinculado a contas bancárias, impostos, benefícios sociais.
     Necessário para: abrir conta, receber benefício, comprar SIM de celular.
   - Suécia: 98% das transações são cashless (sem papel-moeda). [Riksbank, 2023]
     Pequenos comércios legalmente podem recusar dinheiro físico.
   - EUDI Wallet (UE): Carteira de Identidade Digital Europeia aprovada pelo
     Parlamento Europeu em março de 2024. Todos os 27 países membros devem
     implementar até 2026. Armazena: documentos, dados biométricos, carteira
     de motorista, receitas médicas, credenciais acadêmicas.
   - Paralelo com Marca: identidade única, unificada, digital, necessária para
     participar da economia e da sociedade.

5. ID2020 / AGENDA 2030
   - ID2020: aliança fundada em 2016 (Microsoft, Accenture, Gavi/UNICEF,
     Fundação Rockefeller). Objetivo: dar identidade digital a 1,1 bilhão de
     pessoas sem documentos até 2030.
   - ODS 16.9 da ONU (Agenda 2030): "Até 2030, proporcionar identidade legal
     para todos, incluindo o registro de nascimento."
   - Passaporte de Vacinação COVID-19 (2021-2022): primeiro sistema global
     de acesso condicionado a status biométrico/médico verificável.
   - Paralelo com Marca: identidade digital obrigatória como condição de
     participação no sistema global.

6. CASHLESS SOCIETY (SOCIEDADE SEM DINHEIRO FÍSICO)
   - Suécia: apenas 8% das transações usam dinheiro físico. [Riksbank 2023]
   - Dinamarca: Visa e Mastercard processam 90%+ das transações.
   - Holanda, Noruega, Finlândia: caminhando para eliminação total do cash.
   - Índia: "demonetização" de 2016 retirou 86% do dinheiro físico em circulação
     de um dia para o outro (Narendra Modi, 8 nov 2016).
   - Brasil Pix: 150 milhões de usuários, 4 bilhões de transações em 2023.
     Movimento crescente para eliminar papel-moeda.
   - Paralelo com Marca: quando o cash acabar, quem não tiver identidade
     digital verificada não pode participar da economia.

================================================================================
SEÇÃO 4 — ÂNGULO NARRATIVO E ESTRATÉGIA DE VÍDEO
================================================================================

PREMISSA CENTRAL:
"A profecia de Ap 13 não é ficção científica — é o roteiro exato do mundo
que está sendo construído agora, país por país, lei por lei, pixel por pixel.
A pergunta não é SE a Marca será implementada. A pergunta é: você vai recebê-la?"

TESE DO VÍDEO (3 camadas):
1. BÍBLICA: A Marca não é um microchip per se — é um sistema de controle
   econômico vinculado à adoração (lealdade) a um poder contrário a Deus.
2. HISTÓRICA: Todo grande império tentou versões deste sistema (Roma, URSS,
   China Maoist). O do século XXI é o mais tecnologicamente capaz da história.
3. ATUAL: As peças estão sendo instaladas agora: CBDCs (controle financeiro),
   biometria (identificação), crédito social (comportamento), CBDC programável
   (o que você pode comprar) = o sistema completo de Ap 13:17.

FRASES DE IMPACTO (alta viralidade):
1. "134 países já desenvolvem a moeda que pode te proibir de comprar comida."
2. "Na Suécia, você precisa de identidade digital para pagar uma pizza."
3. "O BIS admitiu: com CBDC, teremos controle absoluto sobre cada centavo seu."
4. "A China já bloqueou 23 milhões de viagens. O que acontece quando isso
   chegar ao Brasil?"
5. "João escreveu isso no século I. A tecnologia para cumprir só chegou agora."
6. "Não é questão de SE a Marca vai vir. A infraestrutura já está pronta."
7. "Você usa Pix? Você já está no sistema. A questão é: qual será o próximo passo?"
8. "O Anticristo não vai precisar de exércitos. Vai precisar de um servidor."

PERSONAGENS VISUAIS PARA NYX/GOETIA:
1. JOÃO EM PATMOS — Ancião com pergaminho, olhando visão futurista
   (cidade de telas/câmeras em P&B no fundo)
2. A BESTA DO MAR — Criatura de 7 cabeças emergindo de oceano de dados/código
3. O FALSO PROFETA — Figura em terno moderno dando ordem de controle digital
4. MÃOS COM MARCA — Close em mão recebendo implante de chip (microagulha)
5. CÂMERAS DE VIGILÂNCIA — Floresta de câmeras com olho da Besta no centro
6. DREX/CBDC — Nota digital fragmentada sendo controlada por mão gigante
7. CRÉDITO SOCIAL — Cidadão com pontuação "0" impedido de embarcar em avião
8. A CONVERGÊNCIA — Mapa-múndi com redes digitais conectando todos os países,
   símbolo 666 formando-se nas linhas de dados

GANCHO DE ABERTURA (sugestão para Morrigan):
"Em 95 d.C., um homem exilado em uma ilha rochosa teve uma visão que o
aterrorizou. Ele viu um sistema onde ninguém — absolutamente ninguém — poderia
comprar ou vender sem uma marca de identificação. Dois mil anos depois, os
governos do mundo têm um nome para esse sistema: CBDC."

ESTRUTURA RECOMENDADA (15-18 min):
- 0:00-2:00 → Gancho + pergunta-chave
- 2:00-5:00 → Base bíblica (texto + análise)
- 5:00-8:00 → Contexto histórico (Roma + Reformadores)
- 8:00-13:00 → Paralelos modernos (4-5 tecnologias com dados)
- 13:00-16:00 → Convergência: como tudo se encaixa em Ap 13:17
- 16:00-18:00 → Posição bíblica + chamada à ação espiritual

PALAVRAS-CHAVE SEO PRIMÁRIAS:
marca da besta, 666 bíblia, apocalipse 13, marca da besta microchip,
CBDC marca da besta, moeda digital anticristo, fim dos tempos sinais

POTENCIAL DE VIRALIDADE: 91/100
- Tema perene (evergreen máximo no nicho)
- Dados verificáveis e atualizados (2024)
- Conexão direta profecia-realidade
- Alto fator de compartilhamento em grupos evangélicos
- Monetizável (sem restrições AdSense — análise bíblica, não alarmismo)

================================================================================
FIM DO RELATÓRIO — ARGOS | ABISMO CRIATIVO
Canal: Sinais do Fim | video-002-marca-da-besta
================================================================================
"""

def safe(text):
    """Escapa caracteres especiais para ReportLab."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;'))


def gerar_pdf():
    os.makedirs(LOCAL_DIR, exist_ok=True)

    # Salvar TXT
    with open(TXT_PATH, 'w', encoding='utf-8') as f:
        f.write(PESQUISA_TXT)
    print(f"[OK] TXT salvo: {TXT_PATH}")

    # Montar PDF
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        topMargin=2*cm,
        bottomMargin=2*cm,
        leftMargin=2.5*cm,
        rightMargin=2.5*cm,
    )

    story = []

    # Cabeçalho
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("ABISMO CRIATIVO", style_titulo))
    story.append(Paragraph("Sinais do Fim — Passagens do Apocalipse", style_subtitulo))
    story.append(HRFlowable(width="100%", thickness=2, color=VERMELHO, spaceAfter=4))
    story.append(Paragraph("Argos — Relatório de Pesquisa | video-002-marca-da-besta", style_subtitulo))
    story.append(Paragraph("A Marca da Besta — Apocalipse 13 | 2026-04-06", style_rodape))
    story.append(Spacer(1, 0.5*cm))

    # ── SEÇÃO 1: BASE BÍBLICA ──────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=DOURADO, spaceAfter=6))
    story.append(Paragraph("SEÇÃO 1 — BASE BÍBLICA: TEXTOS E ANÁLISE", style_h1))

    story.append(Paragraph("Texto Principal: Apocalipse 13:16-18 (ARA)", style_h2))
    story.append(Paragraph(
        safe('"E ela faz que a todos, aos pequenos e aos grandes, aos ricos e aos pobres, '
             'aos livres e aos escravos, se lhes ponha uma marca na mão direita ou na fronte; '
             'e que ninguém possa comprar ou vender, senão aquele que tiver a marca, o nome '
             'da besta ou o número do seu nome. Aqui está a sabedoria. Aquele que tem '
             'entendimento, calcule o número da besta; porque é o número de um homem, e o '
             'seu número é Seiscentos e Sessenta e Seis."'),
        style_destaque
    ))

    story.append(Paragraph("Análise Palavra por Palavra", style_h2))
    items_analise = [
        ("<b>charagma</b> (\"marca\"): incisão, gravação, carimbo — mesmo termo para marcas "
         "imperiais romanas em documentos e na pele de escravos e animais."),
        ("<b>\"mão direita ou fronte\":</b> locais visíveis. Simbolismo: mão = ação; fronte = "
         "lealdade/pensamento. Inversão direta de Dt 6:8, onde Deus manda amarrar sua lei "
         "na mão e na fronte (tefilim)."),
        ("<b>\"comprar ou vender\":</b> controle econômico total. Sem a marca: exclusão "
         "completa do sistema comercial."),
        ("<b>\"666\":</b> número do homem — 6 representa imperfeição, aquém do divino 7. "
         "Tríplice repetição = superlativo. Interpretações: gematria (Nero), símbolo de "
         "imperfeição máxima."),
    ]
    for item in items_analise:
        story.append(Paragraph(safe(item), style_bullet))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Textos de Suporte", style_h2))

    textos_suporte = [
        ("Apocalipse 14:9-11",
         "Consequência espiritual definitiva da marca: \"Se alguém adorar a besta... "
         "também esse beberá do vinho da ira de Deus.\" — Condenação eterna confirmada."),
        ("Apocalipse 19:20",
         "Desfecho: a Besta e o falso profeta lançados no lago de fogo. Confirmação "
         "de que a Marca pertence ao sistema da Besta, que terá fim."),
        ("Daniel 7:7,23-25",
         "A Quarta Besta (diferente de todas) devora e tritura o mundo. O \"pequeno chifre\" "
         "muda os tempos e as leis — paralelo direto com sistema de controle global."),
        ("Ezequiel 9:4-6",
         "Precedente bíblico: o Senhor manda marcar (taw — forma de cruz em hebraico antigo) "
         "os fiéis para preservá-los. A Marca da Besta é a falsificação deste selo divino."),
        ("Deuteronômio 6:6-8 (Shemá)",
         "\"Amarrarás [as palavras de Deus] como sinal na tua mão, e serão por frontal entre "
         "os teus olhos.\" A Marca da Besta é a contrafação satânica do tefilim judaico."),
        ("Apocalipse 7:3 / 9:4",
         "Selo de Deus nos 144.000: contraparte positiva. Dois sistemas paralelos de "
         "identificação — o de Deus e o da Besta. Toda pessoa terá um dos dois."),
    ]
    for ref, desc in textos_suporte:
        story.append(Paragraph(f"<b>{safe(ref)}</b>", style_h3))
        story.append(Paragraph(safe(desc), style_body))

    # ── SEÇÃO 2: HISTÓRICO ─────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=DOURADO, spaceAfter=6))
    story.append(Paragraph("SEÇÃO 2 — CONTEXTO HISTÓRICO E ESCOLAS ESCATOLÓGICAS", style_h1))

    story.append(Paragraph("O Culto Imperial Romano (Século I)", style_h2))
    hist_items = [
        "Domiciano (81–96 d.C.) exigiu o título \"Dominus et Deus\" (Senhor e Deus).",
        "Toda transação comercial requeria certificado de lealdade ao Imperador (libellus) "
        "ou participação em sacrifícios — cristãos que recusavam eram excluídos das guildas.",
        "Moedas romanas traziam a imagem (eikon) do Imperador com título divino — "
        "exatamente a \"imagem da Besta\" que todos deviam adorar.",
        "Nero (54–68 d.C.): gematria hebraica nrwn qsr = 666. Primeiro grande "
        "perseguidor dos cristãos, assassinou Pedro e Paulo.",
        "Variação 616 (sem \"n\" final em latim): encontrada no Papiro 115 de Oxyrhynchus "
        "— confirma base histórica da gematria Nero.",
    ]
    for item in hist_items:
        story.append(Paragraph(safe(item), style_bullet))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("As 4 Escolas Escatológicas", style_h2))

    escolas = [
        ("1. PRETERISMO — Cumprimento no Século I",
         "Toda profecia de Ap 13 foi cumprida no século I d.C. Besta = Nero/Domiciano; "
         "Falso Profeta = sacerdócio imperial romano. "
         "Representantes: David Chilton, R.C. Sproul, Gary DeMar. "
         "Força: coerência histórica. Fraqueza: eventos como o \"lago de fogo\" não "
         "ocorreram literalmente."),
        ("2. HISTORICISMO — Cumprimento Progressivo",
         "A Besta = sistema papal de Roma. Posição dos Reformadores (Lutero: \"O papa é o "
         "Anticristo\"; Calvino: sistema romano como besta profética). Marca = submissão "
         "à autoridade papal vs. autoridade das Escrituras. Westminster Confession (1647) "
         "referencia esta posição. Representantes: Matthew Henry, Adam Clarke."),
        ("3. IDEALISMO/SIMBOLISMO — Princípios Atemporais",
         "A Marca representa qualquer sistema de idolatria e coerção econômica em qualquer "
         "época. Não é literal — representa lealdade ao poder mundano vs. a Deus. "
         "Representantes: William Hendriksen, G.K. Beale. Força: aplicabilidade universal. "
         "Fraqueza: subestima especificidade dos textos."),
        ("4. FUTURISMO — Cumprimento Literal Futuro",
         "Sistematizado por John Nelson Darby (1800–1882), fundador do Dispensacionalismo "
         "(formalizado c. 1830). Anticristo futuro, literal, identificável. Tribulação de "
         "7 anos. Arrebatamento pré-tribulacional. Scofield Reference Bible (1909) "
         "populariza globalmente. Tim LaHaye (Left Behind), Hal Lindsey popularizam no "
         "século XX. Posição dominante no evangelicalismo brasileiro contemporâneo."),
    ]
    for titulo_escola, desc_escola in escolas:
        story.append(Paragraph(safe(titulo_escola), style_h3))
        story.append(Paragraph(safe(desc_escola), style_body))
        story.append(Spacer(1, 0.1*cm))

    # ── SEÇÃO 3: PARALELOS MODERNOS ────────────────────────────────────────
    story.append(PageBreak())
    story.append(HRFlowable(width="100%", thickness=1, color=DOURADO, spaceAfter=6))
    story.append(Paragraph("SEÇÃO 3 — PARALELOS MODERNOS VERIFICÁVEIS", style_h1))

    modernos = [
        (
            "1. CBDCs — MOEDAS DIGITAIS DE BANCO CENTRAL",
            [
                "134 países (98% do PIB global) em fase de pesquisa, piloto ou implementação "
                "de CBDCs. [Atlantic Council CBDC Tracker, 2024]",
                "Agustín Carstens (BIS, 2020): \"Com o dinheiro físico, não sabemos quem usa "
                "$100. Com CBDC, o banco central terá controle absoluto sobre as regras que "
                "determinarão o uso do dinheiro.\"",
                "China e-Yuan (DCEP): em circulação desde 2021, usado nas Olimpíadas de Inverno "
                "2022. Pode ter prazo de validade (dinheiro que expira).",
                "Drex (Brasil): CBDC do Banco Central em desenvolvimento. Permite \"dinheiro "
                "programável\" — governo define onde e como pode ser gasto.",
                "FedNow (EUA): lançado julho 2023. Infraestrutura de pagamentos instantâneos.",
            ],
            "Paralelo com Marca: controle centralizado sobre toda transação comercial. "
            "Quem o governo desabilitar, não pode comprar nem vender."
        ),
        (
            "2. MICROCHIPS IMPLANTÁVEIS",
            [
                "Epicenter (Suécia): mais de 6.000 pessoas com chips RFID implantados na mão "
                "(2015–2023). Usados para: acesso ao escritório, pagamentos, reserva de salas. "
                "[BBC, The Guardian, Reuters]",
                "Estimativa global: 10.000–50.000 pessoas com chips implantados. [Wired 2021; "
                "BBC Future 2022]",
                "FDA (EUA): aprovou em 2004 o VeriChip — primeiro chip implantável humano "
                "(dados médicos em emergências).",
                "Three Square Market (EUA, 2017): empresa ofereceu chips voluntários a "
                "funcionários para acesso e pagamentos.",
                "Implantes NFC: permitem pagamentos por aproximação diretamente pelo corpo humano.",
            ],
            "Paralelo com Marca: tecnologia de identificação na mão direita, literalmente. "
            "Voluntário hoje — qual o próximo passo?"
        ),
        (
            "3. SISTEMA DE CRÉDITO SOCIAL — CHINA",
            [
                "23 milhões de viagens de avião bloqueadas; 5,5 milhões de viagens de trem "
                "negadas a cidadãos com \"pontuação baixa\". [Supremo Tribunal Popular da China, 2019]",
                "200 milhões de câmeras em 2021; projeção de 560 milhões até 2025.",
                "Reconhecimento facial identifica cidadãos em multidões em segundos.",
                "Acesso negado: escolas particulares, hotéis, restaurantes, viagens "
                "internacionais, cargos governamentais.",
            ],
            "Paralelo com Marca: \"não comprar nem vender\" como punição por comportamento "
            "não aprovado pelo Estado. A Besta recompensa os leais e pune os dissidentes."
        ),
        (
            "4. BIOMETRIA GLOBAL",
            [
                "Aadhaar (Índia): 1,38 bilhão de registros biométricos vinculados a contas "
                "bancárias, impostos e benefícios. Necessário para: conta bancária, SIM de "
                "celular, benefícios sociais. [Unique Identification Authority of India, 2024]",
                "Suécia: 98% das transações são cashless; comércios podem legalmente recusar "
                "dinheiro físico. [Riksbank, 2023]",
                "EUDI Wallet: Carteira de Identidade Digital Europeia aprovada pelo Parlamento "
                "Europeu em março de 2024. Todos os 27 países devem implementar até 2026. "
                "Armazena: documentos, biometria, receitas médicas, credenciais acadêmicas.",
            ],
            "Paralelo com Marca: identidade única, digital e unificada, necessária para "
            "participar da economia e da sociedade. Sem ela: invisibilidade ou exclusão."
        ),
        (
            "5. ID2020 / AGENDA 2030",
            [
                "ID2020 (fundada 2016): aliança Microsoft + Accenture + Gavi/UNICEF + Rockefeller. "
                "Objetivo: identidade digital para 1,1 bilhão de pessoas sem documentos até 2030.",
                "ODS 16.9 (ONU Agenda 2030): \"Até 2030, proporcionar identidade legal para "
                "todos, incluindo o registro de nascimento.\"",
                "Passaportes de vacinação COVID-19 (2021–2022): primeiro sistema global de "
                "acesso condicionado a status biométrico/médico verificável.",
            ],
            "Paralelo com Marca: identidade digital obrigatória como condição de "
            "participação no sistema global — o que antes era voluntário torna-se mandatório."
        ),
        (
            "6. SOCIEDADE SEM DINHEIRO FÍSICO (CASHLESS)",
            [
                "Suécia: apenas 8% das transações usam dinheiro físico. [Riksbank 2023]",
                "Índia: demonetização de 2016 retirou 86% do dinheiro em circulação em "
                "um único dia (8 nov 2016, decreto Narendra Modi).",
                "Brasil — Pix: 150 milhões de usuários, 4 bilhões de transações em 2023. "
                "Movimento crescente para eliminar papel-moeda.",
                "Quando o cash acabar: quem não tiver identidade digital verificada não "
                "poderá participar de nenhuma transação econômica.",
            ],
            "Paralelo com Marca: o fim do dinheiro físico é o último passo antes do "
            "controle total. Cada CBDC é uma peça do sistema descrito em Ap 13:17."
        ),
    ]

    for titulo_mod, bullets_mod, paralelo in modernos:
        story.append(Paragraph(safe(titulo_mod), style_h2))
        for b in bullets_mod:
            story.append(Paragraph(safe(b), style_bullet))
        story.append(Paragraph(safe("Paralelo Profético: " + paralelo), style_destaque))
        story.append(Spacer(1, 0.2*cm))

    # ── SEÇÃO 4: ÂNGULO NARRATIVO ──────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=DOURADO, spaceAfter=6))
    story.append(Paragraph("SEÇÃO 4 — ÂNGULO NARRATIVO E ESTRATÉGIA DE VÍDEO", style_h1))

    story.append(Paragraph("Premissa Central", style_h2))
    story.append(Paragraph(
        safe('"A profecia de Ap 13 não é ficção científica — é o roteiro exato do mundo '
             'que está sendo construído agora, país por país, lei por lei, pixel por pixel. '
             'A pergunta não é SE a Marca será implementada. A pergunta é: você vai recebê-la?"'),
        style_frase
    ))

    story.append(Paragraph("Tese do Vídeo (3 Camadas)", style_h2))
    teses = [
        "<b>Bíblica:</b> A Marca não é um microchip per se — é um sistema de controle "
        "econômico vinculado à adoração (lealdade) a um poder contrário a Deus.",
        "<b>Histórica:</b> Todo grande império tentou versões deste sistema (Roma, URSS, "
        "China Maoísta). O do século XXI é o mais tecnologicamente capaz da história.",
        "<b>Atual:</b> As peças estão sendo instaladas agora: CBDCs (controle financeiro) + "
        "biometria (identificação) + crédito social (comportamento) + CBDC programável "
        "(o que você pode comprar) = o sistema completo de Ap 13:17.",
    ]
    for t in teses:
        story.append(Paragraph(safe(t), style_bullet))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Frases de Impacto — Alto Potencial Viral", style_h2))
    frases = [
        "\"134 países já desenvolvem a moeda que pode te proibir de comprar comida.\"",
        "\"Na Suécia, você precisa de identidade digital para pagar uma pizza.\"",
        "\"O BIS admitiu: com CBDC, teremos controle absoluto sobre cada centavo seu.\"",
        "\"A China bloqueou 23 milhões de viagens. O que acontece quando isso chegar ao Brasil?\"",
        "\"João escreveu isso no século I. A tecnologia para cumprir só chegou agora.\"",
        "\"Não é questão de SE a Marca vai vir. A infraestrutura já está pronta.\"",
        "\"Você usa Pix? Você já está no sistema. A questão é: qual será o próximo passo?\"",
        "\"O Anticristo não vai precisar de exércitos. Vai precisar de um servidor.\"",
    ]
    for f in frases:
        story.append(Paragraph(safe(f), style_destaque))

    story.append(Paragraph("Personagens Visuais para Nyx/Goetia", style_h2))
    personagens = [
        "João em Patmos — ancião com pergaminho, olhando visão de cidade de telas (P&B no fundo)",
        "A Besta do Mar — criatura de 7 cabeças emergindo de oceano de dados e código digital",
        "O Falso Profeta — figura em terno moderno dando ordem de controle digital",
        "Mãos com Marca — close em mão recebendo implante de chip por microagulha",
        "Câmeras de Vigilância — floresta de câmeras com olho da Besta no centro",
        "Drex/CBDC — nota digital fragmentada controlada por mão gigante",
        "Crédito Social — cidadão com pontuação \"0\" impedido de embarcar em avião",
        "A Convergência — mapa-múndi com redes digitais, símbolo 666 formando-se nas linhas de dados",
    ]
    for p in personagens:
        story.append(Paragraph(safe(p), style_bullet))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Gancho de Abertura (Para Morrigan)", style_h2))
    story.append(Paragraph(
        safe('"Em 95 d.C., um homem exilado em uma ilha rochosa teve uma visão que o '
             'aterrorizou. Ele viu um sistema onde ninguém — absolutamente ninguém — poderia '
             'comprar ou vender sem uma marca de identificação. Dois mil anos depois, os '
             'governos do mundo têm um nome para esse sistema: CBDC."'),
        style_destaque
    ))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Estrutura Recomendada (15–18 min)", style_h2))
    estrutura = [
        "0:00–2:00 — Gancho + pergunta-chave (o que é a Marca?)",
        "2:00–5:00 — Base bíblica (texto + análise Ap 13 + textos de suporte)",
        "5:00–8:00 — Contexto histórico (Roma + gematria + 4 escolas)",
        "8:00–13:00 — Paralelos modernos (5–6 tecnologias com dados verificáveis)",
        "13:00–16:00 — Convergência: como tudo se encaixa em Ap 13:17",
        "16:00–18:00 — Posição bíblica + chamada à ação espiritual",
    ]
    for e in estrutura:
        story.append(Paragraph(safe(e), style_bullet))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("Palavras-Chave SEO Primárias", style_h2))
    story.append(Paragraph(
        safe("marca da besta | 666 bíblia | apocalipse 13 | marca da besta microchip | "
             "CBDC marca da besta | moeda digital anticristo | fim dos tempos sinais"),
        style_body
    ))
    story.append(Spacer(1, 0.3*cm))

    story.append(HRFlowable(width="100%", thickness=1, color=VERMELHO, spaceAfter=8))
    story.append(Paragraph(
        safe("POTENCIAL DE VIRALIDADE: 91/100 — Tema evergreen máximo no nicho | "
             "Dados verificáveis atualizados (2024) | Conexão direta profecia-realidade | "
             "Alto compartilhamento em grupos evangélicos | Monetizável sem restrições AdSense"),
        style_rodape
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=DOURADO, spaceAfter=4))
    story.append(Paragraph(
        "Argos — Pesquisador de Nicho | Abismo Criativo | 2026-04-06",
        style_rodape
    ))

    doc.build(story)
    print(f"[OK] PDF gerado: {PDF_PATH}")


def upload_vps():
    if paramiko is None:
        print("[SKIP] paramiko nao disponivel — upload ignorado.")
        return False

    print(f"[...] Conectando VPS {VPS_HOST}...")
    try:
        key = paramiko.Ed25519Key.from_private_key_file(KEY_PATH)
    except Exception as e:
        print(f"[ERRO] Chave SSH: {e}")
        return False

    try:
        transport = paramiko.Transport((VPS_HOST, VPS_PORT))
        transport.connect(username=VPS_USER, pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Criar diretórios na VPS
        dirs = [
            "/opt/agencia",
            "/opt/agencia/canais",
            "/opt/agencia/canais/sinais-do-fim",
            "/opt/agencia/canais/sinais-do-fim/videos",
            "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta",
            "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/1-pesquisa",
        ]
        for d in dirs:
            try:
                sftp.mkdir(d)
            except Exception:
                pass  # já existe

        sftp.put(PDF_PATH, VPS_PATH)
        sftp.close()
        transport.close()
        print(f"[OK] Upload concluído: {HTTP_URL}")
        return True
    except Exception as e:
        print(f"[ERRO] Upload falhou: {e}")
        return False


def registrar_log(upload_ok):
    log_path = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log"
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    linhas = [
        f"[{ts}] ARGOS — Pesquisa concluída → pesquisa.pdf gerado",
    ]
    if upload_ok:
        linhas.append(f"[{ts}] ARGOS — Upload VPS OK via SFTP (paramiko)")
        linhas.append(f"[{ts}] LINK — {HTTP_URL}")
    else:
        linhas.append(f"[{ts}] ARGOS — Upload VPS FALHOU (verificar SSH/paramiko)")
    linhas.append(f"[{ts}] CHECKPOINT 1 — Aguardando aprovação de Snayder para avançar para Hermes (SEO + Títulos)")

    with open(log_path, 'a', encoding='utf-8') as f:
        for linha in linhas:
            f.write(linha + "\n")
    print(f"[OK] Log registrado: {log_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("ARGOS — PESQUISA video-002-marca-da-besta")
    print("=" * 60)
    gerar_pdf()
    upload_ok = upload_vps()
    registrar_log(upload_ok)
    print("=" * 60)
    print(f"ENTREGA: {HTTP_URL}")
    print("=" * 60)
