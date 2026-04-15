#!/usr/bin/env python3
"""Converte todos os quadros Banana 2.0 para Veo 3 e gera prompts para todos."""
import os, re, paramiko

BASE      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_DIR = os.path.join(BASE, "canais", "sinais-do-fim", "videos", "video-001-armagedom")
PROMPTS_DIR = os.path.join(VIDEO_DIR, "5-prompts")

# ── Novos quadros (1 clip cada) ───────────────────────────────────────────────
NOVOS_QUADROS = [

    {   "num":"02","ts":"0:15 - 0:23","bloco":"GANCHO — ARCANJO SOBRE CIDADE DESTRUÍDA",
        "prompt": "A towering medieval archangel in full vivid color descends in slow motion through parting dark storm clouds, trailing golden and crimson fire from a massive flaming sword raised high. The angel's vast feathered wings spread fully across the frame, radiating divine golden light. Below in absolute black and white — a vast aerial cityscape of devastation — crumbling skyscrapers, collapsed bridges, ash-covered streets. The camera begins at extreme wide establishing the full scene, then performs a slow deliberate dolly in toward the angel. Crimson embers and golden sparks rain from the sword in dense spiraling trails. The contrast between vivid color angel and B&W world below is sharp and surreal. 35mm grain, anamorphic lens with horizontal flares from the sword's golden fire. Color grading: isolated vivid crimson (#8B0000) and gold (#C5A355) on angel, complete desaturated B&W on the world below. Volumetric golden rays break through parting storm clouds. Dense black smoke and ash drift upward from the city. 0.5x slow motion. Epic, apocalyptic, revelatory mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Extreme wide — angel descending center frame, destroyed city as B&W backdrop",
        "camera":"Slow deliberate dolly in toward the descending angel — 20% advance over 10 seconds",
        "lighting":"Golden volumetric rays from parting clouds, practical fire light from the flaming sword, shadowless B&W overcast below",
        "dof":"Deep f/8 — angel in sharp focus, B&W city visible and secondary",
        "film":"35mm grain, anamorphic flares from sword fire, vivid color isolation on angel against full B&W world",
        "particles":"Crimson embers and golden sparks spiraling from the sword, black ash and smoke rising from city below",
        "speed":"0.5x slow motion",
        "mood":"Divine descent — heaven intervening in a destroyed world",
        "continuity":"Opening visual — establishes the central contrast: divine vivid color descending into B&W destruction",
    },

    {   "num":"03","ts":"0:30 - 0:38","bloco":"CONTEXTO — MONTANHA DE MEGIDDO",
        "prompt": "An aerial photorealistic view of the ancient tel of Megiddo in Israel, bathed in warm late-afternoon golden light. The archaeological mound rises above the surrounding Jezreel valley. The camera begins at extreme wide in a slow aerial crane down, gradually descending toward the landscape. As the camera descends, a translucent ancient medieval map of the same geography materializes as a golden overlay across the real landscape below — two realities merging. Ancient battle position markings and Hebrew script glow in deep crimson on the map overlay. The physical landscape is rendered in muted warm parchment tones. The valley glows with a historic golden haze. 35mm grain, anamorphic lens. Color grading: warm parchment gold tones with crimson overlay elements. Dust particles drift across the landscape. 0.5x slow motion. Revelatory, historic, prophetic mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Extreme wide aerial descending — the valley fills the frame as the ancient map overlay materializes",
        "camera":"Slow aerial crane down — descending from the sky toward the ancient landscape of Megiddo",
        "lighting":"Warm golden late-afternoon light on the real landscape, crimson glow from the map overlay",
        "dof":"Deep f/11 — full landscape in focus from foreground to horizon",
        "film":"35mm grain, no flares, warm parchment gold + crimson overlay grading",
        "particles":"Dust and ash drifting across the ancient valley in the wind",
        "speed":"0.5x slow motion",
        "mood":"Historical revelation — where ancient prophecy meets real geography",
        "continuity":"Grounds the prophecy in real geography — Megiddo exists, this battle will happen here",
    },

    {   "num":"04","ts":"1:00 - 1:08","bloco":"CONTEXTO — PERGAMINHO APOCALIPSE 16:16",
        "prompt": "An ancient illuminated parchment scroll unfurls dramatically at the center of the frame, glowing with warm golden and amber tones. Sacred text appears on the parchment surface letter by letter, as if being burned into the material by divine fire — glowing crimson before settling into gold. Three elaborate wax seals hang from the scroll's lower edge, dripping slowly in ultra slow motion. Ornate candles with vivid warm flames surround the parchment, their wax dripping. Pale smoke curls upward from each candle flame. The camera performs a very slow push in toward the center of the scroll where the text is appearing. Background: the interior of a ruined stone cathedral in deep black and white — collapsed arches, stone debris, darkness beyond. The candlelight creates a warm island of vivid color in the surrounding B&W ruin. 35mm grain, shallow depth of field on the scroll. Strong chiaroscuro from candle light. 0.5x slow motion. Mystical, reverential, awe-inspiring mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Medium close-up — scroll fills the center frame, candles flanking, B&W cathedral ruin in background",
        "camera":"Slow push in toward the appearing sacred text — 15% advance over 10 seconds",
        "lighting":"Practical candle light as warm key light on parchment and seals, cathedral background in deep B&W shadow",
        "dof":"Shallow f/2.0 — scroll text in sharp focus, candles soft, cathedral blur",
        "film":"35mm grain, warm golden color on scroll isolated against B&W ruin, chiaroscuro candle grading",
        "particles":"Pale smoke wisps from candles, floating wax motes, faint dust in the dark cathedral air",
        "speed":"0.5x slow motion",
        "mood":"Sacred revelation — scripture burning itself into existence on ancient parchment",
        "continuity":"The word made visible — prophecy revealed through fire on parchment",
    },

    {   "num":"06","ts":"2:00 - 2:08","bloco":"CONTEXTO — QUATRO CAVALEIROS",
        "prompt": "Four Horsemen of the Apocalypse gallop powerfully in full vivid color across the mid-ground of a wide frame — a white horse with a crowned rider bearing a raised bow, a blood red horse with a rider wielding a great sword, a black horse with a rider holding golden scales, and a pale spectral horse carrying Death as a skeletal robed figure. Each horseman rendered in rich saturated medieval illustration color — gold crowns, crimson cloaks, deep black armor, sickly pale green on Death's horse. The camera holds in a wide lateral tracking shot following the gallop from left to right with cinematic weight. Below and behind in absolute black and white: a panoramic collapsing modern city — burning skyscrapers, panicked crowds, explosions. Deep crimson storm clouds fill the sky, ash and embers fall like snow. 35mm grain, anamorphic lens. Color grading: vivid saturated horsemen vs. complete B&W world. 0.5x slow motion. Epic, inevitable, apocalyptic mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Wide — all four horsemen visible mid-frame galloping left to right, destroyed city as B&W backdrop",
        "camera":"Slow lateral tracking shot — following the gallop from left to right with cinematic authority",
        "lighting":"Dramatic red-tinted storm light from above, each horseman self-illuminated with their distinct colors",
        "dof":"Deep f/8 — horsemen in sharp vivid focus, B&W city slightly softened in background",
        "film":"35mm grain, anamorphic lens, vivid color isolation on horsemen against B&W world",
        "particles":"Ash and embers falling like snow throughout frame, smoke rising from city below, sparks from hooves",
        "speed":"0.5x slow motion",
        "mood":"Inevitability galloping — the four forces of end times in full momentum",
        "continuity":"First arc of full biblical iconography in motion — the four forces now ride",
    },

    {   "num":"07","ts":"2:30 - 2:38","bloco":"SINAL 1 — MAPA ORIENTE MÉDIO",
        "prompt": "A glowing ancient parchment map of the Middle East hovers center frame, rendered in vivid gold and crimson as if made of fire and old leather. Deep red pulsing circles mark active conflict zones — each pulse sending a crimson ripple outward like sonar. Beams of intense crimson light radiate from Jerusalem at the map's center outward to surrounding nations. Floating heraldic shield emblems in full vivid color represent the nations — American eagle, Russian bear, Iranian crescent, Israeli star — orbiting the map's edges. The camera executes a slow orbit counterclockwise around the hovering map revealing it in three dimensions against a black void. Background: black and white satellite imagery of military operations — tank convoys, smoke columns, missile trails. 35mm grain, anamorphic lens. Color grading: gold + crimson map vs. cold B&W military imagery. 0.5x slow motion. Tense, prophetic, geopolitical mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Medium — parchment map fills 70% of frame, military imagery visible at edges in B&W",
        "camera":"Slow counterclockwise orbit around the floating map — revealing it as a 3D prophetic object",
        "lighting":"Self-luminous crimson glow from conflict markers, golden light radiating from Jerusalem at center",
        "dof":"Deep f/8 — map sharp in focus, B&W background slightly softened",
        "film":"35mm grain, anamorphic flares from crimson pulses, gold + crimson map vs. cold B&W grading",
        "particles":"Crimson pulse ripples expanding from conflict markers, ember trails from radiating light beams",
        "speed":"0.5x slow motion",
        "mood":"Geopolitical revelation — the world's attention converging on one ancient land",
        "continuity":"Introduces the spatial geography of conflict — the map prophecy described now made visible",
    },

    {   "num":"08","ts":"3:00 - 3:08","bloco":"SINAL 1 — TIMELINE 1948-PRESENTE",
        "prompt": "A long ancient illuminated manuscript scroll stretches horizontally across the full frame width, rendered in vivid gold and crimson on warm parchment. The scroll's surface displays a visual timeline — ornate golden numerals marking years from 1948 onward, with heraldic explosion symbols in crimson bursting from key conflict dates. At each conflict year the parchment smolders — embers glow around those dates. The camera performs a slow lateral tracking movement from left to right, moving chronologically through the timeline. The scroll floats in deep black void. Background in deep shadow — barely visible desaturated archival imagery of wars. Each conflict marker briefly illuminates as the camera passes it. 35mm grain, anamorphic lens. Color grading: warm parchment gold + smoldering crimson on timeline, deep shadow background. 0.5x slow motion. Solemn, historic, prophetic mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Medium — the horizontal scroll fills the frame width, camera tracks laterally across it",
        "camera":"Slow deliberate lateral track from left to right — reading the timeline chronologically",
        "lighting":"Self-luminous golden glow from the scroll, smoldering crimson from conflict markers, deep shadow background",
        "dof":"Deep f/8 — scroll surface in sharp focus throughout the track",
        "film":"35mm grain, anamorphic flares from crimson conflict markers, warm gold + crimson grading",
        "particles":"Embers and smoke wisps rising from smoldering conflict dates, ash drifting in deep background",
        "speed":"0.5x slow motion",
        "mood":"History burning — every conflict date a wound still glowing on the parchment of time",
        "continuity":"End of timeline arc — establishes the continuous cycle of war before Q09 reveals the global scale",
    },

    {   "num":"10","ts":"4:00 - 4:08","bloco":"SINAL 1 — PROFETA ZACARIAS",
        "prompt": "The prophet Zechariah stands commanding at center frame in full vivid color — ancient robes of deep blue, purple and gold, long grey beard, arms raised to the heavens with palms open. From his outstretched hands a vibrant illuminated scroll unfurls upward, ancient Hebrew text glowing in golden fire as it rises. His expression is intense, authoritative, prophetic. The camera performs a very slow push in toward the prophet's raised hands and the rising scroll. Background: the ruins of ancient Jerusalem in absolute black and white — collapsed stone walls, rubble-strewn streets, fallen columns, desolate landscape under dark overcast sky. Dramatic golden volumetric light descends from above onto the prophet alone, leaving the ruins in deep shadow. Ash and cinders float through the air. 35mm grain, anamorphic lens. Color grading: vivid saturated color on prophet and scroll vs. complete B&W ruins. 0.5x slow motion. Prophetic, epic, reverent mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Medium — prophet fills center frame from waist up, B&W ruins of Jerusalem as full backdrop",
        "camera":"Slow push in toward the prophet's raised hands and the rising scroll — 20% advance",
        "lighting":"Golden volumetric column descending on prophet alone from above, ruins in deep B&W shadow",
        "dof":"Shallow f/2.8 — prophet in sharp vivid focus, B&W ruins softly blurred",
        "film":"35mm grain, anamorphic flares from the golden light column, saturated prophet vs. B&W ruins",
        "particles":"Glowing golden text particles rising from the scroll, ash and cinders floating in the air",
        "speed":"0.5x slow motion",
        "mood":"Ancient prophecy spoken into a destroyed world — the words still burning",
        "continuity":"Closes Sinal 1 — the prophet who predicted the global convergence stands in its ruins",
    },

    {   "num":"11","ts":"4:30 - 4:38","bloco":"SINAL 2 — BESTA DE 7 CABEÇAS",
        "prompt": "A monstrous medieval beast with seven distinct heads rises slowly from the base of the frame in full vivid color — each head rendered in deep crimson, gold and dark emerald scales with meticulous detail, each bearing a single glowing red digital camera eye that pulses like a living circuit. The beast's serpentine body is powerful and armored in ornate medieval scale patterns. The camera holds at medium wide as the beast rises, its heads spreading apart to fill the upper frame. Each digital eye sweeps red laser scan lines across the environment. Background: a cold black and white surveillance cityscape — CCTV cameras on every corner, giant screens displaying faces, watchtowers, crowds being passively monitored. Deep red scan lines sweep the B&W background. 35mm grain, anamorphic lens. Color grading: vivid saturated beast vs. cold desaturated B&W city. 0.5x slow motion. Deeply ominous, unsettling, prophetic mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Medium wide — beast rising center frame, surveillance city as full B&W backdrop",
        "camera":"Static hold as beast rises — camera holds its ground as the beast grows to fill the frame",
        "lighting":"Cold red digital scan light from the beast's eyes illuminating the scene, no warm natural light",
        "dof":"Deep f/8 — beast in vivid focus, B&W city visible and sharp in background",
        "film":"35mm grain, anamorphic flares from digital eye pulses, vivid beast colors vs. cold B&W city",
        "particles":"Red digital scan lines sweeping across frame, surveillance grid particles, cold neon reflections",
        "speed":"0.5x slow motion",
        "mood":"Ancient prophecy made technological — the biblical beast is the surveillance state",
        "continuity":"Introduces Sinal 2 with maximum visual impact — the beast of Revelation is here, now",
    },

    {   "num":"12","ts":"5:00 - 5:08","bloco":"SINAL 2 — MÃO COM MICROCHIP",
        "prompt": "An extreme close-up of the back of a human hand, lit from below by an eerie glowing light. Beneath the skin on the back of the hand, an intricate microchip glows with pulsing electric blue and gold bioluminescent light, its circuit patterns visible through translucent flesh. The glow pulses three times over 10 seconds, each pulse sending blue light spreading across the veins of the hand. Beside the hand at the edge of frame, an ancient wax seal in deep crimson and gold floats — cracked but still pulsing with the same rhythm as the chip. The camera holds in extreme close-up, nearly static, with a barely perceptible slow push in. Background: cascading black and white binary code matrix, ghostly crowd faces fading in and out of the digital rain. Single upward light from the chip illuminates the hand with clinical precision. 35mm grain. Color grading: isolated chip blue + gold glow on near-black, B&W binary background. 0.3x ultra slow motion on each pulse. Deeply disturbing, intimate, prophetic mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Extreme close-up — the hand fills the frame, chip glow as the primary visual anchor",
        "camera":"Near static with barely perceptible slow push in — the intimacy is suffocating",
        "lighting":"Upward practical glow from the microchip as sole key light, deep shadow everything else",
        "dof":"Shallow f/1.4 — chip glow through skin in sharp focus, binary code background in deep blur",
        "film":"35mm grain, no flares, isolated electric blue + gold on near-black, B&W binary matrix",
        "particles":"Binary code raining in background, ghostly crowd faces materializing and dissolving",
        "speed":"0.3x ultra slow motion on each chip pulse",
        "mood":"The mark of the beast is already under the skin — it just has not been activated",
        "continuity":"Q11 showed the beast from Revelation — this shows the mark it demands, already real",
    },

    {   "num":"14","ts":"6:00 - 6:08","bloco":"SINAL 2 — TRONO COM TELAS HOLOGRÁFICAS",
        "prompt": "A massive throne of pure gold, ornately carved with medieval heraldic symbols and draped in deep crimson velvet, dominates the center of the frame in full vivid color. Surrounding the throne, translucent holographic screens in cold electric blue display cascading global surveillance feeds, financial data streams and population tracking grids — their cold blue light contrasting with the warm gold of the throne. A shadowy figure sits on the throne, its form completely obscured in darkness — only a silhouette of a crowned shape visible. Red smoke particles rise slowly around the throne base. The camera executes a very slow clockwise orbit around the throne revealing it from multiple angles. Background: a vast black and white global command center, scale vast and oppressive. 35mm grain, anamorphic lens. Color grading: warm gold throne + cold blue holographics + deep red smoke. 0.5x slow motion. Ominous, totalitarian, prophetic mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Medium — throne centered, holographic screens visible around it, command center in B&W background",
        "camera":"Slow clockwise orbit around the throne — circling the seat of global power",
        "lighting":"Warm gold from the throne itself, cold blue from holographic screens, deep shadow on the figure",
        "dof":"Deep f/8 — throne and screens in focus, B&W command center background slightly softened",
        "film":"35mm grain, anamorphic flares from holographic screen edges, warm gold + cold blue split grading",
        "particles":"Deep red smoke rising slowly around the throne base, blue data particles from the screens",
        "speed":"0.5x slow motion",
        "mood":"The seat of global control already built — waiting for its occupant to be revealed",
        "continuity":"Closes Sinal 2 — from the beast, to the mark, to the throne: the complete system of control",
    },

    {   "num":"15","ts":"6:30 - 6:38","bloco":"SINAL 3 — MUNDO PARTIDO AO MEIO",
        "prompt": "A dramatic split-world composition fills the entire frame. The left half is bathed in warm vivid golden light — an ornate medieval temple with soaring gothic arches, a radiant gold cross at center, and two magnificent white-winged angels with outstretched arms, all in full saturated color. The right half plunges into cold darkness — sleek black technological architecture, cold blue surveillance screens, shadowy materialism, desaturated to near-monochrome steel and shadow. Down the exact center of the frame, a jagged crimson fissure glows like molten lava (#8B0000), cracking and pulsing as if reality itself is tearing apart. The fissure widens very slowly over 10 seconds. The camera holds perfectly static. Embers and red sparks leap from the fissure. 35mm grain, anamorphic lens. Color grading: warm gold on left, cold steel on right, molten crimson center. 0.5x slow motion. Conflicted, symbolic, prophetic mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Symmetrical wide — fissure runs down the exact center of the frame, dividing both worlds equally",
        "camera":"Static — the camera witnesses the split without taking sides",
        "lighting":"Warm golden divine light from the left, cold blue artificial from the right, crimson glow from the fissure",
        "dof":"Deep f/11 — both worlds and the fissure all in sharp focus simultaneously",
        "film":"35mm grain, anamorphic flares from the fissure's crimson glow, split warm gold + cold steel grading",
        "particles":"Crimson embers leaping from the fissure, golden motes on the left, blue data particles on the right",
        "speed":"0.5x slow motion",
        "mood":"The world's great division made visible — faith vs. materialism tearing reality apart",
        "continuity":"Introduces Sinal 3 — the ideological fracture made into a physical visual reality",
    },

    {   "num":"16","ts":"7:00 - 7:08","bloco":"SINAL 3 — ANJOS EM COMBATE",
        "prompt": "High above a vast confronting crowd in black and white, two enormous medieval angels clash in violent combat in the dark storm sky in full vivid color. One angel blazes in warm gold and radiant white — great wings of pure white feathers spread wide, a sword of pure light raised high, golden armor glinting. The opposing angel is cloaked in deep shadow-purple and blood crimson — dark raven wings outstretched, wielding dark fire from its fist. Their collision point erupts in a blinding burst of golden and dark energy. The camera positions at low angle looking upward — the B&W crowd below visible as faceless silhouettes, the angels filling the storm sky above. Lightning strikes in the background storm clouds. 35mm grain, anamorphic lens. Color grading: vivid gold + white vs. deep crimson + purple angels, B&W crowd below. 0.5x slow motion. Epic, conflicted, devastating mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Low angle wide — looking upward at the angels in combat, B&W crowd silhouettes at frame bottom",
        "camera":"Low angle static with barely perceptible upward tilt — as if the viewer cranes to see the battle",
        "lighting":"Self-luminous golden light from the divine angel, dark fire glow from the shadow angel, lightning in storm",
        "dof":"Deep f/8 — angels in vivid focus against storm sky, crowd in B&W silhouette below",
        "film":"35mm grain, anamorphic lens, vivid color angels vs. B&W crowd, chiaroscuro storm lighting",
        "particles":"Lightning sparks from the collision point, ash and embers raining down on the B&W crowd below",
        "speed":"0.5x slow motion",
        "mood":"The invisible war made visible — the spiritual battle directly above a divided humanity",
        "continuity":"Closes Sinal 3 — the ideological split of Q15 is revealed to be a cosmic spiritual war",
    },

    {   "num":"18","ts":"8:00 - 8:08","bloco":"SINAL 4 — ANJO COM TROMBETA",
        "prompt": "A mighty medieval angel stands suspended at great height in full vivid color — golden armor gleaming, vast luminous wings spread wide, robes of crimson and gold streaming in a divine wind. The angel raises an enormous ornate golden trumpet to the sky and blows. The trumpet blast is caught in ultra slow motion — a visible shockwave of golden energy radiates outward from the trumpet's bell, rippling through the air like a visible pressure wave. Below in black and white, the earth tears apart — massive fissures opening across a landscape of ruined cities, rivers of fire erupting from the cracks, buildings collapsing. The sky is a deep blood red with churning storm clouds. The camera holds at medium wide low angle looking up at the angel, then slowly cranes upward. 35mm grain, anamorphic lens. Color grading: vivid gold angel vs. blood red sky vs. B&W destruction below. 0.3x ultra slow motion. Apocalyptic, authoritative, awe-inspiring mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Medium wide low angle — angel above center frame, blood red sky surrounding, B&W destruction visible below",
        "camera":"Slow crane up — camera rises to reveal more of the sky and the scale of the trumpet blast shockwave",
        "lighting":"Self-luminous golden light from angel and trumpet shockwave, blood red ambient sky, B&W destruction below",
        "dof":"Deep f/8 — angel in vivid focus, sky and ground both visible and sharp",
        "film":"35mm grain, anamorphic flares from the golden shockwave, vivid gold + blood red + B&W destruction grading",
        "particles":"Golden shockwave ripples expanding outward, crimson embers and ash raining down, fissure fire below",
        "speed":"0.3x ultra slow motion",
        "mood":"Divine judgement announced — the trumpet calls and the earth responds",
        "continuity":"Bridges Sinal 4 — the earthquake and disasters are the earth's response to this trumpet call",
    },

    {   "num":"19","ts":"8:30 - 8:38","bloco":"SINAL 4 — 4 PAINÉIS DE DESASTRES",
        "prompt": "A dramatic four-panel collage in a 2x2 grid fills the entire frame, each panel bordered by a glowing blood-red frame (#8B0000) that pulses. Top-left: a massive earthquake — ground fissures splitting and widening in ultra slow motion, concrete rubble falling. Top-right: a colossal hurricane viewed from above — the perfect eye visible at the spiral's center, counterclockwise rotation. Bottom-left: raging wildfire consuming a dark forest — crimson flames in ultra slow motion, ash raining upward. Bottom-right: a cracked parched earth landscape under a dead overcast sky — the ground fragmenting like porcelain in slow motion. All four panels are rendered in stark desaturated black and white. Across all four panels simultaneously, a faint ghosted medieval prophet in rich vivid color overlays all panels like a transparent watermark — arms outstretched in warning. Camera holds static. 35mm grain. 0.3x ultra slow motion on all destructive elements. Urgent, overwhelming, prophetic mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Full frame symmetrical 2x2 grid — all four disaster panels equal in size, prophet overlay spanning all panels",
        "camera":"Static — all four panels demand equal attention simultaneously",
        "lighting":"Desaturated natural overcast light within each panel, blood-red border glow as the only color accent",
        "dof":"Deep f/11 — all four panels simultaneously in sharp focus",
        "film":"Full bleach bypass B&W on all panels, blood-red borders pulsing, vivid color prophet overlay as transparent layer",
        "particles":"Ash unique to each panel — earthquake dust, hurricane clouds, wildfire smoke, parched earth fragments",
        "speed":"0.3x ultra slow motion across all four panels simultaneously",
        "mood":"The acceleration of judgement — all disasters running at once, the prophet watching them all",
        "continuity":"Amplifies Q18's trumpet — four simultaneous catastrophes answer the angel's call",
    },

    {   "num":"20","ts":"9:00 - 9:08","bloco":"SINAL 5 — CRISTÃO EM ORAÇÃO",
        "prompt": "A lone figure kneels in prayer at the center of the frame, illuminated by a powerful column of divine golden light descending vertically from above — warm, vivid, saturated gold and white. The praying figure's face is turned upward with an expression of profound faith and anguish. Their hands are clasped before them. The golden light isolates the figure as the only vivid color element in the entire frame. Surrounding this illuminated figure in absolute black and white: ominous silhouettes of soldiers with weapons raised, chains coiled on the ground, prison bars casting shadows. The camera performs a very slow push in toward the praying figure. The golden column of light intensifies slightly as the camera advances. 35mm grain, anamorphic horizontal flares from the golden light. Color grading: isolated vivid gold on the figure and divine light, everything else near-black B&W. 0.5x slow motion. Intimate, dramatic, emotionally powerful mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Medium — praying figure centered in golden light column, oppressive B&W silhouettes at the edges",
        "camera":"Slow push in toward the praying figure — the golden light grows as the camera approaches",
        "lighting":"Single vertical column of golden divine light from above, deep shadow with B&W practical ambient on everything else",
        "dof":"Shallow f/2.0 — figure and golden light in vivid focus, B&W shadows softly blurred",
        "film":"35mm grain, anamorphic flares from golden light, complete color isolation on the divine light only",
        "particles":"Golden light motes descending in the column, dust motes visible in the beam, shadow particles in the dark",
        "speed":"0.5x slow motion",
        "mood":"Solitary courage — one person's faith burning against the surrounding darkness",
        "continuity":"Introduces Sinal 5 with maximum intimacy — persecution is not abstract, it is this one person",
    },

    {   "num":"21","ts":"9:30 - 9:38","bloco":"SINAL 5 — 360 MILHÕES",
        "prompt": "Enormous blood-red Roman-style numerals spelling '360 MILLION' fill the upper two-thirds of the frame, rendered in a medieval illuminated manuscript style and burning with living fire at their edges — embers eating at the number's contours, smoke rising from each digit. The numerals glow with intense internal crimson light (#8B0000). The camera holds static on the burning numerals for the first 5 seconds, then slowly cranes down to reveal below: an ancient world map in deep parchment tones, with dozens of blood-red flame markers pulsing at persecution locations across every continent — each small flame alive and burning. The camera continues its slow crane down to frame both the burning numerals and the world map together. 35mm grain, anamorphic lens. Color grading: blood-red burning numerals vs. parchment-toned map with crimson flames. 0.3x ultra slow motion on the fire details. Impactful, grief-laden, urgent mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Upper frame: burning numerals dominant. Crane reveals lower frame: ancient world map with persecution markers",
        "camera":"Static on numerals for 5 seconds, then slow crane down revealing the world map below",
        "lighting":"Internal crimson glow from the burning numerals, individual flame glow from each persecution marker on the map",
        "dof":"Deep f/8 — numerals in sharp focus, world map sharp as it is revealed",
        "film":"35mm grain, anamorphic flares from the burning numeral edges, blood-red + parchment gold grading",
        "particles":"Embers and smoke consuming the edges of the numerals, small flame particles at each persecution marker",
        "speed":"0.3x ultra slow motion on the fire consuming the numerals",
        "mood":"The weight of 360 million — a number that burns because each digit is a person",
        "continuity":"Closes Sinal 5 — the scale of persecution made viscerally real through burning numerals",
    },

    {   "num":"22","ts":"10:00 - 10:08","bloco":"CONEXÃO — CAVALEIRO NO CAVALO BRANCO",
        "prompt": "The heavens split open above with blinding golden radiance as the sky tears apart — dark storm clouds parting to reveal a vast opening of pure golden light. Through this opening a majestic rider on a magnificent white horse descends in ultra slow motion in full vivid color — armor gleaming gold and pure white, a sword of pure brilliant light raised high, long crimson and white robes streaming behind in a divine wind. The white horse is powerful and majestic, mane flowing, its hooves trailing golden light particles. The rider's face is obscured by divine radiance — pure light where features should be. The camera begins at medium wide looking up, then slowly cranes upward to follow the descent, revealing more of the golden sky opening. Below in black and white: thousands of tiny human silhouettes looking upward, some falling to their knees. 35mm grain, anamorphic lens. Color grading: vivid gold + white rider vs. B&W crowd. 0.5x slow motion. Glorious, triumphant, transcendent mood. Duration 8 seconds. Aspect ratio 16:9.",
        "framing":"Medium wide low angle — rider descending center frame, golden sky opening above, B&W crowd at frame bottom",
        "camera":"Slow crane upward — following the descent, revealing more of the golden sky opening above",
        "lighting":"Divine golden radiance from the sky opening above, rider self-luminous in gold and white, B&W ambient below",
        "dof":"Shallow f/2.8 — rider and horse in vivid focus, golden sky soft, B&W crowd in shadow blur",
        "film":"35mm grain, anamorphic flares from the divine radiance, vivid gold + white rider vs. complete B&W world",
        "particles":"Golden light particles trailing from the horse's hooves, radiant motes from the sword of light, ash falling below",
        "speed":"0.5x slow motion",
        "mood":"The promised return — glory descending into a broken black and white world",
        "continuity":"The cosmic answer to 'Are you ready?' — the rider arrives before the personal question of Q23",
    },
]


