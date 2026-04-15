#!/usr/bin/env python3
"""
PIPELINE COMPLETO — 1 clip por cena
Imagem (Goetia) + Video (Phantasma) consolidados
"""

import os
import paramiko
from datetime import datetime

LOCAL_DIR = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-002-marca-da-besta\5-prompts"
TXT_OUT = os.path.join(LOCAL_DIR, "PIPELINE_COMPLETO.txt")
LOG_PATH = r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log"

VPS_HOST = "31.97.165.64"
VPS_PORT = 22
VPS_USER = "root"
KEY_PATH = os.path.expanduser("~/.ssh/id_ed25519")
VPS_REMOTE = "/opt/agencia/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/PIPELINE_COMPLETO.txt"
TXT_URL = "http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-002-marca-da-besta/5-prompts/PIPELINE_COMPLETO.txt"

CENAS = [
    {
        "quadro": "V01",
        "timestamp": "00:00-00:10",
        "titulo": "PATMOS / JOAO ESCREVENDO",
        "q": "Q01",
        "q_titulo": "Abertura: Joao em Patmos",
        "imagem_prompt": "Foreground: an elderly bearded prophet (John the Apostle) in richly colored medieval illuminated manuscript style -- crimson and ochre robes, hunched over a large parchment scroll on a rocky cliffside, holding a golden quill, face etched with terror and awe. Background: black and white stormy Aegean seascape, desaturated rocky cliffs, monochrome lightning bolts, a modern city skyline in grayscale with surveillance camera poles, storm clouds swirling. Add fire glow and floating ash particles. Strong contrast: vibrant medieval prophet versus monochrome apocalyptic modern world. Cinematic dramatic lighting, glowing golden highlights on the scroll, epic prophetic atmosphere medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847201 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid elderly apostle in crimson and gold robe writing on parchment scroll on rocky clifftop foreground, black and white stormy sea of Patmos island in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847301 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "Low",
        "animation_prompt": "Wide camera slowly pulling back from elderly apostle, revealing rocky island coastline, robe fabric rippling in wind, feather quill scratching parchment, dark storm waves crashing in background",
        "mood": "Solitude and divine calling",
        "camera": "Slow pull back wide reveal",
    },
    {
        "quadro": "V02",
        "timestamp": "00:24-00:34",
        "titulo": "PERGAMINHO APOCALIPTICO",
        "q": "Q02",
        "q_titulo": "Pergaminho com caligrafia de Ap 13",
        "imagem_prompt": "Foreground: an ancient parchment scroll dramatically unrolled, richly colored in medieval illuminated manuscript style -- crimson and gold ink calligraphy of Apocalipse 13, ornate borders with seven-headed serpents and golden fleur-de-lis, flames licking the parchment edges in deep red, burning golden candles flanking it. Background: black and white gothic stone altar, monochrome cathedral arches, ghost-like binary code floating desaturated in the air. Strong contrast between vibrant glowing parchment and monochrome stone environment. Cinematic lighting with dramatic shadows and glowing golden highlights medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847202 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid illuminated parchment scroll unfurling slowly in foreground, ancient apocalyptic calligraphy glowing gold, black and white gothic altar with candelabras in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847303 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "Low",
        "animation_prompt": "Parchment scroll slowly unfurling downward revealing ancient text, multiple candle flames flickering in synchrony, melted wax dripping in slow motion, candlelight casting warm shadows on gothic stonework",
        "mood": "Solemn prophecy",
        "camera": "Static",
    },
    {
        "quadro": "V03",
        "timestamp": "00:48-00:58",
        "titulo": "BESTA DO MAR",
        "q": "Q08",
        "q_titulo": "Besta de 7 cabecas emergindo do mar",
        "imagem_prompt": "Foreground: a devout Jewish man in rich medieval illuminated style -- ornate gold-and-blue prayer shawl, colorful tefilim boxes bound to right hand and forehead, face illuminated in warm golden prayer light, eyes closed in reverence. Background: black and white modern environment -- monochrome synagogue fading into a sterile lab, grayscale microchip implant diagrams overlapping the tefilim straps, desaturated digital screens. Fire glow and floating ash. Strong contrast: sacred colored ritual versus cold monochrome technology. Cinematic dramatic lighting medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847208 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid seven-headed sea beast with golden and crimson scales rising from crashing ocean waves in foreground, black and white stormy tempestuous sky with lightning in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847305 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "High",
        "animation_prompt": "Wide camera revealing massive seven-headed beast rising from ocean, enormous waves breaking and spraying, thunderbolts illuminating black and white storm clouds in background, golden scales gleaming with crimson fire glow",
        "mood": "Terrifying cosmic revelation",
        "camera": "Wide slow pull back revealing full beast scale",
    },
    {
        "quadro": "V04",
        "timestamp": "01:12-01:22",
        "titulo": "MAO RECEBENDO A MARCA",
        "q": "Q19",
        "q_titulo": "Mao com marca -- secao CBDC",
        "imagem_prompt": "Foreground: an elaborate medieval illuminated world mappamundi in vivid color -- 134 countries glowing in deep crimson and golden hues with radiating light, ornate medieval cartographic borders, sea monsters in painted oceans, biblical margin illustrations. Background: black and white digital global network -- monochrome fiber optic cables connecting the globe, desaturated satellite dishes, grayscale central bank architecture, dark network infrastructure. Strong contrast: vivid glowing medieval world map versus cold monochrome digital control grid. Cinematic dramatic lighting, pulsing crimson energy medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847219 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid human right hand palm up in extreme foreground, modern microsyringe descending in slow motion toward skin, black and white sterile laboratory with medical equipment in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847307 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "Low",
        "animation_prompt": "Static macro close-up of hand with syringe descending in extreme slow motion, air droplets on needle tip catching light, hand skin texture revealed, background laboratory completely desaturated and blurred",
        "mood": "Dread and inevitability",
        "camera": "Static close-up macro",
    },
    {
        "quadro": "V05",
        "timestamp": "01:36-01:46",
        "titulo": "ROMA IMPERIAL",
        "q": "Q03",
        "q_titulo": "Roma vs Modernidade",
        "imagem_prompt": "Foreground: ancient Rome in full vibrant color -- medieval illustration style depicting richly dressed Romans in scarlet and purple togas, golden laurel wreaths, marble columns, a centurion in gleaming bronze armor holding a Roman eagle standard, colorful market stalls. The vivid Roman scene merges with a seamless background in black and white: a modern city skyline of desaturated glass towers, highways, surveillance cameras, monochrome crowds. Fire and smoke transition between epochs. Dramatic cinematic lighting, strong contrast between vibrant antiquity and monochrome modernity. Epic surreal composition medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847203 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid Roman imperial procession in crimson and gold togas marching in foreground, black and white Colosseum ruins and Roman forum in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847309 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "Low",
        "animation_prompt": "High angle wide shot of Roman procession advancing toward viewer, camera slowly descending from bird's eye view to eye level, golden standards catching light, togas billowing, sandals striking stone pavement",
        "mood": "Imperial authority and ancient power",
        "camera": "Slow descend from high angle",
    },
    {
        "quadro": "V06",
        "timestamp": "02:00-02:10",
        "titulo": "LUTERO E REFORMADORES",
        "q": "Q13",
        "q_titulo": "Lutero -- contexto da Reforma",
        "imagem_prompt": "Foreground: Emperor Nero in vivid medieval illuminated illustration style -- deep purple and gold toga, golden laurel crown, holding a Roman coin bearing his profile, seated on an ornate golden throne with carved lions, imperious cruel expression. Background: black and white Colosseum -- monochrome Roman amphitheater ruins, a desaturated nuclear mushroom cloud rising on the horizon, grayscale Roman legions marching, dark storm sky. Strong contrast: richly colored imperial throne versus monochrome destruction. Cinematic dramatic lighting, fire glow, epic apocalyptic scale medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847213 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid Martin Luther in black Augustinian habit preaching from cathedral steps holding Bible aloft in foreground, black and white crowd of medieval townspeople in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847311 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "Low",
        "animation_prompt": "Wide shot slowly pushing in toward Luther preaching, papers and pamphlets swirling in wind around his feet, dramatic sidelight on his raised Bible, crowd shifting and murmuring in desaturated background",
        "mood": "Defiant spiritual courage",
        "camera": "Slow push in wide to medium",
    },
    {
        "quadro": "V07",
        "timestamp": "02:24-02:34",
        "titulo": "MAPA CBDC / 134 PAISES",
        "q": "Q21",
        "q_titulo": "Mapa CBDC global",
        "imagem_prompt": "Foreground: a powerful medieval authority figure representing global financial control -- richly detailed bishop-king in deep crimson robes with golden chain of office, holding a golden orb with interconnected rings symbolizing global banking, surrounded by golden seals and official documents, stern authoritative face. Background: black and white global banking institution -- monochrome imposing tower architecture, desaturated central bank imagery, grayscale international flags, dark institutional environment. Strong contrast: vivid golden authority figure versus cold monochrome financial institutions. Cinematic dramatic lighting medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847221 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid holographic 3D world map floating in dark digital void in foreground, countries beginning to illuminate in crimson red progressively, data streams flowing between nations, black and white server infrastructure in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847313 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "Low",
        "animation_prompt": "Wide shot slowly pulling back from holographic world map, countries activating in red one by one like spreading fire, golden data lines connecting central banking nodes, entire map pulsing with ominous energy",
        "mood": "Global surveillance and control spreading",
        "camera": "Slow pull back",
    },
    {
        "quadro": "V08",
        "timestamp": "02:48-02:58",
        "titulo": "CHIP IMPLANTAVEL",
        "q": "Q24",
        "q_titulo": "Chip e microagulha",
        "imagem_prompt": "Foreground: an ornate medieval Brazilian-themed illuminated coin in vivid color -- large glowing gold coin with Portuguese colonial baroque motifs, a crimson serpent coiling through the currency symbol, tropical birds and ornate decorative elements, radiating golden power. Background: black and white Brazilian digital banking -- monochrome central bank architecture, desaturated digital payment interface screens, grayscale DREX currency code streams, dark fintech environment. Strong contrast: vivid golden medieval coin versus cold monochrome digital banking. Cinematic dramatic lighting medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847224 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid surgical steel tray with microsyringe and RFID microchip in foreground, gloved hand positioning needle with clinical precision, black and white sterile operating room in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847315 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "Low",
        "animation_prompt": "Overhead camera slowly descending toward surgical tray revealing instruments one by one, gloved hand picking up microsyringe with deliberate precision, harsh surgical light creating deep shadows around tools",
        "mood": "Clinical inevitability and surveillance",
        "camera": "Overhead descend",
    },
    {
        "quadro": "V09",
        "timestamp": "03:12-03:22",
        "titulo": "TRANSACAO BLOQUEADA",
        "q": "Q28",
        "q_titulo": "Vigilancia e exclusao economica",
        "imagem_prompt": "Foreground: a medieval commoner figure in vivid illuminated illustration style -- colorful ochre and crimson robes, standing before a towering crimson forbidden seal, face showing shock and desperation, chains of golden numerals binding wrists, an open ledger of deeds. Background: black and white modern Chinese city -- monochrome skyscrapers, desaturated facial recognition screens, grayscale airport departure board with denial marks, dark authoritarian architecture. Strong contrast: vivid medieval human figure versus cold monochrome surveillance state. Cinematic dramatic lighting, crimson seal glow, ominous atmosphere medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847228 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid person at supermarket checkout counter attempting payment in foreground, payment terminal screen flashing ACCESS DENIED in crimson red, person's face just beginning to register shock, black and white supermarket aisles with other shoppers in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847317 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "Low",
        "animation_prompt": "Static wide surveillance-style shot of checkout lane, person sliding card through terminal, machine suddenly emitting red denial light that bathes the person's face, other shoppers in black and white background turning to stare",
        "mood": "Social exclusion and economic exile",
        "camera": "Static wide surveillance aesthetic",
    },
    {
        "quadro": "V10",
        "timestamp": "03:36-03:46",
        "titulo": "CAMERA DE VIGILANCIA",
        "q": "Q29",
        "q_titulo": "Cameras de vigilancia",
        "imagem_prompt": "Foreground: a richly detailed medieval Indian figure in vivid illuminated style -- elaborate crimson and gold sari with ornate jewelry, right thumb raised glowing with a golden biometric seal, standing before a carved sacred archway, expression reverent and unsettled. Background: black and white modern biometric enrollment -- monochrome fingerprint scanner terminals, desaturated Aadhaar registration stations, grayscale crowds in queues, dark administrative architecture. Strong contrast: vivid golden medieval Indian figure versus cold monochrome biometric state. Cinematic dramatic lighting, golden thumb glow medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847229 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid matte black security camera in extreme foreground slowly rotating on its mount, red recording LED pulsing, black and white city street with tiny monitored citizens below in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847319 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "Low",
        "animation_prompt": "Camera slowly orbiting around the security camera dome, surveillance device tracking smoothly on its gimbal, red LED blinking rhythmically, city below rendered in black and white scale showing full scope of monitoring",
        "mood": "Omniscient surveillance state",
        "camera": "Slow orbit around surveillance camera",
    },
    {
        "quadro": "V11",
        "timestamp": "04:00-04:10",
        "titulo": "REDE NEURAL / IA CONTROLANDO",
        "q": "Q30",
        "q_titulo": "IA e rede neural de controle",
        "imagem_prompt": "Foreground: a medieval European herald in vivid illuminated illustration style -- richly detailed deep blue, gold, and crimson royal livery, holding aloft a glowing golden document wallet with seven crimson apocalyptic wax seals, EU stars rendered as golden medieval stars. Background: black and white European Parliament -- monochrome Strasbourg building, desaturated EU institutional imagery, grayscale digital ID interface screens, dark institutional architecture. Strong contrast: vivid golden medieval herald versus cold monochrome EU institution. Cinematic dramatic lighting, golden seal glow medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847230 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid vast holographic neural network expanding through digital space in foreground, crimson red pulsing nodes connected by golden data streams, surveillance camera icons and financial institution symbols at each node, black and white globe in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847321 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "High",
        "animation_prompt": "Wide shot slowly pulling back to reveal full scale of AI neural network spanning globe, data pulses traveling along golden connection lines at light speed, new nodes continuously activating, network growing exponentially",
        "mood": "Incomprehensible scale of AI control",
        "camera": "Slow pull back revealing scale",
    },
    {
        "quadro": "V12",
        "timestamp": "04:24-04:34",
        "titulo": "CLAMOR / TESTEMUNHO",
        "q": "Q33",
        "q_titulo": "Profeta e testemunho final",
        "imagem_prompt": "Foreground: an ornate medieval chess board in vivid illuminated illustration style -- richly detailed crimson and gold pieces versus obsidian and silver pieces, a dark king piece as a seven-crowned advancing figure, golden pawns toppling around it, sacred geometric board patterns. Background: black and white modern world map as the board surface -- monochrome nation borders as grid, grayscale geopolitical markers as fallen pieces, dark global strategy environment. Strong contrast: vivid golden medieval chess game versus cold monochrome world map board. Cinematic dramatic lighting, strategic apocalyptic tension medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847233 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid prophet in crimson robe with arms raised holding apocalyptic scroll toward sky in foreground, black and white storm clouds gathering and swirling rapidly in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847323 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "Low",
        "animation_prompt": "Wide shot craning upward slowly as prophet raises arms higher, storm clouds in background accelerating their rotation, scroll text illuminating gold in the wind, robe fabric whipping dramatically",
        "mood": "Prophetic urgency and divine calling",
        "camera": "Slow crane up",
    },
    {
        "quadro": "V13",
        "timestamp": "04:48-04:58",
        "titulo": "SELOS ABERTOS / JULGAMENTO",
        "q": "Q11",
        "q_titulo": "Cordeiro com 7 Selos",
        "imagem_prompt": "Foreground: a crowd of medieval commoners in vivid illuminated illustration style -- diverse figures in colorful crimson, ochre, and deep blue robes, faces showing desperation and anguish, hands raised pleading, holding empty baskets, a medieval guard blocking a market gate with a sealed document. Background: black and white modern supermarket -- monochrome automatic checkout gates, desaturated product shelves, grayscale digital payment terminals with denied access symbols. Strong contrast: colorful desperate medieval crowd versus cold monochrome modern commerce. Cinematic dramatic lighting, emotional atmosphere, smoke and fire wisps medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847211 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid golden white Lamb of God standing on celestial altar with seven wax seals in foreground, first seal cracking and golden light exploding outward, black and white apocalyptic celestial throne room in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847325 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "High",
        "animation_prompt": "Camera slowly pushing in toward the Lamb on the altar, first seal dramatically cracking apart in slow motion, golden light burst emanating from broken seal, heavenly choir of light rays radiating outward",
        "mood": "Divine judgment unleashed",
        "camera": "Slow push in",
    },
    {
        "quadro": "V14",
        "timestamp": "05:12-05:22",
        "titulo": "CONCLUSAO / CHAMADO",
        "q": "Q35",
        "q_titulo": "Conclusao e chamado final",
        "imagem_prompt": "Foreground: a magnificent archangel herald in richest medieval illuminated illustration style -- golden armor, enormous detailed wings spread wide, trumpet at lips, unfurling golden banner with Gothic lettering, deep crimson and gold with heavenly white divine light radiating outward. Background: black and white epic apocalyptic panorama -- monochrome destroyed civilization skyline, desaturated lightning-shot storm clouds, grayscale collapsing structures and smoke columns, vast dark scale. Strong contrast: magnificent glowing golden angel versus cold monochrome apocalyptic world. Cinematic dramatic lighting, golden divine radiance, epic brand atmosphere medieval illuminated manuscript style colorful vivid detailed foreground, monochrome desaturated modern world background, cinematic dramatic lighting, chiaroscuro deep shadows, fire glow and floating ash particles, strong contrast vivid foreground vs black and white background, epic surreal prophetic apocalyptic atmosphere, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --chaos 20 --seed 847235 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --no text, watermark, logo, anime, cartoon, cute, cheerful, modern colors in foreground, clean background, digital flat art, photorealistic faces, identifiable real people, blurry, low quality, neon colors",
        "video_end_prompt": "colorful vivid golden divine light breaking through parting storm clouds and descending in radiant beams in foreground, silhouette of kneeling figure in crimson robe at center, black and white city skyline below in background, chiaroscuro dramatic lighting from above, fire glow and floating orange ash embers, 35mm film grain, anamorphic lens flares --ar 16:9 --style raw --v 7 --q 2 --stylize 750 --sref https://cdn.midjourney.com/bf50970e-30dd-47f1-8b2e-7d1f40c180da/0_0.png --sw 750 --seed 847327 --no text, watermark, logo, anime, cartoon, blurry, low quality",
        "motion": "Low",
        "animation_prompt": "Wide shot slowly tilting upward from black and white city below to golden sky above, divine light beams breaking through clouds and intensifying, kneeling figure's crimson robe glowing warmer as light descends",
        "mood": "Hope and divine invitation",
        "camera": "Slow tilt up from city to sky",
    },
]

