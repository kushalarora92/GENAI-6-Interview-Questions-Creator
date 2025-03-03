# EC2 Setup Guide

## Initial Setup (One-time Process)

1. **Launch EC2 Instance**:
   - AMI: Amazon Linux 2023
   - Instance Type: t2.micro (free tier)
   - Security Group:
     ```
     Inbound Rules:
     - SSH (22): Your IP
     - HTTP (80): 0.0.0.0/0
     - HTTPS (443): 0.0.0.0/0
     - Custom TCP (8000): 0.0.0.0/0  # Application port
     ```

2. **Generate SSH Key**:
   ```bash
   # Generate key pair
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/ec2_deploy_key -N ""
   
   # Store private key in GitHub Secrets as EC2_SSH_KEY
   cat ~/.ssh/ec2_deploy_key
   ```

3. **Run Setup Script**:
   ```bash
   # Connect to instance
   aws ec2-instance-connect ssh --instance-id <your-instance-id>
   
   # Copy setup script
   scp scripts/setup-ec2.sh ec2-user@<instance-ip>:~/
   
   # Run setup and follow the prompts
   chmod +x setup-ec2.sh
   ./setup-ec2.sh
   ```

4. **Configure GitHub Repository**:
   - Add Variables:
     ```
     AWS_REGION: your-region (e.g., us-east-1)
     EC2_INSTANCE_ID: your-instance-id
     AWS_SA_ROLE_ARN: your-role-arn
     ```
   - Add Secrets:
     ```
     EC2_SSH_KEY: your-private-key (from step 2)
     ```

## Verification Steps

1. **Test Docker Installation**:
   ```bash
   # Reconnect to apply group changes
   exit
   aws ec2-instance-connect ssh --instance-id <your-instance-id>
   
   # Verify Docker
   docker run hello-world
   ```

2. **Check Directories**:
   ```bash
   ls -la ~/deploy ~/static
   ```

3. **Verify Environment**:
   ```bash
   cat ~/.env
   ```

## Deployment Process (Automated)

The GitHub Actions workflow will automatically:
1. Get EC2 instance IP
2. Build Docker image
3. Deploy to EC2 instance

Deployments are triggered by:
- Push to main branch
- Manual workflow dispatch

## Troubleshooting

1. **Docker Permission Issues**:
   ```bash
   sudo usermod -aG docker ec2-user
   # Log out and log back in
   ```

2. **Directory Permissions**:
   ```bash
   chmod 755 ~/deploy ~/static
   ```

3. **Environment Variables**:
   ```bash
   chmod 600 ~/.env
   source ~/.env
   ```

## References
- [Amazon Linux 2023 Guide](https://docs.aws.amazon.com/linux/al2023/ug/)
- [Docker Installation](https://docs.docker.com/engine/install/)
- [EC2 Instance Connect](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Connect-using-EC2-Instance-Connect.html) 