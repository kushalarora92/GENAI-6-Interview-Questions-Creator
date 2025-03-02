# Moving Away from ECS/Fargate

## Context
After determining AWS Lambda was not suitable due to size limitations, we initially considered ECS/Fargate for containerized deployment. However, cost analysis revealed it wasn't suitable for our development/testing phase.

## Initial Architecture with ECS/Fargate

```
GitHub Actions --> Amazon ECR --> ECS/Fargate
     │                               │
     │                               │
     └─────> AWS Secrets ───────────>│
                                     │
                                     ▼
                               Application Load Balancer
                                     │
                                     ▼
                                  Internet
```

## Cost Analysis (Monthly Estimates)

1. **ECS/Fargate**
   - Compute (1 vCPU, 2GB RAM): ~$30-40
   - No free tier available
   - Minimum viable setup required

2. **ECR (Container Registry)**
   - Storage: First 500MB free
   - After free tier: $0.10 per GB-month
   - Data transfer out: $0.09-$0.13 per GB

3. **Application Load Balancer**
   - Fixed cost: ~$20/month
   - No free tier available

4. **Total Minimum Cost**
   - Base cost: ~$50-70/month
   - Additional costs for scaling/traffic

## Problems
1. **Cost Inefficiency**
   - No free tier for Fargate
   - Required components have base costs
   - Overprovisioned for development needs

2. **Complexity**
   - Complex infrastructure setup
   - Multiple AWS services to manage
   - Steeper learning curve

## Alternative: EC2 with Docker

### Proposed Architecture
```
GitHub Actions --> EC2 Instance (Docker)
     │                  │
     │                  │
     └─> AWS Secrets ──>│
                        │
                        ▼
                     Internet
```

### Benefits
1. **Cost Effective**
   - Free tier eligible (t2.micro for 12 months)
   - Single instance instead of multiple services
   - Pay only for additional storage/traffic

2. **Simpler Management**
   - Direct Docker deployment
   - Fewer moving parts
   - Easier debugging and monitoring

3. **Development Friendly**
   - Suitable for testing/development
   - Easy to scale later if needed
   - Can migrate to ECS/Fargate when required

## Decision
Move to EC2-based deployment with Docker due to:
1. Free tier eligibility
2. Simpler architecture
3. Sufficient for current needs
4. Easy path to scale up later

## Next Steps
1. Set up EC2 instance with Docker
2. Configure GitHub Actions for EC2 deployment
3. Implement monitoring and logging
4. Document scaling strategies for future

## References
- [AWS Free Tier](https://aws.amazon.com/free/)
- [ECS Pricing](https://aws.amazon.com/ecs/pricing/)
- [EC2 Pricing](https://aws.amazon.com/ec2/pricing/) 
- [deploy-ecs.yaml](https://github.com/ai6-dev/ai6-interview-questions-creator/blob/main/.github/workflows/deploy-ecs.yaml)
