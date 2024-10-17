import React, { useEffect, useState } from 'react';
import './Chatbox.css';
import Message from './Message'; // Import the Message component
import axios from 'axios';


function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await axios.get('http://localhost:3500/messages');
        setMessages(response.data);
      }
      catch (err) {
        console.log (err.response);
      }
    };

    fetchMessages();
  }, []);


  const sendRequest = async (input) => {
    try {
      const response = await axios.post('http://localhost:5000/generate', 
        { prompt: input } , // Ensure the key matches what the server expects
        { headers: { 'Content-Type': 'application/json' } }
      );      

      console.log (response.data.content);
      
      const newmsg = {text: input, sender: "user"};
      const resp = await axios.post('http://localhost:3500/messages', newmsg);
      console.log ("Error not in adding input");
      
      const msg2 = {text: response.data.content, sender: 'bot'};
      const resp2 = await axios.post('http://localhost:3500/messages', msg2);
      console.log ("Error not in adding bot op");
      
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          {text: response.data.content, sender: 'bot'}
        ]);
      }, 1000);
    }
    catch (err) {
      // Log the error message
      console.log(`Error message: ${err.message}`);
  
      // Log the Axios error response if it exists
      if (err.response) {
        console.log("error");
      }
    }
  }
  
  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user' }]);
      sendRequest(input);
      setInput('');
    }
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  const handleClear = async () => {
    const excludedId = "91f8";
    try {
      // Step 1: Get all messages.
      const response = await axios.get('http://localhost:3500/messages');
      const messages = response.data;
  
      // Step 2: Filter out the message with the excluded ID.
      const messagesToDelete = messages.filter(message => message.id !== excludedId);
  
      // Step 3: Loop through each message and delete them by ID.
      const deletePromises = messagesToDelete.map((message) =>
        axios.delete(`http://localhost:3500/messages/${message.id}`)
      );
  
      // Step 4: Wait for all delete requests to complete.
      await Promise.all(deletePromises);
      console.log(`All messages except ID ${excludedId} have been deleted successfully.`);
    } catch (error) {
      console.error('Error deleting messages:', error);
    }

    setMessages([{id: "91f8", text: "Hello, how can I help you?", sender: "bot"}]);
  };
  

  return (
    <div className="chat-box">
      <div className="messages">
        {messages.map((message, index) => (
          <Message 
            key={index} 
            text={message.text} 
            sender={message.sender} 
          />
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          className="chat-input"
        />
        <button onClick={handleSend} className="send-button" style={{ marginRight: '10px' }}>
          Send
        </button>
        <button onClick={handleClear} className="send-button">
          Clear history
        </button>
      </div>
    </div>
  );
}

export default ChatBox;
