#!/usr/bin/env python3
"""Gera TXT de prompts de video (Phantasma/Veo3) — tudo em ingles, 1 paragrafo por clipe."""
import os, re, paramiko

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS_DIR = os.path.join(BASE, "canais", "sinais-do-fim", "videos",
                           "video-001-armagedom", "5-prompts")

# ── Traducoes de labels ──────────────────────────────────────────────────────
LABEL_MAP = {
    "ENQUADRAMENTO": "FRAMING",
    "ILUMINACAO":    "LIGHTING",
    "PARTICULAS":    "PARTICLES",
    # Ja em ingles — mantidos
    "CAMERA": "CAMERA", "DEPTH OF FIELD": "DEPTH OF FIELD",
    "FILM STYLE": "FILM STYLE", "SPEED": "SPEED", "MOOD": "MOOD",
    "ASPECT RATIO": "ASPECT RATIO", "CONTINUITY": "CONTINUITY",
}

# ── Traducoes de valores (frases completas primeiro, depois palavras) ─────────
PHRASE_MAP = [
    # --- Q09 ---
    ("globo completo, espaco ao redor visivel", "full globe, surrounding space visible"),
    ("globo rotaciona sozinho, camera fixa contemplando", "globe rotates on its own, camera fixed and contemplating"),
    ("Rim lighting solar dourado (#C5A355) vindo da direita, sombra profunda na esquerda",
     "Golden solar rim lighting (#C5A355) from the right, deep shadow on the left"),
    ("globo e estrelas ao fundo em foco", "globe and background stars in focus"),
    ("35mm grain pesado, anamorphic flare horizontal, desaturated cool + amber split grading",
     "Heavy 35mm grain, horizontal anamorphic flare, desaturated cool + amber split grading"),
    ("Poeira espacial tenue, particulas de nebulosa ao fundo",
     "Faint space dust, nebula particles in the background"),
    ("Revelacao cosmica — o mundo em perspectiva", "Cosmic revelation — the world in perspective"),
    ("Inicio do arco Q09 — estabelece escala cosmica do globo antes das linhas surgirem",
     "Start of Q09 arc — establishes cosmic scale of the globe before the lines appear"),
    ("Wide → Medium — dolly in aproxima o Oriente Medio ao centro",
     "Wide → Medium — dolly in brings the Middle East to center"),
    ("Dolly in lento e deliberado, avanca 40% em direcao ao Oriente Medio",
     "Slow and deliberate dolly in, advances 40% toward the Middle East"),
    ("Chiaroscuro — Israel iluminado dourado, resto do globo em sombra profunda",
     "Chiaroscuro — Israel lit in gold, rest of globe in deep shadow"),
    ("globo em foco, espaco levemente suavizado ao fundo",
     "globe in focus, space softly blurred in the background"),
    ("35mm grain, anamorphic flares nas linhas vermelhas, teal + crimson grading",
     "35mm grain, anamorphic flares on the red lines, teal + crimson grading"),
    ("Brasas vermelhas flutuando ao longo das linhas, poeira espacial",
     "Red embers floating along the lines, space dust"),
    ("Convergencia profetica — todas as conexoes levam a um ponto",
     "Prophetic convergence — all connections lead to one point"),
    ("Clipe anterior estabeleceu o globo distante — agora a camera avanca revelando a rede de linhas que conectam o mundo a Israel",
     "Previous clip established the distant globe — now the camera advances revealing the network of lines connecting the world to Israel"),
    ("Close geografico — Israel no epicentro absoluto do frame, regra dos tercos aplicada",
     "Geographic close-up — Israel at the absolute epicenter of the frame, rule of thirds applied"),
    ("Orbit lento counterclockwise ao redor de Israel, revelando convergencia em 3D",
     "Slow counterclockwise orbit around Israel, revealing convergence in 3D"),
    ("Volumetric rays dourados irradiando de Israel, chiaroscuro extremo ao redor",
     "Golden volumetric rays radiating from Israel, extreme chiaroscuro around"),
    ("Israel nitido, bordas do globo desfocadas", "Israel sharp, globe edges softly blurred"),
    ("35mm grain, anamorphic flares dos raios dourados, vermelho sangue + dourado envelhecido",
     "35mm grain, anamorphic flares from golden rays, blood red + aged gold"),
    ("Brasas e cinzas irradiando do epicentro, fumos vermelhos",
     "Embers and ash radiating from the epicenter, red smoke wisps"),
    ("0.5x slow motion nas pulsacoes de luz", "0.5x slow motion on the light pulses"),
    ("Inevitabilidade profetica — o mundo converge, nao ha escape do epicentro",
     "Prophetic inevitability — the world converges, there is no escape from the epicenter"),
    ("Clipe anterior mostrou as linhas chegando — este fecha no epicentro vivo onde elas convergem, criando o climax visual do Q09",
     "Previous clip showed the lines arriving — this closes on the living epicenter where they converge, creating Q09's visual climax"),
    # --- Q13 ---
    ("Medium close-up — camera CCTV ocupa dois tercos do frame, parede de concreto ao fundo",
     "Medium close-up — CCTV camera occupies two-thirds of the frame, concrete wall in background"),
    ("Handheld com tremor nervoso sutil — urgencia de documentario",
     "Handheld with subtle nervous tremor — documentary urgency"),
    ("Practical red LED da camera de vigilancia, luz artificial fria e dura, sem luz natural",
     "Practical red LED from the surveillance camera, cold and harsh artificial light, no natural light"),
    ("lente da CCTV nitida, parede de concreto levemente desfocada",
     "CCTV lens sharp, concrete wall slightly blurred"),
    ("16mm grain documental, sem lens flare, desaturado com vermelho elevado",
     "Documentary 16mm grain, no lens flare, desaturated with boosted red channel"),
    ("Fumaca fina deslizando pela parede, poeira no ar",
     "Thin smoke sliding along the wall, dust in the air"),
    ("Opressao e vigilancia — o olho mecanico que nao pisca",
     "Oppression and surveillance — the mechanical eye that never blinks"),
    ("Inicio do arco Q13 — introduz o elemento primario de vigilancia antes de revelar a escala do sistema",
     "Start of Q13 arc — introduces the primary surveillance element before revealing the scale of the system"),
    ("Medium — tracking lateral revela cada elemento de controle em sequencia",
     "Medium — lateral tracking reveals each control element in sequence"),
    ("Tracking shot lateral da esquerda para direita, velocidade media e deliberada",
     "Lateral tracking shot from left to right, medium deliberate speed"),
    ("Neon artificial — azul-branco das telas, vermelho dos indicadores, sem luz quente",
     "Artificial neon — blue-white from screens, red from indicators, no warm light"),
    ("todos os elementos do corredor em foco simultaneamente",
     "all corridor elements simultaneously in focus"),
    ("35mm grain, aberracao cromatica nas bordas das telas, teal + neon red grading",
     "35mm grain, chromatic aberration on screen edges, teal + neon red grading"),
    ("Fumaca entre os servidores, poeira nos raios de luz artificial",
     "Smoke between servers, dust in artificial light beams"),
    ("Inevitabilidade — o sistema ja existe, ja opera, ja rastreia",
     "Inevitability — the system already exists, already operates, already tracks"),
    ("O clipe anterior mostrou o olho isolado da camera CCTV — este revela a infraestrutura por tras dele: reconhecimento facial, rastreamento financeiro, a maquina completa",
     "The previous clip showed the isolated CCTV camera eye — this reveals the infrastructure behind it: facial recognition, financial tracking, the complete machine"),
    ("Medium → Wide — crane up revela satelite como olho cosmico sobre a Terra",
     "Medium → Wide — crane up reveals satellite as cosmic eye over Earth"),
    ("Crane up lento — camera sobe se afastando do satelite, Terra aparece abaixo",
     "Slow crane up — camera rises pulling away from satellite, Earth appears below"),
    ("Luz solar fria azulada refletida no metal do satelite, Terra iluminada por baixo com clusters vermelhos",
     "Cold blue solar light reflected on satellite metal, Earth lit from below with red clusters"),
    ("satelite e Terra em foco, espaco ao fundo profundo e escuro",
     "satellite and Earth in focus, deep dark space in background"),
    ("35mm grain, anamorphic flares no painel solar do satelite, cold steel blue + crimson grading",
     "35mm grain, anamorphic flares on the satellite solar panel, cold steel blue + crimson grading"),
    ("Cinzas e poeira derivando no vacuo espacial", "Ash and dust drifting in the space vacuum"),
    ("Onisciencia mecanica — nada escapa, o sistema ve tudo de cima",
     "Mechanical omniscience — nothing escapes, the system sees everything from above"),
    ("Clipes anteriores mostraram os componentes do sistema no nivel do chao — este se eleva ao espaco revelando que o sistema tem olhos ate no cosmos, completando o arco de vigilancia total do Q13",
     "Previous clips showed system components at ground level — this ascends to space revealing the system has eyes even in the cosmos, completing Q13's total surveillance arc"),
    # --- Q17 ---
    ("Extreme wide — vulcao visivel do cone a base, ceu de cinzas acima, paisagem P&B embaixo",
     "Extreme wide — volcano visible from cone to base, ash sky above, B&W landscape below"),
    ("Static + parallax — camadas de cena em movimento, camera absolutamente fixa (contemplacao)",
     "Static + parallax — scene layers in motion, camera absolutely fixed (contemplation)"),
    ("Lava como luz pratica (vermelha dourada), ceu de cinzas como difusor total, sem sol direto",
     "Lava as practical light (red-gold), ash sky as total diffuser, no direct sunlight"),
    ("tudo em foco, do primeiro plano ao horizonte", "everything in focus, from foreground to horizon"),
    ("35mm grain pesado, bleach bypass (contraste extremo), crimson + ash grey grading",
     "Heavy 35mm grain, bleach bypass (extreme contrast), crimson + ash grey grading"),
    ("Chuva densa de cinzas negras, fumaca pesada subindo, brasas flutuando na corrente de ar quente",
     "Dense shower of black ash, heavy smoke rising, embers floating in the hot air current"),
    ("Juizo irrevogavel — a terra consume a si mesma", "Irrevocable judgement — the earth consumes itself"),
    ("Inicio do arco Q17 — estabelece a escala total da catastrofe antes de aproximar",
     "Start of Q17 arc — establishes the full scale of the catastrophe before closing in"),
    ("Low angle close — lava avancando em direcao a camera, shot a nivel do chao",
     "Low angle close — lava advancing toward the camera, shot at ground level"),
    ("Handheld tremulo no nivel do solo, leve tilt up para capturar o avancar da lava",
     "Trembling handheld at ground level, slight tilt up to capture the advancing lava"),
    ("Chiaroscuro de baixo para cima — lava como unica fonte de luz, iluminacao infernal ascendente",
     "Bottom-up chiaroscuro — lava as the only light source, ascending infernal lighting"),
    ("borda da lava nitida em primeiro plano, corrente ao fundo suavemente desfocada",
     "lava edge sharp in the foreground, flow softly blurred in the background"),
    ("35mm grain, anamorphic flares da lava, cor isolada apenas na lava (resto desaturado ao preto)",
     "35mm grain, anamorphic flares from the lava, color isolated only on the lava (rest desaturated to black)"),
    ("Explosao densa de fagulhas e brasas, fumaca de enxofre subindo, cinzas na corrente de ar quente",
     "Dense burst of sparks and embers, sulfur smoke rising, ash in the hot air current"),
    ("0.3x ultra slow motion — impacto maximo", "0.3x ultra slow motion — maximum impact"),
    ("0.3x ultra slow motion — cada segundo de impacto maximizado", "0.3x ultra slow motion — every second of impact maximized"),
    ("Terror visceral — a destruicao chegando, imparavel, ao nivel dos olhos",
     "Visceral terror — destruction arriving, unstoppable, at eye level"),
    ("O clipe anterior estabeleceu o vulcao em escala epica — este desce ao nivel da lava, mostrando o horror no detalhe fisico e textural de sua destruicao avancando",
     "The previous clip established the volcano at epic scale — this descends to lava level, showing the horror in the physical and textural detail of its advancing destruction"),
    ("High angle → Medium — crane down desce ao nivel dos telhados enquanto tsunami domina o fundo",
     "High angle → Medium — crane down descends to rooftop level as tsunami dominates the background"),
    ("Crane down lento e dramatico — descendo de posicao elevada em direcao a cidade",
     "Slow and dramatic crane down — descending from elevated position toward the city"),
    ("Luz natural difusa e fria (ceu de cinzas), sem sombras, tudo em claridade clinica P&B",
     "Cold diffused natural light (ash sky), no shadows, everything in clinical B&W clarity"),
    ("cidade em primeiro plano e tsunami ao fundo ambos em foco",
     "city in foreground and tsunami in background both in focus"),
    ("35mm grain, sem flares, bleach bypass total, preto e branco completo exceto espuma branca da onda",
     "35mm grain, no flares, full bleach bypass, complete black and white except white wave foam"),
    ("Bruma maritima densa, espuma e spray do oceano, poeira dos edificios comecando a ruir",
     "Dense sea mist, ocean foam and spray, dust from buildings beginning to crumble"),
    ("Fim absoluto — a ira da natureza consumindo a cidade em silencio cinematografico",
     "Absolute end — the wrath of nature consuming the city in cinematic silence"),
    ("Clipe anterior mostrou a lava avancando no nivel do chao — este eleva a camera ao macro, mostrando outra forca elemental (agua) consumindo o mundo P&B da civilizacao moderna, completando o arco de destruicao do Q17",
     "Previous clip showed lava advancing at ground level — this elevates the camera to macro scale, showing another elemental force (water) consuming the B&W world of modern civilization, completing Q17's destruction arc"),
    # --- Q23 ---
    ("Medium close-up — rosto da testa ao pescoco, ceu parcialmente visivel acima",
     "Medium close-up — face from forehead to neck, sky partially visible above"),
    ("Slow push in extremamente suave — avancando em direcao ao rosto ao longo dos 10s",
     "Extremely gentle slow push in — advancing toward the face over 10 seconds"),
    ("Rim light dourado sagrado vindo de cima (luz divina), sombra profunda no queixo e pescoce",
     "Sacred golden rim light from above (divine light), deep shadow on chin and neck"),
    ("rosto em foco, ceu ao fundo totalmente desfocado em ouro suave",
     "face in focus, sky in background fully blurred in soft gold"),
    ("35mm grain suave, anamorphic flares dourados, warm gold + antique white grading",
     "Soft 35mm grain, golden anamorphic flares, warm gold + antique white grading"),
    ("Orbs de luz dourada descendo suavemente, fumaca tenue ao fundo",
     "Golden light orbs descending gently, faint smoke in the background"),
    ("Reverencia emocional — o momento em que a pergunta profecia se torna pessoal",
     "Emotional reverence — the moment the prophetic question becomes personal"),
    ("Inicio do arco Q23 — a escala epica dos quadros anteriores colapsa para o intimo: um rosto unico, uma pergunta pessoal",
     "Start of Q23 arc — the epic scale of previous frames collapses to the intimate: a single face, a personal question"),
    ("Close — metade inferior do rosto, olho e lagrima como foco absoluto, regra dos tercos com lagrima no ponto de ouro",
     "Close-up — lower half of the face, eye and tear as absolute focus, rule of thirds with tear on the golden point"),
    ("Static com micro-tremor emocional — quase imperceptivel, camera segura pelo peso do momento",
     "Static with micro emotional tremor — almost imperceptible, camera held by the weight of the moment"),
    ("Rim light dourado esculpindo o osso da bochecha, sombra profunda no queixo, sem luz ambiente",
     "Golden rim light sculpting the cheekbone, deep shadow on chin, no ambient light"),
    ("lagrima em foco perfeito, tudo ao fundo em bokeh dourado",
     "tear in perfect focus, everything in background in golden bokeh"),
    ("35mm grain texturado na pele, anamorphic bokeh horizontal ao fundo, amber + gold grading",
     "Textured 35mm grain on skin, horizontal anamorphic bokeh in background, amber + gold grading"),
    ("Poeira flutuando no raio de luz dourado acima do rosto",
     "Dust floating in the golden light beam above the face"),
    ("0.3x ultra slow motion na trajetoria da lagrima", "0.3x ultra slow motion on the tear's trajectory"),
    ("Intimidade crua — a emocao que atravessa o espectador pela identificacao humana universal",
     "Raw intimacy — the emotion that pierces the viewer through universal human identification"),
    ("O clipe anterior mostrou o rosto completo em reverencia — este fecha no detalhe fisico e humano da lagrima, a prova material da emocao, o momento em que a profecia toca a carne",
     "The previous clip showed the full face in reverence — this closes on the physical and human detail of the tear, the material proof of emotion, the moment prophecy touches flesh"),
    ("Extreme close-up macro — o olho ocupa 80% do frame, o ceu dourado refletido dentro da pupila",
     "Extreme macro close-up — the eye occupies 80% of the frame, the golden sky reflected inside the pupil"),
    ("Macro orbit microscopico — a camera orbita suavemente poucos milimetros ao redor do olho",
     "Microscopic macro orbit — the camera orbits gently a few millimeters around the eye"),
    ("Rim light dourado perfeito no cilio superior, pupila iluminada pelo reflexo do ceu dentro dela",
     "Perfect golden rim light on the upper eyelid, pupil illuminated by the sky reflection within it"),
    ("pupila e reflexo em foco absoluto, iris levemente suavizada nas bordas",
     "pupil and reflection in absolute focus, iris slightly softened at the edges"),
    ("35mm macro grain, sem flares (escala intima demais), pure amber + gold + darkness grading",
     "35mm macro grain, no flares (too intimate a scale), pure amber + gold + darkness grading"),
    ("Lagrima final deslizando pelo iris distorcendo e clarificando o reflexo do ceu",
     "Final tear sliding across the iris distorting and clarifying the sky reflection"),
    ("Transcendencia — a eternidade refletida nos olhos de um ser humano comum, a pergunta respondida no proprio olhar",
     "Transcendence — eternity reflected in the eyes of a common human being, the question answered in the very gaze"),
    ("O arco Q23 vai do rosto (distancia emocional) a lagrima (contato humano) ao reflexo do ceu nos olhos (o ceu e o espectador se encontram dentro de uma unica pupila). Este e o climax emocional de todo o video-001-armagedom.",
     "The Q23 arc goes from the face (emotional distance) to the tear (human contact) to the sky's reflection in the eyes (heaven and viewer meet inside a single pupil). This is the emotional climax of the entire video-001-armagedom."),
]

