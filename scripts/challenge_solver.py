import json
import hashlib
import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Delete existing nonce.json file if it exists
if os.path.exists("auth.json"):
    os.remove("auth.json")

# Give an error if something goes wrong
class ResponseError(Exception):
    def __init__(self, status_code, error, message):
        self.status_code = status_code
        self.error = error
        self.message = message
        super().__init__(f"{error}: {message}")

# Checks that the solved challenge complies with the target
def verify_nonce(result, target):
    if len(result) != len(target):
        return False

    for i in range(len(result) - 1):
        if result[i] > target[i]:
            return False
        elif result[i] < target[i]:
            break

    return True

def solve_challenge(prefix, target_hex):
    nonce = 0
    target = bytes.fromhex(target_hex)

    while True:
        input_str = f"{prefix}{nonce}"
        hashed = hashlib.sha256(input_str.encode()).digest()

        if verify_nonce(hashed, target):
            break
        else:
            nonce += 1

    return str(nonce)


if __name__ == "__main__":
    
    challenge_response = json.loads(sys.argv[1])
    prefix = challenge_response["prefix"]
    target = challenge_response["target"]
    
    try:
        nonce = solve_challenge(prefix, target)
        print(f"Solved nonce: {nonce}")
        
        # Output to auth.json
        with open("auth.json", "w") as f:
            json.dump({"nonce": nonce, "prefix": prefix}, f)
    except ResponseError as e:
        print(f"Error: {e}")
