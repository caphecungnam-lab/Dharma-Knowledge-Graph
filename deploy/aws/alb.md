# DKG AWS ALB Configuration

Use an internet-facing Application Load Balancer for HTTPS ingress and keep ECS
tasks in private subnets.

Required listener rules:

- `HTTPS :443` with ACM certificate.
- Forward `/health`, `/metrics`, `/metrics/prometheus`, and API paths to the
  `dkg-api` target group.
- Redirect `HTTP :80` to `HTTPS :443`.

Target group:

- Target type: `ip`
- Protocol: `HTTP`
- Port: `8000`
- Health check path: `/health`
- Healthy threshold: `2`
- Unhealthy threshold: `3`

Security groups:

- ALB accepts `443` from the internet.
- ECS service accepts `8000` only from the ALB security group.
- Neo4j, Qdrant, and Redis must not be publicly exposed.
