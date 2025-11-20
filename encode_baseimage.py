import streamlit as st
import base64
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="🖼️ Image ↔ Base64 Converter", page_icon="🧩", layout="wide")

st.title("🧩 Image ↔ Base64 Converter")

st.write("Convert images to Base64 or convert Base64 back to JPG.")

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
            uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "gif", "webp"])
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
                # Clean Base64 string
                b64_clean = base64_input.strip().replace("\n", "").replace(" ", "")

                # Fix missing padding
                missing_padding = len(b64_clean) % 4
                if missing_padding:
                    b64_clean += "=" * (4 - missing_padding)

                # Fix URL-safe Base64
                b64_clean = b64_clean.replace("-", "+").replace("_", "/")

                # Decode Base64
                decoded_bytes = base64.b64decode(b64_clean)

                # Convert to image
                img = Image.open(BytesIO(decoded_bytes)).convert("RGB")

                # Save JPG in memory
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
