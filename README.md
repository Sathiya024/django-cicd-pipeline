
## Application endpoint

`GET /health/` returns `{"status": "ok"}` and is used to confirm the app is running.

<img width="1808" height="991" alt="image" src="https://github.com/user-attachments/assets/60756abf-0398-4951-bb68-1dc70c097d78" />


## Setup

### 1. Run the app locally

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Open http://127.0.0.1:8000/health/ to check it.

### 2. Run the tests

```bash
cd app
pytest
```

### 3. Build and run the container

```bash
cd app
docker build -t django-cicd-app:local .
docker run -d -p 8000:8000 --name django-test django-cicd-app:local
curl http://localhost:8000/health/
```

### 4. Start Jenkins and SonarQube

Both run on the host machine:
- Jenkins: http://localhost:8080
- SonarQube: http://localhost:9000

### 5. Configure Jenkins

- Install the **SonarQube Scanner** and **GitHub Integration** plugins.
- Add a *Secret text* credential with ID `sonar-token`, containing a SonarQube token.
- Add a *Username with password* credential with ID `dockerhub-creds`, containing a Docker Hub access token.
- Under **Manage Jenkins > System > SonarQube servers**, add a server named `SonarQube` with URL `http://localhost:9000`.
- Under **Manage Jenkins > Tools > SonarQube Scanner installations**, add a scanner named `SonarScanner` with *Install automatically* ticked.

### 6. Create the pipeline job

Create a Pipeline job named `django-cicd-pipeline`, set it to **Pipeline script from SCM**, and point it at this repository with script path `Jenkinsfile`.

## Running the pipeline

Click **Build Now** in Jenkins. A successful run shows all four stages in green, and the image appears in your Docker Hub account.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `No tests ran` (exit code 5) | `pytest.ini` is in the wrong folder | Put `pytest.ini` in `app/`, not `app/core/` |
| `No tool named SonarScanner found` | Scanner tool not saved in Jenkins | Add it under **Manage Jenkins > Tools** and click **Save** |
| `SonarQube installation ... does not match` | Server name is not `SonarQube` | Rename the server entry in **Manage Jenkins > System** |
| `Failed to query server version` | Scanner can't reach SonarQube | Use `http://localhost:9000` when both run on the host |
| Webhook URL rejected | SonarQube blocks private and loopback addresses in webhooks | Poll the API instead of using a webhook |
| `permission denied` on Docker | Jenkins user not in the `docker` group | `sudo usermod -aG docker jenkins`, then restart Jenkins |
| `git push` rejected | Remote has commits you don't have locally | `git pull origin main --rebase --allow-unrelated-histories`, then push |

## Lessons learned

- Pytest needs its configuration file in the folder where it runs.
- Jenkins plugins and tools must be saved before a pipeline can use them.
- Each tool's name in the Jenkinsfile must match the name in Jenkins exactly.
- Services running on the same machine should use `localhost`, not container names.

## Possible improvements

- Add back the SonarQube Quality Gate check, so a failing code-quality result stops the pipeline.
- Trigger builds automatically on every push through a GitHub webhook.
- Deploy the image to a server or Kubernetes cluster.

## Author

[Sathiya Narayanan] — [sathiyanarayanan2003s@gmail.com]
