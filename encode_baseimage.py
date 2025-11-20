import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AVIF → JPG API Converter", page_icon="🖼")

st.title("🖼 AVIF → JPG API Converter")

st.write("""Use this API like:https://your-app.streamlit.app/?url=IMAGE_URL""")

# -----------------------------------------
# READ QUERY PARAM "url"
# -----------------------------------------
params = st.query_params
img_url = params.get("url", [None])[0]

# -----------------------------------------
# INPUT BOX (auto-filled if ?url= provided)
# -----------------------------------------
url = st.text_input("Input Image URL:", value=img_url or "")

# -----------------------------------------
# PROCESS BUTTON (or auto-run if ?url= is present)
# -----------------------------------------
if url:
    try:
        # Fetch image bytes
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        img_bytes = BytesIO(response.content)

        # Convert to JPG
        img = Image.open(img_bytes).convert("RGB")
        output = BytesIO()
        img.save(output, format="JPEG")
        output.seek(0)

        st.success("✔ Conversion Successful")

        # Provide download link only
        st.download_button(
            label="⬇ Download JPG",
            data=output,
            file_name="converted.jpg",
            mime="image/jpeg"
        )

    except Exception as e:
        st.error(f"❌ Failed to convert: {e}")
