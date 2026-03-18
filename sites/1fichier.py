import re
import requests
from bs4 import BeautifulSoup

# Provider: Bolly4U

'''
Supports:
https://1fichier.com/
'''

# The site has SSL and IP verification measures, so the scraper may not always work reliably.

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
base_url = "https://1fichier.com/?p7ix9lf97rshtdr9anmq"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
af_value = re.search(r"af=(\d+)", base_url).group(1) if "af=" in base_url else "0"
headers = {
    "Referer": "https://1fichier.com",
    "User-Agent": user_agent
}
cookies = {
    "AF": af_value
}

# Set up session
session = requests.Session()
session.headers.update(headers)
session.cookies.update(cookies)

# Fetch response
response = session.get(base_url).text
soup = BeautifulSoup(response, "html.parser")

# Prepare POST payload
adz = soup.find("input", attrs = {"name":"adz"})['value']
payload = {
    "adz" : adz
}

# Get download page
response = session.post(base_url, data=payload).text
soup = BeautifulSoup(response, "html.parser")

# Extract download URL
download_href = soup.find("a", attrs={"class": "ok btn-general btn-orange"})
if download_href is None:
    exit(f"{Colors.warning}Access blocked due to security detection. Try a different IP or use a proxy. Exiting...{Colors.endc}")

# Get video URL
video_url = download_href.get('href')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
