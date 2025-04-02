
### LRCPut

LRCPut is a simple program to upload lrc files to [LRCLIB](lrclib.net).
It scans your lrc file and creates a non-synced version if it can.
The program includes a challenge solver to gain permission to edit the database.

#### Usage
1. Start the script.
2. Enter the path of your lrc file.
	Ensure the mp3 file of that song is in the same directory
3. Check the lrc output. Ensure that the correct information is present, including the Name information that will be used to identify the song.
4. Get a LRCLIB key. The script will freeze while it solves the challenge, which will take a variable amount of time depending on hardware and the challenge result.
5. Submit to LRCLIB. A window will show what information was submitted.

This process must be repeated for each lyric you upload, as the key only works once after generation.

#### Considerations
- It is best to publish synced lyrics if possible. The script will automatically generate a non-synced version during processing.
- If possible, ensure that the related mp3 file is as close to the original song as possible. Track length information is included and an incorrect time will result in the lyric not being used for some users.
- The challenge is a brute force random hash. It may take a long time or very little time to solve, depending on hardware, and the result will only last 5 minutes. This means some keys may be invalid when they are solved, and make some very weak hardware incapable of consistently submitting lyrics.
 
