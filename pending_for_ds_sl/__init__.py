import logging
import json
import azure.functions as func
import os
from azure.cosmos import exceptions, CosmosClient, PartitionKey

def connect():
    
        # return func.HttpResponse(json.dumps({'error':'Connection Strings are not set'}),headers={"content-type":"application/json"},status_code=500)
    try:
        client = CosmosClient('https://alpha-audit-cosmosdb.documents.azure.com:443/', 'y2tpZTwiwaScnl1twmWZm7WsYlzGiPLM1a2EYipN1EBObkZZqz3fzldqjQE14H3ehx1njvOdDL4jgUZQLx4QQw==')
        database_name = 'beta-project-db'
        database = client.get_database_client(database_name)
        container_name = 'attachment_object_metadata'
        container = database.get_container_client(container_name)
        return {'container':container}
    except exceptions.CosmosResourceNotFoundError as rnef:
        logging.info("============Exception========%r",str(rnef))
        return {'error':str(rnef)}
    except Exception as e:
        logging.info("============Exception========%r",str(e))
        return {'error':str(e)}

def get_record(container,location):
    try:
        # NOTE: Use MaxItemCount on Options to control how many items come back per trip to the server
        #       Important to handle throttles whenever you are doing operations such as this that might
        #       result in a 429 (throttled request)
        # item_list = list(container.read_all_items(max_item_count=10))
        
        q = "SELECT * FROM c WHERE c.location="+"'"+location+"' and (c.digi_signed=null or c.digi_signed=0)"
        print("================",q)
        items = list(container.query_items(query=q,
        enable_cross_partition_query=True
    ))
        return func.HttpResponse(json.dumps(items),headers={"content-type":"application/json"},status_code=200)
    except Exception as e:
        logging.info('==========ERROR IN GETTING EMPLOYEES====22===.%r',e)
        return func.HttpResponse(json.dumps({'error':str(e)}),headers={"content-type":"application/json"},status_code=500)



def main(req: func.HttpRequest) -> func.HttpResponse:
    location=req.params.get('location','')
    container = connect()
    if container.get('error'):
        return func.HttpResponse(json.dumps(container),headers={"content-type":"application/json"},status_code=500)
    try:
        return get_record(container['container'],location.upper())
    except Exception as e:
        logging.info('==========ERROR IN GETTING EMPLOYEES===11====.%r',e)
        return func.HttpResponse(json.dumps({'error':e}),headers={"content-type":"application/json"},status_code=500)