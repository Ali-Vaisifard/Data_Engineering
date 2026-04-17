# 🚀 Data Engineering – Docker Tutorial

![Docker](https://img.shields.io/badge/Docker-Containerization-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.13-yellow?logo=python)
![Level](https://img.shields.io/badge/Level-Beginner-green)

---

## 🐳 Docker Tutorial – Beginner to Practical

This hands-on guide walks you through essential Docker concepts:

- ✅ Running containers  
- 🔒 Understanding container isolation  
- 🧹 Managing & removing containers  
- ⚠️ Understanding stateless behavior  
- 💾 Persisting data using volumes  

---

## 📌 1. Customizing the Terminal (Optional)

Check Python version:

```bash
python --version
```

Example:

```bash
Python 3.12.1
```

Temporary prompt:

```bash
PS1="> "
```

Permanent prompt:

```bash
echo 'PS1="> "' >> ~/.bashrc
```

---

## 🐳 2. Verify Docker Installation

```bash
docker --version
docker run hello-world
```
In case you dont have it:

first Update your system:
```bash
sudo apt update
sudo apt upgrade -y
```
Install required packages
```bash
sudo apt install -y ca-certificates curl gnupg
```

Add Docker’s official GPG key
```bash
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

Add Docker repository
```bash
echo \
"deb [arch=$(dpkg --print-architecture) \
signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

```
Install Docker Engine
```bash
sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Again verify Docker installation:
```bash
docker --version
docker run hello-world
```
Run Docker without sudo (IMPORTANT)

By default, Docker needs sudo. Fix that:
```bash
sudo usermod -aG docker $USER
```


Then restart your session (or run):
```bash
newgrp docker
```

Now test:
```bash
docker run hello-world
```
---

## 🖥️ 3. Running an Ubuntu Container

```bash
docker run ubuntu
docker run -it ubuntu
```

Inside container:

```bash
apt update
apt install python3
python3 -V
```

Exit:

```bash
exit
```

---

## 🔐 4. Container Isolation

```bash
docker run -it ubuntu
python -V
```

❗ You may see:

```bash
command not found
```

👉 Each container is independent and starts fresh.

---

## 🐍 5. Using Official Python Image

```bash
docker run -it python:3.13.11
docker run -it --entrypoint=bash python:3.13.11
```

Inside container:

```bash
python --version
echo 123 > file
ls
cat file
exit
```

Run again:

```bash
docker run -it --entrypoint=bash python:3.13.11
cat file
```

❗ Output:

```bash
No such file or directory
```

### ⚠️ Key Concept: Stateless Containers

- Each `docker run` creates a new container  
- Changes are NOT saved unless persisted  

---

## 🧹 6. Managing Containers

```bash
docker ps -a
docker ps -aq
docker rm $(docker ps -aq)
docker rm -f $(docker ps -aq)
```

---

## 💾 7. Persisting Data with Volumes

### 📁 Step 1: Create Project

```bash
mkdir test
cd test
touch file1.txt file2.txt file3.txt
echo "Hello from host" > file1.txt
cat file1.txt
```

---

### 🧠 Step 2: Create Python Script

```python
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
```

---

### 🔗 Step 3: Mount Volume

```bash
cd ..
pwd
docker run -it --entrypoint=bash -v $(pwd)/test:/app/test python:3.13.11
```

---

### ▶️ Step 4: Run Script

```bash
cd /app/test
ls
python script.py
```

### ✅ Expected Output

```bash
Files in /app/test:
  - file1.txt
    Content: Hello from host
  - file2.txt
  - file3.txt
```

---

## 🎓 Final Takeaways

| Concept | Explanation |
|--------|------------|
| ❌ Without `-v` | Data is lost when container stops |
| ✅ With `-v` | Data persists on host machine |
| 🐳 Containers | Always stateless by default |

---

## ⭐ Tips

- Use official images whenever possible  
- Keep containers lightweight  
- Use volumes for real projects  

---

## 👨‍💻 Author

Ali Vaisifard  
MSc Data Science | Data Engineering Enthusiast
