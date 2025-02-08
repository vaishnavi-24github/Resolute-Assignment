# 📌 FastAPI Scraper Project

This project allows users to upload a CSV file containing URLs. The system scrapes each URL asynchronously, extracts metadata (title, description, keywords), and stores the results in PostgreSQL. It is built with **FastAPI**, **Celery**, **Redis**, **Docker**, and **Kubernetes**.

## 🚀 Features
- ✅ **User Authentication** (Login system)
- ✅ **Upload CSV of URLs** (`POST /upload`)
- ✅ **Track Scraping Progress** (`GET /status/{task_id}`)
- ✅ **Retrieve Extracted Metadata** (`GET /results/{task_id}`)
- ✅ **Asynchronous Processing** with Celery & Redis
- ✅ **Scalable & Secure** (Docker, Kubernetes)
- ✅ **Automated CI/CD** (GitHub Actions)
- ✅ **Monitoring** (Prometheus & Grafana)

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/fastapi-scraper.git
cd fastapi-scraper
2️⃣ Create & Activate Virtual Environment
sh
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
3️⃣ Set Up Environment Variables (.env)
Create a .env file in the root directory and add:

ini
Copy
Edit
DATABASE_URL=postgresql://user:password@localhost:5432/scraper_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your_secret_key
4️⃣ Run the Application Locally
4.1 Start PostgreSQL & Redis
Ensure PostgreSQL and Redis are running locally.

4.2 Start FastAPI Server
sh
Copy
Edit
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
4.3 Start Celery Worker
sh
Copy
Edit
celery -A app.tasks.tasks worker --loglevel=info
 Docker Setup
1️⃣ Build & Run Docker Containers
sh
Copy
Edit
docker-compose up --build
This will spin up:

FastAPI backend (port 8000)
Redis queue (port 6379)
PostgreSQL database (port 5432)
Celery worker
📡 API Endpoints
Method	Endpoint	Description
POST	/upload	Upload CSV of URLs
GET	/status/{id}	Check scraping progress
GET	/results/{id}	Get extracted metadata
🚀 Deployment Options
📌 Deploy to Railway.app
Install Railway CLI:
sh
Copy
Edit
curl -fsSL https://railway.app/install.sh | sh
Login:
sh
Copy
Edit
railway login
Deploy:
sh
Copy
Edit
railway up
📌 Deploy to Fly.io
Install Fly CLI:
sh
Copy
Edit
brew install flyctl
Authenticate:
sh
Copy
Edit
flyctl auth login
Deploy:
sh
Copy
Edit
flyctl deploy
🔍 Monitoring with Prometheus & Grafana
Start Prometheus
sh
Copy
Edit
docker run -p 9090:9090 -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
Start Grafana
sh
Copy
Edit
docker run -d -p 3000:3000 grafana/grafana
Access Grafana at http://localhost:3000
Import grafana-dashboard.json for visualization.
✅ Running Tests
sh
Copy
Edit
pytest --cov=app tests/
📜 License
This project is licensed under the MIT License.

