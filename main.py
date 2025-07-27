import cv2
import mediapipe as mp
import streamlit as st
import numpy as np

# To calucate the Jump using Mediapipe
class JumpHeightEstimator:
    
    #Encapsulates MediaPipe pose detection and jump height estimation logic.
    
    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        # State variables
        self.baseline_y = None
        self.peak_disp = 0.0

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        
        #Process a single video frame: detect pose, estimate jump displacement,
        #annotate frame with landmarks and jump text, and update peak value.
        
        h, w, _ = frame.shape
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        annotated = frame.copy()

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            left_y = lm[self.mp_pose.PoseLandmark.LEFT_ANKLE].y * h
            right_y = lm[self.mp_pose.PoseLandmark.RIGHT_ANKLE].y * h
            ankle_y = max(left_y, right_y)

            # Update baseline height (ground level)
            if self.baseline_y is None or ankle_y > self.baseline_y:
                self.baseline_y = ankle_y

            # Compute current displacement
            disp = self.baseline_y - ankle_y
            self.peak_disp = max(self.peak_disp, disp)

            # Draw pose landmarks
            mp.solutions.drawing_utils.draw_landmarks(
                annotated,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
            )
            # Overlay jump displacement text
            cv2.putText(
                annotated,
                f"Jump: {disp:.1f} px",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
            )
        return annotated

    def reset(self):
        #Reset baseline and peak values.
        self.baseline_y = None
        self.peak_disp = 0.0

# To Run the application as webapp platform(Optional)
class StreamlitApp:
    
    #Streamlit web app to run the JumpHeightEstimator.
    
    def __init__(self):
        st.set_page_config(page_title="Jump Height Estimator", layout="wide")
        self.estimator = JumpHeightEstimator()
        self.cap = None
        self.frame_placeholder = st.empty()
        self.metric_placeholder = st.sidebar.empty()

    def start_capture(self):
        self.cap = cv2.VideoCapture(0)

    def stop_capture(self):
        if self.cap:
            self.cap.release()
        self.estimator.pose.close()

    def run(self):
        st.title("📹 Jump Height Estimator (Streamlit + MediaPipe)")
        st.sidebar.markdown("### Controls")
        start_btn = st.sidebar.button("Start")
        stop_btn = st.sidebar.button("Stop")

        if start_btn:
            self.estimator.reset()
            self.start_capture()

        if self.cap and self.cap.isOpened():
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret or stop_btn:
                    break

                annotated = self.estimator.process_frame(frame)
                # Show annotated frame
                rgb_frame = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                self.frame_placeholder.image(rgb_frame, channels="RGB")
                # Update peak metric
                self.metric_placeholder.metric(
                    "Peak Jump (px)", f"{self.estimator.peak_disp:.1f}"
                )

                # Break if user clicked Stop
                if stop_btn:
                    break

            self.stop_capture()
            st.sidebar.success("Stopped.")
        else:
            st.info("Click **Start** in the sidebar to begin.")


if __name__ == "__main__":
    # Entry point for running the Streamlit app
    app = StreamlitApp()
    app.run()
