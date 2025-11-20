import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import uuid
import os

st.set_page_config(page_title="AVIF → JPG API", layout="centered")

st.title("AVIF → JPG API Converter")
st.write("Use this API like:")
st.code("https://your-app.streamlit.app/?url=IMAGE_URL")

# Read query params (the ONLY supported way)
params = st.query_params
image_url = params.get("url", [""])[0]

if image_url:
    st.write("**Input Image URL:**")
    st.write(image_url)

    try:
        # Fetch image
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        # Convert image
        img = Image.open(BytesIO(response.content)).convert("RGB")

        # Save JPG inside /tmp (Streamlit Cloud)
        file_name = f"{uuid.uuid4()}.jpg"
        file_path = f"/tmp/{file_name}"
        img.save(file_path, "JPEG")

        # Generate public download URL
        file_bytes = open(file_path, "rb").read()
        st.write("✔ Conversion Successful")

        # Create a download link (direct)
        st.markdown(
            f"[Click here to download JPG](data:file/jpg;base64,{file_bytes.hex()})"
        )

    except Exception as e:
        st.error(f"❌ Failed to convert: {e}")

else:
    st.info("Add ?url=IMAGE_URL to use the API.")
