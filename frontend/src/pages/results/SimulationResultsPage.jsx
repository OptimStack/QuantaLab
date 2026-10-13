import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import LoadingSpinner from '../../components/ui/LoadingSpinner';
import Badge from '../../components/ui/Badge';

const SimulationResultsPage = () => {
  const { jobId } = useParams();
  const [status, setStatus] = useState('running');
  const [activeTab, setActiveTab] = useState('histogram');

  useEffect(() => {
    // Mock simulation wait
    const timer = setTimeout(() => setStatus('completed'), 1500);
    return () => clearTimeout(timer);
  }, [jobId]);

  if (status === 'running') {
    return (
      <div className="h-[calc(100vh-4rem)] flex items-center justify-center">
        <LoadingSpinner label="Simulation in progress..." />
      </div>
    );
  }

  const tabs = [
    { id: 'histogram', name: 'Probability Histogram' },
    { id: 'blochsphere', name: 'Bloch Sphere' },
    { id: 'statevector', name: 'Statevector' },
    { id: 'diagram', name: 'Circuit Diagram' }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-start mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Simulation Results</h1>
          <div className="flex items-center gap-3 text-sm">
            <Badge variant="success">Completed</Badge>
            <span className="text-gray-500 dark:text-gray-400">Job ID: {jobId}</span>
            <span className="text-gray-500 dark:text-gray-400">•</span>
            <span className="text-gray-500 dark:text-gray-400">Backend: Qiskit Aer</span>
            <span className="text-gray-500 dark:text-gray-400">•</span>
            <span className="text-gray-500 dark:text-gray-400">1024 shots</span>
          </div>
        </div>
        <div className="flex gap-3">
          <Button variant="secondary">Download JSON</Button>
          <Button>Open in AI Tutor</Button>
        </div>
      </div>

      <Card className="mb-8 p-0 overflow-hidden">
        <div className="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 px-6">
          <nav className="-mb-px flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`${
                  activeTab === tab.id
                    ? 'border-quantum-500 text-quantum-600 dark:text-quantum-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                {tab.name}
              </button>
            ))}
          </nav>
        </div>
        <div className="p-6 h-[500px] flex items-center justify-center bg-white dark:bg-gray-950">
          {/* Placeholder for visualizations */}
          <div className="text-center text-gray-500 dark:text-gray-400">
            {activeTab === 'histogram' && 'Histogram component goes here'}
            {activeTab === 'blochsphere' && 'Bloch Sphere component goes here'}
            {activeTab === 'statevector' && 'Statevector table goes here'}
            {activeTab === 'diagram' && 'Circuit SVG diagram goes here'}
          </div>
        </div>
      </Card>
    </div>
  );
};

export default SimulationResultsPage;
