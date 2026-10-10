import requests
from bs4 import BeautifulSoup


def complexAlbumList(album, url):
    currentList = album
    artist_url = url.split("artists/")[1]
    albumPage = f"https://genius.com/artists/{artist_url}/albums"

    #uses the full album page for the artist to get them all
    headers = {
            "User-Agent": "Mozilla/5.1 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Alt-Used": "genius.com",
            "Connection": "keep-alive"
        }

    response = requests.get(albumPage, headers=headers, timeout=10)
    
    if response.status_code != 200:
        print("Website Blocking u")
        print(response.status_code)
        return currentList

    soup = BeautifulSoup(response.text, 'html.parser')

    #TEST
    testHtml(soup, "output2.txt")

    newAlbums = []
    for a in soup.select('a[class*="DiscographyItem__Container"]'):
        t = a.find("h3")
        y = a.select_one('div[class*="ReleaseDate"]')

        if t:
            newAlbums.append({
                "title": t.get_text(strip=True),
                "year": y.get_text(strip=True)
                })
    return newAlbums

#looks at albums on the artist page and finds if there are more albums then on just the page returns that there is more and the albums
# returns: albums + if there are more that need a complex AlbumList Search 
def simpleAlbumList(page: BeautifulSoup):
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
    moreAlbums = page.select_one("a.full_width_button[href*='albums']")
    if moreAlbums:
        print("found extra albums!")
        return {
            "albums": albums,
            "moreAlbums": True
        }
    return {
        "albums": albums,
        "moreAlbums": False
    }


def main():

    url = input("enter your artists genius page!")
    if url == "test":
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

    #TEST
    testHtml(soup, "output.txt")

    list = simpleAlbumList(soup)

    albums = []

    if list["moreAlbums"] == True:
            albums = complexAlbumList(list["albums"], url)

    if albums:
        print(albums)
    else:
        print(list["moreAlbums"])
    return

#TEST
#outputs the website html to the txt for easier searching
def testHtml(s: BeautifulSoup, output_loco):
    f = open(output_loco, "w", encoding="utf-8")
    try:
        f.write(s.prettify())
    finally:
        f.close()


if __name__ == "__main__":
    main()

