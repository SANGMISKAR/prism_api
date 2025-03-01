import os
import numpy as np
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from pathlib import Path
from script import colorize_image
from helper import get_file_extension, does_file_exist, get_file_with_extension

app = FastAPI()

# Ensure static directory exists
static_path = Path(__file__).parent / "static"
os.makedirs(static_path, exist_ok=True)

@app.get("/")
async def root():
    return JSONResponse(content={"message": "API is running successfully!"})

@app.post("/upload")
async def upload_image(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Please upload a file")

    # Extract file extension
    extension = get_file_extension(file.filename)

    # If a colorized image exists from an earlier run, delete it
    if does_file_exist(static_path, "colorized_image"):
        os.remove(static_path / get_file_with_extension(static_path, "colorized_image"))

    try:
        # Read file data
        data = await file.read()
        nparr = np.frombuffer(data, np.uint8)

        # Process the image using colorization
        output_file = static_path / f"colorized_image.{extension}"
        colorize_image(nparr, extension, output_file)  # Save directly to output_file

        # Return the processed image
        media_types = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
        }
        media_type = media_types.get(extension, "image/png")
        return FileResponse(output_file, filename=f"colorized_image.{extension}", media_type=media_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

if __name__ == "__main__":
    print("🚀 FastAPI server is starting...")
    port = int(os.getenv("PORT", 5000))
    uvicorn.run(app, host="0.0.0.1", port=port)
    print(f"✅ FastAPI server is running successfully at http://0.0.0.1:{port}")
