# Lab 12 Part A: containerize YOUR application.
#
# Copy this file to the folder that holds your application's build file
# (requirements.txt / pyproject.toml for Python, pom.xml / build.gradle for
# Java), then fill in each TODO. When you are done this should work:
#     docker build -t myapp:local .
#     docker run --rm -p 8080:8080 myapp:local
#
# Delete the hint comments for the language you are NOT using.

# TODO FROM: an official base image with your runtime.
FROM python:3.12-slim

#   Why is the final image smaller with two stages? Answer in your README.

# TODO WORKDIR: the working directory inside the image, e.g. /app
WORKDIR /app

# TODO Install dependencies BEFORE copying the rest of your source code.
#   Python: COPY requirements.txt .   then   RUN pip install --no-cache-dir -r requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#   Why does this order make rebuilds faster? Answer in your README.

# TODO COPY your application code (and any data files it needs at runtime).
COPY . .
# TODO COPY your application code (and any data files it needs at runtime).
COPY data/ ./data/

# TODO ENV: non-secret settings with safe defaults, e.g. PORT=8080.
ENV PORT=8080
#   Do NOT put passwords, API keys or database URLs here: anyone who pulls the
#   image can read them with `docker history` / `docker inspect`.
#   Your app must listen on 0.0.0.0 inside the container, not 127.0.0.1/localhost.

EXPOSE 8080
# TODO EXPOSE the port your app listens on.

# Optional (good practice): run as a non-root user.
#   Debian-based images: RUN useradd --create-home appuser   then   USER appuser

# TODO CMD: the command that starts your app, in exec (JSON array) form.
#   Python: CMD ["python", "-m", "yourpackage"]   or   CMD ["python", "app.py"]
CMD ["python", "app.py"]
