import React from 'react';
import Plot from 'react-plotly.js';

const BlochSphere = ({ coordinates = [{x: 1, y: 0, z: 0}] }) => {
  // Simplistic representation for placeholder
  return (
    <div className="w-full h-full flex flex-col items-center justify-center">
      <Plot
        data={[
          {
            type: 'scatter3d',
            mode: 'lines',
            x: [0, coordinates[0]?.x || 0],
            y: [0, coordinates[0]?.y || 0],
            z: [0, coordinates[0]?.z || 1],
            line: { width: 6, color: '#6366f1' },
            name: 'State Vector'
          },
          {
            type: 'scatter3d',
            mode: 'markers',
            x: [coordinates[0]?.x || 0],
            y: [coordinates[0]?.y || 0],
            z: [coordinates[0]?.z || 1],
            marker: { size: 5, color: '#ef4444' }
          }
        ]}
        layout={{
          width: 400,
          height: 400,
          margin: { l: 0, r: 0, b: 0, t: 0 },
          scene: {
            xaxis: { title: 'X', range: [-1.2, 1.2] },
            yaxis: { title: 'Y', range: [-1.2, 1.2] },
            zaxis: { title: 'Z', range: [-1.2, 1.2] }
          },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent'
        }}
        config={{ displayModeBar: false }}
      />
      <div className="mt-4 flex gap-2">
        <button className="px-3 py-1 bg-quantum-100 text-quantum-700 rounded-md text-sm">Qubit 0</button>
        <button className="px-3 py-1 bg-gray-100 text-gray-700 rounded-md text-sm">Qubit 1</button>
      </div>
    </div>
  );
};

export default BlochSphere;
