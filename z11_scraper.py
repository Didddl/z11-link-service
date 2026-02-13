import requests
from bs4 import BeautifulSoup
import urllib.parse

# Ziel-Konfiguration
BASE_URL = "https://moflix-stream.xyz"
OUTPUT_FILE = "moflex_z11.m3u"

def run_scraper():
    print(f"Z11-Experte: Scrape gestartet für {BASE_URL}")
    
    # Tarnkappe für den Scraper (User-Agent)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        # 1. Seite laden
        session = requests.Session()
        response = session.get(BASE_URL, headers=headers, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links_found = 0

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            # 2. Suche nach JEDEM Link, der Filme oder Serien enthalten könnte
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                text = a_tag.get_text().strip()
                
                # Filter: Wir nehmen Links, die typische Streaming-Begriffe enthalten
                # oder die in Kacheln/Containern liegen
                if any(x in href.lower() for x in ['/movie/', '/serie/', '/watch/', '/film/', '/vose/']):
                    
                    # URL vervollständigen
                    full_url = urllib.parse.urljoin(BASE_URL, href)
                    
                    # Falls kein Text da ist (z.B. nur ein Bild-Link), Titel aus URL generieren
                    if not text or len(text) < 2:
                        text = href.rstrip('/').split('/')[-1].replace('-', ' ').title()
                    
                    # Eintrag schreiben
                    f.write(f"#EXTINF:-1, {text}\n")
                    f.write(f"{full_url}\n")
                    links_found += 1

        print(f"Z11-Experte: Erfolg! {links_found} Filme/Serien gefunden.")

    except Exception as e:
        print(f"Z11-Experte: Fehler aufgetreten -> {e}")

if __name__ == "__main__":
    run_scraper()
