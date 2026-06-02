# Python App Frontend – CI/CD with GitHub Actions

This repository contains a Python-based application packaged as a Docker image. The CI/CD pipeline is triggered when a Pull Request (PR) to the `master` branch is **approved, merged, and closed**.

---

## 📁 Project Structure

```
.
├── api
│   ├── app.py          # Application source code
│   └── Dockerfile      # Docker image definition
└── .github
    └── workflows
        └── cicd.yml    # GitHub Actions CI/CD pipeline
```

---

## 🚀 What This Pipeline Does

The GitHub Actions workflow automates the following steps:

1. **Triggers only when a PR is merged into `master`**
2. **Runs a SonarQube scan** to enforce code quality gates
3. **Builds a Docker image** from the `api/` directory

---

## 🔁 CI/CD Workflow Trigger

The pipeline is triggered by this event:

```yaml
on:
  pull_request:
    types: [closed]
    branches:
      - master
```

And it only runs **if the PR was actually merged**:

```yaml
if: github.event.pull_request.merged == true
```

This ensures:
- ❌ No pipeline runs on PR close without merge
- ✅ Pipeline runs only after approved & merged code

---

## 🔐 Secrets

Required GitHub Secrets:

| Secret Name | Description |
|------------|------------|
| `SONAR_TOKEN` | SonarQube authentication token |

---

## 🧩 Complete CI/CD Flow

1. Create a **new feature branch** from `master`
2. Make code changes
3. Commit & push the branch
4. Open a **Pull Request to `master`**
5. PR is **reviewed and approved**
6. PR is **merged manually**
7. GitHub Actions pipeline runs automatically

---