from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, vertical_reference,
    to_pixel, landmark_to_point,
)


class BulgarianSplitSquatAnalyzer(BaseAnalyzer):
    """Bulgarian Split Squat — front knee depth, torso upright."""
    DEPTH_THRESHOLD = 100.0
    TORSO_LEAN_THRESHOLD = 30.0

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
        if angles["knee_angle"] > self.DEPTH_THRESHOLD:
            penalty += 25
            mistakes.append(f"Not deep enough ({int(angles['knee_angle'])}°). Lower your hips.")
        if angles["torso_angle"] > self.TORSO_LEAN_THRESHOLD:
            penalty += 15
            mistakes.append(f"Torso leaning ({int(angles['torso_angle'])}°). Stay upright.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Knee: {int(meta['knee_angle'])}", meta["knee_pos"])
        self._put_angle(image, f"Torso: {int(meta['torso_angle'])}", meta["hip_pos"])
