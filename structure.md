domain-harvester/
│
├── backend/
│   ├── app.py              # Main FastAPI backend with scheduler
│   ├── modules/            # Scraper modules
│   │   ├── commoncrawl.py
│   │   ├── opencorporates.py
│   │   ├── certscan.py
│   │   ├── classifier.py
│   │   └── validator.py
│   ├── utils/
│   │   ├── export_txt.py
│   │   ├── export_md.py
│   │   ├── export_csv.py
│   │   └── export_json.py
│   ├── db.py               # SQLite DB connection
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── output/                 # Exported domain files
└── README.md