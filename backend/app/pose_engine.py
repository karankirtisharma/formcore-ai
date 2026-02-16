import logging
import os
import subprocess
import tempfile

import base64
import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

logger = logging.getLogger(__name__)

# Use the Heavy model for maximum accuracy
MODEL_PATH = "app/models/pose_landmarker_heavy.task"
if not os.path.exists(MODEL_PATH):
    logger.warning("Heavy model not found, falling back to Lite")
    MODEL_PATH = "app/models/pose_landmarker_lite.task"

class PoseAnalyzer:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=False, # We don't need masks, saves compute
            min_pose_detection_confidence=0.6, # Increased for accuracy
            min_pose_presence_confidence=0.6,
            min_tracking_confidence=0.6,
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)

    def process_image(self, image_bytes: bytes, exercise_type: str = "squat") -> dict | None:
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return None

        # MediaPipe needs RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        
        # Run detection
        detection_result = self.detector.detect(mp_image)

        score = 0
        mistakes: list[str] = []

        if detection_result.pose_landmarks:
            landmarks = detection_result.pose_landmarks[0]
            h, w, _ = image.shape
            
            # GET ANALYZER FROM REGISTRY
            from app.analyzers.registry import ExerciseRegistry
            analyzer = ExerciseRegistry.get_analyzer(exercise_type)
            
            score, mistakes, _, metadata = analyzer.analyze(landmarks, w, h)

            # --- Visualization ---
            
            # Draw Connections
            skele_connections = [
                (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),  # Arms
                (11, 23), (12, 24), (23, 24),                      # Torso
                (23, 25), (24, 26), (25, 27), (26, 28),            # Legs
                (27, 29), (28, 30), (29, 31), (30, 32)             # Feet
            ]
            
            # Draw Skeleton (delegated to analyzer or base)
            analyzer.draw_skeleton(image, landmarks, skele_connections, w, h)
            
            # Draw specific overlay
            if hasattr(analyzer, 'draw_overlay'):
                analyzer.draw_overlay(image, metadata)
            
        else:
            score = 0
            mistakes.append("No human subject detected in frame.")

        # Encode result
        _, buffer = cv2.imencode(".jpg", image)
        image_base64 = base64.b64encode(buffer).decode("utf-8")

        return {"score": score, "mistakes": mistakes, "image_base64": image_base64}


    def _annotate_frame(self, frame: np.ndarray, exercise_type: str = "squat") -> tuple:
        """Run pose detection on a single BGR frame, draw skeleton, return (annotated_frame, score, mistakes)."""
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

        detection_result = self.detector.detect(mp_image)

        score = 0
        mistakes: list[str] = []

        if detection_result.pose_landmarks:
            landmarks = detection_result.pose_landmarks[0]
            h, w, _ = frame.shape
            
            # GET ANALYZER FROM REGISTRY
            from app.analyzers.registry import ExerciseRegistry
            analyzer = ExerciseRegistry.get_analyzer(exercise_type)
            
            score, mistakes, _, metadata = analyzer.analyze(landmarks, w, h)

            skele_connections = [
                (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
                (11, 23), (12, 24), (23, 24),
                (23, 25), (24, 26), (25, 27), (26, 28),
                (27, 29), (28, 30), (29, 31), (30, 32)
            ]
            analyzer.draw_skeleton(frame, landmarks, skele_connections, w, h)
            
            if hasattr(analyzer, 'draw_overlay'):
                analyzer.draw_overlay(frame, metadata)
        else:
            score = 0
            mistakes.append("No human subject detected in frame.")

        return frame, score, mistakes

    def process_video(self, video_bytes: bytes, exercise_type: str = "squat") -> dict | None:
        """Process all frames of a video with pose tracking, returning an annotated MP4."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tfile:
            tfile.write(video_bytes)
            temp_input = tfile.name

        temp_output = temp_input.replace(".mp4", "_tracked.mp4")

        try:
            cap = cv2.VideoCapture(temp_input)
            if not cap.isOpened():
                return None

            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Cap at ~30 seconds
            max_frames = int(fps * 30)
            total_frames = min(total_frames, max_frames)

            # Scale down large videos for performance
            scale = 1.0
            if frame_w > 1080:
                scale = 1080 / frame_w
                frame_w = 1080
                frame_h = int(frame_h * scale)

            # Use mp4v codec for broad compatibility
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(temp_output, fourcc, fps, (frame_w, frame_h))

            if not writer.isOpened():
                cap.release()
                return None

            all_scores = []
            all_mistakes: list[str] = []
            worst_score = 101
            worst_frame = None
            frame_idx = 0

            # Process every 2nd frame for speed; annotate all frames
            SKIP = 2  
            
            while frame_idx < total_frames:
                ret, frame = cap.read()
                if not ret:
                    break

                if scale != 1.0:
                    frame = cv2.resize(frame, (frame_w, frame_h))

                # Process this frame for pose
                if frame_idx % SKIP == 0:
                    frame, f_score, f_mistakes = self._annotate_frame(frame, exercise_type=exercise_type)
                    all_scores.append(f_score)
                    for m in f_mistakes:
                        if m not in all_mistakes:
                            all_mistakes.append(m)
                    
                    if f_score < worst_score:
                        worst_score = f_score
                        worst_frame = frame.copy()

                writer.write(frame)
                frame_idx += 1

            cap.release()
            writer.release()

            # Re-encode to H.264 for browser compatibility
            temp_h264 = temp_input.replace(".mp4", "_h264.mp4")
            try:
                import imageio_ffmpeg
                ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
                subprocess.run(
                    [ffmpeg_path, "-y", "-i", temp_output, "-c:v", "libx264",
                     "-preset", "ultrafast", "-crf", "30", "-pix_fmt", "yuv420p",
                     "-movflags", "+faststart", temp_h264],
                    check=True, capture_output=True,
                )
                video_file = temp_h264
            except Exception:
                logger.warning("H.264 re-encoding failed, falling back to mp4v")
                video_file = temp_output

            # Compute aggregate score (average of all analyzed frames)
            avg_score = int(sum(all_scores) / len(all_scores)) if all_scores else 0

            # Encode the tracked video to base64
            with open(video_file, "rb") as vf:
                video_base64 = base64.b64encode(vf.read()).decode("utf-8")

            # Encode the worst frame as the representative image
            image_base64 = None
            if worst_frame is not None:
                _, buffer = cv2.imencode(".jpg", worst_frame)
                image_base64 = base64.b64encode(buffer).decode("utf-8")

            return {
                "score": avg_score,
                "mistakes": all_mistakes,
                "image_base64": image_base64,
                "video_base64": video_base64,
            }

        except Exception:
            logger.exception("Error processing video")
            return None
        finally:
            for f in [temp_input, temp_output, temp_input.replace(".mp4", "_h264.mp4")]:
                if os.path.exists(f):
                    os.remove(f)
