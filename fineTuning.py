from openai import OpenAI
import vectordb
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.environ['OPENAI_API_KEY']
organization_id = os.environ['ORGANIZATION_ID_OPENAI']
client = OpenAI()

def create_embeddings_by_prompt(propmpt):
    embedding = client.embeddings.create(input=[propmpt], model="text-embedding-3-small")
    vectors = embedding.data[0].embedding
    return vectors

def create_context(prompt):
    best_chunks_on_vectors_score = vectordb.getHighestScoreByPrompt(prompt)
    context = ''
    for row in best_chunks_on_vectors_score:
        context += row.text
        context += " "
    return context