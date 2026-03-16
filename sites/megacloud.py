import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


'''
Supports:
https://megacloud.blog/
https://rapid-cloud.co/
https://hianimes.to/
'''

# @Megacloud, @VideoStr || Love you guys! ❤️

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
provider_url = 'https://nine.mewcdn.online/ajax/episode/sources?id=1333688&type=sub-16/03/2026%206:00'
base_url = requests.get(provider_url).json()['link'] # https://rapid-cloud.co/embed-2/v2/e-1/<VIDEO_ID>?z=&_debug=true
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
headers = {
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": default_domain,
    "User-Agent": user_agent
}

# Fetch initial response
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Get file ID
video_tag = soup.select_one('#vidcloud-player')
if not video_tag:
    exit(print(f'{Colors.fail}Looks like URL expired!{Colors.endc}'))
file_id = video_tag['data-id']

# Get streaming data
response = requests.get(f'{default_domain}/embed-2/v2/e-1/getSources?id={file_id}', headers=headers).json()
video_url = response.get('sources')[0].get('file')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")