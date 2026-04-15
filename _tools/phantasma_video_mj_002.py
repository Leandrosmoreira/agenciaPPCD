#!/usr/bin/env python3
"""
PHANTASMA — Gera prompts_video_mj.txt
Formato: instrucoes Midjourney Animate (Start Frame + End Frame + Motion)
14 quadros x 2 clips = 28 instrucoes
Canal: Sinais do Fim | Video: video-002-marca-da-besta
"""

import os
import paramiko
from datetime import datetime

# --- Configuracoes fixas -------------------------------------------------------
SREF_URL   = "https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png"
MJ_PARAMS  = "--ar 16:9 --style raw --v 7 --q 2 --stylize 750"
SREF_PARAM = f"--sref {SREF_URL} --sw 750"
NEGATIVE   = "--no text, watermark, logo, anime, cartoon, blurry, low quality"
SEED_BASE  = 847300

LOCAL_DIR  = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\5-prompts"
TXT_OUT    = os.path.join(LOCAL_DIR, "prompts_video_mj.txt")
LOG_PATH   = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log"

VPS_HOST   = "31.97.165.64"
VPS_PORT   = 22
VPS_USER   = "root"
KEY_PATH   = os.path.expanduser("~/.ssh/id_ed25519")
VPS_REMOTE = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/prompts_video_mj.txt"
TXT_URL    = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/prompts_video_mj.txt"


# --- Dados dos 14 quadros ------------------------------------------------------
# Cada entrada: (v_num, timecode, titulo, goetia_ref, clip_a, clip_b)
# clip_a / clip_b: (end_frame_prompt, motion, animation_prompt, mood, camera)

