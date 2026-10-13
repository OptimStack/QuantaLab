from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.db import get_db
from app.models.circuit import Circuit
from app.schemas.circuit import CircuitCreate, CircuitUpdate, CircuitResponse
from app.utils.decorators import get_current_user
from app.models.user import User
from .qasm_converter import circuit_json_to_qasm, qasm_to_circuit_json

router = APIRouter()

@router.post("", response_model=CircuitResponse)
async def create_circuit(circuit_in: CircuitCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new_circuit = Circuit(
        owner_id=current_user.id,
        lesson_id=circuit_in.lesson_id,
        title=circuit_in.title,
        gate_sequence_json=circuit_in.gate_sequence_json,
        source_mode=circuit_in.source_mode,
        source_code=circuit_in.source_code
    )
    db.add(new_circuit)
    await db.commit()
    await db.refresh(new_circuit)
    return new_circuit

@router.get("", response_model=List[CircuitResponse])
async def list_circuits(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).where(Circuit.owner_id == current_user.id))
    return result.scalars().all()

@router.get("/{circuit_id}", response_model=CircuitResponse)
async def get_circuit(circuit_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).where(Circuit.id == circuit_id, Circuit.owner_id == current_user.id))
    circuit = result.scalar_one_or_none()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit

@router.put("/{circuit_id}", response_model=CircuitResponse)
async def update_circuit(circuit_id: UUID, circuit_in: CircuitUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).where(Circuit.id == circuit_id, Circuit.owner_id == current_user.id))
    circuit = result.scalar_one_or_none()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    
    circuit.title = circuit_in.title
    circuit.lesson_id = circuit_in.lesson_id
    circuit.gate_sequence_json = circuit_in.gate_sequence_json
    circuit.source_mode = circuit_in.source_mode
    circuit.source_code = circuit_in.source_code
    
    await db.commit()
    await db.refresh(circuit)
    return circuit

@router.get("/{circuit_id}/qasm")
async def export_qasm(circuit_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    circuit = await get_circuit(circuit_id, current_user, db)
    qasm_str = circuit_json_to_qasm(circuit.gate_sequence_json)
    return {"qasm": qasm_str}

@router.post("/{circuit_id}/qasm")
async def import_qasm(circuit_id: UUID, qasm_str: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    circuit = await get_circuit(circuit_id, current_user, db)
    gate_sequence = qasm_to_circuit_json(qasm_str)
    circuit.gate_sequence_json = gate_sequence
    await db.commit()
    await db.refresh(circuit)
    return circuit
