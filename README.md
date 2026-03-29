# Data_Engineering

🐳 Docker Tutorial – Beginner to Practical

This tutorial walks through basic Docker concepts step by step, including:

Running containers

Understanding container isolation

Removing containers

Understanding stateless behavior

Persisting data with volumes
-----------------------------------------------------

1️⃣ Customizing the Terminal (Optional)

Check your Python version:

python --version

Example output:

Python 3.12.1

You can customize your terminal prompt temporarily:

PS1="> "

To make it permanent:

echo 'PS1="> "' >> ~/.bashrc
------------------------------------------------------------
2️⃣ Verify Docker Installation

Check Docker version:

docker --version

Test Docker with:

docker run hello-world
--------------------------------------------------------------
3️⃣ Running an Ubuntu Container

Run Ubuntu:

docker run ubuntu

Run Ubuntu interactively:

docker run -it ubuntu

Now inside the container:

apt update
apt install python3
python3 -V

Exit the container:

exit
-----------------------------------------------------
4️⃣ Understanding Container Isolation

Run Ubuntu again:

docker run -it ubuntu

If you try:

python -V

You may see:

command not found

Each container starts fresh unless changes are committed.
----------------------------------------------------------------------
5️⃣ Using an Official Python Image

Instead of manually installing Python, use the official image:

docker run -it python:3.13.11

You can also start it with bash:

docker run -it --entrypoint=bash python:3.13.11

Inside the container:

python --version
echo 123 > file
ls
cat file
exit

Run the container again:

docker run -it --entrypoint=bash python:3.13.11

Try:

cat file

You will see:

No such file or directory
🚨 Important Concept: Containers Are Stateless

Each time you run docker run, Docker creates a new container.
Changes are not saved unless explicitly persisted.
------------------------------------------------------------------------
6️⃣ Managing Containers

List all containers:

docker ps -a

List only container IDs:

docker ps -aq

Remove all containers:

docker rm $(docker ps -aq)

Force remove (including running containers):

docker rm -f $(docker ps -aq)
----------------------------------------------------------------------
7️⃣ Persisting Data with Volumes

To preserve files, we mount a host directory into the container.

Step 1 — Create a Project Folder on Host
mkdir test
cd test
touch file1.txt file2.txt file3.txt
echo "Hello from host" > file1.txt
cat file1.txt

Step 2 — Create script.py

Inside the test/ directory, create a file named script.py:

from pathlib import Path

current_dir = Path.cwd()
current_file = Path(__file__).name

print(f"Files in {current_dir}:")

for filepath in current_dir.iterdir():
    if filepath.name == current_file:
        continue    

    print(f"  - {filepath.name}")

    if filepath.is_file():
        content = filepath.read_text(encoding='utf-8')
        print(f"    Content: {content}")
🔎 What This Script Does

Detects the current working directory inside the container

Lists all files in that directory

Skips printing the script.py file itself

Reads and prints the content of each file

This helps demonstrate how Docker interacts with mounted host files.

Step 3 — Run Docker with Volume Mounting

Go back to your project root:

cd ..
pwd

Now run:

docker run -it --entrypoint=bash -v $(pwd)/test:/app/test python:3.13.11

Step 4 — Access and Execute Script Inside Container

Inside the container:

cd /app/test
ls
python script.py
✅ Expected Output Example
Files in /app/test:
  - file1.txt
    Content: Hello from host
  - file2.txt
  - file3.txt

Now you can clearly see:

The container can access host files

File contents persist

The container itself remains stateless

The host directory holds the actual data

🎓 Concept Reinforced

Without -v, files disappear when the container stops.
With -v, the container uses the host filesystem — making your data persistent.