QUADROS = [
    {
        "v": 1,
        "timecode": "00:00-00:10",
        "titulo": "PATMOS / JOAO ESCREVENDO",
        "goetia": "Q01",
        "goetia_desc": 'Abertura: Joao em Patmos',
        "clip_a": {
            "end_frame": (
                "colorful vivid elderly apostle in crimson and gold robe writing on parchment scroll "
                "on rocky clifftop foreground, black and white stormy sea of Patmos island in background, "
                "chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, "
                "35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Wide camera slowly pulling back from elderly apostle, revealing rocky island coastline, robe fabric rippling in wind, feather quill scratching parchment, dark storm waves crashing in background",
            "mood": "Solitude and divine calling",
            "camera": "Slow pull back wide reveal",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid golden light pulsing on open parchment scroll with ancient Greek text "
                "in extreme foreground, black and white rocky cliff and apostle silhouette in background, "
                "chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, "
                "35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Camera slowly zooming in toward scroll resting on rock, golden light emanating from the written words, letters glowing with divine energy, sea wind causing scroll edges to flutter",
            "mood": "Sacred revelation",
            "camera": "Slow zoom in toward scroll",
        },
    },
    {
        "v": 2,
        "timecode": "00:24-00:34",
        "titulo": "PERGAMINHO APOCALIPTICO",
        "goetia": "Q02",
        "goetia_desc": "Pergaminho com caligrafia de Ap 13",
        "clip_a": {
            "end_frame": (
                "colorful vivid illuminated parchment scroll unfurling slowly in foreground, "
                "ancient apocalyptic calligraphy glowing gold, black and white gothic altar with "
                "candelabras in background, chiaroscuro dramatic lighting from above, fire glow and "
                "floating orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Parchment scroll slowly unfurling downward revealing ancient text, multiple candle flames flickering in synchrony, melted wax dripping in slow motion, candlelight casting warm shadows on gothic stonework",
            "mood": "Solemn prophecy",
            "camera": "Static",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid close-up of ancient apocalyptic text glowing crimson on parchment "
                "in extreme foreground, black and white binary code matrix cascading in background, "
                "candle flames growing taller, chiaroscuro dramatic lighting from above, fire glow and "
                "floating orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "High",
            "animation_prompt": "Camera slowly zooming into the parchment text, candle flames growing taller and brighter, binary code digits materializing like rain in the dark background, golden letters on scroll pulsing with red energy",
            "mood": "Apocalyptic revelation connecting ancient and modern",
            "camera": "Slow zoom in",
        },
    },
    {
        "v": 3,
        "timecode": "00:48-00:58",
        "titulo": "BESTA DO MAR",
        "goetia": "Q08",
        "goetia_desc": "Besta de 7 cabecas emergindo do mar",
        "clip_a": {
            "end_frame": (
                "colorful vivid seven-headed sea beast with golden and crimson scales rising from "
                "crashing ocean waves in foreground, black and white stormy tempestuous sky with "
                "lightning in background, chiaroscuro dramatic lighting from above, fire glow and "
                "floating orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "High",
            "animation_prompt": "Wide camera revealing massive seven-headed beast rising from ocean, enormous waves breaking and spraying, thunderbolts illuminating black and white storm clouds in background, golden scales gleaming with crimson fire glow",
            "mood": "Terrifying cosmic revelation",
            "camera": "Wide slow pull back revealing full beast scale",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid seven-headed beast at full height dominating foreground, all seven "
                "heads roaring open-mouthed, golden and crimson scales blazing, black and white "
                "apocalyptic sky raining embers in background, chiaroscuro dramatic lighting from above, "
                "fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "High",
            "animation_prompt": "Camera craning upward slowly to show full vertical scale of the beast, all seven heads roaring simultaneously, burning embers falling from stormy sky, ocean churning violently below, beast casting shadow over entire scene",
            "mood": "Overwhelming supernatural terror",
            "camera": "Crane up slowly",
        },
    },
    {
        "v": 4,
        "timecode": "01:12-01:22",
        "titulo": "MAO RECEBENDO A MARCA",
        "goetia": "Q19",
        "goetia_desc": "Mao com marca — secao CBDC",
        "clip_a": {
            "end_frame": (
                "colorful vivid human right hand palm up in extreme foreground, modern microsyringe "
                "descending in slow motion toward skin, black and white sterile laboratory with medical "
                "equipment in background, chiaroscuro dramatic lighting from above, fire glow and "
                "floating orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Static macro close-up of hand with syringe descending in extreme slow motion, air droplets on needle tip catching light, hand skin texture revealed, background laboratory completely desaturated and blurred",
            "mood": "Dread and inevitability",
            "camera": "Static close-up macro",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid extreme macro of needle touching human skin in foreground, crimson "
                "bioluminescent pulse spreading under translucent skin, microscopic RFID chip circuit "
                "pattern visible beneath skin surface, black and white sterile lab in background, "
                "chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, "
                "35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Extreme static macro of needle tip touching skin, crimson red bioluminescent pulse radiating outward under skin like veins of light, microchip circuit pattern illuminating beneath translucent skin tissue",
            "mood": "Horror and violation",
            "camera": "Extreme close-up static",
        },
    },
    {
        "v": 5,
        "timecode": "01:36-01:46",
        "titulo": "ROMA IMPERIAL",
        "goetia": "Q03",
        "goetia_desc": "Roma vs Modernidade",
        "clip_a": {
            "end_frame": (
                "colorful vivid Roman imperial procession in crimson and gold togas marching in "
                "foreground, black and white Colosseum ruins and Roman forum in background, "
                "chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, "
                "35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "High angle wide shot of Roman procession advancing toward viewer, camera slowly descending from bird's eye view to eye level, golden standards catching light, togas billowing, sandals striking stone pavement",
            "mood": "Imperial authority and ancient power",
            "camera": "Slow descend from high angle",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid Roman merchant presenting libellus document to armored soldier in "
                "medium foreground, golden sunlight casting dramatic diagonal shadow of authority, "
                "black and white forum and crowd in background, chiaroscuro dramatic lighting from above, "
                "fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Static medium shot of merchant handing compliance document to soldier, golden afternoon light creating long dramatic shadows across stone tiles, crowd frozen in watchful silence in background",
            "mood": "Submission to earthly authority",
            "camera": "Static medium",
        },
    },
    {
        "v": 6,
        "timecode": "02:00-02:10",
        "titulo": "LUTERO E REFORMADORES",
        "goetia": "Q13",
        "goetia_desc": "Lutero — contexto da Reforma",
        "clip_a": {
            "end_frame": (
                "colorful vivid Martin Luther in black Augustinian habit preaching from cathedral "
                "steps holding Bible aloft in foreground, black and white crowd of medieval townspeople "
                "in background, chiaroscuro dramatic lighting from above, fire glow and floating orange "
                "ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Wide shot slowly pushing in toward Luther preaching, papers and pamphlets swirling in wind around his feet, dramatic sidelight on his raised Bible, crowd shifting and murmuring in desaturated background",
            "mood": "Defiant spiritual courage",
            "camera": "Slow push in wide to medium",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid extreme macro of Luther's hand holding iron nail against wooden "
                "cathedral door in foreground, hammer descending in slow motion, 95 Theses parchment "
                "visible at edge of frame, black and white stone cathedral facade in background, "
                "chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, "
                "35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Extreme macro static shot of nail being driven into cathedral door in slow motion, wood grain fibers splitting under iron nail tip, parchment document pinned beneath, splinters catching golden light",
            "mood": "Historic turning point",
            "camera": "Extreme macro static",
        },
    },
    {
        "v": 7,
        "timecode": "02:24-02:34",
        "titulo": "MAPA CBDC / 134 PAISES",
        "goetia": "Q21",
        "goetia_desc": "Mapa CBDC global",
        "clip_a": {
            "end_frame": (
                "colorful vivid holographic 3D world map floating in dark digital void in foreground, "
                "countries beginning to illuminate in crimson red progressively, data streams flowing "
                "between nations, black and white server infrastructure in background, chiaroscuro "
                "dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, "
                "anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Wide shot slowly pulling back from holographic world map, countries activating in red one by one like spreading fire, golden data lines connecting central banking nodes, entire map pulsing with ominous energy",
            "mood": "Global surveillance and control spreading",
            "camera": "Slow pull back",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid holographic world map nearly fully crimson red pulsing like living "
                "heart in foreground, red data streams and financial control lines connecting all "
                "continents, black and white earth sphere below, chiaroscuro dramatic lighting from "
                "above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "High",
            "animation_prompt": "Camera slowly pushing through the holographic map surface, crimson red pulse spreading to final remaining nations, map breathing like a living organism, golden financial data streams accelerating to maximum speed",
            "mood": "Total global financial control achieved",
            "camera": "Slow push in through map",
        },
    },
    {
        "v": 8,
        "timecode": "02:48-02:58",
        "titulo": "CHIP IMPLANTAVEL",
        "goetia": "Q24",
        "goetia_desc": "Chip e microagulha",
        "clip_a": {
            "end_frame": (
                "colorful vivid surgical steel tray with microsyringe and RFID microchip in foreground, "
                "gloved hand positioning needle with clinical precision, black and white sterile operating "
                "room in background, chiaroscuro dramatic lighting from above, fire glow and floating "
                "orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Overhead camera slowly descending toward surgical tray revealing instruments one by one, gloved hand picking up microsyringe with deliberate precision, harsh surgical light creating deep shadows around tools",
            "mood": "Clinical inevitability and surveillance",
            "camera": "Overhead descend",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid extreme macro of RFID microchip suspended in clear liquid inside "
                "syringe tube in foreground, chip circuits glowing like miniature golden city grid, "
                "black and white sterile background dissolved in bokeh, chiaroscuro dramatic lighting "
                "from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Extreme macro zoom through liquid medium toward chip surface, microscopic circuit pathways illuminating gold and red, liquid refracting light into prismatic patterns, chip circuits pulsing like a tiny heartbeat",
            "mood": "Technology as spiritual threat",
            "camera": "Extreme macro zoom through liquid",
        },
    },
    {
        "v": 9,
        "timecode": "03:12-03:22",
        "titulo": "TRANSACAO BLOQUEADA",
        "goetia": "Q28",
        "goetia_desc": "Vigilancia e exclusao economica",
        "clip_a": {
            "end_frame": (
                "colorful vivid person at supermarket checkout counter attempting payment in foreground, "
                "payment terminal screen flashing ACCESS DENIED in crimson red, person's face just "
                "beginning to register shock, black and white supermarket aisles with other shoppers "
                "in background, chiaroscuro dramatic lighting from above, fire glow and floating orange "
                "ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Static wide surveillance-style shot of checkout lane, person sliding card through terminal, machine suddenly emitting red denial light that bathes the person's face, other shoppers in black and white background turning to stare",
            "mood": "Social exclusion and economic exile",
            "camera": "Static wide surveillance aesthetic",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid extreme close-up of person's face illuminated entirely by crimson red "
                "denial screen light in foreground, expression of realization and horror, tears forming, "
                "black and white supermarket crowd blurred in background, chiaroscuro dramatic lighting "
                "from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Camera slowly zooming in from medium to extreme close-up of person's face, red terminal light painting their features in crimson, micro-expressions of disbelief and terror, background crowd slowly turning in judgment",
            "mood": "Existential horror of exclusion",
            "camera": "Slow zoom in to face",
        },
    },
    {
        "v": 10,
        "timecode": "03:36-03:46",
        "titulo": "CAMERA DE VIGILANCIA",
        "goetia": "Q29",
        "goetia_desc": "Cameras de vigilancia",
        "clip_a": {
            "end_frame": (
                "colorful vivid matte black security camera in extreme foreground slowly rotating on "
                "its mount, red recording LED pulsing, black and white city street with tiny monitored "
                "citizens below in background, chiaroscuro dramatic lighting from above, fire glow and "
                "floating orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Camera slowly orbiting around the security camera dome, surveillance device tracking smoothly on its gimbal, red LED blinking rhythmically, city below rendered in black and white scale showing full scope of monitoring",
            "mood": "Omniscient surveillance state",
            "camera": "Slow orbit around surveillance camera",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid fisheye POV from inside security camera lens looking down at street "
                "in foreground, wide-angle distorted view of pedestrians, crimson red digital crosshair "
                "reticle and biometric scan lines overlaid, black and white city in background, "
                "chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, "
                "35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Fisheye lens POV of surveillance camera rotating field of view, crimson targeting reticles locking on to individual pedestrians, biometric data readouts flickering alongside each person, all citizens reduced to data points",
            "mood": "Loss of anonymity and freedom",
            "camera": "Fisheye lens POV",
        },
    },
    {
        "v": 11,
        "timecode": "04:00-04:10",
        "titulo": "REDE NEURAL / IA CONTROLANDO",
        "goetia": "Q30",
        "goetia_desc": "IA e rede neural de controle",
        "clip_a": {
            "end_frame": (
                "colorful vivid vast holographic neural network expanding through digital space in "
                "foreground, crimson red pulsing nodes connected by golden data streams, surveillance "
                "camera icons and financial institution symbols at each node, black and white globe "
                "in background, chiaroscuro dramatic lighting from above, fire glow and floating orange "
                "ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "High",
            "animation_prompt": "Wide shot slowly pulling back to reveal full scale of AI neural network spanning globe, data pulses traveling along golden connection lines at light speed, new nodes continuously activating, network growing exponentially",
            "mood": "Incomprehensible scale of AI control",
            "camera": "Slow pull back revealing scale",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid extreme close-up of central pulsing crimson node at heart of neural "
                "network in foreground, millions of data streams flowing inward like rivers of light, "
                "node beating like a heart, black and white network branches extending to infinity in "
                "background, chiaroscuro dramatic lighting from above, fire glow and floating orange "
                "ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "High",
            "animation_prompt": "Camera zooming slowly into central control node, data rivers accelerating inward, node pulsing with increasing intensity like a digital heart, the weight of all global surveillance compressed into this single point",
            "mood": "Total control centralized in one system",
            "camera": "Slow zoom into central node",
        },
    },
    {
        "v": 12,
        "timecode": "04:24-04:34",
        "titulo": "CLAMOR / TESTEMUNHO",
        "goetia": "Q33",
        "goetia_desc": "Profeta e testemunho final",
        "clip_a": {
            "end_frame": (
                "colorful vivid prophet in crimson robe with arms raised holding apocalyptic scroll "
                "toward sky in foreground, black and white storm clouds gathering and swirling rapidly "
                "in background, chiaroscuro dramatic lighting from above, fire glow and floating orange "
                "ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Wide shot craning upward slowly as prophet raises arms higher, storm clouds in background accelerating their rotation, scroll text illuminating gold in the wind, robe fabric whipping dramatically",
            "mood": "Prophetic urgency and divine calling",
            "camera": "Slow crane up",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid extreme close-up of prophet's face illuminated by golden divine light "
                "streaming from above in foreground, eyes closed in prayer and surrender, single tear "
                "catching golden light on cheek, black and white burning sky in background, chiaroscuro "
                "dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, "
                "anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Camera slowly dollying in toward prophet's face, divine golden light intensifying from above, eyelashes trembling in wind, tear slowly forming and rolling down cheek catching warm light, expression of complete surrender",
            "mood": "Sacred surrender and divine peace",
            "camera": "Slow dolly in to face",
        },
    },
    {
        "v": 13,
        "timecode": "04:48-04:58",
        "titulo": "SELOS ABERTOS / JULGAMENTO",
        "goetia": "Q11",
        "goetia_desc": "Cordeiro com 7 Selos",
        "clip_a": {
            "end_frame": (
                "colorful vivid golden white Lamb of God standing on celestial altar with seven "
                "wax seals in foreground, first seal cracking and golden light exploding outward, "
                "black and white apocalyptic celestial throne room in background, chiaroscuro dramatic "
                "lighting from above, fire glow and floating orange ash embers, 35mm film grain, "
                "anamorphic lens flares"
            ),
            "motion": "High",
            "animation_prompt": "Camera slowly pushing in toward the Lamb on the altar, first seal dramatically cracking apart in slow motion, golden light burst emanating from broken seal, heavenly choir of light rays radiating outward",
            "mood": "Divine judgment unleashed",
            "camera": "Slow push in",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid extreme macro of apocalyptic wax seal exploding apart in slow motion "
                "in foreground, crimson red wax fragments flying outward, golden divine light pouring "
                "through the breach, Lamb silhouette visible through golden light, black and white "
                "celestial background, chiaroscuro dramatic lighting from above, fire glow and floating "
                "orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "High",
            "animation_prompt": "Extreme macro static shot of wax seal breaking in ultra slow motion, individual wax crystals tumbling in zero gravity, golden light spilling through crack and expanding, divine energy materializing as the seal falls away",
            "mood": "The moment of cosmic judgment",
            "camera": "Extreme macro static",
        },
    },
    {
        "v": 14,
        "timecode": "05:12-05:22",
        "titulo": "CONCLUSAO / CHAMADO",
        "goetia": "Q35",
        "goetia_desc": "Conclusao e chamado final",
        "clip_a": {
            "end_frame": (
                "colorful vivid golden divine light breaking through parting storm clouds and "
                "descending in radiant beams in foreground, silhouette of kneeling figure in crimson "
                "robe at center, black and white city skyline below in background, chiaroscuro dramatic "
                "lighting from above, fire glow and floating orange ash embers, 35mm film grain, "
                "anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Wide shot slowly tilting upward from black and white city below to golden sky above, divine light beams breaking through clouds and intensifying, kneeling figure's crimson robe glowing warmer as light descends",
            "mood": "Hope and divine invitation",
            "camera": "Slow tilt up from city to sky",
        },
        "clip_b": {
            "end_frame": (
                "colorful vivid dramatic crane shot revealing full panorama — golden divine light "
                "from above meeting black and white city below, solitary crimson-robed figure kneeling "
                "at center as axis between heaven and earth, chiaroscuro dramatic lighting from above, "
                "fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares"
            ),
            "motion": "Low",
            "animation_prompt": "Dramatic crane rising upward revealing full scale composition — divine light descending from above, city extending to horizon below, lone figure in crimson at the axis point, everything converging toward this moment of decision",
            "mood": "Final invitation and eternal consequence",
            "camera": "Dramatic crane up",
        },
    },
]


# --- Gerar TXT -----------------------------------------------------------------
def gerar_txt():
    os.makedirs(LOCAL_DIR, exist_ok=True)

    linhas = []

    # Cabecalho
    linhas.append("=" * 80)
    linhas.append("PROMPTS MIDJOURNEY ANIMATE — video-002-marca-da-besta")
    linhas.append("Canal: Sinais do Fim | Agencia: Abismo Criativo")
    linhas.append(f"Gerado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    linhas.append("Agente: PHANTASMA")
    linhas.append("Total: 14 quadros x 2 clips = 28 instrucoes")
    linhas.append("=" * 80)
    linhas.append("")
    linhas.append("INSTRUCOES GERAIS:")
    linhas.append("1. Para cada quadro, gere o End Frame via /imagine no Midjourney")
    linhas.append("2. Acesse Midjourney Web > Create > Animate")
    linhas.append("3. Carregue Start Frame + End Frame gerado")
    linhas.append("4. Configure Motion e Animation Prompt conforme indicado")
    linhas.append("5. Clip A e Clip B se encadeiam: End Frame de A vira Start Frame de B")
    linhas.append("")
    linhas.append(f"SREF aprovado: {SREF_URL}")
    linhas.append(f"Parametros fixos: {MJ_PARAMS}")
    linhas.append(f"SEED BASE: {SEED_BASE} (incremento +1 por clip)")
    linhas.append("")

    seed = SEED_BASE

    for q in QUADROS:
        v_num  = q["v"]
        seed_a = seed + 1
        seed_b = seed + 2
        seed   = seed_b

        separator = "=" * 80
        linhas.append(separator)
        linhas.append(f"QUADRO V{v_num:02d} -- [{q['timecode']}] -- {q['titulo']}")
        linhas.append(f"TOTAL: 10s | Clip A (5s) + Clip B (5s)")
        linhas.append(f"Referencia Goetia: {q['goetia']} -- \"{q['goetia_desc']}\"")
        linhas.append(separator)
        linhas.append("")

        # Clip A
        ca = q["clip_a"]
        linhas.append("--- CLIP A (00:00 - 00:05) ---")
        linhas.append(f"START FRAME -> {q['goetia']} da Goetia")
        linhas.append("Upload no Midjourney Web > Create > Start Frame")
        linhas.append("")
        linhas.append("END FRAME -- Gerar este /imagine e usar como End Frame:")
        mj_cmd_a = (
            f"/imagine prompt: {ca['end_frame']} "
            f"{MJ_PARAMS} "
            f"{SREF_PARAM} "
            f"--seed {seed_a} "
            f"{NEGATIVE}"
        )
        linhas.append(mj_cmd_a)
        linhas.append("")
        linhas.append(f"MOTION: {ca['motion']}")
        linhas.append(f"ANIMATION PROMPT: {ca['animation_prompt']}")
        linhas.append(f"MOOD: {ca['mood']}")
        linhas.append(f"CAMERA: {ca['camera']}")
        linhas.append("")

        # Clip B
        cb = q["clip_b"]
        linhas.append("--- CLIP B (00:05 - 00:10) ---")
        linhas.append("START FRAME -> End Frame do Clip A (a imagem gerada acima)")
        linhas.append("")
        linhas.append("END FRAME -- Gerar este /imagine e usar como End Frame:")
        mj_cmd_b = (
            f"/imagine prompt: {cb['end_frame']} "
            f"{MJ_PARAMS} "
            f"{SREF_PARAM} "
            f"--seed {seed_b} "
            f"{NEGATIVE}"
        )
        linhas.append(mj_cmd_b)
        linhas.append("")
        linhas.append(f"MOTION: {cb['motion']}")
        linhas.append(f"ANIMATION PROMPT: {cb['animation_prompt']}")
        linhas.append(f"MOOD: {cb['mood']}")
        linhas.append(f"CAMERA: {cb['camera']}")
        linhas.append("")

    # Rodape
    linhas.append("=" * 80)
    linhas.append("FIM DO ARQUIVO — PHANTASMA | ABISMO CRIATIVO")
    linhas.append(f"Seeds utilizados: {SEED_BASE + 1} a {SEED_BASE + 28}")
    linhas.append("=" * 80)

    conteudo = "\n".join(linhas)

    with open(TXT_OUT, "w", encoding="utf-8") as f:
        f.write(conteudo)

    total_chars = len(conteudo)
    print(f"[OK] TXT gerado: {TXT_OUT}")
    print(f"[INFO] 28 instrucoes, {total_chars} caracteres")
    return TXT_OUT


# --- Upload VPS ----------------------------------------------------------------
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

        # Garantir que o diretorio remoto existe
        remote_dir = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts"
        try:
            sftp.stat(remote_dir)
        except FileNotFoundError:
            # Criar diretorios recursivamente
            parts = remote_dir.split("/")
            path_acc = ""
            for part in parts:
                if not part:
                    continue
                path_acc += "/" + part
                try:
                    sftp.stat(path_acc)
                except FileNotFoundError:
                    sftp.mkdir(path_acc)

        sftp.put(txt_path, VPS_REMOTE)
        sftp.close()
        transport.close()
        print(f"[OK] Upload concluido!")
        print(f"[URL] {TXT_URL}")
        return True
    except Exception as e:
        print(f"[ERRO] Upload: {e}")
        try:
            transport.close()
        except Exception:
            pass
        return False


# --- Log -----------------------------------------------------------------------
def registrar_log(upload_ok):
    now    = datetime.now().strftime("%Y-%m-%d %H:%M")
    status = f"OK -> {TXT_URL}" if upload_ok else "FALHOU (salvo local)"
    linha  = (
        f"[{now}] PHANTASMA -- prompts_video_mj.txt gerado "
        f"(14 quadros x 2 clips = 28 instrucoes Midjourney Animate), upload {status}\n"
    )
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(linha)
    print(f"[OK] pipeline.log atualizado")


# --- Main ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("PHANTASMA -- Midjourney Animate | video-002-marca-da-besta")
    print("14 quadros x 2 clips = 28 instrucoes")
    print("=" * 60)

    txt_path  = gerar_txt()
    upload_ok = upload_vps(txt_path)
    registrar_log(upload_ok)

    print("=" * 60)
    if upload_ok:
        print("[CONCLUIDO] Disponivel em:")
        print(f"  {TXT_URL}")
    else:
        print("[CONCLUIDO] Salvo localmente em:")
        print(f"  {txt_path}")
    print("=" * 60)
