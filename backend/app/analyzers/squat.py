from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, vertical_reference,
    to_pixel, landmark_to_point,
)


class SquatAnalyzer(BaseAnalyzer):
    SQUAT_DEPTH_THRESHOLD = 100.0
    BACK_ANGLE_THRESHOLD = 60.0

    def compute_angles(self, landmarks, w, h):
        side = detect_visible_side(landmarks, [23, 25, 27], [24, 26, 28])
        idx_s, idx_h, idx_k, idx_a = self._side_indices(
            side, (11, 23, 25, 27), (12, 24, 26, 28)
        )
        shoulder = landmark_to_point(landmarks[idx_s])
        hip = landmark_to_point(landmarks[idx_h])
        knee = landmark_to_point(landmarks[idx_k])
        ankle = landmark_to_point(landmarks[idx_a])

        knee_angle = calculate_angle(hip, knee, ankle)
        back_angle = calculate_angle(vertical_reference(hip), hip, shoulder)

        return {
            "knee_angle": knee_angle,
            "back_angle": back_angle,
            "knee_pos": to_pixel(knee[0], knee[1], w, h),
            "hip_pos": to_pixel(hip[0], hip[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        if angles["knee_angle"] > self.SQUAT_DEPTH_THRESHOLD:
            penalty += 30
            mistakes.append(f"Depth invalid ({int(angles['knee_angle'])}°). Go lower.")
        if angles["back_angle"] > self.BACK_ANGLE_THRESHOLD:
            penalty += 20
            mistakes.append(f"Leaning too forward ({int(angles['back_angle'])}°).")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"{int(meta['knee_angle'])} deg", meta["knee_pos"])
        self._put_angle(image, f"Back: {int(meta['back_angle'])} deg", meta["hip_pos"])
