import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db import Base
import enum

class JobBackend(str, enum.Enum):
    qiskit_aer = "qiskit_aer"
    pennylane = "pennylane"
    cirq = "cirq"
    qbraid = "qbraid"

class JobStatus(str, enum.Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"
    timeout = "timeout"

class SimulationJob(Base):
    __tablename__ = "simulation_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    circuit_id = Column(String(36), ForeignKey("circuits.id"), nullable=False)
    requested_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    backend = Column(Enum(JobBackend, native_enum=False), nullable=False)
    status = Column(Enum(JobStatus, native_enum=False), default=JobStatus.queued, nullable=False)
    result_json = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    circuit = relationship("Circuit")
    requester = relationship("User")
