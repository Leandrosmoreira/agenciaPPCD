#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARONTE SYNC GUARD (ADR-008)
============================

Helper compartilhado pelos scripts caronte_upload*.py.

Chama _tools/validar_sync_audio_video.py antes do upload e BLOQUEIA
se qualquer parte estiver dessincronizada (audio > video).

Uso:
    from caronte_sync_guard import validar_sync_adr008
    if not validar_sync_adr008(VIDEO_FILE):
        return False  # aborta upload
"""

import os
import re
import subprocess
import sys


def validar_sync_adr008(video_file_path: str) -> bool:
    """Chama validar_sync_audio_video.py antes do upload.

    Extrai canal/video do path absoluto do VIDEO_FILE e executa o
    validador via subprocess. Retorna False se qualquer parte estiver
    dessincronizada (bloqueia upload).

    Args:
        video_file_path: path absoluto para o video_final.mp4

    Returns:
        True se OK (ou se path nao-padrao), False se BLOQUEADO
    """
    m = re.search(
        r'canais[\\/]([^\\/]+)[\\/]videos[\\/]([^\\/]+)[\\/]',
        video_file_path
    )
    if not m:
        print('[AVISO ADR-008] Nao consegui extrair canal/video do path '
              '— pulando validacao')
        return True  # nao bloqueia se path for nao-padrao

    canal, video = m.group(1), m.group(2)
    validator = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'validar_sync_audio_video.py'
    )

    if not os.path.exists(validator):
        print(f'[AVISO ADR-008] Validador nao encontrado: {validator}')
        return True

    print(f'[CARONTE] Validando sync audio/video (ADR-008) — '
          f'{canal}/{video}...')

    r = subprocess.run(
        [sys.executable, validator, '--canal', canal, '--video', video],
        capture_output=True, text=True
    )
    print(r.stdout)

    if r.returncode != 0:
        if r.stderr:
            print(r.stderr)
        print('[BLOQUEADO ADR-008] Upload cancelado — audio maior que '
              'video em alguma parte.')
        print('                   Rode novamente o prometheus_partes.py '
              'antes de tentar upload:')
        print(f'                   python _tools/prometheus_partes.py '
              f'--canal {canal} --video {video}')
        return False

    return True
