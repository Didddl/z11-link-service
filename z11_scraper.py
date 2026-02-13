import requests
from bs4 import BeautifulSoup

# Ziel-URL
URL = "https://moflix-stream.xyz" 
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
            
            # Suche nach allen Links, die Filme oder Serien enthalten könnten
            for link in soup.find_all('a', href=True):
                href = link['href']
                title = link.text.strip()
                
                # Wir filtern nach typischen Pfaden wie /movie/, /series/ oder /watch/
                if any(x in href for x in ['/movie/', '/series/', '/watch/', '/film/']):
                    # Vervollständige die URL, falls sie nur ein Pfad ist
                    full_url = href if href.startswith('http') else URL + href
                    
                    # Falls kein Text im Link steht, versuchen wir den Namen aus der URL zu ziehen
                    if not title:
                        title = href.rstrip('/').split('/')[-1].replace('-', ' ').title()
                    
                    f.write(f"#EXTINF:-1, {title}\n")
                    f.write(f"{full_url}\n")
                    count += 1
        
        print(f"Erfolg! {count} Einträge wurden in {OUTPUT_FILE} geschrieben.")

    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    generate_m3u()
