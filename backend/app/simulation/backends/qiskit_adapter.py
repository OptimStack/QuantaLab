import time
from .base_adapter import SimulationAdapter, CircuitSpec, SimulationResult

try:
    import qiskit
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

class QiskitAdapter(SimulationAdapter):
    @property
    def name(self) -> str:
        return "qiskit_aer"

    def is_available(self) -> bool:
        return QISKIT_AVAILABLE

    def run(self, circuit: CircuitSpec, shots: int = 1024) -> SimulationResult:
        if not self.is_available():
            return SimulationResult(backend_name=self.name, error="Qiskit is not installed.")

        start_time = time.time()
        try:
            qc = QuantumCircuit(circuit.num_qubits)
            for gate in circuit.gate_sequence:
                name = gate.get("name").lower()
                qubits = gate.get("qubits", [])
                
                if name == "h":
                    qc.h(*qubits)
                elif name == "x":
                    qc.x(*qubits)
                elif name == "cx" or name == "cnot":
                    qc.cx(*qubits)
                elif name == "measure":
                    qc.measure_all()
                # Add more gates as needed...

            simulator = AerSimulator()
            compiled_circuit = qiskit.transpile(qc, simulator)
            result = simulator.run(compiled_circuit, shots=shots).result()
            
            counts = {}
            if "measure" in [g.get("name").lower() for g in circuit.gate_sequence]:
                counts = result.get_counts()
            
            exec_time = (time.time() - start_time) * 1000
            return SimulationResult(
                backend_name=self.name,
                measurement_counts=counts,
                execution_time_ms=exec_time,
                num_qubits=circuit.num_qubits
            )
        except Exception as e:
            return SimulationResult(backend_name=self.name, error=str(e))
