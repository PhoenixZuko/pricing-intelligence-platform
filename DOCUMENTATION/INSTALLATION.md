# Installation Requirements

Before running the project, make sure your server has:

- **Docker** version >= 20.10  
- **Docker Compose** version >= 2.5  
- Linux server (Ubuntu/Debian recommended, Alpine also works but requires stricter permissions)

Check versions with:
```bash
docker --version
docker compose version


Environment Configuration (.env)
The .env file configures all services.
It contains 4 sections:

1. Scrapers Database (PostgreSQL)

Stores extracted data.
DB_NAME=preismatrix_data
DB_USER=preismatrix_user
DB_PASSWORD=********
DB_HOST=postgres
DB_PORT=5432


DB_NAME → name of the main database
DB_USER / DB_PASSWORD → login credentials for scrapers database
DB_HOST / DB_PORT → must match the Docker service postgres


2. Metabase Internal Database
Metabase uses its own database to store settings, dashboards, and accounts.

MB_DB_NAME=metabase_data
MB_DB_USER=metabase_user
MB_DB_PASSWORD=********
MB_DB_HOST=postgres
MB_DB_PORT=5432

Separate from scrapers’ DB for stability and isolation
MB_DB_USER and MB_DB_PASSWORD should be different from scrapers’ user


3. Orchestrator & Scheduler
Defines how often the scrapers run automatically.

# SCRAPER_SCHEDULE=7  <-- every 7 days
# SCRAPER_SCHEDULE=10 <-- every 10 days
SCRAPER_SCHEDULE=7
Value is number of days
Example: SCRAPER_SCHEDULE=7 → runs every 7 days at 2AM


4. Traefik / SSL / Domain
Settings for HTTPS and reverse proxy.
DOMAIN=preismatrix.dare-gmbh.de
LETSENCRYPT_EMAIL=info@dare-gmbh.de


DOMAIN → public domain of the project
LETSENCRYPT_EMAIL → email used for SSL certificate renewal

 With these 4 sections you configure:

Scrapers database
Metabase dashboards
Automation schedule
Secure HTTPS domain



# ⚠️ Important: About the `.env` file

- The `.env` file contains **all critical settings** (databases, API, Metabase, scheduler, domain).  
- These values are **read by all services** when containers start.  
  - Example: the Flask API and the Orchestrator connect to PostgreSQL using credentials from `.env`.  
  - Metabase also stores its users and dashboards in its own database, defined in `.env`.  

---
## When to edit `.env`?

- ✅ Set values **once at installation**, when the system is deployed from zero.  
- ❌ Avoid editing `.env` after the system is already running, unless you know exactly what you are doing.  

---

## What happens if you change `.env` later?

- **Database settings** → If you change `DB_NAME`, `DB_USER`, or `DB_PASSWORD`, the system will no longer connect to the old database. A new empty database will be created, and all existing data will be lost.  
- **Metabase database settings** → Changing these will reset Metabase completely. All users, dashboards, and settings will be lost.  
- **API / Orchestrator** → Will fail to connect if database credentials do not match.  

---

✅ **Best practice**: Configure `.env` only at the beginning (fresh install).  
If you really need to change credentials later, you must **backup databases**, update `.env`, and then restore data manually.  




# Installation Scenarios

The project can be installed in two different ways, depending on whether you want to keep or reset the databases.

---

## 1. Fresh Install (reset everything)   ⚠️ WARNING – Fresh Install 

# ⚠️ WARNING – Fresh Install

- This method **deletes all existing data**.  
- Both PostgreSQL and Metabase databases will be erased.  
- Metabase will restart with **no users and no dashboards**.  
- Use only if you want to reset the system completely.  

Command:
```bash
docker compose down -v
docker compose up -d



2. Re-Deploy with existing databases  RECOMMENDED – Safe Restart / Update

RECOMMENDED – Safe Restart / Update
Keeps all existing databases and user accounts.
Suitable for:
Moving the project folder
Restarting services
Small updates or fixes
Data in PostgreSQL and Metabase will remain untouched.
If you already have PostgreSQL and Metabase databases with data you want to keep,
make sure not to delete volumes (-v option).

# Stop services (containers only, keep volumes!)
docker compose down

# Restart with existing data
docker compose up -d


This way:

Scrapers will continue writing to the same PostgreSQL database.
Metabase will keep all users, dashboards, and settings.
Only the application code and containers are refreshed.




# 🔑 Changing Traefik Password (BasicAuth)

Traefik uses **BasicAuth** for protecting the API.  
The credentials are defined in `traefik/traefik_dynamic.yml`.

Go to Pricing/traefik  traefik_dynamic.yml

Example config:
```yaml
http:
  middlewares:
    api-auth:
      basicAuth:
        users:
          - "admin:$apr1$x856PDmm$2urvGvU1aKjkBbJYqCgH2."


1. Generate a new password hash
On Linux or Mac:

htpasswd -nb admin NewStrongPassword

Example output:
admin:$apr1$GfT9xH6h$kDmvPzvUXr4jshsmEY5Hf0

2. Replace the password in traefik/traefik_dynamic.yml
Update the users line with the new hash.

3. Restart Traefik
docker compose restart traefik








Useful Commands Cheat Sheet
🐳 Docker Basics
# Start all services in background
docker compose up -d

# Stop services
docker compose down

# Stop and remove containers + volumes (⚠️ this deletes databases!)
docker compose down -v

📦 Logs & Debugging
# View logs for all containers
docker compose logs -f

# View logs for a specific service
docker compose logs -f api
docker compose logs -f orchestrator
docker compose logs -f traefik

🛠️ Exec into Containers
# Access orchestrator container
docker compose exec orchestrator bash

# Access scheduler container
docker compose exec scheduler bash

# Access main Postgres database
docker compose exec postgres psql -U preismatrix_user -d preismatrix_data

# Access Metabase database
docker compose exec metabase-postgres psql -U metabase_user -d metabase_data

📅 Scheduler / Crontab
# Show scheduled jobs
docker compose exec scheduler crontab -l


# Run the scraper manually
docker compose run --rm orchestrator python3 runner.py

🔒 Security (Traefik BasicAuth)
# Generate a new BasicAuth password hash (replace 'newpassword')
docker run --rm httpd:2.4 htpasswd -nb admin newpassword


Copy the output and update traefik_dynamic.yml under:

api-auth:
  basicAuth:
    users:
      - "admin:<HASH>"

💾 Volumes (Databases)
# List all volumes
docker volume ls

# Inspect where a volume is stored
docker volume inspect pricing_pgdata
docker volume inspect pricing_metabase_pgdata

# Backup a volume manually
docker run --rm -v pricing_pgdata:/data -v $(pwd):/backup busybox tar czf /backup/pgdata.tar.gz /data

🌍 Certificates & Traefik
# Check Let's Encrypt certificates
docker compose logs traefik | grep acme

# Force Traefik to reload/renew certificates
docker compose restart traefik






