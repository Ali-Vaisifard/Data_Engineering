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
12. Prepare for Docker Deployment

Now that the setup is complete, it's time to prepare everything for deployment in a Docker image.