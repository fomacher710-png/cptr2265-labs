# Capstone Risk Register: DevOps Pipeline

**Project:** Automated DevSecOps Pipeline  
**Target Release:** December 18, 2026  

---

## Risk Register

| ID | Risk | Probability | Impact | Mitigation Strategy (Required for High Risks) |
| :--- | :--- | :---: | :---: | :--- |
| **R-01** | **Leaked Secrets:** API keys or tokens accidentally committed to GitHub. | Medium | **High** | Store all credentials in **GitHub Secrets** and enable secret scanning in CI to block commits containing keys. |
| **R-02** | **Failed Deployment:** New container crashes in production due to config errors. | Medium | **High** | Run an automated `/health` smoke test after deploy and roll back to the previous image if it fails. |
| **R-03** | **Scope Creep:** Over-complicating Kubernetes or Terraform delays core CI/CD goals. | **High** | **High** | Stick strictly to the milestone schedule; use Docker Compose first before attempting complex orchestration. |
| **R-04** | **Container Vulnerabilities:** Trivy flags `CRITICAL` CVEs and blocks builds. | **High** | Medium | Use minimal official base images (e.g., `python:3.14-slim`) and update dependencies weekly. |
| **R-05** | **Server Disk Full / Downtime:** Old Docker images fill up the host VM before demo day. | Low | **High** | Run `docker image prune -af` automatically after deployments and record a backup demo video early. |
| **R-06** | **Broken `main` Branch:** Direct pushes bypass tests and break the working pipeline. | Low | **High** | Enable **Branch Protection Rules** on `main` requiring pull requests and passing CI checks before merge. |
| **R-07** | **Flaky Tests:** Timing issues cause automated tests to fail randomly. | Medium | Medium | Mock external calls in unit tests and use retry loops instead of fixed `sleep` timers. |
| **R-08** | **CI Minute / Rate Limits:** Frequent builds exhaust free GitHub Actions minutes or pull limits. | Low | Medium | Cache Docker layers and authenticate image pulls using `GITHUB_TOKEN`. |