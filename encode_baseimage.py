from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
import requests
from PIL import Image
from io import BytesIO

app = FastAPI(title="AVIF/WebP → JPG API Converter")

@app.get("/convert")
def convert_to_jpg(url: str = Query(..., description="URL of AVIF/WebP image")):
    try:
        # Fetch image from URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Open image and convert to JPG
        img = Image.open(BytesIO(response.content)).convert("RGB")
        output = BytesIO()
        img.save(output, format="JPEG")
        output.seek(0)

        # Return as streaming response
        return StreamingResponse(output, media_type="image/jpeg")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch image: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert image: {e}")
