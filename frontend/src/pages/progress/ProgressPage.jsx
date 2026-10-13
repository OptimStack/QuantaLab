import React from 'react';
import Card from '../../components/ui/Card';
import Badge from '../../components/ui/Badge';
import { formatPercentage } from '../../utils/format';

const ProgressPage = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">My Progress</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card className="flex flex-col items-center justify-center p-6 text-center">
          <div className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">Overall Completion</div>
          <div className="mt-2 text-4xl font-extrabold text-quantum-600 dark:text-quantum-400">42%</div>
        </Card>
        <Card className="flex flex-col items-center justify-center p-6 text-center">
          <div className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">Circuits Built</div>
          <div className="mt-2 text-4xl font-extrabold text-gray-900 dark:text-white">14</div>
        </Card>
        <Card className="flex flex-col items-center justify-center p-6 text-center">
          <div className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">Average Score</div>
          <div className="mt-2 text-4xl font-extrabold text-green-600 dark:text-green-400">88%</div>
        </Card>
      </div>

      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Course Progress</h2>
      <div className="space-y-4">
        {[
          { title: 'Introduction to Quantum Computing', progress: 0.8 },
          { title: 'Quantum Algorithms', progress: 0.15 },
          { title: 'Error Correction', progress: 0.0 }
        ].map((course, idx) => (
          <Card key={idx}>
            <div className="flex justify-between items-center mb-2">
              <span className="font-medium text-gray-900 dark:text-white">{course.title}</span>
              <span className="text-sm text-gray-500 dark:text-gray-400">{formatPercentage(course.progress)}</span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
              <div 
                className="bg-quantum-600 h-2.5 rounded-full" 
                style={{ width: `${course.progress * 100}%` }}
              ></div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default ProgressPage;
