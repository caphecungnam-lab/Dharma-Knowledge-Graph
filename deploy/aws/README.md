# DKG AWS Deployment

Production target:

- FastAPI runs as stateless ECS Fargate tasks.
- Neo4j, Qdrant, and Redis endpoints are supplied by AWS SSM Parameter Store or
  Secrets Manager.
- HTTPS terminates at an Application Load Balancer.
- Logs go to CloudWatch via `awslogs`.

Required SSM parameters:

- `/dkg/prod/api-key`
- `/dkg/prod/neo4j-uri`
- `/dkg/prod/neo4j-user`
- `/dkg/prod/neo4j-password`
- `/dkg/prod/qdrant-host`
- `/dkg/prod/redis-url`

Build and push image:

```bash
AWS_REGION=us-east-1 AWS_ACCOUNT_ID=123456789012 ./deploy/aws/ecr-build-push.sh
```

Deploy:

```bash
aws ecs register-task-definition --cli-input-json file://deploy/aws/ecs-task-definition.json
aws ecs update-service --cluster dkg-prod --service dkg-api --force-new-deployment
```

Scaling:

- Set ECS service desired count to at least `2`.
- Use target tracking on ALB request count or CPU utilization.
- Keep API containers stateless; Redis stores shared cache/rate-limit state.
