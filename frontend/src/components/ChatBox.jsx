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
  const textareaRef = useRef(null);

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

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  useEffect(() => {
    if (!textareaRef.current) return;
    textareaRef.current.style.height = '0px';
    const nextHeight = Math.min(textareaRef.current.scrollHeight, 160);
    textareaRef.current.style.height = `${nextHeight}px`;
  }, [input]);

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
          <textarea
            ref={textareaRef}
            style={styles.input}
            placeholder="Paste suspicious message here..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isAnalyzing}
            rows={1}
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
    minHeight: 0,
    maxWidth: '960px',
    width: '100%',
    margin: '0 auto',
    padding: '0 clamp(0.75rem, 2vw, 1.5rem)',
    position: 'relative',
  },
  chatArea: {
    flex: 1,
    overflowY: 'auto',
    minHeight: 0,
    padding: '1rem 0 0',
    overscrollBehavior: 'contain',
  },
  content: {
    width: '100%',
    maxWidth: '820px',
    margin: '0 auto',
    paddingBottom: '1.5rem',
  },
  inputArea: {
    position: 'sticky',
    bottom: 0,
    zIndex: 30,
    width: '100%',
    padding: '0.85rem 0 calc(0.9rem + env(safe-area-inset-bottom, 0px))',
    background: 'linear-gradient(to top, rgba(244, 241, 236, 0.96) 68%, rgba(244, 241, 236, 0.78) 86%, rgba(244, 241, 236, 0))',
    backdropFilter: 'blur(16px)',
  },
  inputWrapper: {
    display: 'flex',
    alignItems: 'flex-end',
    gap: '0.75rem',
    background: 'linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(243,248,249,0.88) 100%)',
    border: '1px solid var(--border-strong)',
    borderRadius: '26px',
    padding: '0.95rem 1rem',
    boxShadow: 'var(--shadow-card)',
    transition: 'border-color 0.2s, box-shadow 0.2s',
    maxWidth: '820px',
    margin: '0 auto',
  },
  input: {
    flex: 1,
    background: 'none',
    border: 'none',
    color: 'var(--text-primary)',
    fontSize: '0.98rem',
    padding: '0.25rem 0.2rem 0.35rem',
    outline: 'none',
    resize: 'none',
    minHeight: '28px',
    maxHeight: '160px',
    lineHeight: '1.5',
    overflowY: 'auto',
    fontFamily: 'inherit',
  },
  sendBtn: {
    color: 'var(--primary)',
    minWidth: '44px',
    minHeight: '44px',
    borderRadius: '999px',
    background: 'linear-gradient(135deg, rgba(111, 142, 149, 0.16), rgba(148, 180, 187, 0.28))',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'transform 0.2s, opacity 0.2s, box-shadow 0.2s',
    flexShrink: 0,
    boxShadow: '0 10px 24px rgba(111, 142, 149, 0.18)',
  },
  disclaimer: {
    fontSize: '0.72rem',
    color: 'var(--text-muted)',
    textAlign: 'center',
    marginTop: '0.7rem',
    padding: '0 0.5rem',
    letterSpacing: '0.02em',
  },
};

export default ChatBox;
