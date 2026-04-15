#!/usr/bin/env python3
"""
Renomeia imagens do Midjourney para Q01.png, Q02.png...
Ordena por data de modificação (ordem em que foram geradas).

Uso: python renomear_imagens_mj.py --pasta 6-assets/imagens/
  ou: python renomear_imagens_mj.py --canal sinais-do-fim --video video-007-falsa-paz
"""

import argparse
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def renomear(pasta: Path, dry_run: bool = False):
    # Coletar imagens
    images = [f for f in pasta.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS]

    if not images:
        print(f"Nenhuma imagem encontrada em {pasta}")
        return

    # Ordenar por data de modificação (ordem de geração no MJ)
    images.sort(key=lambda f: f.stat().st_mtime)

    print(f"Encontradas {len(images)} imagens em {pasta}")
    print(f"{'[DRY RUN] ' if dry_run else ''}Renomeando...\n")

    for i, img in enumerate(images, 1):
        novo_nome = f"Q{i:02d}{img.suffix.lower()}"
        novo_path = pasta / novo_nome

        if dry_run:
            print(f"  {img.name}  ->  {novo_nome}")
        else:
            # Evitar sobrescrever se já existe
            if novo_path.exists() and novo_path != img:
                # Mover para temp primeiro
                temp = pasta / f"_temp_{novo_nome}"
                shutil.move(str(img), str(temp))
                shutil.move(str(temp), str(novo_path))
            else:
                shutil.move(str(img), str(novo_path))
            print(f"  OK {img.name}  ->  {novo_nome}")

    print(f"\n{'[DRY RUN] Nada alterado.' if dry_run else f'Pronto! {len(images)} imagens renomeadas.'}")


def main():
    parser = argparse.ArgumentParser(description="Renomear imagens MJ para Q01, Q02...")
    parser.add_argument("--pasta", help="Pasta com as imagens")
    parser.add_argument("--canal", help="Slug do canal")
    parser.add_argument("--video", help="Slug do vídeo")
    parser.add_argument("--dry-run", action="store_true", help="Simular sem renomear")
    args = parser.parse_args()

    if args.pasta:
        pasta = Path(args.pasta)
    elif args.canal and args.video:
        pasta = BASE_DIR / "canais" / args.canal / "videos" / args.video / "6-assets" / "imagens"
    else:
        print("Use --pasta OU --canal + --video")
        return

    if not pasta.exists():
        print(f"Pasta não encontrada: {pasta}")
        return

    renomear(pasta, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
