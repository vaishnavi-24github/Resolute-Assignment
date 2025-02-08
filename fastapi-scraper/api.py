# fastapi_scraper_project - Complete Code

## Project Structure
```
📦 fastapi_scraper_project
│── 📁 app                  
│   │── 📁 models           # Database models (SQLAlchemy)
│   │── 📁 schemas          # Pydantic schemas for request/response
│   │── 📁 services         # Business logic (scraping, processing)
│   │── 📁 tasks            # Celery tasks
│   │── 📁 api              # API routes
│   │── 📁 core             # Configurations (settings, DB, Redis)
│   │── main.py             # FastAPI app entry point
│── 📁 tests                # Unit & integration tests
│── 📁 deployment           # Kubernetes, CI/CD scripts
│── .dockerignore           # Ignore unnecessary files in Docker builds
│── .gitignore              # Ignore unnecessary files in Git
│── Dockerfile              # Docker container setup
│── docker-compose.yml      # Local multi-container setup
│── requirements.txt        # Python dependencies
│── README.md               # Project setup and usage guide
│── postman_collection.json # API collection for testing
│── kubernetes.yml          # Kubernetes deployment config
│── prometheus.yml          # Prometheus monitoring config
│── grafana-dashboard.json  # Grafana dashboard setup
│── .github/workflows/ci.yml # GitHub Actions for CI/CD
```

---

## `services.py` (Scraping & Business Logic)
```python
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
```

---

## `tasks.py` (Celery Task for Scraping)
```python
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
```

---

## `api.py` (FastAPI Endpoints)
```python
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.tasks.tasks import scrape_task
import csv
import uuid

router = APIRouter()

@router.post("/upload")
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a CSV file with URLs and start scraping."""
    task_ids = []
    contents = file.file.read().decode("utf-8").splitlines()
    csv_reader = csv.reader(contents)
    for row in csv_reader:
        if row:
            url = row[0]
            task_id = str(uuid.uuid4())
            scrape_task.delay(url, task_id)
            task_ids.append(task_id)
    return {"message": "Scraping started", "task_ids": task_ids}

@router.get("/status/{task_id}")
def get_status(task_id: str):
    """Check the scraping status of a specific task."""
    task_result = scrape_task.AsyncResult(task_id)
    return {"task_id": task_id, "status": task_result.status, "result": task_result.result}

@router.get("/results/{task_id}")
def get_results(task_id: str, db: Session = Depends(get_db)):
    """Retrieve metadata for a completed scraping task."""
    from app.models.models import Metadata
    metadata = db.query(Metadata).filter(Metadata.task_id == task_id).first()
    if metadata:
        return metadata
    return {"message": "No results found for this task_id"}