import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps

# Page Configuration
st.set_page_config(
    page_title="Traffic Sign Recognition AI",
    page_icon="🚦",
    layout="centered"
)

# Load the Model (Cached so it doesn't reload on every click)
@st.cache_resource
def load_my_model():
    model = tf.keras.models.load_model('my_model.keras')
    return model

# Load the model immediately
try:
    model = load_my_model()
    st.success("✅ AI Model Loaded Successfully!")

except Exception as e:
    st.error(f"Error loading model: {e}")

# 3. Label Dictionary (Hardcoded for simplicity so you don't need the CSV locally)
classes = {
    0:'Speed limit (20km/h)', 1:'Speed limit (30km/h)', 2:'Speed limit (50km/h)',
    3:'Speed limit (60km/h)', 4:'Speed limit (70km/h)', 5:'Speed limit (80km/h)',
    6:'End of speed limit (80km/h)', 7:'Speed limit (100km/h)', 8:'Speed limit (120km/h)',
    9:'No passing', 10:'No passing veh over 3.5 tons', 11:'Right-of-way at intersection',
    12:'Priority road', 13:'Yield', 14:'Stop', 15:'No vehicles',
    16:'Veh > 3.5 tons prohibited', 17:'No entry', 18:'General caution',
    19:'Dangerous curve left', 20:'Dangerous curve right', 21:'Double curve',
    22:'Bumpy road', 23:'Slippery road', 24:'Road narrows on the right',
    25:'Road work', 26:'Traffic signals', 27:'Pedestrians', 28:'Children crossing',
    29:'Bicycles crossing', 30:'Beware of ice/snow', 31:'Wild animals crossing',
    32:'End speed + passing limits', 33:'Turn right ahead', 34:'Turn left ahead',
    35:'Ahead only', 36:'Go straight or right', 37:'Go straight or left',
    38:'Keep right', 39:'Keep left', 40:'Roundabout mandatory',
    41:'End of no passing', 42:'End no passing veh > 3.5 tons'
}

# UI Layout
st.title("🚦 Traffic Sign Recognition System")
st.write("Upload an image of a traffic sign, and the AI will identify it.")

#File Uploader
uploaded_file = st.file_uploader("Choose a traffic sign image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file).convert("RGB")

    # Create columns to show input vs prediction
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your Input")
        st.image(image, use_container_width=True)

        # Preprocessing Function
        def predict_sign(img):
            # Resize to 32x32 as required by the model
            img = img.resize((32, 32))
            # Convert to numpy array
            img_array = np.array(img)
            # Normalize
            img_array = img_array.astype('float32')/255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict
            prediction = model.predict(img_array)
            class_idx = np.argmax(prediction)
            confidence = np.max(prediction)

            return class_idx, confidence

        # Button to trigger prediction
        if st.button("Identify Traffic Sign"):
            with st.spinner("Analyzing image"):
                class_index, conf_score = predict_sign(image)
                result_text = classes[class_index]

                # Display Results in the second column
                with col2:
                    st.subheader("AI Prediction")
                    if conf_score > 0.8:
                        st.success(f"**{result_text}**")
                    else:
                        st.warning(f"**{result_text}**")

                        st.metric("Confidence Score", f"{conf_score*100:.2f}%")
