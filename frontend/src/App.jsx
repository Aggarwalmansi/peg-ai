import React from 'react';
import Header from './components/Header';
import ChatBox from './components/ChatBox';
import './App.css';

function App() {
  return (
    <main className="app-container">
      <Header />
      <div className="main-content">
        <ChatBox />
      </div>
      
      {/* Background radial glow for luxury feel */}
      <div className="bg-glow"></div>
    </main>
  );
}

export default App;
