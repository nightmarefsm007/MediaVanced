import re
import json
import random
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from urllib.parse import urlparse
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2


'''
Supports:
https://player.vidplus.to/
https://vidplus.to/
'''


class Colors:
    header = '\033[95m'
    okblue = '\033[94m'
    okcyan = '\033[96m'
    okgreen = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


# Constants
base_url = "https://player.vidplus.pro/embed/movie/687163?autoplay=true&download=true"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
server = 3
default_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))
headers = {
    "Accept": "*/*",
    "Referer": default_domain,
    "User-Agent": user_agent,
    "X-Requested-With": "XMLHttpRequest"
}

# TMDB API Key (VidRock)
''' ⚠️ Warning: Unauthorized use of another person’s API key is prohibited. The provided key is intended strictly for testing purposes. We strongly recommend generating and using your own API key in production.'''
api_key = base64.b64decode("NTRlMDA0NjZhMDk2NzZkZjU3YmE1MWM0Y2EzMGIxYTY=").decode('utf-8')

# Get content info
match = re.search(r'\/embed\/(.*?)\/(\d+)(?:\/(\d+)\/(\d+))?', base_url)
if match:
    content_type = match.group(1)
    content_id, season, episode = (
        match.group(2),
        match.group(3) or None,
        match.group(4) or None
    )

# Get required data
response = requests.get(f"https://api.themoviedb.org/3/{content_type}/{content_id}?api_key={api_key}&append_to_response=external_ids").json()
imdb_id = response.get('imdb_id') or (response.get('external_ids') or {}).get('imdb_id')
title = response.get('title')
release_year = response.get('release_date').split('-')[0]

# Build request parameters and fetch encrypted response
request_args = '*'.join([title, release_year, imdb_id])
response = requests.get(f'{default_domain}/api/server?id={content_id}&sr={server}&args={request_args}', headers=headers).json()

# Decode the base64-encoded JSON container
encoded_payload = response.get('data')
decoded_payload = base64.b64decode(encoded_payload).decode('utf-8')
payload_json = json.loads(decoded_payload)

# Extract encryption parameters
ciphertext = base64.b64decode(payload_json.get('encryptedData'))
password = payload_json.get('key')
salt = bytes.fromhex(payload_json.get('salt'))
iv = bytes.fromhex(payload_json.get('iv'))

# Derive AES decryption key using PBKDF2 (SHA256)
derived_key = PBKDF2(password, salt, dkLen=32, count=1000, hmac_hash_module=SHA256)

# Initialize AES cipher and decrypt
cipher = AES.new(derived_key, AES.MODE_CBC, iv)
decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

# Parse final JSON containing streaming details
streaming_info = json.loads(decrypted_text)

# Resolve proxied URL to actual stream URL
video_url = streaming_info.get('url')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Origin:{Colors.endc} {default_domain}")
print("\n")
