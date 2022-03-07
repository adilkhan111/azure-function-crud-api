import logging
import json
import azure.functions as func
from utility.db_con import connect


def main(req: func.HttpRequest) -> func.HttpResponse:
    container = connect()
    if container.get('error'):
        return func.HttpResponse(json.dumps(container),headers={"content-type":"application/json"},status_code=500)
    try:
        req_body = req.get_json()
        logging.info('==========RESPONSE JSon=======.%r',req.get_json())
        response = container['container'].create_item(body=req_body)
        status_code = 201
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