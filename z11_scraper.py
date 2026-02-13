import requests
from bs4 import BeautifulSoup
import re

URL = "https://moflix-stream.xyz" 
OUTPUT_FILE = "moflex_z11.m3u"

def get_stream_link(page_url):
    # Diese Funktion simuliert das 'Tiefer-Graben'
    # Sie sucht nach m3u8 oder mp4 Links im Quellcode der Unterseiten
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(page_url, headers=headers, timeout=10)
        # Suche nach gängigen Streaming-Mustern
        match = re.search(r'(https?://[^\s^"]+\.(?:m3u8|mp4))', r.text)
        return match.group(1) if match else page_url
    except:
        return page_url

def generate_m3u():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        # Suche nach Film-Links (angepasst an die Struktur der Seite)
        for link in soup.find_all('a', href=True):
            if "/watch/" in link['href'] or "/movie/" in link['href']:
                title = link.text.strip() or "Unbekannter Film"
                full_url = link['href'] if link['href'].startswith('http') else URL + link['href']
                
                # Hol den 'echten' Link
                stream_url = get_stream_link(full_url)
                
                f.write(f"#EXTINF:-1, {title}\n")
                f.write(f"{stream_url}\n")

if __name__ == "__main__":
    generate_m3u()
