import cv2
import numpy as np

# Load the colorization model
prototxt_path = "models/colorization_deploy_v2.prototxt"
model_path = "models/colorization_release_v2.caffemodel"
points_path = "models/pts_in_hull.npy"

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
pts = np.load(points_path)

points = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(net.getLayerId("class8_ab")).blobs = [points.astype("float32")]
net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [
    np.full([1, 313], 2.606, dtype="float32")
]

def colorize_image(file, extension, output_file):
    """
    Colorize the input image and save it to the output file.
    """
    try:
        # Decode the image from bytes
        image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Failed to decode image. Please check the file format.")

        # Preprocess the image
        scaled = image.astype("float32") / 255.0
        lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
        resized = cv2.resize(lab, (224, 224))

        # Extract the L channel and subtract 50 for mean centering
        L = cv2.split(resized)[0]
        L -= 50

        # Colorize the image
        net.setInput(cv2.dnn.blobFromImage(L))
        ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
        ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
        L = cv2.split(lab)[0]

        # Combine the L channel with the colorized ab channels
        colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
        colorized = (255 * colorized).astype("uint8")

        # Save the colorized image
        cv2.imwrite(str(output_file), colorized)
        print(f"✅ Colorized image saved to {output_file}")

        return colorized
    except Exception as e:
        raise Exception(f"Failed to colorize image: {str(e)}")
