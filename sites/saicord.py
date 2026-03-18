import re
import time
import base64
import requests
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse

'''
Supports:
https://saicord.com/
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
base_url = "https://saicord.com/hi/movies/1433-attack-on-finland.html"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Referer": default_domain,
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
}

# Create Cloudscraper Session to bypass Cloudflare
scraper = cloudscraper.create_scraper()

# Fetch response and try to bypass CF
response = scraper.get(base_url, headers=headers).text
if "Just a moment" in response:
    exit("Cloudflare detected retry again...")
soup = BeautifulSoup(response,"html.parser")

# Get main script
iframe = soup.find("div", attrs={"class": "player-iframe"})
script = iframe.find_all("script")

encrypted_data_match = re.search(r'atob\("([^"]*)"\)', script[1].string)
if not encrypted_data_match:
    exit("No encrypted data found!")

# Decode encrypted data
encoded_data = encrypted_data_match.group(1);
decoded_data = base64.b64decode(encoded_data).decode('utf-8')

# Extract video URL
video_match = re.search(r'file:"([^"]+)"', decoded_data)
video_url = video_match.group(1) if video_match else exit(print("No video URL found!"))

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
