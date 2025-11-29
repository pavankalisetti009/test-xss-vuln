import React from 'react';

function AnotherVulnerableComponent({ userInput }) {
  // Vulnerability: Using dangerouslySetInnerHTML with user-controlled input
  // This allows an attacker to inject arbitrary scripts if userInput contains malicious HTML/JS.
  return (
    <div className="vulnerable-container">
      <h4>Another Vulnerable Area (dangerouslySetInnerHTML)</h4>
      <div dangerouslySetInnerHTML={{ __html: userInput }} />
    </div>
  );
}

export default AnotherVulnerableComponent;
