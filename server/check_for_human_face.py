import cv2

def has_face(image_path):
    """Detects if a human face is present in an image.

    Args:
        image_path: The path to the image file.

    Returns:
        True if a human face is found, False otherwise.
    """
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale (Haar cascade classifiers work in grayscale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Load the Haar cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Check if any faces were found
    if len(faces) > 0:
        print("A human face was found in the submitted image.\n\n")
        return True
    else:
        print("No human face was found in the submitted image.")
        return False
