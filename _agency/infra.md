# Infraestrutura — Abismo Criativo

## VPS
- **URL base:** `http://31.97.165.64:3456/`
- **Caminho:** `/opt/agencia/`
- **SSH:** `root@31.97.165.64` (key: `~/.ssh/id_ed25519`)

## Entrega de Output (OBRIGATÓRIO para todos os agentes)
1. Gerar PDF com visual da agência (cores: vermelho #8B0000, dourado #C5A355)
2. Salvar localmente em `canais/{canal}/videos/video-NNN-{slug}/{pasta}/`
3. Upload para VPS via sftp (paramiko)
4. Fornecer link: `http://31.97.165.64:3456/canais/{canal}/videos/video-NNN-{slug}/{pasta}/{arquivo}.pdf`
5. Registrar no `pipeline.log`

## Formato do Pipeline Log
```
[2026-04-04 23:00] PIPELINE INICIADO — sinais-do-fim/video-002-marca-da-besta
[2026-04-04 23:01] ARGOS — Pesquisa concluída → 1-pesquisa/pesquisa.pdf
[2026-04-04 23:02] CHECKPOINT — Aguardando aprovação do tópico
```

## Estrutura de Pastas por Vídeo
```
canais/{canal}/videos/video-NNN-{slug}/
├── 1-pesquisa/pesquisa.pdf
├── 2-titulos/titulos_seo.pdf
├── 3-roteiro/roteiro.pdf + roteiro.txt
├── 4-storyboard/storyboard.pdf
├── 5-prompts/prompts_imagens.txt + suno_prompt.txt
├── 6-assets/imagens/ + audio_suno/
├── 7-edicao/video_cinematografico.mp4
├── 8-publicacao/thumb_prompt.txt + metadata.txt + status_upload.txt
└── 9-metricas/metricas_[data].pdf
```
