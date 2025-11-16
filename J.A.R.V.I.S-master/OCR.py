import cv2
import pytesseract

# Use a raw string or double backslashes on Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def OCR():
    # request 1080p
    frameWidth = 1920
    frameHeight = 1080
    brightness = 180

    # Using DirectShow backend on Windows often helps with setting properties
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera (index 0)")

    # Set properties using CAP_PROP constants
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)

    # Read back actual values to see if the camera honored the request
    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Requested: {frameWidth}x{frameHeight}, actual: {actual_w}x{actual_h}")

    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # If camera didn't give 1080p, upscale to requested size (so downstream code works with expected shape)
        if (actual_w, actual_h) != (frameWidth, frameHeight):
            img = cv2.resize(img, (frameWidth, frameHeight), interpolation=cv2.INTER_LINEAR)

        # Preprocess for OCR (grayscale; you can add denoising / thresholding if needed)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Run Tesseract on the grayscale image
        textRecognized = pytesseract.image_to_string(gray, lang='eng')
        textRecognized = textRecognized.replace("\n\x0c", "")
        print(textRecognized)

        # Draw recognized text on image at a sensible location
        img_display = img.copy()
        cv2.putText(img_display, textRecognized, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Image (press q to quit)", img_display)

        # Proper key check
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    OCR()
