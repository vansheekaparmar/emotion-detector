import cv2
from deepface import DeepFace

BACKENDS = ["opencv", "yunet"]


def detect_emotions(image_bgr):
    """Try several face detectors; return [] only if all of them fail."""
    for backend in BACKENDS:
        try:
            return DeepFace.analyze(
                image_bgr,
                actions=["emotion"],
                enforce_detection=True,
                detector_backend=backend,
            )
        except ValueError as e:
            if "Face could not be detected" not in str(e):
                raise
    return []


def draw_results(image_bgr, results):
    """Draw a box and the emotion label on each detected face."""
    annotated = image_bgr.copy()
    for face in results:
        region = face["region"]
        x, y, w, h = region["x"], region["y"], region["w"], region["h"]
        label = face["dominant_emotion"]

        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            annotated, label, (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2,
        )
    return annotated