def gerar_consolidado():
    linhas = []
    linhas.append("=" * 100)
    linhas.append("PIPELINE COMPLETO -- video-002-marca-da-besta")
    linhas.append("Abismo Criativa | Sinais do Fim | 1 CLIP POR CENA")
    linhas.append(f"Gerado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    linhas.append("=" * 100)
    linhas.append("")
    linhas.append("INSTRUCOES:")
    linhas.append("1. Para cada QUADRO: gere a IMAGEM no Midjourney com o /imagine")
    linhas.append("2. Apos gerar a imagem, baixe/salve ela")
    linhas.append("3. No MJ Web > Create > Animate:")
    linhas.append("   - Upload a imagem como START FRAME")
    linhas.append("   - Gere a imagen de END FRAME com o /imagine indicado")
    linhas.append("   - Configure Motion e Animation Prompt")
    linhas.append("   - Gere o clip de 10s")
    linhas.append("")
    linhas.append("=" * 100)
    linhas.append("")

    for cena in CENAS:
        linhas.append("")
        linhas.append("=" * 100)
        linhas.append(f"QUADRO {cena['quadro']} -- [{cena['timestamp']}] -- {cena['titulo']}")
        linhas.append("=" * 100)
        linhas.append("")

        linhas.append(f"{cena['q']} -- {cena['q_titulo']}")
        linhas.append(f"/imagine prompt: {cena['imagem_prompt']}")
        linhas.append("")

        linhas.append(f"--- CLIP (00:00 - 00:10) ---")
        linhas.append("START FRAME -> Usar a imagem gerada acima (Q01, Q02, etc)")
        linhas.append("Upload no Midjourney Web > Create > Animate")
        linhas.append("")

        linhas.append("END FRAME -- Gerar este /imagine e usar como End Frame:")
        linhas.append(f"/imagine prompt: {cena['video_end_prompt']}")
        linhas.append("")

        linhas.append(f"MOTION: {cena['motion']}")
        linhas.append(f"ANIMATION PROMPT: {cena['animation_prompt']}")
        linhas.append(f"MOOD: {cena['mood']}")
        linhas.append(f"CAMERA: {cena['camera']}")
        linhas.append("")

    conteudo = "\n".join(linhas)

    with open(TXT_OUT, "w", encoding="utf-8") as f:
        f.write(conteudo)

    print(f"[OK] Arquivo consolidado gerado: {TXT_OUT}")
    print(f"[INFO] {len(CENAS)} cenas processadas")
    return TXT_OUT

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
        sftp.put(txt_path, VPS_REMOTE)
        sftp.close()
        transport.close()
        print(f"[OK] Upload concluido!")
        print(f"[URL] {TXT_URL}")
        return True
    except Exception as e:
        print(f"[ERRO] Upload: {e}")
        transport.close()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("PIPELINE COMPLETO -- 1 Clip por Cena")
    print("=" * 60)

    txt_path = gerar_consolidado()
    upload_ok = upload_vps(txt_path)

    print("=" * 60)
    if upload_ok:
        print(f"[CONCLUIDO] Disponivel em:")
        print(f"  {TXT_URL}")
    else:
        print(f"[CONCLUIDO] Salvo localmente em:")
        print(f"  {txt_path}")
    print("=" * 60)
