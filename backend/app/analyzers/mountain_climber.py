from app.analyzers.base import BaseAnalyzer
from app.geometry import (
    calculate_angle, detect_visible_side, to_pixel, landmark_to_point,
)


class MountainClimberAnalyzer(BaseAnalyzer):
    """Mountain Climber — body alignment + knee drive toward chest."""
    ALIGNMENT_THRESHOLD = 155.0   # Shoulder-Hip-Ankle (allow slight bend)
    KNEE_DRIVE_THRESHOLD = 90.0   # Hip-Knee angle when knee is driven

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
            "body_angle": calculate_angle(shoulder, hip, ankle),
            "knee_drive": calculate_angle(shoulder, hip, knee),
            "hip_pos": to_pixel(hip[0], hip[1], w, h),
            "knee_pos": to_pixel(knee[0], knee[1], w, h),
            "side": side,
        }

    def validate_constraints(self, angles):
        penalty = 0
        mistakes = []
        if angles["body_angle"] < self.ALIGNMENT_THRESHOLD:
            penalty += 20
            mistakes.append(f"Hips dropping ({int(angles['body_angle'])}°). Keep core tight.")
        return penalty, mistakes

    def draw_annotations(self, image, meta):
        self._put_angle(image, f"Body: {int(meta['body_angle'])}", meta["hip_pos"])
        self._put_angle(image, f"Drive: {int(meta['knee_drive'])}", meta["knee_pos"])
