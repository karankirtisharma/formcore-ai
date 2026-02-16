from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, vertical_reference,
    to_pixel, landmark_to_point,
)


class BicepCurlAnalyzer(BaseAnalyzer):
    """Bicep Curl — elbow stability, full ROM, no swinging."""
    ELBOW_DRIFT_THRESHOLD = 20.0  # Shoulder-Elbow should stay near vertical

    def compute_angles(self, landmarks, w, h):
        side = detect_visible_side(landmarks, [11, 13, 15], [12, 14, 16])
        idx_s, idx_e, idx_w = self._side_indices(
            side, (11, 13, 15), (12, 14, 16)
        )
        shoulder = landmark_to_point(landmarks[idx_s])
        elbow = landmark_to_point(landmarks[idx_e])
        wrist = landmark_to_point(landmarks[idx_w])

        return {
            "elbow_angle": calculate_angle(shoulder, elbow, wrist),
            "elbow_drift": calculate_angle(vertical_reference(shoulder), shoulder, elbow),
            "elbow_pos": to_pixel(elbow[0], elbow[1], w, h),
            "shoulder_pos": to_pixel(shoulder[0], shoulder[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        if angles["elbow_drift"] > self.ELBOW_DRIFT_THRESHOLD:
            penalty += 20
            mistakes.append(f"Elbow drifting ({int(angles['elbow_drift'])}°). Pin elbow to side.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Curl: {int(meta['elbow_angle'])}", meta["elbow_pos"])
        self._put_angle(image, f"Drift: {int(meta['elbow_drift'])}", meta["shoulder_pos"])
