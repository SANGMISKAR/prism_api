import os
import numpy as np
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from script import colorize_image
from helper import get_file_extension, does_file_exist, get_file_with_extension

app = FastAPI()

# Ensure static directory exists
static_path = "static"
os.makedirs(static_path, exist_ok=True)

@app.get("/")  # Root endpoint to check if the API is running
async def root():
    return JSONResponse(content={"message": "API is running successfully!"})

@app.post("/upload")  # API for uploading and processing an image
async def upload_image(file: UploadFile):
    if not file.filename:
        return JSONResponse(content={"error": "Please upload a file"}, status_code=400)

    # Extract file extension
    extension = get_file_extension(file.filename)

    # If a colorized image exists from an earlier run, delete it
    if does_file_exist(static_path, "colorized_image"):
        os.remove(os.path.join(static_path, get_file_with_extension(static_path, "colorized_image")))

    # Read file data
    data = await file.read()
    nparr = np.frombuffer(data, np.uint8)

    # Process the image using colorization
    colorize_image(nparr, extension)

    # Save processed image in static folder
    output_file = f"{static_path}/colorized_image.{extension}"
    os.rename(f"colorized_image.{extension}", output_file)

    return FileResponse(output_file, filename="colorized_image.png", media_type="image/png")

if __name__ == "__main__":
    print("🚀 FastAPI server is starting...")

    # ✅ Automatically use Render's assigned port
    port = int(os.getenv("PORT", 10000))  # Default to 10000 if PORT not set
    uvicorn.run(app, host="0.0.0.0", port=port)

    print(f"✅ FastAPI server is running successfully at http://0.0.0.0:{port}")
