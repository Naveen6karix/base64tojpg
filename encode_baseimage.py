import streamlit as st
from PIL import Image
from io import BytesIO
import requests

st.title("🖼 AVIF/WebP → JPG Converter")

# Input URL from user
img_url = st.text_input("Enter AVIF/WebP Image URL:")

if img_url:
    try:
        # Download image
        response = requests.get(img_url)
        response.raise_for_status()
        img_bytes = BytesIO(response.content)

        # Convert to JPG
        img = Image.open(img_bytes).convert("RGB")
        output = BytesIO()
        img.save(output, format="JPEG")
        output.seek(0)

        # Show image and download button
        st.image(img, caption="Converted JPG", use_column_width=True)
        st.download_button(
            label="⬇ Download JPG",
            data=output,
            file_name="converted.jpg",
            mime="image/jpeg"
        )

    except Exception as e:
        st.error(f"❌ Failed to convert: {e}")
