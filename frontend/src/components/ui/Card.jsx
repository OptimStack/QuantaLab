import React from 'react';

const Card = ({ children, header, className = '' }) => {
  return (
    <div className={`bg-white dark:bg-gray-900 rounded-lg shadow-md overflow-hidden ${className}`}>
      {header && (
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-800">
          {header}
        </div>
      )}
      <div className="p-6">
        {children}
      </div>
    </div>
  );
};

export default Card;
