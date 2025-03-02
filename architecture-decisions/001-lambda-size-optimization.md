# Lambda Deployment Size Optimization

## Context
The application is a FastAPI-based service that uses LangChain, OpenAI, and FAISS for AI-powered interview question generation. When deploying to AWS Lambda, we encountered size limitations:
- Lambda has a deployment package size limit of 250MB (unzipped)
- Our initial package exceeded this limit significantly

## Initial Problem
First deployment attempt resulted in: 
```
An error occurred (InvalidParameterValueException) when calling the UpdateFunctionCode operation: Unzipped size must be smaller than 262144000 bytes
```

## Solution Attempts

### 1. Initial Package Size Reduction
- Removed unnecessary files (tests, docs, cache)
- Added cleanup commands:
  ```yaml
  find . -type d -name "__pycache__" -exec rm -rf {} +
  find . -type d -name "*.dist-info" -exec rm -rf {} +
  find . -type f -name "*.pyc" -delete
  find . -type f -name "*.pyo" -delete
  ```
- Result: Still exceeded limits

### 2. Lambda Layers Approach
Split dependencies into two layers:

1. ML Layer (`ai6-interview-questions-layer`):
   ```
   openai==0.28.0
   tiktoken==0.9.0
   faiss-cpu==1.10.0
   ```

2. Utils Layer (`ai6-interview-utils-layer`):
   ```
   langchain==0.3.18
   langchain-community==0.3.17
   langchain-core==0.3.35
   pypdf==5.3.0
   PyPDF2==3.0.1
   python-dotenv==1.0.1
   ```

3. Function Package:
   ```
   fastapi==0.115.8
   uvicorn==0.34.0
   jinja2==3.1.5
   python-multipart==0.0.20
   aws-wsgi==0.2.7
   aiofiles==24.1.0
   ```

### 3. Additional Size Optimization
Added aggressive cleanup:
```
rm -rf numpy/tests numpy/doc
rm -rf langchain/tests langchain_community/tests
rm -rf faiss/tests
rm -rf sqlalchemy/testing sqlalchemy/test
rm -rf yaml/tests yaml/examples
find . -type f -name ".c" -delete
find . -type f -name ".h" -delete
find . -type f -name ".hpp" -delete
find . -type f -name ".txt" -delete
find . -type f -name ".md" -delete
find . -type f -name "README" -delete
find . -type f -name "LICENSE" -delete
find . -type f -name "CHANGELOG" -delete
```


## Results
- ML Layer size: ~209MB
- Combined size still exceeded limits: 346MB (actual) vs 250MB (limit)
- Even with two layers and aggressive optimization, couldn't get under the Lambda size limit

## Consequences
1. Positive:
   - Better organization of dependencies
   - Clear separation of concerns
   - Reduced individual package sizes

2. Negative:
   - Still exceeded Lambda limits
   - Added complexity with layer management
   - Need to maintain multiple deployment workflows

## Alternative Considerations
Due to size limitations, considering migration to:
1. AWS ECS/Fargate
2. AWS App Runner
3. AWS Elastic Beanstalk
4. EC2 with Docker

## Decision
Need to migrate away from Lambda due to size constraints. Next steps:
1. Containerize the application
2. Choose between ECS/Fargate or App Runner
3. Set up new deployment pipeline

## References
- [AWS Lambda Quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)
- [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
- [deploy-layer.yaml](https://github.com/ai6-dev/ai6-interview-questions-creator/blob/main/.github/workflows/deploy-layer.yaml)
- [deploy-utils-layer.yaml](https://github.com/ai6-dev/ai6-interview-questions-creator/blob/main/.github/workflows/deploy-utils-layer.yaml)
- [deploy.yaml](https://github.com/ai6-dev/ai6-interview-questions-creator/blob/main/.github/workflows/deploy.yaml)
