"""
Generator script for video-015 Nano Banana JSONs (Q02-Q98).
Run once, then delete. Creates 97 JSON files in 6-prompts-imagem/.
"""
import json
from pathlib import Path

OUT_DIR = Path(r"C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos\video-015-economist-manipulacao\6-prompts-imagem")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# === CONSTANTS ===
CANAL = "sinais-do-fim"
VIDEO = "video-015-economist-manipulacao"
VERSION = "nano-banana-v1"
MODEL_TARGET = "gemini-2.5-flash-image"
STYLE_REF_URL = "canais/sinais-do-fim/_config/style_refs/sinais_dark.png"
STYLE_REF_DESC = "dark cinematic chiaroscuro, Caravaggio-inspired, foreground in rich warm tones (crimson, amber, gold) with background in desaturated black-and-white, film grain, candlelight, floating orange embers"

# Standard negative_as_positive for the channel
BASE_NEGATIVE = [
    "clean frame without visible text or watermarks",
    "photorealistic documentary cinematography, not illustrated or cartoon",
    "analog film photography aesthetic, no digital art flatness",
    "muted desaturated background palette, warm saturated foreground only",
    "tack-sharp focus on primary subject"
]

# Copyright: anonymous figure entries
COPYRIGHT_PERSON = [
    "anonymous figure without recognizable facial features",
    "silhouette or contre-jour lighting hiding identity",
    "photorealistic anonymous aristocratic figure"
]

COPYRIGHT_ECONOMIST = [
    "unbranded publication without visible logo or trademark",
    "generic editorial magazine without specific masthead"
]

# Quadros that are REAL PEOPLE
PERSON_QUADROS = {6, 9, 15, 20, 39, 50, 68, 75, 76, 77, 78}
# Quadros that represent The Economist
ECONOMIST_QUADROS = {51, 71, 73}

# PRO model quadros (bible verses with in_scene_text)
PRO_VERSE_QUADROS = {45, 46, 47, 56, 61, 79, 80}
# PRO model quadros (visual complexity, no in_scene_text)
PRO_COMPLEX_QUADROS = {2, 78, 81}
ALL_PRO = PRO_VERSE_QUADROS | PRO_COMPLEX_QUADROS

def make_style_ref():
    return {
        "primary_image_url": STYLE_REF_URL,
        "weight": 0.85,
        "transfer_targets": ["color_palette", "lighting", "texture", "atmosphere", "film_grain"],
        "textual_description": STYLE_REF_DESC
    }

def make_base_style():
    return {
        "film_stock": "Kodak Portra 800 pushed two stops",
        "post_processing": "halation, crushed blacks, amber highlights, anamorphic lens flares",
        "texture_detail": "35mm film grain, dust particles, floating orange embers"
    }

def make_lighting(key="warm 2200K from upper-left", fill="faint amber from below", rim="gold edge light on subject contours", mood="chiaroscuro apocalyptic", shadow="deep hard-edged Caravaggio shadows"):
    return {
        "key_light": key,
        "fill_light": fill,
        "rim_light": rim,
        "mood": mood,
        "shadow_quality": shadow
    }

def make_api_hints(q_num):
    hints = {
        "multimodal_inputs": [
            {"type": "image", "source": "style_reference.primary_image_url", "role": "style_reference",
             "instruction": "Transfer color palette, lighting, grain, atmosphere only. Do not copy composition."},
            {"type": "text", "source": "serialized_prompt_from_this_json", "role": "scene_description"}
        ]
    }
    if q_num in ALL_PRO:
        hints["model_override"] = "pro"
    if q_num in PRO_VERSE_QUADROS:
        hints["critical_note_for_gemini"] = "The text in quotes MUST be rendered exactly as written, letter by letter, in the specified font style. This is a Bible verse and accuracy is sacred."
    return hints

def build_negative(q_num):
    neg = list(BASE_NEGATIVE)
    if q_num in PERSON_QUADROS:
        neg.extend(COPYRIGHT_PERSON)
    if q_num in ECONOMIST_QUADROS:
        neg.extend(COPYRIGHT_ECONOMIST)
    return neg

def suno_part_for_quadro(q):
    if q <= 11: return 1
    if q <= 25: return 2
    if q <= 37: return 3
    if q <= 53: return 4
    if q <= 63: return 5
    if q <= 73: return 6
    if q <= 82: return 7
    if q <= 86: return 8
    return 9

def ato_for_quadro(q):
    if q <= 4: return "Gancho"
    if q <= 11: return "Promessa"
    if q <= 25: return "Historico de Acertos"
    if q <= 37: return "Globo-Bola + Bets"
    if q <= 53: return "Grafico Despencando + Bonds"
    if q <= 63: return "Cerebro, Robos, Pharmakeia"
    if q <= 73: return "Misseis + Bilderberg"
    if q <= 82: return "Tese: Horario de Entrega"
    if q <= 86: return "Chamado"
    return "Fechamento + CTA"

# ===========================
# ALL 97 QUADROS DATA
# ===========================
# Each entry: (q_num, scene_title, narrative_beat, shot_dict, subject_dict, environment_dict, composition_dict, lighting_override_or_None, mood_dict, symbolism_dict, in_scene_text_or_None)

QUADROS = []

def Q(num, title, beat, shot, subject, env, comp, light, mood, sym, ist=None):
    QUADROS.append((num, title, beat, shot, subject, env, comp, light, mood, sym, ist))

# ---- Q02 ----
Q(2, "O contrato selado", "Duas maos apertam acordo sobre mesa — selo de cera rachado",
  {"type": "extreme close-up", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/2.0", "depth_of_field": "razor-thin", "aspect_ratio": "16:9"},
  {"primary": "two masculine hands shaking over a dark jacaranda wood desk, sealing a pact",
   "focal_point": "a cracked red wax seal on a partially rolled document between the hands",
   "secondary": "Left hand wears a heavy gold signet ring with heraldic crest; right hand is young and pale, unadorned. Left sleeve shows crimson velvet fabric.",
   "props": ["partially rolled document with broken red wax seal", "heavy gold signet ring with heraldic emblem", "crimson velvet sleeve"]},
  {"location": "a dimly lit 19th-century council chamber", "time_of_day": "late night, artificial chandelier light", "atmosphere": "conspiratorial, intimate, glacial tension"},
  {"rule": "centered symmetry", "foreground": "hands and document in rich crimson and gold tones, warm and vivid",
   "midground": "jacaranda desk surface with deep grain visible",
   "background": "desaturated black-and-white council room with tall-backed chairs barely visible in shadow",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="harsh warm light from chandelier above-right cutting hands in high contrast", fill="faint amber bounce from desk surface", rim="gold rim on knuckles and ring"),
  {"emotion": "conspiratorial, intimate, glacial", "tension": "high"},
  {"primary": "secret pact between old money and new power", "secondary": "broken seal as irreversible transfer"},
  None)

# ---- Q03 ----
Q(3, "A sombra que sai", "Figura de manto sai por portal gotico — sala vazia atras",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a cloaked figure in full silhouette exiting through a Gothic stone archway into blinding golden exterior light",
   "focal_point": "the elongated shadow stretching back into the room",
   "secondary": "Empty council chairs and fallen parchments on a long table behind the figure. Low-lying smoke on the floor.",
   "props": ["Gothic stone archway", "empty carved wooden council chairs", "fallen parchments on long table", "low-lying fog"]},
  {"location": "interior of a Renaissance council hall opening to bright exterior", "time_of_day": "dawn breaking through the archway", "atmosphere": "abandonment, betrayal, revelation"},
  {"rule": "rule of thirds", "foreground": "silhouetted figure at right third, dark contre-jour",
   "midground": "empty table with scattered documents in desaturated tones",
   "background": "blinding golden light beam from exterior through the Gothic arch",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="intense golden backlight from exterior creating full silhouette", fill="almost none — deep shadows inside", rim="gold edge light defining cloak contour", mood="contre-jour dramatic"),
  {"emotion": "abandonment, betrayal, solemn exit", "tension": "rising"},
  {"primary": "departure of old power, the empty throne left behind", "secondary": "light as both escape and judgement"},
  None)

# ---- Q04 ----
Q(4, "A pergunta sobre a mesa", "Mesa overhead com revista, Biblia Apocalipse 17, vela, relogio de bolso",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a dark wooden bedside table viewed from directly above with four ritual objects arranged deliberately",
   "focal_point": "an antique pocket watch with stopped hands at the center",
   "secondary": "An aged unbranded magazine in parchment tones closed beside an open leather-bound Bible showing Apocalypse 17, a lit beeswax candle projecting golden lateral light, and a tarnished brass pocket watch with frozen hands.",
   "props": ["aged unbranded parchment-toned magazine", "open leather Bible at Apocalypse 17", "lit beeswax candle", "tarnished brass pocket watch with frozen hands"]},
  {"location": "a sparse bedroom nightstand", "time_of_day": "3 AM candlelight", "atmosphere": "interrogative, sacred, threatening"},
  {"rule": "centered symmetry", "foreground": "four objects in warm golden candlelight, rich tones",
   "background": "dark oak table grain disappearing into pure black edges",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="single beeswax candle casting golden lateral glow from lower-left", fill="none — deep black surrounds", rim="faint gold reflection on watch glass and Bible pages", mood="intimate chiaroscuro, candlelit mystery"),
  {"emotion": "interrogative, sacred, ominous", "tension": "medium"},
  {"primary": "the question of hidden knowledge — what do they know?", "secondary": "stopped time as countdown"},
  None)

# ---- Q05 ----
Q(5, "A sala de leitura vitoriana", "Podio com revista iluminada em biblioteca em ruinas",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 40, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "an oak lectern at center holding an open unbranded magazine illuminated by a single golden beam descending from a cracked cathedral ceiling",
   "focal_point": "the open magazine pages catching divine light",
   "secondary": "Dusty leather-bound books on shelves flanking both sides. Low smoke creeping across marble floor.",
   "props": ["carved oak lectern", "open unbranded magazine with parchment pages", "dusty leather books on shelves", "cracked cathedral ceiling with light beam"]},
  {"location": "a ruined Victorian reading room inside a crumbling Gothic library", "time_of_day": "unknown interior, single shaft of golden light from above", "atmosphere": "reverent, mysterious, abandoned"},
  {"rule": "centered symmetry", "foreground": "lectern and golden parchment in warm rich tones",
   "midground": "dusty bookshelves partially collapsed",
   "background": "desaturated black-and-white ruined library architecture",
   "safe_zone_for_overlay": "lower 20% of frame"},
  None,
  {"emotion": "reverence, mystery", "tension": "medium"},
  {"primary": "sacred text as vessel of hidden truth", "secondary": "ruin surrounding preserved knowledge"},
  None)

# ---- Q06 ----
Q(6, "O bilionario canadense", "Homem de negocios em poltrona de couro, sombra no rosto",
  {"type": "close-up", "camera_angle": "low angle", "focal_length_mm": 85, "aperture": "f/2.0", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "an anonymous Canadian businessman in his 60s seated in an oxblood leather wingback chair with cracked patina, face half-concealed in deep shadow, painted in the style of a Rembrandt portrait",
   "focal_point": "the shadowed half of the face, only jaw and ear visible",
   "secondary": "Pile of legal contracts and a Montblanc fountain pen on a polished mahogany side table.",
   "props": ["oxblood leather wingback chair with cracked patina", "pile of legal contracts", "Montblanc fountain pen", "polished mahogany side table"]},
  {"location": "a 1940s Canadian executive study", "time_of_day": "late afternoon, window light from right", "atmosphere": "opaque, anonymous, powerful"},
  {"rule": "rule of thirds", "foreground": "businessman in rich warm classical painting tones (crimson chair, ochre suit fabric)",
   "background": "desaturated black-and-white Toronto skyscrapers visible through window",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="window light from upper-right illuminating half the face", fill="deep shadow on left half", rim="warm gold edge on hair and shoulder", mood="Rembrandt chiaroscuro portrait"),
  {"emotion": "opaque, anonymous, quietly powerful", "tension": "medium"},
  {"primary": "hidden buyer — wealth without identity", "secondary": "the chair as throne of invisible power"},
  None)

# ---- Q07 ----
Q(7, "Mapa-mundi e moedas", "Overhead mapa renascentista com maos movendo moedas de ouro",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 35, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a Renaissance-style painted world map mural covering a table, with three unequal piles of gold coins and a gloved hand transferring coins between piles",
   "focal_point": "the white-gloved hand mid-transfer holding gold coins",
   "secondary": "Map painted in rich colors with gold leaf borders. Three distinct piles of gold coins of different heights.",
   "props": ["Renaissance world map mural", "three piles of gold coins", "white silk glove", "gold leaf map borders"]},
  {"location": "a Vatican-style grand hall with marble columns", "time_of_day": "torchlight, no natural light", "atmosphere": "hidden transaction, power redistribution"},
  {"rule": "dynamic asymmetric", "foreground": "gold coins and gloved hand in rich warm tones",
   "midground": "painted map in rich Renaissance colors",
   "background": "desaturated black-and-white marble columns of the Vatican hall",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm torchlight from multiple sconces above", fill="soft amber bounce from gold coins", rim="gold glint on glove fingers"),
  {"emotion": "covert transaction, redistribution of wealth", "tension": "rising"},
  {"primary": "global wealth as a game of chess — coins moved at will", "secondary": "the gloved hand as invisible puppet master"},
  None)

# ---- Q08 ----
Q(8, "A dinastia Agnelli", "Brasao heraldico italiano com figuras renascentistas",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a large Italian heraldic family crest painted as a Renaissance fresco, with central aristocratic figures in crimson, ochre and gold Renaissance garments",
   "focal_point": "a stylized letter 'A' emblem at the top of the crest",
   "secondary": "Silhouettes of vintage Ferrari and Fiat automobiles visible in monochrome background behind the fresco.",
   "props": ["heraldic family crest in fresco", "Renaissance garments in crimson and ochre", "stylized 'A' emblem", "vintage automobile silhouettes in background"]},
  {"location": "an Italian palazzo wall with aged plaster", "time_of_day": "warm interior candlelight", "atmosphere": "dynastic, continuous, weighty"},
  {"rule": "centered symmetry", "foreground": "fresco figures in vivid Renaissance palette — crimson, ochre, gold",
   "background": "desaturated black-and-white vintage automobile silhouettes and palazzo architecture",
   "safe_zone_for_overlay": "lower 20% of frame"},
  None,
  {"emotion": "dynasty, continuity, gravitas", "tension": "medium"},
  {"primary": "old European money persisting through centuries", "secondary": "family crest as coat of arms for corporate empire"},
  None)

# ---- Q09 ----
Q(9, "A jornalista Nobel", "Close-up mulher jornalista filipina com medalha Nobel, fundo protesto P&B",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/2.0", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "an anonymous Filipino female journalist in her 60s with a concerned expression, holding a vintage microphone, wearing a deep wine-red dress, with a golden Nobel Peace Prize medal visible on her chest",
   "focal_point": "the golden Nobel medal catching light on her chest",
   "secondary": "Crowd in protest visible behind her in full monochrome.",
   "props": ["vintage handheld microphone", "deep wine-red dress", "golden Nobel Peace Prize medal", "protest crowd in monochrome background"]},
  {"location": "outdoor press conference area", "time_of_day": "overcast daylight filtered through clouds", "atmosphere": "authoritative, alert, urgent"},
  {"rule": "rule of thirds", "foreground": "journalist figure in warm rich tones — wine-red dress, gold medal",
   "background": "desaturated black-and-white crowd in protest with signs and raised fists",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="overcast diffused light from above", fill="warm amber reflected from medal", rim="gold edge on hair and shoulders", mood="documentary dramatic"),
  {"emotion": "authority, alarm, moral weight", "tension": "rising"},
  {"primary": "the voice of truth ignored by power", "secondary": "Nobel as divine appointment to warn"},
  None)

