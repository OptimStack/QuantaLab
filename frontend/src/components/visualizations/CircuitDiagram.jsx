import React from 'react';

const CircuitDiagram = ({ sequence = [] }) => {
  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-8">
      <div className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-inner border border-gray-200 dark:border-gray-700 overflow-x-auto min-w-[600px]">
        {/* Placeholder for SVG Circuit Diagram */}
        <div className="text-center text-gray-500 dark:text-gray-400 mb-4">
          Visual Circuit Representation
        </div>
        
        <div className="relative">
          {/* Qubit 0 wire */}
          <div className="flex items-center mb-8 relative">
            <span className="w-12 font-mono text-gray-700 dark:text-gray-300">q[0]</span>
            <div className="flex-1 h-px bg-gray-400 dark:bg-gray-600 relative flex items-center">
              <div className="w-10 h-10 bg-blue-500 text-white rounded flex items-center justify-center font-bold absolute left-10">H</div>
              <div className="w-3 h-3 bg-red-500 rounded-full absolute left-32"></div>
              {/* CX wire connecting 0 to 1 */}
              <div className="w-px h-12 bg-red-500 absolute left-[134px] top-1"></div>
            </div>
          </div>
          
          {/* Qubit 1 wire */}
          <div className="flex items-center relative">
            <span className="w-12 font-mono text-gray-700 dark:text-gray-300">q[1]</span>
            <div className="flex-1 h-px bg-gray-400 dark:bg-gray-600 relative flex items-center">
              <div className="w-8 h-8 rounded-full border-2 border-red-500 text-red-500 flex items-center justify-center font-bold absolute left-30 bg-white dark:bg-gray-800">+</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CircuitDiagram;
