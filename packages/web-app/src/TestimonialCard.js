import React from 'react';

function TestimonialCard({ author, message }) {
  return (
    <div className="card testimonial-card">
      <div className="testimonial-author">{author}</div>
      <div
        className="testimonial-body"
        dangerouslySetInnerHTML={{ __html: message }}
      />
    </div>
  );
}

export default TestimonialCard;