# ---- Q10 ----
Q(10, "Doomsday Clock", "Relogio do Juizo Final — ponteiros a segundos da meia-noite",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a massive antique Doomsday Clock in dark wood and tarnished brass, hands frozen at 85 seconds to midnight, with pulsing blood-red light emanating from behind the clock face",
   "focal_point": "the minute hand trembling near midnight",
   "secondary": "Distant mushroom cloud in monochrome behind the clock.",
   "props": ["massive antique clock in dark wood", "tarnished brass clock hands", "pulsing blood-red backlight", "distant mushroom cloud"]},
  {"location": "a grand institutional hall with the clock mounted on a stone wall", "time_of_day": "permanent twilight, no natural light", "atmosphere": "terminal urgency, countdown"},
  {"rule": "centered symmetry", "foreground": "clock face in aged gold and blood-red tones",
   "background": "desaturated black-and-white distant nuclear mushroom cloud through window",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="pulsing blood-red backlight from behind clock", fill="faint warm amber from below", rim="gold edge on clock hands and frame", mood="apocalyptic crimson glow"),
  {"emotion": "terminal urgency, dread", "tension": "absolute"},
  {"primary": "time running out for civilization", "secondary": "clock as oracle of destruction"},
  None)

# ---- Q11 ----
Q(11, "Tres pecas juntas", "Overhead mesa com revista, relogio, medalha Nobel — luz divina vertical",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "three ritual objects arranged in a triangle on a dark oak table: an aged parchment-toned magazine, a tarnished brass pocket watch, and a golden Nobel medal, all illuminated by a single vertical beam of divine light",
   "focal_point": "the center point where the three objects converge",
   "secondary": "Thin wisps of incense smoke rising through the light beam.",
   "props": ["aged unbranded magazine", "tarnished brass pocket watch", "golden Nobel medal", "vertical beam of divine light", "incense smoke wisps"]},
  {"location": "a dark chamber with the table as the only surface", "time_of_day": "unspecified, divine light from above", "atmosphere": "synthesis, imminence, sacred convergence"},
  {"rule": "centered symmetry", "foreground": "three objects in warm golden light",
   "background": "pure black surroundings",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="single vertical beam of white-gold divine light from directly above", fill="none — pure darkness around", rim="gold reflections on each object surface"),
  {"emotion": "synthesis, convergence, imminence", "tension": "high"},
  {"primary": "three witnesses to the same event — media, science, prophecy", "secondary": "triangular arrangement as trinity of evidence"},
  None)

# ---- Q12 ----
Q(12, "Galeria dos pergaminhos", "Wide de galeria gotica com cinco pergaminhos emoldurados",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a Gothic museum gallery with five ornately framed aged parchments hanging in a row on a stone wall, each representing a different year (2021-2025), with no legible text on any frame",
   "focal_point": "the central parchment (2023) glowing slightly brighter",
   "secondary": "Marble floor reflecting golden light. Low fog creeping along the base of the wall.",
   "props": ["five ornate gilded frames", "aged blank parchments", "Gothic stone wall", "marble floor", "low ground fog"]},
  {"location": "a Gothic cathedral gallery turned museum", "time_of_day": "warm lateral torchlight", "atmosphere": "museological, imposing, archival"},
  {"rule": "centered symmetry", "foreground": "gilded frames in warm gold tones",
   "midground": "stone wall texture",
   "background": "desaturated black-and-white Gothic arched ceiling disappearing into darkness",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm lateral golden light from wall sconces between frames", fill="soft amber bounce from marble floor", rim="gold edge on frame corners"),
  {"emotion": "imposing, archival authority", "tension": "medium"},
  {"primary": "gallery of prophecies fulfilled", "secondary": "empty parchments awaiting their marks of confirmation"},
  None)

# ---- Q13 ----
Q(13, "Caca-niqueis vintage", "Close-up maquina caca-niqueis com simbolos de globo, moedas, caveira",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 85, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a vintage brass slot machine with spinning reels showing symbols of a globe, stacked gold coins, and a human skull, the lever pulled back in mid-action",
   "focal_point": "the spinning reels in the center of the machine",
   "secondary": "Scattered coins on the tray below the machine.",
   "props": ["vintage brass slot machine", "spinning reels with globe/coin/skull symbols", "pulled lever", "scattered gold coins in tray"]},
  {"location": "a dark 1920s speakeasy casino corner", "time_of_day": "neon-lit night interior", "atmosphere": "addiction, vertigo, deception"},
  {"rule": "centered symmetry", "foreground": "slot machine in vivid gold and crimson tones",
   "background": "desaturated black-and-white neon signs and smoke-filled room",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm internal glow from machine reels", fill="faint neon reflection", rim="gold edge on brass surfaces", mood="noir casino glow"),
  {"emotion": "addiction, vertigo, the world gambled", "tension": "rising"},
  {"primary": "the world as casino — everything is a bet", "secondary": "skull on reels as inevitable outcome"},
  None)

# ---- Q14 ----
Q(14, "Grafico despencando", "Medium de grafico vermelho caindo sobre dolares queimando",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a large blood-red financial graph line plummeting diagonally across the frame, overlaid on burning US dollar bills in crimson and amber flames",
   "focal_point": "the point where the graph line crashes through the burning bills",
   "secondary": "Ash particles floating upward from burning currency.",
   "props": ["blood-red plummeting graph line", "burning US dollar bills", "rising ash particles", "financial numbers fading"]},
  {"location": "a stock exchange trading floor in chaos", "time_of_day": "harsh fluorescent interior", "atmosphere": "financial panic, freefall"},
  {"rule": "dynamic asymmetric", "foreground": "burning dollars and red graph in vivid crimson and amber",
   "background": "desaturated black-and-white panicked traders on trading floor",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="harsh overhead fluorescent mixed with fire glow from burning bills", fill="amber from flames below"),
  {"emotion": "panic, financial collapse", "tension": "high"},
  {"primary": "inflation as invisible fire consuming savings", "secondary": "graph as seismograph of systemic failure"},
  None)

# ---- Q15 ----
Q(15, "Tres lideres em afresco", "Wide tres figuras em chiaroscuro — ocidental, eslavo, asiatico",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "three anonymous archetypal world leaders rendered as a Renaissance fresco: an elderly Western man in dark suit at left, a Slavic man in military uniform at center, and an East Asian man in Mao-style tunic at right, all facing the viewer with tense expressions",
   "focal_point": "the narrow gap between the three figures where a cracked map is visible",
   "secondary": "A fragmenting political world map painted on the wall behind them in monochrome.",
   "props": ["Renaissance fresco technique on aged plaster", "dark Western suit", "Slavic military uniform", "Mao-style dark tunic", "fragmenting world map behind"]},
  {"location": "a grand fresco wall in a palazzo", "time_of_day": "warm interior torchlight", "atmosphere": "triple tension, geopolitical standoff"},
  {"rule": "centered symmetry", "foreground": "three figures in rich warm Renaissance tones",
   "background": "desaturated black-and-white fragmenting political map",
   "safe_zone_for_overlay": "lower 20% of frame"},
  None,
  {"emotion": "triple tension, confrontation, standoff", "tension": "high"},
  {"primary": "three powers that define the world's fate", "secondary": "fresco as permanent historical record"},
  None)

# ---- Q16 ----
Q(16, "Tanque sobre mapa", "Medium overhead tanque sobre mapa Europa Oriental com explosoes",
  {"type": "medium", "camera_angle": "high angle", "focal_length_mm": 50, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a dark steel military tank model positioned on an antique map of Eastern Europe, with small explosion effects painted in oil around it",
   "focal_point": "the tank barrel pointing toward Ukraine on the map",
   "secondary": "An ancient Bible parchment scroll in warm tones visible at the lower-right corner.",
   "props": ["dark steel tank model", "antique Eastern Europe map", "painted oil explosion effects", "Bible parchment scroll in corner"]},
  {"location": "a war room table with maps spread", "time_of_day": "overhead military lamp lighting", "atmosphere": "invasion, military aggression"},
  {"rule": "rule of thirds", "foreground": "tank and explosions in rich warm tones — amber fire, dark steel with warm reflections",
   "background": "desaturated black-and-white map paper and table edges",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="harsh overhead military desk lamp", fill="amber explosion glow from map surface"),
  {"emotion": "invasion, violation of sovereignty", "tension": "absolute"},
  {"primary": "war as chess move on the world map", "secondary": "Bible as silent witness to human violence"},
  None)

# ---- Q17 ----
Q(17, "Caveira nuclear", "Close caveira de prata em altar com simbolos nucleares",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 85, "aperture": "f/2.0", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a polished silver human skull on a black stone altar, surrounded by radial nuclear hazard symbols etched in crimson and gold",
   "focal_point": "the empty eye sockets of the skull reflecting red light",
   "secondary": "Intense floating embers and sparks around the skull.",
   "props": ["polished silver skull", "black stone altar", "radial nuclear symbols in crimson and gold", "intense floating embers"]},
  {"location": "a dark ritual chamber", "time_of_day": "pulsing red light from unseen source", "atmosphere": "death, annihilation, nuclear dread"},
  {"rule": "centered symmetry", "foreground": "silver skull and nuclear symbols in vivid crimson and gold",
   "background": "pure black void",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="pulsing crimson light from below and behind", fill="faint gold from embers", rim="silver edge highlights on skull contours", mood="crimson nuclear ritual"),
  {"emotion": "death, extinction-level dread", "tension": "absolute"},
  {"primary": "nuclear war as the final horseman", "secondary": "skull as humanity's epitaph"},
  None)

# ---- Q18 ----
Q(18, "Tel Aviv em chamas", "Wide de edificios em P&B com ceu em chamas, vela judaica quebrada",
  {"type": "wide", "camera_angle": "low angle", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a broken Shabbat candle lying on the ground over a Star of David mosaic, in rich warm tones, with a burning cityscape in the background",
   "focal_point": "the broken candle with its flame still flickering on the ground",
   "secondary": "City buildings burning in the distance. Fiery sky overhead.",
   "props": ["broken Shabbat candle with flickering flame", "Star of David floor mosaic", "burning city buildings", "fiery sky"]},
  {"location": "a city plaza with modernist architecture", "time_of_day": "night with fire illumination", "atmosphere": "mourning, atrocity, devastation"},
  {"rule": "rule of thirds", "foreground": "broken candle and Star of David in warm rich gold and crimson",
   "background": "desaturated black-and-white burning buildings and fiery sky",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="fire glow from burning city casting warm light", fill="amber from candle flame", rim="gold edge on mosaic tiles", mood="devastation firelight"),
  {"emotion": "mourning, horror, atrocity", "tension": "absolute"},
  {"primary": "the attack on sacred ground — innocence destroyed", "secondary": "broken candle as extinguished peace"},
  None)

# ---- Q19 ----
Q(19, "Bancos desmoronando", "Medium de tres fachadas bancarias virando po dourado",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "three neoclassical bank facades crumbling into golden dust and debris, their stone columns fracturing mid-collapse",
   "focal_point": "the central bank facade at the moment of maximum disintegration",
   "secondary": "Gold dust particles cascading downward like a waterfall.",
   "props": ["three neoclassical bank facades", "fracturing stone columns", "cascading golden dust", "scattered financial papers"]},
  {"location": "a corporate financial district", "time_of_day": "harsh daylight through dust cloud", "atmosphere": "systemic collapse, cascading failure"},
  {"rule": "centered symmetry", "foreground": "crumbling facades in warm golden dust and amber tones",
   "background": "desaturated black-and-white corporate skyscrapers behind",
   "safe_zone_for_overlay": "lower 20% of frame"},
  None,
  {"emotion": "systemic collapse, cascading domino effect", "tension": "high"},
  {"primary": "banks as temples that fell — systemic fragility", "secondary": "golden dust as wealth dissolving into nothing"},
  None)

# ---- Q20 ----
Q(20, "Interrogacao dourada", "Close-up ponto de interrogacao em ouro sobre silhueta loira",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 100, "aperture": "f/2.0", "depth_of_field": "razor-thin", "aspect_ratio": "16:9"},
  {"primary": "a massive solid gold question mark floating in mid-air, reflecting warm light, positioned over the silhouette of a man with blonde hair whose face is completely hidden in shadow",
   "focal_point": "the gold question mark dominating the center of the frame",
   "secondary": "Political rally crowd in monochrome behind.",
   "props": ["solid gold question mark", "silhouetted blonde male figure", "rally crowd in monochrome"]},
  {"location": "a political stage with dramatic lighting", "time_of_day": "night rally with spotlights", "atmosphere": "political enigma, uncertainty"},
  {"rule": "centered symmetry", "foreground": "gold question mark in vivid warm tones",
   "midground": "silhouetted figure in pure black",
   "background": "desaturated black-and-white rally crowd",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="spotlight from directly above on the gold question mark", fill="none on figure — pure silhouette", rim="faint gold edge on hair contour"),
  {"emotion": "political enigma, the unanswered question", "tension": "rising"},
  {"primary": "the leader as unknown variable — unpredictability as power", "secondary": "gold as authority, question mark as uncertainty"},
  None)

# ---- Q21 ----
Q(21, "Urnas transbordando", "Overhead de urnas com cedulas sobre mapa EUA em P&B",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 35, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "wooden ballot boxes overflowing with paper ballots scattered across a large desaturated map of the United States, with one single golden-marked ballot at the center catching all the light",
   "focal_point": "the single golden ballot at dead center of the map",
   "secondary": "Hundreds of white ballots scattered chaotically around the boxes.",
   "props": ["wooden ballot boxes", "overflowing paper ballots", "one golden-marked ballot", "map of the United States"]},
  {"location": "an election counting room floor", "time_of_day": "harsh overhead fluorescent", "atmosphere": "electoral confirmation, finality"},
  {"rule": "centered symmetry", "foreground": "golden ballot in rich warm tone",
   "midground": "overflowing ballot boxes in muted tones",
   "background": "desaturated black-and-white US map underneath",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="harsh overhead fluorescent white light", fill="golden glow from the marked ballot", mood="documentary clinical"),
  {"emotion": "confirmation, finality, the question answered", "tension": "medium"},
  {"primary": "democracy as spectacle — the outcome preordained", "secondary": "single golden ballot as the one that mattered"},
  None)

# ---- Q22 ----
Q(22, "Saturno e misseis", "Wide Saturno dourado com tres figuras imperiais e misseis",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "the planet Saturn rendered in burnished gold filling the upper frame, with its rings glowing amber, while three small imperial silhouette figures stand below in commanding poses, each with a stylized missile beneath their feet",
   "focal_point": "Saturn's rings glowing at center-top",
   "secondary": "Starfield behind Saturn in monochrome.",
   "props": ["burnished gold Saturn with amber rings", "three imperial silhouette figures", "three stylized missiles", "monochrome starfield"]},
  {"location": "cosmic void, deep space", "time_of_day": "eternal space darkness with planetary glow", "atmosphere": "mystical-military, cosmic confrontation"},
  {"rule": "centered symmetry", "foreground": "Saturn in rich gold and amber tones, figures in warm silhouette",
   "background": "desaturated black-and-white starfield",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="golden planetary glow from Saturn illuminating everything below", fill="faint starlight", rim="amber ring reflection on missile surfaces"),
  {"emotion": "mystic military tension, cosmic scale", "tension": "high"},
  {"primary": "Saturn as chronos — time god ruling leaders and weapons", "secondary": "missiles as modern swords of Damocles"},
  None)

# ---- Q23 ----
Q(23, "Missil em voo", "Close de missil contra ceu vermelho carmesim, cupula de Jerusalem P&B",
  {"type": "close-up", "camera_angle": "low angle", "focal_length_mm": 135, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a military drone missile in diagonal flight from left to right, motion-blurred fins, against a deep crimson sky",
   "focal_point": "the warhead tip of the missile cutting through the red sky",
   "secondary": "A distant sacred dome silhouette in monochrome below.",
   "props": ["military drone missile with motion blur", "deep crimson sky", "distant sacred dome silhouette"]},
  {"location": "skies above a holy city", "time_of_day": "blood-red dusk", "atmosphere": "imminent attack, holy city under siege"},
  {"rule": "dynamic asymmetric", "foreground": "missile in warm metallic tones with crimson sky",
   "background": "desaturated black-and-white sacred dome on horizon",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="blood-red sky ambient illumination", fill="warm metallic reflection on missile body", rim="crimson edge light on fins"),
  {"emotion": "imminent strike, sacred ground under attack", "tension": "absolute"},
  {"primary": "modern weapons targeting ancient holy ground", "secondary": "red sky as divine wrath backdrop"},
  None)

