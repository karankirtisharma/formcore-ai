"""Lazy-loading exercise registry — zero top-level analyzer imports."""
import importlib
from app.analyzers.base import BaseAnalyzer

# Maps exercise name → (module_path, class_name)
_REGISTRY: dict[str, tuple[str, str]] = {
    "squat":                  ("app.analyzers.squat",                  "SquatAnalyzer"),
    "pushup":                 ("app.analyzers.pushup",                 "PushupAnalyzer"),
    "deadlift":               ("app.analyzers.deadlift",               "DeadliftAnalyzer"),
    "lunge":                  ("app.analyzers.lunge",                  "LungeAnalyzer"),
    "romanian_deadlift":      ("app.analyzers.romanian_deadlift",      "RomanianDeadliftAnalyzer"),
    "glute_bridge":           ("app.analyzers.glute_bridge",           "GluteBridgeAnalyzer"),
    "calf_raise":             ("app.analyzers.calf_raise",             "CalfRaiseAnalyzer"),
    "bulgarian_split_squat":  ("app.analyzers.bulgarian_split_squat",  "BulgarianSplitSquatAnalyzer"),
    "overhead_press":         ("app.analyzers.overhead_press",         "OverheadPressAnalyzer"),
    "shoulder_press":         ("app.analyzers.shoulder_press",         "ShoulderPressAnalyzer"),
    "bicep_curl":             ("app.analyzers.bicep_curl",             "BicepCurlAnalyzer"),
    "tricep_dip":             ("app.analyzers.tricep_dip",             "TricepDipAnalyzer"),
    "plank":                  ("app.analyzers.plank",                  "PlankAnalyzer"),
    "mountain_climber":       ("app.analyzers.mountain_climber",       "MountainClimberAnalyzer"),
}

_instances: dict[str, BaseAnalyzer] = {}

class ExerciseRegistry:

    @classmethod
    def get_analyzer(cls, exercise_type: str) -> BaseAnalyzer:
        exercise_type = exercise_type.lower()
        if exercise_type not in _instances:
            exercise_type = "squat"
        return _instances[exercise_type]

    @classmethod
    def list_exercises(cls) -> list[str]:
        if not _instances:
            for ex, (mod_path, cls_name) in _REGISTRY.items():
                module = importlib.import_module(mod_path)
                _instances[ex] = getattr(module, cls_name)()
        return sorted(_instances.keys())

