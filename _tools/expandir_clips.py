#!/usr/bin/env python3
"""Expande todos os quadros de 1 clip para 3 clips (ESTABELECER/APROXIMAR/IMPACTAR)."""
import re, os, paramiko

BASE      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_DIR = os.path.join(BASE, "canais", "sinais-do-fim", "videos", "video-001-armagedom")
PROMPTS   = os.path.join(VIDEO_DIR, "5-prompts", "prompts_video.txt")

def ts_add(ts_str, seconds):
    """Soma N segundos a um timestamp M:SS."""
    p = ts_str.strip().split(":")
    t = int(p[0])*60 + int(p[1]) + seconds
    return f"{t//60}:{t%60:02d}"

# ── CLIPS 2 e 3 para cada quadro novo ─────────────────────────────────────────
# Formato: QUADRO_NUM → [clip2_dict, clip3_dict]
# Cada dict tem: prompt, framing, camera, lighting, dof, film, particles, speed, mood, continuity

EXPANSAO = {

"02": [
    {   # CLIP 2 — APROXIMAR
        "prompt": "Medium low angle looking upward at the descending medieval archangel from street level. The angel's vast feathered wings dominate the upper frame, each feather rendered in vivid gold and white detail. The massive flaming sword drips crimson and golden fire in ultra slow motion — each drop trailing sparks downward. The angel's ornate golden armor reflects the sword's fire in rippling highlights. Below the angel's feet, black and white rubble of a destroyed city street stretches into deep perspective. Dense black smoke curls around the angel's lower body. The camera performs a very slow tilt upward from the rubble to the angel's raised sword. 35mm grain, anamorphic lens. Color grading: vivid saturated angel against complete B&W destruction below. Volumetric golden light from above. 0.5x slow motion. Awe-inspiring, overwhelming divine presence. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Medium low angle — looking up at the angel from street level, wings filling upper frame",
        "camera": "Slow tilt upward from B&W rubble at bottom to the vivid angel's raised sword above",
        "lighting": "Practical fire light from dripping sword illuminating the angel from below, golden volumetric from above",
        "dof": "Shallow f/2.8 — angel and sword in sharp vivid focus, B&W rubble softly blurred in foreground",
        "film": "35mm grain, anamorphic flares from sword fire, saturated angel vs. B&W destruction",
        "particles": "Crimson fire drops falling in slow motion from the sword, golden sparks trailing each drop, black smoke curling",
        "speed": "0.5x slow motion",
        "mood": "Overwhelming divine presence — heaven's warrior seen from the ground",
        "continuity": "Shift from wide establishing to ground-level perspective — the angel now fills the sky above",
    },
    {   # CLIP 3 — IMPACTAR
        "prompt": "Extreme close-up on the archangel's massive flaming sword filling the entire frame. Golden and crimson fire engulfs the blade in vivid rolling waves. Dense spiraling embers and sparks radiate outward in all directions from the blade's edge. In the polished surface of the sword's metal, a distorted reflection of the black and white destroyed city below warps and shimmers through the heat. The camera holds steady on the blade as fire pulses with increasing intensity. Heat shimmer distorts the edges of the frame. 35mm grain, macro lens feel. Color grading: pure vivid crimson and gold fire against the distorted B&W reflection in metal. Extreme dramatic single-source fire light. 0.5x slow motion. Raw divine power made visible. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — the flaming sword fills the entire frame, fire radiating outward",
        "camera": "Locked steady on the blade — fire pulses with increasing intensity, no camera movement",
        "lighting": "Single source — the sword's own fire illuminates everything, pure fire light in crimson and gold",
        "dof": "Shallow f/1.8 — sword edge razor sharp, fire and sparks bokeh beyond",
        "film": "35mm grain, macro lens, crimson + gold fire against B&W reflection, heat shimmer distortion",
        "particles": "Dense spiraling embers radiating from blade edge, sparks in all directions, heat shimmer",
        "speed": "0.5x slow motion",
        "mood": "Raw divine power — the weapon of heaven in absolute detail",
        "continuity": "Climax of Q02 arc — from wide descent to ground-level awe to the weapon itself",
    },
],

"03": [
    {   # CLIP 2
        "prompt": "Medium shot of the translucent ancient medieval map floating above the Jezreel valley. The map's parchment surface glows in vivid gold and crimson, rendered as a three-dimensional floating object with visible thickness and worn edges. The camera slowly orbits counterclockwise around the floating map, revealing battle position markings that pulse crimson on its surface. Hebrew script glows along the borders. Below the map, the real valley landscape stretches in muted warm parchment tones. Ancient battle lines drawn in crimson fire connect Megiddo to surrounding locations. 35mm grain, anamorphic lens. Warm golden light radiates from the map itself. Dust particles drift through the golden haze between map and landscape. 0.5x slow motion. Revelatory, prophetic tension. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Medium — the floating map fills center frame, real valley visible below and through its translucent edges",
        "camera": "Slow counterclockwise orbit around the floating map — revealing its depth and battle markings",
        "lighting": "Self-luminous golden glow from the map, warm afternoon light on the valley below",
        "dof": "Medium f/4 — map in focus, valley softened below",
        "film": "35mm grain, anamorphic lens, warm gold and crimson tones",
        "particles": "Dust motes drifting through golden haze between map and landscape",
        "speed": "0.5x slow motion",
        "mood": "Prophecy materializing — the ancient plan becoming visible over the real land",
        "continuity": "From aerial establishing of Megiddo to examining the prophetic map up close",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on the crimson marker at Jerusalem on the floating ancient map. The marker burns with intense pulsing crimson fire, brighter than all other markings. Cracks spread outward from Jerusalem across the parchment surface — glowing crimson fissures radiating like veins of fire through the ancient material. Hebrew sacred text glows along the cracks. The camera holds steady as the burning intensifies, the entire map seeming to converge its energy toward this single point. The parchment darkens and smolders around Jerusalem. 35mm grain, macro feel. Color grading: vivid crimson marker against aging golden parchment. Single-point fire light from the marker. 0.5x slow motion. Convergence of all prophecy to one city. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — Jerusalem marker fills center frame, crimson cracks radiating outward",
        "camera": "Locked steady — the burning intensifies and cracks spread, all energy converging on Jerusalem",
        "lighting": "Single-point crimson fire light from Jerusalem marker, parchment darkening around it",
        "dof": "Shallow f/2.0 — Jerusalem marker razor sharp, surrounding map in soft focus",
        "film": "35mm grain, macro feel, vivid crimson against golden parchment",
        "particles": "Smoke wisps rising from smoldering parchment, crimson embers at the cracks",
        "speed": "0.5x slow motion",
        "mood": "All prophecy converges — one city at the center of everything",
        "continuity": "Climax of Q03 arc — from valley overview to map to the single point: Jerusalem",
    },
],

"04": [
    {   # CLIP 2
        "prompt": "Close-up on the ancient parchment scroll's surface as sacred text appears letter by letter. Each letter materializes first as a glowing crimson ember that burns into the parchment, then cools to rich gold. The camera slowly tracks along the line of text from left to right as new letters appear. Three wax seals at the scroll's lower edge drip in ultra slow motion — each drop of crimson wax stretching and falling. Candlelight flickers across the golden surface creating dancing shadows. The parchment texture is rich and detailed — visible fibers, age stains, creases. Background cathedral ruins barely visible in deep B&W shadow. 35mm grain, shallow depth of field. Warm candlelight key. 0.5x slow motion. Sacred intimacy — watching scripture write itself. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Close-up — text appearing on the scroll surface, wax seals dripping at the lower edge",
        "camera": "Slow lateral track following the text appearing from left to right",
        "lighting": "Practical candle light creating warm golden key, deep B&W shadow in background",
        "dof": "Shallow f/2.0 — text and wax seals sharp, background deep blur",
        "film": "35mm grain, warm golden color on parchment, chiaroscuro",
        "particles": "Wax drops stretching in slow motion, smoke wisps from candles, faint dust motes",
        "speed": "0.5x slow motion",
        "mood": "Sacred intimacy — witnessing divine words burn into existence",
        "continuity": "From wide scroll view to the text itself appearing on the surface",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on a single sacred symbol burning into the ancient parchment. The symbol appears as a vivid crimson glow that sears through the material in slow motion — smoke rising from each stroke as if drawn by invisible divine fire. The parchment fibers curl and darken around the burning symbol. The camera holds perfectly still as the complete symbol emerges stroke by stroke. A single wax seal fills the lower corner of the frame, its ancient mark cracked and glowing from within. Extreme warmth of candlelight creates deep golden tones on the parchment surface. 35mm grain, macro lens. Color grading: vivid crimson burning on golden parchment. 0.3x ultra slow motion. The word of God written in fire. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — single burning symbol on parchment, wax seal in corner",
        "camera": "Locked steady — watching the symbol burn stroke by stroke into the parchment",
        "lighting": "Extreme warm candlelight, self-luminous crimson from the burning symbol",
        "dof": "Very shallow f/1.4 — burning symbol sharp, everything else dreamy bokeh",
        "film": "35mm grain, macro lens, crimson fire on golden parchment",
        "particles": "Smoke rising from each burning stroke, parchment fibers curling in heat",
        "speed": "0.3x ultra slow motion",
        "mood": "The word of God — written in fire, one symbol at a time",
        "continuity": "Climax of Q04 arc — from scroll overview to text appearing to a single divine symbol",
    },
],

"06": [
    {   # CLIP 2
        "prompt": "Medium tracking shot following the red horseman of war from a low angle. The rider sits tall on the blood-red horse, a great sword raised high, crimson cloak billowing in slow motion. The horse's powerful legs gallop through ash and debris — each hoof strike sends up a burst of grey ash and crimson sparks. Behind the red rider, the other three horsemen are visible in dynamic motion blur — white, black, and pale shapes thundering forward. The camera tracks laterally keeping the red horseman centered. Background in black and white: burning skyscrapers and panicked crowds. Blood-red storm clouds above. 35mm grain, anamorphic lens. 0.5x slow motion. The fury of war in full gallop. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Medium low angle — red horseman centered, other three in background motion blur",
        "camera": "Lateral tracking shot keeping pace with the red horseman's gallop",
        "lighting": "Red-tinted storm light from above, crimson glow from the rider's sword and cloak",
        "dof": "Medium f/4 — red horseman in sharp focus, others in dynamic blur behind",
        "film": "35mm grain, anamorphic lens, vivid crimson rider against B&W destruction",
        "particles": "Ash clouds from hooves, crimson sparks on impact, smoke rising from B&W city",
        "speed": "0.5x slow motion",
        "mood": "The fury of war — one horseman isolated in all his destructive glory",
        "continuity": "From wide four-horsemen establishing to isolating the red rider of war",
    },
    {   # CLIP 3
        "prompt": "Close-up front-facing shot — all four horsemen of the Apocalypse charge directly toward the camera in vivid saturated color. The white horse and crowned rider lead center, bow drawn. The red, black, and pale horses flank in V-formation. Hooves pound the ground sending massive ash clouds upward. The pale horse carrying skeletal Death fills the right of frame, sickly green glow emanating from its rider. All four horsemen's faces are intense and relentless. The camera is at ground level as they charge forward — overwhelming the frame. Background in B&W: explosions and collapsing buildings. 35mm grain, wide anamorphic. 0.3x ultra slow motion. Extinction riding forward. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Close-up front-facing — four horsemen charging directly at camera in V-formation",
        "camera": "Ground-level locked — horsemen charge toward and overwhelm the frame",
        "lighting": "Each horseman self-illuminated in their color — white, crimson, black, sickly green",
        "dof": "Deep f/8 — all four horsemen sharp, B&W background slightly soft",
        "film": "35mm grain, wide anamorphic, vivid saturated riders against B&W explosions",
        "particles": "Massive ash clouds from charging hooves, embers from explosions behind",
        "speed": "0.3x ultra slow motion",
        "mood": "Extinction charging — the four forces of the end coming directly at you",
        "continuity": "Climax of Q06 arc — from wide side view to red rider detail to all four charging at camera",
    },
],

"07": [
    {   # CLIP 2
        "prompt": "Close-up on the center of the burning Middle East map — Jerusalem radiates intense crimson light outward in pulsing waves. The floating heraldic shield emblems of nations orbit closer around Jerusalem in slow motion — each shield rendered in vivid full color with national symbols glowing. The map's parchment surface cracks and smolders around the holy city, golden fire tracing fault lines between nations. Crimson sonar-like pulses expand outward from Jerusalem, washing over each national emblem as they pass. The camera performs a very slow push in toward the burning center. Background in B&W: missile trails and smoke columns. 35mm grain, anamorphic lens. 0.5x slow motion. All nations converging on one point. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Close-up — Jerusalem at center, national shield emblems orbiting closer",
        "camera": "Slow push in toward Jerusalem as crimson pulses radiate outward",
        "lighting": "Intense crimson from Jerusalem center, golden glow from national emblems",
        "dof": "Medium f/4 — Jerusalem and nearest shields in focus, outer edges softening",
        "film": "35mm grain, anamorphic flares from crimson pulses, gold + crimson grading",
        "particles": "Crimson pulse waves radiating, ember trails from shield emblems, smoke from parchment",
        "speed": "0.5x slow motion",
        "mood": "Convergence — all nations drawn toward one ancient city",
        "continuity": "From overview of map to focusing on the epicenter: Jerusalem and the nations converging",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on a single conflict marker on the ancient Middle East map as it detonates in crimson fire. The explosion sends a visible shockwave across the parchment surface — the golden material rippling like water from the impact point. Surrounding text and battle markings glow brighter as the shockwave passes through them. The parchment cracks and darkens in a starburst pattern around the detonation. Ember fragments and smoke rise from the impact crater on the map. The camera holds steady as the shockwave expands and fades. 35mm grain, macro feel. Vivid crimson explosion against golden parchment. 0.3x ultra slow motion. One spark that ignites the final war. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — single conflict marker detonating, shockwave rippling across parchment",
        "camera": "Locked steady — the detonation and shockwave are the movement",
        "lighting": "Self-luminous crimson from detonation, golden ambient from surrounding parchment",
        "dof": "Shallow f/2.0 — detonation point sharp, shockwave ripples in soft focus expanding outward",
        "film": "35mm grain, macro feel, crimson explosion on golden parchment",
        "particles": "Ember fragments, parchment debris, smoke rising from impact crater",
        "speed": "0.3x ultra slow motion",
        "mood": "The spark — one event that triggers the prophesied convergence",
        "continuity": "Climax of Q07 arc — from map overview to Jerusalem convergence to the triggering event",
    },
],

"08": [
    {   # CLIP 2
        "prompt": "Close-up on a specific conflict date on the illuminated timeline scroll. The golden numeral of the year smolders with deepening crimson — embers glow around each digit as if the date itself is a wound that never healed. The surrounding parchment darkens and crackles from the heat of this moment in history. The camera performs a very slow push in toward the smoldering date. Faint desaturated archival imagery of war is visible as ghostly reflections in the golden surface of the parchment. A heraldic explosion symbol above the date pulses with crimson fire. 35mm grain, shallow depth of field. Golden warm light from the scroll. 0.5x slow motion. History as open wound. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Close-up — single conflict date filling center frame, smoldering on the scroll",
        "camera": "Slow push in toward the date — 15% advance over 8 seconds",
        "lighting": "Self-luminous golden glow from scroll, crimson smolder from the conflict date",
        "dof": "Shallow f/2.8 — date and explosion symbol sharp, rest of scroll in soft focus",
        "film": "35mm grain, warm gold with crimson accents, ghostly B&W reflections",
        "particles": "Embers glowing around the digits, smoke wisps rising, parchment crackling",
        "speed": "0.5x slow motion",
        "mood": "History as open wound — each conflict date still burning on the scroll of time",
        "continuity": "From wide timeline to isolating one specific wound in history",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on the edge of the illuminated timeline scroll where the dates end. The last golden numeral glows at the very edge of the parchment — beyond it, nothing. Raw, torn parchment edge. The unwritten future. The camera slowly advances past the final date toward the blank edge. The parchment trembles faintly as if alive. Smoke rises from the final date. The blank parchment beyond the edge dissolves into deep black void. A faint crimson glow suggests the next date is about to burn into existence. 35mm grain, macro lens. Golden light from the final date, darkness beyond. 0.3x ultra slow motion. The future unwritten — we are at the edge of prophecy. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — the final date at the scroll's edge, blank void beyond",
        "camera": "Slow advance past the final date toward the blank edge of the unwritten future",
        "lighting": "Golden glow from the final date, deep darkness beyond the scroll's edge",
        "dof": "Very shallow f/1.4 — final date sharp, void beyond in deep blur",
        "film": "35mm grain, macro lens, golden date against black void",
        "particles": "Smoke from the final date, faint crimson embers at the blank edge suggesting the next unwritten event",
        "speed": "0.3x ultra slow motion",
        "mood": "The edge of prophecy — we are living at the end of the written scroll",
        "continuity": "Climax of Q08 arc — from full timeline to one wound to the terrifying blank edge",
    },
],

"10": [
    {   # CLIP 2
        "prompt": "Close-up from behind the prophet Zechariah's shoulder and raised hands. His fingers are spread wide, silhouetted against the golden light column descending from above. Through the gaps between his fingers, the black and white ruins of ancient Jerusalem stretch into deep perspective — collapsed walls, fallen columns, desolation. The illuminated scroll rises upward past his hands, golden Hebrew text glowing as it ascends. His robes of deep blue and purple billow slowly. The camera performs a slow tilt upward along the rising scroll. 35mm grain, anamorphic lens. Color grading: vivid prophet against B&W ruins seen through his hands. 0.5x slow motion. The prophet as conduit between heaven and ruin. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Close-up over shoulder — prophet's raised hands framing B&W ruins beyond, scroll rising between",
        "camera": "Slow tilt upward following the rising scroll past the prophet's outstretched hands",
        "lighting": "Golden volumetric column from above, B&W cold light on ruins visible through finger gaps",
        "dof": "Medium f/4 — hands and scroll in focus, ruins as secondary focus through gaps",
        "film": "35mm grain, anamorphic lens, vivid prophet and scroll against B&W ruins seen through hands",
        "particles": "Golden text particles rising from scroll, ash and cinders floating past the prophet's hands",
        "speed": "0.5x slow motion",
        "mood": "The prophet as conduit — standing between heaven's words and earth's destruction",
        "continuity": "From wide establishing of prophet to intimate over-shoulder perspective",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on the illuminated scroll's surface as it rises past the prophet's face. Glowing Hebrew text in golden fire traces each sacred letter in vivid detail against the ancient parchment. The prophet's face is barely visible behind the scroll — eyes intense, lips moving in silent prophecy, lit by the golden glow of his own words. The camera holds as the scroll rises slowly upward, each line of text burning brighter than the last. The final line pulses with crimson urgency. 35mm grain, macro feel. Golden fire text against parchment, prophet's face in warm shadow beyond. 0.3x ultra slow motion. The words themselves are alive. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — scroll text in foreground, prophet's prophesying face visible behind",
        "camera": "Locked — the scroll rises slowly upward through the frame, text lines passing",
        "lighting": "Self-luminous golden fire from Hebrew text, warm ambient glow on prophet's face beyond",
        "dof": "Very shallow f/1.4 — text razor sharp, prophet's face in soft warm focus behind",
        "film": "35mm grain, macro feel, golden fire text against ancient parchment",
        "particles": "Golden letter fragments rising from text, faint smoke from burning parchment",
        "speed": "0.3x ultra slow motion",
        "mood": "Living scripture — the words of prophecy burning themselves into existence",
        "continuity": "Climax of Q10 arc — from prophet establishing to over-shoulder to the sacred text itself",
    },
],

"11": [
    {   # CLIP 2
        "prompt": "Medium shot slowly tilting upward along the seven-headed beast's massive serpentine body. The camera ascends from the beast's armored torso — dark green and crimson scales rendered in vivid medieval illustration detail — upward through coiling necks toward the heads above. Each head turns in sequence as the camera passes, its glowing digital camera eye focusing with a mechanical red iris contraction. Red digital scan lines sweep across the frame at each eye focus. The beast's body writhes with slow power. Background in B&W: surveillance screens and watchtower silhouettes. 35mm grain, anamorphic lens. Color grading: vivid creature against B&W surveillance city. 0.5x slow motion. Technology wearing ancient skin. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Medium tilting upward — beast's body ascending through frame, heads turning above",
        "camera": "Slow vertical tilt from armored torso upward through coiling necks toward the seven heads",
        "lighting": "Red scan line sweeps from each camera eye, dim ambient from B&W screens behind",
        "dof": "Medium f/4 — beast in sharp vivid focus, surveillance city as secondary blur",
        "film": "35mm grain, anamorphic lens, vivid medieval beast against B&W surveillance",
        "particles": "Red digital scan lines sweeping the frame, static interference flickers",
        "speed": "0.5x slow motion",
        "mood": "Ancient horror with digital eyes — technology wearing the skin of prophecy",
        "continuity": "From wide establishing to ascending along the beast's body toward its surveillance heads",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on one head of the seven-headed beast. The glowing digital camera eye fills the center of the frame — a mechanical red iris contracts to focus directly at the viewer. The crimson and dark green scales of the head surround the eye in vivid ornate medieval detail. Inside the eye's lens, miniature reflections of CCTV screens and surveilled crowds are visible. A red scan beam pulses outward from the eye, sweeping across the frame toward the camera. The beast's jaw opens slightly revealing darkness within. 35mm grain, macro feel. Vivid crimson eye against dark scales. 0.3x ultra slow motion. You are being watched by something ancient. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — one beast head's camera eye filling center frame, jaw slightly open",
        "camera": "Locked steady — the eye focuses and the scan beam sweeps toward the viewer",
        "lighting": "Self-luminous red from the camera eye, reflected CCTV light in the lens",
        "dof": "Very shallow f/1.4 — eye iris razor sharp, surrounding scales in soft focus",
        "film": "35mm grain, macro feel, vivid red eye against dark ornate scales",
        "particles": "Red scan beam pulsing outward, digital static interference at frame edges",
        "speed": "0.3x ultra slow motion",
        "mood": "Being watched — something ancient and technological has locked onto you",
        "continuity": "Climax of Q11 arc — from wide beast to ascending body to a single terrifying eye",
    },
],

"12": [
    {   # CLIP 2
        "prompt": "Close-up on the outstretched human hand rotating slowly in warm light. The microchip beneath the skin pulses with intricate bioluminescent blue and gold circuit patterns — each circuit line visible through the translucent flesh. The ancient wax seal in deep crimson and gold floats closer to the hand, its cracked surface glowing with symbols that mirror the chip's circuits. The camera orbits slowly around the hand as if examining it. Binary code falls in B&W behind the hand. The two technologies — ancient mark and modern chip — seem to be merging. 35mm grain, anamorphic lens. Color grading: warm skin tones and glowing circuits against B&W digital rain. 0.5x slow motion. Ancient and modern control becoming one. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Close-up — hand rotating slowly, microchip circuits visible, wax seal floating closer",
        "camera": "Slow orbit around the hand — examining the chip from multiple angles",
        "lighting": "Bioluminescent blue-gold from the chip beneath skin, warm ambient on hand, B&W digital rain behind",
        "dof": "Shallow f/2.8 — hand and chip in sharp focus, floating seal slightly soft, B&W background blur",
        "film": "35mm grain, anamorphic lens, warm skin + glowing circuits against B&W binary rain",
        "particles": "B&W binary code falling behind, faint bioluminescent motes rising from the chip",
        "speed": "0.5x slow motion",
        "mood": "The mark evolving — ancient control and modern technology becoming indistinguishable",
        "continuity": "From wide overview to examining the convergence of chip and ancient seal",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on the back of the hand — the microchip's bioluminescent circuit pattern is fully visible through translucent skin, pulsing with electric blue and gold light. The circuits expand and grow like living veins across the flesh. The ancient wax seal's symbols have merged with the circuit pattern — crimson sigils and blue circuits intertwined as one system. The camera holds steady as the merged pattern pulses with increasing intensity, each pulse sending a ripple through the skin. Binary code reflects across the skin surface. 35mm grain, macro lens. Color grading: vivid bioluminescent circuits on warm flesh against falling B&W binary. 0.3x ultra slow motion. The mark is already inside. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — microchip circuits merging with ancient seal marks on skin surface",
        "camera": "Locked steady — the merged pattern pulses and expands across the skin",
        "lighting": "Bioluminescent blue-gold from circuits within, crimson glow from the merged seal symbols",
        "dof": "Very shallow f/1.4 — circuit pattern razor sharp, skin texture dreamy beyond",
        "film": "35mm grain, macro lens, vivid bioluminescent circuits and crimson seals on flesh",
        "particles": "Bioluminescent motes, binary reflections on skin, faint pulse ripples through flesh",
        "speed": "0.3x ultra slow motion",
        "mood": "The mark is already inside — ancient prophecy and modern control are one and the same",
        "continuity": "Climax of Q12 arc — from overview to examination to the horrifying merger under the skin",
    },
],

"14": [
    {   # CLIP 2
        "prompt": "Medium shot slowly pushing toward the shadowy figure seated on the ornate golden throne. Holographic translucent screens surround the figure, displaying streams of global data and surveillance feeds in eerie cold blue. The figure remains obscured in deep shadow — only the silhouette of broad shoulders and a crowned head visible against the red smoke behind. The camera advances slowly, the holographic screens parting slightly as if making way. The throne's golden carvings catch the blue holographic light. Red smoke particles rise around the throne legs. Background in B&W: vast command center with tiny operators at screens. 35mm grain, anamorphic lens. 0.5x slow motion. Approaching the seat of absolute power. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Medium — camera advancing toward the shadowy figure on throne, holographic screens parting",
        "camera": "Slow deliberate push in toward the figure — holographic screens part as camera advances",
        "lighting": "Cold blue from holographic screens, warm golden reflections on throne carvings, deep shadow on figure",
        "dof": "Medium f/4 — throne and figure in focus, holographic screens at varying focus depths",
        "film": "35mm grain, anamorphic lens, cold blue screens + warm gold throne + red smoke",
        "particles": "Red smoke rising from floor, holographic data streams, faint static interference",
        "speed": "0.5x slow motion",
        "mood": "Approaching absolute power — each step closer reveals more control and more darkness",
        "continuity": "From wide throne room establishing to slowly closing the distance to the hidden ruler",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on the shadowy figure's hand resting on the golden throne armrest. The fingers tap slowly in a deliberate rhythm against the ornate golden carvings. Holographic reflections dance across the gold surface — miniature surveillance feeds, financial data, population counters reflected in the polished metal. The hand is shrouded in deep shadow — only the suggestion of skin and dark rings visible. Above the hand, red smoke particles drift upward. The throne's carved details include ancient symbolic faces with eyes that seem to follow. 35mm grain, macro feel. Color grading: golden throne carvings with blue holographic reflections and red smoke. 0.3x ultra slow motion. Power reduced to a single gesture. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — shadowy hand tapping on golden throne armrest, holographic reflections visible",
        "camera": "Locked steady — the slow tap of fingers is the only movement, reflections dance in gold",
        "lighting": "Holographic blue-white reflections on gold surface, deep shadow on the hand, red smoke glow above",
        "dof": "Very shallow f/1.4 — tapping fingers and throne carvings sharp, everything else in dreamy blur",
        "film": "35mm grain, macro feel, golden carvings with blue holo reflections and red smoke",
        "particles": "Red smoke drifting above the hand, holographic data dancing on gold surface",
        "speed": "0.3x ultra slow motion",
        "mood": "Absolute control — the entire world reduced to the tap of one dark hand on gold",
        "continuity": "Climax of Q14 arc — from wide command center to approach to the hand that controls everything",
    },
],

"15": [
    {   # CLIP 2
        "prompt": "Medium shot dollying laterally along the crimson fissure that splits the world in two. On the left side: warm golden divine light bathes the ornate medieval temple — radiant cross, angel wings, sacred arches in vivid gold and white. On the right: cold blue-grey technological darkness — surveillance screens, shadowy corporate towers, digital grids. The camera moves along the fissure from top to bottom, revealing the depth of the split — molten crimson lava glows within the crack. Fragments of both worlds crumble and fall into the void. The golden light and cold blue fight for dominance at the fissure edge. 35mm grain, anamorphic lens. 0.5x slow motion. Reality splitting along the line of faith. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Medium — split world visible on both sides, camera traveling along the crimson fissure between them",
        "camera": "Lateral dolly traveling along the fissure from top to bottom, revealing its depth",
        "lighting": "Warm golden light from temple side, cold blue from technology side, crimson glow from the fissure",
        "dof": "Deep f/8 — both worlds visible with equal clarity, fissure glowing between",
        "film": "35mm grain, anamorphic lens, warm gold vs. cold blue with crimson fissure",
        "particles": "Fragments falling into the fissure from both sides, molten embers rising from the crack",
        "speed": "0.5x slow motion",
        "mood": "The great divide — two realities splitting further apart with every passing moment",
        "continuity": "From wide split-world establishing to traveling the divide itself",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on the crimson fissure itself — the crack between two realities. Molten crimson lava flows within the fissure, glowing with intense heat. Fragments from both worlds fall into the void — pieces of golden temple architecture and cold technological debris tumbling together into the crimson depth. The camera looks straight down into the fissure. The heat shimmer distorts the edges. The lava churns and pulses. Deep within the crack, there is only fire and void. 35mm grain, macro feel looking into the crack. Color grading: vivid crimson lava, golden and blue fragments falling. 0.3x ultra slow motion. Looking into the end of the world. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up looking down into the fissure — molten crimson lava, falling fragments",
        "camera": "Locked overhead looking straight down into the crack — the lava churns below",
        "lighting": "Self-luminous crimson from the lava within, mixed golden and blue light from falling fragments",
        "dof": "Shallow f/2.0 — fissure edges sharp, lava depths in soft fiery glow",
        "film": "35mm grain, macro feel, vivid crimson lava with heat shimmer distortion",
        "particles": "Golden temple fragments and blue-grey tech debris falling into the lava, heat shimmer",
        "speed": "0.3x ultra slow motion",
        "mood": "The void between — where faith and materialism meet there is only fire",
        "continuity": "Climax of Q15 arc — from wide split world to the fissure's edge to looking directly into the abyss",
    },
],

"16": [
    {   # CLIP 2
        "prompt": "Medium shot of the golden angel swinging the sword of pure light in a powerful arc. The blade trails brilliant white-gold energy as it cuts through the dark storm air. The dark angel in shadow-purple and crimson recoils from the strike — dark feathered wings folding protectively. The collision between sword and dark fire sends a spray of golden and purple sparks in all directions. The camera follows the sword's arc in a slow lateral movement. Below in B&W: surging opposing crowds react to the battle above. Lightning arcs across the storm sky. 35mm grain, anamorphic lens. 0.5x slow motion. Divine offense — light pressing against darkness. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Medium — golden angel's sword mid-swing, dark angel recoiling, sparks exploding between",
        "camera": "Slow lateral follow of the sword's arc — tracking the strike from wind-up to impact",
        "lighting": "Brilliant white-gold from sword of light, shadow-purple from dark angel, lightning flashes",
        "dof": "Medium f/4 — both angels in focus, B&W crowds below as secondary",
        "film": "35mm grain, anamorphic flares from sword of light, gold vs. purple energy",
        "particles": "Golden and purple sparks from collision, lightning arcs, energy trails from sword",
        "speed": "0.5x slow motion",
        "mood": "Divine offense — the sword of light pressing against the shadow's defenses",
        "continuity": "From wide establishing of both angels to isolating the moment of sword strike",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on the collision point between the sword of pure light and the dark angel's fire. A blinding explosion of golden and purple energy fills the entire frame — the two forces pushing against each other in a visible shockwave. Lightning arcs outward from the collision in all directions. The sword's golden edge is visible at one side, the dark fire at the other, the explosion between them consuming the center. Energy ripples distort the air. The camera holds perfectly still as the explosion expands and pulses. 35mm grain, macro feel. Color grading: vivid gold vs. deep purple explosion. 0.3x ultra slow motion. The moment heaven and hell collide. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — collision point filling the frame, golden sword edge vs. dark fire",
        "camera": "Locked steady — the explosion of opposing energies is the only movement",
        "lighting": "Blinding golden and purple energy explosion as the sole light source",
        "dof": "Shallow f/2.0 — collision point sharp, energy ripples in expanding soft focus",
        "film": "35mm grain, macro feel, vivid gold vs. purple energy explosion",
        "particles": "Lightning arcs outward, golden and purple energy sparks, air distortion ripples",
        "speed": "0.3x ultra slow motion",
        "mood": "The collision — the exact moment light meets darkness and reality fractures",
        "continuity": "Climax of Q16 arc — from wide combat to sword strike to the point of impact itself",
    },
],

"18": [
    {   # CLIP 2
        "prompt": "Medium low angle looking upward at the mighty medieval angel's face as the golden trumpet sounds. The angel's expression is grave and authoritative — eyes looking downward at the doomed earth. The trumpet bell extends upward out of frame. Visible golden shockwaves ripple outward from the trumpet in concentric rings. The angel's vast luminous wings frame the dark blood-red sky behind. Golden armor reflects the trumpet's blast energy. The camera performs a very slow push in toward the angel's face. Below in B&W: the cracking earth is visible at the bottom edge of frame. 35mm grain, anamorphic lens. 0.5x slow motion. The face of the one who sounds the end. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Medium low angle — angel's grave face center frame, trumpet extending upward, wings framing sky",
        "camera": "Slow push in toward the angel's face — 15% advance over 8 seconds",
        "lighting": "Golden energy from trumpet blast illuminating the angel's face from above, blood-red sky beyond",
        "dof": "Shallow f/2.8 — angel's face and expression in sharp focus, wings and sky in soft focus",
        "film": "35mm grain, anamorphic flares from golden shockwaves, vivid angel against blood-red sky",
        "particles": "Golden shockwave rings expanding from trumpet, falling ash, storm cloud turbulence",
        "speed": "0.5x slow motion",
        "mood": "The face of judgment — the angel who sounds the end knows what comes next",
        "continuity": "From wide angel-over-cracked-earth to the angel's face as the trumpet sounds",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on the ornate golden trumpet's bell as the blast erupts from it. The golden energy shockwave explodes outward from the trumpet opening in vivid concentric rings — each ring visible as a physical wave of golden light tearing through the blood-red sky. The trumpet's interior glows with white-hot intensity. Sound itself made visible as golden ripples that distort the air and part the storm clouds. The camera is positioned directly in front of the trumpet bell. The blast fills the entire frame. 35mm grain, macro feel. Color grading: vivid gold blast against blood-red sky. 0.3x ultra slow motion. The sound that ends the world. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — trumpet bell filling frame, golden blast erupting directly at camera",
        "camera": "Locked directly in front of trumpet bell — the blast wave is the movement",
        "lighting": "White-hot intensity from trumpet interior, golden shockwave rings illuminating the blood-red sky",
        "dof": "Shallow f/2.0 — trumpet edge sharp, blast waves in expanding soft focus",
        "film": "35mm grain, macro feel, vivid gold blast against blood-red sky",
        "particles": "Golden shockwave rings, sound ripples distorting air, storm clouds parting from the blast",
        "speed": "0.3x ultra slow motion",
        "mood": "The sound that ends the world — pure divine energy erupting from heaven's instrument",
        "continuity": "Climax of Q18 arc — from wide establishing to angel's face to the trumpet blast itself",
    },
],

"19": [
    {   # CLIP 2
        "prompt": "Close-up pushing into one panel of the four-panel disaster collage — the earthquake panel. Massive ground fissures crack open in black and white, swallowing sections of earth. The red border frame (#8B0000) glows intensely around this panel. The spectral medieval prophet overlay becomes more vivid and saturated as the camera enters the panel — his outstretched warning hand visible across the destruction. Buildings collapse into the fissures in slow motion. Dust and debris fill the air. The camera pushes slowly through the red border into the earthquake scene. 35mm grain. Color grading: deep B&W disaster with vivid crimson borders and the prophet's saturated overlay. 0.5x slow motion. Entering the catastrophe. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Close-up — entering the earthquake panel through its red border, prophet overlay intensifying",
        "camera": "Slow push in through the red border into the earthquake destruction",
        "lighting": "Crimson glow from panel border, pale grey B&W light within the disaster, prophet overlay in warm color",
        "dof": "Medium f/4 — fissures and destruction in focus, prophet overlay as translucent depth",
        "film": "35mm grain, B&W earthquake with crimson borders and saturated prophet overlay",
        "particles": "Dust and debris from collapsing buildings, rubble falling into fissures, the prophet's spectral glow",
        "speed": "0.5x slow motion",
        "mood": "Entering the catastrophe — stepping through the frame into the destruction itself",
        "continuity": "From four-panel overview to entering one disaster — the earthquake consumes the viewer",
    },
    {   # CLIP 3
        "prompt": "The four disaster panels collapse inward in slow motion, their red borders shattering like glass. The earthquake, hurricane, wildfire, and drought merge into a single overwhelming scene of total devastation in black and white. At the center of the merged destruction, the medieval prophet stands in full vivid color — arms outstretched in desperate warning, robes of deep crimson and gold billowing. His figure is the only color in a world of grey catastrophe. The camera holds as the panels merge around him. Debris from all four disasters fills the air. 35mm grain, anamorphic lens. Vivid prophet centered in B&W apocalypse. 0.3x ultra slow motion. One voice screaming in the silence of the end. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Wide — four panels collapsing into one merged scene, vivid prophet at the center",
        "camera": "Locked steady — the four panels collapse inward and merge around the prophet",
        "lighting": "B&W catastrophe light surrounding the single warm golden and crimson light source: the prophet",
        "dof": "Deep f/8 — prophet and surrounding devastation all in focus for maximum impact",
        "film": "35mm grain, anamorphic lens, vivid prophet isolated against B&W merged devastation",
        "particles": "Debris from all four disasters — rocks, water spray, embers, dust — swirling around the prophet",
        "speed": "0.3x ultra slow motion",
        "mood": "One voice in the apocalypse — the prophet standing at the center of all catastrophe",
        "continuity": "Climax of Q19 arc — from four panels to entering one to all disasters merging around the prophet",
    },
],

"20": [
    {   # CLIP 2
        "prompt": "Medium shot slowly orbiting around the kneeling praying figure illuminated by the divine golden light column. As the camera orbits, the surrounding B&W shadows reveal different threats — soldier silhouettes shift position, rifle barrels catch faint light, chains on the ground form patterns. The golden light column intensifies with each second, casting longer radiant shadows outward. The praying figure's upturned face is bathed in warm golden light. The contrast between the divine light island and the oppressive B&W darkness sharpens. Prison bars cast shadow patterns across the ground. 35mm grain, anamorphic lens. 0.5x slow motion. Faith surrounded — light persisting in total darkness. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Medium — camera orbiting the kneeling figure, shadows revealing threats on all sides",
        "camera": "Slow 90-degree orbit around the praying figure — each angle reveals new B&W threats",
        "lighting": "Divine golden column as sole warm light, B&W shadow revealing soldier silhouettes",
        "dof": "Medium f/4 — praying figure in sharp focus, surrounding threats in varying shadow depth",
        "film": "35mm grain, anamorphic lens, golden light island against oppressive B&W darkness",
        "particles": "Dust motes in the golden column, faint shadow patterns from prison bars",
        "speed": "0.5x slow motion",
        "mood": "Faith surrounded — golden light persisting despite the encircling darkness",
        "continuity": "From establishing overview to orbiting the figure, revealing the depth of persecution",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on the praying figure's clasped hands illuminated by the divine golden light from above. The hands are weathered, strong, pressed tightly together in deep prayer. A single tear rolls down the visible cheek in ultra slow motion — catching the golden light and refracting it like a tiny prism. On the ground beside the hands, heavy chains lie coiled — cold iron in B&W against the warm golden light on the skin. The camera holds perfectly still as the tear descends. The golden light pulses brighter. 35mm grain, macro lens. Color grading: warm golden light on hands and tear against B&W chains and shadows. 0.3x ultra slow motion. Faith distilled to a single tear in the light. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — clasped hands in golden light, single tear, chains on ground beside",
        "camera": "Locked steady — the single tear's descent is the movement",
        "lighting": "Divine golden light from above illuminating hands and tear, chains in B&W shadow",
        "dof": "Very shallow f/1.4 — hands and tear razor sharp, chains in soft B&W blur beside",
        "film": "35mm grain, macro lens, warm golden on hands against B&W chains",
        "particles": "The single tear catching light, dust motes in the golden column",
        "speed": "0.3x ultra slow motion",
        "mood": "Faith distilled — everything reduced to clasped hands, one tear, and golden light",
        "continuity": "Climax of Q20 arc — from wide isolation to orbit to the intimate moment of prayer",
    },
],

"21": [
    {   # CLIP 2
        "prompt": "Medium shot pushing toward the massive burning number 360 MILLION in blood-red medieval numerals. The flames intensify as the camera approaches — each digit writhes with fire, embers consuming the edges. Below, the ancient illuminated world map comes into sharper focus — blood-red flame markers pulsing across every continent. The camera advances slowly, the heat shimmer from the burning numerals distorting the upper frame. Smoke rises in dense black columns behind the numbers. The emotional weight of the number grows heavier with proximity. 35mm grain, anamorphic lens. Color grading: vivid crimson burning numerals against deep black, warm parchment map below. 0.5x slow motion. A number so large it burns. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Medium — burning numerals growing larger as camera approaches, persecution map below",
        "camera": "Slow push in toward the burning numerals — the number fills more of the frame with each second",
        "lighting": "Self-luminous crimson fire from burning numerals, red glow from map markers below",
        "dof": "Medium f/4 — numerals in sharp focus, map becoming clearer below",
        "film": "35mm grain, anamorphic lens, vivid crimson fire against deep black void",
        "particles": "Dense embers consuming numeral edges, smoke rising, heat shimmer distortion",
        "speed": "0.5x slow motion",
        "mood": "The weight of a number — 360 million persecuted, each digit burning with their suffering",
        "continuity": "From wide establishing to advancing toward the staggering number",
    },
    {   # CLIP 3
        "prompt": "Extreme close-up on one single blood-red flame marker on the ancient world map surface. This one flame represents millions. The camera holds steady on this solitary marker — a small but intense crimson fire burning on the parchment. The parchment around it darkens and curls from the heat. The flame flickers and pulses with a heartbeat rhythm. Surrounding the flame, faintly visible golden text names the region. The map's parchment fibers are visible in extreme detail — ancient, fragile, bearing the weight of suffering. 35mm grain, macro lens. Vivid single crimson flame against aged golden parchment. 0.3x ultra slow motion. One flame. Millions of lives. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Extreme close-up — single persecution flame marker on the ancient world map surface",
        "camera": "Locked steady — the flame pulses with a heartbeat rhythm, parchment darkens around it",
        "lighting": "Self-luminous crimson from the single flame marker, warm golden ambient from parchment",
        "dof": "Very shallow f/1.4 — flame marker razor sharp, surrounding map in dreamy soft focus",
        "film": "35mm grain, macro lens, vivid crimson flame against golden parchment",
        "particles": "The flame flickering with heartbeat pulse, parchment fibers curling from heat",
        "speed": "0.3x ultra slow motion",
        "mood": "One flame for millions — the unbearable intimacy of reducing lives to a map marker",
        "continuity": "Climax of Q21 arc — from staggering number to approaching it to one single flame that holds millions",
    },
],

"22": [
    {   # CLIP 2
        "prompt": "Medium low angle looking upward at the rider on the magnificent white horse descending through golden parting clouds. The rider's armor gleams in vivid gold and white — the sword of brilliant light raised high, robes streaming upward behind. The white horse is majestic — muscular, mane flowing in slow motion, hooves pressing down through clouds. The camera is positioned below, looking up as they descend, giving the rider towering divine scale. The golden light intensifies around the descending figure. Far below in B&W: thousands of tiny human figures visible, some falling to knees. Storm clouds part further revealing more golden radiance. 35mm grain, anamorphic lens. 0.5x slow motion. Heaven descending with authority. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Medium low angle — rider and white horse descending from above, golden sky opening behind",
        "camera": "Slow tilt upward tracking the descent — the rider grows more dominant in the frame",
        "lighting": "Blinding golden radiance from the opening heaven above, sword of light adding pure white illumination",
        "dof": "Medium f/4 — rider and horse in sharp vivid focus, clouds and B&W crowds below as secondary",
        "film": "35mm grain, anamorphic flares from the sword of light, vivid gold against parting storm",
        "particles": "Cloud wisps parting, golden light motes, robes and horse mane streaming in the descent",
        "speed": "0.5x slow motion",
        "mood": "Heaven descending with absolute authority — the promised return made visible",
        "continuity": "From wide heavens-opening to the rider and horse seen from below as they descend",
    },
    {   # CLIP 3
        "prompt": "Close-up on the sword of pure brilliant light held high by the descending rider. The sword blazes with white-gold energy that illuminates everything around it — the rider's face is completely obscured by the divine radiance pouring from the blade. The camera looks upward at the sword against the golden opened heavens. Far below in deep B&W: a sea of thousands of tiny human figures on their knees — a world surrendering to the return. The golden light from the sword expands to fill the frame, engulfing the camera. The final moment before divine light consumes everything. 35mm grain, anamorphic lens. 0.3x ultra slow motion. The light that ends the darkness forever. Duration 8 seconds. Aspect ratio 16:9.",
        "framing": "Close-up upward — sword of light blazing against golden heavens, B&W kneeling multitudes below",
        "camera": "Slow tilt upward — the sword's light expands to fill and engulf the entire frame",
        "lighting": "Blinding white-gold energy from the sword consuming the entire scene, golden heaven beyond",
        "dof": "Deep f/8 — sword light consuming focus itself, everything dissolving into golden radiance",
        "film": "35mm grain, anamorphic flares everywhere from the overwhelming light, golden wash",
        "particles": "Pure golden light motes filling the frame, storm clouds dissolved, radiance consuming everything",
        "speed": "0.3x ultra slow motion",
        "mood": "The light that ends the darkness — divine radiance consuming the entire world",
        "continuity": "Climax of Q22 arc and final clip of the video — from wide descent to rider close to the sword's light engulfing all",
    },
],

}


