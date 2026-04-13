import logging
import os
import shutil
import uuid
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from app.pose_engine import PoseAnalyzer
from app.schemas import AnalysisResult
from app.analyzers.registry import ExerciseRegistry

logger = logging.getLogger(__name__)

MEDIA_DIR = "media"

# Global PoseAnalyzer and Jobs Dictionary
pose_analyzer: PoseAnalyzer = None
JOBS = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup media dir
    if os.path.exists(MEDIA_DIR):
        shutil.rmtree(MEDIA_DIR)
    os.makedirs(MEDIA_DIR, exist_ok=True)
    
    # Initialize singleton model
    global pose_analyzer
    pose_analyzer = PoseAnalyzer()
    
    # Ensure registries are loaded eagerly (if registry supports it)
    ExerciseRegistry.list_exercises()
    
    yield

app = FastAPI(title="FormCore AI", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

@app.get("/")
def read_root():
    return {"message": "FormCore AI Backend is running"}


@app.get("/exercises")
def list_exercises():
    """Return all supported exercise types for frontend auto-sync."""
    return {"exercises": ExerciseRegistry.list_exercises()}


@app.post("/analyze/image", response_model=dict)
async def analyze_image_endpoint(file: UploadFile = File(...), exercise: str = "squat"):
    contents = await file.read()
    result = pose_analyzer.process_image(contents, exercise_type=exercise)
    if result is None:
        return {"score": 0, "mistakes": ["Could not process image"]}
    return result


def process_video_job(job_id: str, contents: bytes, exercise: str):
    try:
        result = pose_analyzer.process_video(contents, exercise_type=exercise)
        if result is None:
            JOBS[job_id] = {"status": "error", "message": "Could not process video"}
        else:
            JOBS[job_id] = {"status": "complete", "result": result}
    except Exception as e:
        logger.exception("Error in background processing")
        JOBS[job_id] = {"status": "error", "message": str(e)}

@app.post("/analyze/video")
async def analyze_video_endpoint(background_tasks: BackgroundTasks, file: UploadFile = File(...), exercise: str = "squat"):
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "processing"}
    
    contents = await file.read()
    background_tasks.add_task(process_video_job, job_id, contents, exercise)
    
    return {"job_id": job_id, "status": "processing"}

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"message": "Job not found"})
    return job

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
