from abc import ABC, abstractmethod
import cv2
from app.geometry import calculate_angle, detect_visible_side, vertical_reference, to_pixel, landmark_to_point

# Visual constants
NEON_GREEN_BGR = (57, 255, 20)
NEON_RED_BGR = (80, 80, 255)
NEON_CYAN_BGR = (255, 255, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
TEXT_THICKNESS = 2


class BaseAnalyzer(ABC):
    """Standardized base class for all exercise analyzers.

    Subclasses must implement:
        compute_angles(landmarks, w, h)  -> dict of angle_name: value
        validate_constraints(angles)     -> (score_delta, list[str])
        draw_annotations(image, meta)    -> None
    """

    mode: str = "dynamic"  # "dynamic" or "static"

    # --- Template Method (final orchestrator) ---
    def analyze(self, landmarks, frame_width, frame_height) -> tuple[float, list[str], tuple, dict]:
        angles = self.compute_angles(landmarks, frame_width, frame_height)
        penalty, mistakes = self.validate_constraints(angles)
        score = self.calculate_score(penalty)
        feedback_color = NEON_GREEN_BGR if score >= 80 else NEON_RED_BGR
        metadata = {**angles, "_w": frame_width, "_h": frame_height}
        return score, mistakes, feedback_color, metadata

    def calculate_score(self, penalty: int) -> float:
        return max(0, 100 - penalty)

    @abstractmethod
    def compute_angles(self, landmarks, w: int, h: int) -> dict:
        """Extract landmarks and compute all relevant angles. Return dict."""
        ...

    @abstractmethod
    def validate_constraints(self, angles: dict) -> tuple[int, list[str]]:
        """Check angles against thresholds. Return (total_penalty, mistakes)."""
        ...

    @abstractmethod
    def draw_annotations(self, image, metadata: dict) -> None:
        """Draw exercise-specific angle overlays on frame."""
        ...

    # backward compat alias
    def draw_overlay(self, image, metadata: dict) -> None:
        if metadata:
            self.draw_annotations(image, metadata)

    # --- Shared drawing ---
    def draw_skeleton(self, image, landmarks, connections, w, h):
        for start_idx, end_idx in connections:
            if start_idx < len(landmarks) and end_idx < len(landmarks):
                sp = to_pixel(landmarks[start_idx].x, landmarks[start_idx].y, w, h)
                ep = to_pixel(landmarks[end_idx].x, landmarks[end_idx].y, w, h)
                cv2.line(image, sp, ep, NEON_CYAN_BGR, 2)
        main_joints = [11, 12, 13, 14, 23, 24, 25, 26, 27, 28]
        for i in main_joints:
            if i < len(landmarks):
                cx, cy = to_pixel(landmarks[i].x, landmarks[i].y, w, h)
                cv2.circle(image, (cx, cy), 5, NEON_GREEN_BGR, -1)
                cv2.circle(image, (cx, cy), 8, (255, 255, 255), 1)

    # --- Helpers ---
    @staticmethod
    def _side_indices(side: str, left_t: tuple, right_t: tuple) -> tuple:
        return left_t if side == "left" else right_t

    @staticmethod
    def _put_angle(image, label: str, pos: tuple[int, int]):
        cv2.putText(image, label, (pos[0] + 10, pos[1]), FONT, FONT_SCALE, NEON_CYAN_BGR, TEXT_THICKNESS)
