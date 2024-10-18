import React, { useEffect, useState, useRef } from 'react';
import './Chatbox.css';
import Message from './Message'; // Import the Message component
import axios from 'axios';
import SuggestionBubble from './SuggestionBubble';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [uploadedFileName, setUploadedFileName] = useState(''); // State to hold the uploaded PDF file name
  const inputRef = useRef(null);

  // Debounce function to delay API calls for fetching suggestions
  const debounce = (func, delay) => {
    let timeoutId;
    return (...args) => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      timeoutId = setTimeout(() => {
        func(...args);
      }, delay);
    };
  };

  // Fetch suggestions function, wrapped with debounce
  const fetchSuggestions = async (query) => {
    if (query.trim()) {
      try {
        const response = await axios.post('http://localhost:4500/generate', {
          prompt: query,
        }, {
          headers: { 'Content-Type': 'application/json' },
        });
        setSuggestions(response.data.suggestions);
      } catch (err) {
        console.log(err.response);
      }
    } else {
      setSuggestions([]);
    }
  };

  const debouncedFetchSuggestions = useRef(debounce(fetchSuggestions, 300)).current;

  // Call debounced function when input changes
  useEffect(() => {
    debouncedFetchSuggestions(input);
  }, [input, debouncedFetchSuggestions]);

  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion);
    inputRef.current?.focus();
  };

  const handleSuggestionClose = (index) => {
    setSuggestions(suggestions.filter((_, i) => i !== index));
  };

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await axios.get('http://localhost:3500/messages');
        setMessages(response.data);
      } catch (err) {
        console.log(err.response);
      }
    };

    fetchMessages();
  }, []);

  const sendRequest = async (input) => {
    try {
      const response = await axios.post('http://localhost:4444/api/chat', 
        { prompt: input },
        { headers: { 'Content-Type': 'application/json' }}
      );      

      const newmsg = { text: input, sender: "user" };
      await axios.post('http://localhost:3500/messages', newmsg);
      
      const botResponse = { text: response.data.response, sender: 'bot' };
      await axios.post('http://localhost:3500/messages', botResponse);
      
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: response.data.response, sender: 'bot' }
      ]);
    } catch (err) {
      console.log(`Error message: ${err.message}`);
      if (err.response) {
        console.log("error");
      }
    }
  };
  
  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user' }]);
      sendRequest(input);
      setInput(''); // Clear the input after sending
      inputRef.current?.focus(); // Refocus the input after sending
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
      const response = await axios.get('http://localhost:3500/messages');
      const messages = response.data;
  
      const messagesToDelete = messages.filter(message => message.id !== excludedId);
      const deletePromises = messagesToDelete.map((message) =>
        axios.delete(`http://localhost:3500/messages/${message.id}`)
      );
  
      await Promise.all(deletePromises);
      console.log(`All messages except ID ${excludedId} have been deleted successfully.`);
    } catch (error) {
      console.error('Error deleting messages:', error);
    }

    setMessages([{ id: "91f8", text: "Hello, how can I help you?", sender: "bot" }]);
  };

  const handlePDFUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('pdf', file);
      setUploadedFileName(file.name); // Store the uploaded file name

      try {
        const response = await axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log(response.data);
      } catch (err) {
        console.error("Error uploading PDF:", err);
      }
    }
  };

  return (
    <div className="chat-box">
      <div className="suggestions-container">
        {suggestions.map((suggestion, index) => (
          <SuggestionBubble 
            key={index} 
            text={suggestion} 
            onClick={() => handleSuggestionClick(suggestion)}
            onClose={() => handleSuggestionClose(index)} 
          />
        ))}
      </div>

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
          ref={inputRef}
        />
        <button onClick={handleSend} className="send-button" style={{ marginRight: '10px' }}>
          Send
        </button>
        <button onClick={handleClear} className="send-button" >
          Clear history
        </button>
      </div>
    </div>
  );
}

export default ChatBox;
