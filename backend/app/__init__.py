from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings

from app.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize resources and tables
    await init_db()
    yield
    # Shutdown: Clean up resources

def create_app() -> FastAPI:
    app = FastAPI(title="QuantaLab API", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.cors_allowed_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    async def health_check():
        return {"status": "ok"}

    from app.auth.routes import router as auth_router
    from app.courses.routes import router as courses_router
    from app.circuits.routes import router as circuits_router
    from app.simulation.routes import router as simulation_router
    from app.assessments.routes import router as assessments_router
    from app.progress.routes import router as progress_router
    from app.instructor.routes import router as instructor_router
    from app.ai_tutor.routes_ws import router as ai_tutor_router

    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
    app.include_router(courses_router, prefix="/api/courses", tags=["courses"])
    app.include_router(circuits_router, prefix="/api/circuits", tags=["circuits"])
    app.include_router(simulation_router, prefix="/api", tags=["simulation"]) # uses /simulate and /sandbox/status
    app.include_router(assessments_router, prefix="/api/assessments", tags=["assessments"])
    app.include_router(progress_router, prefix="/api/progress", tags=["progress"])
    app.include_router(instructor_router, prefix="/api/instructor", tags=["instructor"])
    app.include_router(ai_tutor_router, prefix="/ws/tutor", tags=["ai_tutor"])

    return app
