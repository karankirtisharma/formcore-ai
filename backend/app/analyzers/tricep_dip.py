from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, to_pixel, landmark_to_point,
)


class TricepDipAnalyzer(BaseAnalyzer):
    """Tricep Dip — elbow depth, minimal forward lean."""
    DEPTH_THRESHOLD = 90.0         # Elbow should reach ~90 degrees
    FORWARD_LEAN_THRESHOLD = 30.0  # Shoulder-Elbow angle vs vertical

    def compute_angles(self, landmarks, w, h):
        side = detect_visible_side(landmarks, [11, 13, 15], [12, 14, 16])
        idx_s, idx_e, idx_w, idx_h = self._side_indices(
            side, (11, 13, 15, 23), (12, 14, 16, 24)
        )
        shoulder = landmark_to_point(landmarks[idx_s])
        elbow = landmark_to_point(landmarks[idx_e])
        wrist = landmark_to_point(landmarks[idx_w])
        hip = landmark_to_point(landmarks[idx_h])

        return {
            "elbow_angle": calculate_angle(shoulder, elbow, wrist),
            "body_angle": calculate_angle(shoulder, hip, [hip[0], hip[1] + 0.5]),
            "elbow_pos": to_pixel(elbow[0], elbow[1], w, h),
            "hip_pos": to_pixel(hip[0], hip[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        if angles["elbow_angle"] > self.DEPTH_THRESHOLD + 30:
            penalty += 20
            mistakes.append(f"Not deep enough ({int(angles['elbow_angle'])}°). Bend to 90°.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Elbow: {int(meta['elbow_angle'])}", meta["elbow_pos"])
