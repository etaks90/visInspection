import streamlit as st
import pandas as pd
import numpy as np
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os, datetime
from dotenv import load_dotenv
from PIL import Image
import io
import numpy as np
from io import BytesIO

load_dotenv()

def upload_file_to_blob(blob_service_client, container_name, blob_name, file_stream = None, file_path = None):
    """
    IF file_streamis provided we use the filestream, otherwise we read locally
    """
    try:
        # Create the container if it doesn't already exist
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client = blob_service_client.create_container(container_name)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        if file_stream:
            blob_client.upload_blob(file_stream, overwrite=True)
        else:
            # Upload the file
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
        print("File was uploaded successfully to Blob storage.")

    except Exception as e:
        print(f"An error occurred: {e}")

def get_blob_service_client(connection_string):
    return BlobServiceClient.from_connection_string(connection_string)

def upload_files(uploaded_files):
    for uploaded_file in uploaded_files:
        fn_original = uploaded_file.name
        print(f"UPLOAD FILE {fn_original}")
        file_stream = BytesIO(uploaded_file.getvalue())

        fn_blob = fn_original.replace(".jpeg", f"__{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.jpeg")
        fp_blob = f"{datetime.datetime.now().strftime('%Y')}/{datetime.datetime.now().strftime('%m')}/{datetime.datetime.now().strftime('%d')}/{fn_blob}"
        print(f"UPLOAD LOCAL FILE {fn_original} to BLOB AS {fn_blob}")
        print(f"fp_blob: {fp_blob}")
        upload_file_to_blob(blob_service_client, container_name, fp_blob, file_stream=file_stream)


def generate_data():
    # Simulate data generation for DataFrame
    data = {'Column1': np.random.randint(0, 100, 4),
            'Column2': np.random.randint(0, 100, 4)}
    return pd.DataFrame(data)

# Define your pages as functions
def upload_images():
    st.title('Multiple File Upload Demo')

    # Create a file uploader to accept multiple files
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

    if st.button('Upload files to blob'):
        if uploaded_files:
            upload_files(uploaded_files)
        else:
            st.write("No files uploaded yet. Please upload some files and try again.")

def dashboard():
    st.header("Visualization of evaluated images.")
    st.write("Welcome to the About Page! Learn more about what we do and our mission.")

    # Initial DataFrame
    df = generate_data()

    # Button to refresh the DataFrame
    if st.button('Refresh Data'):
        df = generate_data()  # Generate new data for the DataFrame

    # Display the DataFrame
    st.write("Here is our DataFrame:")
    st.dataframe(df)

    # Display a line chart of the DataFrame
    st.line_chart(df)
    

def main():
    st.set_page_config(page_title="My Streamlit App", layout="wide", initial_sidebar_state="collapsed")

    # Use tabs for navigation
    tab1, tab2 = st.tabs(["Upload Images", "Dashboard"])
    
    with tab1:
        upload_images()
    
    with tab2:
        dashboard()

connection_string = os.getenv("CSTR__BLOB__VISINSP")

# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = get_blob_service_client(connection_string)

container_name = "image-uploads"

# streamlit run app.py

if __name__ == "__main__":
    main()
