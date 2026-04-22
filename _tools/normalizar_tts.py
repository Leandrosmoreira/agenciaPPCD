#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NORMALIZADOR TTS — Abismo Criativo
==================================

Converte texto PT-BR pronto para leitura natural em TTS (Suno, ElevenLabs, etc):
- Numerais arabicos -> por extenso (1.300 -> "mil e trezentos")
- Datas (15/04/2026 -> "quinze de abril de dois mil e vinte e seis")
- Versiculos biblicos (Ap 6:5-6 -> "Apocalipse capitulo seis versiculos cinco a seis")
- Siglas conhecidas (IA, CBDC, ONU, EUA, ...)
- Simbolos ($, %, R$, US$)
- Algarismos romanos (XIV -> "catorze")
- URLs, hashtags, @ removidos
- Abreviacoes (Dr., Sr., Pe., St.)

PRESERVA tags Suno literais: [Voice:], [Background:], [Style:], [pausa Xs], [trilha...]

USO:
    python _tools/normalizar_tts.py --canal {canal} --video {slug}
    python _tools/normalizar_tts.py --file path/to/parte1.txt
    python _tools/normalizar_tts.py --canal sinais-do-fim --video video-020-1984-daniel --inplace

Output:
    parteN.tts.txt  (lado a lado com original) por padrao
    Se --inplace: sobrescreve o original (mantem backup .bak)
