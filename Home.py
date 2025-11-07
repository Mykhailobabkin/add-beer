from AIResource import GeminiRequest
import streamlit as st
import os
import tempfile
from PIL import Image
from io import BytesIO

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
                # Read image bytes
                with open(tmp_path, "rb") as f:
                    image_bytes = f.read()
                
                # Open image with PIL
                image = Image.open(BytesIO(image_bytes))
                
                # Call the API
                response = gemini_request.client.models.generate_content(
                    model=gemini_request.model,
                    contents=[prompt, image],
                )
                
                # Check if response is valid
                if response is None:
                    st.error("API returned no response. Please check your API key and model availability.")
                elif not hasattr(response, 'candidates') or not response.candidates:
                    st.error("API returned empty response. The model may not support image editing or the request failed.")
                else:
                    # Process response
                    image_generated = False
                    for part in response.candidates[0].content.parts:
                        if part.text is not None:
                            st.info(f"Model response: {part.text}")
                        elif part.inline_data is not None:
                            generated_image = Image.open(BytesIO(part.inline_data.data))
                            generated_image.save("generated_image.png")
                            st.success("Beer added successfully!")
                            st.image("generated_image.png")
                            image_generated = True
                    
                    if not image_generated:
                        st.warning("The model returned a text response instead of an edited image. This model may not support image editing.")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                import traceback
                st.error(f"Traceback: {traceback.format_exc()}")
            
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

if __name__ == "__main__":
    run()