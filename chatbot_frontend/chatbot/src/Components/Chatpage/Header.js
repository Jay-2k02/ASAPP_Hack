import React from 'react';
import { Link } from 'react-router-dom'; // If you're using React Router for navigation
import './Header.css'; // Import the CSS file for styling

function Header() {
  return (
    <header className="header">
      <div className="logo">
        <h1 className='logo-text'>ASAPP Chatbot</h1>
      </div>
      <nav className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/faq">FAQ</Link>
        <Link to="/contact">Contact</Link>
      </nav>
    </header>
  );
}

export default Header;
