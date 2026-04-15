import React, { useState, useEffect } from 'react';
import RiskMeter from './RiskMeter';
import ActionPanel from './ActionPanel';

const loadingTexts = [
  "Initializing Guardian Engine...",
  "Running Indian Intelligence...",
  "Cross-referencing Semantic DB...",
  "Invoking External MCP Tools...",
  "Compiling Final Decision..."
];

const MessageBubble = ({ message, type, analysis, loading }) => {
  const isUser = type === 'user';
  const isScam = analysis && analysis.decision?.toLowerCase() !== 'safe';
  
  const [loadingTextIdx, setLoadingTextIdx] = useState(0);

  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(() => {
        setLoadingTextIdx(prev => (prev + 1) % loadingTexts.length);
      }, 800);
    } else {
      setLoadingTextIdx(0);
    }
    return () => clearInterval(interval);
  }, [loading]);

  return (
    <div style={{ 
      ...styles.wrapper, 
      justifyContent: isUser ? 'flex-end' : 'flex-start',
      animation: 'fadeIn 0.3s ease-out',
    }}>
      <div style={{ 
        ...styles.bubble, 
        background: isUser ? 'var(--bg-input)' : 'transparent',
        border: isUser ? '1px solid var(--border)' : 'none',
        padding: isUser ? '0.8rem 1.2rem' : '0',
        borderRadius: isUser ? '18px 18px 4px 18px' : '0',
        maxWidth: isUser ? '80%' : '100%',
      }}>
        {isUser ? (
          <p style={styles.text}>{message}</p>
        ) : (
          <div style={styles.aiContent}>
            <div style={styles.aiHeader}>
              <div style={{ 
                ...styles.pulse, 
                backgroundColor: loading ? 'var(--secondary)' : (isScam ? 'var(--scam)' : 'var(--safe)')
              }} />
              <span style={styles.aiLabel}>
                {loading ? 'PEG Analysis Pipeline Active' : 'PEG Security Analysis'}
              </span>
            </div>
            
            {loading && (
              <div style={styles.skeleton}>
                <div style={styles.loadingTextContainer}>
                  <span style={styles.loadingTextActive}>{loadingTexts[loadingTextIdx]}</span>
                </div>
                <div style={styles.loadingBar}></div>
                <div style={{...styles.loadingBar, width: '60%', animationDelay: '0.2s'}}></div>
                <div style={{...styles.loadingBar, width: '80%', animationDelay: '0.4s'}}></div>
              </div>
            )}

            {!loading && analysis && (
              <>
                <RiskMeter score={analysis.risk_score} />
                <ActionPanel analysis={analysis} />
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  wrapper: {
    display: 'flex',
    margin: '1.5rem 0',
    width: '100%',
  },
  bubble: {
    transition: 'all 0.3s ease',
  },
  text: {
    fontSize: '0.95rem',
    color: 'var(--text-primary)',
    lineHeight: '1.5',
  },
  aiContent: {
    width: '100%',
  },
  aiHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.6rem',
    marginBottom: '0.8rem',
  },
  aiLabel: {
    fontSize: '0.8rem',
    fontWeight: '700',
    color: 'var(--text-secondary)',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  },
  pulse: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    animation: 'pulse 2s infinite',
  },
  skeleton: {
    marginTop: '1rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.8rem',
  },
  loadingTextContainer: {
    marginBottom: '0.5rem',
  },
  loadingTextActive: {
    fontSize: '0.85rem',
    color: 'var(--primary)',
    fontWeight: '600',
    fontStyle: 'italic',
    animation: 'pulse 1s infinite',
  },
  loadingBar: {
    height: '14px',
    background: 'var(--bg-input)',
    borderRadius: '4px',
    width: '100%',
    animation: 'pulse 1.5s infinite',
  },
};

export default MessageBubble;