# Substituicoes de palavras/frases genericas (aplicadas ao final)
WORD_MAP = [
    ("espaco ao redor", "surrounding space"),
    ("camera fixa", "fixed camera"),
    ("sombra profunda", "deep shadow"),
    ("ao fundo", "in the background"),
    ("em foco", "in focus"),
    ("slow motion", "slow motion"),
    ("grain pesado", "heavy grain"),
    ("sem luz natural", "no natural light"),
    ("nivel do chao", "ground level"),
    ("em direcao", "toward"),
    ("a camera", "the camera"),
    ("o frame", "the frame"),
    ("ao redor", "around"),
]


def translate_value(val: str) -> str:
    for pt, en in PHRASE_MAP:
        val = val.replace(pt, en)
    for pt, en in WORD_MAP:
        val = val.replace(pt, en)
    return val


def parse_clips(content: str):
    """Retorna lista de dicts com os dados de cada clipe."""
    clip_pattern = re.compile(
        r'=== QUADRO (\d+) — \[(\d+:\d+)\] — CLIPE (\d+) de (\d+) ===\n'
        r'TIMESTAMP: (.+?)\n'
        r'DURACAO: (.+?)\n'
        r'PROMPT:\n(.*?)\n'
        r'((?:ENQUADRAMENTO|CAMERA|ILUMINACAO|DEPTH).*?)'
        r'=======================================',
        re.DOTALL
    )
    clips = []
    for m in clip_pattern.finditer(content):
        quadro, ts_start, clip_num, total_clips, timestamp, duracao, prompt_text, fields_block = m.groups()
        prompt_text = " ".join(prompt_text.strip().split())

        # Parsear campos adicionais
        field_lines = [l.strip() for l in fields_block.strip().split('\n') if l.strip()]
        fields = {}
        for line in field_lines:
            for label in LABEL_MAP:
                if line.startswith(label + ":"):
                    fields[label] = line[len(label)+1:].strip()
                    break

        clips.append({
            "quadro": quadro,
            "clip_num": clip_num,
            "total": total_clips,
            "timestamp": timestamp,
            "prompt": prompt_text,
            "fields": fields,
        })
    return clips


