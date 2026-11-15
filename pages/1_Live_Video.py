import threading
import time

import av
import streamlit as st
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer

from emotion import detect_emotions, draw_results

st.set_page_config(page_title="Live Emotion Detector", page_icon="🎥")
st.title("🎥 Live Emotion Detector")
st.write("Click START, allow camera access, and the AI will label emotions on your live video.")

RTC_CONFIG = {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}


class EmotionProcessor(VideoProcessorBase):
    def __init__(self):
        self.lock = threading.Lock()
        self.latest_frame = None
        self.last_frame_time = time.time()
        self.results = []
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        """Background thread: analyze the newest frame again and again."""
        while time.time() - self.last_frame_time < 5:
            with self.lock:
                frame = None if self.latest_frame is None else self.latest_frame.copy()
            if frame is None:
                time.sleep(0.1)
                continue
            try:
                results = detect_emotions(frame)
            except Exception:
                results = []
            with self.lock:
                self.results = results
            time.sleep(0.2)

    def recv(self, frame):
        """Runs for every video frame: draw the latest results on it."""
        img = frame.to_ndarray(format="bgr24")
        with self.lock:
            self.latest_frame = img
            self.last_frame_time = time.time()
            results = self.results
        if results:
            img = draw_results(img, results)
        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="emotion-live",
    video_processor_factory=EmotionProcessor,
    rtc_configuration=RTC_CONFIG,
    media_stream_constraints={"video": {"width": 640, "height": 480}, "audio": False},
    async_processing=True,
)

st.caption("Emotions update about once per second. Results depend on lighting and camera angle, and a facial expression doesn't always match what someone actually feels.")