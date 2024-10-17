import React from 'react';
import './SuggestionBubble.css'; // Create this CSS file for styling

function SuggestionBubble({ text, onClose, onClick }) {
  return (
    <div className="suggestion-bubble" onClick={onClick}>
      <span className="suggestion-text">{text}</span>
      <button className="close-button" onClick={(e) => {
        e.stopPropagation(); // Prevent the bubble's onClick from triggering
        onClose();
      }}>
        &times;
      </button>
    </div>
  );
}

export default SuggestionBubble;
