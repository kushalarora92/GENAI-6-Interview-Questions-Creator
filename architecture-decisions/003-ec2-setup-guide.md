# EC2 Instance Setup Guide

## Instance Configuration

1. **Launch EC2 Instance**:
   - AMI: Amazon Linux 2023
   - Instance Type: t2.micro (free tier)
   - Configure Instance Details:
     ```
     Network: Default VPC
     Auto-assign Public IP: Enable
     ```

2. **Security Group**:
   ```
   Inbound Rules:
   - SSH (22): Your IP
   - HTTP (80): 0.0.0.0/0
   - HTTPS (443): 0.0.0.0/0
   - Custom TCP (8000): 0.0.0.0/0  # Application port
   ```

## Instance Setup

1. **Connect to Instance**:
   ```bash
   ssh -i "your-key.pem" ec2-user@your-instance-ip
   ```

2. **Install Docker**:
   ```bash
   # Update system
   sudo yum update -y

   # Install Docker
   sudo yum install docker -y
   sudo systemctl start docker
   sudo systemctl enable docker

   # Add ec2-user to docker group
   sudo usermod -aG docker ec2-user
   ```

3. **Set Environment Variables**:
   ```bash
   # Create environment file
   sudo mkdir -p /etc/app
   sudo nano /etc/app/env.sh

   # Add environment variables
   export OPENAI_API_KEY='your-api-key'
   # Add other environment variables as needed

   # Make it executable
   sudo chmod +x /etc/app/env.sh

   # Load environment variables on startup
   echo "source /etc/app/env.sh" >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Setup Deploy Directory**:
   ```bash
   mkdir ~/deploy
   chmod 755 ~/deploy
   ```

## GitHub Actions Setup

1. **Add Repository Secrets**:
   ```
   AWS_REGION: your-region
   EC2_INSTANCE_ID: your-instance-id
   EC2_AVAILABILITY_ZONE: your-az
   EC2_HOST: your-instance-ip
   ```

2. **IAM Role Requirements**:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "ec2:DescribeInstances",
                   "ec2-instance-connect:SendSSHPublicKey"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

## Validation Steps

1. **Check Docker Installation**:
   ```bash
   docker --version
   docker ps
   ```

2. **Test Environment**:
   ```bash
   echo $OPENAI_API_KEY  # Should show your API key
   ```

3. **Check Application Port**:
   ```bash
   sudo netstat -tulpn | grep 8000
   ```

## Monitoring Setup

1. **Install CloudWatch Agent**:
   ```bash
   sudo yum install amazon-cloudwatch-agent -y
   ```

2. **Configure Basic Monitoring**:
   ```bash
   sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
   ```

## Maintenance

1. **Log Rotation**:
   ```bash
   sudo nano /etc/logrotate.d/docker
   ```
   Add:
   ```
   /var/lib/docker/containers/*/*.log {
       rotate 7
       daily
       compress
       size=10M
   }
   ```

2. **Cleanup Script**:
   ```bash
   # Add to crontab
   echo "0 0 * * 0 docker system prune -f" | sudo tee -a /var/spool/cron/ec2-user
   ```

## Troubleshooting

1. **Check Docker Logs**:
   ```bash
   docker logs ai6-interview
   ```

2. **Check System Resources**:
   ```bash
   top
   df -h
   docker stats
   ```

3. **Common Issues**:
   - Port already in use: `sudo lsof -i :8000`
   - Docker permission issues: `groups` (should include docker)
   - Deployment failures: Check GitHub Actions logs

## Backup Strategy

1. **Create AMI Monthly**:
   ```bash
   # Note: Can be automated via AWS CLI
   aws ec2 create-image \
     --instance-id $INSTANCE_ID \
     --name "ai6-interview-backup-$(date +%Y%m%d)" \
     --description "Monthly backup"
   ```

## References
- [Amazon Linux 2023 Guide](https://docs.aws.amazon.com/linux/al2023/ug/)
- [Docker Installation](https://docs.docker.com/engine/install/)
- [EC2 Instance Connect](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Connect-using-EC2-Instance-Connect.html) 