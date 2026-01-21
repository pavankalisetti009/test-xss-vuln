import React, { useEffect, useRef } from 'react';

function VulnerableComponent({ htmlContent }) {
  const divRef = useRef(null);

  useEffect(() => {
    if (divRef.current) {
      divRef.current.innerHTML = htmlContent;
    }
  }, [htmlContent]);

  return <div ref={divRef} />;
}

export default VulnerableComponent;