#!/bin/bash

echo "Starting EC2 instance setup..."

# Prompt for OpenAI API key
while true; do
    read -p "Enter your OpenAI API key (starts with 'sk-'): " OPENAI_API_KEY
    if [[ $OPENAI_API_KEY == sk-* ]]; then
        break
    else
        echo "Invalid API key format. Key must start with 'sk-'"
    fi
done

# Update system
echo "Updating system packages..."
sudo yum update -y

# Install Docker
echo "Installing and configuring Docker..."
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Create required directories
echo "Creating application directories..."
mkdir -p ~/deploy ~/static
chmod 755 ~/deploy ~/static

# Set environment variables
echo "Setting up environment variables..."
cat > ~/.env << EOF
OPENAI_API_KEY=$OPENAI_API_KEY
# Add other environment variables as needed
EOF
chmod 600 ~/.env

# Verify Docker installation
echo "Verifying Docker installation..."
docker --version
docker ps

echo "Setup complete! Please:"
echo "1. Log out and log back in for Docker permissions to take effect"
echo "2. Verify environment with: cat ~/.env"
echo "3. Test Docker with: docker run hello-world"

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install and start SSM agent
sudo yum install -y amazon-ssm-agent
sudo systemctl enable amazon-ssm-agent
sudo systemctl start amazon-ssm-agent

# Verify installations
echo "Verifying installations..."
docker --version
aws --version
sudo systemctl status amazon-ssm-agent

# Verify SSM agent connectivity
aws ssm get-connection-status \
  --target $INSTANCE_ID \
  --region $AWS_REGION 