#!/usr/bin/env python3
"""
Gera 30 JSONs Goetia (variacoes QNN_1) para video-020-1984-daniel.
Distribui 6 por parte, contextualizados pela transcricao Whisper.
Nomenclatura: Q{par}_1.json para cada parte.
"""
import json
from pathlib import Path

BASE = Path(r"C:/Users/Leandro/Downloads/agencia/canais/sinais-do-fim/videos/video-020-1984-daniel")
OUT = BASE / "6-prompts-imagem"

STYLE_REF = {
    "primary_image_url": "canais/sinais-do-fim/_config/style_refs/sinais_dark.png",
    "weight": 0.85,
    "transfer_targets": ["color_palette", "lighting", "texture", "atmosphere", "film_grain"],
    "textual_description": "dark cinematic chiaroscuro, Caravaggio-inspired, foreground in rich warm tones (crimson, amber, gold) with background in desaturated black-and-white, film grain, candlelight, floating orange embers"
}

API_HINTS = {
    "multimodal_inputs": [
        {"type": "image", "source": "style_reference.primary_image_url", "role": "style_reference",
         "instruction": "Transfer color palette, lighting, grain, atmosphere only. Do not copy composition."},
        {"type": "text", "source": "serialized_prompt_from_this_json", "role": "scene_description"}
    ]
}

NEG = [
    "clean frame without visible text or watermarks",
    "photorealistic documentary cinematography, not illustrated or cartoon",
    "analog film photography aesthetic, no digital art flatness",
    "muted desaturated background palette, warm saturated foreground only",
    "tack-sharp focus on primary subject"
]

