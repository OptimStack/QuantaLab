import React, { useState } from 'react';
import ExplanationCard from './ExplanationCard';
import DebugSuggestionCard from './DebugSuggestionCard';

const TutorChatPanel = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', type: 'text', content: 'Hello! I am your AI Quantum Tutor. How can I help you with this circuit today?' }
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: 'user', content: input }]);
    setInput('');
    
    // Mock response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        type: 'explanation',
        content: 'This is a mock explanation of what you asked. The Hadamard gate creates a superposition.',
        tags: ['Hadamard', 'Superposition']
      }]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 dark:bg-gray-900">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'user' ? (
              <div className="bg-quantum-600 text-white rounded-lg py-2 px-4 max-w-[80%] text-sm shadow-sm">
                {msg.content}
              </div>
            ) : (
              <div className="max-w-[90%]">
                {msg.type === 'text' && (
                  <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white rounded-lg py-2 px-4 text-sm shadow-sm">
                    {msg.content}
                  </div>
                )}
                {msg.type === 'explanation' && (
                  <ExplanationCard explanation={msg.content} tags={msg.tags} />
                )}
                {msg.type === 'debug' && (
                  <DebugSuggestionCard error={msg.error} suggestion={msg.suggestion} onApply={() => {}} />
                )}
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="p-3 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-2">
          <input 
            type="text" 
            className="flex-1 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-1 focus:ring-quantum-500"
            placeholder="Ask AI Tutor..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button 
            onClick={handleSend}
            className="p-2 bg-quantum-600 text-white rounded-md hover:bg-quantum-700"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default TutorChatPanel;
