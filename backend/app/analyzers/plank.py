from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, to_pixel, landmark_to_point,
)


class PlankAnalyzer(BaseAnalyzer):
    """Plank (static exercise) — body alignment, penalize hip sag/pike."""
    mode = "static"
    ALIGNMENT_THRESHOLD = 160.0  # Shoulder-Hip-Ankle should be ~180

    def compute_angles(self, landmarks, w, h):
        side = detect_visible_side(landmarks, [11, 23, 27], [12, 24, 28])
        idx_s, idx_h, _, idx_a = self._side_indices(
            side, (11, 23, 25, 27), (12, 24, 26, 28)
        )
        shoulder = landmark_to_point(landmarks[idx_s])
        hip = landmark_to_point(landmarks[idx_h])
        ankle = landmark_to_point(landmarks[idx_a])

        return {
            "body_angle": calculate_angle(shoulder, hip, ankle),
            "hip_pos": to_pixel(hip[0], hip[1], w, h),
            "shoulder_pos": to_pixel(shoulder[0], shoulder[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        body = angles["body_angle"]
        if body < self.ALIGNMENT_THRESHOLD:
            penalty += 25
            if body < 150:
                mistakes.append(f"Hips sagging/piking ({int(body)}°). Straighten body.")
            else:
                mistakes.append(f"Slight misalignment ({int(body)}°). Tighten core.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Body: {int(meta['body_angle'])}", meta["hip_pos"])
