# Requirements

1. Langchain [have all functionalities - vectorDB, LLM, etc]
2. LLM - OpenAI gpt 3.5-turbo
3. Vector DB - FAISS (implemented by FacebookAI) - It is a local vector DB
4. FastAPI for UI [Alternative: Flask, Django, Falcon, Streamlit, etc]


# Structure
1. User uploads a PDF file
2. Extract docs (everything is a doc)
3. Since LLM has input token limit, split the docs into chunks [x tokens per chunk]
4. We will be using an embedding model to create vector embeddings [convert the chunks / text into vectors]
5. Store the vector embeddings in a vector DB (KNOWLEDGE BASE)
6. On vector embeddings, we will be using a similarity search algorithm to find the most similar chunks to the user's question
7. Pass the most similar chunks to the LLM to answer the user's question (Set a prompt here for the LLM to performs the task)
8. Return the answer to the user

PDF -> Extract docs -> Split into chunks -> Create prompt & optionally refine it to run in a chain for LLM to generate questions

==> In order to generate answers, we need to store the documents in a vector DB / Memory.

For that, use embedding model on chunks -> Create vector embeddings -> Store in vector DB (KNOWLEDGE BASE) -> Perform similarity search -> Answer the question

Prompt -> LLM  -> KNOWLEDGE BASE -> Interview Questions

Interview Questions -> LLM -> Answers


# Steps

1. Create a new virtual environment
```
conda create -n ai6 python=3.10 -y
```

2. Activate the virtual environment
```
conda activate ai6
```

3. Install the requirements
```
pip install -r requirements.txt
```

4. Run the app
```
uvicorn app:app --reload
```

# Push to Github

1. Finalize the versions of the packages in the requirements.txt using pip list
2. Pull & Push to Github

# Preparing for deployment
1. requirements.txt: import aws-wsgi 
2. app.py: import awsgi and add handler function

# Deploying the app on EC2

1. Create Github workflow and configure  variables
2. Trigger the workflow manually from the Actions tab in Github

3. First, create Target Group:
    EC2 Console → Target Groups → Create target group
    - Choose target type: Instances
    - Target group name: interview-app-tg
    - Protocol: HTTP
    - Port: 8000
    - VPC: Select your EC2's VPC (default VPC)
    - Health check settings:
        - Protocol: HTTP
        - Path: /
        - Port: traffic port (8000)
        - Healthy threshold: 2
        - Unhealthy threshold: 2
        - Timeout: 5
        - Interval: 30
        - Success codes: 200
    Click 'Next'
    - Select your EC2 instance
    - Click 'Include as pending below'
    - Click 'Create target group'

4. Create Application Load Balancer:
    EC2 Console → Load Balancers → Create load balancer
    - Select Application Load Balancer

    Basic configuration:
    - Load balancer name: interview-app-alb
    - Scheme: Internet-facing
    - IP address type: IPv4

    Network mapping:
    - VPC: Same as your EC2 (default VPC)
    - Select at least two Availability Zones

    Security groups:
    - Create new security group
    - Name: alb-sg
    - Description: ALB security group
    - Inbound rules:
        - Allow HTTP (80) from anywhere
        - Allow HTTPS (443) from anywhere

    Listeners and routing:
    - HTTPS:443
    - Protocol: HTTPS
    - Select your ACM certificate
    - Default action: Forward to interview-app-tg
    - HTTP:80
    - Protocol: HTTP
    - Default action: Redirect to HTTPS:443

    Click 'Create load balancer'

5. Update EC2 Security Group:
    EC2 Console → Security Groups → Your EC2's security group
    Add inbound rule:
    - Type: Custom TCP
    - Port: 8000
    - Source: Select the ALB security group (alb-sg)
    - Description: Allow ALB traffic

6. Verify Setup:
    - Check Target Group health
    EC2 Console → Target Groups → interview-app-tg
    Look at 'Targets' tab - EC2 should show as 'healthy'

    - Get ALB DNS name
    EC2 Console → Load Balancers → interview-app-alb
    Copy the 'DNS name'

    - Test in browser:
    http://[ALB-DNS-NAME]
    https://[ALB-DNS-NAME]

6. Create a new ACM Certificate in AWS Certificate Manager

7. Update the Route 53 configuration and ALB settings with the new domain name
