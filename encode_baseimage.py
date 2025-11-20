import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import uuid
import os

st.set_page_config(page_title="AVIF → JPG API", page_icon="🖼️")

st.title("AVIF → JPG API Converter")
st.write("Use this API like:<br>https://your-app.streamlit.app/?url=IMAGE_URL", unsafe_allow_html=True)

# Read ?url= parameter
params = st.query_params
img_url = params.get("url", [""])[0]

user_url = st.text_input("Input Image URL:", value=img_url)

if st.button("Convert") and user_url.strip():
    try:
        # Download input image
        r = requests.get(user_url, timeout=15)
        r.raise_for_status()

        # Convert to JPG
        img = Image.open(BytesIO(r.content)).convert("RGB")

        # Save JPG in static directory
        file_id = str(uuid.uuid4()) + ".jpg"
        save_path = f"static/{file_id}"

        os.makedirs("static", exist_ok=True)

        img.save(save_path, format="JPEG")

        # Public URL
        public_url = f"{st.request.url.rsplit('/',1)[0]}/static/{file_id}"

        st.success("✔ Conversion Successful")
        st.subheader("JPG File URL:")
        st.write(public_url)

    except Exception as e:
        st.error(f"❌ Failed to convert: {e}")