"""

from __future__ import annotations
import argparse
import re
import shutil
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────────────────────────
# SIGLAS (expansao canal-agnostica)
# ──────────────────────────────────────────────────────────
SIGLAS = {
    'IA':   'Inteligência artificial',
    'CBDC': 'moeda digital de banco central',
    'CBDCs': 'moedas digitais de banco central',
    'ONU':  'O N U',
    'EUA':  'Estados Unidos',
    'UE':   'Uniao Europeia',
    'OTAN': 'otan',
    'FBI':  'efe be i',
    'CIA':  'ci ai ei',
    'OMS':  'O M S',
    'BCE':  'banco central europeu',
    'WEF':  'Forum Economico Mundial',
    'PIB':  'P I B',
    'FMI':  'F M I',
    'UFO':  'u f o',
    'UAP':  'u a p',
    'CEO':  'ce o',
    'AI':   'Inteligência artificial',
    'USB':  'u s bi',
    'DNA':  'de ene a',
    'RNA':  'erre ene a',
    'mRNA': 'eme erre ene a',
    'GPS':  'G P S',
    'SUV':  'su v',
    'WFP':  'Programa Mundial de Alimentos',
    'PMA':  'Programa Mundial de Alimentos',
    'GB':   'gigabyte',
    'MB':   'megabyte',
    'KB':   'kilobyte',
    'NSA':  'ene es a',
    'KGB':  'ca ge be',
    'FED':  'fed',
    'ETF':  'e te efe',
    'VPN':  'vi pi ene',
    'HTTP': 'http',
}

ROMANOS = {
    'II': 'segundo', 'III': 'terceiro', 'IV': 'quarto', 'V': 'quinto', 'VI': 'sexto',
    'VII': 'setimo', 'VIII': 'oitavo', 'IX': 'nono', 'X': 'decimo', 'XI': 'decimo primeiro',
    'XII': 'decimo segundo', 'XIII': 'decimo terceiro', 'XIV': 'catorze',
    'XV': 'quinze', 'XVI': 'dezesseis', 'XVII': 'dezessete', 'XVIII': 'dezoito',
    'XIX': 'dezenove', 'XX': 'vinte', 'XXI': 'vinte e um',
}

ABREVIACOES = {
    r'\bDr\.':   'doutor',
    r'\bDra\.':  'doutora',
    r'\bSr\.':   'senhor',
    r'\bSra\.':  'senhora',
    r'\bPe\.':   'padre',
    r'\bSto\.':  'santo',
    r'\bSta\.':  'santa',
    r'\bSao\b':  'Sao',  # mantem
    r'\bProf\.': 'professor',
    r'\betc\.':  'etcetera',
    r'\bvs\.?':  'versus',
    r'\bEx\.:':  'exemplo',
    r'\bd\.C\.': 'depois de Cristo',
    r'\ba\.C\.': 'antes de Cristo',
}

MESES = {
    1: 'janeiro', 2: 'fevereiro', 3: 'marco', 4: 'abril', 5: 'maio', 6: 'junho',
    7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro',
}

LIVROS_BIBLIA = {
    'Gn': 'Genesis', 'Ex': 'Exodo', 'Lv': 'Levitico', 'Nm': 'Numeros', 'Dt': 'Deuteronomio',
    'Js': 'Josue', 'Jz': 'Juizes', 'Rt': 'Rute',
    '1Sm': 'Primeiro Samuel', '2Sm': 'Segundo Samuel',
    '1Rs': 'Primeiro Reis', '2Rs': 'Segundo Reis',
    '1Cr': 'Primeiro Cronicas', '2Cr': 'Segundo Cronicas',
    'Ed': 'Esdras', 'Ne': 'Neemias', 'Et': 'Ester', 'Jo': 'Jo', 'Sl': 'Salmo',
    'Pv': 'Proverbios', 'Ec': 'Eclesiastes', 'Ct': 'Cantares',
    'Is': 'Isaias', 'Jr': 'Jeremias', 'Lm': 'Lamentacoes', 'Ez': 'Ezequiel', 'Dn': 'Daniel',
    'Os': 'Oseias', 'Jl': 'Joel', 'Am': 'Amos', 'Ob': 'Obadias', 'Jn': 'Jonas',
    'Mq': 'Miqueias', 'Na': 'Naum', 'Hc': 'Habacuque', 'Sf': 'Sofonias', 'Ag': 'Ageu',
    'Zc': 'Zacarias', 'Ml': 'Malaquias',
    'Mt': 'Mateus', 'Mc': 'Marcos', 'Lc': 'Lucas', 'Joa': 'Joao', 'At': 'Atos',
    'Rm': 'Romanos', '1Co': 'Primeira Corintios', '2Co': 'Segunda Corintios',
    'Gl': 'Galatas', 'Ef': 'Efesios', 'Fp': 'Filipenses', 'Cl': 'Colossenses',
    '1Ts': 'Primeira Tessalonicenses', '2Ts': 'Segunda Tessalonicenses',
    '1Tm': 'Primeira Timoteo', '2Tm': 'Segunda Timoteo', 'Tt': 'Tito', 'Fm': 'Filemon',
    'Hb': 'Hebreus', 'Tg': 'Tiago',
    '1Pe': 'Primeira Pedro', '2Pe': 'Segunda Pedro',
    '1Jo': 'Primeira Joao', '2Jo': 'Segunda Joao', '3Jo': 'Terceira Joao',
    'Jd': 'Judas', 'Ap': 'Apocalipse',
}

# ──────────────────────────────────────────────────────────
# CONVERSAO DE NUMEROS POR EXTENSO (0-9999)
# ──────────────────────────────────────────────────────────
_UNIDADES = ['', 'um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove',
             'dez', 'onze', 'doze', 'treze', 'catorze', 'quinze', 'dezesseis',
             'dezessete', 'dezoito', 'dezenove']
_DEZENAS = ['', '', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta',
            'setenta', 'oitenta', 'noventa']
_CENTENAS = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos',
             'seiscentos', 'setecentos', 'oitocentos', 'novecentos']


def num_to_words(n: int) -> str:
    """Converte int 0-999999 para texto PT-BR."""
    if n == 0:
        return 'zero'
    if n < 0:
        return 'menos ' + num_to_words(-n)
    if n < 20:
        return _UNIDADES[n]
    if n < 100:
        d, u = divmod(n, 10)
        return _DEZENAS[d] + (' e ' + _UNIDADES[u] if u else '')
    if n == 100:
        return 'cem'
    if n < 1000:
        c, r = divmod(n, 100)
        head = _CENTENAS[c]
        return head + (' e ' + num_to_words(r) if r else '')
    if n < 1_000_000:
        m, r = divmod(n, 1000)
        head = 'mil' if m == 1 else num_to_words(m) + ' mil'
        if r == 0:
            return head
        connector = ' e ' if r < 100 or r % 100 == 0 else ' '
        return head + connector + num_to_words(r)
    if n < 1_000_000_000:
        b, r = divmod(n, 1_000_000)
        head = 'um milhao' if b == 1 else num_to_words(b) + ' milhoes'
        return head + (' ' + num_to_words(r) if r else '')
    b, r = divmod(n, 1_000_000_000)
    head = 'um bilhao' if b == 1 else num_to_words(b) + ' bilhoes'
    return head + (' ' + num_to_words(r) if r else '')


# ──────────────────────────────────────────────────────────
# REGEX HELPERS
# ──────────────────────────────────────────────────────────

# Protege tags Suno ANTES de qualquer substituicao
TAG_PATTERN = re.compile(r'\[[^\[\]]*\]')

def _split_tags(text: str):
    """Separa texto em segmentos [tag] e plain. Retorna lista de (is_tag, segment)."""
    parts = []
    idx = 0
    for m in TAG_PATTERN.finditer(text):
        if m.start() > idx:
            parts.append((False, text[idx:m.start()]))
        parts.append((True, m.group(0)))
        idx = m.end()
    if idx < len(text):
        parts.append((False, text[idx:]))
    return parts


# ──────────────────────────────────────────────────────────
# TRANSFORMACOES
# ──────────────────────────────────────────────────────────

def expand_dates(text: str) -> str:
    """15/04/2026 -> quinze de abril de dois mil e vinte e seis"""
    def _date(m):
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= d <= 31 and 1 <= mo <= 12:
            ys = num_to_words(y)
            return f'{num_to_words(d)} de {MESES[mo]} de {ys}'
        return m.group(0)
    text = re.sub(r'(\d{1,2})/(\d{1,2})/(\d{2,4})', _date, text)

    # DD/MM sem ano
    def _day_month(m):
        d, mo = int(m.group(1)), int(m.group(2))
        if 1 <= d <= 31 and 1 <= mo <= 12:
            return f'{num_to_words(d)} de {MESES[mo]}'
        return m.group(0)
    text = re.sub(r'(\d{1,2})/(\d{1,2})(?!\d)', _day_month, text)
    return text


def expand_bible_refs(text: str) -> str:
    """Ap 6:5-6 -> Apocalipse capitulo seis versiculos cinco a seis
       Daniel 9:27 -> Daniel capitulo nove versiculo vinte e sete
    """
    # Abreviacoes -> nome completo
    def _abbrev(m):
        abbrev, cap, verso = m.group(1), m.group(2), m.group(3)
        livro = LIVROS_BIBLIA.get(abbrev, abbrev)
        cap_w = num_to_words(int(cap))
        if verso is None:
            return f'{livro} capitulo {cap_w}'
        # verso pode ser "5" ou "5-6" ou "5,7"
        if '-' in verso:
            a, b = verso.split('-', 1)
            return f'{livro} capitulo {cap_w} versiculos {num_to_words(int(a))} a {num_to_words(int(b))}'
        if ',' in verso:
            vs = [num_to_words(int(v.strip())) for v in verso.split(',')]
            return f'{livro} capitulo {cap_w} versiculos {" e ".join(vs)}'
        return f'{livro} capitulo {cap_w} versiculo {num_to_words(int(verso))}'

    # ABREVIADO: Ap 6:5 | Dn 9:27 | 1Ts 5:3
    pattern_abbrev = r'\b(' + '|'.join(re.escape(k) for k in LIVROS_BIBLIA.keys()) + r')\s+(\d{1,3}):(\d{1,3}(?:[-,]\d{1,3})?)'
    text = re.sub(pattern_abbrev, _abbrev, text)

    # POR EXTENSO: "Apocalipse 6:5-6" -> expande so o :N:N
    def _full(m):
        livro, cap, verso = m.group(1), m.group(2), m.group(3)
        cap_w = num_to_words(int(cap))
        if '-' in verso:
            a, b = verso.split('-', 1)
            return f'{livro} capitulo {cap_w} versiculos {num_to_words(int(a))} a {num_to_words(int(b))}'
        if ',' in verso:
            vs = [num_to_words(int(v.strip())) for v in verso.split(',')]
            return f'{livro} capitulo {cap_w} versiculos {" e ".join(vs)}'
        return f'{livro} capitulo {cap_w} versiculo {num_to_words(int(verso))}'

    livros_full = r'\b(Apocalipse|Genesis|Exodo|Levitico|Numeros|Deuteronomio|Josue|Juizes|Rute|Ester|Salmo|Salmos|Proverbios|Eclesiastes|Cantares|Isaias|Jeremias|Lamentacoes|Ezequiel|Daniel|Oseias|Joel|Amos|Obadias|Jonas|Miqueias|Naum|Habacuque|Sofonias|Ageu|Zacarias|Malaquias|Mateus|Marcos|Lucas|Joao|Atos|Romanos|Galatas|Efesios|Filipenses|Colossenses|Tito|Filemon|Hebreus|Tiago|Judas)\s+(\d{1,3}):(\d{1,3}(?:[-,]\d{1,3})?)'
    text = re.sub(livros_full, _full, text)
    return text


def expand_symbols(text: str) -> str:
    """% $ R$ US$ + outros."""
    text = re.sub(r'US\$\s*(\d+(?:[.,]\d+)?)',
                  lambda m: num_to_words_decimal(m.group(1)) + ' dolares americanos', text)
    text = re.sub(r'R\$\s*(\d+(?:[.,]\d+)?)',
                  lambda m: num_to_words_decimal(m.group(1)) + ' reais', text)
    text = re.sub(r'(\d+(?:[.,]\d+)?)\s*%',
                  lambda m: num_to_words_decimal(m.group(1)) + ' por cento', text)
    text = text.replace('&', ' e ')
    return text


def num_to_words_decimal(s: str) -> str:
    """1.300 -> 'mil e trezentos'; 1,5 -> 'um virgula cinco'; 18,3 tri -> mantém tri como palavra"""
    s = s.strip()
    # Caso separador decimal vírgula
    if ',' in s and not re.match(r'^[\d.]+$', s.replace(',', '')):
        pass
    # 1.300 (milhar) vs 1,5 (decimal)
    if ',' in s:
        integer, decimal = s.split(',', 1)
        integer_clean = integer.replace('.', '')
        int_w = num_to_words(int(integer_clean)) if integer_clean.isdigit() else s
        dec_w = ' '.join(_UNIDADES[int(c)] if int(c) > 0 else 'zero' for c in decimal)
        return f'{int_w} virgula {dec_w}'
    # só inteiros (com . de milhar possivelmente)
    clean = s.replace('.', '')
    if clean.isdigit():
        return num_to_words(int(clean))
    return s


def expand_numbers(text: str) -> str:
    """Numeros soltos: 2026 -> dois mil e vinte e seis; 1.300 -> mil e trezentos.
       IMPORTANTE: rodar DEPOIS de datas/versiculos/simbolos pra nao comer."""
    def _repl(m):
        n_str = m.group(0)
        clean = n_str.replace('.', '')
        if clean.isdigit():
            return num_to_words(int(clean))
        return n_str
    # Numeros com 1+ digitos, podendo ter ponto de milhar
    return re.sub(r'\b\d{1,3}(?:\.\d{3})*\b|\b\d+\b', _repl, text)


def expand_siglas(text: str) -> str:
    """IA -> inteligencia artificial etc. Só caixa alta."""
    for sigla, expand in sorted(SIGLAS.items(), key=lambda x: -len(x[0])):
        text = re.sub(r'\b' + re.escape(sigla) + r'\b', expand, text)
    return text


def expand_romans(text: str) -> str:
    """Leao XIV -> Leao catorze (apenas quando precedido por palavra)"""
    def _repl(m):
        before, roman = m.group(1), m.group(2)
        return f'{before} {ROMANOS.get(roman, roman)}'
    pattern = r'(\b[A-Za-zÀ-ÿ]+)\s+(' + '|'.join(ROMANOS.keys()) + r')\b'
    return re.sub(pattern, _repl, text)


def expand_abreviacoes(text: str) -> str:
    for pat, expand in ABREVIACOES.items():
        text = re.sub(pat, expand, text, flags=re.IGNORECASE)
    return text


def strip_urls_tags(text: str) -> str:
    """Remove URLs, hashtags, @mencoes"""
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'@\w+', '', text)
    return text


def strip_markdown(text: str) -> str:
    """Remove markdown obvio"""
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'_{2}([^_]+)_{2}', r'\1', text)
    return text


def collapse_spaces(text: str) -> str:
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r' +\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'


# ──────────────────────────────────────────────────────────
# PIPELINE
# ──────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Aplica pipeline completo preservando tags Suno [x]."""
    out_parts = []
    for is_tag, seg in _split_tags(text):
        if is_tag:
            out_parts.append(seg)
            continue
        t = seg
        t = strip_urls_tags(t)
        t = strip_markdown(t)
        t = expand_dates(t)
        t = expand_bible_refs(t)
        t = expand_symbols(t)
        t = expand_abreviacoes(t)
        t = expand_siglas(t)
        t = expand_romans(t)
        t = expand_numbers(t)
        out_parts.append(t)
    return collapse_spaces(''.join(out_parts))


