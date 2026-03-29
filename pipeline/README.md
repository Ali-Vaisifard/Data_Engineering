🚀 Python Pipeline Project Setup

This guide walks you through setting up, running, and deploying the Python pipeline project using uv, Docker, and PostgreSQL.

📁 1. Project Setup
Create the pipeline script
touch pipeline.py
Navigate to project folder
cd pipeline
🧪 2. Virtual Environment (uv)
Install uv
pip install uv
Initialize environment (Python 3.13)
uv init --python 3.13
Verify Python version
which python
python -V
Run Python inside uv
uv run python -V
uv run which python
📦 3. Install Dependencies
uv add pandas
🧠 4. IDE Configuration (VSCode)

Select interpreter:

pipeline/.venv/bin/python
▶️ 5. Run the Pipeline
uv run python pipeline.py 12
🚫 6. Git Ignore

Add to .gitignore:

*.parquet
🌿 7. Git Workflow
git status
git add .
git commit -m "Add pipeline setup and script"
git push origin main
🐳 8. Docker Setup
📄 Create Dockerfile
FROM python:3.13

RUN pip install pandas pyarrow

WORKDIR /code

COPY pipeline.py .
🔨 Build Image
docker build -t test:pandas .
🧪 Run Container (Interactive)
docker run -it --entrypoint=bash --rm test:pandas

⚠️ Important:

--rm → container is deleted after exit
Good for temporary runs
⚙️ Automate Execution

Update Dockerfile:

ENTRYPOINT ["python","pipeline.py"]
▶️ Run Pipeline via Docker
docker run -it --rm -v "$(pwd):/code" test:pandas 12
🔁 9. Reproducible Dependencies (uv)

Add to Dockerfile:

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

COPY pyproject.toml .python-version uv.lock ./

RUN uv sync --locked
Option 1: Use uv in ENTRYPOINT
ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
Option 2: Activate venv
ENV PATH="/code/.venv/bin:$PATH"
ENTRYPOINT ["python","pipeline.py"]
✅ Final Dockerfile
FROM python:3.13

RUN pip install pandas pyarrow

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code 

ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./
COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]
🐘 10. PostgreSQL with Docker
▶️ Run PostgreSQL (Named Volume)
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_DB:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:18
📂 Alternative: Bind Mount
mkdir ny_taxi_DB

docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_DB:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:18
🔌 11. Connect to PostgreSQL
Install pgcli
uv add --dev pgcli
Connect
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
Example SQL Commands
\dt

CREATE TABLE test (id INTEGER, name VARCHAR(50));

INSERT INTO test VALUES (1, 'Hello Docker');

SELECT * FROM test;

\q
📊 12. Data Ingestion (Jupyter)
Install Jupyter
uv add --dev jupyter
uv run jupyter notebook
📥 Load Parquet Data
import pandas as pd

url = "https://.../yellow_tripdata_2025-01.parquet"
df = pd.read_parquet(url)

df.head()
df.dtypes
df.shape
📥 Load CSV Data
df = pd.read_csv("file.csv")
⚙️ Fix Data Types
df = pd.read_csv(
    "file.csv",
    dtype=dtype,
    parse_dates=parse_dates
)
🛢️ 13. Load Data into PostgreSQL
Install dependencies
uv add sqlalchemy "psycopg[binary,pool]"
uv add psycopg-binary
Create Engine
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://root:root@localhost:5432/ny_taxi"
)
Generate Schema
print(pd.io.sql.get_schema(df, name='yellow_taxi_data'))
Create Table
df.head(0).to_sql(
    name='yellow_taxi_data',
    con=engine,
    if_exists='replace'
)
🚀 Chunked Data Ingestion (Efficient)
import urllib.request
import pyarrow.parquet as pq

urllib.request.urlretrieve(url, "data.parquet")

pq_file = pq.ParquetFile("data.parquet")

for batch in pq_file.iter_batches(batch_size=100000):
    df_chunk = batch.to_pandas()
    df_chunk.to_sql(
        name='yellow_taxi_data',
        con=engine,
        if_exists='append',
        index=False
    )
✅ Validate Data
pd.read_sql(
    "SELECT COUNT(*) FROM yellow_taxi_data",
    con=engine
)
🎯 Summary

This pipeline includes:

✅ Python environment management (uv)
✅ Dependency locking
✅ Docker containerization
✅ PostgreSQL integration
✅ Scalable data ingestion
✅ Reproducible workflows

If you want, I can next:

⭐ make it GitHub fancy (badges + diagrams)
⭐ add architecture diagram
⭐ or convert this into a portfolio-level README (for job applications)
how can I copy it there?

Good question — here’s the simplest way to copy this into your GitHub README 👇

✅ Method 1: Direct Copy–Paste (Easiest)
Open your repository on GitHub
Click on README.md
Click ✏️ Edit (pencil icon)
Delete everything (or keep parts you want)
Go back here → copy my formatted README
Paste it into GitHub editor
Scroll down → click Commit changes
💻 Method 2: Using VS Code (Recommended for you)

Since you're coding locally:

Step 1: Open README file
code README.md
Step 2: Paste content
Replace everything with the new content
Step 3: Save file
Ctrl + S
Step 4: Push to GitHub
git add README.md
git commit -m "Improve README formatting"
git push origin main
⚠️ Important Tips
1. Make sure it's Markdown

Your file must be named exactly:

README.md
2. Keep code blocks intact

Make sure things like this stay unchanged:

```bash
uv run python pipeline.py 12
```
3. Preview before committing

In GitHub editor:

Click "Preview" tab
Check formatting (headings, code, spacing)
