import time
from .base_adapter import SimulationAdapter, CircuitSpec, SimulationResult

try:
    import pennylane as qml
    import numpy as np
    PENNYLANE_AVAILABLE = True
except ImportError:
    PENNYLANE_AVAILABLE = False

class PennylaneAdapter(SimulationAdapter):
    @property
    def name(self) -> str:
        return "pennylane"

    def is_available(self) -> bool:
        return PENNYLANE_AVAILABLE

    def run(self, circuit: CircuitSpec, shots: int = 1024) -> SimulationResult:
        if not self.is_available():
            return SimulationResult(backend_name=self.name, error="PennyLane is not installed.")

        start_time = time.time()
        try:
            dev = qml.device("default.qubit", wires=circuit.num_qubits, shots=shots)
            
            @qml.qnode(dev)
            def qfunc():
                for gate in circuit.gate_sequence:
                    name = gate.get("name").lower()
                    qubits = gate.get("qubits", [])
                    
                    if name == "h":
                        qml.Hadamard(wires=qubits[0])
                    elif name == "x":
                        qml.PauliX(wires=qubits[0])
                    elif name == "cx" or name == "cnot":
                        qml.CNOT(wires=qubits)
                
                return qml.counts()

            result = qfunc()
            counts = {str(k): int(v) for k, v in result.items()} if isinstance(result, dict) else {}
            
            exec_time = (time.time() - start_time) * 1000
            return SimulationResult(
                backend_name=self.name,
                measurement_counts=counts,
                execution_time_ms=exec_time,
                num_qubits=circuit.num_qubits
            )
        except Exception as e:
            return SimulationResult(backend_name=self.name, error=str(e))
