import React, { useState } from 'react';
import VulnerableComponent from './VulnerableComponent';
import PickleVulnerability from './PickleVulnerability';
import YamlVulnerability from './YamlVulnerability';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('xss');
  const [userInput, setUserInput] = useState('');

  const handleChange = (event) => {
    setUserInput(event.target.value);
  };

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'xss':
        return (
          <div className="card">
            <h2>Live HTML Preview (XSS)</h2>
            <p>Enter HTML content in the box below to see it rendered live. Try an XSS payload like <code>&lt;img src=x onerror=alert('XSS')&gt;</code>.</p>
            <textarea
              value={userInput}
              onChange={handleChange}
              placeholder="Enter HTML here..."
              style={{ width: '95%', height: '100px', padding: '10px', marginBottom: '10px' }}
            />
            <div className="output-area">
              <h3>Rendered Output:</h3>
              <VulnerableComponent htmlContent={userInput} />
            </div>
          </div>
        );
      case 'pickle':
        return <PickleVulnerability />;
      case 'yaml':
        return <YamlVulnerability />;
      default:
        return null;
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Vulnerability Showcase</h1>
        <nav>
          <button onClick={() => setActiveTab('xss')} className={activeTab === 'xss' ? 'active' : ''}>XSS</button>
          <button onClick={() => setActiveTab('pickle')} className={activeTab === 'pickle' ? 'active' : ''}>Insecure Deserialization (Pickle)</button>
          <button onClick={() => setActiveTab('yaml')} className={activeTab === 'yaml' ? 'active' : ''}>Insecure Deserialization (YAML)</button>
        </nav>
        {renderActiveTab()}
      </header>
    </div>
  );
}

export default App;
