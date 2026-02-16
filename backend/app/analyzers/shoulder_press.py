from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, to_pixel, landmark_to_point,
)


class ShoulderPressAnalyzer(BaseAnalyzer):
    """Shoulder Press (seated or standing) — elbow tracking, shoulder abduction."""
    ELBOW_FLARE_THRESHOLD = 100.0  # Shoulder-Elbow-Wrist angle too wide

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
            "shoulder_angle": calculate_angle(hip, shoulder, elbow),
            "elbow_pos": to_pixel(elbow[0], elbow[1], w, h),
            "shoulder_pos": to_pixel(shoulder[0], shoulder[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        if angles["shoulder_angle"] > self.ELBOW_FLARE_THRESHOLD:
            penalty += 15
            mistakes.append(f"Elbows flared ({int(angles['shoulder_angle'])}°). Tuck slightly.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Elbow: {int(meta['elbow_angle'])}", meta["elbow_pos"])
        self._put_angle(image, f"Shoulder: {int(meta['shoulder_angle'])}", meta["shoulder_pos"])
