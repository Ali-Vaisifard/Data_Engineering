# Setting up the Python Pipeline Project

Follow these steps to set up and run the Python pipeline project.

## 1. Create the Python Script

Create a file named `pipeline.py`.

```bash
touch pipeline.py
```

## 2. Navigate to the Project Folder

Change your directory to the `pipeline` folder.

```bash
cd pipeline
```

## 3. Install `uv` (Virtual Environment Manager)

`uv` is a tool that helps manage Python virtual environments.

```bash
pip install uv
```

## 4. Initialize the Virtual Environment

Create a virtual environment with Python 3.13.

```bash
uv init --python 3.13
```

## 5. Verify Python Installation

Check which version of Python is active.

```bash
which python
python -V
```

## 6. Run Python Command in Virtual Environment

Use `uv` to execute the Python command inside the virtual environment.

```bash
uv run python -V
uv run which python
```

## 7. Install Required Libraries

Add the `pandas` library to the virtual environment.

```bash
uv add pandas
```

## 8. Select Python Interpreter in IDE

In your code editor (e.g., VSCode), select the correct Python interpreter. It should be located at:

```text
pipeline/.venv/bin/python
```

Make sure to select this path for the virtual environment interpreter.

## 9. Run the Pipeline Script

Execute the `pipeline.py` script with an argument (e.g., `12`).

```bash
uv run python pipeline.py 12
```

## 10. Add `.parquet` Files to `.gitignore`

To avoid committing large or unnecessary `.parquet` files to Git, add the following to your `.gitignore` file:

```gitignore
*.parquet
```

## 11. Commit Changes to Git

After making changes, use Git to track and commit your changes.

```bash
git status
```

If changes are shown, add them to the staging area:

```bash
git add .
```

Then, commit the changes:

```bash
git commit -m 'Add pipeline setup and script'
```

Your status should look like this:

```text
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   .gitignore
        modified:   README.md
        new file:   pipeline/.python-version
        new file:   pipeline/README.md
        new file:   pipeline/main.py
        new file:   pipeline/pipeline.py
        new file:   pipeline/pyproject.toml
        new file:   pipeline/uv.lock
```

Push the changes to the remote repository:

```bash
git push origin main
```

After pushing, the changes will be uploaded to the online repository.

## 12. Prepare for Docker Deployment

Once the pipeline script is ready, the next step is to package the project into a Docker image so it can run in a reproducible environment.

### a. Create a Dockerfile

Inside the `pipeline` folder, create a file named `Dockerfile` and add the following code:

```dockerfile
FROM python:3.13

RUN pip install pandas pyarrow

WORKDIR /code

COPY pipeline.py .
```

This Dockerfile:

- Uses Python 3.13 as the base image
- Installs required dependencies (`pandas` and `pyarrow`)
- Sets the working directory to `/code`
- Copies the pipeline script into the container

### b. Build the Docker Image

From the project directory, build the Docker image:

```bash
docker build -t test:pandas .
```

This command creates a Docker image named `test:pandas`.

### c. Run the Container (Interactive Mode)

You can start the container with a bash shell for testing:

```bash
docker run -it --entrypoint=bash --rm test:pandas
```

Explanation:

- `-it` → interactive terminal
- `--entrypoint=bash` → opens a bash shell inside the container
- `--rm` → removes the container automatically when it stops

This is **VERY important**:

- `--rm` → deletes container when stopped
- You lose everything tied to it

The `--rm` flag is useful for temporary runs because it prevents stopped containers from accumulating on your system.

Inside the container, you can test the script:

```bash
ls
python pipeline.py 12
```

### d. Automate Execution with ENTRYPOINT

To avoid manually running the Python command every time, add an `ENTRYPOINT` to the Dockerfile.

Update the Dockerfile:

```dockerfile
FROM python:3.13

RUN pip install pandas pyarrow

WORKDIR /code

COPY pipeline.py .

ENTRYPOINT ["python","pipeline.py"]
```

Now the container will automatically execute the pipeline script when it starts.

### e. Run the Pipeline

Run the container and pass the month argument:

```bash
docker run -it --rm -v "$(pwd):/code" test:pandas 12
```

Explanation:

- `-v "$(pwd):/code"` mounts the current directory into the container
- This allows output files (such as `.parquet`) to be written to your local machine

### f. Managing Dependencies with `uv`

To make dependency management reproducible, you can use `uv` together with `pyproject.toml` and `uv.lock`.

Add the following lines to the Dockerfile:

```dockerfile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

COPY pyproject.toml .python-version uv.lock ./

RUN uv sync --locked
```

This ensures the container installs the exact dependency versions defined in your lock file.

### g. Running Python with `uv`

You can modify the entrypoint to use `uv`:

```dockerfile
ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
```

Alternatively, activate the virtual environment by adding:

```dockerfile
ENV PATH="/code/.venv/bin:$PATH"
```

Then the entrypoint can remain:

```dockerfile
ENTRYPOINT ["python","pipeline.py"]
```

### h. Rebuild and Run the Container

After updating the Dockerfile, rebuild the image:

```bash
docker build -t test:pandas .
```

Run the pipeline:

```bash
docker run -it --rm -v "$(pwd):/code" test:pandas 12
```

The pipeline will execute and create the output file (e.g., `output_12.parquet`) in your local directory.

