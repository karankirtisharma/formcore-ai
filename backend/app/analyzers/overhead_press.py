from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, vertical_reference,
    to_pixel, landmark_to_point,
)


class OverheadPressAnalyzer(BaseAnalyzer):
    """Overhead Press — full lockout overhead, vertical bar path."""
    LOCKOUT_THRESHOLD = 160.0     # Elbow should be near-straight at top
    BACK_ARCH_THRESHOLD = 20.0    # Excessive back lean

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
            "back_lean": calculate_angle(vertical_reference(hip), hip, shoulder),
            "elbow_pos": to_pixel(elbow[0], elbow[1], w, h),
            "hip_pos": to_pixel(hip[0], hip[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        if angles["back_lean"] > self.BACK_ARCH_THRESHOLD:
            penalty += 25
            mistakes.append(f"Excessive back arch ({int(angles['back_lean'])}°). Brace core.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Elbow: {int(meta['elbow_angle'])}", meta["elbow_pos"])
        self._put_angle(image, f"Back: {int(meta['back_lean'])}", meta["hip_pos"])
