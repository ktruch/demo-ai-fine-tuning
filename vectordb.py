from sqlalchemy import Column, VARCHAR, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import embeddings
import json
from dotenv import load_dotenv
import os
load_dotenv()

user=os.environ['SINGLESTORE_USERNAME']
password=os.environ['SINGLESTORE_PASSWORD']
                        
engine = create_engine(f'mysql+pymysql://{user}:{password}@svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com:3333/database_54e6d?ssl_ca=/com.docker.devenvironments.code/singlestore_bundle.pem')
conn = engine.connect()

def addEmbedding(chunk:str, vector):
    data = {'chunk' : chunk, 'vector' : json.dumps(vector)}
    query = text("INSERT INTO `demo-vector-table` (text, vector) VALUES (:chunk, JSON_ARRAY_PACK(:vector))")
    result = conn.execute(query, data)
    conn.commit()
    print(result)
    return result

def getAllEmbeddings():
    query = text("SELECT * FROM `demo-vector-table`")
    result = conn.execute(query)
    return result.fetchall()

def getHighestScoreByPrompt(prompt) -> list:
    prompt_vectors = embeddings.create_embeddings_by_prompt(prompt)
    data = {'prompt_vectors' : json.dumps(prompt_vectors)}
    query = text("SELECT text, DOT_PRODUCT(vector, JSON_ARRAY_PACK(:prompt_vectors)) AS score FROM `demo-vector-table` ORDER BY score DESC LIMIT 5;")
    result = conn.execute(query, data).fetchall()
    conn.commit()
    result_list = [row for row in result]
    return result_list


