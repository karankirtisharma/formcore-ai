from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, to_pixel, landmark_to_point,
)


class CalfRaiseAnalyzer(BaseAnalyzer):
    """Calf Raise — ankle plantar flexion, stable knee."""
    KNEE_LOCK_THRESHOLD = 170.0  # Knees should stay nearly locked

    def compute_angles(self, landmarks, w, h):
        side = detect_visible_side(landmarks, [23, 25, 27], [24, 26, 28])
        idx_h, idx_k, idx_a = self._side_indices(
            side, (23, 25, 27), (24, 26, 28)
        )
        hip = landmark_to_point(landmarks[idx_h])
        knee = landmark_to_point(landmarks[idx_k])
        ankle = landmark_to_point(landmarks[idx_a])

        return {
            "knee_angle": calculate_angle(hip, knee, ankle),
            "knee_pos": to_pixel(knee[0], knee[1], w, h),
            "ankle_pos": to_pixel(ankle[0], ankle[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        if angles["knee_angle"] < self.KNEE_LOCK_THRESHOLD:
            penalty += 15
            mistakes.append(f"Knees bending ({int(angles['knee_angle'])}°). Keep legs straight.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Knee: {int(meta['knee_angle'])}", meta["knee_pos"])