def build_paragraph(clip: dict) -> str:
    """Monta um paragrafo unico em ingles com prompt + todos os campos."""
    parts = [clip["prompt"]]
    field_order = ["ENQUADRAMENTO", "CAMERA", "ILUMINACAO", "DEPTH OF FIELD",
                   "FILM STYLE", "PARTICULAS", "SPEED", "MOOD", "ASPECT RATIO", "CONTINUITY"]
    for field in field_order:
        if field in clip["fields"]:
            label_en = LABEL_MAP.get(field, field)
            value_en = translate_value(clip["fields"][field])
            parts.append(f"{label_en}: {value_en}")
    return " ".join(parts)


def main():
    src = os.path.join(PROMPTS_DIR, "prompts_video.txt")
    dst = os.path.join(PROMPTS_DIR, "video-001-armagedom-video.txt")

    with open(src, encoding="utf-8") as f:
        content = f.read()

    clips = parse_clips(content)
    paragraphs = []
    for clip in clips:
        para = build_paragraph(clip)
        paragraphs.append(para)

    output = "\n\n".join(paragraphs)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"[OK] {len(clips)} clipes salvos em {dst}")

    # Upload VPS
    remote = f"/opt/agencia/canais/sinais-do-fim/videos/video-001-armagedom/5-prompts/video-001-armagedom-video.txt"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("31.97.165.64", username="root",
                key_filename=os.path.expanduser("~/.ssh/id_ed25519"))
    sftp = ssh.open_sftp()
    sftp.put(dst, remote)
    sftp.close(); ssh.close()
    url = f"http://31.97.165.64:3456/canais/sinais-do-fim/videos/video-001-armagedom/5-prompts/video-001-armagedom-video.txt"
    print(f"[LINK] {url}")
    return url


if __name__ == "__main__":
    main()
