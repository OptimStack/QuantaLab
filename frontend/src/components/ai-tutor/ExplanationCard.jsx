import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

const ExplanationCard = ({ explanation, tags }) => {
  return (
    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 my-2 shadow-sm">
      <div className="prose dark:prose-invert max-w-none text-sm">
        <ReactMarkdown>{explanation}</ReactMarkdown>
      </div>
      {tags && tags.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {tags.map(tag => (
            <span key={tag} className="px-2 py-1 bg-quantum-100 dark:bg-quantum-900/30 text-quantum-800 dark:text-quantum-200 text-xs rounded-full">
              {tag}
            </span>
          ))}
        </div>
      )}
      <div className="mt-4 flex items-center justify-end gap-2 border-t dark:border-gray-700 pt-2">
        <span className="text-xs text-gray-500">Was this helpful?</span>
        <button className="text-gray-400 hover:text-green-500">👍</button>
        <button className="text-gray-400 hover:text-red-500">👎</button>
      </div>
    </div>
  );
};

export default ExplanationCard;
