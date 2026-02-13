import requests
from bs4 import BeautifulSoup
import urllib.parse

# Konfiguration
BASE_URL = "https://moflix-stream.xyz"
OUTPUT_FILE = "moflex_z11.m3u"

def run_scraper():
    print(f"Z11-Experte: Starte optimierten Scrape für {BASE_URL}")
    
    # Erweiterte Browser-Tarnung
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com/'
    }

    try:
        session = requests.Session()
        # Seite mit Timeout laden, um Hänger zu vermeiden
        response = session.get(BASE_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links_found = 0

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            # Suche nach Links in typischen Film-Containern
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                # Wir suchen nach den Schlagworten im Link-Pfad
                if any(x in href.lower() for x in ['/movie/', '/serie/', '/watch/', '/film/']):
                    
                    full_url = urllib.parse.urljoin(BASE_URL, href)
                    text = a_tag.get_text().strip()
                    
                    # Falls kein Text vorhanden ist, extrahiere den Namen aus dem URL-Pfad
                    if not text or len(text) < 2:
                        text = href.rstrip('/').split('/')[-1].replace('-', ' ').title()
                    
                    f.write(f"#EXTINF:-1, {text}\n")
                    f.write(f"{full_url}\n")
                    links_found += 1

        print(f"Z11-Experte: Fertig! {links_found} Einträge generiert.")

    except Exception as e:
        print(f"Z11-Experte: Fehler beim Scrapen -> {e}")

if __name__ == "__main__":
    run_scraper()
