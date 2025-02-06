import os
import eyed3

def get_mp3_info(mp3_path):
    audiofile = eyed3.load(mp3_path)
    if audiofile is None:
        return None
    info = {
        "track_name": audiofile.tag.title,
        "album_name": audiofile.tag.album,
        "artist_name": audiofile.tag.artist,
        "duration": audiofile.info.time_secs
    }
    return info

def main():
    lrc_file = input("Please submit an LRC file: ")
    if not os.path.isfile(lrc_file):
        print("LRC file not found.")
        return

    mp3_file = os.path.splitext(lrc_file)[0] + ".mp3"
    if not os.path.isfile(mp3_file):
        print("MP3 file not found.")
        return

    mp3_info = get_mp3_info(mp3_file)
    if mp3_info is None:
        print("Failed to retrieve MP3 information.")
        return

    print("Track Information:")
    print(f"Track Name: {mp3_info['track_name']}")
    print(f"Album Name: {mp3_info['album_name']}")
    print(f"Artist Name: {mp3_info['artist_name']}")
    print(f"Duration: {mp3_info['duration']} seconds")

    lrc_type = input("Is the LRC file plain or synced? (plain/synced): ")
    if lrc_type not in ["plain", "synced"]:
        print("Invalid input. Please enter 'plain' or 'synced'.")
        return

    print(f"LRC file is {lrc_type}.")

if __name__ == "__main__":
    main()