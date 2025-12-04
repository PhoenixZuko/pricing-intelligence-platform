

# License & Usage Notice

This repository is published under the Apache License 2.0, strictly for technical review, portfolio purposes, and demonstration of engineering capability.

Commercial use, resale, redistribution, or integration of this code into a production system is not permitted unless explicitly agreed in writing.

Parts of this project were originally designed for a client-specific environment.
All sensitive data, credentials, and proprietary logic have been removed or replaced with neutral examples.
If you wish to use any component of this code in a commercial or client project, please contact me directly to discuss licensing and permissions.




Note:
This repository contains a generalized and cleaned version of a production scraping/data extraction
system originally developed for a commercial environment. All sensitive data, client-specific details,
and private logic have been removed. The project is presented strictly as a technical reference.


Architecture Summary

The orchestrator container provides the full execution environment for the entire extraction system (dependencies, Python runtime, scheduler, network access, database connectivity).
However, it does not contain any scraper logic inside the image.

Instead, the orchestrator executes the scraper scripts directly from the local repository files.
This design ensures that:
updating or fixing any scraper requires only editing the Python files,
no Docker rebuild is necessary after code changes,
deployment and maintenance remain fast and predictable,
development and production always run on the same codebase.
In short, the container supplies the environment, while the actual logic stays fully editable outside the image.


Main Components
Automated scraping modules (scheduled, containerized)
Python orchestration layer (runner.py)
PostgreSQL main database + Metabase internal DB
Metabase dashboards (pricing insights)
Traefik reverse proxy with SSL and Basic Auth
Full Dev Mode version (non-Docker) for development & debugging
Full project documentation inside DOCUMENTATION/


Demo Videos

A set of demo videos is provided for completeness.
These videos were originally prepared for client updates during development and serve as non-technical overviews of the system.
They are intended for presentation purposes only and do not replace the actual technical documentation.


https://www.youtube.com/watch?v=ijqTALUnk1k Milestone 1
https://www.youtube.com/watch?v=iBuDspQvl5s Milestone 2
https://www.youtube.com/watch?v=RJLspqNEm1U Milestone 3
https://www.youtube.com/watch?v=_Zp7e7ik51w Milestone 4

For reference, this project was originally delivered through Upwork:
https://www.upwork.com/freelancers/~01207dc9df982f92c4?p=1955092061314666496  (public portfolio link)


# Pricing Data Platform – First Steps

Welcome!  
This document explains the very first steps after cloning the repository and setting up the environment.

---


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


## 1. Clone the Repository

```bash
git clone https://github.com/PhoenixZuko/pricing-intelligence-platform
cd pricing-intelligence-platform


2. Configure Environment

After cloning, you must configure the environment variables:

a. Copy the example file:

     cp .env.example .env

b. Open .env and adjust the following values:
Database Settings
   Set usernames and passwords for both:
   Scrapers database (preismatrix_data)
   Metabase internal database (metabase_data)

Scheduler
   Configure the scraping frequency:
      SCRAPER_SCHEDULE=7 → run every 7 days
      SCRAPER_SCHEDULE=10 → run every 10 days
      SCRAPER_SCHEDULE=30 → run every 30 days

Traefik / SSL / Domain
Set your domain and contact email for SSL via Let’s Encrypt.

3. Configure Traefik Basic Auth (Access Password)
   Generate a new password hash (replace NewPassword with your password):

  Run:
   docker run --rm httpd:2.4 htpasswd -nbB admin NewPassword
   Copy the generated line (e.g. admin:$2y$05$...).

 Open:
   traefik/traefik_dynamic.yml

  Replace the existing line with your new hash:
     - "admin:$2y$05$R2.X3SxsS4n3yBf/ZsFaFuMVdRArspbY8nuqUsfs2lBA5LKQzY3.O"

   Restart Traefik:
     docker compose restart traefik

Note: Do not store the password hash in .env, because Docker Compose interprets $ characters.
 ### 🔒 Important Security Note
       Based on experience and testing, we found that the `$` symbol inside passwords is interpreted by Docker Compose as the  beginning of an environment variable.  
       This behavior can cause issues when reading passwords and may break the system.  
       To avoid such problems and as an additional security measure, we decided **not to store password hashes inside `.    env`**.  
       Instead, they are managed directly in `traefik_dynamic.yml`.

4. Start the System

Once everything is configured, start the platform with:

     docker compose up -d


 5. Access the Services
     Platform Domain: https://your-domain.com
     Metabase UI: https://your-domain.com/metabase
     API: https://your-domain.com/api-matrix

Summary
Copy .env.example → .env
Set database credentials
Configure scheduler
Adjust Traefik (domain, SSL, Basic Auth)
Start with docker compose up -d
You are now ready to use the Pricing Data Platform

---




## 6. Documentation

For more details, please check the `DOCUMENTATION` folder in this repository.  
It contains additional guides, usage notes, and explanations.  

You will also find a file named `PricingScraper-DevMode.zip`.  
This archive includes the **full documentation for running all scripts without Docker**, including:
- Full dependency list
- Installation steps
- Script execution order
- Complete data flow description

---


## 7. Development Notes

- **Modifications & New Functions**  
  Any new functionality or configuration changes should be made directly in:


runner.py
This file is the main entry point that orchestrates all other scripts.
- **Direct Script Access**  
Even though the system is dockerized, all programs are accessible in their respective folders.  
`runner.py` reads them directly from the repository structure, which makes development and debugging straightforward.

---

## Next Steps

1. For **basic setup and first run**, follow the steps in this README.  
2. For **advanced configurations and development**, consult:
 - The `DOCUMENTATION` folder  
 - `PricingScraper-DevMode.zip` for the complete standalone (non-Docker) flow
