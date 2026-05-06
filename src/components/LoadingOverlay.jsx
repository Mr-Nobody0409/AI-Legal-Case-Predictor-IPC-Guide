import styles from './LoadingOverlay.module.css'

const MESSAGES = [
  'Retrieving relevant IPC sections…',
  'Parsing case semantics…',
  'Running RAG pipeline…',
  'Consulting LLaMA3 legal model…',
  'Structuring legal reasoning…',
]

export default function LoadingOverlay({ step = 0 }) {
  const msg = MESSAGES[step % MESSAGES.length]

  return (
    <div className={styles.overlay}>
      <div className={styles.inner}>
        <div className={styles.scales}>
          <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="40" cy="40" r="38" stroke="currentColor" strokeWidth="1" strokeOpacity="0.2" />
            <path d="M40 12 L40 68" stroke="currentColor" strokeWidth="1.5" />
            <path d="M20 24 L60 24" stroke="currentColor" strokeWidth="1.5" />
            {/* Left pan */}
            <path d="M20 24 L12 46 Q16 50 20 46 Q24 42 28 46 Q32 50 36 46 L28 24" stroke="currentColor" strokeWidth="1.5" fill="none" className={styles.leftPan} />
            {/* Right pan */}
            <path d="M60 24 L52 24 L44 46 Q48 50 52 46 Q56 42 60 46 Q64 50 68 46 L60 24" stroke="currentColor" strokeWidth="1.5" fill="none" className={styles.rightPan} />
            <circle cx="40" cy="18" r="3" fill="currentColor" />
            <path d="M32 68 L48 68" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </div>
        <h3 className={styles.title}>Analysing Your Case</h3>
        <p className={styles.message}>{msg}</p>
        <div className={styles.bar}>
          <div className={styles.barFill} />
        </div>
        <p className={styles.hint}>This may take 10–30 seconds</p>
      </div>
    </div>
  )
}
