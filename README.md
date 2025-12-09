

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


## Design Notes & Project Constraints

This system was designed and deployed under strict technical and operational constraints defined by the client.  
The solution had to run reliably on an **Alpine Linux server** with limited resources, without introducing external dependencies or modifying the existing environment.  
All architectural decisions were made to ensure stability, isolation, and predictable execution.

### 🔒 1. Fully Self-Contained Execution (Alpine Linux)
The platform was required to operate end-to-end using only the resources available on a lightweight **Alpine Linux** server.  
To satisfy this requirement, the system was engineered to:

- run without external cloud services or remote APIs,  
- maintain compatibility with Alpine’s minimal system libraries (musl libc),  
- avoid heavy dependencies that conflict with lightweight Linux distributions,  
- execute predictably through Cron-based orchestration and isolated runtime processes.

This approach ensures high reliability on minimal infrastructure, while preserving full control over the automation workflow.

### 👁️ 2. Transparent and Supervised Automation Behavior
The automation logic was required to mimic human interaction and remain fully observable during execution.  
As a result, the system:

- performs real-time browser actions,  
- avoids aggressive scraping techniques,  
- uses controlled scrolling, filtering, and page state monitoring,  
- logs every operational step for full traceability.  

This guarantees safe behavior aligned with platform policies and prevents disruptive automated patterns.

### ⚙️ 3. Process Isolation and Zero Interference With Host System
Since the client environment also ran multiple business applications, the solution needed to operate without risk of interference.  
To achieve this, the system includes:

- PID tracking and controlled subprocess lifecycle management,  
- clean shutdown and restart routines,  
- sandboxed Chrome profiles,  
- file-level isolation for configuration, storage, and caching.

No global system settings are modified, and all operations remain contained within the application directory.

### 💰 4. Architecture Optimized for Budget and Maintainability
The client required a production-oriented tool while avoiding DevOps overhead such as Docker, Kubernetes, cloud databases, or managed services.  
Therefore, the platform was designed as a **zero-infrastructure**, single-folder application that delivers:

- automated ETL workflow (Extract → Transform → Load),  
- configurable YAML-driven behavior,  
- a real-time dashboard served locally,  
- automated proxy validation and data processing pipelines,  
- SSH-based synchronization between Alpine and cPanel environments.

This achieves enterprise-level functionality within the constraints of a cost-efficient deployment model.

---

This design reflects a balance between technical rigor, robustness, client infrastructure limitations, and long-term maintainability.  
The system remains lightweight, transparent, and fully self-contained while supporting complex automation and data processing workflows.


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

This repository includes a set of demonstration videos created during the development process.
They were originally prepared for client communication and milestone validation.
These videos provide high-level functional overviews and visual context, but they do not replace the official technical documentation contained within the repository.

Milestone Walkthroughs

Milestone 1 — https://www.youtube.com/watch?v=ijqTALUnk1k
Milestone 2 — https://www.youtube.com/watch?v=iBuDspQvl5s
Milestone 3 — https://www.youtube.com/watch?v=RJLspqNEm1U
Milestone 4 — https://www.youtube.com/watch?v=_Zp7e7ik51w

These demonstrations outline the incremental development phases, architectural decisions, and early implementation details.

Portfolio Reference

This project was originally delivered through Upwork, and a public portfolio reference is available here:
https://www.upwork.com/freelancers/~01207dc9df982f92c4?p=1955092061314666496
---



## 1. Clone the Repository

```bash
git clone https://github.com/PhoenixZuko/pricing-intelligence-platform
cd pricing-intelligence-platform



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