# ---- Q24 ----
Q(24, "Galeria validada", "Wide retorno galeria Q12 — cinco checks dourados queimados",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "the same Gothic gallery from Q12 but now each of the five framed parchments bears a large golden checkmark burned into its surface, glowing with embers at the edges",
   "focal_point": "the five burning golden checkmarks in unison",
   "secondary": "Intense golden light pouring from above. Smoke rising from each parchment.",
   "props": ["five ornate gilded frames", "burning golden checkmarks on parchments", "rising smoke from each frame", "intense overhead golden light"]},
  {"location": "the same Gothic gallery as Q12", "time_of_day": "intense golden overhead light", "atmosphere": "terminal validation, prophecy confirmed"},
  {"rule": "centered symmetry", "foreground": "five burning checkmarks in vivid gold and amber",
   "background": "desaturated black-and-white Gothic gallery architecture",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="intense golden light from above flooding the gallery", fill="amber glow from burning checkmarks", rim="gold edge on frame corners"),
  {"emotion": "validation, terminal proof, five for five", "tension": "high"},
  {"primary": "five prophecies confirmed — the track record proven", "secondary": "fire as divine seal of approval"},
  None)

# ---- Q25 ----
Q(25, "Mao sobre a revista 2026", "Overhead mao masculina sobre revista 2026 na mesa de cabeceira",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a man's hand resting on a closed aged unbranded magazine on a bedside table next to an empty rumpled bed, illuminated by cold blue-night light from a window",
   "focal_point": "the hand pressing down on the magazine cover",
   "secondary": "Empty bed with crumpled white sheets visible at edge of frame.",
   "props": ["man's hand", "aged unbranded magazine", "dark wood bedside table", "rumpled white bed sheets", "cold blue window light"]},
  {"location": "a sparse bedroom at night", "time_of_day": "3 AM cold blue moonlight", "atmosphere": "personal accusation, sleeplessness"},
  {"rule": "rule of thirds", "foreground": "hand and magazine in muted warm tones against cold blue ambient",
   "background": "desaturated black-and-white bed and room",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="cold blue-white moonlight from window at upper-right", fill="none — deep shadows", rim="faint silver edge on hand contour"),
  {"emotion": "personal accusation, insomnia, dread", "tension": "high"},
  {"primary": "the question aimed at the viewer — can you sleep knowing this?", "secondary": "empty bed as restlessness of the informed"},
  None)

# ---- Q26 ----
Q(26, "Globo-bola medieval", "Wide globo terrestre como bola de futebol medieval em couro rachado",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 24, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a large globe rendered as a medieval cracked leather football floating at center-frame, with continent shapes visible on the worn leather panels, hovering over a ruined fresco background",
   "focal_point": "the cracked stitching of the leather football-globe at center",
   "secondary": "Ruined Renaissance fresco on the wall behind.",
   "props": ["medieval cracked leather football-globe", "continent shapes on leather panels", "ruined Renaissance fresco wall"]},
  {"location": "a crumbling Renaissance chapel with faded frescoes", "time_of_day": "dim interior with single shaft of golden light", "atmosphere": "grotesque revelation, the world profaned"},
  {"rule": "centered symmetry", "foreground": "leather globe in warm ochre and crimson tones",
   "background": "desaturated black-and-white ruined fresco and chapel walls",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="single shaft of golden light from upper-left illuminating the globe", fill="faint warm bounce from chapel floor"),
  {"emotion": "grotesque revelation, the world as a plaything", "tension": "rising"},
  {"primary": "the world reduced to a toy — kicked and gambled", "secondary": "cracked leather as fragility of civilization"},
  None)

# ---- Q27 ----
Q(27, "Chute no globo", "Medium silhueta chutando globo-bola, estadio vazio P&B",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a silhouetted male figure frozen mid-kick, leg extended, striking the leather globe-ball from Q26, captured in dynamic frozen motion",
   "focal_point": "the point of contact between foot and globe",
   "secondary": "Empty massive stadium seats in monochrome behind. Golden lateral light.",
   "props": ["silhouetted kicking figure", "leather globe-ball", "empty massive stadium", "golden lateral light"]},
  {"location": "center of an enormous empty stadium", "time_of_day": "golden hour sidelight", "atmosphere": "profanation, the world kicked"},
  {"rule": "dynamic asymmetric", "foreground": "silhouetted figure and globe in warm golden-amber contact point",
   "background": "desaturated black-and-white empty stadium seating stretching into distance",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="golden lateral light from right creating full silhouette", fill="none", rim="strong gold edge on leg and globe at impact point"),
  {"emotion": "profanation, admission of control", "tension": "high"},
  {"primary": "the world as something kicked by powerful men", "secondary": "empty stadium as the masses who don't see"},
  None)

# ---- Q28 ----
Q(28, "Tres estadios caca-niqueis", "Overhead tres estadios Copa 2026 como caca-niqueis vintage",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 35, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "three vintage slot machines arranged in a triangular formation viewed from above, each shaped like a football stadium with recognizable arena architecture, connected by ornate golden cables between them",
   "focal_point": "the golden cables connecting the three stadium-slot-machines at center",
   "secondary": "City blocks visible around the stadiums in monochrome.",
   "props": ["three stadium-shaped vintage slot machines", "ornate golden cables connecting them", "city blocks in monochrome", "flashing amber lights on machines"]},
  {"location": "aerial view of three cities", "time_of_day": "night with artificial illumination", "atmosphere": "manipulated spectacle, rigged entertainment"},
  {"rule": "centered symmetry", "foreground": "slot machine stadiums in vivid gold and crimson",
   "background": "desaturated black-and-white city grids",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm amber glow from each slot machine", fill="faint city light ambiance", rim="gold cable reflections"),
  {"emotion": "manipulated spectacle, sport as gambling front", "tension": "rising"},
  {"primary": "World Cup as orchestrated distraction — three countries, three slot machines", "secondary": "connected cables as hidden coordination"},
  None)

# ---- Q29 ----
Q(29, "Familia brasileira desesperada", "Wide familia em sala pequena, pai com rosto nas maos, TV P&B",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a Brazilian family in a small living room: father seated on a worn red fabric sofa with his face buried in his hands, mother standing behind with hand on his shoulder, young son watching from doorway",
   "focal_point": "the father's hands covering his face in despair",
   "secondary": "An old CRT television broadcasting a football match in monochrome. Single warm lamp illuminating the scene.",
   "props": ["worn red fabric sofa", "father in despair", "mother's comforting hand", "young son in doorway", "old CRT TV showing football in P&B", "single warm lamp"]},
  {"location": "a small Brazilian lower-middle-class living room", "time_of_day": "evening, single lamp", "atmosphere": "domestic despair, hidden suffering"},
  {"rule": "rule of thirds", "foreground": "father on red sofa and warm lamp in rich crimson and amber",
   "background": "desaturated black-and-white walls, CRT TV glow, doorway",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="single warm table lamp from left", fill="cold CRT TV glow from right", rim="faint warm edge on mother's hand"),
  {"emotion": "desperation, domestic suffering, silent crisis", "tension": "high"},
  {"primary": "the human cost of gambling — the family destroyed", "secondary": "football on TV as the instrument of ruin"},
  None)

# ---- Q30 ----
Q(30, "Cartoes e inadimplencia", "Close-up cartoes de credito vencidos e carta de cobranca",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 60, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a stack of expired credit cards with visible damage and a debt collection letter stamped with the word INADIMPLENTE in blood-red ink on a worn Formica kitchen table",
   "focal_point": "the blood-red INADIMPLENTE stamp on the letter",
   "secondary": "Scattered crumbs and an empty coffee cup beside the cards.",
   "props": ["expired credit cards with damage", "debt collection letter", "INADIMPLENTE blood-red stamp", "worn Formica table", "empty coffee cup"]},
  {"location": "a modest Brazilian kitchen table", "time_of_day": "harsh overhead kitchen fluorescent", "atmosphere": "personal ruin, financial devastation"},
  {"rule": "rule of thirds", "foreground": "cards and stamped letter in vivid crimson stamp and gold card tones",
   "background": "desaturated black-and-white modest kitchen",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="harsh overhead fluorescent kitchen light", fill="warm reflection from credit card surfaces"),
  {"emotion": "ruin, shame, financial destruction", "tension": "high"},
  {"primary": "gambling debt as death sentence for the poor", "secondary": "INADIMPLENTE as modern scarlet letter"},
  None)

# ---- Q31 ----
Q(31, "Homem no chao com celular", "Wide homem sentado no chao de apartamento vazio, tela de celular",
  {"type": "wide", "camera_angle": "low angle", "focal_length_mm": 24, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a man sitting on the floor of an empty apartment with bare walls, illuminated only by the cold blue-white glow of a smartphone screen in his hands showing a crashing betting graph",
   "focal_point": "the smartphone screen glowing in the dark",
   "secondary": "Bare apartment walls, no furniture. Cold blue light on his face.",
   "props": ["man on bare floor", "smartphone with crashing bet graph", "empty apartment", "cold blue screen glow"]},
  {"location": "an empty apartment stripped of furniture", "time_of_day": "night, no lights except phone screen", "atmosphere": "isolation, addiction, rock bottom"},
  {"rule": "centered symmetry", "foreground": "phone screen glow in cold blue with warm skin tones on hands",
   "background": "desaturated black-and-white bare apartment walls and floor",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="cold blue-white smartphone screen as sole light source", fill="none — pure darkness", rim="faint blue edge on shoulders and hair"),
  {"emotion": "loneliness, addiction, absolute bottom", "tension": "high"},
  {"primary": "technology as both weapon and prison", "secondary": "empty apartment as everything already lost"},
  None)

# ---- Q32 ----
Q(32, "Data center UFDS", "Medium arquitetura data center nordico com servidores rubros",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a futuristic Nordic data center interior with rows of server racks glowing in deep crimson red, and floating golden holographic letters spelling UFDS in ornate Latin script in the foreground",
   "focal_point": "the holographic UFDS letters at center",
   "secondary": "Server racks stretching into deep perspective. Cool blue-white ambient light on ceiling.",
   "props": ["Nordic data center interior", "crimson-glowing server racks", "holographic golden UFDS letters", "cool blue ceiling lights"]},
  {"location": "a high-security Scandinavian data center", "time_of_day": "artificial interior 24/7 lighting", "atmosphere": "opaque technology, surveillance infrastructure"},
  {"rule": "centered symmetry", "foreground": "golden UFDS hologram in warm tones",
   "midground": "crimson server racks",
   "background": "desaturated black-and-white data center ceiling and cooling infrastructure",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="crimson glow from server racks", fill="cool blue ambient from ceiling", rim="gold reflection from holographic letters"),
  {"emotion": "opaque surveillance, hidden processing", "tension": "medium"},
  {"primary": "AI processing bets in real-time — surveillance of gambling", "secondary": "UFDS as all-seeing technological eye"},
  None)

# ---- Q33 ----
Q(33, "Tela de dados com olho", "Close extremo tela de computador com dados de apostas e reflexo de olho",
  {"type": "extreme close-up", "camera_angle": "straight-on", "focal_length_mm": 100, "aperture": "f/1.4", "depth_of_field": "razor-thin", "aspect_ratio": "16:9"},
  {"primary": "an extreme close-up of a computer monitor screen showing cascading lines of green-gold betting data streaming downward like a matrix, with the faint reflection of a human eye visible on the glass surface",
   "focal_point": "the reflected human eye visible through the data cascade",
   "secondary": "Data lines in green-gold on black screen.",
   "props": ["computer monitor with cascading betting data", "green-gold data streams", "reflected human eye on screen glass"]},
  {"location": "a dark monitoring room", "time_of_day": "night, screen-lit", "atmosphere": "inverse surveillance, the watcher watched"},
  {"rule": "centered symmetry", "foreground": "green-gold data streams in vivid warm tones on black screen",
   "midground": "faint reflected eye on glass",
   "background": "pure black",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="green-gold monitor glow as sole light", fill="none", rim="faint data-colored reflection on eye surface"),
  {"emotion": "surveillance, the watcher becomes the watched", "tension": "rising"},
  {"primary": "thousands of bets per second — AI sees everything", "secondary": "human eye reduced to passive observer of its own exploitation"},
  None)

# ---- Q34 ----
Q(34, "Mesa de jogo", "Overhead mesa com fichas empilhadas e carta virando com simbolo apocaliptico",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a green felt poker table viewed from directly above with three stacks of gold and crimson chips and five face-down cards, one card mid-flip revealing a golden apocalyptic symbol (seven-headed beast) on its face",
   "focal_point": "the flipping card revealing the beast symbol",
   "secondary": "Scattered chips and burned card edges.",
   "props": ["green felt poker table", "gold and crimson chip stacks", "five face-down playing cards", "one mid-flip card with apocalyptic symbol", "burned card edges"]},
  {"location": "a high-stakes private casino room", "time_of_day": "dim overhead spot", "atmosphere": "rigged game revealed, apocalyptic hand"},
  {"rule": "centered symmetry", "foreground": "chips and cards in vivid gold and crimson",
   "background": "desaturated black-and-white casino table edge and dark room",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="single overhead spot on the table center", fill="warm amber from gold chips", rim="gold edge on flipping card"),
  {"emotion": "the game was rigged all along", "tension": "high"},
  {"primary": "gambling as apocalyptic conspiracy — the house always wins", "secondary": "beast on the card as the real player"},
  None)

# ---- Q35 ----
Q(35, "Globo-bola em chamas", "Wide globo-bola novamente mas agora em chamas com rachaduras",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 24, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "the same medieval leather globe-ball from Q26, now engulfed in flames with golden-red cracks propagating across its surface like tectonic fractures, surrounded by falling ash",
   "focal_point": "the widest crack at center of the globe emitting molten golden light",
   "secondary": "Empty bleachers in monochrome behind. Ash falling everywhere.",
   "props": ["burning leather globe-ball", "golden-red tectonic cracks", "falling ash", "empty bleachers in monochrome"]},
  {"location": "center of an empty stadium", "time_of_day": "night with fire as sole illumination", "atmosphere": "prophecy fulfilling, the world breaking"},
  {"rule": "centered symmetry", "foreground": "burning globe in vivid crimson, gold and amber flames",
   "background": "desaturated black-and-white empty stadium bleachers",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="fire glow from burning globe as primary light", fill="warm ember glow reflected upward", rim="crimson edge on cracks"),
  {"emotion": "prophecy manifesting, the world splitting", "tension": "absolute"},
  {"primary": "the world-toy is breaking — consequences of being kicked", "secondary": "cracks as fault lines of civilization"},
  None)

# ---- Q36 ----
Q(36, "Calendario novembro 2025", "Close-up calendario antigo marcado NOVEMBRO 2025 em pergaminho",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 85, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "an ancient parchment calendar page showing NOVEMBER with a blood-red circle drawn around a date, a quill pen lying beside it, illuminated by single candle",
   "focal_point": "the blood-red circle on the calendar",
   "secondary": "Candle wax dripping onto the parchment edge.",
   "props": ["aged parchment calendar", "blood-red circle marking", "quill feather pen", "dripping beeswax candle"]},
  {"location": "a scholar's desk in a medieval study", "time_of_day": "candlelight", "atmosphere": "historical record, date of prophecy"},
  {"rule": "rule of thirds", "foreground": "parchment and red circle in warm rich tones",
   "background": "desaturated black-and-white dark study walls",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="single candle from left casting warm amber", fill="none", rim="gold edge on quill feather"),
  {"emotion": "historical certainty, date recorded", "tension": "medium"},
  {"primary": "the date everything was announced — November 2025", "secondary": "quill as instrument of prophecy recording"},
  None)

# ---- Q37 ----
Q(37, "Carteira vazia", "Medium carteira masculina aberta e vazia com moeda de real rolando",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 60, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "an open brown leather men's wallet lying on a dark wooden table, completely empty inside except for a single Brazilian Real coin rolling out of it, caught mid-motion",
   "focal_point": "the single Real coin mid-roll at the wallet's edge",
   "secondary": "Dramatic golden lateral light. Table surface scratched and worn.",
   "props": ["empty brown leather wallet", "single rolling Brazilian Real coin", "scratched dark wooden table"]},
  {"location": "a modest dining table in dim room", "time_of_day": "golden hour light through window", "atmosphere": "personal financial disaster, last coin"},
  {"rule": "rule of thirds", "foreground": "wallet and coin in warm golden-amber light",
   "background": "desaturated black-and-white dim room",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="golden lateral light from left window", fill="none — deep shadow on right", rim="gold glint on rolling coin edge"),
  {"emotion": "personal ruin, the last coin falling", "tension": "high"},
  {"primary": "before you lose the first Real — it is already announced", "secondary": "empty wallet as the endgame of gambling"},
  None)