def build_new_block(q: dict) -> str:
    n = q["num"]
    lines = [
        f"================================================================================",
        f"QUADRO {n} — [{q['ts'].split(' - ')[0]}] — {q['bloco']}",
        f"================================================================================",
        f"",
        f"=== QUADRO {n} — [{q['ts'].split(' - ')[0]}] — CLIPE 1 de 1 ===",
        f"TIMESTAMP: {q['ts']}",
        f"DURACAO: 10s",
        f"",
        f"PROMPT:",
        q["prompt"],
        f"",
        f"ENQUADRAMENTO: {q['framing']}",
        f"CAMERA: {q['camera']}",
        f"ILUMINACAO: {q['lighting']}",
        f"DEPTH OF FIELD: {q['dof']}",
        f"FILM STYLE: {q['film']}",
        f"PARTICULAS: {q['particles']}",
        f"SPEED: {q['speed']}",
        f"MOOD: {q['mood']}",
        f"ASPECT RATIO: 16:9",
        f"CONTINUITY: {q['continuity']}",
        f"=======================================",
        f"",
        f"",
    ]
    return "\n".join(lines)


def update_storyboard():
    sb_path = os.path.join(VIDEO_DIR, "4-storyboard", "storyboard.txt")
    with open(sb_path, encoding="utf-8") as f:
        txt = f.read()

    txt = txt.replace("Distribuicao: 70% Banana 2.0 | 15% Veo 3 | 10% CapCut | 5% Web",
                      "Distribuicao: 75% Veo 3 | 12% CapCut | 13% outros")
    txt = txt.replace("TIPO: Imagem estatica (Banana 2.0)", "TIPO: Clipe com movimento (Veo 3)")
    txt = txt.replace("TIPO: Referencia web + CapCut overlay", "TIPO: Clipe com movimento (Veo 3)")
    # Notas tecnicas
    txt = txt.replace("- Banana 2.0: 17 quadros (71%)", "- Veo 3 novos: 17 quadros (Q02-Q22 exceto CapCut)")
    txt = txt.replace("- Veo 3: 4 quadros (17%)", "- Veo 3 total: 21 quadros (71% do video)")

    with open(sb_path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("[OK] storyboard.txt atualizado — todos os quadros agora Veo 3")


def rebuild_prompts_video():
    """Reconstrói prompts_video.txt com todos os 21 quadros Veo 3."""
    src = os.path.join(PROMPTS_DIR, "prompts_video.txt")
    with open(src, encoding="utf-8") as f:
        original = f.read()

    # Header novo
    header = """================================================================================
PROMPTS DE VIDEO — VEO 3
Agência: Abismo Criativo
Canal: Sinais do Fim — Passagens do Apocalipse
Video: video-001-armagedom
Agente: Phantasma — Diretor de Cinematografia
Data: 2026-04-05 (REFATORADO — Veo 3 em todo o video)
================================================================================
Total de quadros Veo 3: 21 (Q02-Q22 exceto Q01/Q05/Q24 CapCut)
Total de clipes: 29 (17 novos x 1 clip + 4 originais x 3 clips)
Duracao por clipe: 10s
Cobertura total Veo 3: 232s (~3.9 minutos)
================================================================================

"""
    # Extrair blocos Q09, Q13, Q17, Q23 do original
    import re
    existing = {}
    for qnum in ["09","13","17","23"]:
        pat = rf'(={"{72}"}.*?QUADRO {qnum}.*?={"{72}"}.*?)(?=\n={"{72}"}\n[A-Z]|\Z)'
        m = re.search(pat, original, re.DOTALL)
        if m:
            existing[qnum] = m.group(1).strip() + "\n\n\n"

    # Construir output na ordem dos quadros
    output = header
    ORDER = ["02","03","04","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]

    for qnum in ORDER:
        if qnum in ["09","13","17","23"]:
            if qnum in existing:
                output += existing[qnum] + "\n"
        else:
            novo = next((q for q in NOVOS_QUADROS if q["num"] == qnum), None)
            if novo:
                output += build_new_block(novo)

    # Sumario
    output += """================================================================================
SUMARIO TECNICO — PHANTASMA (REFATORADO)
================================================================================
Total de prompts gerados: 29
Quadros cobertos: Q02-Q23 (todos exceto Q01/Q05/Q24 CapCut)
Novos quadros (1 clip): Q02,Q03,Q04,Q06,Q07,Q08,Q10,Q11,Q12,Q14,Q15,Q16,Q18,Q19,Q20,Q21,Q22
Quadros originais (3 clips): Q09,Q13,Q17,Q23
Duracao predominante: 0.5x slow motion | 0.3x nos momentos de impacto maximo
Aspect ratio: 16:9 (todos os clipes)
Paleta: #0A0A0A, #8B0000, #C5A355, #E8E0D0
Assinatura visual: Sujeito biblico em CORES vs mundo moderno em P&B
================================================================================
"""
    with open(src, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"[OK] prompts_video.txt reconstruido — {output.count('=== QUADRO')} blocos de clipe")


def upload_file(local, remote):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("31.97.165.64", username="root",
                key_filename=os.path.expanduser("~/.ssh/id_ed25519"))
    ssh.exec_command(f"mkdir -p {os.path.dirname(remote)}")
    sftp = ssh.open_sftp()
    sftp.put(local, remote)
    sftp.close(); ssh.close()
    rel = remote.replace("/opt/agencia/", "")
    url = f"http://31.97.165.64:3456/{rel}"
    print(f"[LINK] {url}")
    return url


if __name__ == "__main__":
    update_storyboard()
    rebuild_prompts_video()

    # Regenerar TXT via gerar_video_txt
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, os.path.join(BASE, "_tools", "gerar_video_txt.py")],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.stderr:
        print("[STDERR]", result.stderr[:500])
