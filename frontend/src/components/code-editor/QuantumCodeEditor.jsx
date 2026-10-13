import React from 'react';
import Editor from '@monaco-editor/react';

const QuantumCodeEditor = ({ value, onChange, readOnly = false }) => {
  return (
    <Editor
      height="100%"
      defaultLanguage="python"
      theme="vs-dark"
      value={value}
      onChange={onChange}
      options={{
        readOnly,
        minimap: { enabled: false },
        fontSize: 14,
        wordWrap: 'on',
        lineNumbers: 'on',
        scrollBeyondLastLine: false,
      }}
    />
  );
};

export default QuantumCodeEditor;
