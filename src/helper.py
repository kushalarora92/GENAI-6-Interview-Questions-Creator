from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA    
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import FAISS

import os
from dotenv import load_dotenv
from src.prompt import prompt_template, refine_prompt_template

# OpenAI Authentication
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# could also be a class if a lot of functions

def file_processing(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    question_gen = ''
    for page in documents:
        question_gen += page.page_content

    splitter_question_gen = TokenTextSplitter(model_name="gpt-3.5-turbo", chunk_size=10000, chunk_overlap=200)
    chunks_question_gen = splitter_question_gen.split_text(question_gen)
    documents_question_gen = [Document(page_content=t) for t in chunks_question_gen]

    
    splitter_answer_gen = TokenTextSplitter(model_name="gpt-3.5-turbo", chunk_size=1000, chunk_overlap=100)
    documents_answer_gen = splitter_answer_gen.split_documents(documents_question_gen)

    return documents_question_gen, documents_answer_gen


def llm_pipeline(file_path):
    documents_question_gen, documents_answer_gen = file_processing(file_path)

    llm_ques_gen_pipeline = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

    PROMPT_QUESTIONS = PromptTemplate(template=prompt_template, input_variables=["text"])

    REFINE_PROMPT_QUESTIONS = PromptTemplate(template=refine_prompt_template, input_variables=["existing_answer", "text"])

    ques_gen_chain = load_summarize_chain(llm=llm_ques_gen_pipeline,
                             chain_type="refine",
                             verbose=True,
                             question_prompt=PROMPT_QUESTIONS,
                             refine_prompt=REFINE_PROMPT_QUESTIONS)
    
    ques = ques_gen_chain.run(documents_question_gen)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents_answer_gen, embeddings) # It will store in memory;

    llm_answer_gen = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)

    ques_list = ques.split("\n")
    filtered_ques_list = [element for element in ques_list if element.endswith("?") or element.endswith(".")]

    answer_gen_chain = RetrievalQA.from_chain_type(
        llm=llm_answer_gen, chain_type="stuff", retriever=vector_store.as_retriever()
    )

    return filtered_ques_list, answer_gen_chain