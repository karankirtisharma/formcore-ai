from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, to_pixel, landmark_to_point,
)


class GluteBridgeAnalyzer(BaseAnalyzer):
    """Glute Bridge — hip extension at top, shoulders stay grounded."""
    HIP_EXTENSION_THRESHOLD = 160.0  # Shoulder-Hip-Knee should be nearly straight at top

    def compute_angles(self, landmarks, w, h):
        side = detect_visible_side(landmarks, [23, 25, 27], [24, 26, 28])
        idx_s, idx_h, idx_k, _ = self._side_indices(
            side, (11, 23, 25, 27), (12, 24, 26, 28)
        )
        shoulder = landmark_to_point(landmarks[idx_s])
        hip = landmark_to_point(landmarks[idx_h])
        knee = landmark_to_point(landmarks[idx_k])

        return {
            "hip_angle": calculate_angle(shoulder, hip, knee),
            "hip_pos": to_pixel(hip[0], hip[1], w, h),
            "knee_pos": to_pixel(knee[0], knee[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        if angles["hip_angle"] < self.HIP_EXTENSION_THRESHOLD:
            penalty += 25
            mistakes.append(f"Hips not fully extended ({int(angles['hip_angle'])}°). Push higher.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Hip: {int(meta['hip_angle'])}", meta["hip_pos"])
