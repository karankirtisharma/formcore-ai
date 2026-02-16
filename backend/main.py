import logging
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.pose_engine import PoseAnalyzer
from app.schemas import AnalysisResult
from app.analyzers.registry import ExerciseRegistry

logger = logging.getLogger(__name__)

app = FastAPI(title="FormCore AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pose_analyzer = PoseAnalyzer()


@app.get("/")
def read_root():
    return {"message": "FormCore AI Backend is running"}


@app.get("/exercises")
def list_exercises():
    """Return all supported exercise types for frontend auto-sync."""
    return {"exercises": ExerciseRegistry.list_exercises()}


@app.post("/analyze/image", response_model=AnalysisResult)
async def analyze_image_endpoint(file: UploadFile = File(...), exercise: str = "squat"):
    contents = await file.read()
    result = pose_analyzer.process_image(contents, exercise_type=exercise)
    if result is None:
        return AnalysisResult(score=0, mistakes=["Could not process image"])
    return result


@app.post("/analyze/video", response_model=AnalysisResult)
async def analyze_video_endpoint(file: UploadFile = File(...), exercise: str = "squat"):
    try:
        contents = await file.read()
        result = pose_analyzer.process_video(contents, exercise_type=exercise)
        if result is None:
            return AnalysisResult(score=0, mistakes=["Could not process video"])
        return result
    except Exception as e:
        logger.exception("Error processing video")
        return JSONResponse(status_code=500, content={"message": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
