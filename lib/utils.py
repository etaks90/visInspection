import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
from azure.storage.blob import BlobServiceClient
from PIL import Image
import io, os, logging, tempfile
from sqlalchemy import create_engine
import pandas as pd
logger = logging.getLogger('log_utils')
logger.setLevel(logging.INFO)  # Ensure logger captures info level messages
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.info("START AZ FUNC")

def get_engine():
    username = 'rs-assess-adm'  # Include the server name suffix in the username if needed
    password = os.getenv("SQL_SERVER_PASSWORD")
    server = 'rs-assess-db-server.database.windows.net'
    database = 'qialityinspection'

    # Create the connection string for a SQL Server database
    conn_str = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={os.getenv("ODBC_DRIVE")}'
    logger.info(f"CONNECTION STRING FOR DB: {conn_str}")
    # Create the engine
    return create_engine(conn_str)

def upload_file_to_blob(blob_service_client, container_name, file_path, blob_name):
    try:
        # Create the container if it doesn't already exist
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client = blob_service_client.create_container(container_name)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Upload the file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print("File was uploaded successfully to Blob storage.")

    except Exception as e:
        print(f"An error occurred: {e}")

def get_blob_service_client(connection_string):
    logger.info(f"GET BLOB SERVICE CLIENT WITH CONECTION STRING {connection_string[:4]}***{connection_string[-4:]}")

    return BlobServiceClient.from_connection_string(connection_string)

def read_image_from_blob(blob_service_client, container_name, blob):
    logger.info(f"RUN read_image_from_blob. container_name: {container_name}; blob: {blob}")
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob)
    stream = blob_client.download_blob()

    return Image.open(io.BytesIO(stream.readall())) # image.show()

def eval_img_from_blob(loaded_model, blob_service_client, container_name, blob):
    logger.info(f"eval_img_from_blob. container_name: {container_name}; blob: {blob}")
    image = read_image_from_blob(blob_service_client, container_name, blob)
    img_array = format_image_for_model(image)
    result = loaded_model.predict(img_array)
    prob__ok = result[0][1]

    return prob__ok

def format_image_for_model(image):
    logger.info(f"format_image_for_model")
    image = image.convert('RGB')
    image = image.resize((200, 200))
    image_array = img_to_array(image)
    image_array = image_array * (1./255)
    return np.expand_dims(image_array, axis=0)

def download_file_from_blob(blob_service_client, container_name, fp_blob):
    logger.info(f"download_file_from_blob. container_name: {container_name}")
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=fp_blob)

    # Create a temporary file manually
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, "temp_model.keras")

    """
    keras does not allow to read those auto-delete files, tehrefore code it liek below.
    ChatGPT: NamedTemporaryFile in Windows behaves differently compared to Unix-based systems.
    On Windows, the temporary file created by NamedTemporaryFile cannot be opened a second time
    while it is still open in the original context, which is what TensorFlow tries to do when
    load_model is called.
    """

    try:
        # Download the blob to the temporary file
        with open(temp_file_path, "wb") as temp_file:
            download_stream = blob_client.download_blob()
            temp_file.write(download_stream.readall())
            temp_file.flush()

        # Load the model using TensorFlow/Keras
        model = tf.keras.models.load_model(temp_file_path)
        logger.info("Model loaded successfully")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return model

def get_keras_model(blob_service_client, src):
    if src == "local":
        fp_model_local = os.getenv("FP__MODEL_LOCAL")
        logger.info(f"LAOD MODEL FROM LOCAL PATH {fp_model_local}")
        return tf.keras.models.load_model(fp_model_local)
    elif src == "blob":
        fp_model_blob = os.getenv("FP__MODEL_BLOB")
        logger.info(f"LAOD MODEL FROM BLOB {fp_model_blob}")
        return download_file_from_blob(blob_service_client, "config", fp_model_blob)
    

def eval_to_db(loaded_model, blob_service_client, eng, j_config):
    # EVAL
    prob__ok = eval_img_from_blob(loaded_model, blob_service_client, j_config["container_name"], j_config["fp__img__blob"])

    # LOG TO DB
    j__db = {"FN__BLOB" : j_config["fp__img__blob"].split("/")[-1], "CONTAINER_NAME" : j_config["container_name"], "PROBABILITY_OK": round(prob__ok, 4), "FP__BLOB" : j_config["fp__img__blob"]}
    logger.info(j__db)
    df = pd.DataFrame(j__db, index=[0])
    df.to_sql(j_config["log_table"], eng, schema=j_config["log_schema"], if_exists="append", index=False)
    
def get_config():
    j_config = {"container_name" : "image-uploads"
                , "log_table" : "LOG__VISUAL_INSPECTION"
                , "log_schema" : "VISUAL_INSPECTION"
                , "connection_string" : os.getenv("CSTR__BLOB__VISINSP")
                , "model_src": os.getenv("MODEL_SRC")
                , "model_blob_name": os.getenv("MODEL_BLOB_NAME")
                }
    
    # log env for check
    for k in ["SQL_SERVER_PASSWORD", "CSTR__BLOB__VISINSP"]:
        v = os.getenv(k)
        logger.info(f"{k}: {v[:2]}***{v[-3:]}")
        
    return j_config