# ---- Q38 ----
Q(38, "Grafico em catedral", "Wide grafico em queda pintado no teto de catedral com moedas caindo",
  {"type": "wide", "camera_angle": "low angle", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a massive financial graph line painted in crimson and gold on the ceiling of a Gothic cathedral as a medieval fresco, showing a dramatic plunge, with gold coins falling from the graph's lowest point like rain",
   "focal_point": "the lowest point of the plunging graph where coins cascade",
   "secondary": "Two crossed swords painted at the graph's peak. Cathedral nave in monochrome below.",
   "props": ["ceiling fresco of plunging graph", "falling gold coins", "two crossed swords at graph peak", "Gothic cathedral nave"]},
  {"location": "inside a Gothic cathedral, looking up at the vaulted ceiling", "time_of_day": "dim interior with golden accent light", "atmosphere": "sacred collapse, divine-scale economic judgement"},
  {"rule": "centered symmetry", "foreground": "falling gold coins in warm vivid tones",
   "midground": "crimson graph fresco on ceiling",
   "background": "desaturated black-and-white cathedral nave and ribbed vaulting",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm golden accent light from unseen source illuminating ceiling fresco", fill="faint amber from gold coins reflecting", rim="gold edge on coin edges during fall"),
  {"emotion": "sacred-scale economic collapse", "tension": "absolute"},
  {"primary": "the market crash as divine judgement painted in a cathedral", "secondary": "crossed swords as war driving the crash"},
  None)

# ---- Q39 ----
Q(39, "Editor Tom Standage", "Close-up lateral editor de jornal, 50 anos, oculos, pena de tinta",
  {"type": "close-up", "camera_angle": "low angle", "focal_length_mm": 85, "aperture": "f/2.0", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "an anonymous Victorian-era male newspaper editor, approximately 50 years old, with round spectacles and severe expression, holding a dip pen hovering over a parchment, viewed from a 3/4 angle with strong chiaroscuro lighting",
   "focal_point": "the dip pen poised above the parchment",
   "secondary": "Inkwell and scattered papers on desk.",
   "props": ["round wire spectacles", "dip pen with ink", "parchment document", "brass inkwell", "scattered editorial papers"]},
  {"location": "a Victorian newspaper editorial office", "time_of_day": "late night oil lamp", "atmosphere": "solemn declaration, editorial authority"},
  {"rule": "rule of thirds", "foreground": "editor in rich warm tones — ochre vest, amber lamplight on spectacles",
   "background": "desaturated black-and-white Victorian editorial office with typesetters",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm oil lamp from left illuminating the face and parchment", fill="deep shadow on far side", rim="gold reflection on spectacle lenses"),
  {"emotion": "solemn declaration, the weight of the written word", "tension": "rising"},
  {"primary": "the editor as oracle — writing what he knows will happen", "secondary": "dip pen as weapon of revelation"},
  None)

# ---- Q40 ----
Q(40, "Pergaminho com frase", "Overhead pergaminho sobre mesa escura com caligrafia gotica",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 50, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "an aged parchment spread on a dark wooden desk, covered in Gothic calligraphy in faded ink, with one single phrase at center glowing brighter in golden ink than the rest, illuminated by candlelight",
   "focal_point": "the golden-glowing phrase at center of the parchment",
   "secondary": "Candle at the edge. Wax drips on parchment corners.",
   "props": ["aged parchment with Gothic calligraphy", "golden-glowing central phrase", "beeswax candle", "wax drips on corners", "dark wooden desk"]},
  {"location": "a medieval scriptorium desk", "time_of_day": "candlelight late at night", "atmosphere": "official revelation, the confession is in writing"},
  {"rule": "centered symmetry", "foreground": "golden phrase glowing at parchment center",
   "background": "desaturated black-and-white desk and scriptorium shadows",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="candle from lower-right casting warm directional light on parchment", fill="golden glow from the highlighted phrase itself"),
  {"emotion": "revelation in writing, evidence laid bare", "tension": "high"},
  {"primary": "the written confession — bond markets will hammer rich nations", "secondary": "golden text as truth hiding in plain sight"},
  None)

# ---- Q41 ----
Q(41, "Cinco bandeiras em vitral", "Wide cinco bandeiras nacionais em vitral rachadas por ouro liquido",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "five national flags rendered as stained glass windows in a Gothic church, each cracked down the middle by a flowing line of liquid gold: USA, UK, France, Germany, Japan",
   "focal_point": "the liquid gold cracks connecting all five windows",
   "secondary": "Light streaming through the cracked stained glass. Monochrome congressional building visible through the cracks.",
   "props": ["five stained glass flag windows", "liquid gold cracks in each", "Gothic stone arches between windows", "light streaming through cracks"]},
  {"location": "a Gothic church with large stained glass windows", "time_of_day": "daylight filtering through stained glass", "atmosphere": "imperial decay, the richest nations cracking"},
  {"rule": "centered symmetry", "foreground": "stained glass flags in vivid warm colors with gold cracks",
   "background": "desaturated black-and-white congressional building visible through cracks",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="daylight filtering through stained glass creating colored light patches", fill="golden glow from liquid gold cracks", mood="sacred decay"),
  {"emotion": "imperial decline, the rich nations cracking", "tension": "high"},
  {"primary": "sovereign debt crisis as stained glass shattering in a church", "secondary": "liquid gold as wealth literally flowing out"},
  None)

# ---- Q42 ----
Q(42, "Juiz medieval com martelo", "Medium juiz medieval segurando martelo sobre certificados de divida",
  {"type": "medium", "camera_angle": "low angle", "focal_length_mm": 50, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a medieval judge in dark robes and hood, holding a massive bronze gavel raised above a mountain of paper bond certificates piled on a judicial bench",
   "focal_point": "the bronze gavel at the apex of its swing",
   "secondary": "Bond certificates scattered and crumpling. Gothic arch above.",
   "props": ["medieval judge in dark robes", "massive bronze gavel", "mountain of bond certificates", "judicial bench", "Gothic arch"]},
  {"location": "a medieval courtroom with stone walls", "time_of_day": "torchlight from walls", "atmosphere": "economic judgement day, the hammer falls"},
  {"rule": "rule of thirds", "foreground": "judge and bronze gavel in rich warm gold and crimson tones",
   "background": "desaturated black-and-white Treasury-style government building visible through window",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm torchlight from left illuminating judge and gavel", fill="amber bounce from bronze gavel surface"),
  {"emotion": "judgement, economic reckoning", "tension": "absolute"},
  {"primary": "the bond market as judge sentencing nations", "secondary": "gavel as the instrument of financial doom"},
  None)

# ---- Q43 ----
Q(43, "Prova documental", "Close site institucional em monitor com dedo apontando linha destacada",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 60, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a close-up of a finger pointing at a highlighted golden line on a retroilluminated monitor screen displaying an institutional document page, with no legible text but one line glowing brighter than the rest",
   "focal_point": "the golden highlighted line where the finger points",
   "secondary": "Monitor bezels visible. Dim room behind.",
   "props": ["finger pointing", "institutional document on monitor", "golden highlighted line", "dim room"]},
  {"location": "a dark home office or study", "time_of_day": "night, screen-lit", "atmosphere": "documentary proof, evidence highlighted"},
  {"rule": "rule of thirds", "foreground": "finger and golden line in warm tones",
   "background": "desaturated black-and-white monitor and dark room",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="monitor screen backlight as primary source", fill="golden glow from highlighted line"),
  {"emotion": "evidence found, proof undeniable", "tension": "rising"},
  {"primary": "the proof is public — date, signature, and stamp", "secondary": "finger as the act of accusation"},
  None)

# ---- Q44 ----
Q(44, "Biblia aberta no atril", "Wide Biblia antiga aberta com feixe celestial dourado descendo",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a large ancient leather-bound Bible open on an ornate wooden lectern, illuminated by a descending beam of celestial golden light from a cracked chapel ceiling, pages glowing with warmth",
   "focal_point": "the open Bible pages catching the divine light beam",
   "secondary": "Floating embers in the light beam. Chapel in monochrome around.",
   "props": ["ancient leather Bible", "ornate wooden lectern", "celestial golden light beam", "floating embers", "cracked chapel ceiling"]},
  {"location": "a ruined stone chapel", "time_of_day": "divine light from above, no natural time", "atmosphere": "sacred reverence, the Scripture speaks"},
  {"rule": "centered symmetry", "foreground": "Bible and lectern in warm rich golden and amber tones",
   "background": "desaturated black-and-white ruined chapel interior",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="celestial golden beam from directly above", fill="warm amber from glowing pages", rim="gold edge on Bible spine and lectern carvings"),
  {"emotion": "sacred reverence, the word of God illuminated", "tension": "rising"},
  {"primary": "the Bible as the original source — Revelation chapter 18", "secondary": "divine light as God speaking through the text"},
  None)

# ---- Q45 — VERSÍCULO Ap 18:11 (PRO) ----
Q(45, "Mercadores chorando", "Medium mercadores medievais chorando de joelhos sobre fardos em chamas",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 40, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "medieval merchants in rich robes weeping on their knees over burning bales of silk, spices, and gold, in a harbor marketplace engulfed in flames, painted in hyperdetailed Renaissance style",
   "focal_point": "a burning parchment scroll at center displaying the Bible verse text",
   "secondary": "Harbor buildings and ships in monochrome behind. Flames consuming everything.",
   "props": ["weeping medieval merchants in rich robes", "burning bales of silk and spices", "melting gold ingots", "burning parchment scroll with verse", "harbor in monochrome"]},
  {"location": "a medieval Mediterranean harbor marketplace", "time_of_day": "dusk with fire illumination", "atmosphere": "biblical lamentation, commercial apocalypse"},
  {"rule": "rule of thirds", "foreground": "merchants and burning goods in vivid crimson, ochre and gold",
   "background": "desaturated black-and-white harbor city and ships",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="fire glow from burning goods as primary light", fill="warm amber reflected from gold", rim="crimson edge on weeping figures"),
  {"emotion": "lamentation, commercial apocalypse, ruin of the rich", "tension": "high"},
  {"primary": "Revelation 18:11 — merchants weeping because no one buys their goods", "secondary": "fire as divine judgement on commerce"},
  {"enabled": True, "content": "E sobre ela choram e lamentam os mercadores da terra; porque ninguem compra mais as suas mercadorias.", "content_secondary": "Apocalipse 18:11", "font_style": "ancient gothic calligraphy in aged gold ink", "medium": "inscribed on burning aged parchment scroll", "placement": "center of frame on the scroll", "legibility": "crisp and readable", "language": "Portuguese"})

# ---- Q46 — VERSÍCULO Ap 18:16 (PRO) ----
Q(46, "Babilonia em ruinas", "Wide cidade imperial em ruinas, mulheres com vestes de purpura",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a massive imperial Babylon-style city in ruins with flames everywhere, women in foreground wearing fine linen veils with purple and scarlet garments that are crumbling and tearing, molten gold flowing through the rubble",
   "focal_point": "a crumbling stone wall bearing the Bible verse inscription",
   "secondary": "Collapsing towers and temples behind in monochrome.",
   "props": ["Babylon-style city in ruins", "women in purple and scarlet garments", "fine linen veils", "molten gold in rubble", "crumbling stone wall with verse"]},
  {"location": "a destroyed imperial capital city", "time_of_day": "apocalyptic dusk with fire illumination", "atmosphere": "apocalyptic destruction, the great city fallen"},
  {"rule": "rule of thirds", "foreground": "women in vivid purple, scarlet and gold tones",
   "background": "desaturated black-and-white ruined city skyline",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="fire glow from burning city", fill="warm amber from molten gold in rubble", rim="crimson edge on garments"),
  {"emotion": "apocalyptic, the fall of Babylon", "tension": "absolute"},
  {"primary": "Revelation 18:16 — the great city clothed in fine linen, purple and scarlet", "secondary": "ruin of luxury as divine judgement"},
  {"enabled": True, "content": "Ai, ai daquela grande cidade, que estava vestida de linho fino, de purpura e de escarlata", "content_secondary": "Apocalipse 18:16", "font_style": "carved stone serif, weathered", "medium": "etched into crumbling stone wall of ruins", "placement": "center-left on the wall", "legibility": "crisp and readable", "language": "Portuguese"})

# ---- Q47 — VERSÍCULO Ap 18:17 (PRO) ----
Q(47, "Ampulheta partindo", "Close-up ampulheta dourada partindo ao meio",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 100, "aperture": "f/2.0", "depth_of_field": "razor-thin", "aspect_ratio": "16:9"},
  {"primary": "a golden hourglass splitting in half at its narrow waist, sand streaming out in a brilliant golden thread, the two halves separating in mid-fracture",
   "focal_point": "the fracture point where the hourglass splits and sand escapes",
   "secondary": "The escaping sand catches light like a golden waterfall. Dark neutral background.",
   "props": ["golden ornate hourglass", "splitting fracture at center", "streaming golden sand", "glass shards floating"]},
  {"location": "isolated on dark background, studio-style", "time_of_day": "single warm spotlight", "atmosphere": "time expired, irreversible"},
  {"rule": "centered symmetry", "foreground": "golden hourglass and sand in vivid warm gold tones",
   "background": "desaturated black-and-white neutral void",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="single warm spotlight from above", fill="golden reflection from sand stream", rim="gold edge on glass shards"),
  {"emotion": "time has run out, irreversible moment", "tension": "absolute"},
  {"primary": "Revelation 18:17 — in one hour such great riches laid waste", "secondary": "hourglass as literal single hour of destruction"},
  {"enabled": True, "content": "Porque numa so hora tantas riquezas se desolaram.", "content_secondary": "Apocalipse 18:17", "font_style": "ancient gothic calligraphy in gold leaf", "medium": "inscribed on the golden hourglass body", "placement": "center of frame on the hourglass surface", "legibility": "crisp and readable", "language": "Portuguese"})

# ---- Q48 ----
Q(48, "Mapa-mundi com relogio", "Overhead mapa antigo com relogio sobreposto marcando 11:59",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "an ancient parchment world map viewed from above with a large transparent circular clock face overlaid at center showing 11:59, gold coins falling through the map's major cities leaving impact marks",
   "focal_point": "the clock hands at 11:59",
   "secondary": "Gold coins mid-fall over various city locations on the map.",
   "props": ["ancient parchment world map", "transparent clock face at 11:59", "falling gold coins", "impact marks on cities"]},
  {"location": "a navigation table", "time_of_day": "warm lamplight", "atmosphere": "universal, imminent, one minute to midnight"},
  {"rule": "centered symmetry", "foreground": "clock face and gold coins in vivid warm tones",
   "background": "desaturated parchment map tones",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm lamp from above", fill="golden reflection from coins", rim="gold edge on clock hands"),
  {"emotion": "universal countdown, one minute to midnight", "tension": "absolute"},
  {"primary": "the whole world under one clock — time running out globally", "secondary": "coins falling on cities as wealth disappearing everywhere"},
  None)

# ---- Q49 ----
Q(49, "Apostolo Joao escrevendo", "Medium apostolo Joao, barba branca, manto carmesim, caverna de Patmos",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "the apostle John as an elderly man with long white beard and flowing crimson robe, writing on a parchment scroll with a reed pen inside a rocky cave, candlelight illuminating his face and hands",
   "focal_point": "the hand writing on the parchment scroll",
   "secondary": "Rocky cave walls with moisture. Distant ocean visible through cave mouth in monochrome.",
   "props": ["elderly apostle John", "flowing crimson robe", "parchment scroll", "reed pen", "beeswax candle", "rocky cave interior"]},
  {"location": "the cave of Patmos, rocky island grotto", "time_of_day": "candlelight inside cave, ocean daylight visible outside", "atmosphere": "prophetic authorship, ancient divine inspiration"},
  {"rule": "rule of thirds", "foreground": "John in vivid crimson and gold tones with candlelight",
   "background": "desaturated black-and-white rocky cave and ocean through cave mouth",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="single candle from right illuminating face and scroll", fill="faint ocean light from cave mouth", rim="warm gold on white beard"),
  {"emotion": "prophetic authority, ancient divine inspiration", "tension": "medium"},
  {"primary": "John wrote this nearly 2000 years ago", "secondary": "the cave as womb of revelation"},
  None)

