import requests
from bs4 import BeautifulSoup

url = "https://genius.com/artists/Juice-wrld"

#fakes the header so the request seems more legit 
headers = {
    "User-Agent": "Mozilla/5.1 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Alt-Used": "genius.com",
    "Connection": "keep-alive"
}

response = requests.get(url, headers=headers, timeout = 10)

if response.status_code == 200:
    print("it worked")
    print(response.text)
else:
    print(response.status_code)


