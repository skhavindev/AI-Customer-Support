from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

Context = open("prompt.txt", "r")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

# Initialize the LLM and chain
def create_chain(groq_api_key: str, model_name: str):
    prompt = ChatPromptTemplate.from_template(
        """You are a intelligent customer service agent who can provide comprehensive answers to any user query  The agent should answer the question based only on the context provided. Make the answer as comprehensive as possible. Use citations for the sources.

        Context: {context}

        Question: {question}"""
    )

    return (
        RunnablePassthrough.assign(context=(lambda x: x["question"]))
        | prompt
        | ChatGroq(temperature=0, model_name=model_name, groq_api_key=groq_api_key)
        | StrOutputParser()
    )

@app.post("/search", response_model=QueryResponse)
async def search(request: QueryRequest):
    try:
        # Replace with your actual Groq API key and model name
        groq_api_key = "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"
        model_name = "mixtral-8x7b-32768"

        chain = create_chain(groq_api_key, model_name)
        response = chain.invoke({"question": request.question})
        return QueryResponse(answer=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))