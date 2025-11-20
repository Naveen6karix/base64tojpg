import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AVIF → JPG API", page_icon="🖼️")

st.title("AVIF → JPG API Converter")
st.write("Use this API like:")
st.code("https://your-app.streamlit.app/?url=IMAGE_URL")

# Read URL param
avif_url = st.query_params.get("url", "")

if not avif_url:
    st.warning("❗ Add URL param:  ?url=https://example.com/image.avif")
    st.stop()

st.write("### Input Image URL:")
st.code(avif_url)

try:
    # Fetch AVIF image
    response = requests.get(avif_url, timeout=15)
    response.raise_for_status()
    avif_bytes = response.content

    # Convert AVIF → JPG
    img = Image.open(BytesIO(avif_bytes)).convert("RGB")

    # Save JPEG in memory
    jpg_buffer = BytesIO()
    img.save(jpg_buffer, format="JPEG")
    jpg_buffer.seek(0)

    # Create downloadable link
    st.success("✔ Conversion Successful")

    st.download_button(
        label="⬇ Download JPG",
        data=jpg_buffer,
        file_name="converted.jpg",
        mime="image/jpeg"
    )

    # API output JSON-style
    st.write("### API Output (link only):")
    st.json({
        "status": "success",
        "jpg_download": st.experimental_get_query_params()
    })

except Exception as e:
    st.error(f"❌ Failed to convert: {e}")
