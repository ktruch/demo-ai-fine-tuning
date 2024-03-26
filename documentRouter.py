from fastapi import APIRouter, Response
import documentsService
import fineTuning
import vectordb


router = APIRouter(prefix="/f-t")


@router.get("/list")
def get_file_List_s3():
    return documentsService.getListOfDocumentsOnS3()


@router.get("/document-text")
def get_document_text(key):
    return documentsService.getPdfFileTextFromS3(key)

@router.post("/get-embeddings")
def create_embeddings_on_document(key):
    return documentsService.create_embeddings_pdf_by_key(key)

@router.post("/get-all-embeddings-from-db")
def get_all_embeddings():
    return vectordb.getAllEmbeddings()

@router.post("/create-context")
def create_context(prompt: str):
    response = Response(content=fineTuning.create_context(prompt))
    print(response)
    return response
