import cv2
from deepface import DeepFace

def detect_emotions(image_bgr):
    """Return a list with one dict per face found (empty list if none.)"""
    try:
        results = DeepFace.analyze(image_bgr, actions=["emotion"], enforce_detection=True,)
    except ValueError:
        return[]
    return results

def draw_results(image_bgr, results):
    """Draw a box and the emotion label on each detected face."""
    annotated = image_bgr.copy()
    for face in results:
        region = face["region"]
        x, y, w, h = region["x"], region["y"], region["w"], region["h"]
        label = face["dominant_emotion"]

        cv2.rectangle(annotated, (x,y), (x+y, w+h), (0, 255, 0),2)
        cv2.putText(annotated, label, (x, max(y - 10, 20)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2,
                    )
        return annotated 