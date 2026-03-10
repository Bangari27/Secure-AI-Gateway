from fastapi import FastAPI
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate


app = FastAPI()

llm = Ollama(
    model="mistral",
    base_url="http://localhost:11434"
)

prompt_template = PromptTemplate(
    input_variables=["input"],
    template="""
You are a DevOps Engineer AI.
Answer the following infrastructure question clearly and safely.

Question:
{input}
"""
)

@app.post("/run")
def run(data: dict):
    prompt = prompt_template.format(input=data["prompt"])
    result = llm.invoke(prompt)
    return {
        "agent": "devops-agent",
        "result": result
    }
