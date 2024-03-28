from fastapi import APIRouter, Response
import documentsService
import embeddings
import vectordb
import copyFilesToS3
import fineTuning

router = APIRouter(prefix="/f-t")


@router.get("/list-s3-files")
def get_file_List_s3():
    return documentsService.getListOfDocumentsOnS3()

@router.get("/document-text")
def get_document_text(key):
    return documentsService.getPdfFileTextFromS3(key)


@router.post("/create-embeddings-on-single-document")
def create_embeddings_on_document(key):
    return documentsService.create_embeddings_pdf_by_key(key)

@router.post("/create-embeddings-on-all-documents")
def create_embeddings_on_all_documents():
    return embeddings.create_embeddings_for_all_files()

@router.post("/get-all-embeddings-from-db")
def get_all_embeddings():
    return vectordb.getAllEmbeddings()

@router.post("/create-context")
def create_context(prompt: str):
    response = Response(content=embeddings.create_context(prompt))
    print(response)
    return response

@router.get("/fine-tuning-from-all-docs")
def fine_tuning():
    return fineTuning.finetuning_for_all_documents()

@router.get("/copy-files-from-sharepoint-to-s3")
def copy_files():
    return copyFilesToS3.copy_files()
