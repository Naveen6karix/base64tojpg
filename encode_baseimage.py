import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="AVIF → JPG API Converter")

st.title("🖼 AVIF → JPG API Converter")
st.write("Use this API like:")
st.code("https://your-app.streamlit.app/?url=IMAGE_URL")

# Read URL parameter correctly
params = st.query_params
img_url = params.get("url", [None])[0]

# Text input (also filled automatically if ?url= is passed)
url = st.text_input("Input Image URL:", value=img_url or "")

if url:
    try:
        response = requests.get(url)
        response.raise_for_status()

        image = Image.open(io.BytesIO(response.content)).convert("RGB")

        # Convert to JPG
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        st.success("✅ Conversion Successful!")
        st.image(image, caption="Converted Image (JPG)")

        st.download_button(
            label="Download JPG",
            data=img_bytes,
            file_name="converted.jpg",
            mime="image/jpeg"
        )

    except Exception as e:
        st.error(f"❌ Failed to convert: {e}")
