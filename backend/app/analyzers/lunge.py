from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, vertical_reference,
    to_pixel, landmark_to_point,
)


class LungeAnalyzer(BaseAnalyzer):
    """Front/walking lunge — checks front knee tracking and torso uprightness."""
    KNEE_OVER_TOE_THRESHOLD = 80.0   # Front knee angle (Hip-Knee-Ankle)
    TORSO_LEAN_THRESHOLD = 30.0       # Torso deviation from vertical

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
            "torso_angle": calculate_angle(vertical_reference(hip), hip, shoulder),
            "knee_pos": to_pixel(knee[0], knee[1], w, h),
            "hip_pos": to_pixel(hip[0], hip[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        if angles["knee_angle"] < self.KNEE_OVER_TOE_THRESHOLD:
            penalty += 25
            mistakes.append(f"Front knee too far forward ({int(angles['knee_angle'])}°).")
        if angles["torso_angle"] > self.TORSO_LEAN_THRESHOLD:
            penalty += 20
            mistakes.append(f"Torso leaning ({int(angles['torso_angle'])}°). Stay upright.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Knee: {int(meta['knee_angle'])}", meta["knee_pos"])
        self._put_angle(image, f"Torso: {int(meta['torso_angle'])}", meta["hip_pos"])
