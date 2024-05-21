import logging
import azure.functions as func
import logging, os, json, sys, codecs
from lib.utils import *
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Set default encoding to UTF-8
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

    # PARAM
    connection_string = os.getenv("CSTR__BLOB__VISINSP")
    container_name = "image-uploads"
    log_schema = "VISUAL_INSPECTION"
    log_table = "LOG__VISUAL_INSPECTION"

    # DB CONNECTION
    eng = get_engine()

    # BLOB CONNECTION
    blob_service_client = get_blob_service_client(connection_string)

    # model
    loaded_model = get_keras_model(blob_service_client, "local", r"C:\Users\oliver.koehn\Documents\gitProjects\qualityInspection\examples\trained_model.keras")

    print("aaaaaaaaaaaaa")

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
