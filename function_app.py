import azure.functions as func
import logging, os, json, sys, codecs
from lib.utils import *
import pandas as pd

##########################################################################################
##########################PREPARE STUFF################################################
###########################################################################################
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

##########################################################################################
##########################AZURE FUNCTION STUFF################################################
##########################################################################################

# FUNCTIONS
app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="image-uploads",
                               connection="connectionVisualInspection") 
def trigger_image_evaluation(myblob: func.InputStream):
    """
    For some reason the variable 'myblob.name' starts with the container_name. Therefore
    we remove this below.
    """
    fp__img__blob = "/".join(myblob.name.split("/")[1:])
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"fp__img__blob: {fp__img__blob}"
                f"Blob Size: {myblob.length} bytes")
    
    
    

    # EVAL
    prob__ok = eval_img_from_blob(loaded_model, blob_service_client, container_name, fp__img__blob)

    # LOG TO DB
    j__db = {"FN__BLOB" : fp__img__blob.split("/")[-1], "CONTAINER_NAME" : container_name, "PROBABILITY_OK": round(prob__ok, 4), "FP__BLOB" : fp__img__blob}
    logging.info(j__db)
    df = pd.DataFrame(j__db, index=[0])
    df.to_sql(log_table, eng, schema=log_schema, if_exists="append", index=False)
