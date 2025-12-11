 PROJECT: PRICING DATA PLATFORM
 Author: Andrei Sorin Ștefan
```bash

Pricing-Project/
├── docker-compose.yml          # Main Docker Compose file: defines all services (DBs, API, Orchestrator, Scheduler, Metabase, Traefik)
├── requirements.txt            # Common Python dependencies
├── runner.py                   # Entry point for Orchestrator; executes scrapers
│
├── DOCUMENTATION/              # Documentation and guides
│   ├── ARCHITECTURE.md         # Detailed architecture explanation
│   ├── Change_scraper_schedule.md # How to change the cron schedule for scrapers
│   ├── DEV_MODE.md             # Instructions for running project in Dev Mode (no Docker)
│   ├── INSTALLATION.md         # Installation instructions
│   ├── INSTALL_Guide.md        # Additional setup guide
│   ├── PricingScraper-DevMode.zip # Full Dev Mode package (non-dockerized version)
│   ├── README.md               # Documentation overview
│   ├── USAGE.md                # How to use the system
│   └── VIDEO_GUIDE.md          # Script/guide for client presentation video
│
├── Scrapers/                   # Data extraction scripts (scrapers)
│   ├── 1cdz-scraper.py         # Individual scraper for source 1 (example: cdz)
│   ├── 2dino-scraper.py        # Scraper for source 2
│   ├── 3klebs-scraper.py       # Scraper for source 3
│   ├── 4main_clearago.py       # Scraper for source 4 (Clearago)
│   ├── 5main_entsorgo.py       # Scraper for source 5 (Entsorgo)
│   ├── core_clearago/          # Core scraping logic specific to Clearago
│   ├── core_ensorgo/           # Core scraping logic specific to Entsorgo
│   ├── cvs_maker.py            # Utility to export results to CSV
│   ├── json_maker.py           # Utility to export results to JSON
│   └── README.md               # Notes and usage for scrapers
│
├── archive/                    # Archived results of past scraper runs
│   ├── results_data_07_10_2025 # Example archived dataset
│   └── results_data_08_10_2025 # Example archived dataset
│
├── category_parser/            # Category parsing module
│   ├── create_category.py      # Script to create category mappings
│   ├── create_type.py          # Script to create type mappings
│   ├── output_data_with_type.csv # Example output file with type/category
│   ├── type_definitions/       # Folder containing category/type definitions
│   └── README.md               # Notes for category parser usage
│
├── config.yaml                 # Global configuration file
│
├── database/                   # Database initialization scripts
│   ├── db_setup.py             # Script to set up database schema/tables
│   └── README.md               # Documentation for DB setup
│
├── flask_api/                  # Flask REST API service
│   ├── Dockerfile              # Docker build file for API
│   ├── app.py                  # Main Flask app (defines endpoints)
│   ├── auth.py                 # Authentication logic (BasicAuth)
│   ├── db.py                   # Database connection/queries
│   ├── requirements.txt        # API-specific dependencies
│   ├── README.md               # API usage notes
│   └── __pycache__/            # Compiled Python cache (auto-generated)
│
├── metabase/                   # Metabase container (dashboards/visualizations)
├── metabase-postgres/          # PostgreSQL DB for Metabase configuration (users, dashboards)
├── postgres/                   # PostgreSQL DB for scraper data
│   └── Dockerfile              # Docker build file for Postgres
│
├── orchestrator/               # Orchestrator service (controls scraper runs)
│   ├── Dockerfile              # Docker build file for orchestrator
│   └── requirements.txt        # Orchestrator-specific dependencies
│
├── scheduler/                  # Scheduler service (cron jobs)
│   ├── Dockerfile              # Docker build file for scheduler
│   └── entrypoint.sh           # Entrypoint script to run cron jobs
│
├── traefik/                    # Traefik reverse proxy (routing & SSL)
│   ├── traefik.yml             # Main Traefik config
│   ├── traefik_dynamic.yml     # Dynamic routing rules for API/Metabase
│   ├── acme.json               # Stores SSL certificates (Let's Encrypt)
│
└── utils/                      # Utility scripts
    ├── cleaner.py              # Script for cleaning/preprocessing data
    └── README.md               # Notes for utilities



Dockerized services (flask_api, orchestrator, scheduler, postgres, metabase, traefik).
Core logic (scrapers, orchestrator, API).
Docs + configs.


Workflow ASCII diagram
                         ┌──────────────────────────┐
                         │        Scheduler         │
                         │ - Runs cron jobs         │
                         │ - Triggers Orchestrator  │
                         └───────────┬─────────────┘
                                     │
                                     ▼
                         ┌──────────────────────────┐
                         │       Orchestrator       │
                         │ - Executes scrapers      │
                         │ - Installs dependencies  │
                         │ - Uses local scraper code│
                         └───────────┬─────────────┘
                                     │
                       writes data   │
                                     ▼
                       ┌───────────────────────────┐
                       │  PostgreSQL (Scrapers DB) │
                       │ - Stores extracted data   │
                       │ - Persistent volume       │
                       └───────────┬──────────────┘
                                   │
      ┌────────────────────────────┴──────────────────────────┐
      │                                                       │
      ▼                                                       ▼
┌─────────────────────┐                          ┌──────────────────────────┐
│        API          │                          │        Metabase          │
│ - Flask REST API    │                          │ - Dashboards & Charts    │
│ - Secure via Traefik│                          │ - Uses its own Postgres  │
│ - Serves data JSON  │                          │ - Reads Scrapers DB      │
└───────────┬─────────┘                          └───────────┬──────────────┘
            │                                              │
            │ external access                              │ external access
            ▼                                              ▼
   ┌──────────────────────────┐                 ┌──────────────────────────┐
   │         Traefik          │                 │         Traefik          │
   │ - Reverse proxy          │                 │ - SSL certificates       │
   │ - Routes /api and /      │                 │ - Secure HTTPS access    │
   └──────────────────────────┘                 └──────────────────────────┘


Note: Orchestrator Design
The Orchestrator runs inside a Docker container and comes with all scraper dependencies pre-installed.
However, it executes runner.py, which is placed at the root of the project.
Even though it runs dockerized, the Orchestrator directly reads the local scraper files mounted into the container.

✅ This means:

Scrapers can be modified instantly (no need to rebuild Docker images).
New extractors or new functions can be added easily by just dropping new files.
The system remains production-ready, but still very developer-friendly.
🔑 This makes the Orchestrator a powerful and well-designed engine: flexible, easy to extend, and easy to maintain.


# 📖 Pricing Platform – Documentation



Welcome! This folder contains all the documentation needed to **install, configure, and use** the Pricing Platform.  

Use this README as an index and quick start guide.



---



## 📂 Documentation Contents



- **INSTALLATION.md** → Full step-by-step installation guide (fresh install or safe restart).  
- **INSTALL_Guide.md** → Quick setup guide for developers.  
- **USAGE.md** → How to use the system after installation (common commands, daily operations).  
- **Change_scraper_schedule.md** → How to change how often scrapers run (scheduler configuration).  
- **ARCHITECTURE.md** → System architecture and technical overview.  
- **VIDEO_GUIDE.md** → (optional) Placeholder for a video tutorial.  
- **README.md** → This file, overview of documentation.  



---



## 🚀 Quick Start



```bash

