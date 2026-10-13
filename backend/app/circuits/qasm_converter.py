import json

def circuit_json_to_qasm(gate_sequence_json: list) -> str:
    """Convert internal JSON format to OpenQASM 2.0 string."""
    qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n'
    
    # Determine max qubit index
    max_qubit = -1
    for gate in gate_sequence_json:
        qubits = gate.get("qubits", [])
        if qubits:
            max_qubit = max(max_qubit, max(qubits))
    
    if max_qubit >= 0:
        qasm += f"qreg q[{max_qubit + 1}];\n"
        qasm += f"creg c[{max_qubit + 1}];\n"
        
    for gate in gate_sequence_json:
        name = gate.get("name", "").lower()
        qubits = gate.get("qubits", [])
        params = gate.get("params", [])
        
        q_str = ",".join([f"q[{q}]" for q in qubits])
        if name == "measure":
            if qubits:
                qasm += f"measure q[{qubits[0]}] -> c[{qubits[0]}];\n"
        else:
            if params:
                p_str = ",".join(map(str, params))
                qasm += f"{name}({p_str}) {q_str};\n"
            else:
                qasm += f"{name} {q_str};\n"
                
    return qasm

def qasm_to_circuit_json(qasm_str: str) -> list:
    """Convert OpenQASM 2.0 string to internal JSON format. Basic parsing."""
    lines = qasm_str.strip().split('\n')
    gate_sequence = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('OPENQASM') or line.startswith('include') or line.startswith('qreg') or line.startswith('creg'):
            continue
            
        if line.startswith('measure'):
            # measure q[0] -> c[0];
            parts = line.replace('measure', '').replace(';', '').split('->')
            if len(parts) == 2:
                q_part = parts[0].strip()
                q_idx = int(q_part.split('[')[1].split(']')[0])
                gate_sequence.append({"name": "measure", "qubits": [q_idx], "params": []})
        else:
            # h q[0]; or rx(pi) q[0];
            parts = line.split(' ')
            gate_part = parts[0]
            qubits_part = ' '.join(parts[1:]).replace(';', '')
            
            name = gate_part.split('(')[0]
            params = []
            if '(' in gate_part:
                p_str = gate_part.split('(')[1].split(')')[0]
                params = [p_str]  # simplified, assuming string param
                
            qubits_list = qubits_part.split(',')
            qubits = [int(q.strip().split('[')[1].split(']')[0]) for q in qubits_list]
            
            gate_sequence.append({"name": name, "qubits": qubits, "params": params})
            
    return gate_sequence
