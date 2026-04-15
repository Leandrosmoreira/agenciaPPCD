#!/usr/bin/env python3
"""Traduz todos os campos e valores de PT para EN no prompts_imagens.txt"""
import os

path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "canais", "sinais-do-fim", "videos", "video-001-armagedom", "5-prompts", "prompts_imagens.txt")

with open(path, encoding="utf-8") as f:
    txt = f.read()

# Restaurar / corrigir labels para ingles
txt = txt.replace("PROMPT NEGATIVO:", "NEGATIVE PROMPT:")
txt = txt.replace("PROPORCAO:", "ASPECT RATIO:")
txt = txt.replace("ESTILO:", "STYLE:")
txt = txt.replace("ATMOSFERA:", "MOOD:")
txt = txt.replace("SUJEITO:", "SUBJECT:")
txt = txt.replace("CENARIO:", "SETTING:")

# MOOD values PT -> EN
moods = [
    ("Épico / Apocalíptico", "Epic / Apocalyptic"),
    ("Epico / Apocaliptico", "Epic / Apocalyptic"),
    ("Reverente / Místico", "Reverential / Mystical"),
    ("Profético / Épico", "Prophetic / Epic"),
    ("Ominoso / Perturbador", "Ominous / Disturbing"),
    ("Conflituoso / Épico", "Conflicted / Epic"),
    ("Íntimo / Dramático", "Intimate / Dramatic"),
    ("Épico / Glorioso", "Epic / Glorious"),
    ("Épico", "Epic"),
    ("Tenso", "Tense"),
    ("Informativo / Sombrio", "Informative / Somber"),
    ("Perturbador", "Disturbing"),
    ("Ominoso", "Ominous"),
    ("Contrastante", "Contrasting"),
    ("Apocalíptico", "Apocalyptic"),
    ("Urgente", "Urgent"),
    ("Impactante", "Impactful"),
]
for pt, en in moods:
    txt = txt.replace(f"MOOD: {pt}", f"MOOD: {en}")

# SUBJECT values PT -> EN
subjects = [
    ("Arcanjo medieval com espada flamejante", "Medieval archangel with flaming sword"),
    ("Pergaminho com selos de cera e texto sagrado dourado", "Ancient parchment scroll with wax seals and golden sacred text"),
    ("Quatro Cavaleiros do Apocalipse (branco, vermelho, preto, pálido)", "Four Horsemen of the Apocalypse (white, red, black, pale)"),
    ("Mapa medieval do Oriente Médio em fogo e pergaminho com marcações de conflito", "Medieval map of the Middle East in fire and parchment with conflict markings"),
    ("Pergaminho de linha do tempo iluminado com marcos de conflito em dourado", "Illuminated timeline scroll with golden conflict milestones"),
    ("Profeta Zacarias em vestes medievais coloridas com pergaminho hebraico", "Prophet Zechariah in colorful medieval robes with Hebrew scroll"),
    ("Besta de 7 cabeças com olhos digitais/câmeras", "Seven-headed beast with digital camera eyes"),
    ("Mão humana com microchip sob a pele brilhando + selo de cera antigo", "Human hand with glowing microchip under skin + ancient wax seal"),
    ("Trono de ouro com figura sombria e telas holográficas ao redor", "Golden throne with shadowy figure and holographic screens"),
    ("Mundo partido — templo dourado com cruz e anjos vs. tecnologia sombria", "Split world — golden temple with cross and angels vs. dark technology"),
    ("Dois anjos medievais em combate (luz vs. sombra)", "Two medieval angels in combat (light vs. shadow)"),
    ("Anjo com trombeta dourada medieval sobre terra rachada em chamas", "Medieval angel with golden trumpet over cracked earth in flames"),
    ("Profeta medieval em sobreposição espectral sobre os 4 painéis", "Medieval prophet as spectral overlay across 4 panels"),
    ("Cristão ajoelhado em oração banhado por luz divina dourada", "Christian kneeling in prayer bathed in divine golden light"),
    ("Número \"360 MILHÕES\" em numerais medievais flamejantes vermelhos", "Number \"360 MILLION\" in flaming red medieval numerals"),
    ("Cavaleiro no cavalo branco descendo dos céus com espada de luz (Cristo)", "Rider on white horse descending from heavens with sword of light (Christ)"),
]
for pt, en in subjects:
    txt = txt.replace(f"SUBJECT: {pt}", f"SUBJECT: {en}")

# SETTING values PT -> EN
settings = [
    ("Cidade moderna destruída vista aérea em P&B;", "Destroyed modern city aerial view in B&W"),
    ("Cidade moderna destruída vista aérea em P&B", "Destroyed modern city aerial view in B&W"),
    ("Interior de catedral em ruínas em P&B", "Ruined stone cathedral interior in B&W"),
    ("Cidade moderna em colapso, multidões em pânico em P&B", "Collapsing modern city, panicked crowds in B&W"),
    ("Operações militares e explosões em P&B", "Military operations and explosions in B&W"),
    ("Paisagens de guerra e ruínas em P&B estilo arquivo histórico", "War landscapes and ruins in B&W historical archive style"),
    ("Ruínas de Jerusalém em P&B", "Ruins of Jerusalem in B&W"),
    ("Cidade de vigilância e controle tecnológico em P&B", "Surveillance and technological control city in B&W"),
    ("Código binário caindo em P&B, infraestrutura de vigilância", "Binary code falling in B&W, surveillance infrastructure"),
    ("Centro de controle global em P&B", "Global control center in B&W"),
    ("Fissura vermelha dividindo o mundo entre fé e materialismo", "Red fissure splitting the world between faith and materialism"),
    ("Multidões confrontando-se em P&B abaixo", "Crowds confronting each other in B&W below"),
    ("Terra em colapso com fissuras e fogo em P&B", "Collapsing earth with fissures and fire in B&W"),
    ("4 painéis de desastres naturais (terremoto, furacão, incêndio, seca) em P&B com bordas vermelhas",
     "4 panels of natural disasters (earthquake, hurricane, wildfire, drought) in B&W with red borders"),
    ("Silhuetas de soldados e correntes opressoras ao redor em P&B", "Silhouettes of soldiers and oppressive chains around in B&W"),
    ("Mapa-múndi antigo em P&B/pergaminho com pontos de perseguição em vermelho", "Ancient world map in B&W/parchment with persecution markers in red"),
    ("Multidões abaixo olhando para cima em P&B, céu se abrindo", "Crowds below looking upward in B&W, sky opening"),
]
for pt, en in settings:
    txt = txt.replace(f"SETTING: {pt}", f"SETTING: {en}")

with open(path, "w", encoding="utf-8") as f:
    f.write(txt)

print("[OK] Todos os campos traduzidos para ingles")
# Verificar se sobrou algum PT
import re
remaining = re.findall(r'(?:SUBJECT|SETTING|MOOD): [^\n]*[ãõáéíóúâêôàüç][^\n]*', txt)
if remaining:
    print(f"[ATENCAO] Ainda em PT: {len(remaining)} linhas")
    for r in remaining:
        print(f"  {r}")
else:
    print("[OK] Nenhum valor em PT restante")
