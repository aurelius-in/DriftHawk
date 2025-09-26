Overlays

- dev/staging/prod include a `secretGenerator` with a placeholder. Replace with your real secrets or remove if you manage secrets elsewhere (e.g., Sealed Secrets).
- Per-env `LOG_LEVEL` is set via `configMapGenerator`.
- Prod overlay sets replicas=3 and includes HPA.

## Smoke Deploy

- Ensure cluster access and Argo CD installed
- Apply app: `make argo.sync`
- Verify pods: `kubectl -n drifthawk get deploy,svc,pod`
- Check health: port-forward svc and hit `/healthz`, `/readyz`

