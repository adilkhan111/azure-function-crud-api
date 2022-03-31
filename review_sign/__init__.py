import logging
import json
import uuid
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import azure.functions as func
from azure.cosmos import cosmos_client,exceptions

keyVaultName = 'beta-app'
KVUri = f'https://{keyVaultName}.vault.azure.net'

credentials = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri,credential=credentials)

HOST=client.get_secret('DB-HOST').value
MASTER_KEY=client.get_secret('DB-MASTER-KEY').value
DATABASE_ID=client.get_secret('DB-ID').value
CONTAINER_ID=client.get_secret('DB-CONTAINER-ID').value

# HOST='https://review-sign.documents.azure.com:443/'
# MASTER_KEY='NTi94kLk6lQ6iL4NBkj7WQjbTw6wZU2tf9fVEYxQYJHExrCbOT2anAgqw5O3lRkTAdL8s8OEYsDameXYY4MGcQ=='
# DATABASE_ID='demo_db'
# CONTAINER_ID='demo_container_id'

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Distinct Document Type HTTP trigger function processed a request.')

    client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart",
                                    user_agent_overwrite=True)
    try:
        db = client.get_database_client(DATABASE_ID)
        print('Database with id \'{0}\' was found'.format(DATABASE_ID))

    except exceptions.CosmosResourceExistsError:
        print('Database with id \'{0}\' not found'.format(DATABASE_ID))

    # setup container for this sample
    try:
        container = db.get_container_client(CONTAINER_ID)
        print('Container with id \'{0}\' was found'.format(CONTAINER_ID))

    except exceptions.CosmosResourceExistsError:
        print('Container with id \'{0}\' not found'.format(CONTAINER_ID))

    if container:
        try:
            req_body = req.get_json()
            if not req_body.get('id'):
                return func.HttpResponse(json.dumps({'error':'ID not found in request body.'}),headers={"content-type":"application/json"},status_code=400)
            read_item = container.read_item(item=req_body.get('id'), partition_key=req_body.get('id'))
            read_item['digi_signed'] = 1
            response = container.upsert_item(body=read_item)
            return func.HttpResponse(json.dumps(read_item),headers={"content-type":"application/json"},status_code=200)

        except exceptions.CosmosResourceNotFoundError as e:
            return func.HttpResponse(json.dumps({'error':'Record not Found'}),headers={"content-type":"application/json"},status_code=404)
        except ValueError as value_error:
            logging.info('==========ERROR IN Getting POST DATA======.%r',value_error)
            return func.HttpResponse(json.dumps({'error':'Invalid Request'}),headers={"content-type":"application/json"},status_code=400)
        except Exception as e:
            logging.info('==========ERROR IN GETTING Data=======.%r',e)
            return func.HttpResponse(json.dumps({'error':str(e)}),headers={"content-type":"application/json"},status_code=500)
    else:
        return func.HttpResponse(json.dumps({'error':'Connection Error'}),headers={"content-type":"application/json"},status_code=500)