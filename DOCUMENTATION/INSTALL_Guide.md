🚀 Installation Guide
✅ Requirements

Docker >= 24.0
Docker Compose >= 2.20
Linux server (Ubuntu/Debian recommended – Alpine is possible but tricky due to strict permissions)

Domain already pointing to the server (A record to server IP)

📂 Step 1: Clone or copy project
git clone <your-private-repo>
cd pricing_project

If not using Git, upload the folder via scp or another method.
⚙️ Step 2: Configure .env file

All environment variables are set in .env
Important: .env must be configured before the first installation.
If you change values like DB_USER, DB_PASSWORD, DB_NAME later, existing databases will become unusable unless you reset them.
Example:

DB_NAME=preismatrix_data
DB_USER=preismatrix_user
DB_PASSWORD=xxxxxxx
DB_HOST=postgres
DB_PORT=5432

MB_DB_NAME=metabase_data
MB_DB_USER=metabase_user
MB_DB_PASSWORD=xxxxxxx
MB_DB_HOST=metabase-postgres
MB_DB_PORT=5432

SCRAPER_SCHEDULE=7
DOMAIN=preismatrix.dare-gmbh.de
LETSENCRYPT_EMAIL=info@dare-gmbh.de

▶️ Step 3: Start services
docker compose up -d


This will start:
Postgres (main) – stores scraper data
Metabase Postgres – internal DB for Metabase
Orchestrator – runs scrapers (manually or via scheduler)
Scheduler – manages cron jobs for scrapers
API – exposes data from scraper DB
Metabase – analytics UI
Traefik – reverse proxy, SSL via Let’s Encrypt


⚠️ Two installation modes
🔥 Full reset (clean install – will erase all data)
docker compose down -v
docker volume rm pricing_pgdata pricing_metabase_pgdata
docker compose up -d --build


Use this if installing from zero.
This will delete all existing databases and Metabase accounts.

✅ Safe restart (recommended)
docker compose down
docker compose up -d


Keeps existing databases intact.
Use this for updates, migrations, or config changes.

🔑 First login
Metabase → https://DOMAIN
API → https://DOMAIN/api-matrix (BasicAuth protected)
First Metabase login: will ask to create an admin account.