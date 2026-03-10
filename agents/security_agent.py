from fastapi import FastAPI
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import os

app = FastAPI()

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://host.docker.internal:11434"
)

llm = Ollama(
    model="llama3",
    base_url=OLLAMA_BASE_URL
)

prompt_template = PromptTemplate(
    input_variables=["input"],
    template="""
You are a Security Analyst AI.

If the user asks about a vulnerability (CVE),
respond ONLY in this JSON format:

{{
  "action": "vuln_lookup",
  "cve": "CVE-XXXX-YYYY"
}}

Otherwise, respond with:

{{
  "action": "answer",
  "text": "your explanation"
}}

User query:
{input}
"""
)

@app.post("/run")
def run(data: dict):
    prompt = prompt_template.format(input=data["prompt"])
    result = llm.invoke(prompt)
    return {"raw": result}
