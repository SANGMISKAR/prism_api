import requests

# API endpoint
API_URL = "https://magic-s7zz.onrender.com/upload"

# Path to the image file you want to upload
image_path = "girl.jpg"  # Replace with the actual path to your image

# Open the image file in binary mode
with open(image_path, "rb") as file:
    files = {"file": (image_path, file, "image/jpeg")}  # Adjust the MIME type if needed

    # Send a POST request to the API
    response = requests.post(API_URL, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the colorized image returned by the API
        output_path = "colorized_image.png"  # Save the output image with this name
        with open(output_path, "wb") as output_file:
            output_file.write(response.content)
        print(f"✅ Colorized image saved as {output_path}")
    else:
        # Print the error message if the request failed
        print(f"❌ Failed to process image: {response.status_code} - {response.text}")
