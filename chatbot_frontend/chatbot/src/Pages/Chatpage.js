import React from 'react'
import Header from '../Components/Chatpage/Header'
import ChatBox from '../Components/Chatpage/Chatbox'
import "./Chatpage.css"

function Chatpage() {
  return (
    <div className="chat-page">
      <Header />
      <div className="chat-container">
        <ChatBox />
      </div>
    </div>  
  )
}

export default Chatpage