At the end the final Dockerfile must look like:

```dockerfile
FROM python:3.13

RUN pip install pandas pyarrow

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./

COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]
```

## 13. Running PostgreSQL from Docker

You can run a containerized version of PostgreSQL without installation. You only need to create environment variables and a volume to store it.

### a. Running Postgres in a Container

Create a folder anywhere for saving data in Postgres. We will use the folder `ny_taxi_DB`.

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_DB:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:18
```

- `-e` sets environment variables (user, password, database name)
- `-v ny_taxi_postgres_data:/var/lib/postgresql/data` creates a named volume
  - Docker manages this volume automatically
  - Data persists even after container is removed
  - Volume is stored in Docker's internal storage
- `-p 5432:5432` maps port `5432` from container to host
- `postgres:18` uses PostgreSQL version 18

Another way (bind mount):

```bash
mkdir ny_taxi_DB

docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_DB:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:18
```

In this way, first you create the directory and it is owned by the user. If Docker is doing it, it will be created and owned by the Docker root user and may cause permission issues on Linux.

- Named volume: `name:/path`
- Bind mount: `/host/path:/container/path`

### b. Connecting to PostgreSQL

Install `pgcli`:

```bash
uv add --dev pgcli
```

`--dev` flag marks this as a development dependency. You may check it in the `pyproject.toml` file in the dependency-group section.

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

Now after entering your password, try to run some queries:

List of tables:

```sql
\dt
```

Create a table:

```sql
CREATE TABLE test (id INTEGER, name VARCHAR(50));
```

Insert data:

```sql
INSERT INTO test VALUES (1, 'Hello Docker');
```

Query data:

```sql
SELECT * FROM test;
```

Exit:

```sql
\q
```

## 14. Importing Data to PostgreSQL (Data Ingestion)

### a. Create a Jupyter Notebook file

We will use it to read a CSV file and export it to Postgres.

Install Jupyter:

```bash
uv add --dev jupyter
```

Then run Jupyter notebook:

```bash
uv run jupyter notebook
```

Now create a new notebook and run the following code.

The data can be ingested from any data sources in different formats.

#### Parquet

```python
import pandas as pd

# read a sample of the data
prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data/)'
url = f'{prefix}/yellow_tripdata_2025-01.parquet'

df = pd.read_parquet(url)

# Display the first rows
df.head()

# Display the datatypes
df.dtypes

# Check data shape
df.shape
```

#### CSV

```python
import pandas as pd

# read a sample of the data
prefix = 'your address prefix'
url = f'{prefix}/file_name.csv'

df = pd.read_csv(url)

df.head()
df.dtypes
df.shape
```

In case you have any problems in the data types, you may run this code:

```python
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)
```

### Data Ingestion into PostgreSQL

In the notebook we follow these steps:

1. Download the dataset (CSV or Parquet)
2. Read it in chunks with pandas
3. Convert the datatypes if it is necessary (Data transformation)
4. Create an engine to connect Postgres and Jupyter using SQLAlchemy
5. Insert data into PostgreSQL

Install SQLAlchemy:

```bash
uv add sqlalchemy "psycopg[binary,pool]"
uv add psycopg-binary
```

In the notebook create the engine:

```python
from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')
```

Get the schema:

```python
print(pd.io.sql.get_schema(df, name='yellow_taxi_data'))
```

Explanation: `pd.io.sql.get_schema(...)`

This function:

- Looks at the DataFrame structure
- Converts it into a SQL table schema
- It does **NOT** create the table
- It just returns the SQL code as a string

Output:

```sql
CREATE TABLE "yellow_taxi_data" (
"VendorID" INTEGER,
  "tpep_pickup_datetime" TIMESTAMP,
  "tpep_dropoff_datetime" TIMESTAMP,
  "passenger_count" REAL,
  "trip_distance" REAL,
  "RatecodeID" REAL,
  "store_and_fwd_flag" TEXT,
  "PULocationID" INTEGER,
  "DOLocationID" INTEGER,
  "payment_type" INTEGER,
  "fare_amount" REAL,
  "extra" REAL,
  "mta_tax" REAL,
  "tip_amount" REAL,
  "tolls_amount" REAL,
  "improvement_surcharge" REAL,
  "total_amount" REAL,
  "congestion_surcharge" REAL,
  "Airport_fee" REAL,
  "cbd_congestion_fee" REAL
)
```

Create the table:

```python
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
```

Explanation:

- It creates an empty SQL table in your database
- The table structure matches your DataFrame (`df`)
- No data is inserted
- `df.head(0)` → empty DataFrame (only columns)
- `.to_sql(...)` → creates table
- `'replace'` → drops old table + recreates
- Result → empty table with correct schema

Then code this:

```python
import urllib.request
import pyarrow.parquet as pq

# download the parquet file locally
urllib.request.urlretrieve(url, "yellow_tripdata_2025-01.parquet")

pq_file = pq.ParquetFile("yellow_tripdata_2025-01.parquet")

for batch in pq_file.iter_batches(batch_size=100000):
    df_chunk = batch.to_pandas()
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append', index=False)
    print(len(df_chunk))
```

Explanation:

- Reads chunk by chunk
- Memory efficient
- Scalable
- Used in real pipelines

```python
pd.read_sql("SELECT COUNT(*) FROM yellow_taxi_data", con=engine)
```