def build_block(qnum, clip_n, total, ts_base, d):
    """Constroi um bloco de prompt_video.txt."""
    offset = (clip_n - 1) * 8
    ts_start = ts_add(ts_base, offset)
    ts_end   = ts_add(ts_base, offset + 8)
    lines = [
        f"=== QUADRO {qnum} — [{ts_base}] — CLIPE {clip_n} de {total} ===",
        f"TIMESTAMP: {ts_start} - {ts_end}",
        f"DURACAO: 8s",
        f"PROMPT:",
        d["prompt"],
        f"ENQUADRAMENTO: {d['framing']}",
        f"CAMERA: {d['camera']}",
        f"ILUMINACAO: {d['lighting']}",
        f"DEPTH OF FIELD: {d['dof']}",
        f"FILM STYLE: {d['film']}",
        f"PARTICULAS: {d['particles']}",
        f"SPEED: {d['speed']}",
        f"MOOD: {d['mood']}",
        f"ASPECT RATIO: 16:9",
        f"CONTINUITY: {d['continuity']}",
        f"=======================================",
        "", "",
    ]
    return "\n".join(lines)


def get_ts_base(qnum):
    """Retorna o timestamp base de cada quadro conforme o storyboard."""
    TS = {
        "02":"0:15","03":"0:30","04":"1:00","06":"2:00","07":"2:30","08":"3:00",
        "09":"3:30","10":"4:00","11":"4:30","12":"5:00","13":"5:30",
        "14":"6:00","15":"6:30","16":"7:00","17":"7:30","18":"8:00",
        "19":"8:30","20":"9:00","21":"9:30","22":"10:00","23":"10:30",
    }
    return TS.get(qnum, "0:00")