# ---- Q50 ----
Q(50, "Espelho cronologico", "Wide split Joao versus editor moderno conectados por fogo dourado",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a split composition: left half shows the apostle John writing in his cave (warm tones), right half shows an anonymous Victorian editor writing at a desk (warm tones), both connected by a diagonal line of golden fire crossing the center of the frame",
   "focal_point": "the golden fire line connecting the two writers at center",
   "secondary": "Both figures in rich warm tones. Background behind each in monochrome.",
   "props": ["apostle John in cave on left", "Victorian editor at desk on right", "diagonal golden fire line connecting them", "monochrome backgrounds behind each"]},
  {"location": "split scene: Patmos cave left / Victorian office right", "time_of_day": "candlelight on both sides", "atmosphere": "chronological mirror, ancient meets modern"},
  {"rule": "centered symmetry", "foreground": "both writers in rich warm tones connected by gold fire",
   "background": "desaturated black-and-white environments behind each writer",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="candle on each side illuminating respective writer", fill="golden glow from fire line at center", rim="gold edge on both figures"),
  {"emotion": "chronological mirror, the same message across millennia", "tension": "rising"},
  {"primary": "two writers, 2000 years apart, describing the same event", "secondary": "fire as the thread of prophecy connecting eras"},
  None)

# ---- Q51 ----
Q(51, "Revista mostra o Apocalipse", "Wide revista analoga aberta mostrando exatas imagens do Apocalipse",
  {"type": "wide", "camera_angle": "high angle", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "an unbranded generic editorial magazine spread open, its pages showing painted illustrations matching Revelation 18: weeping merchants and falling coins, all rendered in golden tones on the pages",
   "focal_point": "the illustrated magazine pages showing merchants and coins",
   "secondary": "Writing desk surface in monochrome. Quill and inkwell nearby.",
   "props": ["open unbranded magazine", "illustrated pages with Revelation imagery", "weeping merchants on pages", "falling coins on pages", "quill and inkwell", "writing desk"]},
  {"location": "a dark writing desk", "time_of_day": "warm lamplight", "atmosphere": "macabre confirmation, magazine echoing the Bible"},
  {"rule": "centered symmetry", "foreground": "magazine pages in vivid golden illustrated tones",
   "background": "desaturated black-and-white desk and room",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm desk lamp illuminating magazine pages", fill="golden bounce from illustrated pages"),
  {"emotion": "macabre confirmation, the magazine illustrates the prophecy", "tension": "high"},
  {"primary": "modern magazine cover showing exactly what Revelation 18 describes", "secondary": "the Bible's vision made contemporary"},
  None)

# ---- Q52 ----
Q(52, "Maos com moedas desintegrando", "Close maos de varias idades segurando moedas que viram cinzas",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 85, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "multiple hands of different ages (elderly, adult male, female, child) reaching upward holding gold coins that are disintegrating into red-golden ash between their fingers",
   "focal_point": "the moment of disintegration where coins become ash",
   "secondary": "Ash floating upward like embers. Dark void behind.",
   "props": ["multiple hands of different ages", "gold coins disintegrating", "red-golden ash particles", "dark void"]},
  {"location": "abstract dark void", "time_of_day": "warm spotlight from above", "atmosphere": "universal loss, wealth dissolving for everyone"},
  {"rule": "centered symmetry", "foreground": "hands and disintegrating coins in vivid gold and crimson",
   "background": "pure black void",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm spotlight from directly above on the hands", fill="golden glow from disintegrating coins"),
  {"emotion": "universal loss, no one is spared", "tension": "rising"},
  {"primary": "all ages and genders losing everything — the collapse is universal", "secondary": "coins to ash as wealth is an illusion"},
  None)

# ---- Q53 ----
Q(53, "Cerebro com joystick", "Overhead cerebro anatomico iluminado como reliquia com cabos de joystick",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a classical anatomical human brain displayed on a marble museum pedestal under a glass dome, illuminated like a sacred relic, with vintage game controller cables plugged into its cortex from both sides",
   "focal_point": "the connection points where cables enter the brain",
   "secondary": "Glass dome reflecting warm light. Museum plinth in monochrome.",
   "props": ["anatomical human brain", "marble museum pedestal", "glass dome", "vintage game controller cables", "sacred museum lighting"]},
  {"location": "a dark museum exhibition hall", "time_of_day": "single spotlight from above", "atmosphere": "profanation of the human, sacred brain defiled"},
  {"rule": "centered symmetry", "foreground": "brain in vivid crimson with golden cable connectors",
   "background": "desaturated black-and-white museum hall",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="single warm spotlight from directly above on the brain", fill="amber reflection from glass dome"),
  {"emotion": "profanation of the human mind, sacred organ defiled", "tension": "high"},
  {"primary": "the brain as exhibit — controlled by games and technology", "secondary": "museum display as how future civilizations will see us"},
  None)

# ---- Q54 ----
Q(54, "Olho refletindo pixel", "Close-up extremo olho humano com pixel de videogame na pupila",
  {"type": "extreme close-up", "camera_angle": "straight-on", "focal_length_mm": 100, "aperture": "f/1.4", "depth_of_field": "razor-thin", "aspect_ratio": "16:9"},
  {"primary": "an extreme close-up of a human eye wide open, the iris in rich amber-brown tones, with a tiny vintage videogame pixel art character reflected in the pupil, and a single golden teardrop forming at the lower eyelid",
   "focal_point": "the pixel art reflection in the pupil center",
   "secondary": "Eyelashes catching warm light. Dark room visible in iris reflection.",
   "props": ["human eye in amber tones", "pixel videogame reflection in pupil", "single golden teardrop", "warm eyelash highlights"]},
  {"location": "a dark room, face lit only by screen", "time_of_day": "night, screen-lit", "atmosphere": "captured consciousness, the mind hijacked"},
  {"rule": "centered symmetry", "foreground": "eye iris in vivid amber-gold tones",
   "background": "desaturated black-and-white reflected dark room in iris",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm screen glow illuminating the eye from front", fill="none", rim="faint gold on eyelashes"),
  {"emotion": "consciousness captured, humanity reduced to a screen", "tension": "rising"},
  {"primary": "the brain connected to a joystick — the eye reflects the game", "secondary": "golden tear as the soul weeping at its own captivity"},
  None)

# ---- Q55 ----
Q(55, "Mesa com tres objetos sagrados", "Medium mesa com cerebro-joystick, pergaminho Ap 13, coroa de espinhos",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a dark altar table with three sacred objects arranged left to right: a brain connected to a game joystick (left), a parchment scroll open at Apocalypse 13 (center), and a crown of thorns (right), all illuminated by frontal golden light",
   "focal_point": "the central parchment scroll",
   "secondary": "Incense smoke rising between objects.",
   "props": ["brain with joystick cables", "parchment scroll at Revelation 13", "crown of thorns", "frontal golden light", "incense smoke"]},
  {"location": "a dark ritual altar", "time_of_day": "golden frontal illumination", "atmosphere": "sacred interpretation, three witnesses on the altar"},
  {"rule": "rule of thirds", "foreground": "three objects in vivid warm rich tones",
   "background": "pure black void",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="frontal golden light illuminating all three objects equally", fill="incense smoke diffusing light", rim="warm gold edge on each object"),
  {"emotion": "sacred interpretation, connecting symbols to prophecy", "tension": "rising"},
  {"primary": "three witnesses: brain control (tech), the Beast verse (prophecy), and sacrifice (crown)", "secondary": "the altar as place of decoding"},
  None)

# ---- Q56 — VERSÍCULO Ap 13:16 (PRO) ----
Q(56, "Marca na testa e mao", "Wide multidao medieval com marca de ouro na testa ou mao direita",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 28, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a vast medieval crowd rendered in monochrome, with each figure displaying a glowing mark of golden fire on their forehead or right hand, one central figure in the foreground in rich vivid colors with the mark blazing brightest on their forehead",
   "focal_point": "the blazing golden mark on the central figure's forehead",
   "secondary": "A large parchment altar in the background bearing the verse text. Vast crowd stretching to horizon.",
   "props": ["vast medieval crowd in monochrome", "glowing golden marks on foreheads and hands", "central figure in rich colors", "parchment altar with verse", "blazing forehead mark"]},
  {"location": "a medieval city square", "time_of_day": "overcast sky with golden divine light breaking through", "atmosphere": "universal marking, the mark of the Beast"},
  {"rule": "centered symmetry", "foreground": "central figure in vivid crimson and gold with blazing mark",
   "midground": "crowd in monochrome with golden marks",
   "background": "desaturated black-and-white medieval city and parchment altar",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="divine golden light from above breaking through clouds", fill="golden glow from marks on the crowd", rim="gold edge on central figure"),
  {"emotion": "universal subjugation, the mark applied to all", "tension": "absolute"},
  {"primary": "Revelation 13:16 — the mark on forehead or right hand, applied to all", "secondary": "golden fire mark as digital control made flesh"},
  {"enabled": True, "content": "E faz que a todos, pequenos e grandes, ricos e pobres, livres e servos, lhes seja posto um sinal na mao direita, ou na testa.", "content_secondary": "Apocalipse 13:16", "font_style": "ancient gothic calligraphy in gold ink on aged parchment", "medium": "inscribed on large parchment scroll on altar behind crowd", "placement": "upper third of frame on the altar", "legibility": "crisp and readable", "language": "Portuguese"})

# ---- Q57 ----
Q(57, "Marca pulsante na testa", "Close-up frontal figura com marca dourada pulsante na testa",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 85, "aperture": "f/2.0", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a frontal close-up of the central figure from Q56, now isolated: forehead bearing a pulsating golden mark shaped like a circuit pattern, eyes partially hidden in deep shadow, expression solemn",
   "focal_point": "the pulsating golden circuit mark on the forehead",
   "secondary": "Deep shadow hiding the lower face. Faint amber glow from the mark.",
   "props": ["forehead with golden circuit-pattern mark", "deep shadows on face", "solemn expression", "amber glow"]},
  {"location": "isolated dark void", "time_of_day": "no ambient light, mark is sole illumination", "atmosphere": "imminent marking, technological branding"},
  {"rule": "centered symmetry", "foreground": "face and golden forehead mark in warm vivid tones",
   "background": "pure black void",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="golden glow emanating from the mark itself as sole light", fill="none — pure darkness", rim="faint warm edge on hair"),
  {"emotion": "imminent branding, technological mark of control", "tension": "absolute"},
  {"primary": "the forehead — the brain — the exact point on the magazine cover", "secondary": "circuit pattern as digital nature of the mark"},
  None)

# ---- Q58 ----
Q(58, "Altar farmaceutico", "Overhead bandeja de marmore com seringas, canetas injetoras, pilulas",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 50, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a marble tray viewed from above displaying golden syringes, injector pens, and colorful pills arranged like ritual offerings on a sacred altar, with incense smoke curling around them",
   "focal_point": "the central arrangement of syringes in a cross pattern",
   "secondary": "Pharmaceutical laboratory in monochrome behind.",
   "props": ["marble offering tray", "golden syringes in cross pattern", "injector pens", "colorful pills", "incense smoke curls", "pharmaceutical lab in P&B"]},
  {"location": "a pharmaceutical laboratory altar", "time_of_day": "warm overhead ritual lighting", "atmosphere": "pharmaceutical liturgy, medicine as worship"},
  {"rule": "centered symmetry", "foreground": "golden syringes and colorful pills in vivid warm tones",
   "background": "desaturated black-and-white laboratory equipment",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm overhead spot on the marble tray", fill="golden reflection from syringe surfaces"),
  {"emotion": "sacred pharmaceutical ritual, medicine deified", "tension": "rising"},
  {"primary": "syringes and pills as modern sacraments of the Beast", "secondary": "altar arrangement as worship of pharma"},
  None)

# ---- Q59 ----
Q(59, "Ozempic em pilula", "Medium frascos genericos com pilulas brilhando, fundo P&B farmaceutico",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 60, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "several generic pharmaceutical vials and a glowing pill capsule in amber-gold sitting on a sterile white surface, the pill casting warm light outward like a tiny sun",
   "focal_point": "the glowing amber pill capsule at center",
   "secondary": "Production line machinery in monochrome behind.",
   "props": ["generic pharmaceutical vials", "glowing amber pill capsule", "sterile white surface", "production line in P&B"]},
  {"location": "a pharmaceutical production facility", "time_of_day": "harsh clinical white light mixed with amber pill glow", "atmosphere": "new pharmaceutical cycle, the pill replaces the needle"},
  {"rule": "centered symmetry", "foreground": "glowing amber pill and vials in warm golden tones",
   "background": "desaturated black-and-white production machinery",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="clinical overhead white light", fill="amber glow from the pill capsule"),
  {"emotion": "pharmaceutical evolution, new delivery of control", "tension": "medium"},
  {"primary": "the pill as next generation of pharmaceutical control", "secondary": "glow as promise of salvation or damnation"},
  None)

# ---- Q60 ----
Q(60, "Helice de DNA dourada", "Wide helice DNA em cores douradas flutuando sobre fundo P&B de hospital",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a massive golden DNA double helix floating and rotating in the center of the frame, emitting warm amber light, surrounded by floating generic ampules with unreadable labels",
   "focal_point": "the center of the DNA helix where the strands intertwine",
   "secondary": "Hospital corridors in monochrome behind the floating helix.",
   "props": ["massive golden DNA double helix", "floating generic ampules", "amber light emission", "hospital corridors in P&B"]},
  {"location": "a hospital atrium with high ceilings", "time_of_day": "clinical lighting with golden DNA glow", "atmosphere": "biotechnology as new religion, genetic power"},
  {"rule": "centered symmetry", "foreground": "golden DNA helix in vivid warm amber and gold",
   "background": "desaturated black-and-white hospital corridors and ceiling",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="golden light emanating from DNA helix itself", fill="warm amber bounce on ampules", rim="gold edge on helix strands"),
  {"emotion": "biotechnological hegemony, genetic manipulation as power", "tension": "rising"},
  {"primary": "mRNA as the rewriting of human code — malaria, cancer, everything", "secondary": "DNA helix as golden idol of the new age"},
  None)

# ---- Q61 — VERSÍCULO Ap 18:23 PHARMAKEIA (PRO) ----
Q(61, "Pharmakeia", "Close-up pagina de livro grego antigo com a palavra PHARMAKEIA em dourado",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 100, "aperture": "f/2.0", "depth_of_field": "razor-thin", "aspect_ratio": "16:9"},
  {"primary": "an extreme close-up of an ancient Greek manuscript page in aged parchment, with the Greek word in golden calligraphy at center, illuminated by a single candle from the left side",
   "focal_point": "the golden Greek word at center of the page",
   "secondary": "Other faded Greek text surrounding the highlighted word. Candle wax drip on page edge.",
   "props": ["ancient Greek manuscript page", "golden calligraphy text", "beeswax candle", "wax drip on edge", "aged parchment texture"]},
  {"location": "a medieval scholar's reading desk", "time_of_day": "candlelight", "atmosphere": "etymological revelation, the original word revealed"},
  {"rule": "centered symmetry", "foreground": "golden Greek text on warm parchment tones",
   "background": "desaturated black-and-white desk and shadows",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="single candle from left illuminating the page", fill="golden glow from the highlighted text itself"),
  {"emotion": "revelation, the original word that explains everything", "tension": "high"},
  {"primary": "PHARMAKEIA — the Greek word John used means pharmacy/sorcery", "secondary": "etymology as decoder of prophecy"},
  {"enabled": True, "content": "PHARMAKEIA", "content_secondary": "pela tua feiticaria foram enganadas todas as nacoes — Apocalipse 18:23", "font_style": "ancient Greek uncial calligraphy in gold leaf", "medium": "handwritten on aged Greek manuscript page", "placement": "center of frame on the manuscript", "legibility": "crisp and readable", "language": "Greek"})

# ---- Q62 ----
Q(62, "Tres robos humanoides", "Medium tres robos em silhueta com olhos dourados, fundo fabrica P&B",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "three humanoid robots standing in a row in silhouette, each holding a different tool (wrench, tablet, scalpel), their eyes glowing golden in the dark, facing the viewer",
   "focal_point": "the golden glowing eyes of the central robot",
   "secondary": "Automated factory floor stretching behind in monochrome.",
   "props": ["three humanoid robot silhouettes", "wrench", "tablet", "scalpel", "golden glowing eyes", "automated factory floor in P&B"]},
  {"location": "an automated factory floor", "time_of_day": "industrial lighting, dim and cold", "atmosphere": "human replacement, the machines take over"},
  {"rule": "centered symmetry", "foreground": "robot silhouettes with golden glowing eyes",
   "background": "desaturated black-and-white factory production line",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="dim industrial overhead", fill="golden glow from robot eyes casting warm light on their torsos", rim="cool blue edge from factory lighting"),
  {"emotion": "replacement, humanity made obsolete", "tension": "rising"},
  {"primary": "Atlas, Optimus, Neo — the robots that complete the Beast's toolkit", "secondary": "golden eyes as intelligence that serves another master"},
  None)

