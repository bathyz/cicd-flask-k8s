# Flask CI/CD Pipeline (GitHub Actions -> GHCR -> Kubernetes)

A minimal Flask service used as a vehicle for a complete CI/CD pipeline:
test on every push/PR, build a container image, publish it to GitHub
Container Registry, and prepare a rolling deploy to Kubernetes.

## Pipeline stages (`.github/workflows/ci-cd.yml`)

1. **test** — installs dependencies and runs the `pytest` suite in `app/`.
2. **build-and-push** — on a push to `main` only (and after tests pass),
   builds the Docker image and pushes it to `ghcr.io/<owner>/<repo>` tagged
   both `:latest` and `:<commit-sha>` for traceable rollbacks.
3. **deploy** — substitutes the freshly built image tag into
   `k8s/deployment.yaml`. The actual `kubectl apply` / cluster login step is
   included as a commented-out example rather than wired to a live cluster,
   since this repo doesn't have one attached — see the workflow file for
   exactly what to uncomment and which secret to add.

## Running locally

```bash
docker compose up --build
curl http://localhost:5000/
curl http://localhost:5000/healthz
```

Or without Docker:

```bash
cd app
pip install -r requirements.txt
pytest -v
python app.py
```

## Kubernetes manifests

`k8s/deployment.yaml` runs 3 replicas with a rolling update strategy,
resource requests/limits, and liveness/readiness probes hitting `/healthz`.
`k8s/service.yaml` exposes it inside the cluster on port 80.

```bash
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml
```

## Why this project

Most tutorials stop at "build and push an image." This one also shows the
parts that actually gate a production rollout: tests as a hard prerequisite
for the build stage, immutable per-commit image tags, and a deployment
manifest with resource limits and health probes instead of a bare
`kubectl run`.

## License

MIT
