import React, { useState } from 'react';
import Card from '../ui/Card';
import Button from '../ui/Button';

const QuizRunner = ({ question, onAnswer }) => {
  const [selected, setSelected] = useState(null);

  return (
    <Card className="max-w-2xl mx-auto">
      <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-6">{question.text}</h3>
      <div className="space-y-3">
        {question.options.map((opt, idx) => (
          <label 
            key={idx} 
            className={`flex items-center p-4 border rounded-md cursor-pointer transition-colors ${selected === idx ? 'border-quantum-500 bg-quantum-50 dark:bg-quantum-900/20' : 'border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800'}`}
          >
            <input 
              type="radio" 
              name="quiz-option" 
              className="h-4 w-4 text-quantum-600 focus:ring-quantum-500 border-gray-300"
              checked={selected === idx}
              onChange={() => setSelected(idx)}
            />
            <span className="ml-3 text-gray-900 dark:text-gray-100">{opt}</span>
          </label>
        ))}
      </div>
      <div className="mt-6 flex justify-end">
        <Button onClick={() => onAnswer(selected)} disabled={selected === null}>Submit Answer</Button>
      </div>
    </Card>
  );
};

export default QuizRunner;
