import re
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import pad

'''
Supports:
https://kisskh.ws/
https://kisskh.do/
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
base_url = 'https://kisskh.ws/Drama/Pursuit-of-Jade---Chasing-Jade/Episode-1?id=10104&ep=207278&page=0&pageSize=100'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
subs_token = 'VgV52sWhwvBSf8BsM3BRY9weWiiCbtGp' # Use this token for subtitles
vid_token = '62f176f3bb1b5b8e70e39932ad34a0c7'
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Utility Functions
''' Mimics JavaScript's string hashing with 32-bit signed integer behavior '''
def hash_func(string: str) -> int:
    hash_val = 0
    
    for char in string:
        char_code = ord(char)
        int32_hash = hash_val & 0xFFFFFFFF
        if int32_hash > 0x7FFFFFFF:
            int32_hash -= 0x100000000
        shifted = (int32_hash << 5) & 0xFFFFFFFF
        if shifted > 0x7FFFFFFF:
            shifted -= 0x100000000
        hash_val = shifted - hash_val + char_code
    return hash_val


# Extract the episode ID from the URL
match = re.search(r'ep=(\d+)', base_url)
if not match:
    exit("No Episode ID Found")
episode_id = match.group(1)

# Build the initial payload array for token generation
payload_arr = ['', episode_id, '', 'mg3c3b04ba', '2.8.10', vid_token, '4830201', 'kisskh', 'kisskh', 'kisskh', 'kisskh', 'kisskh', 'kisskh', '00', '']

# Insert the hashed value into the payload to mirror JS token behavior
joined = '|'.join(payload_arr)
payload_arr.insert(1, str(hash_func(joined)))
final = '|'.join(payload_arr)

# Prepare AES encryption parameters and pad the payload using PKCS7
key = bytes.fromhex("4F6BDAA39E2F8CB07F5E722D9EDEF314")
iv = bytes.fromhex("01504AF356E619CF2E42BBA68C3F70F9")
data_bytes = final.encode('utf-8')
padded_data = pad(data_bytes, AES.block_size)

# Encrypt the padded payload using AES-128-CBC
cipher = AES.new(key, AES.MODE_CBC, iv)
encrypted = cipher.encrypt(padded_data)

# Convert the encrypted bytes to a hexadecimal string for use in the API request
token = encrypted.hex().upper()

# Request the streaming data from the server using the generated token
response = requests.get(f'https://kisskh.ws/api/DramaList/Episode/{episode_id}.png?err=false&ts=null&time=null&kkey={token}', headers=headers).json()

# Extract the video URL from the API response
video_url = response.get('Video')

# Display the captured video URL
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
