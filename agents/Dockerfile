FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY security_agent.py .

EXPOSE 8000

CMD ["uvicorn", "security_agent:app", "--host", "0.0.0.0", "--port", "8000"]
