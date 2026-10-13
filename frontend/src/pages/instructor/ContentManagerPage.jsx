import React from 'react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';

const ContentManagerPage = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Content Manager</h1>
        <Button>+ Create Course</Button>
      </div>

      <Card>
        <div className="space-y-4">
          <div className="flex justify-between items-center p-4 border border-gray-200 dark:border-gray-700 rounded-md">
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Introduction to Quantum Computing</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">5 Modules • 20 Lessons</p>
            </div>
            <div className="flex gap-2">
              <Button variant="ghost" size="sm">Edit</Button>
              <Button variant="danger" size="sm">Delete</Button>
            </div>
          </div>
          <div className="flex justify-between items-center p-4 border border-gray-200 dark:border-gray-700 rounded-md">
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Quantum Algorithms</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">8 Modules • 32 Lessons</p>
            </div>
            <div className="flex gap-2">
              <Button variant="ghost" size="sm">Edit</Button>
              <Button variant="danger" size="sm">Delete</Button>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default ContentManagerPage;