# ──────────────────────────────────────────────────────────
# VALIDACAO (garantir que nada prejudicial sobrou)
# ──────────────────────────────────────────────────────────

VALIDATION_PATTERNS = [
    (r'\b\d{4,}\b',           'Numero grande nao convertido'),
    (r'\bR\$|\bUS\$|%',       'Simbolo monetario/% nao expandido'),
    (r'https?://',            'URL nao removida'),
    (r'#\w+',                 'Hashtag nao removida'),
    (r'\b(IA|CBDC|ONU|EUA)\b','Sigla nao expandida'),
]

def validate(text: str) -> list[str]:
    """Retorna lista de avisos (nao bloqueia execucao)."""
    warns = []
    # Remove tags antes de validar (tags podem conter %, etc)
    plain = TAG_PATTERN.sub('', text)
    for pat, msg in VALIDATION_PATTERNS:
        matches = re.findall(pat, plain)
        if matches:
            warns.append(f'{msg}: {list(set(matches))[:5]}')
    return warns


# ──────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────

def process_file(fpath: Path, inplace: bool = False) -> dict:
    original = fpath.read_text(encoding='utf-8')
    normalized = normalize(original)
    warns = validate(normalized)

    if inplace:
        backup = fpath.with_suffix(fpath.suffix + '.bak')
        if not backup.exists():
            shutil.copy2(fpath, backup)
        fpath.write_text(normalized, encoding='utf-8')
        out = fpath
    else:
        out = fpath.with_suffix('.tts.txt')
        out.write_text(normalized, encoding='utf-8')

    return {
        'input':  fpath,
        'output': out,
        'chars_before': len(original),
        'chars_after':  len(normalized),
        'warnings': warns,
    }


