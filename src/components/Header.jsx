import styles from './Header.module.css'

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        <div className={styles.emblem}>
          <svg viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="30" cy="30" r="28" stroke="currentColor" strokeWidth="1.5" />
            <path d="M30 10 L30 50" stroke="currentColor" strokeWidth="1.5" />
            <path d="M16 20 L44 20" stroke="currentColor" strokeWidth="1" strokeOpacity="0.6" />
            <path d="M16 20 L10 38 Q13 40 16 38 Q19 36 22 38 Q25 40 28 38" stroke="currentColor" strokeWidth="1.5" fill="none" />
            <path d="M44 20 L50 38 Q47 40 44 38 Q41 36 38 38 Q35 40 32 38" stroke="currentColor" strokeWidth="1.5" fill="none" />
            <circle cx="30" cy="14" r="2" fill="currentColor" />
            <path d="M26 50 L34 50" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          </svg>
        </div>
        <div className={styles.titleGroup}>
          <h1 className={styles.title}>AI Legal Case Predictor</h1>
          <p className={styles.subtitle}>IPC Guidance · Legal Tech AI Platform </p>
        </div>
      </div>
      <div className={styles.rule} />
    </header>
  )
}
