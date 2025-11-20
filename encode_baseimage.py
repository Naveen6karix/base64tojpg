import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(page_title="AVIF → JPG API", page_icon="🖼️")

st.title("AVIF → JPG API Converter")
st.write("Use this API like:<br>https://your-app.streamlit.app/?url=IMAGE_URL", unsafe_allow_html=True)

# ----------------------
# Read query ?url=
# ----------------------
params = st.query_params
img_url = params.get("url", [""])[0]

# Input Box
user_url = st.text_input("Input Image URL:", value=img_url)

# If URL present → auto convert
auto_convert = bool(user_url.strip())

if auto_convert and st.button("Convert"):
    try:
        # Download image
        r = requests.get(user_url, timeout=10)
        r.raise_for_status()

        img = Image.open(BytesIO(r.content)).convert("RGB")

        # Convert to JPG in memory
        output_buffer = BytesIO()
        img.save(output_buffer, format="JPEG")
        output_buffer.seek(0)

        # Generate downloadable link (base64 file)
        b64 = base64.b64encode(output_buffer.read()).decode()
        download_link = f"data:image/jpeg;base64,{b64}"

        st.success("✔ Conversion Successful")

        st.subheader("API Output (link only):")
        st.write(download_link)

        # Also provide button
        st.download_button(
            label="⬇ Download JPG",
            data=base64.b64decode(b64),
            file_name="converted.jpg",
            mime="image/jpeg"
        )

    except Exception as e:
        st.error(f"❌ Failed to convert: {e}")
