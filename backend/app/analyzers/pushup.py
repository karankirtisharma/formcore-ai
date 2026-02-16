from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, to_pixel, landmark_to_point,
)


class PushupAnalyzer(BaseAnalyzer):
    BODY_ALIGNMENT_THRESHOLD = 160.0

    def compute_angles(self, landmarks, w, h):
        side = detect_visible_side(landmarks, [11, 13, 15], [12, 14, 16])
        idx_s, idx_e, idx_w, idx_h, _, idx_a = self._side_indices(
            side, (11, 13, 15, 23, 25, 27), (12, 14, 16, 24, 26, 28)
        )
        shoulder = landmark_to_point(landmarks[idx_s])
        elbow = landmark_to_point(landmarks[idx_e])
        wrist = landmark_to_point(landmarks[idx_w])
        hip = landmark_to_point(landmarks[idx_h])
        ankle = landmark_to_point(landmarks[idx_a])

        return {
            "elbow_angle": calculate_angle(shoulder, elbow, wrist),
            "body_angle": calculate_angle(shoulder, hip, ankle),
            "elbow_pos": to_pixel(elbow[0], elbow[1], w, h),
            "hip_pos": to_pixel(hip[0], hip[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        if angles["body_angle"] < self.BODY_ALIGNMENT_THRESHOLD:
            penalty += 20
            mistakes.append(f"Body not straight ({int(angles['body_angle'])}°). Keep core tight.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Elbow: {int(meta['elbow_angle'])}", meta["elbow_pos"])
        self._put_angle(image, f"Body: {int(meta['body_angle'])}", meta["hip_pos"])
