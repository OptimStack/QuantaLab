import React from 'react';
import GateBlock from './GateBlock';

const GatePalette = () => {
  const categories = [
    {
      name: 'Single-Qubit',
      gates: [
        { id: 'gate-h', gate: 'H', color: 'bg-blue-500' },
        { id: 'gate-x', gate: 'X', color: 'bg-green-500' },
        { id: 'gate-y', gate: 'Y', color: 'bg-green-600' },
        { id: 'gate-z', gate: 'Z', color: 'bg-green-700' },
        { id: 'gate-s', gate: 'S', color: 'bg-purple-500' },
        { id: 'gate-t', gate: 'T', color: 'bg-purple-600' },
      ]
    },
    {
      name: 'Multi-Qubit',
      gates: [
        { id: 'gate-cnot', gate: 'CX', color: 'bg-red-500' },
        { id: 'gate-cz', gate: 'CZ', color: 'bg-red-600' },
        { id: 'gate-swap', gate: 'SWAP', color: 'bg-orange-500' },
      ]
    },
    {
      name: 'Measurement',
      gates: [
        { id: 'gate-meas', gate: 'M', color: 'bg-gray-800 dark:bg-gray-700' },
      ]
    }
  ];

  return (
    <div className="space-y-6">
      {categories.map(cat => (
        <div key={cat.name}>
          <h4 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
            {cat.name}
          </h4>
          <div className="grid grid-cols-4 gap-2">
            {cat.gates.map(g => (
              <GateBlock key={g.id} id={g.id} gate={g.gate} color={g.color} isPaletteItem={true} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default GatePalette;
