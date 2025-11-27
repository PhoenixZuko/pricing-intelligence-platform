#!/bin/bash
set -e

# Citește intervalul din variabilele de mediu (default 7 zile)
: "${SCRAPER_SCHEDULE:=7}"

mkdir -p /etc/cron.d

# Cronjob: rulează runner.py în orchestrator
echo "0 2 */${SCRAPER_SCHEDULE} * * docker exec pricing-orchestrator-1 python3 /app/runner.py >> /var/log/cron.log 2>&1" > /etc/cron.d/scraper

chmod 0644 /etc/cron.d/scraper
crontab /etc/cron.d/scraper

echo "[scheduler] rulează cu schedule: 0 2 */${SCRAPER_SCHEDULE} * *"

# pornește cron în foreground
crond -f -L /dev/stdout
