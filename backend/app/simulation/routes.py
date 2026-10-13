from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.db import get_db
from app.models.simulation_job import SimulationJob, JobStatus
from app.schemas.simulation import SimulationJobCreate, SimulationJobResponse
from app.utils.decorators import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/simulate", response_model=SimulationJobResponse)
async def submit_simulation(
    job_in: SimulationJobCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_job = SimulationJob(
        circuit_id=job_in.circuit_id,
        requested_by=current_user.id,
        backend=job_in.backend,
        status=JobStatus.queued
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    
    from app.simulation.tasks import run_simulation_job_sync
    background_tasks.add_task(run_simulation_job_sync, str(new_job.id))
    
    return new_job

@router.get("/simulate/{job_id}", response_model=SimulationJobResponse)
async def get_simulation_job(job_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SimulationJob).where(SimulationJob.id == job_id, SimulationJob.requested_by == current_user.id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/sandbox/status")
async def sandbox_status():
    return {"status": "ok", "layer": "sandbox"}
