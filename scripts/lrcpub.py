import sys
import requests
from requests.exceptions import ConnectionError
import time
import json

def get_publish_token():
    with open('auth.json', 'r') as f:
        auth_data = json.load(f)
    return f"{auth_data['prefix']}:{auth_data['nonce']}"

def main():
    if len(sys.argv) != 7:
        print("Usage: lrcrel.py <trackName> <artistName> <albumName> <duration> <plainLyrics> <syncedLyrics>")
        return

    track_name = sys.argv[1]
    artist_name = sys.argv[2]
    album_name = sys.argv[3]
    duration = float(sys.argv[4])
    plain_lyrics = sys.argv[5]
    synced_lyrics = sys.argv[6]

    publish_token = get_publish_token()
    headers = {
        "X-Publish-Token": publish_token,
        "User-Agent": "LRCPUT v0.1 (https://github.com/Seraph353/LRCPut)"
    }
    data = {
        "trackName": track_name,
        "artistName": artist_name,
        "albumName": album_name,
        "duration": duration,
        "plainLyrics": plain_lyrics,
        "syncedLyrics": synced_lyrics
    }

    url = "https://lrclib.net/api/publish"
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                print("Lyrics uploaded successfully.")
                break
            else:
                print(f"Failed to upload lyrics. Status code: {response.status_code}, Response: {response.text}")
                break
        except ConnectionError as e:
            print(f"Connection error: {e}. Retrying ({attempt + 1}/{max_retries})...")
            time.sleep(2)
    else:
        print("Failed to upload lyrics after multiple attempts.")

if __name__ == "__main__":
    main()
