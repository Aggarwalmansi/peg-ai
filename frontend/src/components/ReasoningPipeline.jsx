import React, { useState } from 'react';

const ReasoningPipeline = ({ trace, isScam }) => {
  const [isOpen, setIsOpen] = useState(isScam);

  if (!trace || trace.length === 0) return null;

  const parseTrace = (line) => {
    // Basic parsing to make the trace look premium
    const match = line.match(/^\[(.*?)\] (.*)$/);
    if (match) {
      return { layer: match[1], content: match[2], isTool: false };
    }
    if (line.toLowerCase().includes('tool') || line.toLowerCase().includes('url')) {
      return { layer: 'External Tool', content: line, isTool: true };
    }
    return { layer: 'System', content: line, isTool: false };
  };

  const parsedTraces = trace.map(parseTrace);

  return (
    <div style={styles.container}>
      <button style={styles.toggleBtn} onClick={() => setIsOpen(!isOpen)}>
        <span style={styles.toggleText}>
          {isOpen ? '▼ Hide' : '▶ Show'} AI Reasoning Breakdown
        </span>
      </button>

      {isOpen && (
        <div style={styles.pipeline}>
          {parsedTraces.map((t, i) => (
            <div key={i} style={styles.node}>
              <div style={styles.iconWrapper}>
                <div style={{...styles.iconNode, background: t.isTool ? 'var(--primary)' : 'var(--border)'}}></div>
                {i < parsedTraces.length - 1 && <div style={styles.line}></div>}
              </div>
              <div style={styles.nodeContent}>
                <span style={{
                  ...styles.layerLabel,
                  color: t.isTool ? 'var(--primary)' : 'var(--text-secondary)'
                }}>
                  {t.layer}
                </span>
                <span style={styles.layerInfo}>{t.content}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    marginTop: '1.5rem',
    background: 'rgba(255, 255, 255, 0.56)',
    borderRadius: '20px',
    border: '1px solid var(--border)',
    overflow: 'hidden',
  },
  toggleBtn: {
    width: '100%',
    textAlign: 'left',
    padding: '1rem 1.1rem',
    background: 'transparent',
    border: 'none',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    transition: 'background 0.2s',
  },
  toggleText: {
    fontSize: '0.75rem',
    fontWeight: '700',
    color: 'var(--text-secondary)',
    textTransform: 'uppercase',
    letterSpacing: '0.14em',
  },
  pipeline: {
    padding: '1rem 1.1rem',
    borderTop: '1px solid var(--border)',
  },
  node: {
    display: 'flex',
    gap: '1rem',
    minHeight: '40px',
  },
  iconWrapper: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '12px',
  },
  iconNode: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    marginTop: '6px',
    zIndex: 2,
  },
  line: {
    flex: 1,
    width: '2px',
    background: 'rgba(111, 142, 149, 0.16)',
    margin: '4px 0',
  },
  nodeContent: {
    display: 'flex',
    flexDirection: 'column',
    paddingBottom: '1rem',
  },
  layerLabel: {
    fontSize: '0.7rem',
    fontWeight: '800',
    textTransform: 'uppercase',
    letterSpacing: '0.13em',
  },
  layerInfo: {
    fontSize: '0.85rem',
    color: 'var(--text-primary)',
    fontFamily: 'var(--sans)',
    marginTop: '0.25rem',
    lineHeight: '1.55',
  }
};

export default ReasoningPipeline;
