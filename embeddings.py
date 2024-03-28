from openai import OpenAI
import vectordb
import documentsService
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

def create_embeddings_for_all_files():
    titles_list = documentsService.getListOfDocumentsOnS3()
    filtered_list = [title for title in titles_list if ".pdf" in title]
    print(filtered_list)
    for file_key in filtered_list:
        documentsService.create_embeddings_pdf_by_key(file_key)