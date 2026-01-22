# Discord Kubernetes Bot - AI Agent Instructions

## Architecture Overview

This is a **Discord bot deployed on GKE** with full CI/CD automation. The system has three layers:

1. **Application** (`app/`) - Python Discord bot using `discord.py` with system metrics via `psutil`
2. **Kubernetes** (`k8s/`) - Deployment manifest with resource limits and K8s metadata injection
3. **Infrastructure** (`terraform/`) - GKE cluster on GCP with Spot VMs for cost optimization

**Data Flow**: `git push main` → GitHub Actions → Docker build → GCR → kubectl apply → GKE pod restart

## Project Structure

```
app/bot.py          # Single-file bot with !ping and !info commands
app/Dockerfile      # Python 3.12-slim, requirements-first for layer caching
k8s/deployment.yaml # K8s manifest with downward API env vars for pod metadata
terraform/*.tf      # VPC, subnet, GKE cluster with Spot node pool
.github/workflows/  # CI/CD with GCR push and kubectl rollout
```

## Key Patterns

### Kubernetes Metadata Injection
The bot reads K8s context via environment variables injected through `fieldRef` downward API:
```yaml
env:
  - name: POD_NAMESPACE
    valueFrom:
      fieldRef:
        fieldPath: metadata.namespace
```
When adding new K8s metadata to display, update both `k8s/deployment.yaml` and `app/bot.py` env reading.

### Metrics Collection
Bot uses global state for tracking (`commands_executed`, `api_latency_list`). Network/disk metrics are calculated as deltas from `net_io_start`/`disk_io_start` baselines captured at startup.

### Discord Embed Pattern
The `!info` command returns two `discord.Embed` objects (1/2 and 2/2) to overcome Discord's field limits. Follow this pattern for rich responses.

## Developer Workflows

### Local Development
```bash
cd app
# Create .env with DISCORD_TOKEN=your_token
pip install -r requirements.txt
python bot.py
```

### Deployment
Push to `main` triggers automatic deployment via GitHub Actions. Manual deployment:
```bash
cd k8s && kubectl apply -f deployment.yaml
kubectl rollout status deployment/discord-bot-deployment
```

### Infrastructure Changes
```bash
cd terraform
terraform plan   # Preview changes
terraform apply  # Apply to GCP
```

## Conventions

- **Language**: Code comments and bot responses are in Russian
- **Resource Limits**: Always define `requests` and `limits` in deployment.yaml
- **Image Tags**: CI/CD uses `$GITHUB_SHA` for unique, traceable image versions
- **Cost Optimization**: Uses Spot VMs (`spot = true` in Terraform) - pods may be preempted

## External Dependencies

- **GCP Project**: `sharp-oxygen-478014-k9`
- **GCR**: `gcr.io/sharp-oxygen-478014-k9/discord-bot`
- **K8s Secret**: `discord-bot-secrets` with `DISCORD_TOKEN` key
- **Observability**: kube-prometheus-stack (Prometheus + Grafana) deployed via Helm