# ---- Q63 ----
Q(63, "Trono vazio", "Wide trono vazio com coroa dourada, robos e seringas gigantes em P&B ao redor",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "an empty ornate golden throne at the center of a dark hall, with a small golden crown resting on the seat, surrounded by oversized robot silhouettes and giant syringe shapes in monochrome flanking both sides",
   "focal_point": "the golden crown resting on the empty throne seat",
   "secondary": "Robot silhouettes and giant syringes in P&B flanking the throne.",
   "props": ["ornate golden throne", "small golden crown on seat", "robot silhouettes in P&B", "giant syringe shapes in P&B", "dark ceremonial hall"]},
  {"location": "a dark ceremonial throne hall", "time_of_day": "single overhead spot on throne", "atmosphere": "abdication of humanity, the throne abandoned"},
  {"rule": "centered symmetry", "foreground": "golden throne and crown in vivid warm tones",
   "background": "desaturated black-and-white robots and syringes flanking the throne",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="single warm overhead spot illuminating only the throne", fill="none — darkness surrounds", rim="gold reflection on throne armrests"),
  {"emotion": "abdication, humanity surrenders its throne", "tension": "high"},
  {"primary": "the human no longer works, thinks or decides — machines and pills do it all", "secondary": "empty throne as the place humanity vacated"},
  None)

# ---- Q64 ----
Q(64, "Tanques convergentes", "Wide low-angle tres tanques com canhoes apontados para cima",
  {"type": "wide", "camera_angle": "low angle", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "three stylized war tanks in converging perspective from a low angle, their cannon barrels pointed upward toward a stormy sky, rendered in dark steel with warm amber reflections on their armor plating",
   "focal_point": "the central tank's cannon barrel pointing directly upward",
   "secondary": "Stormy sky in monochrome above. Ground debris in foreground.",
   "props": ["three war tanks in perspective", "upward-pointing cannon barrels", "dark steel armor with amber reflections", "stormy sky", "ground debris"]},
  {"location": "a battlefield with torn earth", "time_of_day": "overcast storm light with amber fire reflections", "atmosphere": "belligerence, military convergence"},
  {"rule": "centered symmetry", "foreground": "tanks in warm amber-reflected dark steel tones",
   "background": "desaturated black-and-white tempestuous sky",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="overcast diffused light from stormy sky", fill="warm amber fire reflections on armor", rim="gold edge on cannon barrels"),
  {"emotion": "war machine convergence, weapons pointed at the sky", "tension": "absolute"},
  {"primary": "tanks on the magazine cover — war is on the agenda", "secondary": "cannons pointed up as if challenging heaven"},
  None)

# ---- Q65 ----
Q(65, "Punho algemado", "Close-up punho cerrado com algema azul, sangue no pulso",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 85, "aperture": "f/2.0", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a clenched male fist with a blue steel handcuff locked around the wrist, blood trickling down from where the metal bites into skin, foreground in vivid warm-cool contrast",
   "focal_point": "the blue steel handcuff biting into the wrist with blood",
   "secondary": "Protest crowd in monochrome behind.",
   "props": ["clenched fist", "blue steel handcuff", "blood trickling from wrist", "protest crowd in P&B"]},
  {"location": "an urban protest setting", "time_of_day": "harsh daylight", "atmosphere": "repressed resistance, freedom chained"},
  {"rule": "rule of thirds", "foreground": "fist in warm skin tones with blue-steel cuff and crimson blood",
   "background": "desaturated black-and-white protest crowd",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="harsh overhead daylight", fill="warm ambient", rim="blue steel reflection on cuff surface"),
  {"emotion": "resistance repressed, freedom in chains", "tension": "high"},
  {"primary": "the blue handcuff on the magazine cover — civil liberties chained", "secondary": "blood as cost of resistance"},
  None)

# ---- Q66 ----
Q(66, "Martelo rachado", "Medium martelo de juiz dourado rachado ao meio sobre mesa de tribunal",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 60, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a golden judge's gavel cracked in half lying on an empty Gothic tribunal desk, the two halves separated with a thin line of golden light between them",
   "focal_point": "the fracture line between the two gavel halves emitting golden light",
   "secondary": "Gothic arch above the empty bench. Dust motes in light beam.",
   "props": ["cracked golden gavel in two halves", "golden light from fracture", "Gothic tribunal desk", "Gothic arch", "dust motes"]},
  {"location": "a medieval Gothic courtroom", "time_of_day": "dim torchlight from above", "atmosphere": "justice broken, the law itself failed"},
  {"rule": "centered symmetry", "foreground": "golden gavel halves in warm vivid gold tones",
   "background": "desaturated black-and-white Gothic courtroom architecture",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="golden light emanating from the gavel fracture", fill="warm torchlight from above"),
  {"emotion": "justice broken, the system itself cracked", "tension": "high"},
  {"primary": "the cracked gavel on the magazine — justice no longer functions", "secondary": "golden light from the break as truth escaping failed institutions"},
  None)

# ---- Q67 ----
Q(67, "Sala Bilderberg", "Wide sala de conferencia europeia estilo castelo com cadeiras vazias e auras",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a long conference table in a Scandinavian castle hall with tall empty carved chairs, each chair surrounded by a warm golden aura as if its invisible occupant still radiates power, floating embers above the table",
   "focal_point": "the warm golden auras around each empty chair",
   "secondary": "Tall Gothic windows in monochrome. Candles in sconces along walls. Floating embers.",
   "props": ["long conference table", "empty carved wooden chairs with golden auras", "tall Gothic windows in P&B", "wall sconce candles", "floating embers"]},
  {"location": "a Scandinavian castle conference hall", "time_of_day": "candlelight evening", "atmosphere": "ghostly meeting, invisible power gathered"},
  {"rule": "centered symmetry", "foreground": "chairs with golden auras in warm rich tones",
   "background": "desaturated black-and-white castle hall windows and stone walls",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="candle sconces along walls casting warm lateral light", fill="golden aura glow from each chair", rim="gold edge on chair carvings"),
  {"emotion": "ghostly meeting, the powerful were just here", "tension": "rising"},
  {"primary": "Bilderberg 71st meeting — the chairs still warm with power", "secondary": "golden auras as residual influence of the invisible attendees"},
  None)

# ---- Q68 ----
Q(68, "Editora-chefe", "Medium mulher editora-chefe anonima em sala de conferencia, so ela em cores",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "an anonymous British female editor-in-chief, approximately 50 years old, blonde hair in a bun, wearing a brown earth-toned dress, seated in one of the conference chairs from Q67, she alone rendered in rich warm colors while everything else is monochrome",
   "focal_point": "her hands clasped on the table surface",
   "secondary": "Empty chairs in monochrome flanking her. Conference table stretching away.",
   "props": ["anonymous blonde British woman", "brown earth-toned dress", "conference chair", "clasped hands on table", "monochrome empty chairs around"]},
  {"location": "the same Scandinavian castle conference hall as Q67", "time_of_day": "candle and window light", "atmosphere": "interior witness, the one who was there"},
  {"rule": "rule of thirds", "foreground": "editor in vivid warm brown and gold tones — only color in the frame",
   "background": "desaturated black-and-white conference hall",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm candlelight from left illuminating her face and hands", fill="cool window light from right", rim="gold edge on hair bun"),
  {"emotion": "interior witness, she was there and she knows", "tension": "rising"},
  {"primary": "the editor-in-chief at Bilderberg — the insider witness", "secondary": "her being the only color in a grey room — she is the link"},
  None)

# ---- Q69 ----
Q(69, "Cinco envelopes lacrados", "Overhead cinco envelopes lacrados com cera vermelha sobre veludo",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 50, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "five sealed parchment envelopes in a row on dark velvet cloth, each sealed with red wax and bearing a small distinct golden icon: tank, missile, fist, cake, lightning bolt, numbered 1-5",
   "focal_point": "the red wax seals on each envelope",
   "secondary": "Candle dripping at edge of frame. Dark velvet texture.",
   "props": ["five sealed parchment envelopes", "red wax seals", "golden icons on each: tank, missile, fist, cake, lightning", "dark velvet cloth", "dripping candle"]},
  {"location": "a private desk covered in dark velvet", "time_of_day": "candlelight", "atmosphere": "secret agenda, sealed orders"},
  {"rule": "centered symmetry", "foreground": "envelopes and wax seals in vivid crimson and gold",
   "background": "deep black velvet",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm candle from left illuminating seals", fill="golden glow from tiny icons"),
  {"emotion": "secret agenda, sealed marching orders", "tension": "high"},
  {"primary": "five themes of Bilderberg — sealed like orders from a hidden council", "secondary": "wax seals as secrecy and authority"},
  None)

# ---- Q70 ----
Q(70, "Cinco vitrais tematicos", "Wide cinco cartuchos goticos verticais como vitrais com imagens tematicas",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 28, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "five vertical Gothic stained glass cartouches in a cathedral wall, each containing a symbolic image: (1) three authoritarian silhouettes, (2) a burning map, (3) a raised fist, (4) a military pie chart, (5) a lightning bolt energy grid — all in warm colored glass",
   "focal_point": "the central stained glass panel (the fist)",
   "secondary": "Gothic stone tracery between panels. Cathedral in monochrome behind.",
   "props": ["five Gothic stained glass cartouches", "authoritarian silhouettes", "burning map", "raised fist", "military pie", "energy lightning bolt", "Gothic stone tracery"]},
  {"location": "a Gothic cathedral with five adjacent stained glass windows", "time_of_day": "daylight filtering through stained glass", "atmosphere": "sacred agenda, Bilderberg themes rendered as holy scripture"},
  {"rule": "centered symmetry", "foreground": "five stained glass windows in vivid warm colors",
   "background": "desaturated black-and-white cathedral interior",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="daylight through stained glass casting colored light pools on floor", fill="ambient warm glow from all five panels"),
  {"emotion": "sacred agenda, the meeting made cathedral art", "tension": "high"},
  {"primary": "five Bilderberg topics turned into stained glass — as if holy scripture", "secondary": "the cathedral as temple of power"},
  None)

# ---- Q71 ----
Q(71, "Revista com cinco simbolos", "Overhead capa revista analoga com cinco simbolos exatos do Bilderberg",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "an unbranded editorial magazine spread open viewed from above, with the same five symbols from Q70 (silhouettes, burning map, fist, pie, lightning) visible in the margins of its pages, connected by lines of golden fire linking each symbol",
   "focal_point": "the golden fire lines connecting the five symbols",
   "secondary": "Desk surface in monochrome. Quill pen beside.",
   "props": ["open unbranded magazine", "five matching symbols in margins", "golden fire connection lines", "desk surface in P&B", "quill pen"]},
  {"location": "a dark writing desk", "time_of_day": "warm lamplight", "atmosphere": "impossible coincidence — meeting agenda matches the magazine"},
  {"rule": "centered symmetry", "foreground": "magazine with golden fire connections in vivid warm tones",
   "background": "desaturated black-and-white desk",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm desk lamp illuminating magazine", fill="golden glow from fire connection lines"),
  {"emotion": "impossible coincidence, the proof is visual", "tension": "absolute"},
  {"primary": "every Bilderberg topic became a magazine symbol — in order", "secondary": "golden fire as the hidden hand connecting them"},
  None)

# ---- Q72 ----
Q(72, "Ata de reuniao lacrada", "Close-up caderno antigo de ata lacrado por fita vermelha",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 85, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "an antique leather-bound meeting minutes notebook sealed with a red ribbon and wax seal, lying on a dark monochrome desk surface, the red ribbon and golden wax catching warm candlelight",
   "focal_point": "the red ribbon and wax seal closure",
   "secondary": "Desk surface in monochrome.",
   "props": ["antique leather notebook", "red ribbon seal", "golden wax seal", "dark desk surface", "candlelight"]},
  {"location": "a dark executive desk", "time_of_day": "candlelight", "atmosphere": "the rhetorical question — is this journalism or meeting minutes?"},
  {"rule": "rule of thirds", "foreground": "notebook and red seal in vivid warm crimson and gold",
   "background": "desaturated black-and-white desk and shadows",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm candlelight from left", fill="crimson reflection from ribbon"),
  {"emotion": "rhetorical accusation — journalism or secret agenda?", "tension": "high"},
  {"primary": "is this a magazine or meeting minutes? The question that condemns", "secondary": "sealed notebook as classified information"},
  None)

# ---- Q73 ----
Q(73, "Revista como altar", "Overhead panoramico da revista analoga em tela cheia iluminada como altar",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 24, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a full-frame overhead view of an unbranded editorial magazine open to its center spread, with all ten symbols visible around its margins, illuminated like a sacred altar by warm golden light from above, occupying the entire frame",
   "focal_point": "the center spread of the magazine as altar",
   "secondary": "Ten symbols arrayed around the edges. Incense smoke wisps.",
   "props": ["unbranded magazine center spread", "ten symbolic icons around margins", "warm golden altar light", "incense smoke wisps"]},
  {"location": "viewed from directly above as if a sacred object on display", "time_of_day": "divine golden light from above", "atmosphere": "terminal synthesis, the complete revelation"},
  {"rule": "centered symmetry", "foreground": "illuminated magazine spread in vivid warm golden tones",
   "background": "pure dark edges fading to black",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="divine golden light from directly above", fill="warm glow from magazine pages"),
  {"emotion": "complete synthesis, everything revealed", "tension": "absolute"},
  {"primary": "the magazine as altar — all ten symbols, all five themes, one document", "secondary": "overhead view as God's-eye perspective on human conspiracy"},
  None)

# ---- Q74 ----
Q(74, "Linha do tempo em pedra", "Wide linha do tempo gravada em pedra com marcos iluminados",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a horizontal timeline carved into a massive stone wall, with four dates marked by golden glowing points: 10NOV, 15NOV, 17MAR, and one future point still dark, connected by an engraved gold line",
   "focal_point": "the golden glowing date markers along the timeline",
   "secondary": "City skyline in monochrome behind the stone wall.",
   "props": ["massive stone wall", "carved timeline with golden date points", "engraved gold connecting line", "dark future point", "city skyline in P&B"]},
  {"location": "a monumental stone wall in a city plaza", "time_of_day": "golden hour lateral light", "atmosphere": "fateful chronology, dates that matter"},
  {"rule": "rule of thirds", "foreground": "golden date points and carved timeline in warm tones",
   "background": "desaturated black-and-white city skyline",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="golden hour lateral light illuminating the stone wall", fill="warm glow from date points"),
  {"emotion": "chronological fatality, dates written in stone", "tension": "rising"},
  {"primary": "the timeline of events — publication, sale, exit — all planned", "secondary": "stone carving as permanence of the plan"},
  None)

# ---- Q75 ----
Q(75, "Mao aristocratica assinando", "Close-up mao feminina aristocratica assinando contrato de venda",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 100, "aperture": "f/2.0", "depth_of_field": "razor-thin", "aspect_ratio": "16:9"},
  {"primary": "an aristocratic female hand with a delicate wrist, partial silk glove, gold bracelet, and a family crest ring, signing a document with an ornate fountain pen on a dark desk surface",
   "focal_point": "the pen tip touching the signature line on the document",
   "secondary": "Document with partial text visible but not readable. Desk in monochrome.",
   "props": ["aristocratic female hand", "partial silk glove", "gold bracelet", "family crest ring", "ornate fountain pen", "signing document"]},
  {"location": "a private executive office desk", "time_of_day": "warm desk lamp", "atmosphere": "calculated exit, the signature of departure"},
  {"rule": "rule of thirds", "foreground": "hand and pen in vivid warm gold and silk tones",
   "background": "desaturated black-and-white desk surface",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm desk lamp from upper-left", fill="golden reflection from bracelet and ring"),
  {"emotion": "calculated departure, the surgical exit", "tension": "high"},
  {"primary": "the Rothschild exit — signed, sealed, delivered", "secondary": "aristocratic hand as old money departing with precision"},
  None)

