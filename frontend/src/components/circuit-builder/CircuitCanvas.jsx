import React, { useState } from 'react';
import { DndContext } from '@dnd-kit/core';
import GatePalette from './GatePalette';

const CircuitCanvas = () => {
  const [qubits, setQubits] = useState([0, 1, 2]);
  const steps = 10;

  // This is a placeholder for the actual drag and drop logic
  const handleDragEnd = (event) => {
    console.log("Dropped", event);
  };

  return (
    <DndContext onDragEnd={handleDragEnd}>
      <div className="flex w-full h-full">
        <div className="w-64 border-r border-gray-200 dark:border-gray-800 p-4 bg-gray-50 dark:bg-gray-800 overflow-y-auto">
          <h3 className="font-semibold text-gray-700 dark:text-gray-300 mb-6">Gate Palette</h3>
          <GatePalette />
        </div>
        
        <div className="flex-1 p-6 overflow-auto bg-white dark:bg-gray-900">
          <div className="relative min-w-max">
            {/* Steps header */}
            <div className="flex ml-16 mb-4">
              {Array.from({ length: steps }).map((_, i) => (
                <div key={`step-${i}`} className="w-14 text-center text-xs text-gray-400">
                  {i}
                </div>
              ))}
            </div>

            {/* Qubit wires */}
            {qubits.map((q) => (
              <div key={`q${q}`} className="flex items-center h-14 relative group">
                <div className="w-12 text-sm font-medium text-gray-700 dark:text-gray-300">
                  q[{q}]
                </div>
                {/* The wire */}
                <div className="absolute left-14 right-0 h-px bg-gray-300 dark:bg-gray-700 group-hover:bg-quantum-300"></div>
                
                {/* Drop zones for each step */}
                <div className="flex ml-2">
                  {Array.from({ length: steps }).map((_, i) => (
                    <div 
                      key={`drop-${q}-${i}`} 
                      className="w-14 h-14 flex items-center justify-center border border-transparent hover:border-dashed hover:border-quantum-400 relative z-0"
                    >
                      {/* Placed gates would render here */}
                    </div>
                  ))}
                </div>
              </div>
            ))}

            <div className="mt-6 flex gap-2">
              <button 
                onClick={() => setQubits([...qubits, qubits.length])}
                className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-gray-700"
              >
                + Add Qubit
              </button>
              {qubits.length > 1 && (
                <button 
                  onClick={() => setQubits(qubits.slice(0, -1))}
                  className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-800 text-red-600 dark:text-red-400 rounded hover:bg-gray-200 dark:hover:bg-gray-700"
                >
                  - Remove Qubit
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </DndContext>
  );
};

export default CircuitCanvas;
