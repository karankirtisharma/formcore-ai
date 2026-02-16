from pydantic import BaseModel
from typing import List, Optional

class AnalysisResult(BaseModel):
    score: int
    mistakes: List[str]
    image_base64: Optional[str] = None
    video_base64: Optional[str] = None
