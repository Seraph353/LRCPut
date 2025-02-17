import requests
import json
import hashlib
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class ResponseError(Exception):
    def __init__(self, status_code, error, message):
        self.status_code = status_code
        self.error = error
        self.message = message
        super().__init__(f"{error}: {message}")

def request_challenge(lrclib_instance):
    version = "1.0.0"  # Replace with your actual version
    user_agent = f"LRCGET v{version} (https://github.com/tranxuanthang/lrcget)"
    api_endpoint = f"{lrclib_instance.rstrip('/')}/api/request-challenge"

    headers = {
        "User-Agent": user_agent
    }

    response = requests.post(api_endpoint, headers=headers, timeout=10, allow_redirects=True)

    if response.status_code == 200:
        return response.json()
    elif response.status_code in [400, 503, 500]:
        error_response = response.json()
        raise ResponseError(response.status_code, error_response["error"], error_response["message"])
    else:
        logging.debug(f"Unexpected status code: {response.status_code}")
        logging.debug(f"Response content: {response.content}")
        raise ResponseError(None, "UnknownError", "Unknown error happened")


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

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python challenge_solver.py <challenge_response>")
        sys.exit(1)
    
    challenge_response = json.loads(sys.argv[1])
    prefix = challenge_response["prefix"]
    target = challenge_response["target"]
    
    try:
        nonce = solve_challenge(prefix, target)
        print(f"Solved nonce: {nonce}")
        
        # Output to nonce.json
        with open("nonce.json", "w") as f:
            json.dump({"nonce": nonce}, f)
    except ResponseError as e:
        print(f"Error: {e}")