# ---- Q76 ----
Q(76, "Editora retornando", "Medium editora de Q68 em sala de redacao P&B, retornando com pasta",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "the same anonymous British female editor from Q68, now walking through a monochrome newsroom carrying a leather portfolio case, airplane shadow reflected on the office window behind her, she alone in warm rich tones",
   "focal_point": "the leather portfolio case in her hand",
   "secondary": "Newsroom desks and monitors in monochrome. Airplane reflection on window.",
   "props": ["anonymous British female editor", "leather portfolio case", "monochrome newsroom", "airplane shadow on window"]},
  {"location": "a modern newsroom office", "time_of_day": "daylight through office windows", "atmosphere": "insider returning with privileged information"},
  {"rule": "rule of thirds", "foreground": "editor in warm brown and gold tones — only color",
   "background": "desaturated black-and-white newsroom",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="daylight from office windows behind", fill="warm ambient on her figure", rim="gold edge on portfolio case"),
  {"emotion": "privileged information, the insider returns", "tension": "rising"},
  {"primary": "editor-in-chief back from Bilderberg — carrying the agenda", "secondary": "airplane shadow as proof of the trip"},
  None)

# ---- Q77 ----
Q(77, "Tom Standage fecha livro", "Medium editor Tom Standage fechando livro dourado na escrivaninha",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "the same anonymous Victorian editor from Q39, now closing a large golden leather-bound book on his desk with finality, both hands pressing down on the cover, stern expression",
   "focal_point": "the hands pressing down on the golden book cover",
   "secondary": "Recording studio equipment visible in monochrome behind.",
   "props": ["anonymous Victorian editor with spectacles", "large golden leather-bound book", "hands pressing on cover", "recording studio equipment in P&B"]},
  {"location": "a Victorian study converted into recording studio", "time_of_day": "warm oil lamp light", "atmosphere": "case closed, the declaration is final"},
  {"rule": "centered symmetry", "foreground": "editor and golden book in warm rich tones",
   "background": "desaturated black-and-white studio equipment",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm oil lamp from left", fill="golden reflection from book cover", rim="gold on spectacle rims"),
  {"emotion": "finality, the statement is made and the book closed", "tension": "high"},
  {"primary": "the editor closing the book — the confession is complete", "secondary": "golden book as the document of prophecy-made-journalism"},
  None)

# ---- Q78 — BOMBSHELL (PRO) ----
Q(78, "Rothschild sai / Smith entra", "Split dramatico: silhueta feminina saindo, masculina entrando, mesa central",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a dramatic split-frame composition: LEFT half shows a female aristocratic silhouette in a flowing crimson cloak and small golden crown exiting through a Gothic archway to the left; RIGHT half shows a male silhouette in a dark Canadian suit and fedora entering through a Gothic archway on the right, carrying a briefcase with golden clasps. CENTER: an empty council table lit by a golden candelabrum with an open parchment scroll. Black-and-white checkered marble floor. Floating embers throughout.",
   "focal_point": "the golden candelabrum and open parchment scroll at dead center of the table",
   "secondary": "Both figures in rich warm silhouette tones against the Gothic archways. Empty council chamber in P&B.",
   "props": ["female silhouette in crimson cloak with golden crown exiting left", "male silhouette in dark suit with fedora and golden-clasp briefcase entering right", "empty council table at center", "golden candelabrum", "open parchment scroll", "black-and-white checkered marble floor", "floating embers"]},
  {"location": "a Gothic council chamber with two opposing archways", "time_of_day": "candlelight from central candelabrum", "atmosphere": "conspiratorial handoff, the changing of the guard"},
  {"rule": "centered symmetry", "foreground": "both silhouetted figures in rich warm crimson and dark tones",
   "midground": "empty table with golden candelabrum and parchment",
   "background": "desaturated black-and-white Gothic chamber architecture",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="golden candelabrum at center illuminating the table and scroll", fill="warm amber bounce from checkered floor", rim="crimson edge on female cloak, dark edge on male suit", mood="golden candlelight center with dark contre-jour edges"),
  {"emotion": "conspiratorial transfer of power, the guard changes", "tension": "absolute"},
  {"primary": "Rothschild exits, Smith enters — the transfer of power at the Economist", "secondary": "empty table and parchment as the deal already done"},
  None)

# ---- Q79 — VERSÍCULO Ap 17:12 (PRO) ----
Q(79, "Pergaminho Apocalipse 17", "Wide pergaminho gigantesco com caligrafia gotica de Ap 17:12, catedral P&B",
  {"type": "wide", "camera_angle": "low angle", "focal_length_mm": 28, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a gigantic parchment scroll hanging from the ceiling of a Gothic cathedral, bearing the Bible verse text in large golden Gothic calligraphy, illuminated by a vertical beam of divine light",
   "focal_point": "the golden calligraphic text on the parchment center",
   "secondary": "Cathedral ribbed vaulting in monochrome above. Stone floor below.",
   "props": ["gigantic hanging parchment scroll", "golden Gothic calligraphy", "vertical divine light beam", "Gothic cathedral interior in P&B", "stone floor"]},
  {"location": "inside a massive Gothic cathedral nave", "time_of_day": "divine light beam from above, cathedral interior otherwise dim", "atmosphere": "sacred revelation, the Word of God displayed in grandeur"},
  {"rule": "centered symmetry", "foreground": "parchment with golden text in vivid warm tones",
   "background": "desaturated black-and-white cathedral ribbed vaulting and columns",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="vertical divine golden light beam from above illuminating the scroll", fill="faint amber from cathedral candles", rim="gold edge on parchment edges"),
  {"emotion": "sacred grandeur, the Word displayed in its full authority", "tension": "absolute"},
  {"primary": "Revelation 17:12 — ten horns are ten kings who receive power with the Beast", "secondary": "cathedral as scale befitting the Word of God"},
  {"enabled": True, "content": "E os dez chifres que viste sao dez reis, que ainda nao receberam o reino", "content_secondary": "Apocalipse 17:12", "font_style": "ancient gothic calligraphy in gold leaf, large scale", "medium": "inscribed on gigantic hanging parchment scroll in cathedral", "placement": "center of frame on the scroll", "legibility": "crisp and readable at large scale", "language": "Portuguese"})

# ---- Q80 — VERSÍCULO Ap 17:13 (PRO) ----
Q(80, "Dez reis diante da besta", "Medium dez figuras coroadas ajoelhadas diante de besta sombria",
  {"type": "medium", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "ten crowned figures in crimson and ochre royal robes kneeling in a row before a massive shadowy beast silhouette, its seven heads barely visible in the background darkness, a stone wall behind the beast bearing the verse inscription",
   "focal_point": "the ten kneeling crowned figures in submission",
   "secondary": "Massive beast silhouette behind in monochrome. Verse carved in stone wall behind beast.",
   "props": ["ten crowned figures in crimson and ochre robes", "kneeling poses", "massive seven-headed beast silhouette", "stone wall with carved verse", "dark ceremonial hall"]},
  {"location": "a vast dark ceremonial hall", "time_of_day": "dim torchlight from walls", "atmosphere": "prophetic submission, kings surrendering to the Beast"},
  {"rule": "centered symmetry", "foreground": "ten kings in vivid crimson, ochre and gold",
   "midground": "shadowy beast silhouette in P&B",
   "background": "desaturated black-and-white stone wall with verse inscription",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="torchlight from walls illuminating the kneeling kings", fill="faint crimson from beast's eyes", rim="gold on crowns"),
  {"emotion": "prophetic submission, the kings willingly surrender their power", "tension": "absolute"},
  {"primary": "Revelation 17:13 — they have one purpose and give their power to the Beast", "secondary": "ten kings as modern power brokers bowing to a greater force"},
  {"enabled": True, "content": "Estes tem um mesmo intento, e entregarao o seu poder e autoridade a besta.", "content_secondary": "Apocalipse 17:13", "font_style": "carved stone serif, deep relief", "medium": "etched in stone wall behind the kneeling kings", "placement": "upper background behind the beast silhouette", "legibility": "crisp and readable", "language": "Portuguese"})

# ---- Q81 — COSMOGRAMA (PRO, no verse) ----
Q(81, "Cosmograma dos dez simbolos", "Overhead circulo perfeito com dez simbolos dourados e besta central",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 35, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a perfect golden circle viewed from above like a clock face, with ten distinct golden symbols arranged at each hour position: handcuffed cake, fist, brain-joystick, plunging graph, football-globe, tank, missile, syringe, robot, cracked gavel. At the exact center, a seven-headed beast rendered in blood-red crimson against a pure black background",
   "focal_point": "the seven-headed beast at dead center",
   "secondary": "Golden connecting lines between each symbol forming a decagon. Pure black background.",
   "props": ["ten golden symbols in circle", "golden connecting decagon lines", "seven-headed crimson beast at center", "pure black background"]},
  {"location": "abstract void — pure symbolic composition", "time_of_day": "no natural light — symbols self-illuminated", "atmosphere": "apocalyptic cosmogram, the complete cipher"},
  {"rule": "centered symmetry", "foreground": "golden symbols and crimson beast in vivid warm tones",
   "background": "pure black void",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="golden self-illumination from each symbol", fill="crimson glow from the central beast", rim="gold edge on connecting lines"),
  {"emotion": "the complete cipher decoded — ten horns, one Beast, one purpose", "tension": "absolute"},
  {"primary": "ten magazine symbols arranged like ten horns around the Beast — Revelation decoded", "secondary": "clock arrangement as agenda with timeline"},
  None)

# ---- Q82 ----
Q(82, "Relogio 23:58:35", "Close-up relogio antigo marcando 23:58:35, ponteiros dourados",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 100, "aperture": "f/2.0", "depth_of_field": "razor-thin", "aspect_ratio": "16:9"},
  {"primary": "an antique wall clock with Roman numerals, golden hands pointing to 23:58:35, the second hand trembling, warm amber light on the clock face against a dark wall",
   "focal_point": "the golden clock hands at 23:58:35",
   "secondary": "Dark wall in monochrome. Faint dust motes around clock.",
   "props": ["antique wall clock with Roman numerals", "golden trembling hands at 23:58:35", "dark wall", "dust motes"]},
  {"location": "a dark institutional wall", "time_of_day": "dim ambient with clock face lit", "atmosphere": "terminal countdown, the schedule is written on the cover"},
  {"rule": "centered symmetry", "foreground": "golden clock face and hands in vivid warm tones",
   "background": "desaturated black-and-white dark wall",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm amber light illuminating clock face from left", fill="golden glow from clock numerals"),
  {"emotion": "terminal, the delivery time is on the cover", "tension": "absolute"},
  {"primary": "the agenda has a delivery schedule — and the time is almost up", "secondary": "85 seconds to midnight as literal countdown"},
  None)

# ---- Q83 ----
Q(83, "Sexta moldura vazia", "Wide retorno galeria — agora com seis molduras, a sexta vazia",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "the same Gothic gallery from Q12 and Q24, now with SIX ornate frames on the wall — the first five bearing burned golden checkmarks, the sixth frame still empty, illuminated by a vertical golden light beam waiting",
   "focal_point": "the empty sixth frame under the golden light beam",
   "secondary": "Five confirmed frames to the left. Empty frame at right glowing expectantly.",
   "props": ["six ornate gilded frames", "five with golden checkmarks", "one empty frame under divine light", "Gothic gallery architecture"]},
  {"location": "the same Gothic gallery from Q12/Q24", "time_of_day": "warm golden light with divine beam on empty frame", "atmosphere": "terminal expectation, awaiting 2026's confirmation"},
  {"rule": "rule of thirds", "foreground": "empty sixth frame under golden beam in warm tones",
   "background": "desaturated black-and-white Gothic gallery",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="vertical divine golden beam on the empty sixth frame", fill="warm amber from the five checkmarked frames"),
  {"emotion": "anticipation, the sixth prophecy awaiting fulfillment", "tension": "absolute"},
  {"primary": "if they got five right, what about the sixth?", "secondary": "empty frame as 2026 waiting to be confirmed"},
  None)

# ---- Q84 ----
Q(84, "Rosto brasileiro suando", "Close-up frontal homem brasileiro comum, 40 anos, suando, luz vermelha",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 85, "aperture": "f/2.0", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "an intense frontal close-up of a common Brazilian man, approximately 40 years old, mature face with stubble, eyes half-hidden in shadow, sweating, illuminated by harsh red lateral light",
   "focal_point": "the sweat droplets on his forehead catching red light",
   "secondary": "Living room furniture in monochrome behind him.",
   "props": ["Brazilian man's face with stubble", "sweat droplets on forehead", "harsh red lateral light", "living room in P&B"]},
  {"location": "a Brazilian living room", "time_of_day": "night, red lateral light source", "atmosphere": "personal summoning, the viewer confronted"},
  {"rule": "centered symmetry", "foreground": "face in warm skin tones lit by crimson light",
   "background": "desaturated black-and-white living room",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="harsh crimson lateral light from left", fill="none — deep shadow on right half", rim="warm sweat highlights on forehead"),
  {"emotion": "personal confrontation, the question aimed at the viewer", "tension": "absolute"},
  {"primary": "the question is not IF — it's how long you'll take to believe", "secondary": "common man as the viewer's mirror"},
  None)

# ---- Q85 ----
Q(85, "Quatro testemunhos no altar", "Wide quatro pecas iluminadas sobre altar: pergaminho, microfone, revista, relogio",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "four illuminated objects on a sacred stone altar: a parchment scroll with wax seal (Rothschild), a golden vintage microphone (Ressa), an unbranded magazine (Economist), and a Doomsday clock face (85 seconds) — all in rich warm tones under dramatic overhead lighting",
   "focal_point": "the center of the altar where all four objects converge",
   "secondary": "Dark cathedral backdrop in monochrome.",
   "props": ["parchment scroll with wax seal", "golden vintage microphone", "unbranded magazine", "Doomsday clock face at 85 seconds", "sacred stone altar"]},
  {"location": "a dark cathedral altar", "time_of_day": "dramatic overhead spotlights on each object", "atmosphere": "witnesses assembled, all testimony gathered"},
  {"rule": "centered symmetry", "foreground": "four objects in vivid gold, crimson, amber tones",
   "background": "desaturated black-and-white cathedral backdrop",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="four individual overhead spots on each object", fill="warm ambient from altar candles"),
  {"emotion": "all witnesses assembled — the case is made", "tension": "absolute"},
  {"primary": "Rothschild sold, Ressa warned, Standage confessed, Doomsday says 85 seconds", "secondary": "altar as courtroom where evidence is presented to God"},
  None)

# ---- Q86 ----
Q(86, "Xicara de cafe e carta", "Overhead xicara de cafe fumegante ao lado de carta dobrada",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a steaming cup of dark coffee on a simple ceramic saucer beside a folded handwritten letter on a humble kitchen counter, illuminated by warm golden lateral light",
   "focal_point": "the steam rising from the coffee catching the golden light",
   "secondary": "Simple kitchen counter in monochrome.",
   "props": ["steaming dark coffee in ceramic cup", "ceramic saucer", "folded handwritten letter", "simple kitchen counter", "warm golden light"]},
  {"location": "a simple Brazilian kitchen counter", "time_of_day": "early morning golden light from window", "atmosphere": "personal time, the moment of decision"},
  {"rule": "rule of thirds", "foreground": "coffee and letter in warm golden-amber tones",
   "background": "desaturated black-and-white kitchen",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm golden morning light from window at left", fill="warm steam glow"),
  {"emotion": "personal decision time — 85 seconds to drink coffee or decide", "tension": "medium"},
  {"primary": "85 seconds is the time for a coffee or a decision", "secondary": "folded letter as the message received but not yet opened"},
  None)

# ---- Q87 ----
Q(87, "Tres pergaminhos serie", "Wide tres pergaminhos pendurados em varais de ouro com icones",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "three parchment scrolls hanging from golden wire clotheslines side by side, each bearing a different golden icon: (1) a magazine, (2) a dove of rapture, (3) a red horse, representing the three-video series",
   "focal_point": "the three scrolls as a series announcement",
   "secondary": "Dark background. Golden clips holding scrolls.",
   "props": ["three hanging parchment scrolls", "golden wire clotheslines", "magazine icon on scroll 1", "dove icon on scroll 2", "red horse icon on scroll 3", "golden clips"]},
  {"location": "abstract dark display space", "time_of_day": "warm overhead spotlights on each scroll", "atmosphere": "series announcement, trilogy revealed"},
  {"rule": "centered symmetry", "foreground": "three scrolls in warm parchment and gold tones",
   "background": "pure dark void",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="three overhead spots illuminating each scroll", fill="warm golden ambient"),
  {"emotion": "series announcement, there is more to come", "tension": "medium"},
  {"primary": "this video is the first of three — agenda, escape, judgement", "secondary": "three scrolls as three chapters of the same prophecy"},
  None)

