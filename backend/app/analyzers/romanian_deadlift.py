from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, vertical_reference,
    to_pixel, landmark_to_point,
)


class RomanianDeadliftAnalyzer(BaseAnalyzer):
    """RDL — minimal knee bend, deep hip hinge, straight back."""
    KNEE_SOFTNESS_MAX = 160.0   # Knees should stay mostly straight
    BACK_STRAIGHT_THRESHOLD = 20.0  # Back inclination from vertical when hinging

    def compute_angles(self, landmarks, w, h):
        side = detect_visible_side(landmarks, [23, 25, 27], [24, 26, 28])
        idx_s, idx_h, idx_k, idx_a = self._side_indices(
            side, (11, 23, 25, 27), (12, 24, 26, 28)
        )
        shoulder = landmark_to_point(landmarks[idx_s])
        hip = landmark_to_point(landmarks[idx_h])
        knee = landmark_to_point(landmarks[idx_k])
        ankle = landmark_to_point(landmarks[idx_a])

        return {
            "knee_angle": calculate_angle(hip, knee, ankle),
            "hip_hinge": calculate_angle(vertical_reference(hip), hip, shoulder),
            "knee_pos": to_pixel(knee[0], knee[1], w, h),
            "hip_pos": to_pixel(hip[0], hip[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        if angles["knee_angle"] < self.KNEE_SOFTNESS_MAX:
            penalty += 15
            mistakes.append(f"Too much knee bend ({int(angles['knee_angle'])}°). Keep legs straighter.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Knee: {int(meta['knee_angle'])}", meta["knee_pos"])
        self._put_angle(image, f"Hinge: {int(meta['hip_hinge'])}", meta["hip_pos"])
