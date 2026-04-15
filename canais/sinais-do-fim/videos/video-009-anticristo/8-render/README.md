# video-009-anticristo — Montagem v1
**Canal:** Sinais do Fim — Passagens do Apocalipse
**Agente:** Phantasma
**Data:** 2026-04-13

---

## Dependencias

```
Python 3.10+
moviepy==1.0.3
opencv-python>=4.8.0
numpy>=1.24.0
imageio>=2.31.0
imageio-ffmpeg>=0.4.9
Pillow>=10.0.0
```

Instalar com:

```bash
pip install moviepy==1.0.3 opencv-python numpy imageio imageio-ffmpeg Pillow
```

FFmpeg precisa estar instalado e disponivel no PATH:
- Windows: https://www.gyan.dev/ffmpeg/builds/ (baixar ffmpeg-release-essentials.zip, extrair, adicionar bin/ ao PATH)
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

---

## Estrutura de pastas esperada

```
canais/sinais-do-fim/videos/video-009-anticristo/
├── 5-audio/
│   ├── PARTE1.mp3
│   ├── PARTE2.mp3
│   ├── PARTE3.mp3
│   ├── PARTE4_1.mp3
│   ├── PARTE4_2.mp3
│   ├── PARTE5_1.mp3
│   └── PARTE5.2.mp3
├── 7-imagens/
│   └── *.png   (90+ imagens Midjourney)
└── 8-render/
    ├── montagem_v1.py   (este script)
    └── README.md
```

O script deve ser executado a partir da raiz do repositorio (pasta `agencia/`):

```
agencia/
├── canais/
│   └── sinais-do-fim/
│       └── videos/
│           └── video-009-anticristo/
└── canais/sinais-do-fim/videos/video-009-anticristo/8-render/montagem_v1.py
```

---

## Execucao

A partir da pasta raiz do projeto (`agencia/`):

```bash
cd C:\Users\Leandro\Downloads\agencia
python canais/sinais-do-fim/videos/video-009-anticristo/8-render/montagem_v1.py
```

---

## Output

```
canais/sinais-do-fim/videos/video-009-anticristo/8-render/video-009-anticristo_v1.mp4
```

- Resolucao: 1920x1080
- FPS: 24
- Codec video: H.264 (libx264)
- Codec audio: AAC 192k
- Bitrate video: 8 Mbps
- Duracao estimada: ~12 min 10s

---

## Efeitos aplicados

| Efeito | Descricao |
|--------|-----------|
| Ken Burns | Zoom in/out 1.0->1.15 ou pan lateral em todas as imagens |
| Crossfade | 0.5s de dissolve entre cada imagem |
| Color grading | Brilho -10%, Contraste +15%, leve tint frio |
| Vinheta | Oval gaussiana nas bordas (intensidade 0.55) |

---

## Tempo estimado de render

Em CPU comum (sem GPU):
- 90 quadros x ~8s = ~12 min de video
- Estimativa de render: 45-90 minutos dependendo do hardware

Para acelerar com GPU (opcional, requer CUDA):
```python
# Substituir na chamada write_videofile:
ffmpeg_params=["-hwaccel", "cuda", "-c:v", "h264_nvenc"]
```

---

## Troubleshooting

**Erro: `No module named 'cv2'`**
```bash
pip install opencv-python
```

**Erro: `FileNotFoundError` em imagem especifica**
O script usa fallback automatico — a imagem faltante sera substituida por outra disponivel.

**Erro: `MoviePy error: FFMPEG binary not found`**
Instalar FFmpeg e adicionar ao PATH do sistema.

**Aviso: Video mais longo que audio**
Normal — o ultimo quadro sera exibido em silencio apos o audio terminar. Nao afeta o upload.
