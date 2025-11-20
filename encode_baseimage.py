import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AVIF → JPG API", page_icon="🖼")

st.title("🖼 AVIF → JPG API Converter")

st.write("Use this API like:\n\n"
         "`https://your-app.streamlit.app/?url=IMAGE_URL`\n")


# --- Get URL from query parameters ---
query_params = st.query_params
image_url = query_params.get("url", [None])[0]

# --- UI Input ---
user_url = st.text_input("Input Image URL:", value=image_url if image_url else "")

def is_valid(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


# --- Convert Function ---
def convert_avif_to_jpg(image_url: str):
    # Download AVIF
    r = requests.get(image_url, timeout=10)
    r.raise_for_status()

    # Convert AVIF → JPG
    img = Image.open(BytesIO(r.content)).convert("RGB")
    out = BytesIO()
    img.save(out, format="JPEG")
    out.seek(0)

    return out


# --- PROCESS ---
final_url = user_url.strip()

if st.button("Convert"):

    if not final_url:
        st.error("❌ Please enter an image URL.")
    elif not is_valid(final_url):
        st.error("❌ Invalid URL. It must start with http:// or https://")
    else:
        try:
            jpg_file = convert_avif_to_jpg(final_url)

            # Create a temporary public link
            download_url = st.experimental_upload_file(
                "converted.jpg", jpg_file.getvalue(), "image/jpeg"
            )

            st.success("✔ Conversion Successful")

            if download_url:
                st.write("### API Output (JPG link):")
                st.code(download_url, language="text")
            else:
                st.error("❌ Failed to generate download URL.")

        except Exception as e:
            st.error(f"❌ Failed to convert: {e}")
