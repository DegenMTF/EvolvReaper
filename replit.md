# Domain Harvester

## Overview

Domain Harvester is a web-based domain scraping and intelligence platform. It automatically collects domain data from multiple public sources (Common Crawl, OpenCorporates, Certificate Transparency logs), classifies domains by industry using keyword matching, validates them via DNS lookups, and provides export functionality in multiple formats. The system runs a scheduled 24-hour automated scraping pipeline.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology**: Vanilla HTML/CSS/JavaScript (no framework)
- **Design**: Single-page application with sidebar navigation
- **Theming**: CSS custom properties with light/dark mode toggle
- **Sections**: Dashboard (stats), Scrape (trigger jobs), Export (download data)
- **Serving**: Static files served directly by FastAPI

### Backend Architecture
- **Framework**: FastAPI (Python)
- **Pattern**: Modular scraper architecture with separate modules for each data source
- **Scheduling**: APScheduler running background jobs every 24 hours
- **API Design**: RESTful endpoints under `/api/` prefix

### Data Pipeline
The scraping pipeline follows this flow:
1. **Collection**: Multiple scraper modules pull domains from external sources
2. **Classification**: Keyword-based industry classification (finance, health, tech, legal)
3. **Validation**: DNS resolution checks (A and MX records)
4. **Storage**: All domains stored in SQLite with deduplication

### Scraper Modules
Located in `backend/modules/`:
- `commoncrawl.py` - Extracts domains from Common Crawl web archive indexes
- `opencorporates.py` - Pulls company domains from OpenCorporates API
- `certscan.py` - Harvests domains from Certificate Transparency logs (crt.sh)
- `classifier.py` - Assigns industry labels based on domain keywords
- `validator.py` - Validates domains have valid DNS records

### Export System
Located in `backend/utils/`:
- Supports TXT, CSV, JSON, and Markdown formats
- Exports stored to `backend/output/` directory

### Database
- **Engine**: SQLite (file-based at `backend/domains.db`)
- **Schema**: Single `domains` table with fields: id, domain (unique), country, industry, source, date_added
- **Access**: Simple connection helper in `db.py` with row factory for dict-like access

## External Dependencies

### Third-Party APIs
- **Common Crawl Index API** - Web archive domain extraction
- **OpenCorporates API** - Corporate registry data (v0.4, no auth required for basic queries)
- **crt.sh API** - Certificate Transparency log search

### Python Libraries
- `fastapi` + `uvicorn` - Web framework and ASGI server
- `apscheduler` - Background job scheduling
- `requests` + `aiohttp` - HTTP clients for API calls
- `beautifulsoup4` + `lxml` - HTML parsing
- `dnspython` - DNS validation
- `pandas` - Data manipulation
- `tqdm` - Progress bars

### Frontend Resources
- Google Fonts (Inter) - Typography via CDN