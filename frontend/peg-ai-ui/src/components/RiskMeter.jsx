import React, { useEffect, useState } from 'react';

const RiskMeter = ({ score }) => {
  const [displayScore, setDisplayScore] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDisplayScore(score);
    }, 100);
    return () => clearTimeout(timer);
  }, [score]);

  const getStatusColor = (s) => {
    if (s < 30) return 'var(--safe)';
    if (s < 70) return 'var(--secondary)';
    return 'var(--scam)';
  };

  const color = getStatusColor(displayScore);

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <span style={styles.label}>Risk Probability</span>
        <span style={{ ...styles.value, color }}>{displayScore}%</span>
      </div>
      <div style={styles.track}>
        <div 
          style={{ 
            ...styles.thumb, 
            width: `${displayScore}%`,
            background: color,
            boxShadow: `0 0 15px ${color}44`,
          }} 
        />
      </div>
    </div>
  );
};

const styles = {
  container: {
    margin: '1.5rem 0',
    width: '100%',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'baseline',
    marginBottom: '0.6rem',
  },
  label: {
    fontSize: '0.85rem',
    color: 'var(--text-secondary)',
    fontWeight: '500',
  },
  value: {
    fontSize: '1.25rem',
    fontWeight: '700',
    fontVariantNumeric: 'tabular-nums',
  },
  track: {
    height: '6px',
    background: 'var(--bg-input)',
    borderRadius: '10px',
    overflow: 'hidden',
    position: 'relative',
  },
  thumb: {
    height: '100%',
    borderRadius: '10px',
    transition: 'width 1s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.4s',
  },
};

export default RiskMeter;
