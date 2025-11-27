# ==============================================
# 📌 Common Commands Cheat Sheet
# ==============================================

# ==============================================
# 🚀 Start / Stop Services
# ==============================================
# Start all services
docker compose up -d

# Stop all services (keep data)
docker compose down

# Stop and remove everything (⚠️ deletes databases!)
docker compose down -v

# ==============================================
# 📜 Logs & Monitoring
# ==============================================
# View logs for all services
docker compose logs -f

# View logs for one service (example: API)
docker compose logs -f api

# ==============================================
# 🛠️ Access Containers
# ==============================================
# Access orchestrator
docker compose exec orchestrator bash

# Access scheduler
docker compose exec scheduler bash

# Access main database
docker compose exec postgres psql -U preismatrix_user -d preismatrix_data

# Access Metabase database
docker compose exec metabase-postgres psql -U metabase_user -d metabase_data

# ==============================================
# 📅 Scheduler
# ==============================================
# Show scheduled jobs
docker compose exec scheduler crontab -l

# Run scraper manually
docker compose run --rm orchestrator python3 runner.py

# ==============================================
# 🔒 Change Traefik Password
# ==============================================
# 1. Generate a new password hash (replace 'NewStrongPassword')
docker run --rm httpd:2.4 htpasswd -nb admin NewStrongPassword

# Example output:
# admin:$apr1$GfT9xH6h$kDmvPzvUXr4jshsmEY5Hf0

# 2. Edit file: traefik/traefik_dynamic.yml
# Replace the line under "users:" with the new hash:
# users:
#   - "admin:<NEW_HASH>"

# 3. Restart Traefik so the new password is active
docker compose restart traefik

# ==============================================
# 📅 Change Scraper Schedule
# ==============================================
# 1. Open the .env file and find the line:
# SCRAPER_SCHEDULE=7
# → means scrapers run every 7 days at 02:00 AM

# 2. Change to desired days (examples):
# SCRAPER_SCHEDULE=10   # every 10 days
# SCRAPER_SCHEDULE=5    # every 5 days
# SCRAPER_SCHEDULE=1    # every day

# 3. Save the file and restart scheduler
docker compose restart scheduler

# 4. Verify new schedule
docker compose exec scheduler crontab -l
# Example output for SCRAPER_SCHEDULE=7:
# 0 2 */7 * * python3 /app/runner.py
# → runs every 7 days at 02:00 AM

# ==============================================
# 🔄 Restart Services
# ==============================================
# Restart all services (keep data)
docker compose restart

# Restart one service only (example: API)
docker compose restart api

# ==============================================
# 🐳 Common Docker Commands
# ==============================================
# ▶️ See running containers
docker ps

# 📋 See all containers (running + stopped)
docker ps -a

# 🔍 Inspect container details
docker inspect <container_name>

# 🛠️ Enter a container (example: scheduler)
docker compose exec scheduler bash

# ↩️ Exit container (inside)
exit   # or press Ctrl + D

# 🚮 Stop one container
docker stop <container_name>

# ▶️ Start one container again
docker start <container_name>

# 📦 List Docker volumes
docker volume ls

# 🧹 Remove unused containers/images/volumes
docker system prune -a
# ⚠️ Be careful: this deletes everything not in use

# ==============================================
# END
# ==============================================
