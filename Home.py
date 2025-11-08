from AIResource import GeminiRequest
import streamlit as st
import os

import tempfile


gemini_request = GeminiRequest("gemini-2.5-flash-image")

def run(): 
    st.title("Квадроберы AI")
    
    image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    prompt_beer = "Add beer to this image. Either a beer bottle or a beer glass in hand of a person where it is most suitable"

    prompt_gold = "Give a person in a photo a gold YouTube play button award in their hands, what the award looks like: a big shiny gold play button"

    prompt_silver = "Give a person in a photo a silver YouTube play button award in their hands. What the award looks like: a big shiny silver play button"

    genchoice = st.radio("What do you want to add?", ('Beer', 'Silver YouTube Button', 'Gold YouTube Button'), horizontal=True)

    if genchoice is 'Gold YouTube Button' or genchoice is 'Silver YouTube Button':
        channel_name = st.text_input("Whats your channel name?")
    
    generate_image = st.button("Add")

    if generate_image and image_file is not None:
            # Create a temporary file to store the uploaded image
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_file.name)[1]) as tmp_file:
                tmp_file.write(image_file.getbuffer())
                tmp_path = tmp_file.name

            match genchoice:
                case 'Beer':
                    with st.spinner('Pouring a cold one...'):
                        gemini_request.edit_images(prompt_beer, tmp_path)

                case 'Silver YouTube Button':
                    with st.spinner('Making you famous...'):
                        gemini_request.edit_images(prompt_silver + f"Channel name is {channel_name}", tmp_path)

                case 'Gold YouTube Button':
                    with st.spinner('Shit, you are really famous...'):
                        gemini_request.edit_images(prompt_gold + f"Channel name is {channel_name}", tmp_path)
            
            # Display the generated image
            st.image("generated_image.png")
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
run()