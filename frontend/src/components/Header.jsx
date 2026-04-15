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
    borderBottom: '1px solid var(--border)',
    background: 'rgba(10, 10, 10, 0.8)',
    backdropFilter: 'blur(10px)',
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  logo: {
    fontSize: 'clamp(1.2rem, 2vw, 1.5rem)',
    fontWeight: '800',
    letterSpacing: '-0.02em',
    color: 'var(--text-primary)',
  },
  gradientText: {
    background: 'var(--gradient)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },
  badge: {
    fontSize: 'clamp(0.62rem, 1.5vw, 0.7rem)',
    fontWeight: '600',
    letterSpacing: '0.1em',
    padding: '0.4rem 0.8rem',
    borderRadius: '100px',
    border: '1px solid var(--border)',
    color: 'var(--text-secondary)',
    textTransform: 'uppercase',
  }
};

export default Header;
