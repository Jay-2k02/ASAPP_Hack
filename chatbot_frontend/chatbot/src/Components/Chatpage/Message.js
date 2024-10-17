import React from 'react';
import './Message.css'; // Import the CSS for Message styles

const Message = ({ text, sender }) => {
  return (
    <div className={`message ${sender}`}>
      {text}
    </div>
  );
};

export default Message;
