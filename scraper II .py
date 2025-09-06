import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
# from fake_useragent import UserAgent

def get_mp3_url(golha_url):
    """
    Scrape a Golha programme URL to extract the MP3 URL.
    Args:
        golha_url (str): URL like https://www.golha.co.uk/en/programme/465
    Returns:
        tuple: (mp3_url, error_message) - MP3 URL if found, else (None, error)
    """
    # Initialize User-Agent rotator
    ua = UserAgent()
    
    # Enhanced headers to mimic a browser
    headers = {
        "User-Agent": ua.random,  # Randomize User-Agent
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.golha.co.uk/",
        "DNT": "1",  # Do Not Track
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    # Set up retries
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[403, 429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    try:
        # Fetch the page
        response = session.get(golha_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise for 404, 403, etc.
        html = response.text
        
        # Method 1: Regex for 'mp3: "/vod/...mp3"'
        pattern = r'mp3\s*:\s*["\'](/vod/[^"\']+\.mp3)["\']'
        matches = re.findall(pattern, html, re.IGNORECASE)
        
        if matches:
            mp3_url = urljoin("https://www.golha.co.uk", matches[0])
            time.sleep(1)  # Be polite
            return mp3_url, None
        
        # Method 2: Fallback to <audio> tag
        soup = BeautifulSoup(html, "html.parser")
        audio = soup.find("audio", src=re.compile(r"\.mp3$", re.IGNORECASE))
        if audio and audio.get("src"):
            mp3_url = urljoin(golha_url, audio["src"])
            time.sleep(1)
            return mp3_url, None
        
        return None, "No MP3 found on this page. The site may have changed or the URL is incorrect."
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            # Debug: Log response snippet
            error_debug = f"403 Forbidden: Golha blocked the request. Response start: {response.text[:200]}"
            return None, error_debug
        return None, f"Error fetching page: {str(e)}"
    except requests.exceptions.RequestException as e:
        return None, f"Error fetching page: {str(e)}"