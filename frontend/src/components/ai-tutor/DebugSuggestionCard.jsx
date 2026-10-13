import React from 'react';
import Button from '../ui/Button';

const DebugSuggestionCard = ({ error, suggestion, onApply }) => {
  return (
    <div className="bg-white dark:bg-gray-800 border border-red-200 dark:border-red-900/50 rounded-lg p-4 my-2 shadow-sm">
      <div className="flex items-center gap-2 mb-2 text-red-600 dark:text-red-400">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        <h4 className="font-semibold text-sm">Error Detected</h4>
      </div>
      <div className="bg-red-50 dark:bg-red-900/20 p-2 rounded text-xs font-mono text-red-800 dark:text-red-200 mb-3 overflow-x-auto">
        {error}
      </div>
      <h4 className="font-semibold text-sm text-green-600 dark:text-green-400 mb-2">Suggested Fix:</h4>
      <div className="bg-green-50 dark:bg-green-900/20 p-2 rounded text-xs font-mono text-green-800 dark:text-green-200 mb-3 overflow-x-auto whitespace-pre">
        {suggestion}
      </div>
      <div className="flex justify-end gap-2">
        <Button size="sm" variant="secondary" onClick={() => onApply(suggestion)}>Apply Fix</Button>
      </div>
    </div>
  );
};

export default DebugSuggestionCard;
