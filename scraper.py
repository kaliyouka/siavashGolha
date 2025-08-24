import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time


def get_mp3_url(golha_url):
       headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.golha.co.uk/", 
        "Connection": "keep-alive"
    }
    try:
        response = requests.get(golha_url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text
        pattern = r'mp3\s*:\s*["\'](/vod/[^"\']+\.mp3)["\']'
        matches = re.findall(pattern,html,re.IGNORECASE)
        if matches:
            mp3_url = urljoin("https://www.golha.co.uk", matches[0])
            time.sleep(1)
            return mp3_url, None
        soup = BeautifulSoup(html, "html.parser")
        audio = soup.find("audio", src=re.compiler(r"\.mp3$",re.IGNORECASE))
        if audio and audio.get("src"):
            mp3_url = urljoin(golha_url,audio["src"])
            time.sleep(1)
            return mp3_url,None
        return None, "No MP3 found on this page. The site may have changed or the URL is incorrect."
    except requests.exceptions.RequestException as e :
        return None , f"Error Fetching Page : {str(e)}"

