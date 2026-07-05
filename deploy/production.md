# DKG Production Deployment

This guide deploys Dharma Knowledge Graph as production infrastructure, not a
local prototype.

## Runtime Shape

- `dkg-frontend-service`: Next.js production server.
- `dkg-backend-service`: FastAPI served by Gunicorn with Uvicorn workers.
- Neo4j, Qdrant, and Redis: private network or managed endpoints.
- ALB: public entrypoint with HTTPS termination.
- Nginx: reverse proxy for Docker/EC2 deployments, routing `/` to frontend and
  `/api` to backend.

## Domain And HTTPS

Recommended DNS:

- `https://dkg.yourdomain.com` -> frontend target group.
- `https://api.dkg.yourdomain.com` -> backend target group.

AWS setup:

1. Create an ACM certificate for both names.
2. Attach the certificate to the ALB HTTPS listener.
3. Configure HTTP listener redirect to HTTPS.
4. Route53 records point both domains to the ALB.
5. Store application secrets in AWS Secrets Manager or SSM Parameter Store.

## Environment Separation

Use separate SSM/Secrets paths:

- `/dkg/dev/*`
- `/dkg/staging/*`
- `/dkg/prod/*`

The checked-in `.env.production` is a placeholder template only. Replace values
through the deployment environment; do not commit real credentials.

## Required Production Variables

- `NEXT_PUBLIC_API_URL`
- `DKG_CORS_ORIGINS`
- `DKG_JWT_SECRET`
- `DKG_ADMIN_USER`
- `DKG_ADMIN_PASSWORD`
- `DKG_API_KEY`
- `NEO4J_URI`
- `NEO4J_USER`
- `NEO4J_PASSWORD`
- `QDRANT_HOST`
- `QDRANT_PORT`
- `REDIS_URL`

## Security Baseline

- JWT is required for AI and graph endpoints.
- Frontend never accesses Neo4j or Qdrant.
- Backend remains the single source of truth.
- Safety orchestration remains mandatory before AI graph response generation.
- Rate limiting is enforced at API middleware and Nginx.
- No production localhost API URL is allowed.

## Health And Monitoring

- Backend health: `/health`
- Prometheus metrics: `/metrics/prometheus`
- Runtime dashboard: `/observability/dashboard`
- Logs: CloudWatch for ECS, container stdout/stderr for Docker.

## Docker Production Run

```bash
docker compose --env-file .env.production -f docker/docker-compose.prod.yml up --build
```

For public internet deployment, place the Docker stack behind an HTTPS load
balancer or provide TLS termination at the host level.