VARIACOES = [
    # PARTE 1 — Orwell + Jura + Guerra Espanhola (Q02_1, Q04_1, Q06_1, Q08_1, Q10_1, Q12_1)
    {"q": "Q02_1", "parte": 1, "ato": "Gancho", "title": "Maquina de escrever Remington close-up",
     "beat": "Close-up extremo de maquina de escrever Remington 1940s, dedos magros pressionando tecla, caracter 1984 visivel na folha",
     "shot": {"type": "extreme close-up", "camera_angle": "overhead 45 degrees", "focal_length_mm": 85, "aperture": "f/1.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "an antique black Remington typewriter 1940s with tired thin fingers pressing a key",
                 "focal_point": "half-typed page showing partial text ending in year 1984",
                 "secondary": "cigarette smoke curling up, candle reflection on metal keys",
                 "props": ["black Remington typewriter", "thin tubercular fingers", "half-typed manuscript page", "burning candle", "cigarette ashtray"]},
     "env": {"location": "a cold stone cottage writing desk in Jura", "time_of_day": "late night candlelight", "atmosphere": "feverish, solitary, prophetic"},
     "light": {"key": "single warm candle on right side", "fill": "none (deep shadows)", "rim": "amber rim on keys", "mood": "tenebrist chiaroscuro", "shadow": "hard dramatic"},
     "sym": {"primary": "the final warning being written", "secondary": "fragile flame of prophecy"}},

    {"q": "Q04_1", "parte": 1, "ato": "Gancho", "title": "Casa Barnhill Jura vista aerea",
     "beat": "Vista aerea desolada da casa Barnhill na ilha de Jura, tempestade, mar ao fundo, isolamento absoluto",
     "shot": {"type": "aerial wide", "camera_angle": "high angle 60 degrees", "focal_length_mm": 24, "aperture": "f/8", "depth_of_field": "deep", "aspect_ratio": "16:9"},
     "subject": {"primary": "a solitary stone cottage on windswept Scottish moor — Barnhill farmhouse Jura",
                 "focal_point": "single lit window glowing amber",
                 "secondary": "raging storm clouds, distant grey sea, no other buildings for miles",
                 "props": ["isolated stone cottage", "glowing amber window", "storm clouds", "treeless moor", "distant sea"]},
     "env": {"location": "Isle of Jura Scottish Hebrides 1947", "time_of_day": "stormy dusk", "atmosphere": "absolute isolation, dread"},
     "light": {"key": "diffuse overcast storm", "fill": "cold blue-grey", "rim": "amber window glow", "mood": "foreboding isolation", "shadow": "soft heavy"},
     "sym": {"primary": "the prophet exiled", "secondary": "one light against the dark"}},

    {"q": "Q06_1", "parte": 1, "ato": "Gancho", "title": "Raio-X pulmao tuberculose",
     "beat": "Raio-X de torax humano com cavernas tuberculose visiveis, iluminado por baixo por negatoscopio",
     "shot": {"type": "medium close-up", "camera_angle": "straight-on", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "a 1940s chest X-ray film showing lungs with visible tuberculosis cavitations",
                 "focal_point": "dark cavitation shadows on the right lung",
                 "secondary": "doctor's hands in shadow holding edge of film, backlit light box glow",
                 "props": ["medical X-ray film", "backlit viewer", "physician hands silhouette", "handwritten notes on corner"]},
     "env": {"location": "dim 1940s hospital radiology room", "time_of_day": "evening medical exam", "atmosphere": "clinical dread, mortality"},
     "light": {"key": "cold white medical backlight through film", "fill": "none", "rim": "amber from corridor", "mood": "clinical mortality", "shadow": "hard edges"},
     "sym": {"primary": "death consuming the prophet", "secondary": "seven months remaining"}},

    {"q": "Q08_1", "parte": 1, "ato": "Gancho", "title": "Retrato Orwell jovem",
     "beat": "Retrato preto e branco de George Orwell aos 35 anos, olhar distante, bigode fino, camisa escura sem gravata",
     "shot": {"type": "medium portrait", "camera_angle": "3/4 lateral", "focal_length_mm": 85, "aperture": "f/2", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "a thin middle-aged British man early 40s with tired intelligent eyes, thin mustache, dark open-collar shirt — Orwellian likeness not identifiable as real person",
                 "focal_point": "the haunted eyes staring past camera",
                 "secondary": "cigarette smoke curling from hand out of frame, bookshelf blurred behind",
                 "props": ["unbuttoned dark shirt", "thin mustache", "cigarette smoke", "blurred bookshelf", "wooden chair back"]},
     "env": {"location": "a modest 1940s London study", "time_of_day": "dusk window light", "atmosphere": "contemplative, haunted"},
     "light": {"key": "soft window light from left", "fill": "warm amber from lamp right", "rim": "subtle hair rim", "mood": "Rembrandt portrait", "shadow": "classic portrait triangle"},
     "sym": {"primary": "the witness", "secondary": "prophet bearing memory"}},

    {"q": "Q10_1", "parte": 1, "ato": "Ato1", "title": "Fuzil enferrujado trincheira espanhola",
     "beat": "Fuzil Mauser enferrujado apoiado em parede de terra de trincheira, capacete republicano torto no chao, poca dagua",
     "shot": {"type": "close-up low angle", "camera_angle": "low 30 degrees", "focal_length_mm": 50, "aperture": "f/4", "depth_of_field": "medium", "aspect_ratio": "16:9"},
     "subject": {"primary": "a rusted Spanish Mauser rifle leaning against a trench earth wall",
                 "focal_point": "torn red republican flag fragment tied to rifle barrel",
                 "secondary": "a dented steel helmet half-submerged in muddy trench water, spent shell casings",
                 "props": ["rusted Mauser rifle", "torn red flag scrap", "dented republican helmet", "muddy puddle", "spent brass shells"]},
     "env": {"location": "abandoned Spanish civil war trench 1937", "time_of_day": "overcast battlefield dawn", "atmosphere": "abandoned trauma"},
     "light": {"key": "diffuse overcast", "fill": "cold blue trench shadow", "rim": "faint warm sunbreak", "mood": "abandoned witness", "shadow": "soft muted"},
     "sym": {"primary": "betrayed revolution", "secondary": "memory that wounded Orwell"}},

    {"q": "Q12_1", "parte": 1, "ato": "Ato1", "title": "Camaradas desaparecendo neblina",
     "beat": "Silhuetas de 4 soldados republicanos se dissolvendo em nevoeiro, ultima figura olhando para tras, preto e branco",
     "shot": {"type": "medium wide", "camera_angle": "eye level", "focal_length_mm": 35, "aperture": "f/4", "depth_of_field": "deep", "aspect_ratio": "16:9"},
     "subject": {"primary": "four silhouetted Republican soldier figures walking into thick fog, only last one half-visible turning back",
                 "focal_point": "last soldier's partially visible face turned back toward viewer",
                 "secondary": "tall dry grass, distant broken fence, no horizon line visible",
                 "props": ["four soldier silhouettes in formation", "rifles shouldered", "tall dry grass", "thick erasing fog", "broken wooden fence"]},
     "env": {"location": "anonymous Aragon hillside 1937", "time_of_day": "heavy morning fog", "atmosphere": "disappearance, erasure of history"},
     "light": {"key": "diffuse white fog light", "fill": "grey all around", "rim": "none", "mood": "vanishing witnesses", "shadow": "dissolved"},
     "sym": {"primary": "history being rewritten while it happens", "secondary": "comrades erased from record"}},

    # PARTE 2 — Daniel + Babilonia + 4a Besta (Q14_1 ... Q24_1)
    {"q": "Q14_1", "parte": 2, "ato": "Ato2", "title": "Daniel orando janela Babilonia",
     "beat": "Daniel jovem de joelhos ao lado de janela arqueada com ziggurate babilonica ao fundo noturno",
     "shot": {"type": "medium", "camera_angle": "3/4 side", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "medium", "aspect_ratio": "16:9"},
     "subject": {"primary": "a young Hebrew man in 6th century BC Babylonian court robes kneeling by an arched window, hands clasped",
                 "focal_point": "the prophet's face illuminated by distant ziggurat fire",
                 "secondary": "massive Babylonian ziggurat silhouette glowing with sacrificial fires on horizon",
                 "props": ["embroidered Hebrew tunic", "arched stone window", "distant stepped ziggurat", "sacrificial braziers glowing", "star-filled desert night"]},
     "env": {"location": "royal quarters Babylon 6th century BC", "time_of_day": "deep night with distant firelight", "atmosphere": "exile, vigilant prayer"},
     "light": {"key": "warm ziggurat firelight from window", "fill": "deep blue interior darkness", "rim": "amber profile on face", "mood": "sacred vigilance", "shadow": "long deep"},
     "sym": {"primary": "exiled prophet seeing empires", "secondary": "the seer of the ages"}},

    {"q": "Q16_1", "parte": 2, "ato": "Ato2", "title": "Trono dourado vazio Babilonia",
     "beat": "Sala do trono babilonica vazia, trono dourado ao centro, colunas massivas lapidadas, sensacao de poder ausente",
     "shot": {"type": "wide symmetrical", "camera_angle": "straight-on center", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
     "subject": {"primary": "a massive empty gold-plated Babylonian throne centered in a vast columned hall",
                 "focal_point": "the empty throne with crown on armrest",
                 "secondary": "two rows of massive stone columns with lamassu bas-reliefs, polished basalt floor",
                 "props": ["gold-plated throne", "cuneiform inscribed columns", "lamassu bull-man reliefs", "polished black basalt floor", "abandoned golden crown"]},
     "env": {"location": "throne room palace of Nebuchadnezzar", "time_of_day": "torchlit night", "atmosphere": "absolute power, transient glory"},
     "light": {"key": "amber wall torches on both sides", "fill": "deep shadow between columns", "rim": "gold gleaming on throne", "mood": "imperial emptiness", "shadow": "heavy architectural"},
     "sym": {"primary": "kingdoms that rise and fall", "secondary": "power that does not last"}},

    {"q": "Q18_1", "parte": 2, "ato": "Ato2", "title": "Mao escreve MENE TEKEL parede",
     "beat": "Mao espectral dourada escrevendo hebraico na parede de banquete belsazar, letras MENE MENE TEKEL brilhando",
     "shot": {"type": "close-up", "camera_angle": "straight-on wall", "focal_length_mm": 85, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "a disembodied glowing golden hand writing Hebrew characters on a stone palace wall",
                 "focal_point": "the Hebrew letters glowing with inner fire against stone",
                 "secondary": "spilled wine cup on banquet table in blurred foreground, shocked royal guests silhouetted",
                 "props": ["spectral glowing hand", "Hebrew cuneiform-style engraving", "overturned gold goblet", "spilled red wine", "stunned silhouettes"]},
     "env": {"location": "Belshazzar feast hall", "time_of_day": "banquet night", "atmosphere": "divine judgment interrupts"},
     "light": {"key": "supernatural golden glow from writing", "fill": "warm torchlight", "rim": "gold on hand outline", "mood": "apocalyptic revelation", "shadow": "cast by writing glow"},
     "sym": {"primary": "numbered, weighed, divided", "secondary": "the handwriting on the wall"}},

    {"q": "Q20_1", "parte": 2, "ato": "Ato2", "title": "Quatro bestas tempestade",
     "beat": "Silhuetas grotescas de 4 bestas apocalipticas surgindo de mar tempestuoso, relampagos, ceu rasgado",
     "shot": {"type": "wide low angle", "camera_angle": "low 20 degrees", "focal_length_mm": 35, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
     "subject": {"primary": "four monstrous silhouetted beasts rising from raging stormy sea under cracked apocalyptic sky",
                 "focal_point": "the fourth beast largest and most terrible in center",
                 "secondary": "lightning bolts illuminating the creatures, foam and spray from churning sea",
                 "props": ["four distinct beast silhouettes (lion-eagle, bear, leopard, iron-toothed)", "churning storm sea", "lightning bolts", "cracked sky", "no visible horizon"]},
     "env": {"location": "primordial vision sea", "time_of_day": "apocalyptic night storm", "atmosphere": "cosmic dread"},
     "light": {"key": "stark lightning flashes", "fill": "deep storm blue", "rim": "lightning rim on beast silhouettes", "mood": "apocalyptic vision", "shadow": "stark and shifting"},
     "sym": {"primary": "four world empires", "secondary": "the vision Daniel could not unsee"}},

    {"q": "Q22_1", "parte": 2, "ato": "Ato2", "title": "Dentes de ferro devorando",
     "beat": "Close-up macro de mandibula mecanica com dentes de ferro corroidos devorando terra e pedras",
     "shot": {"type": "extreme close-up", "camera_angle": "low 45 degrees", "focal_length_mm": 100, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "a grotesque iron mechanical jaw with rusted serrated teeth clamping down, crushing stone",
                 "focal_point": "one bright spark erupting between iron teeth",
                 "secondary": "pulverized stone dust falling from crushing teeth, blood-like rust staining teeth",
                 "props": ["iron beast jaw mechanism", "rusted serrated teeth", "spark of friction", "pulverized stone dust", "rust bleeding like blood"]},
     "env": {"location": "vision-realm industrial symbol", "time_of_day": "timeless", "atmosphere": "devouring total"},
     "light": {"key": "single harsh overhead", "fill": "none deep black", "rim": "spark light reflecting", "mood": "mechanical terror", "shadow": "extreme contrast"},
     "sym": {"primary": "devouring and breaking in pieces", "secondary": "system that crushes all"}},

    {"q": "Q24_1", "parte": 2, "ato": "Ato2", "title": "Calendario sendo apagado",
     "beat": "Calendario pergaminho ancestral sendo apagado, meses e leis riscados por mao anonima, tinta sangue escorrendo",
     "shot": {"type": "overhead top-down", "camera_angle": "90 degrees overhead", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "medium", "aspect_ratio": "16:9"},
     "subject": {"primary": "an ancient parchment calendar being defaced by an anonymous gloved hand crossing out dates and laws",
                 "focal_point": "red-black ink dripping down the crossed-out Hebrew lunar calendar",
                 "secondary": "snapped feather quill, overturned inkwell, torn edges of parchment",
                 "props": ["ancient Hebrew lunar calendar", "anonymous gloved hand", "black-red bleeding ink", "snapped quill", "torn parchment edges"]},
     "env": {"location": "concealed scribal desk", "time_of_day": "candlelit secret night", "atmosphere": "sacrilegious erasure"},
     "light": {"key": "single warm candle", "fill": "deep black", "rim": "golden edge on parchment", "mood": "deliberate desecration", "shadow": "intimate sinister"},
     "sym": {"primary": "changing times and laws", "secondary": "God's calendar defaced"}},

    # PARTE 3 — Paulo + Duplipensar (Q26_1 ... Q36_1)
    {"q": "Q26_1", "parte": 3, "ato": "Ato3", "title": "Paulo escrevendo a Tessalonica",
     "beat": "Paulo apostolo escrivao a luz de candelabro com pergaminho, pena dourada, carta grega manuscrita",
     "shot": {"type": "medium close-up", "camera_angle": "3/4 over shoulder", "focal_length_mm": 50, "aperture": "f/2", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "a 1st century hooded Apostle Paul figure writing on parchment by candelabrum",
                 "focal_point": "the golden feather quill mid-stroke writing Greek letters",
                 "secondary": "finished scrolls stacked beside, amphora of wine, olive branch as bookmark",
                 "props": ["hooded robed scribe back view", "gold-tipped quill", "parchment with Greek text", "stacked scrolls", "clay oil lamp"]},
     "env": {"location": "1st century Corinthian apartment", "time_of_day": "deep night candlelight", "atmosphere": "prophetic urgency"},
     "light": {"key": "warm candle cluster", "fill": "deep amber", "rim": "gold on quill", "mood": "devotional urgency", "shadow": "intimate warm"},
     "sym": {"primary": "the apostolic warning", "secondary": "word preserved across centuries"}},

    {"q": "Q28_1", "parte": 3, "ato": "Ato3", "title": "Manuscrito grego energeia planes",
     "beat": "Close-up macro de pergaminho grego antigo mostrando palavras ENERGEIA PLANES brilhando em tinta dourada",
     "shot": {"type": "extreme close-up", "camera_angle": "90 degrees overhead", "focal_length_mm": 100, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "ancient Greek uncial manuscript text on weathered papyrus with visible words energeia planes glowing gold",
                 "focal_point": "the two Greek words highlighted with golden illumination",
                 "secondary": "magnifying lens hovering partially in frame, dust particles floating in light beam",
                 "props": ["ancient Greek papyrus fragment", "glowing gilded Greek characters", "scholar's magnifying lens", "floating dust particles", "wooden scholar's desk"]},
     "env": {"location": "biblical scholar's archive", "time_of_day": "timeless study", "atmosphere": "revelation of meaning"},
     "light": {"key": "single focused beam from above", "fill": "dark archive around", "rim": "gold on glowing words", "mood": "sacred decoding", "shadow": "dramatic pinpoint"},
     "sym": {"primary": "the operation of error named", "secondary": "original language preserves truth"}},

    {"q": "Q30_1", "parte": 3, "ato": "Ato3", "title": "Cerebro dividido luz sombra",
     "beat": "Secao transversal de cerebro humano metade iluminada dourada metade em sombra fria, dualidade duplipensar",
     "shot": {"type": "medium close-up", "camera_angle": "straight-on", "focal_length_mm": 85, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "an anatomical cross-section of a human brain, left half bathed in golden warm light, right half in cold blue shadow",
                 "focal_point": "the dividing line exactly through center",
                 "secondary": "neurons firing visible only on illuminated side, dormant on shadow side",
                 "props": ["anatomical brain cross-section", "perfect vertical division", "golden firing synapses left", "frozen grey matter right", "no skull visible"]},
     "env": {"location": "symbolic medical illustration space", "time_of_day": "timeless", "atmosphere": "cognitive dissonance visualized"},
     "light": {"key": "split hard lighting exact center", "fill": "none preserving division", "rim": "gold on illuminated half", "mood": "doublethink made flesh", "shadow": "absolute half-division"},
     "sym": {"primary": "knowing and not knowing", "secondary": "doublethink literalized"}},

    {"q": "Q32_1", "parte": 3, "ato": "Ato3", "title": "Multidao rostos apagados",
     "beat": "Multidao vista de frente com rostos em branco liso sem tracos, perfilados como estatuas humanas",
     "shot": {"type": "wide", "camera_angle": "eye level", "focal_length_mm": 35, "aperture": "f/5.6", "depth_of_field": "medium", "aspect_ratio": "16:9"},
     "subject": {"primary": "a crowd of people standing in formal rows with blank featureless faces smooth as marble",
                 "focal_point": "one slightly tilted head in center row hinting humanity beneath",
                 "secondary": "identical dark business attire, rain streaks reflecting off shoulders",
                 "props": ["uniform dark coats", "faceless smooth heads", "perfect posture rows", "wet street reflections", "grey sky"]},
     "env": {"location": "public square total system", "time_of_day": "overcast morning rally", "atmosphere": "dehumanized compliance"},
     "light": {"key": "overcast diffuse", "fill": "cold grey", "rim": "faint gold on one face hint", "mood": "erased identity", "shadow": "uniform soft"},
     "sym": {"primary": "those who believe the lie", "secondary": "humanity effaced by system"}},

    {"q": "Q34_1", "parte": 3, "ato": "Ato3", "title": "Televisao vintage falso pregador",
     "beat": "Televisao de madeira anos 60 exibindo falso pregador smiling estatica, tela rachada, sinal interferido",
     "shot": {"type": "medium", "camera_angle": "slight low angle", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "a wooden 1960s television set broadcasting a smiling false preacher in pixelated broadcast",
                 "focal_point": "the preacher's unnaturally wide smile behind CRT glass",
                 "secondary": "cracked glass screen, interference static bars, gold cross pin on preacher's lapel",
                 "props": ["vintage wooden TV set", "cracked curved CRT screen", "smiling false preacher", "broadcast static bars", "golden crucifix pin"]},
     "env": {"location": "dim empty living room", "time_of_day": "late night broadcast", "atmosphere": "deceptive comfort"},
     "light": {"key": "TV glow blue-white on viewer", "fill": "deep black room", "rim": "amber from nearby lamp", "mood": "mass deception", "shadow": "flickering from TV"},
     "sym": {"primary": "signs and wonders of lies", "secondary": "false gospel televised"}},

    {"q": "Q36_1", "parte": 3, "ato": "Ato3", "title": "Igreja interior simbolos invertidos",
     "beat": "Interior vasto de igreja moderna com cruzes e simbolos subtilmente invertidos, luz pela vidraca manchada",
     "shot": {"type": "wide symmetrical", "camera_angle": "straight-on center", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
     "subject": {"primary": "a vast modern cathedral nave with subtly inverted crosses and distorted symbols on altar",
                 "focal_point": "the inverted cross on the altar glowing with cold light",
                 "secondary": "empty wooden pews in perfect symmetry, stained glass showing distorted biblical scenes",
                 "props": ["modern cathedral interior", "inverted altar cross", "wooden pews symmetrical", "distorted stained glass", "cold marble floor"]},
     "env": {"location": "apostate cathedral interior", "time_of_day": "late afternoon colored light", "atmosphere": "sacred space inverted"},
     "light": {"key": "filtered cold blue through stained glass", "fill": "deep architectural shadows", "rim": "amber from distant candles", "mood": "holy place desecrated", "shadow": "long symmetrical"},
     "sym": {"primary": "the great falling away", "secondary": "faith turned against itself"}},

    # PARTE 4 — Vigilancia China + CBDC (Q38_1 ... Q48_1)
    {"q": "Q38_1", "parte": 4, "ato": "Ato4", "title": "Parede de cameras CCTV China",
     "beat": "Parede urbana chinesa com dezenas de cameras de vigilancia CCTV alinhadas, luzes vermelhas piscando",
     "shot": {"type": "wide", "camera_angle": "slight low angle", "focal_length_mm": 35, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
     "subject": {"primary": "an urban wall covered with dozens of CCTV surveillance cameras in organized rows, red recording lights active",
                 "focal_point": "one central camera turning to face viewer directly",
                 "secondary": "Chinese character signage partially visible, rainy reflective pavement, passersby silhouetted below",
                 "props": ["multiple CCTV cameras", "pulsing red recording lights", "Chinese street signage", "wet dark pavement", "silhouetted pedestrians"]},
     "env": {"location": "modern Chinese metropolis surveillance street", "time_of_day": "rainy night", "atmosphere": "pervasive observation"},
     "light": {"key": "red recording lights pulsing", "fill": "cyan neon signs reflecting", "rim": "amber from one shop window", "mood": "panopticon", "shadow": "harsh urban"},
     "sym": {"primary": "700 million electronic eyes", "secondary": "Big Brother is watching"}},

    {"q": "Q40_1", "parte": 4, "ato": "Ato4", "title": "Rosto escaneado laser biometrico",
     "beat": "Rosto humano de perfil sendo escaneado por linhas laser vermelhas biometricas, pontos brilhantes em traços faciais",
     "shot": {"type": "medium close-up", "camera_angle": "3/4 profile", "focal_length_mm": 85, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "a human male face in 3/4 profile scanned by red biometric laser grid lines",
                 "focal_point": "bright red point fixed on pupil identifying iris",
                 "secondary": "wire-frame data overlay ghosted around face, Chinese digital readout in corner",
                 "props": ["red laser scanning grid", "biometric data wireframe", "iris focus marker", "digital Chinese characters readout", "cold dark background"]},
     "env": {"location": "biometric checkpoint station", "time_of_day": "timeless scan", "atmosphere": "total identification"},
     "light": {"key": "red laser scan primary", "fill": "deep black void", "rim": "subtle amber from peripheral display", "mood": "clinical identification", "shadow": "hard cold"},
     "sym": {"primary": "no escape from the gaze", "secondary": "face turned to number"}},

    {"q": "Q42_1", "parte": 4, "ato": "Ato4", "title": "Telao score social baixo",
     "beat": "Telao gigante em praca urbana exibindo rosto anônimo e score de credito social 142 em vermelho pulsante",
     "shot": {"type": "wide low angle", "camera_angle": "low 30 degrees", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
     "subject": {"primary": "a massive urban LED billboard displaying an anonymous face with pulsing red social credit score 142",
                 "focal_point": "the score number 142 pulsing red",
                 "secondary": "crowd below looking up silhouetted, rain streaks on screen, Chinese characters scrolling",
                 "props": ["huge LED billboard", "anonymous citizen face", "pulsing red score number", "silhouetted crowd below", "scrolling Chinese text"]},
     "env": {"location": "Chinese public square at night", "time_of_day": "night public shaming", "atmosphere": "public humiliation system"},
     "light": {"key": "red billboard glow", "fill": "urban neon ambient", "rim": "amber street lamps", "mood": "algorithmic judgment", "shadow": "long cast by billboard"},
     "sym": {"primary": "the low score as mark of exile", "secondary": "modern scarlet letter"}},

    {"q": "Q44_1", "parte": 4, "ato": "Ato4", "title": "Cartao recusado terminal vermelho",
     "beat": "Terminal de pagamento moderno mostrando X vermelho grande TRANSACAO RECUSADA, mao hesitante segurando cartao",
     "shot": {"type": "close-up", "camera_angle": "slight overhead", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "a modern payment terminal screen showing a large red X and rejection message",
                 "focal_point": "the red X symbol glowing against screen",
                 "secondary": "a trembling hand still holding a chip card near terminal, cashier blurred behind",
                 "props": ["modern card payment terminal", "red rejection X", "chip credit card", "trembling hand", "blurred cashier background"]},
     "env": {"location": "modern store checkout counter", "time_of_day": "fluorescent commercial day", "atmosphere": "economic exclusion"},
     "light": {"key": "cold fluorescent overhead", "fill": "red glow from terminal", "rim": "amber from register", "mood": "denied access", "shadow": "harsh commercial"},
     "sym": {"primary": "cannot buy or sell", "secondary": "mark determines commerce"}},

    {"q": "Q46_1", "parte": 4, "ato": "Ato4", "title": "QR code na palma da mao",
     "beat": "Close-up macro de palma da mao com QR code tatuado brilhando levemente sob a pele como implante RFID",
     "shot": {"type": "extreme close-up", "camera_angle": "straight-on", "focal_length_mm": 100, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "an adult human palm with a subtle glowing QR code pattern visible beneath the skin, not tattooed but implanted",
                 "focal_point": "the center of the QR pattern glowing soft amber",
                 "secondary": "skin texture natural, subtle veins, no jewelry or watches",
                 "props": ["adult human palm", "implanted glowing QR code pattern", "natural skin texture", "visible veins", "black void background"]},
     "env": {"location": "symbolic prophetic space", "time_of_day": "timeless", "atmosphere": "final mark revealed"},
     "light": {"key": "soft amber glow from implant", "fill": "deep warm shadow", "rim": "warm skin edge", "mood": "the mark fulfilled", "shadow": "intimate cradle"},
     "sym": {"primary": "mark on the right hand", "secondary": "Revelation 13:16 literal"}},

    {"q": "Q48_1", "parte": 4, "ato": "Ato4", "title": "Mapa mundial 130 paises CBDC",
     "beat": "Mapa mundial escuro com 130 pontos vermelhos flamejantes marcando paises implementando moeda digital",
     "shot": {"type": "overhead top-down", "camera_angle": "90 degrees", "focal_length_mm": 50, "aperture": "f/4", "depth_of_field": "deep", "aspect_ratio": "16:9"},
     "subject": {"primary": "a dark world map viewed from above with 130 glowing red fire-like markers on countries",
                 "focal_point": "clustering of red markers across continents forming a global network",
                 "secondary": "subtle connecting lines between markers, IMF logo watermark faintly visible",
                 "props": ["dark world political map", "130 red flame markers", "connecting network lines", "faint IMF watermark", "hand with compass in corner"]},
     "env": {"location": "global financial surveillance room", "time_of_day": "timeless overview", "atmosphere": "global net closing"},
     "light": {"key": "red glow from markers", "fill": "deep map shadow", "rim": "amber from compass brass", "mood": "inevitable global system", "shadow": "topographical"},
     "sym": {"primary": "global currency control", "secondary": "system ready for the mark"}},

    # PARTE 5 — Tortura + Morte Orwell + Esperanca (Q50_1 ... Q60_1)
    {"q": "Q50_1", "parte": 5, "ato": "Ato5", "title": "Sala 101 cadeira institucional",
     "beat": "Sala interrogatorio bunker nua com cadeira metalica central, luz fria pendente, paredes de concreto nuas",
     "shot": {"type": "wide symmetrical", "camera_angle": "straight-on center", "focal_length_mm": 35, "aperture": "f/4", "depth_of_field": "deep", "aspect_ratio": "16:9"},
     "subject": {"primary": "a bare concrete interrogation cell with a single metal chair centered under a dangling bulb",
                 "focal_point": "the empty metal chair with restraint straps visible",
                 "secondary": "a small iron door ajar at back, puddle of water on concrete floor, number 101 stenciled on wall",
                 "props": ["metal interrogation chair", "leather restraint straps", "single bulb pendant", "bare concrete walls", "stenciled 101 numbers"]},
     "env": {"location": "Ministry of Love Room 101", "time_of_day": "institutional timeless", "atmosphere": "totalitarian terror"},
     "light": {"key": "single harsh pendant bulb", "fill": "none deep black walls", "rim": "faint from half-open door", "mood": "total despair", "shadow": "hard institutional"},
     "sym": {"primary": "the final test room", "secondary": "where hope is extinguished"}},

    {"q": "Q52_1", "parte": 5, "ato": "Ato5", "title": "Winston torturado close-up",
     "beat": "Close-up de homem magro anos 50 de olhos bandados com venda preta, sangue seco no canto da boca, suor",
     "shot": {"type": "close-up", "camera_angle": "straight-on", "focal_length_mm": 85, "aperture": "f/1.8", "depth_of_field": "very shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "a gaunt thin man 40s with black cloth blindfold across his eyes, dried blood corner of mouth, sweat on brow",
                 "focal_point": "a single tear escaping below the blindfold",
                 "secondary": "blurred interrogator silhouette hand out of focus behind",
                 "props": ["black blindfold cloth", "dried blood trickle", "sweat drops on brow", "pale distressed skin", "out-of-focus hand behind"]},
     "env": {"location": "interrogation cell", "time_of_day": "endless institutional", "atmosphere": "broken human"},
     "light": {"key": "single hard overhead", "fill": "cold blue from side", "rim": "amber from far door", "mood": "spirit being broken", "shadow": "deep cheek shadow"},
     "sym": {"primary": "does hope exist", "secondary": "the breaking point"}},

    {"q": "Q54_1", "parte": 5, "ato": "Ato5", "title": "Hospital Londres 1950 fachada",
     "beat": "University College Hospital Londres 1950, fachada vitoriana neblina janela acesa amarela single",
     "shot": {"type": "wide", "camera_angle": "low 20 degrees", "focal_length_mm": 24, "aperture": "f/5.6", "depth_of_field": "deep", "aspect_ratio": "16:9"},
     "subject": {"primary": "a Victorian London hospital facade at night 1950 with one lit window on upper floor",
                 "focal_point": "the single amber-lit hospital window",
                 "secondary": "thick fog covering street, gas lamp on corner, no pedestrians, bare tree silhouettes",
                 "props": ["Victorian hospital brick facade", "single lit upper window", "thick London fog", "Victorian gas lamp", "bare black trees"]},
     "env": {"location": "University College Hospital London January 1950", "time_of_day": "foggy winter night", "atmosphere": "a prophet dying"},
     "light": {"key": "warm single window amber", "fill": "cold fog grey", "rim": "gas lamp halo", "mood": "final vigil", "shadow": "soft fog-dissolved"},
     "sym": {"primary": "the witness extinguishing", "secondary": "1950 London remembers"}},

    {"q": "Q56_1", "parte": 5, "ato": "Ato5", "title": "Cama hospitalar vazia",
     "beat": "Cama hospital anos 50 vazia com manta branca amassada, luz de janela enviesada, mesinha com livro 1984",
     "shot": {"type": "medium", "camera_angle": "3/4 side", "focal_length_mm": 50, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "an empty 1950s hospital bed with crumpled white blanket, golden hour light through window",
                 "focal_point": "a copy of a hardcover book on the nightstand titled 1984",
                 "secondary": "glass of water half-full, folded spectacles, no occupant",
                 "props": ["1950s iron hospital bed", "crumpled white blanket", "hardcover book 1984", "water glass half-full", "folded wire-rim spectacles"]},
     "env": {"location": "private hospital room 1950", "time_of_day": "early morning light", "atmosphere": "absence, legacy"},
     "light": {"key": "soft golden window light", "fill": "cold hospital white", "rim": "gold on book cover", "mood": "peaceful departure", "shadow": "long gentle"},
     "sym": {"primary": "he is gone, the book remains", "secondary": "warning outlived the prophet"}},

    {"q": "Q58_1", "parte": 5, "ato": "Ato5", "title": "Titulo original riscado",
     "beat": "Manuscrito datilografado The Last Man in Europe riscado em tinta vermelha, numero 1984 escrito abaixo",
     "shot": {"type": "extreme close-up", "camera_angle": "90 degrees overhead", "focal_length_mm": 100, "aperture": "f/2.8", "depth_of_field": "shallow", "aspect_ratio": "16:9"},
     "subject": {"primary": "a typewritten manuscript cover page with THE LAST MAN IN EUROPE crossed out in red ink, 1984 handwritten below",
                 "focal_point": "the number 1984 in strong black handwriting",
                 "secondary": "the cross-out strokes in red ink, typewriter partially visible in corner",
                 "props": ["typewritten manuscript title page", "red ink crossing out original title", "handwritten 1984 in black", "typewriter edge visible", "aged paper texture"]},
     "env": {"location": "editor's desk 1948", "time_of_day": "late editorial afternoon", "atmosphere": "the title that became prophecy"},
     "light": {"key": "soft warm desk lamp", "fill": "none deep shadow edges", "rim": "gold on edges of paper", "mood": "decision point", "shadow": "intimate angled"},
     "sym": {"primary": "last man erased, year inverted", "secondary": "1984 as inverted 1948"}},

    {"q": "Q60_1", "parte": 5, "ato": "CTA", "title": "Cruz luminosa horizonte Biblia aberta",
     "beat": "Horizonte escuro com cruz de luz dourada elevando-se, Biblia aberta em primeiro plano brilhando paginas",
     "shot": {"type": "wide", "camera_angle": "eye level low", "focal_length_mm": 35, "aperture": "f/4", "depth_of_field": "deep", "aspect_ratio": "16:9"},
     "subject": {"primary": "a dark horizon with a radiant golden cross of light rising, an open Bible glowing in foreground on a stone",
                 "focal_point": "the open Bible pages glowing with inner warm light",
                 "secondary": "mist rising from ground, distant silhouetted mountain range, hopeful sky break",
                 "props": ["radiant golden cross", "open glowing Bible", "ancient stone altar", "rising morning mist", "silhouetted mountains"]},
     "env": {"location": "apocalyptic dawn symbolic vista", "time_of_day": "breaking dawn", "atmosphere": "final hope, true word"},
     "light": {"key": "golden sunrise behind cross", "fill": "deep warm ambient", "rim": "amber on Bible pages", "mood": "redemption after warning", "shadow": "long hopeful"},
     "sym": {"primary": "the apocalypse continues past the last page", "secondary": "hope endures where 1984 has none"}},
]


def make_json(v):
    return {
        "id": f"video-020_PARTE{v['parte']}_{v['q']}",
        "version": "nano-banana-v1",
        "model_target": "gemini-2.5-flash-image",
        "scene_title": v["title"],
        "narrative_beat": v["beat"],
        "canal_context": {
            "canal": "sinais-do-fim",
            "video": "video-020-1984-daniel",
            "parte_suno": v["parte"],
            "quadro": v["q"],
            "ato": v["ato"]
        },
        "style_reference": STYLE_REF,
        "shot": v["shot"],
        "subject": v["subject"],
        "environment": v["env"],
        "composition": {
            "rule": "rule of thirds with primary subject at strong point",
            "foreground": "warm saturated primary subject",
            "background": "desaturated contextual depth",
            "safe_zone_for_overlay": "lower 20% of frame"
        },
        "lighting": {
            "key_light": v["light"]["key"],
            "fill_light": v["light"]["fill"],
            "rim_light": v["light"]["rim"],
            "mood": v["light"]["mood"],
            "shadow_quality": v["light"]["shadow"]
        },
        "style": {
            "film_stock": "Kodak Portra 800 pushed two stops",
            "post_processing": "halation, crushed blacks, amber highlights, anamorphic lens flares",
            "texture_detail": "35mm film grain, dust particles, floating orange embers"
        },
        "mood": {"emotion": v["light"]["mood"], "tension": "medium-high"},
        "symbolism": {"primary": v["sym"]["primary"], "secondary": v["sym"]["secondary"]},
        "negative_as_positive": NEG,
        "in_scene_text": {"enabled": False},
        "api_call_hints": API_HINTS
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for v in VARIACOES:
        path = OUT / f"{v['q']}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(make_json(v), f, ensure_ascii=False, indent=2)
        print(f"[OK] {path.name}")
    print(f"\n{len(VARIACOES)} JSONs gerados em {OUT}")


if __name__ == "__main__":
    main()
