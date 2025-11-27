# System Architecture

## Overview
The system is fully containerized using **Docker Compose**.  
It consists of **7 services** organized into independent containers, with **two separate PostgreSQL databases** (one for scrapers, one for Metabase).  
The architecture is designed for **easy modification and scalability** – code files remain accessible locally, while execution runs inside containers.

---

## Components

### 1. **Postgres (Scrapers DB)**
- Stores data collected by the scrapers.  
- Accessible internally by the Orchestrator, Scheduler, and API.  
- Data is persisted via Docker volume: `pricing_pgdata`.

---

### 2. **Metabase Postgres**
- Dedicated database for Metabase’s internal configuration.  
- Keeps dashboards, user accounts, queries.  
- Independent from scrapers DB.  
- Data is persisted via Docker volume: `pricing_metabase_pgdata`.

---

### 3. **Orchestrator**
- Container that manages the execution of scrapers.  
- Runs manually or via Scheduler.  
- Mounted with local project files → any scraper code changes apply instantly without rebuilding the container.

---

### 4. **Scheduler**
- Runs cron jobs.  
- Executes orchestrator tasks according to `SCRAPER_SCHEDULE` from `.env`.  
- Example: run scrapers every 7 days.  
- Can also trigger orchestrator manually.

---

### 5. **API (Flask)**
- Flask REST API exposing collected data.  
- Accessible externally via Traefik at:  
  - `https://<DOMAIN>/api` (or custom path, e.g. `/api-matrix`)  
- Protected via BasicAuth middleware.  
- Reads directly from Scrapers Postgres.

---

### 6. **Metabase**
- Business Intelligence tool for dashboards and visualizations.  
- Uses dedicated Postgres DB for configuration.  
- Exposed externally via Traefik at:  
  - `https://<DOMAIN>/`  
- Users log in with configured credentials.

---

### 7. **Traefik**
- Reverse proxy handling routing and SSL termination.  
- Routes requests to Metabase and API based on path rules.  
- Automatically manages Let’s Encrypt certificates via ACME.  
- Configured with `traefik_dynamic.yml`.

---

## Networking
- All services run inside the same Docker network: `traefik-net`.  
- Internal communication is isolated.  
- External access only via **Traefik** (HTTPS).  

---

## Volumes & Persistence
- **`pricing_pgdata`** → scraper data (Postgres)  
- **`pricing_metabase_pgdata`** → Metabase data  
- Volumes ensure data persists even if containers are removed.  

---

## Key Advantages
1. **Separation of concerns** → scrapers DB vs Metabase DB.  
2. **Full containerization** → services isolated but integrated.  
3. **Hot code changes** → scraper/API code runs from local folder inside Docker, no rebuild needed.  
4. **Security** → API protected via BasicAuth, HTTPS enforced with Let’s Encrypt.  
5. **Scalability** → easy to add scrapers, APIs, or dashboards.  


# System Summary

The system is composed of **8 Dockerized services**, all running under `docker compose`:

- **Postgres** → database for scrapers data  
- **Metabase Postgres** → database for Metabase configuration  
- **Orchestrator** → central engine that sustains and runs the project  
- **Scheduler** → executes tasks automatically via cron (runs orchestrator on schedule)  
- **API** → Flask REST API exposing collected data  
- **Metabase** → dashboards and visualizations  
- **Traefik** → reverse proxy with HTTPS + routing  
- **Network** → isolated bridge `traefik-net` connecting everything  

---

## How it works
- **Orchestrator** is the **core service**: it supports and runs the project logic.  
- At its base, it executes `runner.py`, which **reads each scraper directly from the project files** and executes them inside Docker.  
- This approach ensures **easy modifications**: any change to a scraper file is instantly available without rebuilding containers.  

---

## Documentation
For the complete flow explanation of each program, see the **`PricingScraper-DevMode`** documentation file.  
There you will find a detailed breakdown of the full pipeline and how all components interact.
