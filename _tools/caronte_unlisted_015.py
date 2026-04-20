#!/usr/bin/env python3
import os, pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

VIDEO_ID   = 'VwlZ2NLQyFc'
TOKEN_FILE = os.path.expanduser('~/.claude/youtube_token.pickle')

with open(TOKEN_FILE, 'rb') as f:
    creds = pickle.load(f)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

youtube = build('youtube', 'v3', credentials=creds)
youtube.videos().update(
    part='status',
    body={'id': VIDEO_ID, 'status': {'privacyStatus': 'unlisted', 'madeForKids': False}}
).execute()
print(f'[OK] {VIDEO_ID} -> UNLISTED | https://youtu.be/{VIDEO_ID}')
