import requests
import subprocess
import json

url = "https://lrclib.net/api/request-challenge"

response = requests.post(url)

if response.status_code == 200:
    print("Request successful")
    challenge_response = response.json()
    print(challenge_response)
    
    # Run challenge_solver with the challenge_response as an argument
    subprocess.run(["python", "scripts/challenge_solver.py", json.dumps(challenge_response)])
else:
    print(f"Request failed with status code {response.status_code}")