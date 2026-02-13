import requests
from bs4 import BeautifulSoup
import re

# Ziel-URL der Webseite
URL = "https://moflix-stream.xyz" 
# Name der Datei, die für die Z11 generiert wird
OUTPUT_FILE = "moflex_z11.m3u"

def generate_m3u():
    print(f"Starte Scraper für {URL}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        count = 0
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            # Suche nach allen Links auf der Seite
            for link in soup.find_all('a', href=True):
                href = link['href']
                title = link.text.strip()
                
                # Filtert nach typischen Film- und Serien-Pfaden
                if any(pattern in href for pattern in ['/movie/', '/serie/', '/watch/', '/film/']):
                    # Sicherstellen, dass die URL vollständig ist
                    full_url = href if href.startswith('http') else URL + href
                    
                    # Falls kein Text im Link steht, nutze einen Platzhalter oder den Slug aus der URL
                    if not title:
                        title = href.split('/')[-1].replace('-', ' ').title()
                    
                    # Eintrag in die M3U schreiben
                    f.write(f"#EXTINF:-1, {title}\n")
                    f.write(f"{full_url}\n")
                    count += 1
        
        print(f"Erfolg! {count} Einträge wurden in {OUTPUT_FILE} geschrieben.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    generate_m3u()
