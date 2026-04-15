"""
ORFEU — Gerador de PDF de Narracoes para Suno
video-002-marca-da-besta | Abismo Criativo
"""

import os
import paramiko
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)

# ── Cores da agência ─────────────────────────────────────────────────────────
PRETO   = HexColor("#0A0A0A")
VERMELHO = HexColor("#8B0000")
DOURADO = HexColor("#C5A355")
CINZA   = HexColor("#1A1A1A")

# ── Estilos ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    'AgTitle',
    parent=styles['Title'],
    fontSize=24,
    textColor=VERMELHO,
    fontName='Helvetica-Bold',
    spaceAfter=4,
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
style_agencia = ParagraphStyle(
    'AgAgencia',
    parent=styles['Normal'],
    fontSize=9,
    textColor=DOURADO,
    fontName='Helvetica',
    spaceAfter=16,
    alignment=1,
)
style_h1 = ParagraphStyle(
    'AgH1',
    parent=styles['Heading1'],
    fontSize=14,
    textColor=VERMELHO,
    fontName='Helvetica-Bold',
    spaceBefore=18,
    spaceAfter=6,
)
style_h2 = ParagraphStyle(
    'AgH2',
    parent=styles['Heading2'],
    fontSize=11,
    textColor=DOURADO,
    fontName='Helvetica-Bold',
    spaceBefore=10,
    spaceAfter=4,
)
style_body = ParagraphStyle(
    'AgBody',
    parent=styles['Normal'],
    fontSize=10,
    textColor=PRETO,
    leading=15,
    spaceAfter=6,
    fontName='Helvetica',
)
style_narracao = ParagraphStyle(
    'AgNarr',
    parent=styles['Normal'],
    fontSize=10,
    textColor=PRETO,
    leading=16,
    spaceAfter=4,
    fontName='Helvetica',
    leftIndent=10,
    rightIndent=10,
)
style_meta = ParagraphStyle(
    'AgMeta',
    parent=styles['Normal'],
    fontSize=8,
    textColor=DOURADO,
    fontName='Helvetica-Bold',
    spaceAfter=6,
)
style_suno = ParagraphStyle(
    'AgSuno',
    parent=styles['Normal'],
    fontSize=9,
    textColor=PRETO,
    leading=14,
    spaceAfter=4,
    fontName='Helvetica-Oblique',
    leftIndent=10,
    rightIndent=10,
    backColor=HexColor("#F5F0E8"),
    borderPadding=8,
)
style_footer = ParagraphStyle(
    'AgFooter',
    parent=styles['Normal'],
    fontSize=8,
    textColor=DOURADO,
    fontName='Helvetica',
    alignment=1,
)

# ── Caminhos ──────────────────────────────────────────────────────────────────
LOCAL_DIR  = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\5-prompts"
PDF_PATH   = os.path.join(LOCAL_DIR, "suno_narracoes.pdf")
LOG_PATH   = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log"
VPS_HOST   = "31.97.165.64"
VPS_USER   = "root"
KEY_PATH   = os.path.expanduser("~/.ssh/id_ed25519")
VPS_REMOTE = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/suno_narracoes.pdf"
VPS_URL    = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/suno_narracoes.pdf"

