import streamlit as st
import base64
import requests
from PIL import Image
from io import BytesIO
import os
import uuid
import json

# ---------------------------------------------------------
#               API MODE: AVIF URL → JPG
# ---------------------------------------------------------

query_params = st.experimental_get_query_params()

if "avif_url" in query_params:
    avif_url = query_params["avif_url"][0]

    try:
        # Download AVIF image
        response = requests.get(avif_url, timeout=10)
        response.raise_for_status()

        avif_bytes = response.content

        # Convert AVIF → JPG
        img = Image.open(BytesIO(avif_bytes)).convert("RGB")

        # Save JPG into /static
        os.makedirs("static", exist_ok=True)
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join("static", filename)
        img.save(filepath, "JPEG")

        # Build public URL
        base_url = "https://base64tojpg-nqy3cuvfdnnbgp8htt5ecn.streamlit.app"
        jpg_url = f"{base_url}/static/{filename}"

        # Return JSON response
        st.write(json.dumps({
            "status": "success",
            "jpg_url": jpg_url
        }))

        st.stop()

    except Exception as e:
        st.write(json.dumps({
            "status": "error",
            "message": str(e)
        }))
        st.stop()


# ---------------------------------------------------------
#              NORMAL STREAMLIT UI MODE
# ---------------------------------------------------------

st.set_page_config(page_title="🖼️ Image ↔ Base64 Converter", page_icon="🧩", layout="wide")
st.title("🧩 Image ↔ Base64 Converter")

tab1, tab2 = st.tabs(["🔼 Image → Base64", "🔽 Base64 → JPG"])

# ---------------------------------------------------------
#  TAB 1 : IMAGE → BASE64
# ---------------------------------------------------------
with tab1:

    left_col, right_col = st.columns([1, 2])

    with left_col:
        option = st.radio("Choose input method:", ["Upload Image", "Enter URL"])

        image_data = None
        image_source = None

        if option == "Upload Image":
            uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "gif", "webp", "avif"])
            if uploaded_file:
                image_data = uploaded_file.read()
                image_source = uploaded_file.name

        elif option == "Enter URL":
            image_url = st.text_input("Enter image URL (must start with https://)")
            if image_url:
                try:
                    response = requests.get(image_url, timeout=10)
                    response.raise_for_status()
                    image_data = response.content
                    image_source = image_url
                except Exception as e:
                    st.error(f"❌ Failed to fetch image: {e}")

    with right_col:
        if image_data:
            st.subheader("🖼️ Image Preview")
            st.image(image_data, caption=image_source, use_container_width=True)

            st.subheader("📜 Base64 Encoded String")
            encoded_string = base64.b64encode(image_data).decode("utf-8")
            st.text_area("Base64 Output", encoded_string, height=250)

            st.download_button(
                label="💾 Download Base64 as .txt",
                data=encoded_string.encode(),
                file_name="image_base64.txt",
                mime="text/plain",
            )

# ---------------------------------------------------------
#  TAB 2 : BASE64 → JPG
# ---------------------------------------------------------
with tab2:

    st.subheader("Paste Base64 String → Convert to JPG")

    base64_input = st.text_area("Paste Base64 String Here", height=250)

    if st.button("Convert to JPG"):
        if not base64_input.strip():
            st.error("❌ Please paste a Base64 string!")
        else:
            try:
                # Clean base64
                b64_clean = base64_input.strip().replace("\n", "").replace(" ", "")
                missing_padding = len(b64_clean) % 4
                if missing_padding:
                    b64_clean += "=" * (4 - missing_padding)

                b64_clean = b64_clean.replace("-", "+").replace("_", "/")

                decoded_bytes = base64.b64decode(b64_clean)

                img = Image.open(BytesIO(decoded_bytes)).convert("RGB")

                output = BytesIO()
                img.save(output, format="JPEG")
                output.seek(0)

                st.success("✅ Conversion Successful!")
                st.image(img, caption="Converted JPG", use_container_width=True)

                st.download_button(
                    label="💾 Download JPG",
                    data=output,
                    file_name="converted.jpg",
                    mime="image/jpeg"
                )

            except Exception as e:
                st.error(f"❌ Failed to convert: {e}")
