import azure.functions as func
import os, json, sys, codecs
from lib.utils import *
import pandas as pd
import logging

# Create logger
logger = logging.getLogger('log_az_func')
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
# PARAM
j_config = get_config()
# DB CONNECTION
eng = get_engine()

# BLOB CONNECTION
blob_service_client = get_blob_service_client(j_config["connection_string"])

# model
loaded_model = get_keras_model(blob_service_client, j_config["model_src"], r"C:\Users\oliver.koehn\Documents\gitProjects\qualityInspection\examples\trained_model.keras")

##########################################################################################
##########################AZURE FUNCTION STUFF################################################
##########################################################################################
# FUNCTIONS
app = func.FunctionApp()

def main(myblob: func.InputStream):
    """
    For some reason the variable 'myblob.name' starts with the container_name. Therefore
    we remove this below.
    """
    logging.info("blablubb2 az_function log")
    print("blablubb2 az_function print")
    fp__img__blob = "/".join(myblob.name.split("/")[1:])

    j_config["fp__img__blob"] = fp__img__blob

    eval_to_db(loaded_model, blob_service_client, eng, j_config)
