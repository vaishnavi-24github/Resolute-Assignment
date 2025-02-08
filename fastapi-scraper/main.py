from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import models
from app.schemas import schemas
from app.services.scraper import scrape_url
from app.tasks.celery_worker import scrape_task
import uuid
import csv
import io

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = file.file.read().decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        urls = [row[0] for row in reader if row]
        task_id = str(uuid.uuid4())
        scrape_task.delay(task_id, urls)
        return {"task_id": task_id, "message": "Scraping started"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@app.get("/status/{task_id}")
def get_status(task_id: str):
    return {"task_id": task_id, "status": "In Progress"}

@app.get("/results/{task_id}")
def get_results(task_id: str, db: Session = Depends(get_db)):
    results = db.query(models.Metadata).filter(models.Metadata.task_id == task_id).all()
    return results