def find_parts(canal: str, video: str) -> list[Path]:
    base = ROOT / 'canais' / canal / 'videos' / video / '5-prompts'
    if not base.exists():
        print(f'[ERRO] Pasta nao existe: {base}', file=sys.stderr)
        sys.exit(1)
    files = sorted(base.glob('*parte*.txt'))
    files = [f for f in files if '.tts.txt' not in f.name and not f.name.endswith('.bak')]
    return files


def main():
    ap = argparse.ArgumentParser(description='Normaliza texto para TTS (Suno/ElevenLabs).')
    ap.add_argument('--canal', help='Slug do canal (ex: sinais-do-fim)')
    ap.add_argument('--video', help='Slug do video (ex: video-020-1984-daniel)')
    ap.add_argument('--file',  help='Arquivo individual (alternativa a --canal/--video)')
    ap.add_argument('--inplace', action='store_true', help='Sobrescreve original (com backup .bak)')
    args = ap.parse_args()

    files = []
    if args.file:
        p = Path(args.file)
        if not p.exists():
            print(f'[ERRO] Arquivo nao existe: {p}', file=sys.stderr); sys.exit(1)
        files = [p]
    elif args.canal and args.video:
        files = find_parts(args.canal, args.video)
        if not files:
            print('[ERRO] Nenhum arquivo parteN.txt encontrado', file=sys.stderr); sys.exit(1)
    else:
        ap.print_help(); sys.exit(1)

    print('=' * 58)
    print(f'NORMALIZADOR TTS | {len(files)} arquivo(s) | inplace={args.inplace}')
    print('=' * 58)

    total_warns = 0
    for f in files:
        r = process_file(f, inplace=args.inplace)
        print(f'[OK] {r["input"].name} -> {r["output"].name}')
        print(f'     {r["chars_before"]} chars -> {r["chars_after"]} chars')
        if r['warnings']:
            for w in r['warnings']:
                print(f'     [AVISO] {w}')
                total_warns += 1

    print('=' * 58)
    print(f'[CONCLUIDO] {len(files)} arquivo(s) normalizado(s) | {total_warns} aviso(s)')
    print('=' * 58)
    return 0 if total_warns == 0 else 2  # 2 = OK mas com avisos


if __name__ == '__main__':
    sys.exit(main())
