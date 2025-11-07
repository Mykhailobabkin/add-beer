from AIResource import GeminiRequest
import streamlit as st
import os

import tempfile


gemini_request = GeminiRequest("gemini-2.5-flash-image")

def run(): 
    st.title("Beer Image Editor")
    
    image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    prompt = "Add beer to this image. Either a beer bottle or a beer glass in hand of a person where it is most suitable"

    if st.button("Add beer") and image_file is not None:
        with st.spinner("Adding beer..."):
            # Create a temporary file to store the uploaded image
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_file.name)[1]) as tmp_file:
                tmp_file.write(image_file.getbuffer())
                tmp_path = tmp_file.name

            gemini_request.edit_images(prompt, tmp_path)

            # Display the generated image
            st.image("generated_image.png")
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
run()