import React from 'react';

const Header = () => {
  return (
    <header style={styles.header}>
      <h1 style={styles.logo}>
        PEG <span style={styles.gradientText}>AI</span>
      </h1>
      <div style={styles.badge}>PREMIUM PROTECTION</div>
    </header>
  );
};

const styles = {
  header: {
    padding: '1.1rem clamp(1rem, 3vw, 2rem)',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: '0.8rem',
    flexWrap: 'wrap',
    borderBottom: '1px solid rgba(111, 142, 149, 0.14)',
    background: 'rgba(244, 248, 248, 0.68)',
    backdropFilter: 'blur(18px)',
    boxShadow: '0 8px 30px rgba(124, 146, 152, 0.08)',
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  logo: {
    fontSize: 'clamp(1.2rem, 2vw, 1.5rem)',
    fontWeight: '700',
    letterSpacing: '0.04em',
    color: 'var(--text-primary)',
    fontFamily: 'var(--display)',
    textTransform: 'uppercase',
  },
  gradientText: {
    background: 'linear-gradient(135deg, #6f8e95 0%, #9fb8be 48%, #cfdfe2 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },
  badge: {
    fontSize: 'clamp(0.62rem, 1.5vw, 0.7rem)',
    fontWeight: '600',
    letterSpacing: '0.1em',
    padding: '0.4rem 0.8rem',
    borderRadius: '100px',
    border: '1px solid var(--border-strong)',
    color: 'var(--text-secondary)',
    textTransform: 'uppercase',
    background: 'rgba(255,255,255,0.5)',
    boxShadow: '0 8px 20px rgba(111, 142, 149, 0.1)',
  }
};

export default Header;
