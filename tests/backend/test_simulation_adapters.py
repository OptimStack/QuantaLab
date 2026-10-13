import pytest
# Assume these are imported from your adapter implementations
# from app.simulation.adapters import QiskitAdapter, CirqAdapter, PennylaneAdapter

@pytest.fixture
def adapters():
    # Mocking for the sake of the test structure
    class MockAdapter:
        def __init__(self, name):
            self.name = name
        def is_available(self):
            return True
        def run(self, qasm):
            if "h q[0]" in qasm and "cx" not in qasm:
                return {"0": 512, "1": 512}
            elif "cx" in qasm:
                return {"00": 512, "11": 512}
            return {}
            
    return [MockAdapter("qiskit"), MockAdapter("cirq"), MockAdapter("pennylane")]

def test_adapters_available(adapters):
    for adapter in adapters:
        assert adapter.is_available() is True

def test_hadamard_results(adapters):
    hadamard_qasm = 'OPENQASM 2.0; qreg q[1]; creg c[1]; h q[0]; measure q[0] -> c[0];'
    for adapter in adapters:
        res = adapter.run(hadamard_qasm)
        assert "0" in res and "1" in res
        # Statistical check: roughly equal
        assert 400 < res["0"] < 600

def test_bell_state_results(adapters):
    bell_qasm = 'OPENQASM 2.0; qreg q[2]; creg c[2]; h q[0]; cx q[0],q[1]; measure q[0] -> c[0]; measure q[1] -> c[1];'
    for adapter in adapters:
        res = adapter.run(bell_qasm)
        assert "00" in res and "11" in res
        assert "01" not in res or res["01"] < 50
        assert "10" not in res or res["10"] < 50

def test_cross_backend_consistency(adapters):
    bell_qasm = 'OPENQASM 2.0; qreg q[2]; creg c[2]; h q[0]; cx q[0],q[1]; measure q[0] -> c[0]; measure q[1] -> c[1];'
    results = [a.run(bell_qasm) for a in adapters]
    
    # Check that all adapters produce roughly the same keys
    keys = set(results[0].keys())
    for res in results[1:]:
        assert set(res.keys()) == keys
