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

