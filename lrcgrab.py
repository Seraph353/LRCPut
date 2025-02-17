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
        if timestamp_pattern.search(lrc_content):
            synced_lyrics = lrc_content
            plain_lyrics = None
        else:
            plain_lyrics = lrc_content
            synced_lyrics = None

    messagebox.showinfo("Track Information", 
                        f"Track Name: {track_name}\n"
                        f"Artist Name: {artist_name}\n"
                        f"Album Name: {album_name}\n"
                        f"Duration: {duration}\n"
                        f"Plain Lyrics: {plain_lyrics}\n"
                        f"Synced Lyrics: {synced_lyrics}")

    return track_name, artist_name, album_name, duration, plain_lyrics, synced_lyrics

def forward_to_lrcpub():
    result = submit_file()
    if result:
        track_name, artist_name, album_name, duration, plain_lyrics, synced_lyrics = result
        plain_lyrics = plain_lyrics if plain_lyrics is not None else ""
        synced_lyrics = synced_lyrics if synced_lyrics is not None else ""
        subprocess.run(["python", "lrcpub.py", track_name, artist_name, album_name, str(duration), plain_lyrics, synced_lyrics])
        forward_button.config(state=tk.DISABLED)
        guidance_label.config(text="Please get a new key to enable submissions.", fg="red")

def get_key():
    try:
        subprocess.run(["python", "get_challenge.py"])
        # Do not try to grab the auth, just notify the user
        messagebox.showinfo("Info", "Challenge solved. Please use the new key to submit within 5 minutes.")
        forward_button.config(state=tk.NORMAL)
        guidance_label.config(text="")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get key: {e}")

def close_app(event):
    root.destroy()

root = tk.Tk()
root.title("LRC Metadata Extractor")

root.bind('<Escape>', close_app)

path_entry = tk.Entry(root, width=50)
path_entry.pack(pady=10)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=5)

submit_button = tk.Button(root, text="Check LRC result", command=submit_file)
submit_button.pack(pady=20)

forward_button = tk.Button(root, text="Submit to LRCLIB", command=forward_to_lrcpub)
forward_button.pack(pady=20)

guidance_label = tk.Label(root, text="")
guidance_label.pack()

get_key_button = tk.Button(root, text="Get LRCLIB Key", command=get_key)
get_key_button.pack(pady=5)

root.mainloop()
