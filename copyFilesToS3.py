from dotenv import load_dotenv
from azure.identity import DeviceCodeCredential
from azure.identity import ClientSecretCredential

import json
from msgraph import GraphServiceClient
import os
import asyncio
import configparser
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
import documentsService
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
load_dotenv()



s3 = documentsService.s3
bucket_name = 'tbscg-internal-hr-documents-bucket' 


scopes = ['AllSites.Read, AllSites.Write, MyFiles.Read, MyFiles.Write, Sites.Search.All']

tenant_id = os.environ['AZURE_TENANT']
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

# azure.identity
# credential = DeviceCodeCredential(
#     tenant_id=tenant_id,
#     client_id=client_id,
#     client_secret = client_secret
#     )
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret = client_secret
    )


graph_client = GraphServiceClient(credential, scopes)

sourceFolderId = os.environ['SHAREPOINT_FOLDER_ID']

# async def copyFilesToS3(folderId):
#     print(folderId)
#     print('/me/drive/items/'+folderId+'/children')
#     response = await graph_client.api('/me/drive/items/'+folderId+'/children').get()
#     print(response)
#     for item in response.value :
#         if item.folder :
#             await copyFilesToS3(item.id)
#         else :
#             fileContent = await graph_client.api('/me/drive/items/'+ item.id+'/content').get()
            
#             params = {
#                 "Bucket": bucket_name,
#                 "Key": folderId+'/'+item.name,
#                 "Body": fileContent
#             }
            
#             await s3.upload(params).promise()
#             print('Copied file '+ item.id+' to S3')
url1 = "https://graph.microsoft.com/v1.0/sites/tbscg370.sharepoint.com:/sites/"
url2 = "https://graph.microsoft.com/v1.0/sites/7537c4e4-7513-4880-8998-53737a129b84/lists/"
url3 = "https://graph.microsoft.com/v1.0/sites/zheguo.sharepoint.com,91a47a59-db5e-4d17-a689-479ee8905533,274459c9-4c96-42bf-9b96-838ffa387aaa/drive/root:/X:/children"
async def copyFilesToS3(folderId):
    user = await graph_client.me.get()
    # user_dict = await user.json()
    print("user_dict")
    # response = graph_client.api('/me/drive/items/'+folderId+'/children').get()
    # drives = await graph_client.sites.by_site_id(tenant_id).lists.get()
    # print("items")
    # print(drives)

    # for item in response.value :
    #     if item.folder :
    #         copyFilesToS3(item.id)
    #     else :
    #         fileContent = graph_client.api('/me/drive/items/'+ item.id+'/content').get()
            
    #         params = {
    #             "Bucket": bucket_name,
    #             "Key": folderId+'/'+item.name,
    #             "Body": fileContent
    #         }
            
    #         s3.upload(params).promise()
    #         print('Copied file '+ item.id+' to S3')

def copy_files():
    return copyFilesToS3(sourceFolderId)