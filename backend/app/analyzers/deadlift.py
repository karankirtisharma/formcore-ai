from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, vertical_reference,
    to_pixel, landmark_to_point,
)


class DeadliftAnalyzer(BaseAnalyzer):

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
            "back_inclination": calculate_angle(vertical_reference(hip), hip, shoulder),
            "knee_pos": to_pixel(knee[0], knee[1], w, h),
            "hip_pos": to_pixel(hip[0], hip[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        ka = angles["knee_angle"]
        bi = angles["back_inclination"]
        if ka > 170 and bi > 20:
            penalty += 10
            mistakes.append(f"Incomplete lockout ({int(bi)}°). Stand tall.")
        if ka < 140 and bi < 15:
            penalty += 10
            mistakes.append("Too vertical. Hips might be too low.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Knee: {int(meta['knee_angle'])}", meta["knee_pos"])
        self._put_angle(image, f"Back Inc: {int(meta['back_inclination'])}", meta["hip_pos"])
