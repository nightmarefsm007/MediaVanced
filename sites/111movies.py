import re
import random
import base64
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import pad

'''
Supports:
https://111movies.net/
https://111movies.com/
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
base_url = "https://111movies.net/movie/533535"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent,
    "Content-Type": "application/x-shockwave-flash",
    "X-Csrf-Token": "lOky1FfH4K8k7nlP1rymCoe3q2smDW8T",
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input):
    src = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    dst = "zF-NXZYgxKqj7nbuGoI_SDfkQ9y3VcJrRBip6tadPwv0MWLehT5Um4As2l8C1HEO"
    trans = str.maketrans(src, dst)
    b64 = base64.b64encode(input.encode()).decode().replace('+', '-').replace('/', '_').replace('=', '')
    return b64.translate(trans)

# Fetch page content
response = requests.get(base_url, headers=headers).text

# Extract raw data
match = re.search(r'{\"data\":\"(.*?)\"', response)
if not match:
    exit(print("No data found!"))
raw_data = match.group(1)


# AES encryption setup
key_hex = "55eb57c5e52d3ae19f899e702cb539084adf606b06cc44382c21e48a82215d8a"
iv_hex = "324d1fae84bafaba643f236ee116de27"
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data).hex()

# XOR operation
xor_key = bytes.fromhex("dd69ce")
xor_result = ''.join(chr(ord(char) ^ xor_key[i % len(xor_key)]) for i, char in enumerate(aes_encrypted))

# Custom encoded string
encoded_final = custom_encode(xor_result)

# Make final request
static_path = "9816ad6837c78fcc2e0944fe2e6398b8a525d43f1afea28f9d5347b35cd53128/c1a5e2db/APA91iMgb2ifswAU727_OpyUBk45sDi2ciUVYVGZXVUXlYUrIshxfIIWC7WwfK3Rug52O7fWefpKiXKVeVPB-I4gl5GeF6Wj-MeAmJpzWiKkZMhg5kDvEv0fRguit6YtNIAHOpF47joyVLBgqzKlw98WhN6eQiF_QvG8Mmq3j2tpbtfSw0oAU-o/2db11c71f014bd4128f1a3ec314796da7e09b87e/tor/c6779436-9455-57ed-8527-73ad249a83db"
api_servers = f"https://111movies.net/{static_path}/{encoded_final}/sr"
response = requests.post(api_servers, headers=headers).json()

# Select a random server
server = response[0].get('data')
api_stream = f"https://111movies.net/{static_path}/{server}"
response = requests.post(api_stream, headers=headers)

# Extract video URL
video_url = response.json()['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")