# ---- Q88 ----
Q(88, "Porta gotica entreaberta", "Close porta gotica entreaberta com luz dourada fortissima escapando",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/2.0", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a Gothic stone doorway slightly ajar, with an intensely bright golden-white light flooding through the narrow opening, everything else in total darkness, the door edge glowing",
   "focal_point": "the narrow opening where blinding golden light escapes",
   "secondary": "Complete darkness everywhere except the door crack. Dust particles in the light beam.",
   "props": ["Gothic stone doorway", "slightly ajar heavy door", "intense golden-white light through crack", "total darkness surroundings", "dust in light beam"]},
  {"location": "a dark corridor leading to the door", "time_of_day": "no ambient light — all light from beyond the door", "atmosphere": "hope, escape route, the way out"},
  {"rule": "centered symmetry", "foreground": "blinding golden light through door crack",
   "background": "total black darkness",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="intense golden-white light flooding through door crack", fill="none — pure darkness", rim="gold edge on door frame"),
  {"emotion": "hope amidst darkness, the escape route exists", "tension": "rising"},
  {"primary": "the next video shows the escape route — the Rapture", "secondary": "light through the crack as salvation available but narrow"},
  None)

# ---- Q89 ----
Q(89, "Quatro luas de sangue", "Wide quatro luas cheias carmesim sobre cidade em ruinas P&B",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "four full blood-red moons aligned horizontally across the sky over a ruined cityscape, with falling stars streaking between them, the moons in vivid deep crimson",
   "focal_point": "the four crimson moons in alignment",
   "secondary": "Ruined city skyline in monochrome below. Falling stars between moons.",
   "props": ["four blood-red full moons", "falling stars", "ruined cityscape in P&B", "deep crimson sky"]},
  {"location": "above a ruined modern city", "time_of_day": "apocalyptic night with crimson moons", "atmosphere": "apocalyptic lyrical, the blood moons announced"},
  {"rule": "centered symmetry", "foreground": "four crimson moons in vivid blood-red",
   "background": "desaturated black-and-white ruined city below",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="crimson moonlight from four blood moons", fill="faint star-trail light"),
  {"emotion": "apocalyptic lyrical beauty, the signs in the sky", "tension": "high"},
  {"primary": "four blood moons — the sign RaptureTok is shouting about", "secondary": "falling stars as biblical signs of the end"},
  None)

# ---- Q90 ----
Q(90, "Porta celestial fechando", "Medium porta celestial dourada se fechando, ultima sombra passando",
  {"type": "medium", "camera_angle": "low angle", "focal_length_mm": 40, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a massive celestial golden gate slowly closing, the last human shadow slipping through the narrowing gap, the light beam from inside reducing to a sliver",
   "focal_point": "the narrowing gap as the gate closes",
   "secondary": "Brilliant golden light inside the gate diminishing. Dark exterior.",
   "props": ["massive golden celestial gate", "closing gap", "last human shadow slipping through", "diminishing golden light", "dark exterior"]},
  {"location": "the threshold between earth and heaven", "time_of_day": "divine golden light inside, darkness outside", "atmosphere": "definitive closure, the last chance passing"},
  {"rule": "centered symmetry", "foreground": "golden gate and diminishing light in vivid warm tones",
   "background": "pure darkness outside",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="brilliant golden light from inside the gate", fill="none — exterior darkness", rim="gold on gate edges"),
  {"emotion": "the door is closing — last chance to enter", "tension": "absolute"},
  {"primary": "the only door that closes before judgement begins — the Rapture", "secondary": "last shadow as the final person to make it through"},
  None)

# ---- Q91 ----
Q(91, "Cavalo vermelho galopando", "Wide cavalo vermelho apocaliptico com cavaleiro, espada elevada",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 28, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a massive red apocalyptic horse galloping from left to right, its rider in a flowing crimson cloak raising a broad sword overhead, mane and cloak streaming in the wind",
   "focal_point": "the raised sword catching golden light",
   "secondary": "Battle scene in monochrome in the background with explosions and smoke.",
   "props": ["massive red horse galloping", "rider in crimson cloak", "raised broad sword", "streaming mane and cloak", "battle scene in P&B"]},
  {"location": "a vast battlefield", "time_of_day": "fiery dusk with battle smoke", "atmosphere": "imminent divine punishment, the Red Horse rides"},
  {"rule": "dynamic asymmetric", "foreground": "horse and rider in vivid crimson and gold",
   "background": "desaturated black-and-white battle scene",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="fiery dusk ambient with golden light on sword", fill="warm amber from battle fires", rim="crimson edge on cloak and horse"),
  {"emotion": "divine wrath unleashed, war comes for those who remain", "tension": "absolute"},
  {"primary": "the Second Seal — the Red Horse of war for those left behind", "secondary": "sword raised as judgement about to strike"},
  None)

# ---- Q92 ----
Q(92, "Botao de inscricao", "Close-up mao apertando botao dourado abstrato estilizado como inscricao",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 100, "aperture": "f/2.0", "depth_of_field": "razor-thin", "aspect_ratio": "16:9"},
  {"primary": "a hand pressing down on a large abstract golden button shaped like a medieval seal press, glowing with warm amber light upon contact, no brand or logo visible",
   "focal_point": "the finger pressing the golden button at the moment of contact",
   "secondary": "Dark background. Warm glow emanating from the pressed button.",
   "props": ["abstract golden seal-press button", "pressing finger", "warm amber contact glow", "dark background"]},
  {"location": "abstract dark space", "time_of_day": "button glow as sole light", "atmosphere": "direct action, subscribe now"},
  {"rule": "centered symmetry", "foreground": "golden button and hand in vivid warm tones",
   "background": "pure black",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm amber glow from the button upon pressing", fill="none"),
  {"emotion": "urgent call to action, do it now", "tension": "high"},
  {"primary": "subscribe — rendered as a sacred act of commitment", "secondary": "golden seal press as ancient compact between viewer and channel"},
  None)

# ---- Q93 ----
Q(93, "Sino dourado", "Close sino antigo dourado com badalo balancando",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 60, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "an ancient golden church bell with its clapper swinging mid-strike, warm golden light pulsing outward from the impact point, viewed from below looking up",
   "focal_point": "the clapper striking the bell wall with golden light burst",
   "secondary": "Dark bell tower interior. Rope hanging below.",
   "props": ["ancient golden church bell", "swinging clapper", "golden light pulse from impact", "bell tower interior", "rope"]},
  {"location": "inside a dark church bell tower", "time_of_day": "no ambient — golden bell glow only", "atmosphere": "sacred alarm, the notification bell rings"},
  {"rule": "centered symmetry", "foreground": "golden bell in vivid warm tones",
   "background": "desaturated black-and-white bell tower interior",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="golden light pulsing from bell impact point", fill="warm ambient bounce from bell interior"),
  {"emotion": "alarm, activation, the bell tolls", "tension": "rising"},
  {"primary": "activate the bell — rendered as a sacred church alarm", "secondary": "bell as the watchman's call"},
  None)

# ---- Q94 ----
Q(94, "Teclado ARREBATAMENTO", "Overhead teclado de celular formando palavra ARREBATAMENTO em dourado",
  {"type": "overhead", "camera_angle": "overhead", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a smartphone keyboard viewed from directly above, with glowing golden letters forming the word ARREBATAMENTO one letter at a time on the screen above the keyboard, warm amber glow from each typed letter",
   "focal_point": "the golden word ARREBATAMENTO forming on screen",
   "secondary": "Hands typing on sides of phone. Dark table surface.",
   "props": ["smartphone with keyboard", "golden letters spelling ARREBATAMENTO", "amber letter glow", "hands on phone sides", "dark table"]},
  {"location": "a dark table surface", "time_of_day": "screen-lit night", "atmosphere": "collective ritual, the audience types the sacred word"},
  {"rule": "centered symmetry", "foreground": "golden word and phone screen in vivid warm tones",
   "background": "pure dark table surface",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm phone screen glow", fill="amber from golden letters"),
  {"emotion": "collective ritual, the comment section as prayer", "tension": "medium"},
  {"primary": "type ARREBATAMENTO — the word becomes a collective declaration", "secondary": "golden letters as each viewer's act of faith"},
  None)

# ---- Q95 ----
Q(95, "Mesa de jantar familiar", "Wide mesa de jantar brasileira em cores quentes com Biblia e celular",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 35, "aperture": "f/4.0", "depth_of_field": "moderate", "aspect_ratio": "16:9"},
  {"primary": "a Brazilian family dinner table set with warm food, an open Bible at the center, and a smartphone being passed from one hand to another across the table, warm golden lamplight illuminating the scene",
   "focal_point": "the smartphone being passed between hands over the Bible",
   "secondary": "Multiple family hands visible. Modest home in monochrome behind.",
   "props": ["Brazilian dinner table with warm food", "open Bible at center", "smartphone being passed hand to hand", "warm golden lamp", "multiple family hands"]},
  {"location": "a modest Brazilian family dining room", "time_of_day": "evening dinner, warm lamp", "atmosphere": "community mission, share with your family and church"},
  {"rule": "centered symmetry", "foreground": "table and hands in vivid warm crimson and golden tones",
   "background": "desaturated black-and-white modest home interior",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm golden ceiling lamp over table", fill="amber food and skin tones"),
  {"emotion": "community, sharing, mission", "tension": "medium"},
  {"primary": "share this video with your church group, your family", "secondary": "smartphone over Bible as modern evangelism"},
  None)

# ---- Q96 ----
Q(96, "Revista com luz rasante", "Close-up revista analoga fechada com luz rasante vermelho-sangue",
  {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 60, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
  {"primary": "a closed unbranded generic magazine lying on a dark surface, illuminated by blood-red raking light from the left side, floating embers around it, the cover surface reflecting crimson highlights",
   "focal_point": "the crimson light reflection on the magazine cover surface",
   "secondary": "Floating embers around. Dark table surface.",
   "props": ["closed unbranded magazine", "blood-red raking light", "floating embers", "dark surface"]},
  {"location": "a dark table surface", "time_of_day": "blood-red lateral light only", "atmosphere": "final warning, the Economist is more than an economics magazine"},
  {"rule": "centered symmetry", "foreground": "magazine in crimson-lit warm tones",
   "background": "dark surface and floating embers",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="blood-red raking light from left", fill="ember glow", rim="crimson reflection on magazine cover"),
  {"emotion": "last alert, the warning made plain", "tension": "high"},
  {"primary": "for those who still think the Economist is just a magazine", "secondary": "blood-red light as the truth that reveals"},
  None)

# ---- Q97 ----
Q(97, "Profeta de bracos abertos", "Wide profeta medieval bracos abertos, manto carmesim, ceu tempestuoso P&B",
  {"type": "wide", "camera_angle": "straight-on", "focal_length_mm": 28, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
  {"primary": "a medieval prophet figure (styled as John of Patmos) standing with arms outstretched, wearing a flowing crimson robe, eyes closed in prayer, in high contrast against a monochrome stormy sky",
   "focal_point": "the outstretched arms and upturned face of the prophet",
   "secondary": "Stormy clouds and lightning in monochrome behind. Floating embers around the figure.",
   "props": ["medieval prophet figure", "flowing crimson robe", "outstretched arms", "closed eyes in prayer", "stormy monochrome sky", "floating embers"]},
  {"location": "a rocky cliff edge", "time_of_day": "stormy dusk with divine light breaking through clouds", "atmosphere": "prophetic confession, they admitted everything"},
  {"rule": "centered symmetry", "foreground": "prophet in vivid crimson and gold high contrast",
   "background": "desaturated black-and-white stormy sky with lightning",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="divine golden light from above breaking through storm clouds", fill="warm amber on crimson robe", rim="gold edge on outstretched arms"),
  {"emotion": "prophetic declaration, they admitted everything", "tension": "absolute"},
  {"primary": "they admitted EVERYTHING — the prophet speaks the final truth", "secondary": "arms open as both accusation and surrender to God"},
  None)

# ---- Q98 ----
Q(98, "Olho com cidade em chamas", "Close-up extremo olho aberto refletindo cidade em chamas na pupila",
  {"type": "extreme close-up", "camera_angle": "straight-on", "focal_length_mm": 150, "aperture": "f/1.4", "depth_of_field": "razor-thin", "aspect_ratio": "16:9"},
  {"primary": "an extreme macro close-up of a single human eye occupying 80% of the frame, the iris in rich amber-brown tones, the pupil reflecting a tiny burning city skyline in flames, the eye wide open in stunned awareness",
   "focal_point": "the burning city reflection inside the pupil",
   "secondary": "Eyelashes in sharp detail. Skin texture visible around the eye.",
   "props": ["single human eye macro", "amber-brown iris", "burning city reflection in pupil", "sharp eyelash detail", "skin texture"]},
  {"location": "abstract — the eye fills the entire frame", "time_of_day": "warm light from the reflected fire in the pupil", "atmosphere": "conscious witness, now you know too"},
  {"rule": "centered symmetry", "foreground": "eye iris in vivid amber-gold tones",
   "background": "desaturated black-and-white skin and shadow around the eye",
   "safe_zone_for_overlay": "lower 20% of frame"},
  make_lighting(key="warm fire reflection from inside the pupil as primary light", fill="faint amber on iris surface", rim="gold on eyelash tips"),
  {"emotion": "conscious witness, you now know what they know", "tension": "absolute"},
  {"primary": "and now, you also know — the final frame of testimony", "secondary": "burning city in the eye as the future already visible to the informed"},
  None)


# ===========================
# BUILD AND WRITE ALL JSONS
# ===========================

def build_json(num, title, beat, shot, subject, env, comp, light_override, mood, sym, ist):
    parte = suno_part_for_quadro(num)
    ato = ato_for_quadro(num)
    qstr = f"Q{num:02d}"

    obj = {
        "id": f"video-015_PARTE{parte}_{qstr}",
        "version": VERSION,
        "model_target": MODEL_TARGET,
        "scene_title": title,
        "narrative_beat": beat,
        "canal_context": {
            "canal": CANAL,
            "video": VIDEO,
            "parte_suno": parte,
            "quadro": qstr,
            "ato": ato
        },
        "style_reference": make_style_ref(),
        "shot": shot,
        "subject": subject,
        "environment": env,
        "composition": comp,
        "lighting": light_override if light_override else make_lighting(),
        "style": make_base_style(),
        "mood": mood,
        "symbolism": sym,
        "negative_as_positive": build_negative(num),
        "api_call_hints": make_api_hints(num)
    }

    # in_scene_text
    if ist:
        obj["in_scene_text"] = ist
    else:
        obj["in_scene_text"] = {"enabled": False}

    return obj

count = 0
for (num, title, beat, shot, subject, env, comp, light, mood, sym, ist) in QUADROS:
    obj = build_json(num, title, beat, shot, subject, env, comp, light, mood, sym, ist)
    qstr = f"Q{num:02d}"
    out_path = OUT_DIR / f"{qstr}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    count += 1

print(f"Total JSONs gerados: {count}")
print(f"Diretorio: {OUT_DIR}")

# Verify shot type alternation
shot_types = []
for (num, title, beat, shot, subject, env, comp, light, mood, sym, ist) in sorted(QUADROS, key=lambda x: x[0]):
    st = shot["type"]
    shot_types.append((num, st))

violations = []
for i in range(1, len(shot_types)):
    prev_num, prev_type = shot_types[i-1]
    curr_num, curr_type = shot_types[i]
    # Only check consecutive quadros
    if curr_num == prev_num + 1:
        if curr_type == prev_type:
            violations.append(f"Q{prev_num:02d}({prev_type}) -> Q{curr_num:02d}({curr_type})")

if violations:
    print(f"\nATENCAO: {len(violations)} violacoes de shot type consecutivo:")
    for v in violations:
        print(f"  {v}")
else:
    print("\nSem violacoes de shot type consecutivo. OK!")

# List Pro quadros
print("\nQuadros PRO:")
for (num, title, beat, shot, subject, env, comp, light, mood, sym, ist) in sorted(QUADROS, key=lambda x: x[0]):
    if num in ALL_PRO:
        reason = "versiculo biblico com in_scene_text" if num in PRO_VERSE_QUADROS else "complexidade visual alta"
        print(f"  Q{num:02d} — {title} — {reason}")
