import math


def calculate_angle(
    point_a: list[float],
    vertex: list[float],
    point_c: list[float],
) -> float:
    """Calculate the angle (in degrees) at the vertex formed by three 2D points."""
    ax, ay = point_a[0], point_a[1]
    bx, by = vertex[0], vertex[1]
    cx, cy = point_c[0], point_c[1]

    radians = math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx)
    angle = abs(radians * 180.0 / math.pi)

    if angle > 180.0:
        angle = 360.0 - angle

    return float(angle)


def detect_visible_side(landmarks, left_indices: list[int], right_indices: list[int]) -> str:
    """Return 'left' or 'right' based on which side's landmarks have higher visibility."""
    left_vis = sum(landmarks[i].visibility for i in left_indices)
    right_vis = sum(landmarks[i].visibility for i in right_indices)
    return "left" if left_vis > right_vis else "right"


def vertical_reference(point: list[float]) -> list[float]:
    """Create a point directly above the given point (for vertical angle calculations)."""
    return [point[0], point[1] - 0.5]


def to_pixel(norm_x: float, norm_y: float, w: int, h: int) -> tuple[int, int]:
    """Convert normalized (0-1) coordinates to pixel coordinates."""
    return (int(norm_x * w), int(norm_y * h))


def landmark_to_point(landmark) -> list[float]:
    """Extract [x, y] from a MediaPipe landmark."""
    return [landmark.x, landmark.y]
