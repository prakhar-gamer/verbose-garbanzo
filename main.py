import requests
from bs4 import BeautifulSoup

def albumList(page: BeautifulSoup):
    albums = []
    #looks for the any album cards visible, then checks if it has a title
    for a in page.select("a.vertical_album_card"):
        t = a.select_one(".vertical_album_card-info h3")
        y = a.select_one(".vertical_album_card-release_date")
        if t:
            albums.append({
                "title":  t.get_text(strip=True),
                "year": y.get_text(strip=True) if y else None
                })
    return albums


def main():
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

    if response.status_code != 200:
        print(response.status_code)
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    #TESTING
    #print(soup.prettify())

    list = albumList(soup)
    print(list)

if __name__ == "__main__":
    main()

