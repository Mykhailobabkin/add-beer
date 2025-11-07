from AIResource import GeminiRequest
import streamlit as st
import os
import tempfile

gemini_request = GeminiRequest("gemini-2.0-flash-exp")

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
            
            try:
                # Call the edit_images method
                gemini_request.edit_images(prompt, tmp_path)
                
                # Check if the generated image exists
                if os.path.exists("generated_image.png"):
                    st.success("Beer added successfully!")
                    st.image("generated_image.png")
                else:
                    st.error("Failed to generate image. Please try again.")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

if __name__ == "__main__":
    run()