"""
PHANTASMA — Gerador de PDF + Upload VPS
Canal: Sinais do Fim | video-002-marca-da-besta
Agente: Phantasma | Abismo Criativo
Data: 2026-04-06
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
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ── Cores da Agência ──────────────────────────────────────────────────────────
PRETO   = HexColor("#0A0A0A")
VERMELHO = HexColor("#8B0000")
DOURADO = HexColor("#C5A355")
CINZA   = HexColor("#2A2A2A")
CINZA_CLARO = HexColor("#C0C0C0")
BRANCO  = white

# ── Caminhos ──────────────────────────────────────────────────────────────────
LOCAL_DIR   = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\5-prompts"
TXT_PATH    = os.path.join(LOCAL_DIR, "prompts_video.txt")
PDF_PATH    = os.path.join(LOCAL_DIR, "prompts_video.pdf")
LOG_PATH    = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log"

VPS_HOST    = "31.97.165.64"
VPS_PORT    = 22
VPS_USER    = "root"
KEY_PATH    = os.path.expanduser("~/.ssh/id_ed25519")
VPS_REMOTE  = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/prompts_video.pdf"
VPS_DIR     = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts"
URL_PDF     = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/prompts_video.pdf"


# ── Estilos ───────────────────────────────────────────────────────────────────
def build_styles():
    styles = getSampleStyleSheet()

    style_capa_title = ParagraphStyle(
        'CapaTitle',
        parent=styles['Title'],
        fontSize=26,
        textColor=VERMELHO,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        spaceAfter=8,
        leading=32,
    )
    style_capa_sub = ParagraphStyle(
        'CapaSub',
        parent=styles['Normal'],
        fontSize=13,
        textColor=DOURADO,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    style_capa_meta = ParagraphStyle(
        'CapaMeta',
        parent=styles['Normal'],
        fontSize=9,
        textColor=CINZA_CLARO,
        fontName='Helvetica',
        alignment=TA_CENTER,
        spaceAfter=3,
    )
    style_section = ParagraphStyle(
        'Section',
        parent=styles['Heading1'],
        fontSize=13,
        textColor=VERMELHO,
        fontName='Helvetica-Bold',
        spaceBefore=16,
        spaceAfter=4,
        borderPad=4,
    )
    style_quadro_header = ParagraphStyle(
        'QuadroHeader',
        parent=styles['Normal'],
        fontSize=11,
        textColor=DOURADO,
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=4,
        borderPad=3,
    )
    style_clipe_label = ParagraphStyle(
        'ClipeLabel',
        parent=styles['Normal'],
        fontSize=9,
        textColor=DOURADO,
        fontName='Helvetica-Bold',
        spaceBefore=8,
        spaceAfter=2,
    )
    style_field_key = ParagraphStyle(
        'FieldKey',
        parent=styles['Normal'],
        fontSize=8,
        textColor=VERMELHO,
        fontName='Helvetica-Bold',
        spaceAfter=1,
    )
    style_field_val = ParagraphStyle(
        'FieldVal',
        parent=styles['Normal'],
        fontSize=8,
        textColor=PRETO,
        fontName='Helvetica',
        spaceAfter=3,
        leading=12,
    )
    style_prompt = ParagraphStyle(
        'Prompt',
        parent=styles['Normal'],
        fontSize=8,
        textColor=CINZA,
        fontName='Helvetica',
        spaceAfter=6,
        leading=12,
        leftIndent=8,
        borderPad=4,
        backColor=HexColor("#F5F0E8"),
        borderColor=DOURADO,
        borderWidth=0.5,
        borderRadius=3,
        alignment=TA_JUSTIFY,
    )
    style_continuity = ParagraphStyle(
        'Continuity',
        parent=styles['Normal'],
        fontSize=7,
        textColor=HexColor("#666666"),
        fontName='Helvetica-Oblique',
        spaceAfter=3,
        leftIndent=8,
    )
    style_sumario = ParagraphStyle(
        'Sumario',
        parent=styles['Normal'],
        fontSize=9,
        textColor=PRETO,
        fontName='Helvetica',
        spaceAfter=3,
        leading=13,
    )

    return {
        'capa_title': style_capa_title,
        'capa_sub': style_capa_sub,
        'capa_meta': style_capa_meta,
        'section': style_section,
        'quadro_header': style_quadro_header,
        'clipe_label': style_clipe_label,
        'field_key': style_field_key,
        'field_val': style_field_val,
        'prompt': style_prompt,
        'continuity': style_continuity,
        'sumario': style_sumario,
    }


# ── Dados dos prompts ─────────────────────────────────────────────────────────
QUADROS = [
    {
        "id": "V01", "titulo": "PATMOS / JOÃO ESCREVENDO",
        "timestamp": "00:00 → 00:24",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "00:00 → 00:08",
                "sujeito": "João de Patmos — ancião envelhecido, barba longa branca, manto vermelho e dourado em estilo medieval iluminado",
                "acao": "Figura solitária encurvada sobre uma mesa de pedra, pena na mão, rolo de pergaminho aberto à frente",
                "camera": "Extreme wide establishing shot, câmera afasta lentamente do ancião revelando a ilha de Patmos ao redor",
                "iluminacao": "Luz quente dourada irradiando do pergaminho, contraste dramático com o mar escuro ao redor",
                "estilo": "Cinematic medieval illuminated manuscript come to life, fotorealista, 35mm grain",
                "atmosfera": "Mar revolto com ondas altas ao fundo, céu com nuvens de tempestade massivas se acumulando no horizonte",
                "mood": "Isolamento profético, peso sagrado, véspera de revelação",
                "continuity": None,
                "prompt": "An ancient elderly prophet with long white beard and deep-set eyes, wearing a richly colored medieval-style crimson and gold robe with detailed embroidery, crouched over a stone table on a rocky island cliff, writing on an open parchment scroll with a quill pen. Foreground figure in full vivid color, ultra-detailed medieval illuminated manuscript style. Background: black and white dramatic seascape of Patmos island, stormy waves crashing against jagged rocks, dark churning sky with massive cumulonimbus clouds building on the horizon. Extreme wide establishing shot slowly pulling back to reveal the full isolation of the figure on the cliff. Warm golden light emanates from the parchment itself, illuminating the prophet's focused face from below. 35mm cinematic grain, slow cinematic camera movement, epic and ominous mood, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "00:08 → 00:16",
                "sujeito": "Mesmo ancião João, rosto expressivo de 90 anos, olhos vidrados em transe visionário",
                "acao": "Câmera se aproxima do rosto do ancião enquanto ele para de escrever e olha para o horizonte com expressão de terror sagrado",
                "camera": "Medium shot se fechando progressivamente em close, dolly in lento",
                "iluminacao": "Flash de relâmpago distante ilumina dramaticamente metade do rosto em branco; outra metade em sombra dourada",
                "estilo": "Cinematic documentary, hiper-realista, profundidade de campo rasa",
                "atmosfera": "Vento mais forte, cinzas flutuando ao redor, névoa marítima subindo pelas rochas",
                "mood": "Visão apocalíptica iminente, terror e êxtase simultâneos",
                "continuity": "Saindo do plano geral, fechando no rosto que havia estado inclinado",
                "prompt": "Close-up approach of the ancient prophet on Patmos island — an aged man, 90 years old, white beard, deep wrinkled face, trembling lips, eyes wide open in sacred terror and divine trance — stopping his writing mid-stroke, turning his gaze toward the stormy horizon. Full vivid color on the prophet's face and crimson-gold robes, richly detailed medieval portrait style. Background: black and white stormy sea and lightning-split sky. Slow dolly-in medium shot progressively closing to tight close-up. Dramatic side-lighting: lightning flash illuminates one half of face in stark white, the other half bathed in warm golden emanation from the parchment. Floating ash particles in the air, sea mist rising. 35mm film grain, cinematic depth of field, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "00:16 → 00:24",
                "sujeito": "Os olhos do ancião João — olhos de idoso cheios de visões, pupila refletindo imagens apocalípticas",
                "acao": "Extreme close-up dos olhos — dentro das pupilas, reflexo de uma criatura monstruosa emergindo do mar",
                "camera": "Extreme close-up (ECU) dos olhos, câmera absolutamente estática, profundidade de campo mínima",
                "iluminacao": "Reflexo interno nas pupilas em vermelho sangue e dourado; íris azul-cinza do ancião ao redor",
                "estilo": "Surreal, hiper-macro, onírico",
                "atmosfera": "Reflexo nas pupilas mostra visão vívida; lágrimas formando nos cantos dos olhos",
                "mood": "Revelação devastadora, peso profético insustentável",
                "continuity": "Fechamento extremo a partir do close do clipe anterior",
                "prompt": "Extreme macro close-up of ancient prophet's eyes — pale grey-blue irises, aged deep wrinkles around the eyes, white lashes — pupils dilated wide reflecting a tiny vivid image in full color: a monstrous seven-headed beast rising from churning waters. One tear forming at the corner of the left eye catching the golden light. The reflected vision in the pupils glows in crimson and gold against the surrounding black and white. Ultra-sharp foreground on the eye, extreme bokeh on background. The emotion conveyed: sacred terror mixed with divine awe. 35mm film grain, absolutely static camera hold, surreal hyper-real macro cinematography, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V02", "titulo": "PERGAMINHO APOCALÍPTICO",
        "timestamp": "00:24 → 00:48",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "00:24 → 00:32",
                "sujeito": "Mesa de pedra com o pergaminho aberto — texto grego manuscrito visível, iluminado por um candelabro de 7 velas",
                "acao": "Câmera flutua lentamente sobre a mesa, revelando o pergaminho como um objeto sagrado",
                "camera": "Overhead bird's-eye view descendo lentamente para plano médio sobre a mesa, como uma câmera divina",
                "iluminacao": "7 velas iluminam o pergaminho em chama viva dourada; borda do pergaminho irradia luz própria",
                "estilo": "Medieval sacred document, hiper-detalhe, cinematic sacred mystery",
                "atmosfera": "Poeira flutuando na luz das velas, sombras dançantes nas paredes de pedra",
                "mood": "Sagrado, intocável, peso eterno do texto",
                "continuity": None,
                "prompt": "A bird's-eye overhead camera slowly descending toward a stone table holding an ancient open parchment scroll covered in hand-written Greek manuscript text in vivid golden ink. A seven-branched candelabra with burning candles in full vivid warm color stands beside it — foreground parchment and candelabra in rich color detail, each candle flame alive and flickering. The stone cave walls in background are black and white. The parchment itself emits a faint inner glow as if divinely illuminated. Floating dust motes visible in the candlelight. Slow divine descending camera movement from overhead to medium shot. 35mm film grain, sacred atmosphere, cinematic composition, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "00:32 → 00:40",
                "sujeito": "O texto grego no pergaminho — linha específica de Apocalipse 13:17",
                "acao": "Câmera se aproxima do texto enquanto uma linha específica começa a brilhar com luz dourada pulsante",
                "camera": "Slow push-in de plano médio para close sobre o texto, câmera levemente inclinada",
                "iluminacao": "Linha de texto ganha vida própria — pulsa em dourado então em vermelho sangue",
                "estilo": "Mystical sacred document animation, hiper-realista",
                "atmosfera": "Uma gota de cera de vela cai em câmera lenta sobre o canto do pergaminho",
                "mood": "Revelação iminente, texto ganhando poder próprio",
                "continuity": "Descida continuada da câmera do clipe anterior, focando em trecho específico",
                "prompt": "Slow push-in close-up shot approaching ancient Greek manuscript text on aged yellowed parchment — hand-written with a quill in dark ink, slight imperfections visible in each letter stroke. One specific line of text begins to pulse with living golden light then shifts to deep crimson, as if activated by divine power. The parchment is in full vivid color with extreme texture detail — visible fibers, age spots, slight curling edges. In slow-motion, a drop of candle wax falls and lands on the lower corner. Background shadows in black and white. Gentle candlelight flicker. Slow dolly-in, slightly tilted angle. 35mm film grain, mystical atmosphere, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "00:40 → 00:48",
                "sujeito": "Uma única palavra grega — CHARAGMA — no centro do pergaminho",
                "acao": "A câmera vai ao ECU da palavra enquanto ela literalmente se levanta do pergaminho como escrita tridimensional em ouro vivo",
                "camera": "Extreme close-up estático com leve rack focus entre a palavra e o fundo",
                "iluminacao": "A palavra emite luz própria dourada intensa; as outras linhas tornam-se menos brilhantes",
                "estilo": "Surreal sacred typography come to life",
                "atmosfera": "As letras lançam sombras reais nas fibras do pergaminho",
                "mood": "Revelação climática de uma palavra que carrega peso eterno",
                "continuity": "Continuação direta do push-in anterior chegando ao limite macro",
                "prompt": "Extreme macro close-up of a single ancient Greek word 'CHARAGMA' written in hand-calligraphed ink on aged parchment — the letters rising slightly off the page like living three-dimensional golden engravings, glowing with intense warm golden light that casts real shadows on the parchment fibers around them. The surrounding text remains on the page in normal ink, slightly blurred by shallow depth of field. The word's light pulses slowly and rhythmically. Visible parchment texture: individual fibers, ancient stains, the slight indentation of the quill stroke. Static camera with subtle rack focus. 35mm grain. Sacred revelation mood, cinematic surreal, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V03", "titulo": "BESTA EMERGINDO DO OCEANO DIGITAL",
        "timestamp": "00:48 → 01:12",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "00:48 → 00:56",
                "sujeito": "Oceano noturno vasto e tempestuoso — superfície agitada por redemoinhos — em preto e branco",
                "acao": "Câmera sobre a superfície do oceano, água borbulhando e formando espirais, algo massivo se movimentando sob a superfície",
                "camera": "Low angle wide shot sobre a superfície da água, câmera levemente instável como montada em barco",
                "iluminacao": "Relâmpagos iluminam a cena intermitentemente; sombra enorme visível sob a água",
                "estilo": "Apocalyptic ocean horror, documentário épico",
                "atmosfera": "Mar todo em preto e branco; trovões, ondas de 10 metros, redemoinho central",
                "mood": "Terror cósmico, presença massiva se aproximando",
                "continuity": None,
                "prompt": "Sweeping low-angle wide shot over a vast black and white stormy ocean at night — massive 10-meter waves crashing in slow motion, intermittent lightning flashes illuminating churning water. A colossal dark shape is visible beneath the surface, moving upward — suggestion of enormous scale, barely distinguishable from the deep black water. Violent whirlpool forming at center frame. The entire scene is desaturated, black and white with deep contrast. Camera is slightly unstable as if mounted on a vessel. The atmosphere is pure dread — something ancient and massive is waking from the deep. 35mm film grain, epic cinematic apocalyptic framing, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "00:56 → 01:04",
                "sujeito": "Sete cabeças de uma besta colossal emergindo da água — escamas douradas e vermelhas vibrantes, chifres de ouro",
                "acao": "As sete cabeças surgem lentamente da superfície do mar com água torrencial caindo delas",
                "camera": "Medium shot frontal levemente baixo, câmera estática enquanto a besta sobe",
                "iluminacao": "As cabeças da besta em cores ricas — escamas douradas e vermelhas — contra oceano e céu em P&B",
                "estilo": "Medieval bestiário iluminado em live-action, referência ao Apocalipse de Bamberg",
                "atmosfera": "Água em cascata das sete cabeças, chamas nas bocas abertas, olhos vermelho-sangue luminosos",
                "mood": "Êxtase profético e terror absoluto",
                "continuity": "A sombra submersa do clipe anterior agora emerge como besta identificável",
                "prompt": "Seven enormous dragon heads of a colossal sea beast slowly rising from a black and white churning ocean — each head covered in richly detailed golden and crimson scales, massive curved golden horns on each crown, jaws opening to reveal flames, eyes glowing blood red. The creature's heads and upper body are in full vivid color — medieval illuminated manuscript bestiary style, hyper-detailed scales and anatomical features. The ocean, sky, and background remain pure black and white. Torrents of water cascade from the rising heads. Static medium shot, low camera angle, frontal composition. Epic scale — the heads dwarf any building. 35mm grain, apocalyptic wonder, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "01:04 → 01:12",
                "sujeito": "Uma das cabeças da besta — a central — olhando diretamente para a câmera",
                "acao": "A cabeça central se abaixa até o nível da câmera e os olhos vermelhos encaram diretamente o espectador",
                "camera": "Extreme close-up do rosto da besta, câmera absolutamente estática",
                "iluminacao": "Os olhos da besta iluminam tudo ao redor em vermelho sangue pulsante",
                "estilo": "Horror divino, confronto direto com o espectador",
                "atmosfera": "Fumaça saindo das narinas, calor visível distorcendo o ar ao redor",
                "mood": "Confronto direto, cumprimento profético, decisão iminente",
                "continuity": "A cabeça central do grupo do clipe anterior descendo para encarar a câmera",
                "prompt": "Extreme close-up of the central head of the seven-headed beast — a massive dragon face with golden and crimson scales, enormous curved golden horn, blood-red luminous eyes staring directly into the camera at eye level. The beast's face fills the frame. Its eyes pulse with deep crimson light that illuminates the surrounding black and white storm in red. Smoke rises slowly from flared nostrils. Heat distortion ripples the air around its face. Full vivid color on the beast's face and scales — medieval illuminated bestiary hyper-detail on every scale and facial feature. The confrontational gaze creates immediate dread. Static camera, held ECU. 35mm grain, apocalyptic confrontation mood, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V04", "titulo": "MÃO RECEBENDO A MARCA",
        "timestamp": "01:12 → 01:36",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "01:12 → 01:20",
                "sujeito": "Uma mão direita — pele clara, veias visíveis — estendida com a palma voltada para cima",
                "acao": "A mão entra em quadro vinda de baixo, se estabiliza no centro",
                "camera": "Medium close-up frontal, câmera estática, mão centralizada no frame",
                "iluminacao": "Fundo de laboratório moderno em preto e branco; a mão iluminada por luz branca clínica",
                "estilo": "Medical documentary meets prophetic horror",
                "atmosfera": "Sala asséptica em P&B ao fundo, superfície de mesa de metal fria visível",
                "mood": "Vulnerabilidade, submissão involuntária, limiar irrevogável",
                "continuity": None,
                "prompt": "A single human right hand — pale skin, visible veins on the back, slight tremor — extended palm-up in the center of frame, as if being presented for a procedure. The hand is in neutral skin tones, naturalistically lit. Background: a modern medical laboratory room in black and white — stainless steel surfaces, clinical lighting rigs, out-of-focus medical equipment. The hand is the only subject in near focus. Static medium close-up, frontal composition, hand centered. The mood is submission and vulnerability. 35mm film grain, clinical horror atmosphere, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "01:20 → 01:28",
                "sujeito": "A mesma mão — agora com uma microseringa se aproximando da base do polegar",
                "acao": "A agulha desce em câmera lenta em direção à pele, tocando a superfície levemente",
                "camera": "Close-up macro da mão e agulha, câmera levemente inclinada, shallow depth of field",
                "iluminacao": "A agulha captura reflexos brancos; ao tocar a pele, surge brilho vermelho pulsante sob a pele",
                "estilo": "Medical macro horror, hyper-real",
                "atmosfera": "Tensão máxima no momento de contato; chip minúsculo visível dentro da seringa",
                "mood": "Ponto de não-retorno, horror cotidiano, decisão irrevogável materializada",
                "continuity": "Câmera se fechou sobre a mão do clipe anterior e agora a agulha entra em quadro",
                "prompt": "Macro close-up of a human right hand — palm area near the base of the thumb — as a translucent micro-needle syringe slowly descends in extreme slow motion toward the skin. Inside the syringe, a tiny metallic microchip is visible suspended in clear liquid. The needle tip makes first contact with the skin, slightly indenting it. At the moment of contact, a subtle deep crimson red pulse glow begins emanating from beneath the skin. The hand is in full color, hyper-detailed skin texture. Syringe in clinical silver and translucent. Background out-of-focus black and white laboratory. Extreme shallow depth of field, static slightly-tilted close-up. 35mm grain, medical horror, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "01:28 → 01:36",
                "sujeito": "A pele da mão após a implantação — microchip visível como saliência sob a pele",
                "acao": "A agulha é retirada em câmera lenta enquanto a saliência do chip pulsa em vermelho sangue rítmico",
                "camera": "Extreme close-up estático, macro extremo, profundidade de campo mínima",
                "iluminacao": "O brilho vermelho pulsante sob a pele como único ponto de cor",
                "estilo": "Body horror surreal, médico-profético",
                "atmosfera": "Uma pequena gota de sangue forma-se no ponto de entrada",
                "mood": "Irreversível, o sistema entra no corpo, marca permanente",
                "continuity": "Sequência direta do momento da inserção",
                "prompt": "Extreme macro static close-up of human right hand skin — palm area — immediately after a microchip implantation. The needle has been withdrawn, leaving a tiny entry point from which a single small drop of deep red blood slowly forms and trails down the pale skin. Beneath the skin surface, a tiny rectangular microchip outline is visible as a subtle raised contour, pulsing with a deep crimson red internal glow that rhythmically brightens and dims like a heartbeat. The pulse glow is the only vivid color in the frame. Everything else in natural skin tones. Background entirely out of focus black and white. Minimum depth of field, static camera. The emotional weight: irreversibility. 35mm grain, body horror atmosphere, surreal medical imagery, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V05", "titulo": "ROMA IMPERIAL",
        "timestamp": "01:36 → 02:00",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "01:36 → 01:44",
                "sujeito": "Roma no século I — procissão imperial colorida atravessando o Fórum Romano",
                "acao": "Câmera em plano geral elevado mostra a procissão avançando: soldados dourados, sacerdotes vermelhos, estandartes",
                "camera": "High angle wide establishing shot, câmera lentamente baixando",
                "iluminacao": "Sol mediterrâneo quente e dourado sobre a procissão colorida; Coliseu ao fundo em P&B",
                "estilo": "Epic Roman historical drama, Ridley Scott aesthetic, medievalizado",
                "atmosfera": "Fumaça de incenso, multidão de cidadãos assistindo nos lados em P&B",
                "mood": "Poder imperial esmagador, pompa e opressão simultâneas",
                "continuity": None,
                "prompt": "High angle wide establishing shot of an ancient Roman imperial procession moving through the Forum Romanum — soldiers in gleaming golden armor, crimson-cloaked centurions, priests in white and purple togas, golden eagle standard-bearers, all in full vivid color with rich detail. The procession subjects are in bright Roman colors — gold, crimson, white, purple — medieval historical illustration style brought to photorealistic life. Background: the Colosseum and Roman cityscape in dramatic black and white, crowds of watching citizens on either side desaturated. Rich Mediterranean golden sunlight on the procession. Incense smoke visible. Camera slowly descending from high angle. Epic scale. 35mm grain, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "01:44 → 01:52",
                "sujeito": "Um mercador apresentando o libellus — certificado de lealdade imperial — a um soldado romano",
                "acao": "O mercador (colorido) estende o rolo de papel ao soldado que inspeciona antes de permitir a passagem",
                "camera": "Medium shot levemente baixo, câmera estática",
                "iluminacao": "Luz dourada do sol; sombra do soldado cobre parcialmente o mercador",
                "estilo": "Narrative historical drama",
                "atmosfera": "Fundo do mercado romano em P&B; outros mercadores aguardando na fila",
                "mood": "Controle econômico, lealdade obrigatória, sistema de permissões imperiais",
                "continuity": "A câmera desceu da procissão para focar neste momento cotidiano de controle",
                "prompt": "Medium shot of a Roman merchant in the Forum — a middle-aged man in colorful humble brown and ochre merchant's tunic and cloak, richly textured in full color — presenting a rolled papyrus document (libellus — certificate of imperial loyalty) to a Roman legionary soldier in full polished armor. The soldier examines the document carefully before permitting passage. The merchant is in full color, the soldier in gold and crimson armor in full color. Background: black and white Roman market street, other waiting merchants desaturated. Golden Mediterranean sunlight creates a power shadow from the soldier over the merchant. Static medium shot, slightly low angle. 35mm grain, historical drama atmosphere, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "01:52 → 02:00",
                "sujeito": "Moeda romana de ouro — denário — com o rosto do imperador gravado",
                "acao": "A moeda gira lentamente no ar em câmera lenta, o rosto do imperador passando de retrato imperial para expressão demoníaca",
                "camera": "Extreme close-up da moeda girando, fundo preto e branco desfocado",
                "iluminacao": "Luz dourada pura na moeda; o rosto do imperador iluminado dramaticamente",
                "estilo": "Numismatic horror, surreal transformation",
                "atmosfera": "À medida que a moeda gira, a expressão do imperador parece viva e ameaçadora",
                "mood": "Idolatria ao poder, marcas imperiais como proto-Marca da Besta",
                "continuity": "A moeda conecta o libellus ao tema da Marca via objeto tangível",
                "prompt": "Extreme close-up slow-motion shot of a golden Roman denarius coin spinning slowly in mid-air against an out-of-focus black and white background. The coin is in full vivid gold color, hyper-detailed — visible engraving imperfections, aged patina, profile of a Roman emperor on one face. As the coin rotates, the emperor's portrait seems to subtly shift expression — a slight, almost imperceptible change from regal authority to something darker and threatening, a surreal living quality. Both sides of the coin rotate into view. The golden light on the spinning coin is the primary illumination source. Static ECU camera. 35mm grain, surreal numismatic horror, prophetic undertone, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V06", "titulo": "LUTERO E OS REFORMADORES",
        "timestamp": "02:00 → 02:24",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "02:00 → 02:08",
                "sujeito": "Martinho Lutero em praça alemã medieval — hábito de monge preto, pregando para uma multidão",
                "acao": "Wide shot mostra Lutero no alto de degraus de catedral, gesticulando com livro aberto",
                "camera": "Wide shot ligeiramente elevado, câmera lenta se aproximando",
                "iluminacao": "Tarde nublada com luz difusa; Lutero em cores ricas, catedral gótica ao fundo em P&B",
                "estilo": "Reformation historical epic, medieval German town atmosphere",
                "atmosfera": "Vento agitando os hábitos de Lutero, papéis voando, multidão em P&B ao redor",
                "mood": "Coragem reformadora, choque entre autoridade espiritual e institucional",
                "continuity": None,
                "prompt": "Wide cinematic shot of Martin Luther — a robust, intense man in his 30s wearing a full black Augustinian monk's habit with rich fabric detail — standing on cathedral steps above a crowd in a medieval German town square, holding an open Bible and gesturing passionately while preaching. Luther is in full vivid color — deep black habit, intense eyes, strong jaw — medieval historical portrait style brought to life. Background: Gothic cathedral architecture and the surrounding medieval town in black and white. The crowd of listeners is desaturated. Windswept papers in the air. Overcast atmospheric lighting with one shaft of light on Luther. Camera slowly pushing in from wide. 35mm grain, Reformation epic atmosphere, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "02:08 → 02:16",
                "sujeito": "Lutero pregando — expressão de confronto total, dedo apontando para cima",
                "acao": "Medium shot de Lutero no clímax da pregação, rosto avermelhado de convicção",
                "camera": "Medium shot frontal, câmera levemente baixa para heroicizar",
                "iluminacao": "Raio de sol penetrando nuvens ilumina Lutero como luz divina; ao redor tudo em sombra P&B",
                "estilo": "Heroic reformation portraiture",
                "atmosfera": "Ao fundo em sombra e P&B, figuras encurvadas com mitras papais se retiram",
                "mood": "Confronto com sistema religioso estabelecido, coragem profética",
                "continuity": "Câmera fechou do wide anterior para o medium shot de Lutero",
                "prompt": "Medium shot of Martin Luther at the climax of his sermon — face flushed red with conviction, eyes blazing with certainty, left hand holding an open Bible raised chest-height, right hand with index finger pointed forcefully upward toward heaven. Full vivid color: black habit, intense flushed face, golden candlelight catching the Bible's gilt pages. Low camera angle makes Luther appear heroic. A shaft of pale sunlight breaks through storm clouds to illuminate only him. In the background shadows, black and white silhouettes of figures in papal mitres and robes retreat. 35mm film grain, dramatic side-lighting, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "02:16 → 02:24",
                "sujeito": "Uma folha pregada na porta de madeira da catedral — as 95 Teses",
                "acao": "ECU da folha sendo fixada com um prego na madeira — o prego entra em câmera lenta",
                "camera": "Extreme close-up da mão, o prego e a porta — câmera estática macro",
                "iluminacao": "A folha do texto iluminada por tocha; a madeira da porta em P&B",
                "estilo": "Historical symbolic moment, hiper-detalhe",
                "atmosfera": "A madeira trinca levemente com o prego",
                "mood": "Ponto de ruptura histórica, ato que mudou o mundo, irreversibilidade",
                "continuity": "Consequência direta do ato proclamado no clipe anterior",
                "prompt": "Extreme macro close-up of a human hand hammering an iron nail through a handwritten document into an ancient dark oak cathedral door — the nail entering the wood in extreme slow motion, wood fibers splitting slightly around it, the document pressed flat against the rough grain of the door. The hand is in full color — knuckles pale with effort, iron nail reflecting torchlight warmly. The document parchment is in full color, handwritten text visible but unreadable as detail. The cathedral door wood is in black and white with deep grain texture. A faint echo implied in the frame. Macro static camera. 35mm grain, historic symbolic weight, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V07", "titulo": "MAPA CBDC / 134 PAÍSES",
        "timestamp": "02:24 → 02:48",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "02:24 → 02:32",
                "sujeito": "Mapa-múndi em projeção holográfica flutuando no escuro — países em cinza aguardando ativação",
                "acao": "Câmera se afasta do mapa para mostrar a escala completa do globo em holograma",
                "camera": "Wide shot se afastando do mapa 3D, revelando que flutua no vácuo digital",
                "iluminacao": "Mapa emitindo luz própria suave azul-cinza; fundo completamente negro",
                "estilo": "Digital surveillance thriller, data visualization aesthetic",
                "atmosfera": "Partículas de dados flutuando ao redor do mapa, linhas de conexão entre países",
                "mood": "Escala global de um sistema que se prepara para ativar",
                "continuity": None,
                "prompt": "Wide shot of a glowing holographic three-dimensional world map floating in total digital darkness — continents and countries rendered in pale grey-white light, borders visible, all countries initially in neutral grey awaiting activation. The map emits its own cool blue-white light. Floating data particles drift around it like digital fireflies. Thin lines of connection between major city nodes on the map pulse faintly. Camera slowly pulls back to reveal the full globe projection in its entirety. The feeling of a global surveillance control room display. Black void background. 35mm grain effect on digital aesthetic, cinematic data visualization, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "02:32 → 02:40",
                "sujeito": "O mesmo mapa holográfico — países começando a acender em vermelho um por um",
                "acao": "Países vão acendendo em vermelho sangue em sequência rápida — Oriente, Europa, Américas",
                "camera": "Medium shot do mapa, câmera estática",
                "iluminacao": "Cada ativação em vermelho sangue pulsante; o resto do mapa ainda em cinza neutro",
                "estilo": "Apocalyptic data visualization, countdown aesthetic",
                "atmosfera": "O mapa vai ficando mais e mais vermelho conforme os países acendem",
                "mood": "Sistema global se fechando ao redor da humanidade, escala inescapável",
                "continuity": "O mapa do clipe anterior começa sua ativação progressiva",
                "prompt": "Medium shot of the holographic world map — countries activating one by one in rapid sequence, each lighting up in deep blood red that pulses outward from its center like a spreading contamination. The activation sequence moves from East Asia westward — China, India, Europe, Americas — each country's activation creates a brief bright crimson flare before settling into steady deep red. Grey countries rapidly becoming outnumbered by red ones. The red glow of activated nations reflects off floating data particles in the dark void. Static camera holds on the entire map. The cumulative visual effect is alarming — the world is turning red. 35mm grain, apocalyptic data visualization, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "02:40 → 02:48",
                "sujeito": "O mapa agora quase totalmente vermelho — os últimos países acendendo",
                "acao": "Os últimos países acendem; o mapa torna-se completamente vermelho e pulsa como um coração vivo",
                "camera": "Extreme close-up do mapa inteiramente vermelho, câmera avançando através dele",
                "iluminacao": "O mapa vermelho ilumina tudo ao redor; sem luz restante em azul ou cinza",
                "estilo": "Total system capture, visceral global horror",
                "atmosfera": "O mapa pulsando como órgão vivo; linhas tornando-se veias vermelhas",
                "mood": "Sistema global completo, nenhuma saída, cumprimento profético",
                "continuity": "Sequência final da ativação progressiva",
                "prompt": "Extreme close-up push-in through a completely blood-red holographic world map — every country now activated and glowing deep crimson. The map pulses rhythmically like a living heart, each pulse sending ripples of deeper red across all borders simultaneously. Connection lines between nations have transformed into pulsing red veins. The camera pushes forward through the map surface as if entering it, the red glow intensifying and filling the entire frame. The surrounding digital void is washed entirely in crimson light. The feeling: total system capture, global completion. The map breathes. 35mm grain effect, apocalyptic systemic horror, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V08", "titulo": "CHIP IMPLANTÁVEL / MICROAGULHA",
        "timestamp": "02:48 → 03:12",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "02:48 → 02:56",
                "sujeito": "Mesa de laboratório cirúrgico — microseringa, microchip RFID, luvas cirúrgicas, campo estéril",
                "acao": "Câmera desce lentamente sobre a mesa revelando os objetos como artefatos proféticos",
                "camera": "Overhead bird's-eye shot descendo lentamente, câmera estável",
                "iluminacao": "Luz cirúrgica branca intensa; objetos em tons naturais contra campo cirúrgico em P&B",
                "estilo": "Surgical medical horror still life",
                "atmosfera": "Laboratório asséptico totalmente em P&B; apenas os objetos na mesa com cor sutil",
                "mood": "Precisão clínica como prelúdio ao horror",
                "continuity": None,
                "prompt": "Overhead bird's-eye shot slowly descending over a sterile surgical tray — a tiny translucent micro-syringe barely 3mm long, a miniature rectangular RFID microchip with visible antenna coils, sterile surgical gloves still sealed in packaging, a sterile drape. The objects are rendered in natural colors on a desaturated black and white surgical table surface. Harsh overhead surgical light. The camera descends steadily revealing each object in deliberate sequence. Clinical sterility and inhuman precision. Modern medical laboratory background in black and white. 35mm grain, surgical horror still life, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "02:56 → 03:04",
                "sujeito": "Mão com luva cirúrgica segurando a microseringa sobre a pele de uma mão estendida",
                "acao": "A mão enluvada posiciona a microagulha sobre a pele, alinhando com precisão milimétrica",
                "camera": "Close-up médio levemente de cima, câmera lenta aproximando",
                "iluminacao": "Luz cirúrgica criando sombra precisa; a ponta da agulha refletindo luz em ponto brilhante",
                "estilo": "Surgical procedure documentary macro",
                "atmosfera": "Tensão do momento pré-inserção; pele levemente comprimida",
                "mood": "Frieza técnica vs. violação corporal iminente",
                "continuity": "Mão enluvada pegou a seringa da bandeja do clipe anterior",
                "prompt": "Close-up shot from slightly above of a latex-gloved hand — pale blue surgical glove — precisely positioning a micro-syringe over the skin of an outstretched human right hand. The gloved hand's grip is steady, clinical, efficient. The micro-needle tip catches the surgical light with a bright point of reflection. The patient's hand skin is visible below, slightly compressed by the procedure contact. Both hands are in muted natural color tones. Background: out-of-focus black and white laboratory. Slow camera approach. The visual tension of the pre-insertion moment. 35mm grain, surgical documentary macro, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "03:04 → 03:12",
                "sujeito": "O microchip — visível dentro da agulha — em macro extremo revelando circuitos como cidade",
                "acao": "A câmera entra na agulha translúcida em zoom macro extremo, revelando o chip como uma cidade em miniatura",
                "camera": "Extreme macro zoom através do líquido translúcido da seringa",
                "iluminacao": "Luz atravessando o líquido criando refração; o chip iluminado de dentro",
                "estilo": "Surreal macro contemplation, scientific horror meets biblical prophecy",
                "atmosfera": "O chip parece vasto quando visto em macro — um universo de controle em miniatura",
                "mood": "O horror está na escala — uma cidade de controle dentro de um grão de arroz",
                "continuity": "Zoom dentro da seringa posicionada no clipe anterior",
                "prompt": "Extreme macro zoom-through shot passing through clear liquid inside a translucent micro-syringe to reveal the RFID microchip within — at this scale, the chip's circuit traces appear vast and complex, like an aerial view of a city grid: gold and silver circuit lines as roads, dark rectangular capacitors as buildings, the antenna coil as a highway ring. The liquid refracts the surgical light into prismatic rainbows around the chip. Everything is hyper-detailed and surreal — the scale inversion makes something tiny appear monumental and overwhelming. Static extreme macro, rack focus through the liquid to the chip. The weight of the image: infinite control compressed to a grain of rice. 35mm grain, surreal scientific macro, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V09", "titulo": "TRANSAÇÃO BLOQUEADA",
        "timestamp": "03:12 → 03:36",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "03:12 → 03:20",
                "sujeito": "Interior de supermercado moderno — filas de caixa, prateleiras, luzes fluorescentes",
                "acao": "Câmera em plano geral mostra ambiente familiar do supermercado, pessoas fazendo compras normalmente",
                "camera": "Wide shot levemente elevado, câmera estática",
                "iluminacao": "Fluorescentes frias do supermercado em P&B; figura específica na fila com cor natural",
                "estilo": "Observational documentary, surveillance camera aesthetic",
                "atmosfera": "Ambiente P&B desaturado, normalidade antes da ruptura",
                "mood": "Falsa segurança, cotidiano prestes a ser interrompido",
                "continuity": None,
                "prompt": "Wide slightly elevated static shot of a modern supermarket checkout area — multiple checkout lanes, fluorescent overhead lighting, shelves of products visible. The entire scene is rendered in cold black and white desaturation — like security camera footage. One figure stands in a checkout lane holding grocery items, rendered in slightly more naturalistic color than the surroundings, making them stand out. The quiet normalcy of everyday commerce before something goes wrong. Surveillance aesthetic, institutional coldness. 35mm grain overlay, documentary wide shot, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "03:20 → 03:28",
                "sujeito": "O momento do pagamento — pessoa passando o cartão na maquineta",
                "acao": "Pessoa passa o cartão — a maquineta emite tela vermelha de recusa",
                "camera": "Medium shot da pessoa e da maquineta, câmera estática",
                "iluminacao": "O vermelho intenso da tela de recusa ilumina o rosto da pessoa — único brilho colorido",
                "estilo": "Economic horror, moment of exclusion",
                "atmosfera": "Cashier neutro; fila atrás olhando; silêncio embaraçoso",
                "mood": "Exclusão econômica, o sistema recusando existência, humilhação pública",
                "continuity": "A pessoa colorida da fila do clipe anterior chegou ao caixa",
                "prompt": "Medium static shot of a person at a supermarket checkout — they swipe their card through a payment terminal. The terminal displays a large red denial screen that pulses with deep crimson light, illuminating the person's face in red from below — the only strong color in the otherwise black and white scene. The person's face shows confusion then dawning horror. Behind them, the black and white silhouettes of other customers watching. The cashier's expression is neutral, institutional. The groceries sit waiting on the belt. The red light of the denied transaction is harsh, pulsing. 35mm grain, economic horror atmosphere, no text on the terminal screen, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "03:28 → 03:36",
                "sujeito": "O rosto da pessoa após a recusa — close extremo",
                "acao": "A câmera vai para o close do rosto iluminado em vermelho — confusão evoluindo para terror-compreensão",
                "camera": "Extreme close-up do rosto, câmera estática",
                "iluminacao": "Apenas a luz vermelha da maquineta iluminando o rosto — resto em sombra P&B",
                "estilo": "Portrait of exclusion, prophetic horror",
                "atmosfera": "Reflexo da tela vermelha nos olhos; lágrimas formando",
                "mood": "Realização da profecia — Apocalipse 13:17 materializado",
                "continuity": "Close do rosto da pessoa que acabou de ter o cartão recusado",
                "prompt": "Extreme close-up static shot of a person's face after their payment was denied — lit only by the pulsing blood-red light of the declined transaction screen reflected on their skin. The expression moves in slow motion from confusion through disbelief to dawning existential horror. The red light creates harsh shadows across their face, leaving half in deep shadow. Their eyes reflect tiny crimson screens. A tear catches the red light at the corner of one eye. The background is complete black and white darkness. The face fills the frame. This is what Revelation 13:17 looks like. 35mm grain, portrait of prophetic exclusion, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V10", "titulo": "DREX / REAL DIGITAL",
        "timestamp": "03:36 → 04:00",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "03:36 → 03:44",
                "sujeito": "O símbolo do Real brasileiro — R$ — flutuando em espaço digital escuro, se transformando",
                "acao": "O símbolo R$ começa a se transformar digitalmente, pixels se reorganizando para versão fria",
                "camera": "Medium shot do símbolo flutuante, câmera lenta afastando",
                "iluminacao": "Símbolo emitindo luz verde-dourada inicial que vai esfriando para azul digital",
                "estilo": "Digital currency visualization, monetary horror",
                "atmosfera": "Espaço digital vazio e escuro ao redor; símbolo como objeto isolado",
                "mood": "Transição do dinheiro humano para o dinheiro programado",
                "continuity": None,
                "prompt": "Medium shot of a golden Brazilian Real currency symbol (R$) floating in dark digital void space — initially glowing warm gold, the symbol slowly begins to digitally transform: pixels and data fragments breaking away from the edges, the warm gold color cooling to cold electric blue-white, as if the currency is being dematerialized and reprogrammed. The transformation is gradual and unsettling. The symbol floats centered in darkness, emitting its own light. Camera slowly pulls back. Background: pure digital void. 35mm grain aesthetic over digital imagery, monetary horror atmosphere, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "03:44 → 03:52",
                "sujeito": "O símbolo R$ transformado em digital — circundado por código binário orbital",
                "acao": "Fluxos de código binário giram em órbita ao redor do símbolo como planetas ao redor do sol",
                "camera": "Medium close-up, câmera girando lentamente em torno do símbolo",
                "iluminacao": "Código binário em azul frio; símbolo central em dourado frio",
                "estilo": "Digital surveillance aesthetic, code visualization",
                "atmosfera": "O código orbita cada vez mais rápido; o símbolo parece cada vez mais preso",
                "mood": "O dinheiro aprisionado pelo código, programabilidade como controle",
                "continuity": "O símbolo transformado do clipe anterior agora completamente rodeado",
                "prompt": "Medium close-up shot with slow camera orbit around a digital Real currency symbol (R$) now transformed to cold metallic electric blue — surrounded by streams of binary code (zeros and ones) flowing in orbital rings around it like digital electrons or planetary rings. The binary streams move with increasing velocity. The currency symbol at center appears trapped, encircled. The binary code streams are in cold electric blue, the symbol in dim cold gold. The entire system floats in black digital void. Camera slowly rotates around the symbol. 35mm grain, digital control visualization, no text beyond binary 0/1 characters in the code streams, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "03:52 → 04:00",
                "sujeito": "O símbolo do real digital com um cadeado digital pulsante sobre ele",
                "acao": "Um cadeado digital dourado fecha sobre o símbolo R$; a câmera vai ao ECU do cadeado fechado",
                "camera": "Extreme close-up do cadeado fechando, câmera absolutamente estática",
                "iluminacao": "O cadeado emite luz dourada intensa ao fechar; depois escurece para vermelho baixo",
                "estilo": "Digital lock horror, monetary control visualization",
                "atmosfera": "O código binário para de orbitar após o fechamento do cadeado",
                "mood": "Controle total ativado, dinheiro programável aprisionado pelo Estado",
                "continuity": "Consequência do aprisionamento progressivo do símbolo nos clipes anteriores",
                "prompt": "Extreme close-up static shot of a digital golden padlock materializing over the Brazilian Real digital symbol — the lock mechanism closing in slow motion, golden light flaring intensely at the moment of closure, then dimming to a low threatening deep crimson glow. After the lock closes, the binary code streams in orbit slow to a halt. The padlock and symbol are in full color detail — intricate digital engraving on the lock surface. Everything else in digital black void. The lock is the size of the currency symbol it imprisons. The silence after the click. Static camera holds on the closed lock. 35mm grain aesthetic, digital control horror, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V11", "titulo": "CÂMERAS PROLIFERANDO",
        "timestamp": "04:00 → 04:24",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "04:00 → 04:08",
                "sujeito": "Rua urbana moderna — câmeras de vigilância crescendo como plantas dos postes",
                "acao": "Time-lapse estilizado mostra câmeras brotando de postes e paredes como plantas crescendo",
                "camera": "Wide shot de rua, câmera estática como câmera de segurança",
                "iluminacao": "Dia urbano frio em P&B; câmeras crescendo em preto metálico",
                "estilo": "Surreal surveillance horror, botanical metaphor",
                "atmosfera": "Rua vazia em P&B; câmeras crescendo organicamente como erva daninha",
                "mood": "Proliferação inevitável e orgânica de vigilância",
                "continuity": None,
                "prompt": "Wide static surveillance-camera-style shot of an empty black and white urban street — lamp posts and walls sprout security cameras organically, as if they are growing like plants in a time-lapse effect. Each camera grows upward from a post like a dark metallic flower, the lens opening like a blooming eye. The cameras are rendered in black metallic tones against the black and white city. The effect is botanical and uncanny — urban infrastructure breeding its own surveillance organs. The street is empty of humans. Cold overcast sky. Surveillance POV aesthetic. 35mm grain, surreal horror of proliferating surveillance, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "04:08 → 04:16",
                "sujeito": "Floresta de câmeras — dezenas apontando em todas as direções de um único poste",
                "acao": "Câmera se aproxima do poste que tem câmeras crescendo em todas as direções como galhos de árvore",
                "camera": "Medium shot do poste-árvore de câmeras, câmera lentamente girando ao redor dele",
                "iluminacao": "Todos os lentes refletem um olho medieval dourado e colorido no centro",
                "estilo": "Gothic surveillance surrealism",
                "atmosfera": "As câmeras se movem levemente como ramos ao vento, cada uma rastreando silenciosamente",
                "mood": "Ubiquidade total do olhar do Estado, o all-seeing eye do Apocalipse",
                "continuity": "Uma das câmeras proliferando do clipe anterior revela-se como a central",
                "prompt": "Medium shot slowly orbiting around a single lamp post that has grown into a tree-like structure of surveillance cameras — dozens of cameras branching in all directions from the central post like dark metallic branches. Each camera lens reflects a tiny vivid medieval golden eye illustration — bright color against the black and white scene. The cameras sway very slightly like branches in wind, each tracking independently. The overall structure resembles both a technological tree and a multi-eyed supernatural creature. Black and white urban background. Slow 360° camera orbit. 35mm grain, gothic surveillance surrealism, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "04:16 → 04:24",
                "sujeito": "O lente de uma única câmera — ECU — o olho mecânico com olho medieval gravado",
                "acao": "ECU de lente de câmera — dentro do reflexo, o rosto de uma pessoa é visível, rastreado e identificado em vermelho",
                "camera": "Extreme close-up da lente, câmera absolutamente estática",
                "iluminacao": "A lente reflete a cidade em P&B; no centro, o rosto rastreado iluminado em vermelho",
                "estilo": "Surveillance system POV horror, the machine looking back",
                "atmosfera": "Bordas da lente com olho medieval colorido gravado; tecnologia e profecia fundidas",
                "mood": "Você está sendo visto, não há evasão",
                "continuity": "ECU do lente de uma das câmeras da árvore do clipe anterior",
                "prompt": "Extreme close-up static shot of a single surveillance camera lens — filling the entire frame. The lens reflects the black and white city street in its curved glass surface. In the very center of the reflection, a single human face is visible, highlighted in red targeting light as if being tracked by facial recognition, surrounded by faint red targeting reticle lines visible on the lens surface. The rim of the lens has an engraved medieval eye illustration in vivid gold and crimson color — technology and biblical prophecy fused as one object. The lens stares. Static ECU. 35mm grain, surveillance horror, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V12", "titulo": "CRÉDITO SOCIAL",
        "timestamp": "04:24 → 04:48",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "04:24 → 04:32",
                "sujeito": "Rua urbana asiática — cidadão caminhando com número de score flutuando acima da cabeça",
                "acao": "Wide shot mostra rua com cidadão andando, câmeras rastreando, número dourado-laranja sobre a cabeça",
                "camera": "Wide shot levemente elevado, câmera estática",
                "iluminacao": "Rua em P&B; o número flutuante acima da cabeça em dourado-laranja vibrante",
                "estilo": "Dystopian documentary, social credit visualization",
                "atmosfera": "Outros pedestres em P&B sem scores; apenas este cidadão com score visível",
                "mood": "Normalidade distópica, vigilância como arquitetura do cotidiano",
                "continuity": None,
                "prompt": "Wide slightly elevated static shot of a black and white modern urban Asian street — a single citizen walking normally among surveillance cameras mounted everywhere, neon signs, other pedestrians. Above the walking citizen's head, a glowing floating score number in vivid golden-orange color is visible — holographic, like an augmented reality overlay. The number is high (like 950) at this point. Other pedestrians in the street have no visible score — they are fully desaturated. Surveillance cameras on every post track the citizen automatically. Dystopian normalcy — surveillance as invisible architecture. 35mm grain, dystopian documentary, no text beyond the single number above the figure, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "04:32 → 04:40",
                "sujeito": "O cidadão passando por situações — o score caindo visivelmente após cada ação",
                "acao": "Série de três momentos: semáforo vermelho, prédio proibido, celular em local não autorizado — score caindo",
                "camera": "Medium tracking shot seguindo o cidadão, câmera andando junto",
                "iluminacao": "O número flutuante vai de dourado para laranja para vermelho à medida que cai",
                "estilo": "Dystopian social scoring nightmare",
                "atmosfera": "O ambiente P&B se escurece conforme o score cai",
                "mood": "Perda progressiva de status, o sistema punindo invisível e automaticamente",
                "continuity": "Seguindo o cidadão do clipe anterior em seu percurso deteriorando",
                "prompt": "Medium tracking shot following a citizen through a black and white urban environment — three sequential moments shown in the same continuous shot: they step past a red light (score number above their head drops and shifts from golden to orange), they open a door marked with a restriction (score drops further, number shifts orange to red), they check their phone in a designated no-phone zone (score plummets to a low red number). The floating score number above their head transitions from warm gold through orange to alarming blood red as it decreases. Nearby surveillance cameras swivel to follow each infraction automatically. Tracking camera moves with the citizen. 35mm grain, dystopian scoring visualization, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "04:40 → 04:48",
                "sujeito": "O cidadão diante de terminal de embarque — pontuação vermelha — barreira fechando",
                "acao": "O scanner lê o score vermelho, a barreira fecha automaticamente, o cidadão para diante dela",
                "camera": "Medium shot frontal do cidadão e da barreira, câmera estática",
                "iluminacao": "A barreira iluminada em vermelho sangue ao fechar; cidadão em sombra fria",
                "estilo": "Point of exclusion, economic embargo made physical",
                "atmosfera": "Outros passageiros em P&B passam pelas barreiras abertas; apenas a deste cidadão fecha",
                "mood": "Exclusão física do sistema, Apocalipse 13 em metal e vidro moderno",
                "continuity": "Consequência direta da queda de pontuação do clipe anterior",
                "prompt": "Medium static frontal shot of a citizen attempting to pass through a transit barrier — a sleek modern turnstile with glass panels. A scanner reads their low red social score (the floating red number above their head is now visibly low). The barrier slams shut with a red warning light flooding the entire structure and the citizen's face. They stop short, hands slightly raised. Other passengers in black and white around them pass freely through open barriers. The citizen stands alone before the closed red-lit barrier. Their face is lit in red from below. The exclusion is absolute and mechanical. 35mm grain, economic embargo made physical, no text, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V13", "titulo": "CONVERGÊNCIA 666",
        "timestamp": "04:48 → 05:12",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "04:48 → 04:56",
                "sujeito": "Cinco fontes de dados separadas — moeda digital, olho biométrico, câmera, chip, QR code",
                "acao": "Wide shot mostra os cinco símbolos flutuando separadamente, cada um pulsando com cor própria",
                "camera": "Wide establishing shot com os 5 elementos separados, câmera lentamente recuando",
                "iluminacao": "Cada símbolo com cor própria — dourado, azul, vermelho, verde, branco",
                "estilo": "Data visualization surrealism, prophetic convergence",
                "atmosfera": "Linhas tênues de conexão entre os símbolos já se formando",
                "mood": "Cinco sistemas independentes prestes a se unir",
                "continuity": None,
                "prompt": "Wide establishing shot of a dark digital void space containing five separate floating symbolic icons, each pulsing with its own distinct light: a golden digital currency coin (monetary control), a blue biometric eye iris (identity verification), a red surveillance camera (monitoring), a green microchip with circuit traces (physical implant), a white QR code (digital identity). They float at equal distances from each other, each with connecting data streams beginning to form between them like spider silk in the void. Camera slowly pulls back to reveal all five simultaneously. Faint energy between them. 35mm grain, prophetic convergence aesthetic, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "04:56 → 05:04",
                "sujeito": "Os cinco fluxos de dados se movendo uns em direção aos outros, acelerando",
                "acao": "Os cinco símbolos começam a se mover em direção a um ponto central, acelerando",
                "camera": "Medium shot do ponto central onde a convergência ocorrerá, câmera estática",
                "iluminacao": "As cores fundindo-se em espiral de luz branca-vermelha no centro",
                "estilo": "Cosmic convergence horror, apocalyptic data fusion",
                "atmosfera": "Velocidade dos dados aumentando dramaticamente; símbolos se fragmentando",
                "mood": "Inevitabilidade, as peças do sistema finalmente se unindo",
                "continuity": "Os cinco elementos do clipe anterior agora em movimento convergente",
                "prompt": "Medium static shot of a central point in digital void space where five data streams are converging at increasing velocity — the golden monetary stream, the blue biometric stream, the red surveillance stream, the green chip stream, and the white identity stream spiraling inward simultaneously. As they approach the center, they begin to fragment and intermingle, their colors blending into a white-red energy spiral. The five original symbols are barely recognizable, dissolving into pure data flow. The convergence spiral grows brighter and more violent. The center point pulses. 35mm grain, cosmic convergence horror, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "05:04 → 05:12",
                "sujeito": "O ponto de convergência — os cinco fluxos formando o número 666 em energia pura",
                "acao": "Os fluxos colidem e a energia forma organicamente '666' em luz vermelha sangue pulsante; depois escuridão total",
                "camera": "Extreme close-up do ponto de convergência, câmera absolutamente estática",
                "iluminacao": "A formação do 666 ilumina tudo em vermelho sangue; depois escuridão total",
                "estilo": "Prophetic horror climax, number as revelation",
                "atmosfera": "Os dados que formam o número têm textura de pele e código ao mesmo tempo",
                "mood": "Revelação profética do sistema completo, o número do Apocalipse materializado em dados modernos",
                "continuity": "A convergência dos 5 fluxos resulta na formação do número",
                "prompt": "Extreme close-up static shot of a central convergence point in digital void — the five data streams crash together and their combined energy organically forms the number 666 in pulsing blood-red light, the digits constructed from living data streams rather than fonts — each digit made of flowing binary code, circuit traces, and pulsing vein-like lines. The 666 holds for a moment, pulsing with intense crimson light that floods the entire frame red. Then a single final pulse — maximum brightness — and total darkness. The number was never 'placed' there, it emerged from the collision of the five modern systems. Static ECU, one held frame then black. 35mm grain, prophetic horror climax, no text beyond the emergent number, no watermark. 8 seconds."
            },
        ]
    },
    {
        "id": "V14", "titulo": "HORIZONTE APOCALÍPTICO / CONCLUSÃO",
        "timestamp": "05:12 → 05:36",
        "clipes": [
            {
                "num": 1, "nome": "ESTABELECER", "ts": "05:12 → 05:20",
                "sujeito": "Horizonte vasto — planície ou costa com sol vermelho baixo, céu dramático",
                "acao": "Ultra wide shot revela o horizonte com sol vermelho sangue descendo, nuvens em tons de brasa",
                "camera": "Ultra wide establishing shot, câmera absolutamente estática",
                "iluminacao": "Sol vermelho como único ponto de cor intensa; terra em P&B",
                "estilo": "Apocalyptic landscape cinema, Terrence Malick contemplative epic",
                "atmosfera": "Poeira fina, cinzas flutuando, silêncio absoluto",
                "mood": "Peso do tempo, presença do eterno, beleza e terror simultâneos",
                "continuity": None,
                "prompt": "Ultra-wide establishing shot of a vast desolate landscape at dusk — flat plain or coastal terrain stretching to a distant horizon where a blood-red sun hangs low, enormous and saturated, the only intense color in the frame. The sky around it gradients through deep orange and crimson to near-black at the zenith — all in vivid color. The ground, any vegetation, and distant structures are in black and white desaturation. Fine dust and floating ash particles visible in the low light rays. Absolute stillness — no movement except drifting ash. Static camera. Terrence Malick contemplative epic aesthetic. The weight of eternity. 35mm grain, apocalyptic landscape, no text, no watermark. 8 seconds."
            },
            {
                "num": 2, "nome": "APROXIMAR", "ts": "05:20 → 05:28",
                "sujeito": "Silhueta solitária humana — em pé no horizonte, diante do sol vermelho",
                "acao": "A câmera lentamente avança em direção à silhueta que permanece imóvel diante do sol",
                "camera": "Medium shot se aproximando devagar da silhueta, dolly in cinematográfico",
                "iluminacao": "Silhueta em contraluz P&B; sol vermelho rimlight nas bordas em vermelho",
                "estilo": "Existential contemplation, prophetic solitude",
                "atmosfera": "Vento leve movendo as roupas da silhueta; cinzas passando pela frente da câmera",
                "mood": "Escolha diante do Apocalipse, solidão humana face ao profético",
                "continuity": "A câmera descobre que o horizonte do clipe anterior não estava vazio",
                "prompt": "Slow cinematic dolly-in medium shot approaching a solitary human silhouette standing alone on the vast desolate plain, facing the blood-red sun on the horizon — completely backlit, rendered as a pure black silhouette with the vivid crimson sun-glow rimming the edges of the figure like a halo of fire. The figure is absolutely still, arms at sides, looking toward the horizon. Slow ash particles drift in front of camera in soft-focus. The figure's complete stillness against the moving ash creates a powerful contrast. The approach is slow — we move toward the figure but it never turns. Existential confrontation with the prophetic horizon. 35mm grain, contemplative apocalyptic cinema, no text, no watermark. 8 seconds."
            },
            {
                "num": 3, "nome": "IMPACTAR", "ts": "05:28 → 05:36",
                "sujeito": "O sol vermelho no horizonte — dentro do disco solar, a visão de uma cidade de luz dourada",
                "acao": "ECU do sol vermelho — dentro do disco, visível como mirage, uma Jerusalém dourada e luminosa",
                "camera": "Extreme close-up do sol, câmera absolutamente estática",
                "iluminacao": "Sol em vermelho intenso ao redor; centro do disco solar em dourado puro",
                "estilo": "Prophetic surrealism, hope within judgment, Revelation 21 glimpsed through Revelation 13",
                "atmosfera": "O calor do sol distorce o ar; a cidade de luz dentro do disco vibra levemente",
                "mood": "Esperança distante mas real, o julgamento não é a última palavra",
                "continuity": "A câmera olha para onde a silhueta olha — o sol e o que está dentro",
                "prompt": "Extreme close-up static shot of the blood-red setting sun — the solar disc filling most of the frame, edges burning deep crimson, surface texture visible with solar activity. In the very center of the disc, through the intense heat haze and color, a faint but unmistakable golden city is visible as a mirage or vision — luminous golden architecture, towers and gates of radiant light, the New Jerusalem — glowing pure warm gold within the red fire of the surrounding sun. The center of judgment contains hope. The heat shimmer makes the city vibrate gently. Foreground: the sun in full red color. The inner city vision in vivid gold. Absolute stillness of the camera. This is Revelation 21 seen through Revelation 13. 35mm grain, prophetic surrealist climax, no text, no watermark. 8 seconds."
            },
        ]
    },
]


# ── Geração do PDF ────────────────────────────────────────────────────────────
def gerar_pdf():
    os.makedirs(LOCAL_DIR, exist_ok=True)
    styles = build_styles()

    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="Prompts de Vídeo Veo 3 — A Marca da Besta",
        author="Phantasma | Abismo Criativo",
    )

    story = []

    # ── CAPA ──────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.5*cm))
    story.append(HRFlowable(width="100%", thickness=3, color=VERMELHO))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("PROMPTS DE VÍDEO — VEO 3", styles['capa_title']))
    story.append(Paragraph("A Marca da Besta Já Está Sendo Implementada — Apocalipse 13", styles['capa_sub']))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=DOURADO))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Canal: Sinais do Fim — Passagens do Apocalipse", styles['capa_meta']))
    story.append(Paragraph("Vídeo: video-002-marca-da-besta", styles['capa_meta']))
    story.append(Paragraph("Agente: Phantasma | Abismo Criativo", styles['capa_meta']))
    story.append(Paragraph("Data: 2026-04-06", styles['capa_meta']))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("14 quadros VIDEO × 3 clipes Veo 3 = 42 clipes × 8s = ~336s de material bruto", styles['capa_meta']))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="100%", thickness=3, color=VERMELHO))
    story.append(Spacer(1, 0.8*cm))

    # ── LEGENDA DE ESTILO ─────────────────────────────────────────────────────
    story.append(Paragraph("REGRAS VISUAIS GLOBAIS", styles['section']))
    regras = [
        ["Foreground", "Bíblico COLORIDO (dourado, vermelho, medieval ilustrado)"],
        ["Background", "Mundo moderno PRETO E BRANCO desaturado"],
        ["Câmera", "Movimentos lentos e cinematográficos em todos os clipes"],
        ["Grain", "35mm film em 100% dos clipes"],
        ["Proibido", "Texto em tela, watermark, logotipos"],
        ["Arco", "V01-V02 Profecia | V03-V04 Besta/Marca | V05-V06 Histórico | V07-V10 Digital | V11-V13 Vigilância | V14 Conclusão"],
    ]
    t = Table(regras, colWidths=[3.5*cm, 12*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor("#F0E8D8")),
        ('TEXTCOLOR', (0, 0), (0, -1), VERMELHO),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('TEXTCOLOR', (1, 0), (1, -1), PRETO),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor("#FAFAFA"), HexColor("#F5F0E8")]),
        ('GRID', (0, 0), (-1, -1), 0.3, CINZA_CLARO),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))

    # ── QUADROS ───────────────────────────────────────────────────────────────
    ARCO_LABELS = {
        "V01": "INTRODUÇÃO", "V02": "INTRODUÇÃO",
        "V03": "ATO 1 — BASE BÍBLICA", "V04": "ATO 1 — BASE BÍBLICA",
        "V05": "ATO 2 — CONTEXTO HISTÓRICO", "V06": "ATO 2 — CONTEXTO HISTÓRICO",
        "V07": "ATO 3 — CBDC + CHIP", "V08": "ATO 3 — CBDC + CHIP",
        "V09": "ATO 3 — CBDC + CHIP", "V10": "ATO 3 — CBDC + CHIP",
        "V11": "ATO 4 — VIGILÂNCIA", "V12": "ATO 4 — VIGILÂNCIA",
        "V13": "ATO 4 — VIGILÂNCIA", "V14": "CONCLUSÃO",
    }

    prev_arco = ""
    for quadro in QUADROS:
        arco = ARCO_LABELS.get(quadro["id"], "")
        if arco != prev_arco:
            story.append(Paragraph(arco, styles['section']))
            story.append(HRFlowable(width="100%", thickness=0.5, color=VERMELHO))
            story.append(Spacer(1, 0.2*cm))
            prev_arco = arco

        header_text = f"QUADRO {quadro['id']} — {quadro['titulo']}  |  VIDEO — Veo 3  |  {quadro['timestamp']}  |  24s"
        story.append(Paragraph(header_text, styles['quadro_header']))

        for clipe in quadro['clipes']:
            block = []

            clipe_text = f"CLIPE {clipe['num']} — {clipe['nome']}  ({clipe['ts']})"
            block.append(Paragraph(clipe_text, styles['clipe_label']))

            fields = [
                ("SUJEITO", clipe['sujeito']),
                ("AÇÃO", clipe['acao']),
                ("CÂMERA", clipe['camera']),
                ("ILUMINAÇÃO", clipe['iluminacao']),
                ("ESTILO", clipe['estilo']),
                ("ATMOSFERA", clipe['atmosfera']),
                ("MOOD", clipe['mood']),
                ("DURAÇÃO", "8 segundos"),
            ]
            if clipe.get('continuity'):
                fields.append(("CONTINUITY", clipe['continuity']))

            for key, val in fields:
                block.append(Paragraph(key + ":", styles['field_key']))
                block.append(Paragraph(val, styles['field_val']))

            block.append(Paragraph("PROMPT:", styles['field_key']))
            block.append(Paragraph(clipe['prompt'], styles['prompt']))

            story.append(KeepTogether(block))

        story.append(Spacer(1, 0.3*cm))

    # ── SUMÁRIO ───────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=2, color=VERMELHO))
    story.append(Paragraph("SUMÁRIO DE PRODUÇÃO", styles['section']))
    sumario_data = [
        ["Total de quadros VIDEO:", "14"],
        ["Total de clipes Veo 3:", "42"],
        ["Duração total de material bruto:", "~336 segundos (5 min 36s)"],
        ["Duração estimada no vídeo (40%):", "~6 minutos dos 15:30 totais"],
        ["Arco V01-V02:", "Profecia e texto (antigo, sagrado)"],
        ["Arco V03-V04:", "Besta e marca (bíblico, horror)"],
        ["Arco V05-V06:", "Paralelos históricos (épico, reforma)"],
        ["Arco V07-V10:", "Sistema digital moderno (tecnológico, distópico)"],
        ["Arco V11-V13:", "Vigilância e convergência (horror, acumulativo)"],
        ["Arco V14:", "Conclusão e esperança (contemplativo, transcendente)"],
    ]
    for row in sumario_data:
        story.append(Paragraph(
            f'<b><font color="#8B0000">{row[0]}</font></b> {row[1]}',
            styles['sumario']
        ))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=3, color=VERMELHO))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("FIM — PHANTASMA | ABISMO CRIATIVO", styles['capa_sub']))
    story.append(Paragraph("Canal: Sinais do Fim | video-002-marca-da-besta | 2026-04-06", styles['capa_meta']))

    doc.build(story)
    print(f"[OK] PDF gerado: {PDF_PATH}")


# ── Upload VPS ────────────────────────────────────────────────────────────────
def upload_vps():
    print(f"[...] Conectando à VPS {VPS_HOST}...")
    try:
        key = paramiko.Ed25519Key.from_private_key_file(KEY_PATH)
    except Exception as e:
        print(f"[ERRO] Chave SSH: {e}")
        return False

    try:
        transport = paramiko.Transport((VPS_HOST, VPS_PORT))
        transport.connect(username=VPS_USER, pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Garantir que o diretório existe (criação recursiva)
        parts = VPS_DIR.split("/")
        current = ""
        for part in parts:
            if not part:
                current = "/"
                continue
            current = current.rstrip("/") + "/" + part
            try:
                sftp.stat(current)
            except FileNotFoundError:
                try:
                    sftp.mkdir(current)
                    print(f"[DIR] Criado: {current}")
                except Exception:
                    pass

        sftp.put(PDF_PATH, VPS_REMOTE)
        sftp.close()
        transport.close()
        print(f"[OK] Upload concluído: {VPS_REMOTE}")
        print(f"[URL] {URL_PDF}")
        return True
    except Exception as e:
        print(f"[ERRO] Upload VPS: {e}")
        return False


# ── Log ───────────────────────────────────────────────────────────────────────
def registrar_log(upload_ok):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] PHANTASMA — 14 quadros VIDEO, 42 clipes Veo 3 gerados → prompts_video.pdf\n")
        if upload_ok:
            f.write(f"[{ts}] LINK — {URL_PDF}\n")
        else:
            f.write(f"[{ts}] PHANTASMA — Upload VPS falhou, arquivo salvo localmente em {PDF_PATH}\n")
    print(f"[OK] Log registrado: {LOG_PATH}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("PHANTASMA — Gerador de Prompts de Vídeo Veo 3")
    print("video-002-marca-da-besta | Abismo Criativo")
    print("=" * 60)

    gerar_pdf()
    upload_ok = upload_vps()
    registrar_log(upload_ok)

    print("=" * 60)
    if upload_ok:
        print(f"ENTREGA CONCLUÍDA")
        print(f"PDF local : {PDF_PATH}")
        print(f"URL VPS   : {URL_PDF}")
    else:
        print(f"PDF gerado localmente (upload pendente)")
        print(f"PDF local : {PDF_PATH}")
    print("=" * 60)
