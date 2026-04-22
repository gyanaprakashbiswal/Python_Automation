import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout, ConnectionError
import time
from modules.logger import setup_logger

logger = setup_logger(__name__)

class WebScraper:
    def __init__(self, headers=None, timeout=10):
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        self.timeout = timeout

    def fetch_url(self, url: str, retries: int = 3, backoff_factor: float = 0.5) -> str:
        """
        Fetches the HTML content of a given URL with retry logic.
        """
        logger.info(f"Fetching URL: {url}")
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status() # Raise an exception for bad status codes
                logger.info(f"Successfully fetched {url} (Status: {response.status_code})")
                return response.text
            except (ConnectionError, Timeout) as e:
                logger.warning(f"Attempt {attempt + 1}/{retries} failed for {url}. Error: {e}")
                time.sleep(backoff_factor * (2 ** attempt)) # Exponential backoff
            except RequestException as e:
                logger.error(f"Failed to fetch {url}. Error: {e}")
                break # Don't retry for 4xx/5xx errors typically
        
        logger.error(f"All {retries} attempts failed for {url}.")
        return ""

    def parse_html(self, html_content: str) -> dict:
        """
        Parses HTML content and extracts key elements.
        """
        if not html_content:
            logger.warning("Empty HTML content provided to parse_html.")
            return {}

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract data
            title = soup.title.string.strip() if soup.title else ""
            
            headings = []
            for h in soup.find_all(['h1', 'h2', 'h3']):
                headings.append(h.get_text(strip=True))
                
            links = []
            for a in soup.find_all('a', href=True):
                links.append(a['href'])
                
            paragraphs = []
            for p in soup.find_all('p'):
                text = p.get_text(strip=True)
                if text:
                    paragraphs.append(text)
            
            tables = []
            for table in soup.find_all('table'):
                table_data = []
                for row in table.find_all('tr'):
                    row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
                    if row_data:
                        table_data.append(row_data)
                tables.append(table_data)

            extracted_data = {
                "title": title,
                "headings": headings,
                "links": links,
                "paragraphs": paragraphs,
                "tables": tables
            }
            logger.info("Successfully parsed HTML content.")
            return extracted_data

        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return {}

    def parse_xml(self, xml_content: str) -> dict:
        """
        Parses XML content.
        """
        if not xml_content:
             logger.warning("Empty XML content provided to parse_xml.")
             return {}
             
        try:
            # Requires lxml to be installed
            soup = BeautifulSoup(xml_content, 'xml')
            
            # Basic extraction, can be customized based on XML structure
            tags = [tag.name for tag in soup.find_all()]
            text_content = [tag.get_text(strip=True) for tag in soup.find_all() if tag.string]

            extracted_data = {
                "tags_found": list(set(tags)),
                "content": text_content
            }
            logger.info("Successfully parsed XML content.")
            return extracted_data
            
        except Exception as e:
             logger.error(f"Error parsing XML: {e}")
             return {}

    def run(self, url: str) -> dict:
        """
        Convenience method to fetch and parse in one go.
        """
        html = self.fetch_url(url)
        if html:
            return self.parse_html(html)
        return {}
