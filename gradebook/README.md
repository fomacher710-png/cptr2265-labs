# Lab 12 Templates: Containerization & Docker Compose

These are **fill-in templates**, not an application. You containerize your own project (your midterm/team project, or one of the earlier lab starters such as the Lab 9 gradebook). They work for Python or Java.

Requires **Docker Desktop** (Windows/macOS) or Docker Engine with the Compose plugin (Linux). Check with `docker --version` and `docker compose version`.

## What's inside
| File | Part | Copy it to |
|---|---|---|
| `templates/Dockerfile` | A | the folder with your app's build file (`requirements.txt` or `pom.xml`) |
| `templates/.dockerignore` | A | same folder as the Dockerfile |
| `templates/docker-compose.yml` | B | same folder as the Dockerfile |
| `templates/.env.example` | B | same folder; then copy it to `.env` and fill in values |
| `templates/ci/docker-image-job.yml` | C | paste the job into `.github/workflows/ci.yml` from Lab 11 |

Every file has `TODO` comments explaining what to fill in. Files starting with a dot are hidden by default: in File Explorer turn on **View > Show > Hidden items**; on macOS press Cmd+Shift+. in Finder.

## Before you start: is your app container-ready?
1. **Configuration from the environment.** The port, database URL, passwords and similar settings must be read from environment variables (Python `os.getenv("PORT", "8080")`, Java `System.getenv()`), not hardcoded. Part B requires this.
2. **Listen on 0.0.0.0.** A server bound to `127.0.0.1`/`localhost` inside a container cannot be reached through `-p 8080:8080`.
3. **`.env` is ignored.** Add `.env` to both `.gitignore` and `.dockerignore`.

## Part A: Dockerfile, .dockerignore, GitHub Container Registry
```
docker build -t myapp:local .
docker run --rm -p 8080:8080 myapp:local
docker run --rm -p 9000:8080 -e APP_ENV=demo myapp:local    # same image, different config
docker image ls myapp                                       # note the image size
```
Push it by hand once (Part C automates this):
```
# GitHub personal access token (classic) with the write:packages scope
echo YOUR_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
docker tag myapp:local ghcr.io/your-github-username/myapp:v1
docker push ghcr.io/your-github-username/myapp:v1
```
The image appears under **Packages** on your GitHub profile. Image names must be lowercase.

## Part B: Docker Compose with a dependency
```
copy .env.example .env          # macOS/Linux: cp .env.example .env   (change the password)
docker compose up -d --build
docker compose ps               # db should show (healthy) and app should be running
docker compose logs app
```
Prove the dependency works: create some data through your app, run `docker compose down`, then `docker compose up -d`. The data should still be there because it lives in a named volume. `docker compose down -v` removes the volume.

## Part C: build and push from CI/CD
Add the job from `templates/ci/docker-image-job.yml` to your Lab 11 workflow. After a merge to main, screenshot your package page on GitHub showing the image tagged with the commit SHA.

## Questions to answer in your README
1. Why copy the dependency file (`requirements.txt` / `pom.xml`) and install dependencies before copying the rest of the source?
2. Why must your app listen on `0.0.0.0` inside a container?
3. Why does the database URL use the host name `db` instead of `localhost`?
4. What would be lost if the database service had no volume?
5. How does tagging the image with the commit SHA help when something breaks in production?

## Submit
- Dockerfile, .dockerignore, docker-compose.yml and .env.example committed (not .env)
- Updated `.github/workflows/ci.yml`
- Screenshots: `docker compose ps` with both services up, and the GitHub Container Registry package showing the SHA tag
- README answers to the questions above
