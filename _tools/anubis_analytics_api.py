#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANUBIS — Agente de Analytics via YouTube API
Extrai dados completos de todos os vídeos do canal
"""

import os
import json
import pickle
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ──────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────

CREDS_FILE = os.path.expanduser('~/.claude/youtube_oauth_creds.json')
TOKEN_FILE = os.path.expanduser('~/.claude/youtube_analytics_token.pickle')
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly',
          'https://www.googleapis.com/auth/yt-analytics.readonly']

OUTPUT_DIR = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\videos'
LOG_FILE = r'C:\Users\Leandro\Downloads\agencia\canais\sinais-do-fim\_config\pipeline.log'

# ──────────────────────────────────────────────────────────
# AUTHENTICATE
# ──────────────────────────────────────────────────────────

def authenticate():
    """Autentica com YouTube API"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_FILE):
                print(f'[ERRO] Credenciais nao encontradas em {CREDS_FILE}')
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds

# ──────────────────────────────────────────────────────────
# GET CHANNEL ID
# ──────────────────────────────────────────────────────────

def get_channel_id(youtube):
    """Obtem ID do canal"""
    request = youtube.channels().list(part='id', mine=True)
    response = request.execute()
    if response['items']:
        return response['items'][0]['id']
    return None

# ──────────────────────────────────────────────────────────
# GET ALL VIDEOS
# ──────────────────────────────────────────────────────────

def get_all_videos(youtube, channel_id):
    """Lista todos os vídeos do canal"""
    videos = []
    request = youtube.search().list(
        part='id,snippet',
        channelId=channel_id,
        type='video',
        maxResults=50,
        order='date'
    )

    while request:
        response = request.execute()
        for item in response.get('items', []):
            video = {
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'published': item['snippet']['publishedAt']
            }
            videos.append(video)

        if 'nextPageToken' in response:
            request = youtube.search().list_next(request, response)
        else:
            break

    return videos

# ──────────────────────────────────────────────────────────
# GET VIDEO ANALYTICS
# ──────────────────────────────────────────────────────────

def query_analytics(youtube_analytics, channel_id, video_id, dimensions, metrics, days=30):
    """Query genérica para Analytics API"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    try:
        return youtube_analytics.reports().query(
            ids=f'channel=={channel_id}',
            startDate=str(start_date),
            endDate=str(end_date),
            metrics=','.join(metrics),
            filters=f'video=={video_id}',
            dimensions=dimensions,
            maxResults=25
        ).execute()
    except Exception as e:
        print(f'  [ERRO] {dimensions}: {e}')
        return None


def get_video_analytics(youtube_analytics, channel_id, video_id, days=30):
    """Extrai todos os analytics disponíveis de um vídeo"""

    # Série histórica por dia
    historico = query_analytics(
        youtube_analytics, channel_id, video_id,
        dimensions='day',
        metrics=['views', 'estimatedMinutesWatched', 'averageViewDuration',
                 'averageViewPercentage', 'subscribersGained', 'likes', 'comments']
    )

    # Fontes de tráfego
    trafego = query_analytics(
        youtube_analytics, channel_id, video_id,
        dimensions='insightTrafficSourceType',
        metrics=['views', 'estimatedMinutesWatched']
    )

    # Países
    paises = query_analytics(
        youtube_analytics, channel_id, video_id,
        dimensions='country',
        metrics=['views', 'estimatedMinutesWatched', 'subscribersGained']
    )

    # Dispositivos
    devices = query_analytics(
        youtube_analytics, channel_id, video_id,
        dimensions='deviceType',
        metrics=['views', 'estimatedMinutesWatched']
    )

    return {
        'historico_diario': historico,
        'trafego': trafego,
        'paises': paises,
        'dispositivos': devices
    }

# ──────────────────────────────────────────────────────────
# GET REALTIME STATS (Data API v3 — sem lag)
# ──────────────────────────────────────────────────────────

def get_realtime_stats(youtube, video_ids):
    """
    Busca estatísticas em tempo real via Data API v3.
    Retorna views, likes, comments, favorites atualizados agora.
    """
    ids_str = ','.join(video_ids)
    try:
        response = youtube.videos().list(
            part='statistics,snippet',
            id=ids_str
        ).execute()

        stats = {}
        for item in response.get('items', []):
            vid = item['id']
            s = item.get('statistics', {})
            stats[vid] = {
                'viewCount':     int(s.get('viewCount', 0)),
                'likeCount':     int(s.get('likeCount', 0)),
                'commentCount':  int(s.get('commentCount', 0)),
                'favoriteCount': int(s.get('favoriteCount', 0)),
            }
        return stats
    except Exception as e:
        print(f'[ERRO] Falha ao obter stats em tempo real: {e}')
        return {}

# ──────────────────────────────────────────────────────────
# GENERATE REPORT
# ──────────────────────────────────────────────────────────

def generate_report(youtube, youtube_analytics, channel_id, videos):
    """Gera relatório completo: stats em tempo real + histórico Analytics"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = {
        'data_coleta': now,
        'canal_id': channel_id,
        'total_videos': len(videos),
        'videos': []
    }

    # Stats em tempo real (Data API v3)
    print('[ANUBIS] Coletando stats em tempo real (Data API v3)...')
    video_ids = [v['id'] for v in videos]
    realtime = get_realtime_stats(youtube, video_ids)

    print(f'[ANUBIS] Coletando histórico de analytics de {len(videos)} vídeos...')

    for i, video in enumerate(videos, 1):
        print(f'[{i}/{len(videos)}] {video["title"][:50]}...')

        analytics = get_video_analytics(youtube_analytics, channel_id, video['id'])
        rt = realtime.get(video['id'], {})

        video_report = {
            'id': video['id'],
            'title': video['title'],
            'published': video['published'],
            'realtime_stats': rt,          # ← dados de AGORA sem lag
            'analytics': analytics
        }
        report['videos'].append(video_report)

    return report

# ──────────────────────────────────────────────────────────
# SAVE REPORT
# ──────────────────────────────────────────────────────────

def save_report(report):
    """Salva relatório em JSON"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f'analytics_completo_{date_str}.json'
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f'[OK] Relatório salvo: {filepath}')

    # Registrar no log
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(LOG_FILE, 'a', encoding='utf-8') as lf:
        lf.write(f'[{now}] ANUBIS -- Analytics completo extraído via API -> {filepath}\n')

    return filepath

# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

def main():
    print('='*60)
    print('ANUBIS — Agente de Analytics')
    print('='*60)

    # Autenticar
    creds = authenticate()
    if not creds:
        print('[ERRO] Falha na autenticacao')
        return False

    youtube = build('youtube', 'v3', credentials=creds)
    youtube_analytics = build('youtubeAnalytics', 'v2', credentials=creds)
    print('[OK] Autenticado no YouTube')

    # Obter ID do canal
    channel_id = get_channel_id(youtube)
    if not channel_id:
        print('[ERRO] Canal nao encontrado')
        return False
    print(f'[OK] Canal ID: {channel_id}')

    # Obter todos os vídeos
    videos = get_all_videos(youtube, channel_id)
    print(f'[OK] {len(videos)} vídeos encontrados')

    # Gerar relatório
    report = generate_report(youtube, youtube_analytics, channel_id, videos)

    # Salvar
    save_report(report)

    print('='*60)
    print('[SUCESSO] Analytics coletados!')
    print('='*60)
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
