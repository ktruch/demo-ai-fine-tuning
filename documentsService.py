from typing import List
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
import boto3
import PyPDF2
import tiktoken
import vectordb



#S3 client config
role_arn = "arn:aws:iam::613546732509:role/local-app-to-copy-files-sharepoint-to-s3-role" 
role_session_name = "myLocalAppSession"
sts_client = boto3.client('sts') 
response = sts_client.assume_role( RoleArn=role_arn, RoleSessionName=role_session_name )
credentials = response['Credentials']

s3 = boto3.client( 
    's3', aws_access_key_id=credentials['AccessKeyId'], 
    aws_secret_access_key=credentials['SecretAccessKey'], 
    aws_session_token=credentials['SessionToken'] )

bucket_name = 'tbscg-internal-hr-documents-bucket' 

#OpenAI config
api_key = os.environ['OPENAI_API_KEY']
organization_id = os.environ['ORGANIZATION_ID_OPENAI']
client = OpenAI()

def getPdfFileTextFromS3(object_key: str):
    file_name = object_key.split('/')[-1]
    object_key = object_key.replace('"', "")
    s3.download_file(bucket_name, object_key, file_name)
    pdf_file = open(file_name, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    text = text.replace("\n", " ")
    pdf_file.close()

    return text



def getListOfDocumentsOnS3():
    response = s3.list_objects(Bucket=bucket_name)
    files = []
    if 'Contents' in response:
        for obj in response['Contents']:
            files.append(obj['Key'])
    return files

def create_embeddings_pdf_by_key(key):
    text = getPdfFileTextFromS3(key)
    chunk_size = 3000
    text_chunks = []
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    text_chunks.extend(chunks)
    print("Number of tokens used to create embeddings: ")
    print(get_num_of_tokens_from_string(text, "cl100k_base"))
    embeddings = []
    for chunk in chunks:
        embedding = client.embeddings.create(input=[chunk], model="text-embedding-3-small")
        embeddings.append(embedding.data[0].embedding)
        vectordb.addEmbedding(chunk, embedding.data[0].embedding)
    return embeddings


def get_num_of_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


        
    