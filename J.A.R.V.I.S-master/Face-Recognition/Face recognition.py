import cv2
import os
import sys

# --- CONFIG ---
TRAINER_PATH = "trainer/trainer.yml"
CASCADE_FILENAME = "haarcascade_frontalface_default.xml"  # fallback below uses cv2.data.haarcascades
NAMES = ['', 'avi']   # make sure this list covers all label numbers used during training
CONFIDENCE_THRESHOLD = 70.0   # LBPH: lower means better. <70 => accept (tweak for your data)
# ---------------

# load recognizer (must be opencv-contrib)
try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
except Exception as e:
    print("ERROR: cv2.face not available. Did you install opencv-contrib-python into this interpreter?")
    print(repr(e))
    sys.exit(1)

# ensure trainer file exists
if not os.path.exists(TRAINER_PATH):
    print(f"ERROR: Trainer file not found: {TRAINER_PATH}")
    print("Make sure you have trained the recognizer and produced trainer/trainer.yml")
    sys.exit(1)

recognizer.read(TRAINER_PATH)
print("Loaded trainer:", TRAINER_PATH)

# initialize cascade (use cv2.data.haarcascades if local file not present)
cascade_path_local = CASCADE_FILENAME
if not os.path.exists(cascade_path_local):
    cascade_path_local = os.path.join(cv2.data.haarcascades, CASCADE_FILENAME)
    if not os.path.exists(cascade_path_local):
        print("ERROR: Haar cascade not found:", CASCADE_FILENAME)
        sys.exit(1)

faceCascade = cv2.CascadeClassifier(cascade_path_local)
print("Using cascade:", cascade_path_local)

font = cv2.FONT_HERSHEY_SIMPLEX

# start camera
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cam.isOpened():
    print("ERROR: Could not open camera")
    sys.exit(1)

# set resolution (optional)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# min face size for detection
minW = 0.1 * cam.get(cv2.CAP_PROP_FRAME_WIDTH)
minH = 0.1 * cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

print("Min face size:", int(minW), int(minH))
print("Names list length:", len(NAMES))

while True:
    ret, img = cam.read()
    if not ret:
        print("Failed to capture frame from camera. Exiting.")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH))
    )

    if len(faces) == 0:
        # optionally show frame and continue
        cv2.imshow('camera', img)
        if cv2.waitKey(10) & 0xff == 27:
            break
        continue

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        face_roi = gray[y:y + h, x:x + w]

        # IMPORTANT: resize to the same size you used for training (if any)
        # If you trained with 200x200, you must resize here too. If unsure, try 200x200.
        face_for_pred = cv2.resize(face_roi, (200, 200), interpolation=cv2.INTER_LINEAR)

        # Predict — wrap in try/except in case something odd happens
        try:
            label, confidence = recognizer.predict(face_for_pred)
        except Exception as e:
            print("Recognizer.predict failed:", repr(e))
            label, confidence = -1, float('inf')

        # DEBUG: show raw values in terminal for tuning
        print(f"Predicted label={label}, confidence={confidence:.2f}")

        # map label -> name safely
        name = "unknown"
        if 0 <= label < len(NAMES):
            name = NAMES[label]
        else:
            # If labels start from 1 in your training, ensure NAMES has a dummy at index 0.
            name = "unknown (label {})".format(label)

        # Decide acceptance using LBPH: lower confidence == better match
        if confidence < CONFIDENCE_THRESHOLD:
            display_name = name
        else:
            display_name = "unknown"

        accuracy_text = f"{round(100 - confidence, 2)}%"  # informal "accuracy" view; can be negative if confidence>100

        # Put text on image
        cv2.putText(img, str(display_name), (x + 5, y - 10), font, 0.9, (255, 255, 255), 2)
        cv2.putText(img, str(accuracy_text), (x + 5, y + h + 20), font, 0.8, (255, 255, 0), 1)

    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff
    if k == 27:  # ESC to quit
        break

print("Thanks for using this program, have a good day.")
cam.release()
cv2.destroyAllWindows()
