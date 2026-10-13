import React from 'react';
import Card from '../../components/ui/Card';

const CohortDashboardPage = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Cohort Dashboard</h1>
        <select className="border border-gray-300 dark:border-gray-700 rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
          <option>Fall 2026 - CS480</option>
          <option>Spring 2026 - CS480</option>
        </select>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card className="text-center">
          <div className="text-sm font-medium text-gray-500 dark:text-gray-400">Active Learners</div>
          <div className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">45</div>
        </Card>
        <Card className="text-center">
          <div className="text-sm font-medium text-gray-500 dark:text-gray-400">Avg Completion</div>
          <div className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">65%</div>
        </Card>
        <Card className="text-center">
          <div className="text-sm font-medium text-gray-500 dark:text-gray-400">Avg Assessment Score</div>
          <div className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">82%</div>
        </Card>
      </div>

      <Card>
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Learner Progress</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Progress</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Avg Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Last Active</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">Alice Johnson</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">75%</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">92%</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">2 hrs ago</td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">Bob Smith</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">40%</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">78%</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">1 day ago</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

export default CohortDashboardPage;
