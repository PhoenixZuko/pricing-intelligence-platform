⏱ Change scraper schedule

The scraper schedule is defined in the .env file using the variable:

SCRAPER_SCHEDULE=7   # every 7 days
Example changes:
Run daily:

SCRAPER_SCHEDULE=1

Run every 30 days:
SCRAPER_SCHEDULE=30

Apply changes:
After modifying .env, restart the containers:

docker compose down
docker compose up -d

Verify new schedule:
Check inside the scheduler:

docker compose exec scheduler bash
crontab -l

Example for daily:
0 2 */1 * * docker exec pricing-orchestrator-1 python3 /app/runner.py >> /var/log/cron.log 2>&1

Example for every 30 days:
0 2 */30 * * docker exec pricing-orchestrator-1 python3 /app/runner.py >> /var/log/cron.log 2>&1




Orchestrator execution (runner.py)
Once the orchestrator starts (runner.py), it is important to let it finish the entire process.
What happens during execution:
Reads and runs all extractors one by one.
Saves raw data temporarily.
Formats results, assigns categories and subcategories
Writes the processed data into the PostgreSQL database.

Cleans up:
Deletes old archives.
Keeps only the last processed file.
Removes any files older than 7 days to keep storage clean.

Duration
A full run usually takes 14–17 minutes.
Important
❌ Do not stop the orchestrator while it is running.
✅ Always allow the process to complete for correct functionality and a clean database.

