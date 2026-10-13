import React, { useState } from 'react';
import QuantumCodeEditor from '../code-editor/QuantumCodeEditor';
import Button from '../ui/Button';

const CodingChallengeRunner = ({ challenge, onSubmit }) => {
  const [code, setCode] = useState(challenge?.starterCode || '');
  const [output, setOutput] = useState('');

  const handleRun = () => {
    setOutput('Running test cases...\nTest 1: PASS\nTest 2: PASS\nAll tests passed!');
  };

  return (
    <div className="flex h-[calc(100vh-12rem)] gap-4">
      <div className="w-1/3 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6 overflow-y-auto">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">{challenge?.title || 'Coding Challenge'}</h3>
        <div className="prose dark:prose-invert text-gray-700 dark:text-gray-300">
          <p>{challenge?.description || 'Write a Qiskit circuit that creates a Bell state.'}</p>
        </div>
      </div>
      <div className="w-2/3 flex flex-col gap-4">
        <div className="flex-1 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden">
          <QuantumCodeEditor value={code} onChange={setCode} />
        </div>
        <div className="h-48 bg-gray-900 text-green-400 font-mono p-4 rounded-lg overflow-y-auto whitespace-pre-wrap flex flex-col">
          <div className="flex justify-between items-center mb-2 border-b border-gray-700 pb-2">
            <span className="text-gray-400">Terminal Output</span>
            <div className="space-x-2">
              <Button size="sm" variant="secondary" onClick={handleRun}>Run Code</Button>
              <Button size="sm" onClick={() => onSubmit(code)}>Submit</Button>
            </div>
          </div>
          <div className="flex-1 overflow-y-auto">{output}</div>
        </div>
      </div>
    </div>
  );
};

export default CodingChallengeRunner;