def main():
    with open(PROMPTS, encoding="utf-8") as f:
        content = f.read()

    # Parsear todos os blocos individuais
    block_pat = re.compile(
        r'(=== QUADRO (\d+) — \[[\d:]+\] — CLIPE (\d+) de (\d+) ===.*?=======================================)',
        re.DOTALL
    )

    blocks = []  # lista de (qnum_int, clip_int, text)
    for m in block_pat.finditer(content):
        blocks.append((int(m.group(2)), int(m.group(3)), m.group(1).strip()))

    # Dedup
    seen = set()
    unique = []
    for q, c, txt in blocks:
        if (q, c) not in seen:
            seen.add((q, c))
            unique.append((q, c, txt))

    # Para quadros "CLIPE 1 de 1" que estao no EXPANSAO, expandir para 3 clips
    expanded = []
    for q, c, txt in unique:
        qnum = f"{q:02d}"
        if qnum in EXPANSAO and c == 1 and "CLIPE 1 de 1" in txt:
            # Clip 1: trocar "CLIPE 1 de 1" → "CLIPE 1 de 3"
            txt1 = txt.replace("CLIPE 1 de 1", "CLIPE 1 de 3")
            expanded.append((q, 1, txt1))
            # Clip 2
            ts = get_ts_base(qnum)
            expanded.append((q, 2, build_block(qnum, 2, 3, ts, EXPANSAO[qnum][0])))
            # Clip 3
            expanded.append((q, 3, build_block(qnum, 3, 3, ts, EXPANSAO[qnum][1])))
        else:
            expanded.append((q, c, txt))

    # Ordenar por quadro, depois por clip
    ORDER = [2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    final = []
    for qn in ORDER:
        clips = sorted([(q, c, t) for q, c, t in expanded if q == qn], key=lambda x: x[1])
        final.extend(clips)

    total_clips = len(final)
    # Header
    header = f"""================================================================================
PROMPTS DE VIDEO — VEO 3
Agencia: Abismo Criativo
Canal: Sinais do Fim — Passagens do Apocalipse
Video: video-001-armagedom
Agente: Phantasma — Diretor de Cinematografia
Data: 2026-04-05 (REFATORADO — Veo 3 em todo o video, 3 clips por quadro)
================================================================================
Total de quadros Veo 3: 21 (Q02-Q23 exceto Q01/Q05/Q24 CapCut)
Total de clipes: {total_clips} (21 quadros x 3 clips)
Duracao por clipe: 8s
Cobertura total Veo 3: {total_clips * 8}s (~{total_clips * 8 / 60:.1f} minutos)
================================================================================

"""
    output = header
    for q, c, txt in final:
        output += txt + "\n\n\n"

    output += f"""================================================================================
SUMARIO TECNICO — PHANTASMA (EXPANDIDO)
================================================================================
Total de clipes gerados: {total_clips}
Quadros cobertos: Q02-Q23 (todos exceto Q01/Q05/Q24 CapCut)
Todos os quadros: 3 clipes (ESTABELECER → APROXIMAR → IMPACTAR)
Duracao por clipe: 8s
Duracao total Veo 3: {total_clips * 8}s (~{total_clips * 8 / 60:.1f} minutos)
Aspect ratio: 16:9 (todos os clipes)
Paleta: #0A0A0A, #8B0000, #C5A355, #E8E0D0
Assinatura visual: Sujeito biblico em CORES vs mundo moderno em P&B
================================================================================
"""

    with open(PROMPTS, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"[OK] prompts_video.txt expandido — {total_clips} clipes ({total_clips // 3} quadros x 3 clips)")

    # Regenerar TXT
    import subprocess, sys
    subprocess.run([sys.executable, os.path.join(BASE, "_tools", "gerar_video_txt.py")],
                   cwd=BASE, check=True)

    # Regenerar PDF + ZIP
    subprocess.run([sys.executable, os.path.join(BASE, "_tools", "gerar_pdfs.py"), "video"],
                   cwd=BASE, check=True)


if __name__ == "__main__":
    main()
