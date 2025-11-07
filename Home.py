from AIResource import GeminiRequest
import streamlit as st
import os

gemini_request = GeminiRequest("gemini-2.5-flash-image")

def run(): 
    image_path = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    with open(image_path.name, "wb") as f:
        f.write(image_path.getbuffer())

    prompt = "Add beer to this image. Either a beer bottle or a beer glass where it is most suitable"

    if st.button("Add beer") and image_path is not None:
        with st.spinner("Generating..."):
            gemini_request.edit_images(prompt, image_path.name)

            # Display the generated image
            st.image("generated_image.png")

            os.remove(image_path.name)

run()