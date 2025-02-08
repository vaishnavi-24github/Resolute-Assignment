import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.models.models import Metadata

def scrape_url(url: str, task_id: str, db: Session):
    """Scrapes a URL and extracts meta tags."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else ""
        description = soup.find("meta", attrs={"name": "description"})
        description = description["content"] if description else ""
        keywords = soup.find("meta", attrs={"name": "keywords"})
        keywords = keywords["content"] if keywords else ""

        metadata = Metadata(
            task_id=task_id,
            url=url,
            title=title,
            description=description,
            keywords=keywords
        )
        db.add(metadata)
        db.commit()
        return metadata
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None