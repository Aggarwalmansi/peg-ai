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
            background: isSafe ? 'rgba(74, 222, 128, 0.1)' : 'rgba(248, 113, 113, 0.1)',
            padding: '2px 8px',
            borderRadius: '4px',
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
                borderColor: isSafe ? 'var(--border)' : 'rgba(248, 113, 113, 0.4)',
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
    borderRadius: '12px',
    background: 'var(--bg-card)',
    border: '1px solid var(--border)',
    padding: '1.5rem',
    animation: 'fadeIn 0.5s ease-out',
    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.4)',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '1rem',
    marginBottom: '1.5rem',
  },
  item: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.4rem',
  },
  label: {
    fontSize: '0.7rem',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    color: 'var(--text-muted)',
    fontWeight: '700',
  },
  value: {
    fontSize: '1rem',
    color: 'var(--text-primary)',
    fontWeight: '500',
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
    padding: '0.3rem 0.7rem',
    background: 'var(--bg-input)',
    borderRadius: '6px',
    color: 'var(--text-secondary)',
    border: '1px solid var(--border)',
  },
  p: {
    fontSize: '0.9rem',
    color: 'var(--text-secondary)',
    marginTop: '0.4rem',
    lineHeight: '1.5',
  },
  baitSection: {
    marginTop: '1.5rem',
    padding: '1rem',
    background: 'rgba(244, 43, 3, 0.05)',
    borderRadius: '8px',
    border: '1px dashed var(--primary)',
  },
  baitHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '0.8rem',
  },
  copyBtn: {
    fontSize: '0.7rem',
    color: 'var(--primary)',
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  baitText: {
    fontSize: '0.9rem',
    fontStyle: 'italic',
    color: 'var(--text-primary)',
    lineHeight: '1.6',
  },
};

export default ActionPanel;