# 1. Requirements

# - Docker >= 20.10

# - Docker Compose >= 2.5

# - Linux server (Ubuntu/Debian recommended)



# 2. Setup Environment

# Copy `.env.example` → rename to `.env`

# Configure databases, domain, schedule inside `.env`



# 3. Start / Stop Services

## Start all services (in background)
docker compose up -d

## Stop all services (keep data)
docker compose down

## Stop and remove everything (⚠️ deletes databases!)
docker compose down -v




# 4. Access the Platform

https://<your-domain>



---





 ⚙️ Daily Operations



# Restart all services
docker compose restart



# Check logs (all services)

docker compose logs -f



# Enter scheduler container

docker compose exec scheduler bash



For a full list of useful commands, see USAGE.md.





🔒 Security



# Generate a new Traefik password hash
docker run --rm httpd:2.4 htpasswd -nb admin NewStrongPassword



# Edit traefik/traefik_dynamic.yml and update the hash

# Then restart Traefik
docker compose restart traefik





📅 Scheduler



# Default: runs every 7 days at 2 AM

# To change frequency: edit `.env`

SCRAPER_SCHEDULE=<days>



# After updating restart the scheduler

docker compose restart scheduler



# Verify the new schedule

docker compose exec scheduler crontab -l



💾 Backups



# List volumes

docker volume ls



# Backup main PostgreSQL database

docker run --rm -v pricing_pgdata:/data -v $(pwd):/backup busybox tar czf /backup/pgdata.tar.gz /data





Architecture

The system includes:
Scrapers (data extraction)
Orchestrator & Scheduler (automation)
PostgreSQL databases (scrapers + Metabase)
Metabase (dashboards and analytics)
Traefik (reverse proxy & SSL)

For detailed diagrams and explanations, see ARCHITECTURE.md.
