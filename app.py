import numpy as np
import pandas as pd
from gtts import gTTS
#from ultralytics import YOLO
import streamlit as st
import cv2
import time
import base64
import time
import shutil
import os
from PIL import Image
import base64
import random

from utils1 import message,upload,process_image_with_yolo,generate_recipe

def set_background_image(img_path):
    with open(img_path, "rb") as f:
        img_data = f.read()# Use encode() for binary data
    return base64.b64encode(img_data).decode()
 
img = set_background_image("D:\Streamlit\working (1).jpg")
page_bg_img = f"""
    <style>
    [data-testid ="stApp"]{{
        background-image: url("data:image/jpg;base64,{img}");
        background-repeat: no-repeat; /* Prevents image repeating */
        background-attachment: fixed; /* Makes image fixed */
         background-position: center center;
        background-size: cover; /* Makes image cover the entire viewport */
        }}
        </style>"""
st.markdown(page_bg_img, unsafe_allow_html=True)
    # Replace "D:\Streamlit\working.jpg" with the actual path to your image
img_path = "D:\Streamlit\working (1).jpg" 

#image uplaod through camera.

def main():
    
    st.title("CULINARY COMPANION :cooking:")

    if st.button('Take a Picture :camera:'):
        picture =st.camera_input("vegetable image")
        if picture:
            image,original_image,image_filename=upload()
        if original_image is not None and image_filename is not None and len(image_filename)!=0 and st.checkbox('Prediction'):  # Check if original_image is not None
            st.info('Wait for the results...!')
                #image1=cv2.imread(image)
            pic0=image
            uniquelist=process_image_with_yolo(pic0)
            if uniquelist:
                    
                for i,j in uniquelist.items():
                    
                    st.write(uniquelist)
                lan_dcit={
                        'Telugu':'te',
                        'Malayalam':'ml',
                        'Hindi':'hi',
                        'Kannada':'kn',
                        'Tamil':'ta'
                    }
                recip_dict={
                    'one':1,
                    'two':2,
                    'three':3
                }
                choices=['Telugu','Malayalam','Hindi','Kannada','Tamil']
                language=st.selectbox('Choose the language in which you want the recipe?',choices)
                recipe=st.selectbox('How many different types of recipes you want??',['1','2','3'])
                if st.button('Generate Recipe'):
                    
                    final_result=generate_recipe(uniquelist,lan_dcit[language],int(recipe))
                    #recipe_paragraphs=final_result.split('\n\n')
                    st.write(final_result)
                    #for i in range(recip_dict[recipe],recip_dict[recipe]+1):
                        #for i in recipe_paragraphs:
                            #st.write(i)
                        #st.write('-'*100)
                    text_to_speech = final_result
                    tts = gTTS(text=text_to_speech, lang=lan_dcit[language])
                    
                        # Save the audio file
                    audio_path = 'saved_audio.wav'
                    tts.save(audio_path)
                    
                        # Play the audio
                    st.balloons()
                    with st.spinner('Wait for the audio version................'):
                        time.sleep(3)
                    st.audio(audio_path, format='audio/wav')                                    
            else:
                message()
            
            
            
if __name__ == '__main__':
    
   
    main()

