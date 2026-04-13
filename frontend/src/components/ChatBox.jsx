import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import { analyzeMessage } from '../services/api';

const ChatBox = () => {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      type: 'ai',
      text: 'Hello, I am PEG. Share any message (SMS, Email, or Web link) to analyze for security risks.',
      analysis: null,
      loading: false
    }
  ]);
  const [input, setInput] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isAnalyzing) return;

    const userMessage = { 
      id: Date.now(), 
      type: 'user', 
      text: input 
    };

    const aiResponse = { 
      id: Date.now() + 1, 
      type: 'ai', 
      loading: true 
    };

    setMessages(prev => [...prev, userMessage, aiResponse]);
    setInput('');
    setIsAnalyzing(true);

    try {
      const result = await analyzeMessage(input);
      setMessages(prev => 
        prev.map(msg => 
          msg.id === aiResponse.id 
            ? { ...msg, analysis: result, loading: false } 
            : msg
        )
      );
    } catch (error) {
      setMessages(prev => 
        prev.map(msg => 
          msg.id === aiResponse.id 
            ? { ...msg, loading: false, text: "Error: Could not connect to PEG analysis engine." } 
            : msg
        )
      );
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.chatArea} ref={scrollRef}>
        <div style={styles.content}>
          {messages.map((msg) => (
            <MessageBubble 
              key={msg.id} 
              message={msg.text} 
              type={msg.type} 
              analysis={msg.analysis}
              loading={msg.loading}
            />
          ))}
        </div>
      </div>
      
      <div style={styles.inputArea}>
        <div style={styles.inputWrapper}>
          <input 
            style={styles.input}
            placeholder="Paste suspicious message here..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            disabled={isAnalyzing}
          />
          <button 
            onClick={handleSend} 
            disabled={!input.trim() || isAnalyzing}
            style={{ 
              ...styles.sendBtn, 
              opacity: (!input.trim() || isAnalyzing) ? 0.3 : 1 
            }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
        <p style={styles.disclaimer}>
          PEG uses advanced AI to analyze patterns. Always exercise caution.
        </p>
      </div>
    </div>
  );
};

const styles = {
  container: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    maxWidth: '800px',
    width: '100%',
    margin: '0 auto',
    padding: '0 1rem',
    position: 'relative',
    height: 'calc(100vh - 80px)',
  },
  chatArea: {
    flex: 1,
    overflowY: 'auto',
    padding: '1rem 0',
    scrollbarWidth: 'none',
    msOverflowStyle: 'none',
  },
  content: {
    paddingBottom: '2rem',
  },
  inputArea: {
    padding: '1.5rem 0 2.5rem',
    background: 'linear-gradient(to top, var(--bg-dark) 60%, transparent)',
  },
  inputWrapper: {
    display: 'flex',
    alignItems: 'center',
    background: 'var(--bg-input)',
    border: '1px solid var(--border)',
    borderRadius: '16px',
    padding: '0.6rem 0.8rem',
    boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
    transition: 'border-color 0.2s',
  },
  input: {
    flex: 1,
    background: 'none',
    border: 'none',
    color: 'var(--text-primary)',
    fontSize: '0.95rem',
    padding: '0.6rem',
    outline: 'none',
  },
  sendBtn: {
    color: 'var(--primary)',
    padding: '0.5rem',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'transform 0.2s, opacity 0.2s',
  },
  disclaimer: {
    fontSize: '0.7rem',
    color: 'var(--text-muted)',
    textAlign: 'center',
    marginTop: '0.8rem',
  },
};

export default ChatBox;
