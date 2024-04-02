FROM python:3.12

WORKDIR /app

COPY . .
COPY singlestore_bundle.pem /usr/local/lib/python3.12/
COPY singlestore_bundle.pem /usr/local/share/ca-certificates/

COPY requirements.txt .

RUN apt-get update 
RUN apt-get install python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python-is-python3
RUN apt-get update 

ENV AWS_ACCESS_KEY_ID=yourdata
ENV AWS_SECRET_ACCESS_KEY=yourdata
ENV AWS_REGION=yourdata
#TBSCG
ENV ORGANIZATION_ID_OPENAI=yourdata
ENV OPENAI_API_KEY=yourdata
ENV MODEL_NAME=yourdata
#MY_OWN
ENV SINGLESTORE_USERNAME=yourdata
ENV SINGLESTORE_PASSWORD=yourdata

ENV ECR_REPO=yourdata

EXPOSE 7000
 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV CURLOPT_SSL_VERIFYHOST=0
ENV CURLOPT_SSL_VERIFYPEER=0
ENV PYTHONUNBUFFERED=1

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]