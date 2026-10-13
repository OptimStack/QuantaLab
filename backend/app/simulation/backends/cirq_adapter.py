import time
from .base_adapter import SimulationAdapter, CircuitSpec, SimulationResult

try:
    import cirq
    CIRQ_AVAILABLE = True
except ImportError:
    CIRQ_AVAILABLE = False

class CirqAdapter(SimulationAdapter):
    @property
    def name(self) -> str:
        return "cirq"

    def is_available(self) -> bool:
        return CIRQ_AVAILABLE

    def run(self, circuit: CircuitSpec, shots: int = 1024) -> SimulationResult:
        if not self.is_available():
            return SimulationResult(backend_name=self.name, error="Cirq is not installed.")

        start_time = time.time()
        try:
            qubits = [cirq.LineQubit(i) for i in range(circuit.num_qubits)]
            qc = cirq.Circuit()
            
            for gate in circuit.gate_sequence:
                name = gate.get("name").lower()
                q_idx = gate.get("qubits", [])
                
                if name == "h":
                    qc.append(cirq.H(qubits[q_idx[0]]))
                elif name == "x":
                    qc.append(cirq.X(qubits[q_idx[0]]))
                elif name == "cx" or name == "cnot":
                    qc.append(cirq.CNOT(qubits[q_idx[0]], qubits[q_idx[1]]))
                elif name == "measure":
                    qc.append(cirq.measure(*qubits, key='result'))

            simulator = cirq.Simulator()
            result = simulator.run(qc, repetitions=shots)
            
            counts = result.histogram(key='result')
            # convert integer keys to bitstrings
            formatted_counts = {f"{k:0{circuit.num_qubits}b}": v for k, v in counts.items()}
            
            exec_time = (time.time() - start_time) * 1000
            return SimulationResult(
                backend_name=self.name,
                measurement_counts=formatted_counts,
                execution_time_ms=exec_time,
                num_qubits=circuit.num_qubits
            )
        except Exception as e:
            return SimulationResult(backend_name=self.name, error=str(e))
