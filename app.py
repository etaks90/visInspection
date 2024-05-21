import streamlit as st
import pandas as pd
import numpy as np

def print_file_names(uploaded_files):
    for uploaded_file in uploaded_files:
        print(uploaded_file.name)

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

    if st.button('Print File Names'):
        if uploaded_files:
            print_file_names(uploaded_files)
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

if __name__ == "__main__":
    main()
