import React from 'react';
import ReasoningPipeline from './ReasoningPipeline';

const ActionPanel = ({ analysis }) => {
  if (!analysis) return null;

  const { decision, action, bait_reply, signals, recommendation, trace } = analysis;
  const isSafe = decision?.toLowerCase() === 'safe';

  return (
    <div style={styles.container}>
      <div style={styles.grid}>
        <div style={styles.item}>
          <span style={styles.label}>Decision</span>
          <span style={{ 
            ...styles.value, 
            color: isSafe ? 'var(--safe)' : 'var(--scam)',
            background: isSafe ? 'rgba(78, 138, 113, 0.12)' : 'rgba(179, 108, 103, 0.12)',
            padding: '0.4rem 0.8rem',
            borderRadius: '999px',
            fontSize: '0.8rem',
            textTransform: 'uppercase',
            fontWeight: '800'
          }}>
            {decision}
          </span>
        </div>
        <div style={styles.item}>
          <span style={styles.label}>Action</span>
          <span style={styles.value}>{action}</span>
        </div>
      </div>

      {signals && signals.length > 0 && (
        <div style={styles.section}>
          <span style={styles.label}>Detected Signals</span>
          <div style={styles.tagCloud}>
            {signals.map((sig, i) => (
              <span key={i} style={{
                ...styles.tag,
                borderColor: isSafe ? 'var(--border)' : 'rgba(179, 108, 103, 0.35)',
                color: isSafe ? 'var(--text-secondary)' : 'var(--scam)'
              }}>{sig}</span>
            ))}
          </div>
        </div>
      )}

      {recommendation && (
        <div style={styles.section}>
          <span style={styles.label}>Expert Recommendation</span>
          <p style={styles.p}>{recommendation}</p>
        </div>
      )}

      {bait_reply && (
        <div style={styles.baitSection}>
          <div style={styles.baitHeader}>
            <span style={styles.label}>Generated Bait Reply</span>
            <button 
              onClick={() => navigator.clipboard.writeText(bait_reply)}
              style={styles.copyBtn}
            >
              Copy
            </button>
          </div>
          <p style={styles.baitText}>{bait_reply}</p>
        </div>
      )}

      <ReasoningPipeline trace={trace} isScam={!isSafe} />
    </div>
  );
};

const styles = {
  container: {
    marginTop: '1.5rem',
    borderRadius: '28px',
    background: 'linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(244,248,249,0.88) 100%)',
    border: '1px solid var(--border)',
    padding: '1.6rem',
    animation: 'fadeIn 0.5s ease-out',
    boxShadow: 'var(--shadow-card)',
    backdropFilter: 'blur(18px)',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
    gap: '1rem',
    marginBottom: '1.5rem',
  },
  item: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.4rem',
    padding: '0.95rem 1rem',
    background: 'rgba(255,255,255,0.52)',
    borderRadius: '18px',
    border: '1px solid rgba(111, 142, 149, 0.08)',
  },
  label: {
    fontSize: '0.7rem',
    textTransform: 'uppercase',
    letterSpacing: '0.14em',
    color: 'var(--text-muted)',
    fontWeight: '700',
  },
  value: {
    fontSize: '1rem',
    color: 'var(--text-primary)',
    fontWeight: '600',
  },
  section: {
    marginTop: '1.2rem',
  },
  tagCloud: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.5rem',
    marginTop: '0.5rem',
  },
  tag: {
    fontSize: '0.75rem',
    padding: '0.45rem 0.8rem',
    background: 'rgba(255,255,255,0.7)',
    borderRadius: '999px',
    color: 'var(--text-secondary)',
    border: '1px solid var(--border)',
  },
  p: {
    fontSize: '0.9rem',
    color: 'var(--text-secondary)',
    marginTop: '0.4rem',
    lineHeight: '1.65',
  },
  baitSection: {
    marginTop: '1.5rem',
    padding: '1.1rem 1.15rem',
    background: 'linear-gradient(180deg, rgba(214,228,231,0.48), rgba(255,255,255,0.68))',
    borderRadius: '20px',
    border: '1px solid rgba(111, 142, 149, 0.18)',
  },
  baitHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: '0.75rem',
    flexWrap: 'wrap',
    marginBottom: '0.8rem',
  },
  copyBtn: {
    fontSize: '0.7rem',
    color: 'var(--primary)',
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: '0.12em',
  },
  baitText: {
    fontSize: '0.95rem',
    fontStyle: 'italic',
    color: 'var(--text-primary)',
    lineHeight: '1.7',
  },
};

export default ActionPanel;
