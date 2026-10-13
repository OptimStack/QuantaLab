export const circuitToQasm = (gateSequence, numQubits) => {
  let qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n\n';
  qasm += `qreg q[${numQubits}];\n`;
  qasm += `creg c[${numQubits}];\n\n`;

  // Sort gates by step to maintain temporal order
  const sortedGates = [...gateSequence].sort((a, b) => a.step - b.step);

  for (const op of sortedGates) {
    const { gate, qubit, target_qubit, params } = op;
    const g = gate.toLowerCase();

    if (g === 'measure' || g === 'm') {
      qasm += `measure q[${qubit}] -> c[${qubit}];\n`;
    } else if (g === 'cx' || g === 'cnot') {
      qasm += `cx q[${qubit}], q[${target_qubit}];\n`;
    } else if (g === 'cz') {
      qasm += `cz q[${qubit}], q[${target_qubit}];\n`;
    } else if (g === 'swap') {
      qasm += `swap q[${qubit}], q[${target_qubit}];\n`;
    } else if (['rx', 'ry', 'rz'].includes(g) && params) {
      qasm += `${g}(${params}) q[${qubit}];\n`;
    } else {
      qasm += `${g} q[${qubit}];\n`;
    }
  }

  return qasm;
};

export const qasmToCircuit = (qasmString) => {
  // Simplified parser for demo
  const lines = qasmString.split('\n');
  const sequence = [];
  let stepCounter = 0;

  for (const line of lines) {
    const l = line.trim();
    if (!l || l.startsWith('//') || l.startsWith('OPENQASM') || l.startsWith('include') || l.startsWith('qreg') || l.startsWith('creg')) continue;

    if (l.startsWith('measure')) {
      const match = l.match(/q\[(\d+)\].*c\[(\d+)\]/);
      if (match) {
        sequence.push({ gate: 'M', qubit: parseInt(match[1]), step: stepCounter++ });
      }
    } else if (l.startsWith('cx')) {
      const match = l.match(/q\[(\d+)\],\s*q\[(\d+)\]/);
      if (match) {
        sequence.push({ gate: 'CX', qubit: parseInt(match[1]), target_qubit: parseInt(match[2]), step: stepCounter++ });
      }
    } else {
      const match = l.match(/([a-z]+)\s+q\[(\d+)\]/);
      if (match) {
        sequence.push({ gate: match[1].toUpperCase(), qubit: parseInt(match[2]), step: stepCounter++ });
      }
    }
  }

  return sequence;
};
