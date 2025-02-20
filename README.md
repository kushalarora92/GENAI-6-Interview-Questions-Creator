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

