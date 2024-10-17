import React from 'react';
import Header from './Header';
import './Content.css';
import Footer from './Footer';
import { useNavigate } from 'react-router-dom';

function Content() {
  const navigate = useNavigate();

  const handleStartChatting = () => {
    navigate('/chat');
  }

  return (
    <div className="home-page">
      <div className="animated-background"></div>
      <Header />
      <main className="main-content">
        <h2>Welcome to ASAPP Bot</h2>
        <p>
          Our intelligent chatbot is here to assist you with any queries you may have. Whether you're looking for 
          information or just need a quick chat, our bot has you covered.
        </p>
        <button className="dark-button" onClick={handleStartChatting}>Start Chatting</button>
      </main>
      <Footer />
    </div>
  );
}

export default Content;
