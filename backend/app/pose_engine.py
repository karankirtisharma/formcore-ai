import logging
import os
import subprocess
import tempfile

import shutil
import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

logger = logging.getLogger(__name__)

import uuid

MODEL_PATH = "app/models/pose_landmarker_heavy.task"
if not os.path.exists(MODEL_PATH):
    logger.warning("Heavy model not found, falling back to Lite")
    MODEL_PATH = "app/models/pose_landmarker_lite.task"

# Frame sampling: process every N-th frame for performance
SKIP = 2

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

    def _auto_detect_exercise(self, landmarks) -> str:
        avg_y = lambda indices: sum([landmarks[i].y for i in indices]) / len(indices)
        
        shoulder_y = avg_y([11, 12])
        hip_y = avg_y([23, 24])
        ankle_y = avg_y([27, 28])
        wrist_y = avg_y([15, 16])
        
        xs = [lm.x for lm in landmarks[11:29]] 
        ys = [lm.y for lm in landmarks[11:29]]
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)

        arms_spread = abs(landmarks[15].x - landmarks[16].x)
        if arms_spread > 0.7 or ankle_y < hip_y:
            return "unsupported"
        
        is_horizontal = width > height * 1.2
        
        if is_horizontal:
            return "pushup" # Most common horizontal exercise, plank is harder to cleanly separate without history
        else:
            if wrist_y < shoulder_y:
                return "overhead_press"
                
            if abs(wrist_y - hip_y) < 0.1 and abs(wrist_y - shoulder_y) > 0.2:
                return "deadlift"
                
            if shoulder_y < wrist_y < hip_y - 0.1:
                return "bicep_curl"
                
            return "squat"

    def process_image(self, image_bytes: bytes, exercise_type: str = "auto") -> dict | None:
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
            
            if exercise_type == "auto":
                exercise_type = self._auto_detect_exercise(landmarks)
            
            if exercise_type == "unsupported":
                return {
                    "score": 0, 
                    "mistakes": ["AI is not suitable for that particular workout. Outside of supported scope."], 
                    "image_url": None,
                    "detected_exercise": "Unsupported"
                }

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

        # Save result to media dir
        file_id = str(uuid.uuid4())
        filepath = f"media/{file_id}.jpg"
        cv2.imwrite(filepath, image)

        return {"score": score, "mistakes": mistakes, "image_url": f"/media/{file_id}.jpg", "detected_exercise": exercise_type.replace('_', ' ').title()}

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

        return frame, score, mistakes, exercise_type

    def process_video(self, video_bytes: bytes, exercise_type: str = "auto") -> dict | None:
        """Process all frames of a video with pose tracking, returning an annotated MP4."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tfile:
            tfile.write(video_bytes)
            temp_input = tfile.name

        temp_output = temp_input.replace(".mp4", "_tracked.mp4")
        temp_h264 = temp_input.replace(".mp4", "_h264.mp4")
        
        cap = None
        writer = None

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
                return None

            all_scores = []
            all_mistakes: list[str] = []
            worst_score = 101
            worst_frame = None
            frame_idx = 0

            # Setup tracking
            detected_type = exercise_type
            
            while frame_idx < total_frames:
                ret, frame = cap.read()
                if not ret:
                    break

                if scale != 1.0:
                    frame = cv2.resize(frame, (frame_w, frame_h))

                # If auto, we need to detect on the first processed frame
                if exercise_type == "auto" and frame_idx % SKIP == 0:
                    # Quick detection
                    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
                    detection_result = self.detector.detect(mp_image)
                    if detection_result.pose_landmarks:
                        detected_type = self._auto_detect_exercise(detection_result.pose_landmarks[0])
                    else:
                        detected_type = "squat" # fallback if no landmarks on frame 0
                        
                    if detected_type == "unsupported":
                        cap.release()
                        writer.release()
                        return {
                            "score": 0, 
                            "mistakes": ["AI is not suitable for that particular workout. Outside of supported scope."], 
                            "image_url": None,
                            "video_url": None,
                            "detected_exercise": "Unsupported"
                        }
                    exercise_type = detected_type # Only detect once

                # Process this frame for pose
                if frame_idx % SKIP == 0:
                    frame, f_score, f_mistakes, _ = self._annotate_frame(frame, exercise_type=detected_type)
                    if f_mistakes and f_mistakes[0] == "No human subject detected in frame.":
                        # Ignore frame without tanking the score
                        pass
                    else:
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

            # Save tracked video to media dir
            file_id = str(uuid.uuid4())
            final_video_path = f"media/{file_id}.mp4"
            shutil.copy(video_file, final_video_path)
            
            image_url = None
            if worst_frame is not None:
                final_image_path = f"media/{file_id}.jpg"
                cv2.imwrite(final_image_path, worst_frame)
                image_url = f"/media/{file_id}.jpg"

            return {
                "score": avg_score,
                "mistakes": all_mistakes,
                "image_url": image_url,
                "video_url": f"/media/{file_id}.mp4",
                "detected_exercise": detected_type.replace('_', ' ').title(),
            }

        except Exception:
            logger.exception("Error processing video")
            return None
        finally:
            if cap is not None:
                cap.release()
            if writer is not None:
                writer.release()
                
            for f in [temp_input, temp_output, temp_h264]:
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except Exception as e:
                        logger.warning(f"Failed to remove temp file {f}: {e}")
