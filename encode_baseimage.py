import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os

st.set_page_config(page_title="AVIF → JPG API", page_icon="🖼")

st.title("🖼 AVIF → JPG API Converter")

st.write("Use this API like:")
st.code("https://your-app.streamlit.app/?url=IMAGE_URL")


# -----------------------------
# GET QUERY PARAM
# -----------------------------
params = st.query_params
image_url = params.get("url", [None])[0]


# -----------------------------
# INPUT FIELD
# -----------------------------
user_url = st.text_input("Input Image URL:", value=image_url if image_url else "")


def is_valid_url(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


# -----------------------------
# CONVERSION FUNCTION
# -----------------------------
def convert_avif_to_jpg(url: str) -> BytesIO:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    img = Image.open(BytesIO(response.content)).convert("RGB")

    output = BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)
    return output


# -----------------------------
# STATIC FOLDER FOR DOWNLOAD LINK
# -----------------------------
STATIC_FOLDER = "static"
os.makedirs(STATIC_FOLDER, exist_ok=True)


# -----------------------------
# PROCESS
# -----------------------------
if st.button("Convert"):

    if not user_url.strip():
        st.error("❌ Please enter a URL.")
    elif not is_valid_url(user_url):
        st.error("❌ Invalid URL. Must start with http:// or https://")
    else:
        try:
            jpg_data = convert_avif_to_jpg(user_url)

            output_path = os.path.join(STATIC_FOLDER, "converted.jpg")
            with open(output_path, "wb") as f:
                f.write(jpg_data.getvalue())

            # Public link (Streamlit automatically serves /static/* files)
            app_base = st.get_option("browser.serverAddress")
            app_port = st.get_option("browser.serverPort")

            download_link = f"https://{app_base}/static/converted.jpg"

            st.success("✔ Conversion Successful!")
            st.write("### API Output (JPG Link):")
            st.code(download_link)

        except Exception as e:
            st.error(f"❌ Failed to convert: {e}")
