import tkinter as tk
from tkinter import filedialog, messagebox
import os
import eyed3
from mutagen.flac import FLAC
import re
import subprocess
import json

def browse_file():
    lrc_file_path = filedialog.askopenfilename(filetypes=[("LRC files", "*.lrc")])
    if lrc_file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, lrc_file_path)

def submit_file():
    lrc_file_path = path_entry.get()
    if not lrc_file_path or not os.path.exists(lrc_file_path):
        messagebox.showerror("Error", "Please provide a valid LRC file path.")
        return

    base_name = os.path.splitext(lrc_file_path)[0]
    mp3_file_path = base_name + ".mp3"
    flac_file_path = base_name + ".flac"

    if os.path.exists(mp3_file_path):
        audio_file = eyed3.load(mp3_file_path)
        if audio_file and audio_file.tag:
            track_name = audio_file.tag.title
            album_name = audio_file.tag.album
            artist_name = audio_file.tag.artist
            duration = audio_file.info.time_secs
        else:
            messagebox.showerror("Error", "Failed to load MP3 metadata.")
            return
    elif os.path.exists(flac_file_path):
        audio_file = FLAC(flac_file_path)
        track_name = audio_file.get("title", ["Unknown"])[0]
        album_name = audio_file.get("album", ["Unknown"])[0]
        artist_name = audio_file.get("artist", ["Unknown"])[0]
        duration = audio_file.info.length
    else:
        messagebox.showerror("Error", "No corresponding MP3 or FLAC file found.")
        return

    with open(lrc_file_path, 'r', encoding='utf-8') as lrc_file:
        lrc_content = lrc_file.read()
        timestamp_pattern = re.compile(r'\[\d{2}:\d{2}.\d{2}\]')
        synced_lyrics = "true" if timestamp_pattern.search(lrc_content) else "false"
        plain_lyrics = "true" if synced_lyrics == "false" else "false"

    messagebox.showinfo("Track Information", 
                        f"Track Name: {track_name}\n"
                        f"Artist Name: {artist_name}\n"
                        f"Album Name: {album_name}\n"
                        f"Duration: {duration}\n"
                        f"Plain Lyrics: {plain_lyrics}\n"
                        f"Synced Lyrics: {synced_lyrics}")

    return track_name, artist_name, album_name, duration, plain_lyrics, synced_lyrics

def forward_to_lrcrel():
    track_name, artist_name, album_name, duration, plain_lyrics, synced_lyrics = submit_file()
    subprocess.run(["python", "lrcrel.py", track_name, artist_name, album_name, str(duration), plain_lyrics, synced_lyrics])

def get_key():
    try:
        result = subprocess.run(["python", "get_challenge.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(result.stderr)
        
        if not result.stdout.strip():
            raise Exception("Empty response from get_challenge.py")
        
        challenge_response = json.loads(result.stdout)
        prefix = challenge_response["prefix"]
        target = challenge_response["target"]
        
        result = subprocess.run(["python", "challenge_solver.py", json.dumps(challenge_response)], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(result.stderr)
        
        nonce = result.stdout.strip()
        messagebox.showinfo("Nonce", f"Solved nonce: {nonce}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON response from get_challenge.py")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get key: {e}")

root = tk.Tk()
root.title("LRC Metadata Extractor")

path_entry = tk.Entry(root, width=50)
path_entry.pack(pady=10)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=5)

submit_button = tk.Button(root, text="Submit LRC File", command=submit_file)
submit_button.pack(pady=20)

forward_button = tk.Button(root, text="Forward to lrcrel.py", command=forward_to_lrcrel)
forward_button.pack(pady=20)

get_key_button = tk.Button(root, text="Get Key", command=get_key)
get_key_button.pack(pady=5)

root.mainloop()
