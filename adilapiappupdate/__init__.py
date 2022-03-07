import logging
import os
import json
import azure.functions as func
from webbrowser import get
from azure.cosmos import exceptions, CosmosClient, PartitionKey


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if not (os.getenv('END_POINT_URI') and os.getenv('PRIMARY_KEY')):
        return func.HttpResponse(json.dumps({'error':'Connection Strings are not set'}),headers={"content-type":"application/json"},status_code=500)
    try:
        client = CosmosClient(os.environ['END_POINT_URI'], os.environ['PRIMARY_KEY'])
        database_name = 'adilcosmosdb'
        database = client.get_database_client(database=database_name)
        container_name = 'adilcosmoscontainer'
        container = database.get_container_client(container_name)
    except exceptions.CosmosResourceNotFoundError:
        logging.info('==========ERROR IN CREATING EMPLOYEES=======.%r',e)
        return func.HttpResponse(json.dumps({'error':'The Given container or db not found'}),headers={"content-type":"application/json"},status_code=500)
    try:
        req_body = req.get_json()
        logging.info('==========RESPONSE JSon=======.%r',req.get_json())
        read_item = container.read_item(item=req_body.get('id'), partition_key=req_body.get('department'))
        if read_item:
            # read_item['experience'] = '3 years'
            read_item.update(req_body)
            response = container.upsert_item(body=read_item)
            status_code = 200
        else:
            response = {'error':'Item Not Found'}
            status_code = 404
        # if req_body.get('id') and req_body.get('department'):
    except ValueError as value_error:
        logging.info('==========ERROR IN CREATING EMPLOYEES=11======.%r',value_error)
        response = {'error':str(value_error)}
        status_code = 400
    except TypeError as type_error:
        logging.info('==========ERROR IN CREATING EMPLOYEES==22=====.%r',type_error)
        response = {'error':str(type_error)}
        status_code = 400
    except Exception as e:
        logging.info('==========ERROR IN CREATING EMPLOYEES===33====.%r',e)
        response = {'error':str(e)}
        status_code = 500

    return func.HttpResponse(json.dumps(response),headers={"content-type":"application/json"},status_code=status_code)