# ── Partes da narração ────────────────────────────────────────────────────────
PARTES = [
    {
        "num": 1,
        "chars": 1247,
        "texto": (
            "No ano noventa e cinco depois de Cristo, um homem exilado em uma ilha rochosa teve uma visão.\n\n"
            "Ele não era jovem.\n"
            "Ele não era poderoso.\n"
            "Era um ancião solitário, sem exército, sem poder político.\n\n"
            "E ele viu algo que o aterrorizou.\n\n"
            "Viu um sistema.\n"
            "Um sistema onde ninguém — absolutamente ninguém — poderia comprar ou vender... sem uma marca de identificação.\n\n"
            '"João escreveu isso no século I. A tecnologia para cumprir só chegou agora."\n\n'
            "Hoje, os governos do mundo têm um nome para esse sistema.\n"
            "Chamam de C-B-D-C.\n"
            "Moeda Digital de Banco Central.\n\n"
            "Cento e trinta e quatro países estão construindo esse sistema agora.\n"
            "Representam noventa e oito por cento do P-I-B do planeta.\n\n"
            '"Cento e trinta e quatro países já desenvolvem a moeda que pode te proibir de comprar comida."\n\n'
            "Neste vídeo, vamos olhar para o que João realmente escreveu.\n"
            "Vamos olhar para o que está acontecendo hoje.\n"
            "E vamos deixar você tirar suas próprias conclusões.\n\n"
            "Não vamos afirmar que o fim é amanhã.\n"
            "Vamos mostrar que as peças estão no tabuleiro."
        ),
    },
    {
        "num": 2,
        "chars": 1598,
        "texto": (
            "Apocalipse, capítulo treze, versículos dezesseis a dezoito.\n\n"
            "Leitura na Almeida Revista e Atualizada:\n\n"
            '"E ela faz que a todos, aos pequenos e aos grandes, aos ricos e aos pobres, aos livres e aos escravos, se lhes ponha uma marca na mão direita ou na fronte."\n\n'
            '"E que ninguém possa comprar ou vender, senão aquele que tiver a marca, o nome da besta, ou o número do seu nome."\n\n'
            '"Aqui está a sabedoria. Aquele que tem entendimento, calcule o número da besta. Porque é o número de um homem. E o seu número é seiscentos e sessenta e seis."\n\n'
            "João não usou uma palavra qualquer para \"marca.\"\n"
            "Ele usou a palavra grega \"charagma.\"\n\n"
            "Charagma significava: incisão, gravação, carimbo.\n"
            "Era o mesmo termo usado para marcas imperiais romanas.\n"
            "Marcas em documentos oficiais.\n"
            "Marcas na pele de escravos.\n"
            "Marcas em animais de propriedade do Império.\n\n"
            "A localização não é acidental.\n\n"
            "No livro de Deuteronômio, capítulo seis, versículo oito, Deus manda o povo de Israel amarrar Sua lei como sinal na mão. E como frontal entre os olhos.\n\n"
            "Os judeus chamam esses objetos de tefilim.\n"
            "São caixinhas com pergaminhos das Escrituras, usadas na mão direita e na testa durante a oração.\n\n"
            "A Marca da Besta não é uma invenção aleatória.\n"
            "É a contrafação exata do sinal de Deus."
        ),
    },
    {
        "num": 3,
        "chars": 1421,
        "texto": (
            "A frase mais importante do texto é esta:\n"
            '"Ninguém possa comprar ou vender."\n\n'
            "Não é uma ameaça de violência física.\n"
            "É uma exclusão econômica.\n"
            "Quem não tiver a marca... não come.\n"
            "Não paga aluguel.\n"
            "Não recebe salário.\n"
            "Não existe dentro do sistema.\n\n"
            '"O Anticristo não vai precisar de exércitos. Vai precisar de um servidor."\n\n'
            "Há quatro maneiras principais de interpretar Apocalipse treze.\n\n"
            "O preterismo diz que tudo se cumpriu no século I.\n"
            "A Besta seria Nero ou Domiciano.\n\n"
            "O historicismo foi a posição dos Reformadores.\n"
            "Lutero e Calvino viam o papado romano como o sistema da Besta.\n\n"
            "O idealismo vê símbolos atemporais.\n"
            "Qualquer sistema de coerção e idolatria em qualquer época.\n\n"
            "O futurismo espera um cumprimento literal ainda no futuro.\n"
            "Foi sistematizado em mil oitocentos e trinta por John Nelson Darby.\n"
            "É a posição dominante no evangelicalismo brasileiro hoje.\n\n"
            "Neste canal, trabalhamos com o futurismo como lente principal.\n"
            "Sem descartar os outros ângulos."
        ),
    },
    {
        "num": 4,
        "chars": 1487,
        "texto": (
            "Para entender o que João descreveu... precisamos entender o mundo onde ele vivia.\n\n"
            "O imperador Domiciano governou Roma de oitenta e um a noventa e seis depois de Cristo.\n"
            "Ele exigiu ser tratado como \"Dominus et Deus.\"\n"
            "Senhor e Deus.\n\n"
            "Toda transação comercial na Roma imperial requeria participação nos sacrifícios ao Imperador.\n"
            "Ou um documento chamado libellus — um certificado de lealdade ao poder romano.\n\n"
            "Cristãos que recusavam esse sistema... eram expulsos das guildas comerciais.\n"
            "Perdiam acesso a trabalho.\n"
            "Perdiam acesso ao mercado.\n"
            "Literalmente, não podiam comprar nem vender.\n\n"
            "Isso é o que João estava descrevendo para sua geração.\n"
            "E projetando para o futuro.\n\n"
            "O número seiscentos e sessenta e seis tem uma história.\n\n"
            "Na tradição judaica, cada letra tem um valor numérico.\n"
            "É a prática chamada de gematria.\n\n"
            "Nero César, escrito em hebraico como \"nrwn qsr\", soma exatamente seiscentos e sessenta e seis.\n"
            "Nun, Resh, Waw, Nun: cinquenta, duzentos, seis, cinquenta.\n"
            "Qoph, Samekh, Resh: cem, sessenta, duzentos.\n"
            "Total: seiscentos e sessenta e seis.\n\n"
            "Há manuscritos antigos, como o Papiro cento e quinze de Oxyrhynchus, que trazem o número como seiscentos e dezesseis — a variação latina do nome de Nero, sem o \"n\" final.\n\n"
            "Os preteristas usam isso para dizer que o texto se encerrou no século I.\n"
            "Os futuristas respondem: Nero foi o padrão.\n"
            "O cumprimento final ainda está por vir."
        ),
    },
    {
        "num": 5,
        "chars": 1473,
        "texto": (
            "Quando Martinho Lutero pregou contra Roma em mil quinhentos e dezessete... ele não estava apenas falando de doutrina.\n\n"
            "Lutero afirmou publicamente: o papa é o Anticristo.\n"
            "Calvino concordava.\n"
            "A Confissão de Westminster de mil seiscentos e quarenta e sete registra esta posição.\n\n"
            "A Marca, para eles, era a submissão à autoridade papal em vez da autoridade das Escrituras.\n\n"
            "Isso mostra que cada geração viu em seu tempo a estrutura que o texto descreve.\n"
            "Cada geração estava parcialmente certa.\n"
            "E cada geração apontava para algo maior.\n\n"
            "Voltemos ao presente.\n\n"
            "Em outubro de dois mil e vinte, Agustín Carstens falou.\n"
            "Ele é o diretor-geral do B-I-S — o Banco de Compensações Internacionais.\n"
            "O banco dos bancos centrais do mundo.\n\n"
            "Ele disse, com todas as letras, no B-I-S Innovation Summit:\n\n"
            '"Com o dinheiro físico, não sabemos quem está usando cem dólares hoje. Com C-B-D-C, o banco central terá controle absoluto sobre as regras que determinarão o uso do dinheiro."\n\n'
            '"O B-I-S admitiu: com C-B-D-C, teremos controle absoluto sobre cada centavo seu."\n\n'
            "Controle absoluto.\n"
            "Palavras do homem que supervisiona os bancos centrais do planeta."
        ),
    },
    {
        "num": 6,
        "chars": 1692,
        "texto": (
            "O Atlantic Council mantém um rastreador público de C-B-D-Cs.\n"
            "Em dois mil e vinte e quatro, o número é este: cento e trinta e quatro países.\n"
            "Noventa e oito por cento do P-I-B global.\n\n"
            "A China já lançou o e-Yuan — o yuan digital.\n"
            "Foi testado nas Olimpíadas de Inverno de dois mil e vinte e dois.\n"
            "O e-Yuan pode ter prazo de validade.\n"
            "Dinheiro que expira se você não gastar quando o governo quer.\n\n"
            "O Brasil tem o Drex.\n"
            "É a C-B-D-C do Banco Central do Brasil.\n"
            "Permite \"dinheiro programável.\"\n"
            "O governo pode definir onde e como o dinheiro pode ser gasto.\n\n"
            '"Você usa Pix? Você já está no sistema. A questão é: qual será o próximo passo?"\n\n'
            "Os Estados Unidos lançaram o FedNow em julho de dois mil e vinte e três.\n"
            "É a infraestrutura de pagamentos instantâneos.\n"
            "O primeiro bloco do sistema.\n\n"
            "Agora leia novamente o versículo dezessete de Apocalipse treze.\n"
            '"Ninguém possa comprar ou vender senão aquele que tiver a marca."\n\n'
            "A tecnologia para isso não existia em mil novecentos e noventa.\n"
            "Em dois mil e vinte e quatro, está em piloto em dezenas de países.\n\n"
            "Em dois mil e quinze, uma empresa sueca chamada Epicenter começou a implantar chips R-F-I-D nas mãos de funcionários.\n"
            "Voluntariamente.\n"
            "Com festa e celebração.\n\n"
            "Até dois mil e vinte e três, mais de seis mil pessoas tinham chips implantados na mão.\n"
            "O chip abre portas.\n"
            "Paga contas.\n"
            "Guarda informações médicas.\n"
            "Identifica o portador em segundos."
        ),
    },
    {
        "num": 7,
        "chars": 1679,
        "texto": (
            "Em dois mil e quatro, o F-D-A dos Estados Unidos aprovou o VeriChip — o primeiro chip implantável humano para uso médico.\n\n"
            "Em dois mil e dezessete, uma empresa americana chamada Three Square Market ofereceu chips voluntários a seus funcionários.\n"
            "Para acessar o escritório.\n"
            "Para fazer pagamentos na cantina.\n"
            "Na mão direita.\n\n"
            "Chips N-F-C implantados já permitem pagamentos por aproximação.\n"
            "Diretamente pelo corpo.\n"
            "Sem cartão.\n"
            "Sem celular.\n"
            "Apenas a mão.\n\n"
            '"A tecnologia já funciona. O debate agora é sobre escala."\n\n'
            "Não estamos falando de ficção científica.\n"
            "Estamos falando de produto comercial disponível hoje.\n\n"
            "A China começou a testar seu sistema de crédito social em dois mil e catorze.\n"
            "Expandiu em dois mil e dezoito.\n\n"
            "Os números do Supremo Tribunal Popular da China, de dois mil e dezenove: vinte e três milhões de viagens de avião bloqueadas.\n"
            "Cinco milhões e meio de viagens de trem negadas.\n"
            "Tudo por \"pontuação baixa\" no sistema estatal.\n\n"
            "Não é crime.\n"
            "É comportamento não aprovado pelo Estado.\n\n"
            '"A China já bloqueou vinte e três milhões de viagens. O que acontece quando isso chegar ao Brasil?"\n\n'
            "Em dois mil e vinte e um, havia duzentos milhões de câmeras de vigilância na China.\n"
            "A projeção para dois mil e vinte e cinco: quinhentos e sessenta milhões de câmeras.\n"
            "O reconhecimento facial identifica cidadãos em multidões em segundos.\n\n"
            "Acesso negado a quem tem pontuação baixa: escolas particulares, hotéis, restaurantes, viagens internacionais, cargos no governo.\n\n"
            "Compare com Apocalipse treze, versículo dezessete.\n"
            "Palavra por palavra."
        ),
    },
    {
        "num": 8,
        "chars": 1751,
        "texto": (
            "A Índia construiu o maior sistema de identidade biométrica do mundo.\n"
            "Chama-se Aadhaar.\n\n"
            "Em dois mil e vinte e quatro, são um bilhão trezentos e oitenta milhões de registros.\n"
            "Cada registro vinculado a: impressão digital, retina, rosto.\n"
            "E a: conta bancária, declaração de impostos, benefícios sociais.\n\n"
            "Para abrir uma conta no banco na Índia: você precisa do Aadhaar.\n"
            "Para receber benefício do governo: Aadhaar.\n"
            "Para comprar um chip de celular: Aadhaar.\n\n"
            "Sem identidade digital: você não existe para o sistema.\n\n"
            "Em março de dois mil e vinte e quatro, o Parlamento Europeu aprovou a E-U-D-I Wallet.\n"
            "Carteira de Identidade Digital Europeia.\n\n"
            "Todos os vinte e sete países membros da União Europeia devem implementar até dois mil e vinte e seis.\n\n"
            "O que a E-U-D-I Wallet armazena: documentos de identidade, dados biométricos, carteira de motorista, receitas médicas, credenciais acadêmicas.\n"
            "Tudo em um único perfil digital vinculado ao indivíduo.\n\n"
            "Em dois mil e dezesseis, uma aliança foi fundada.\n"
            "Chama-se ID dois mil e vinte.\n\n"
            "Os fundadores: Microsoft, Accenture, Fundação Rockefeller, U-N-I-C-E-F e Gavi — a aliança global de vacinas.\n\n"
            "O objetivo declarado: dar identidade digital verificável a um bilhão e cem milhões de pessoas sem documentos até dois mil e trinta.\n\n"
            "A O-N-U incluiu identidade digital para todos como meta dezesseis ponto nove da Agenda dois mil e trinta.\n\n"
            "Aqui está o que torna este momento diferente de todos os anteriores.\n\n"
            "Cinco tecnologias convergindo ao mesmo tempo: C-B-D-Cs — controle sobre toda transação financeira. Biometria — identificação única e inegável do indivíduo. Crédito social — acesso condicionado ao comportamento aprovado. Dinheiro programável — controle sobre o que você pode comprar. Identidade digital obrigatória — condição para participar da economia."
        ),
    },
    {
        "num": 9,
        "chars": 1499,
        "texto": (
            "Cada uma dessas tecnologias existe.\n"
            "Cada uma está em expansão agora.\n"
            "Nenhuma sozinha é a Marca.\n"
            "Mas juntas... formam exatamente o sistema descrito em Apocalipse treze, versículo dezessete.\n\n"
            '"Não é questão de SE a Marca vai vir. A infraestrutura já está pronta."\n\n'
            "A Suécia é o exemplo mais avançado.\n"
            "Noventa e oito por cento das transações são sem dinheiro físico.\n"
            "Pequenos comércios podem legalmente recusar cédulas.\n\n"
            "Não afirmamos que o Anticristo já chegou.\n"
            "Não afirmamos que a Marca está sendo implantada hoje.\n\n"
            "O que podemos dizer com certeza: as peças estão sendo colocadas no tabuleiro.\n"
            "Lentamente. Metodicamente. País por país. Lei por lei.\n\n"
            "João pode ter sido o homem mais improvável do mundo para descrever um sistema de pagamentos digitais.\n"
            "Mas a estrutura que ele descreveu... é a estrutura que está sendo construída.\n\n"
            '"A profecia não é sobre o futuro distante. É sobre o mundo que você usa todo dia."\n\n'
            "Aqui está a pergunta que fica: se este sistema for implementado na sua cidade, no seu país — se um dia exigirem uma marca para comprar, para vender, para existir dentro da economia — o que você fará?\n\n"
            "A Bíblia não deixa dúvida sobre as consequências de receber a Marca.\n"
            "Apocalipse quatorze, versículo nove, fala da ira de Deus sobre quem a aceitar.\n"
            "Essa é uma decisão que cada pessoa fará sozinha.\n\n"
            '"Quando chegar o momento, não haverá tempo para pesquisar. Você já precisa saber."\n\n'
            "Se este conteúdo te fez pensar... se a conexão que você acabou de ver merece mais atenção — inscreva-se no canal.\n"
            "Ative o sino.\n"
            "Porque o próximo vídeo vai abrir os Sete Selos.\n"
            "E o que está lá... é ainda mais perturbador."
        ),
    },
]

