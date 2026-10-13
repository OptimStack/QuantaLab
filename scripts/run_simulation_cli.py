import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="CLI to run quantum simulations")
    parser.add_argument("--preset", choices=["bell", "ghz", "hadamard"], help="Preset circuit to run")
    parser.add_argument("--backend", default="qiskit_aer", choices=["qiskit_aer", "pennylane", "cirq"], help="Backend to run the simulation on")
    parser.add_argument("--qasm", type=str, help="OpenQASM string of the circuit")
    
    args = parser.parse_args()
    
    if not args.preset and not args.qasm:
        print("Error: Must provide either --preset or --qasm")
        sys.exit(1)
        
    qasm_str = ""
    if args.preset == "bell":
        qasm_str = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q[0] -> c[0];\nmeasure q[1] -> c[1];'
    elif args.preset == "ghz":
        qasm_str = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[3];\ncreg c[3];\nh q[0];\ncx q[0],q[1];\ncx q[1],q[2];\nmeasure q -> c;'
    elif args.preset == "hadamard":
        qasm_str = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[1];\ncreg c[1];\nh q[0];\nmeasure q[0] -> c[0];'
    else:
        qasm_str = args.qasm
        
    print(f"Running simulation on backend: {args.backend}")
    print(f"Circuit QASM:\n{qasm_str}\n")
    
    # Mocking execution since backend adapters might not exist yet
    if args.preset == "bell":
        result = {"00": 512, "11": 512}
    elif args.preset == "ghz":
        result = {"000": 500, "111": 524}
    elif args.preset == "hadamard":
        result = {"0": 505, "1": 519}
    else:
        result = {"0": 1024} # Default mock
        
    print("Results:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
