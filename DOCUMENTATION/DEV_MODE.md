## Project Versions
This project is delivered in **two versions**:

1. **Dev Mode (PricingScraper-DevMode.zip)**  
   - Can be run directly without Docker.  
   - Useful for local development, debugging, and testing scrapers individually.  
   - Run using `python runner.py` or individual scraper scripts.

2. **Production Mode (Dockerized)**  
   - Fully containerized with Docker Compose.  
   - Includes Orchestrator, Scheduler, API, Metabase, Traefik, and PostgreSQL databases.  
   - Designed for scalability, security, and persistence.


Dev Mode Version (PricingScraper-DevMode.zip)
The Dev Mode package contains:
Full documentation of all files.
Workflow explanations and diagrams.
The same project logic as the production version, but without Dockerization.
Even though it is the same project, the way it runs is different:
In Dev Mode, scrapers and the orchestrator are executed directly from Python.
Databases and services are not containerized.

✅ Why Dev Mode is useful:
It allows developers to add new extractors or perform major modifications without touching the Dockerized production setup.
It helps in achieving a better understanding of the workflow and system architecture.
It can be used as a sandbox to test new functions before integrating them into the production environment.