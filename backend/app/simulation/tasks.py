import asyncio
from datetime import datetime
from uuid import UUID
from sqlalchemy import select
from app.db import SessionLocal
from app.models.simulation_job import SimulationJob, JobStatus
from app.models.circuit import Circuit
from app.simulation.backends.base_adapter import CircuitSpec
import dataclasses
import logging

logger = logging.getLogger(__name__)

def _get_adapters():
    adapters = {}
    try:
        from app.simulation.backends.qiskit_adapter import QiskitAdapter
        adapters["qiskit_aer"] = QiskitAdapter()
    except ImportError:
        logger.warning("Qiskit not installed, qiskit_aer backend unavailable")
    try:
        from app.simulation.backends.pennylane_adapter import PennylaneAdapter
        adapters["pennylane"] = PennylaneAdapter()
    except ImportError:
        logger.warning("PennyLane not installed, pennylane backend unavailable")
    try:
        from app.simulation.backends.cirq_adapter import CirqAdapter
        adapters["cirq"] = CirqAdapter()
    except ImportError:
        logger.warning("Cirq not installed, cirq backend unavailable")
    try:
        from app.simulation.backends.qbraid_adapter import QbraidAdapter
        adapters["qbraid"] = QbraidAdapter()
    except ImportError:
        logger.warning("qBraid not installed, qbraid backend unavailable")
    return adapters

async def _run_job(job_id_str: str):
    async with SessionLocal() as db:
        job_id = UUID(job_id_str)
        result = await db.execute(select(SimulationJob).where(SimulationJob.id == job_id))
        job = result.scalar_one_or_none()
        
        if not job:
            return
            
        job.status = JobStatus.running
        job.started_at = datetime.utcnow()
        await db.commit()
        
        circuit_result = await db.execute(select(Circuit).where(Circuit.id == job.circuit_id))
        circuit = circuit_result.scalar_one_or_none()
        
        if not circuit:
            job.status = JobStatus.failed
            job.error_message = "Circuit not found"
            job.completed_at = datetime.utcnow()
            await db.commit()
            return
            
        adapters = _get_adapters()
        adapter = adapters.get(job.backend.value if hasattr(job.backend, 'value') else job.backend)
        if not adapter:
            job.status = JobStatus.failed
            job.error_message = f"Backend '{job.backend}' not available. Install the required SDK."
            job.completed_at = datetime.utcnow()
            await db.commit()
            return
            
        num_qubits = 0
        gate_seq = circuit.gate_sequence_json or []
        for gate in gate_seq:
            qubits = gate.get("qubits", [])
            if qubits:
                num_qubits = max(num_qubits, max(qubits) + 1)
        if num_qubits == 0:
            num_qubits = 1
            
        spec = CircuitSpec(
            gate_sequence=gate_seq,
            num_qubits=num_qubits,
            source_code=circuit.source_code
        )
        
        try:
            sim_result = adapter.run(spec)
            if sim_result.error:
                job.status = JobStatus.failed
                job.error_message = sim_result.error
            else:
                job.status = JobStatus.completed
                job.result_json = dataclasses.asdict(sim_result)
        except Exception as e:
            job.status = JobStatus.failed
            job.error_message = str(e)
            
        job.completed_at = datetime.utcnow()
        await db.commit()

def run_simulation_job_sync(job_id: str):
    """Run simulation job synchronously (for use with BackgroundTasks)."""
    asyncio.run(_run_job(job_id))