ESTILO_SUNO = """[Voice: Deep aged male narrator, 55-65 years old, gravelly radio announcer voice, slow deliberate pacing, dramatic suspense tone, Portuguese Brazilian accent, whispered intensity on key phrases, documentary style narration]

[Background: Dark ambient suspense soundtrack, deep ethereal drones, low cello strings, subtle ominous choir pads, reverb-heavy atmosphere, cinematic tension, builds gradually through video]

[Style: Dark biblical documentary, prophetic tone, dramatic pauses between sentences, slow burning intensity, sacred weight on every word]"""


def hr(color=DOURADO, thickness=1):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=8, spaceBefore=8)


def build_pdf():
    os.makedirs(LOCAL_DIR, exist_ok=True)
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=2.5*cm,
        rightMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm,
    )

    story = []

    # ── Cabeçalho ──────────────────────────────────────────────────────────────
    story.append(Paragraph("ABISMO CRIATIVO", style_title))
    story.append(Paragraph("Agência de Canais Dark", style_agencia))
    story.append(hr(VERMELHO, 2))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("NARRAÇÕES PARA SUNO", style_h1))
    story.append(Paragraph("Canal: Sinais do Fim — Passagens do Apocalipse", style_subtitle))
    story.append(Paragraph("Vídeo: video-002-marca-da-besta", style_subtitle))
    story.append(Paragraph(
        "Título: A Marca da Besta Já Está Sendo Implementada — Apocalipse 13",
        style_subtitle
    ))
    story.append(Paragraph("Duração: 15 minutos e 30 segundos | Agente: Orfeu", style_agencia))
    story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}", style_agencia))
    story.append(hr())
    story.append(Spacer(1, 0.5*cm))

    # ── Instruções de uso ─────────────────────────────────────────────────────
    story.append(Paragraph("INSTRUÇÕES DE USO", style_h1))
    story.append(Paragraph(
        "Este documento contém 9 partes de narração limpas para uso no Suno AI. "
        "Cada parte tem no máximo 1.800 caracteres (margem de segurança abaixo do limite de 2.000 do Suno). "
        "Cole cada parte individualmente no campo de narração do Suno, junto com o Estilo de Voz abaixo. "
        "Mantenha a ordem das partes para preservar a continuidade narrativa.",
        style_body
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(hr())

    # ── Estilo Suno ────────────────────────────────────────────────────────────
    story.append(Paragraph("ESTILO DE VOZ E TRILHA (Suno)", style_h1))
    story.append(Paragraph(
        "Cole este bloco junto com cada parte no campo de estilo/prompt do Suno:",
        style_body
    ))
    story.append(Spacer(1, 0.2*cm))
    for linha in ESTILO_SUNO.strip().split("\n"):
        if linha.strip():
            story.append(Paragraph(linha, style_suno))
        else:
            story.append(Spacer(1, 0.2*cm))
    story.append(hr())
    story.append(PageBreak())

    # ── Partes ────────────────────────────────────────────────────────────────
    total = len(PARTES)
    for p in PARTES:
        story.append(Paragraph(
            f"PARTE {p['num']} DE {total}",
            style_h1
        ))
        story.append(Paragraph(
            f"video-002-marca-da-besta — Caracteres: {p['chars']} | Limite: 1.800",
            style_meta
        ))
        story.append(hr(DOURADO, 0.5))
        story.append(Spacer(1, 0.2*cm))

        # Dividir por parágrafo (linha em branco)
        paragrafos = p["texto"].split("\n\n")
        for par in paragrafos:
            linhas = par.strip().split("\n")
            for linha in linhas:
                if linha.strip():
                    story.append(Paragraph(linha, style_narracao))
            story.append(Spacer(1, 0.15*cm))

        story.append(Spacer(1, 0.3*cm))
        story.append(hr())

        if p["num"] < total:
            story.append(PageBreak())

    # ── Rodapé final ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 1*cm))
    story.append(hr(VERMELHO, 2))
    story.append(Paragraph(
        "ABISMO CRIATIVO | Sinais do Fim | video-002-marca-da-besta | Orfeu",
        style_footer
    ))
    story.append(Paragraph(
        f"Total: {total} partes | {sum(p['chars'] for p in PARTES):,} caracteres totais",
        style_footer
    ))

    doc.build(story)
    print(f"[OK] PDF gerado: {PDF_PATH}")


def upload_vps():
    print(f"[SFTP] Conectando em {VPS_HOST}...")
    key = paramiko.Ed25519Key.from_private_key_file(KEY_PATH)
    transport = paramiko.Transport((VPS_HOST, 22))
    transport.connect(username=VPS_USER, pkey=key)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Garantir que o diretório remoto existe (cria recursivamente se necessário)
    remote_dir = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts"
    partes_dir = remote_dir.split("/")
    caminho = ""
    for parte in partes_dir:
        if not parte:
            continue
        caminho += "/" + parte
        try:
            sftp.mkdir(caminho)
        except Exception:
            pass  # já existe

    sftp.put(PDF_PATH, VPS_REMOTE)
    sftp.close()
    transport.close()
    print(f"[OK] Upload concluido: {VPS_URL}")


def registrar_log():
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_chars = sum(p["chars"] for p in PARTES)
    total_partes = len(PARTES)
    linhas = [
        f"[{agora}] ORFEU — {total_partes} partes de narracao geradas ({total_chars} chars totais) → suno_narracoes.pdf na VPS",
        f"[{agora}] LINK — {VPS_URL}",
    ]
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha + "\n")
    print(f"[OK] Log registrado em: {LOG_PATH}")


if __name__ == "__main__":
    print("=" * 60)
    print("ORFEU — Gerando PDF de Narracoes para Suno")
    print("video-002-marca-da-besta | Abismo Criativo")
    print("=" * 60)
    build_pdf()
    upload_vps()
    registrar_log()
    print("=" * 60)
    print(f"ENTREGA CONCLUIDA")
    print(f"PDF local : {PDF_PATH}")
    print(f"URL VPS   : {VPS_URL}")
    print("=" * 60)
