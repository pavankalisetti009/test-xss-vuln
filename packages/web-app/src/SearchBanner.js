import React from 'react';

function SearchBanner() {
  const params = new URLSearchParams(window.location.search);
  const query = params.get('q') || '';

  const highlight = `Results for <strong>${query}</strong>`;

  return (
    <div className="search-banner">
      <div
        className="search-banner-text"
        dangerouslySetInnerHTML={{ __html: highlight }}
      />
    </div>
  );
}

export default SearchBanner;
