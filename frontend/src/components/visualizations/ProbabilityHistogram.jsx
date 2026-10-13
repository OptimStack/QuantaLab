import React from 'react';
import Plot from 'react-plotly.js';

const ProbabilityHistogram = ({ counts = {'00': 512, '11': 512} }) => {
  const states = Object.keys(counts);
  const values = Object.values(counts);
  const total = values.reduce((a, b) => a + b, 0);
  const probabilities = values.map(v => v / total);

  return (
    <div className="w-full h-full flex items-center justify-center">
      <Plot
        data={[
          {
            x: states,
            y: probabilities,
            type: 'bar',
            marker: { color: '#6366f1' },
            text: probabilities.map(p => `${(p * 100).toFixed(1)}%`),
            textposition: 'auto',
          }
        ]}
        layout={{
          width: 600,
          height: 400,
          title: 'Measurement Probabilities',
          xaxis: { title: 'Computational Basis State' },
          yaxis: { title: 'Probability', range: [0, 1] },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          font: { color: '#9ca3af' }
        }}
        config={{ displayModeBar: false }}
      />
    </div>
  );
};

export default ProbabilityHistogram;
