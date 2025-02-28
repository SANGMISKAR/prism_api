import requests

# API URL
url = "http://127.0.0.1:5000/upload"

# Image file to test (Change the path to your image file)
file_path = "2.png"

# Open file in binary mode
with open(file_path, "rb") as image_file:
    files = {"file": (file_path, image_file, "image/jpeg")}  # Change MIME type if needed
    response = requests.post(url, files=files)

# Print response
if response.status_code == 200:
    print("✅ Image uploaded successfully! Download the colorized image from:", response.url)
else:
    print("❌ Failed to upload image. Response:", response.json())
