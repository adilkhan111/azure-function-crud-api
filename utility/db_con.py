import logging
import os
from azure.cosmos import exceptions, CosmosClient, PartitionKey

def connect():
    if not (os.getenv('END_POINT_URI') and os.getenv('PRIMARY_KEY')):
        return {'error':'Connection Strings are not set'}
        # return func.HttpResponse(json.dumps({'error':'Connection Strings are not set'}),headers={"content-type":"application/json"},status_code=500)
    try:
        client = CosmosClient(os.environ['END_POINT_URI'], os.environ['PRIMARY_KEY'])
        database_name = 'adilcosmosdb'
        database = client.get_database_client(database_name)
        container_name = 'adilcosmoscontainer'
        container = database.get_container_client(container_name)
        return {'container':container}
    except exceptions.CosmosResourceNotFoundError as rnef:
        logging.info("============Exception========%r",str(rnef))
        return {'error':str(rnef)}
    except Exception as e:
        logging.info("============Exception========%r",str(e))
        return {'error':str(e)}