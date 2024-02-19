import streamlit as st
from gtts import gTTS
import time
from utils import upload, process_image_with_yolo, generate_recipe, message

# Custom CSS for headings
heading_styles = '''
    <style>
        .fancy-heading {
            font-family: 'Pacifico', cursive;
            font-size: 48px;
            text-align: center;
            color: #FF3399;
            text-shadow: 2px 2px 4px #333;
        }

        .sub-heading {
            font-family: 'Raleway', sans-serif;
            font-size: 28px;
            text-align: center;
            color: #0099FF;
        }
    </style>
'''

# Display custom heading styles
st.markdown(heading_styles, unsafe_allow_html=True)

# Main heading and sub-heading
st.markdown(f'<p class="fancy-heading">🌈 Culinary Wizard 🌈</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-heading">Discover Magical Recipes with AI</p>', unsafe_allow_html=True)

# Image
st.image('working.jpg', use_column_width=True)

# Function to handle main logic
def main():
    if st.checkbox('📸 Take a Picture for Prediction'):
        image, original_image, image_filename = upload()
        if original_image is not None and image_filename is not None and len(image_filename) != 0 and st.checkbox('🔮 Prediction'):
            st.info('⏳ Wait for the results...')
            pic0 = image
            uniquelist = process_image_with_yolo(pic0)
            if uniquelist:
                for i, j in uniquelist.items():
                    st.write(uniquelist)
                language_mapping = {
                    'Telugu': 'te',
                    'Malayalam': 'ml',
                    'Hindi': 'hi',
                    'Kannada': 'kn',
                    'Tamil': 'ta'
                }
                recipe_count_mapping = {
                    '1': 1,
                    '2': 2,
                    '3': 3
                }
                language = st.selectbox('🗣️ Choose the Language for the Recipe', list(language_mapping.keys()))
                recipe_count = st.selectbox('📝 How Many Recipes Do You Want?', ['1', '2', '3'])
                if st.button('🍽️ Generate Recipe'):
                    final_result = generate_recipe(uniquelist, language_mapping[language], recipe_count_mapping[recipe_count])
                    st.write(final_result)
                    text_to_speech = final_result
                    tts = gTTS(text=text_to_speech, lang=language_mapping[language])
                    audio_path = 'saved_audio.wav'
                    tts.save(audio_path)
                    st.balloons()
                    with st.spinner('🔊 Wait for the Audio Version...'):
                        time.sleep(3)
                    st.audio(audio_path, format='audio/wav')
            else:
                message()

if __name__ == '__main__':
    main()
