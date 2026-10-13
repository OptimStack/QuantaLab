import React from 'react';

const StatevectorView = ({ statevector = [{real: 0.707, imag: 0}, {real: 0, imag: 0}, {real: 0, imag: 0}, {real: 0.707, imag: 0}] }) => {
  
  const toBinaryString = (num, length) => num.toString(2).padStart(length, '0');
  const numQubits = Math.log2(statevector.length);

  return (
    <div className="w-full max-w-2xl mx-auto">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead className="bg-gray-50 dark:bg-gray-800">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Basis State</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Amplitude (a + bi)</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Magnitude |α|²</th>
          </tr>
        </thead>
        <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
          {statevector.map((amp, idx) => {
            const magSq = (amp.real * amp.real + amp.imag * amp.imag).toFixed(4);
            // Hide extremely small amplitudes
            if (magSq < 0.0001) return null;
            
            return (
              <tr key={idx}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-quantum-600 dark:text-quantum-400">
                  |{toBinaryString(idx, numQubits)}⟩
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300 font-mono">
                  {amp.real.toFixed(3)} {amp.imag >= 0 ? '+' : '-'} {Math.abs(amp.imag).toFixed(3)}i
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">
                  <div className="flex items-center gap-2">
                    <span>{magSq}</span>
                    <div className="w-24 bg-gray-200 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
                      <div className="bg-quantum-500 h-full" style={{ width: `${magSq * 100}%` }}></div>
                    </div>
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default StatevectorView;
