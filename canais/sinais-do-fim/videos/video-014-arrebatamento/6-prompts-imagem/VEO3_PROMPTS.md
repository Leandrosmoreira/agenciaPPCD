# Veo3 — v014 Arrebatamento — Q01-Q04 (Gancho 0-30s)

Modelo: `veo-3.1-fast-generate-preview` | 8s | 1080p | 16:9 | sem audio
Custo estimado: 4 x ~$0.12 = **~$0.48**

Cada prompt é passado a `veo3_oneshot.py --image Q0N.png --out VEO_Q0N.mp4 --dur 8 --prompt "..."`.

## Q01 — Tela preta + brasa solitária

**Prompt (safe, sem violência):**
```
Hyper-realistic cinematic. Complete black frame. At the center-bottom,
a single orange-crimson ember glowing softly, slowly drifting upward
and dissolving into smoke. Subtle drone ambience. No text, no logos,
no watermark. Pure darkness with one tiny luminous particle.
Ultra-slow motion. Cinematic depth of field.
```

## Q02 — Pastor no púlpito

**Prompt:**
```
Hyper-realistic cinematic 3D animation. Medium shot of a charismatic
50-year-old preacher at a dark wooden pulpit, black robe with burgundy
collar, arms raised, face partially in shadow so identity cannot be
seen. Dramatic warm golden top light. Desaturated black-and-white
background of a blurred packed auditorium in silhouettes. Subtle slow
zoom-in toward the pulpit. No dialogue, no text overlay, no watermark.
Kodak Portra 800 film grain aesthetic, chiaroscuro lighting.
```

## Q03 — Chaves de carro, escritura, cédulas, mão assinando

**Prompt:**
```
Hyper-realistic cinematic. Overhead 90-degree shot of a dark wooden
table. On the table: car keys, a folded house deed, a stack of cash
bills. A masculine hand in warm golden light slowly signing a sale
document with a fountain pen. Desaturated black-and-white background
of an empty garage and emptied living room visible at the edges of
frame. Ken Burns style slow zoom-out revealing the whole table.
35mm film grain, Caravaggio chiaroscuro, amber foreground vs gray
background. No text overlay, no watermark.
```

## Q04 — Porta entreaberta à noite

**Prompt:**
```
Hyper-realistic cinematic. Wide frontal shot of a residential house
door left unlocked and slightly ajar at night. Soft wind gently moves
dry leaves just inside the empty entryway. Warm golden interior light
spilling outward. The outside street is desaturated black-and-white,
abandoned, empty. Floating orange embers drift in the air. Slow
push-in camera move toward the door. 24mm wide lens, shallow depth
on door edge. 35mm film grain. No dialogue, no text, no watermark.
```

---

## Runner (copiar e colar no PowerShell ou bash)

```bash
VIDEO_DIR="canais/sinais-do-fim/videos/video-014-arrebatamento"
IMG="$VIDEO_DIR/6-assets"
OUT="$VIDEO_DIR/6-assets/veo3"

python _tools/veo3_oneshot.py --image "$IMG/Q01.png" --out "$OUT/VEO_Q01.mp4" --dur 8 \
  --prompt "Hyper-realistic cinematic. Complete black frame. At the center-bottom, a single orange-crimson ember glowing softly, slowly drifting upward and dissolving into smoke. Subtle drone ambience. No text, no logos, no watermark. Pure darkness with one tiny luminous particle. Ultra-slow motion. Cinematic depth of field."

python _tools/veo3_oneshot.py --image "$IMG/Q02.png" --out "$OUT/VEO_Q02.mp4" --dur 8 \
  --prompt "Hyper-realistic cinematic 3D animation. Medium shot of a charismatic 50-year-old preacher at a dark wooden pulpit, black robe with burgundy collar, arms raised, face partially in shadow so identity cannot be seen. Dramatic warm golden top light. Desaturated black-and-white background of a blurred packed auditorium in silhouettes. Subtle slow zoom-in toward the pulpit. No dialogue, no text overlay, no watermark. Kodak Portra 800 film grain aesthetic, chiaroscuro lighting."

python _tools/veo3_oneshot.py --image "$IMG/Q03.png" --out "$OUT/VEO_Q03.mp4" --dur 8 \
  --prompt "Hyper-realistic cinematic. Overhead 90-degree shot of a dark wooden table. On the table: car keys, a folded house deed, a stack of cash bills. A masculine hand in warm golden light slowly signing a sale document with a fountain pen. Desaturated black-and-white background of an empty garage and emptied living room visible at the edges of frame. Ken Burns style slow zoom-out revealing the whole table. 35mm film grain, Caravaggio chiaroscuro, amber foreground vs gray background. No text overlay, no watermark."

python _tools/veo3_oneshot.py --image "$IMG/Q04.png" --out "$OUT/VEO_Q04.mp4" --dur 8 \
  --prompt "Hyper-realistic cinematic. Wide frontal shot of a residential house door left unlocked and slightly ajar at night. Soft wind gently moves dry leaves just inside the empty entryway. Warm golden interior light spilling outward. The outside street is desaturated black-and-white, abandoned, empty. Floating orange embers drift in the air. Slow push-in camera move toward the door. 24mm wide lens, shallow depth on door edge. 35mm film grain. No dialogue, no text, no watermark."
```

**Custo total:** ~$0.48 (4 clips x $0.12 Veo3 Fast 8s)

**Safety notes:**
- Nenhum dos prompts contém palavras-chave problemáticas (blood, weapon, sword, violence, death).
- Rosto do pregador em Q02 intencionalmente na sombra — evita filtro de identidade.
- Se Q02 for bloqueado: substituir "preacher at pulpit" por "figure silhouette at wooden stage".
