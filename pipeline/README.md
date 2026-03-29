Setting up the Python Pipeline Project

Follow these steps to set up and run the Python pipeline project.

1. Create the Python Script

Create a file named pipeline.py.

touch pipeline.py


2. Navigate to the Project Folder

Change your directory to the pipeline folder.

cd pipeline


3. Install uv (Virtual Environment Manager)

uv is a tool that helps manage Python virtual environments.

pip install uv


4. Initialize the Virtual Environment

Create a virtual environment with Python 3.13.

uv init --python 3.13


5. Verify Python Installation

Check which version of Python is active.

which python
python -V


6. Run Python Command in Virtual Environment

Use uv to execute the Python command inside the virtual environment.

uv run python -V
uv run which python


7. Install Required Libraries

Add the pandas library to the virtual environment.

uv add pandas


8. Select Python Interpreter in IDE

In your code editor (e.g., VSCode), select the correct Python interpreter. It should be located at:

pipeline/.venv/bin/python

Make sure to select this path for the virtual environment interpreter.


9. Run the Pipeline Script

Execute the pipeline.py script with an argument (e.g., 12).

uv run python pipeline.py 12


10. Add .parquet Files to .gitignore

To avoid committing large or unnecessary .parquet files to Git, add the following to your .gitignore file:

*.parquet


11. Commit Changes to Git

After making changes, use Git to track and commit your changes.

git status

If changes are shown, add them to the staging area:

git add .

Then, commit the changes:

git commit -m 'Add pipeline setup and script'

Your status should look like this:

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

Push the changes to the remote repository 

git push origin main 

After pushing the changeds will be uploaded to the online repository


12. Prepare for Docker Deployment

Once the pipeline script is ready, the next step is to package the project into a Docker image so it can run in a reproducible environment.

a_Create a Dockerfile

Inside the pipeline folder, create a file named Dockerfile and add the following code:

FROM python:3.13

RUN pip install pandas pyarrow

WORKDIR /code

COPY pipeline.py .

This Dockerfile:

Uses Python 3.13 as the base image

Installs required dependencies (pandas and pyarrow)

Sets the working directory to /code

Copies the pipeline script into the container

b_Build the Docker Image

From the project directory, build the Docker image:

docker build -t test:pandas .

This command creates a Docker image named test:pandas.

c_Run the Container (Interactive Mode)

You can start the container with a bash shell for testing:

docker run -it --entrypoint=bash --rm test:pandas

Explanation:

-it → interactive terminal

--entrypoint=bash → opens a bash shell inside the container

--rm → removes the container automatically when it stops

The --rm flag is useful for temporary runs because it prevents stopped containers from accumulating on your system.

Inside the container, you can test the script:

ls
python pipeline.py 12
d_Automate Execution with ENTRYPOINT

To avoid manually running the Python command every time, add an ENTRYPOINT to the Dockerfile.

Update the Dockerfile:

FROM python:3.13

RUN pip install pandas pyarrow

WORKDIR /code

COPY pipeline.py .

ENTRYPOINT ["python","pipeline.py"]

Now the container will automatically execute the pipeline script when it starts.

e_Run the Pipeline

Run the container and pass the month argument:

docker run -it --rm -v "$(pwd):/code" test:pandas 12

Explanation:

-v "$(pwd):/code" mounts the current directory into the container

This allows output files (such as .parquet) to be written to your local machine

f_Managing Dependencies with uv

To make dependency management reproducible, you can use uv together with pyproject.toml and uv.lock.

Add the following lines to the Dockerfile:

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

COPY pyproject.toml .python-version uv.lock ./

RUN uv sync --locked

This ensures the container installs the exact dependency versions defined in your lock file.

g_Running Python with uv

You can modify the entrypoint to use uv:

ENTRYPOINT ["uv", "run", "python", "pipeline.py"]

Alternatively, activate the virtual environment by adding:

ENV PATH="/code/.venv/bin:$PATH"

Then the entrypoint can remain:

ENTRYPOINT ["python","pipeline.py"]
h_Rebuild and Run the Container

After updating the Dockerfile, rebuild the image:

docker build -t test:pandas .

Run the pipeline:

docker run -it --rm -v "$(pwd):/code" test:pandas 12

The pipeline will execute and create the output file (e.g., output_12.parquet) in your local directory.

At the end the final docker file mulst look like: 

FROM python:3.13

RUN pip install pandas pyarrow

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code 

ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./

COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]



13. Running postgres from docker:

You can run a containerized version of postgres, without installation.
You only need to create environment variables and a volume to stop it.

a) Running Postgres in a Container 

Create a folder anywhere for saving data in Postgres. 
We will use the folder ny_taxi_DB

docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \ 
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_DB:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18


    -e sets environment variables (user, password, database name)
    -v ny_taxi_postgres_data:/var/lib/postgresql creates a named volume
        Docker manages this volume automatically
        Data persists even after container is removed
        Volume is stored in Docker's internal storage
    -p 5432:5432 maps port 5432 from container to host
    postgres:18 uses PostgreSQL version 18 (latest as of Dec 2025)

Another way (bind mount):

mkdir ny_taxi_DB

docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \ 
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_DB:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

In this way first you create the directory and it is owned by the user. If docker is doing it it will be created and owned by the docker root user and may cause permission issues on linux.

Named volume: name:/path
Bind mount: /host/path:/container/path


b) Connecting to PostgreSQL

Install pgcli:

uv add --dev pgcli
--dev flag marks this as a development dependency. You may check it in the pyproject,toml file in the dependency-group section.

uv run pgcli -h localhost -p 5432 -u root -d ny_taxi

Now after entering your password try to run some queries: 

List of tables: 
\dt

Create a table:
CREATE TABLE test (id INTEGER, name VARCHAR(50));

Insert data: 
INSERT INTO test VALUES (1, 'Hello Docker');

Query data:
SELECT * FROM test;

-- Exit
\q


14. Importing data to pstgresql(Data Ingestion)

a) create a Jupyter Notebook file (We will use it to read a csv file and export it to Postgres.

Install Jupyter:
uv add --dev jupyter

Then run Jupyter notebook:
uv run jupyter notebook

Now create a new notebook and run the following code:

The data can be ingested from any data sources in different formats: 

parquet: 

import pandas as pd 
#read a sample of the data 
prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data/)'
url = f'{prefix}/yellow_tripdata_2025-01.parquet'

df = pd.read_parquet(url)

#Display the first rows 
df.head()

#Display the datatypes 
df.dtypes

#Check data  shape
df.shape

CSV:

import pandas as pd 
// read a sample of the data 
prefix = 'your address prefix'
url = f'{prefix}/file_name.csv'

df = pd.read_csv(url)

df.head()
df.dtypes
df.shape


In case you have any problems in the data types you may run this code:

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


Data Ingstion into postgres: 
In the notebook we follow these steps: 

1. Download the dataset(CSV or Parquet)
2. read it in chunks with pandas
3. Convert the datatypes if it is necessary(Data transformation)
4. Create an engine to connect postgres and jupyter using SQLAlchemy 
5. Insert data into PostgreSQL


Install SQLAlchemy:
uv add aqlalchemy "psycopg[binary,pool]"
uv add psycopg-binary


In the notebook create the engine: 
from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')

Get Thw Schema:
print(pd.io.sql.get_schema(df, name='yellow_taxi_data'))

Output: 
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


Create the Table:
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

