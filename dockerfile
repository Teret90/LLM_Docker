FROM python:3.11-slim

WORKDIR /LLM_Docker

COPY . /LLM_Docker

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "openai_recetas.py"]