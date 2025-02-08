from celery import Celery
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.models import Metadata

celery = Celery("tasks", broker="redis://redis:6379/0")

@celery.task
def scrape_task(task_id: str, urls: list):
    db: Session = SessionLocal()
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            metadata = Metadata(
                task_id=task_id,
                url=url,
                title=soup.title.string if soup.title else "",
                description=soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={"name": "description"}) else "",
                keywords=soup.find("meta", attrs={"name": "keywords"})["content"] if soup.find("meta", attrs={"name": "keywords"}) else ""
            )
            db.add(metadata)
            db.commit()
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    db.close()