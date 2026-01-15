Here is your Deployment Guide in pure Markdown format — ready for download, copy-paste, GitHub, or documentation.


---

📦 Domain Harvester — Deployment Guide (Hostinger Ubuntu VPS)

FastAPI + Gunicorn + Uvicorn + SQLite + Nginx + 24h Auto Scheduler


---

🛠️ 0. Pre-Deployment Check
Before updating, check what is currently running on your VPS:
```bash
sudo systemctl status domainharvester
sudo systemctl status nginx
```

🧰 1. Update VPS & Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx -y
```

---

🏗️ 2. Create Project Directory
```bash
mkdir -p /var/www/domainharvester
cd /var/www/domainharvester
```
Upload your backend + frontend files into this directory.

---

🐍 3. Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

---

📦 4. Install Python Requirements
```bash
pip install -r requirements.txt
```
Ensure the file includes:
- fastapi
- uvicorn
- gunicorn
- apscheduler
- aiohttp
- beautifulsoup4
- requests
- pydantic
- python-dotenv
- sqlite-utils

---

🗄️ 5. Initialize SQLite Database
Your backend auto-creates the table, but ensure the file exists:
```bash
touch domains.db
```

---

🚀 6. Test FastAPI Before Deploying
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
Open in browser: http://YOUR_SERVER_IP:8000

---

🔥 7. Set Up Gunicorn + Uvicorn Worker
Create a systemd service:
`sudo nano /etc/systemd/system/domainharvester.service`

Paste:
```ini
[Unit]
Description=DomainHarvester FastAPI
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/domainharvester
Environment="PATH=/var/www/domainharvester/venv/bin"
ExecStart=/var/www/domainharvester/venv/bin/gunicorn app:app -k uvicorn.workers.UvicornWorker --workers 3 --bind 0.0.0.0:8000

Restart=always

[Install]
WantedBy=multi-user.target
```

Save and enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable domainharvester
sudo systemctl start domainharvester
```

---

🌐 8. Configure Nginx Reverse Proxy
`sudo nano /etc/nginx/sites-available/domainharvester`

Paste:
```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/domainharvester/frontend/;
    }
}
```

Enable it:
```bash
sudo ln -s /etc/nginx/sites-available/domainharvester /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

🔐 9. Enable HTTPS (FREE)
Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx -y
```

Run:
```bash
sudo certbot --nginx -d YOUR_DOMAIN
```

---

⏱️ 10. 24-Hour Auto-Run Scraper
Built inside your FastAPI backend:
```python
scheduler.add_job(scheduled_scrape, "interval", hours=24)
scheduler.start()
```

---

📤 11. Sync Changes & Restart
After making updates to your code:
1. Commit and push changes to your private GitHub repo.
2. On the VPS, pull the latest changes:
   ```bash
   cd /var/www/domainharvester
   git pull origin main
   ```
3. Restart services:
   ```bash
   sudo systemctl restart domainharvester
   sudo systemctl restart nginx
   ```

---

🧪 12. Verify Everything
Check status: `sudo systemctl status domainharvester`
Check logs: `journalctl -u domainharvester -f`
