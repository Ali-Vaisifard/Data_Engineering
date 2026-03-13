FROM python:3.13

RUN pip install pandas pyarrow

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code 

ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./

COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]

