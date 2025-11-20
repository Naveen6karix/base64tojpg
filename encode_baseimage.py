import streamlit as st
import base64
import requests
from io import BytesIO
from PIL import Image
import urllib.parse

st.set_page_config(page_title="AVIF to JPG API", layout="centered")

st.title("AVIF → JPG API")

# -------------------------------
# API MODE (when ?url= is present)
# -------------------------------
query = st.experimental_get_query_params()

if "url" in query:
    # Normal (not encoded) link from user
    raw_url = query["url"][0]

    # Encode the URL safely
    encoded_url = urllib.parse.quote(raw_url, safe=":/?=&")

    try:
        response = requests.get(encoded_url, timeout=10)
        response.raise_for_status()

        avif_bytes = BytesIO(response.content)

        try:
            img = Image.open(avif_bytes).convert("RGB")
        except:
            return_error = {"error": "Cannot decode AVIF image"}
            st.json(return_error)
            st.stop()

        # Convert to JPG buffer
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        jpeg_bytes = buffer.getvalue()

        base64_str = base64.b64encode(jpeg_bytes).decode("utf-8")

        st.json({"base64": base64_str})
        st.stop()

    except Exception as e:
        st.json({"error": str(e)})
        st.stop()


# -------------------------------
# Normal UI Mode (No API)
# -------------------------------
st.write("Use this API like this:")
st.code(
    "https://your-app-url.streamlit.app/?url=YOUR_IMAGE_URL",
    language="bash"
)

st.write("Example:")
st.code(
    "https://your-app-url.streamlit.app/?url=https://manyavar.scene7.com/is/image/manyavar/KOS009-301-White.13638_21-03-2024-14-19"
)
