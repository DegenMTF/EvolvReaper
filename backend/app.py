from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from modules import commoncrawl, opencorporates, certscan, classifier, validator
from utils import export_txt, export_md, export_csv, export_json
from db import initialize_db
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = FastAPI(title="Domain Harvester Dashboard")
initialize_db()

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.start()

def scheduled_scrape():
    print("Starting scheduled 24h scrape...")
    # Example scraping pipeline
    commoncrawl.scrape()
    opencorporates.scrape()
    certscan.scrape()
    classifier.classify_all()
    validator.validate_all()
    print("Scheduled scrape completed!")

# Add 24h interval job
scheduler.add_job(scheduled_scrape, 'interval', hours=24)

# Serve frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.get("/api/stats")
def get_stats():
    from db import get_connection
    conn = get_connection()
    c = conn.cursor()
    
    total = c.execute("SELECT COUNT(*) FROM domains").fetchone()[0]
    industries = c.execute("SELECT COUNT(DISTINCT industry) FROM domains").fetchone()[0]
    countries = c.execute("SELECT COUNT(DISTINCT country) FROM domains").fetchone()[0]
    
    conn.close()
    return {
        "total_domains": total,
        "industry_count": industries,
        "country_count": countries
    }

@app.delete("/api/domains")
def delete_all_domains():
    from db import get_connection
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM domains")
    conn.commit()
    conn.close()
    return {"status": "success", "message": "All domains deleted"}

@app.post("/scrape")
def manual_scrape(background_tasks: BackgroundTasks):
    background_tasks.add_task(scheduled_scrape)
    return {"status": "Manual scrape started"}

@app.get("/export/txt")
def export_txt_file():
    path = export_txt.generate()
    return FileResponse(path, filename="domains.txt")

@app.get("/export/md")
def export_md_file():
    path = export_md.generate()
    return FileResponse(path, filename="domains.md")

@app.get("/export/csv")
def export_csv_file():
    path = export_csv.generate()
    return FileResponse(path, filename="domains.csv")

@app.get("/export/json")
def export_json_file():
    path = export_json.generate()
    return FileResponse(path, filename="domains.json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)