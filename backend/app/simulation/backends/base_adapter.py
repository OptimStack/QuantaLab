from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class CircuitSpec:
    gate_sequence: list  # List of gate operations
    num_qubits: int
    source_code: Optional[str] = None  # Raw Python code if code-mode

@dataclass 
class SimulationResult:
    backend_name: str
    statevector: Optional[list] = None  # Complex amplitudes as [real, imag] pairs
    measurement_counts: Optional[dict] = None  # {'00': 512, '11': 488}
    bloch_coordinates: Optional[list] = None  # [{x, y, z}] per qubit
    execution_time_ms: float = 0.0
    num_qubits: int = 0
    error: Optional[str] = None

class SimulationAdapter(ABC):
    @abstractmethod
    def run(self, circuit: CircuitSpec, shots: int = 1024) -> SimulationResult:
        ...
    
    @abstractmethod
    def is_available(self) -> bool:
        ...
    
    @property
    @abstractmethod
    def name(self) -> str:
        ...
