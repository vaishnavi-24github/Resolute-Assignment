from celery import Celery
from sqlalchemy.orm import Session
from app.services import scrape_url
from app.core.database import SessionLocal

celery = Celery(
    "tasks",
    broker="redis://redis_queue:6379/0",
    backend="redis://redis_queue:6379/0"
)

@celery.task
def scrape_task(url: str, task_id: str):
    """Background task to scrape a URL."""
    db: Session = SessionLocal()
    try:
        result = scrape_url(url, task_id, db)
        return result.title if result else "Failed"
    finally:
        db.close()