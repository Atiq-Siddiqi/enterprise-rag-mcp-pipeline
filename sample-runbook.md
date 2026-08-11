# Service Deployment Runbook: Payment Gateway V2
   
## Overview
The Payment Gateway V2 service handles credit card transactions securely.
   
## Troubleshooting 504 Gateway Timeouts
If you encounter 504 errors:
1. Check the ECS task cluster CPU utilization via CloudWatch.
2. Verify the Redis cluster connection pool settings in AWS Secrets Manager (`/prod/payment/redis`).
3. Restart the task gracefully using the CLI: `aws ecs update-service --cluster prod-cluster --service payment-v2 --force-new-deployment`