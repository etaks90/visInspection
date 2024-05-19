import streamlit as st
from PIL import Image
import io

def process_image(image_data):
    """ A function to process the image. For example, print its dimensions. """
    image = Image.open(image_data)
    st.write("Image dimensions:", image.size)  # Prints dimensions

    predicted_label = "def"
    return predicted_label

def main():
    st.title("Image Upload Demo")

    # Create a file uploader to upload images
    uploaded_file = st.file_uploader("Drag and Drop or Click to Upload an Image", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        

        # Display the uploaded image
        image_data = io.BytesIO(uploaded_file.getvalue())
        # Process the image (example function)
        predicted_label = process_image(image_data)
        image = Image.open(image_data)
        # To See details
        file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type,
                        "filesize": uploaded_file.size,
                        "true-label": uploaded_file.name.split("_")[1],
                        "predicted-label": predicted_label
                        }
        st.write(file_details)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        

if __name__ == "__main__":
    main()
