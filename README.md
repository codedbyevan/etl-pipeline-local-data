# 🚀 Accelerated Data Engineering Portfolio Project: Local ETL Pipeline

This repository demonstrates an end-to-end Extract, Transform, Load (ETL) pipeline using industry-standard open-source tools running entirely within a Dockerized environment.

This project was developed as a key component of an accelerated career transition into Data Engineering, showcasing foundational skills in data modeling, scalable processing (via Python/Pandas), orchestration, and containerization.

## 🎯 Architecture & Objective

The objective of this project is to reliably process simulated raw data and load it into an analytical data store using an orchestrated workflow.

### Technical Stack

| Tool | Purpose | 
 | ----- | ----- | 
| **Apache Airflow** | Workflow orchestration (scheduling, monitoring, and dependency management of ETL tasks). | 
| **PostgreSQL** | Analytical Data Warehouse (Target destination for processed data). | 
| **Python / Pandas** | Data transformation logic (cleaning, type casting, feature engineering). | 
| **Docker Compose** | Environment containerization and service management. | 

### Data Flow

1. **Extract (E)**: A Python script (simulating an API call or file read) loads mock data into a Pandas DataFrame.

2. **Transform (T)**: The Python script cleans, validates, and transforms the data (e.g., converting types, creating derived features like `pickup_hour`).

3. **Load (L)**: The script performs a bulk load using `psycopg2`'s `copy_from` command into the PostgreSQL Data Warehouse.

4. **Orchestration**: An Airflow DAG is responsible for triggering and monitoring this Python job.

## ⚙️ Prerequisites

To run this project, you must have the following installed:

1. **Docker & Docker Compose**

2. **Python 3.x** (for running the local processing script)

## 🛠️ Deployment Steps

Follow these steps to spin up the entire environment and run the data pipeline.

### Step 1: Configure Environment Variables (if applicable)

**Crucial:** Ensure the database credentials in your Python processing scripts match the credentials defined in your `docker-compose.yml` file.

| Component | Variable | Example Value | 
 | ----- | ----- | ----- | 
| `docker-compose.yml` (Postgres service) | `POSTGRES_USER` | `my_etl_user` | 
| `data_processor.py` | `DB_USER` | `my_etl_user` | 
| Airflow UI Connection (`Host`, `Login`, `Password`) | N/A | Must match `docker-compose.yml` values. | 

### Step 2: Start the Docker Services

Navigate to the project root directory and execute:
`docker-compose up -d`
This will spin up three main services: `webserver`, `scheduler`, and `postgres`. Wait a minute or two for Airflow to initialize.

### Step 3: Access Airflow and Set up the Connection

1. Open your browser to the Airflow UI (typically `http://localhost:8080`).

2. Go to **Admin** > **Connections**.

3. **Create/Edit** the connection your DAG uses (e.g., `postgres_default`). Ensure the fields are set correctly for Docker networking:

   * **Conn Type:** `Postgres`

   * **Host:** `postgres` (the Docker service name)

   * **Schema/DB:** (Your target DB, e.g., `airflow`)

   * **Login:** (Your `POSTGRES_USER` value)

   * **Password:** (Your `POSTGRES_PASSWORD` value)

   * **Port:** `5432`

### Step 4: Run the DAG

1. Navigate to the DAGs list in the Airflow UI.

2. Find the DAG (`load_taxi_zone_data_to_postgres` or similar).

3. Toggle it **ON** and manually trigger it using the "Play" button.

### Step 5: Verify Results in DBeaver

Access the data in your local PostgreSQL instance:

* **Host:** `localhost`

* **Port:** `5432` (or whatever you mapped in `docker-compose.yml`)

* **Database:** (Your target DB, e.g., `airflow`)

* **User/Password:** (Your `POSTGRES_USER/PASSWORD`)

The table (`taxi_zones` or `processed_taxi_trips` depending on the script) should now be populated with the processed records.

## 💡 Key Takeaways Demonstrated

* **Idempotent Table Management:** The pipeline uses `CREATE TABLE IF NOT EXISTS` to ensure it can be run multiple times without failure.

* **Efficient Loading:** Uses `psycopg2`'s `COPY FROM` command for high-speed bulk data insertion, avoiding slow row-by-row `INSERT` statements.

* **Containerization:** The entire dependency stack is managed and isolated using Docker, ensuring portability.
