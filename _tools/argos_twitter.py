#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARGOS — Integração Twitter API v2
Busca trending topics e dados de engagement para viral score
"""

import json
import os
import requests
from datetime import datetime, timedelta

CREDS_FILE = os.path.expanduser('~/.claude/twitter_creds.json')

def load_creds():
    with open(CREDS_FILE, encoding='utf-8') as f:
        return json.load(f)

def search_tweets(query, max_results=10):
    """Busca tweets recentes (últimos 7 dias) via Twitter API v2"""
    creds = load_creds()
    bearer = creds['bearer_token']

    headers = {'Authorization': f'Bearer {bearer}'}

    # Query: texto + filtro de engagement mínimo
    query_str = f'{query} -is:retweet lang:pt'

    params = {
        'query': query_str,
        'max_results': max_results,
        'tweet.fields': 'public_metrics,created_at',
        'expansions': 'author_id',
        'user.fields': 'username,public_metrics'
    }

    try:
        resp = requests.get(
            'https://api.twitter.com/2/tweets/search/recent',
            headers=headers,
            params=params,
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f'[ERRO] Twitter search falhou: {e}')
        return None


def extract_engagement(tweets_response):
    """Extrai métricas de engagement dos tweets"""
    if not tweets_response or 'data' not in tweets_response:
        return []

    results = []
    for tweet in tweets_response['data']:
        metrics = tweet.get('public_metrics', {})
        results.append({
            'text': tweet['text'][:100],
            'likes': metrics.get('like_count', 0),
            'retweets': metrics.get('retweet_count', 0),
            'replies': metrics.get('reply_count', 0),
            'quotes': metrics.get('quote_count', 0),
            'total_engagement': sum([
                metrics.get('like_count', 0),
                metrics.get('retweet_count', 0),
                metrics.get('reply_count', 0),
                metrics.get('quote_count', 0)
            ])
        })

    return sorted(results, key=lambda x: x['total_engagement'], reverse=True)


def calculate_twitter_score(engagement_list):
    """Calcula viral score baseado em engagement no Twitter"""
    if not engagement_list:
        return 0

    avg_engagement = sum(e['total_engagement'] for e in engagement_list) / len(engagement_list)

    # Normalizar para 0-100
    # Twitter trending: ~1000+ engagement é "quente"
    score = min(100, (avg_engagement / 1000) * 100)

    return score


def main():
    print('='*60)
    print('ARGOS — Twitter Integration Test')
    print('='*60)

    # Testar com alguns tópicos do nicho
    topics = [
        'apocalipse profecia',
        'fim dos tempos',
        'tecnologia CBDC',
        'inteligência artificial perigo',
        'criptomoedas'
    ]

    results = {}

    print('\n[ARGOS] Buscando trending topics no Twitter...')
    for topic in topics:
        print(f'  Buscando: {topic}...')
        tweets = search_tweets(topic, max_results=10)
        engagement = extract_engagement(tweets)
        score = calculate_twitter_score(engagement)

        results[topic] = {
            'score': score,
            'engagement_avg': sum(e['total_engagement'] for e in engagement) / len(engagement) if engagement else 0,
            'tweet_count': len(engagement),
            'top_tweet': engagement[0] if engagement else None
        }

        print(f'    Score: {score:.1f} | Avg engagement: {results[topic]["engagement_avg"]:.0f}')

    # Ranking
    print('\n=== RANKING TWITTER (Viral Score) ===')
    ranked = sorted(results.items(), key=lambda x: x[1]['score'], reverse=True)
    for i, (topic, data) in enumerate(ranked, 1):
        print(f'{i}. {topic}: {data["score"]:.1f} (avg engagement: {data["engagement_avg"]:.0f})')

    print('='*60)
    print('[OK] Dados coletados da Twitter API v2')
    print('='*60)


if __name__ == '__main__':
    main()
