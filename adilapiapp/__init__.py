import logging
import json
import azure.functions as func
from utility.db_con import connect

def get_employees(container):
    try:
        # NOTE: Use MaxItemCount on Options to control how many items come back per trip to the server
        #       Important to handle throttles whenever you are doing operations such as this that might
        #       result in a 429 (throttled request)
        item_list = list(container.read_all_items(max_item_count=10))
        return func.HttpResponse(json.dumps(item_list),headers={"content-type":"application/json"},status_code=200)
    except Exception as e:
        logging.info('==========ERROR IN GETTING EMPLOYEES=======.%r',e)
        return func.HttpResponse(json.dumps({'error':str(e)}),headers={"content-type":"application/json"},status_code=500)

def get_employee(container,item_id,partition_key):
    try:
        response = container.read_item(item=item_id, partition_key=partition_key)
        return func.HttpResponse(json.dumps(response),headers={"content-type":"application/json"},status_code=200)
    except Exception as e:
        logging.info('==========ERROR IN GETTING EMPLOYEES=======.%r',e)
        return func.HttpResponse(json.dumps({'error':e}),headers={"content-type":"application/json"},status_code=500)


def main(req: func.HttpRequest) -> func.HttpResponse:
    container = connect()
    if container.get('error'):
        return func.HttpResponse(json.dumps(container),headers={"content-type":"application/json"},status_code=500)
    try:
        req_body = req.get_json()
        logging.info('==========RESPONSE JSon=======.%r',req.get_json())
        # if req_body.get('id') and req_body.get('department'):
        return get_employee(container['container'], req_body.get('id'), req_body.get('department'))
    except ValueError:
        return get_employees(container['container'])
    except Exception as e:
        logging.info('==========ERROR IN GETTING EMPLOYEES=======.%r',e)
        return func.HttpResponse(json.dumps({'error':e}),headers={"content-type":"application/json"},status_code=500)


    
