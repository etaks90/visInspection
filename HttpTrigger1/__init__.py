import azure.functions as func
import logging, os, json, sys, codecs
from lib.utils import *
import azure.functions as func
logger = logging.getLogger('log_http')
logger.setLevel(logging.INFO)  # Ensure logger captures info level messages
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.info("START AZ FUNC")

##########################################################################################
##########################PREPARE STUFF################################################
###########################################################################################
# Set default encoding to UTF-8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())



def main(req: func.HttpRequest) -> func.HttpResponse:

    # Check if the config exists
    try:
        j_config
        print("j_config EXISSTS")
    except:
        print(f"FIRST RUN: INITIALIZE")
        # PARAM
        j_config = get_config()
        # DB CONNECTION
        eng = get_engine()
        # BLOB CONNECTION
        blob_service_client = get_blob_service_client(j_config["connection_string"])
        # model
        loaded_model = get_keras_model(blob_service_client, j_config["model_src"])

    if 1 == 1:
        fp__img__blob = req.params.get('blob')
        print(f"CALLED WITH BLOB {fp__img__blob}")
        logger.info("blablubb2 az_function log")
        print("blablubb2 az_function print")

        j_config["fp__img__blob"] = fp__img__blob

        eval_to_db(loaded_model, blob_service_client, eng, j_config)

    return func.HttpResponse("Function executed", status_code=200)
