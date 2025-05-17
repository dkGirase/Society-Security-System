import cv2

def take_photo(file_path):
    cam = cv2.VideoCapture(0)  # Initialize the camera
    if not cam.isOpened():  # Check if the camera opened successfully
        print("Error: Camera not accessible.")
        return None
    
    ret, frame = cam.read()  # Capture a frame
    if ret:
        cv2.imwrite(file_path, frame)  # Save the captured image
        print(f"Photo taken and saved to {file_path}")
    else:
        print("Error: Failed to capture photo.")
    
    cam.release()  # Release the camera
    return file_path
