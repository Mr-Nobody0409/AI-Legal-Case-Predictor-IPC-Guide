import { useState, useEffect, useRef } from 'react'
import Header from './components/Header'
import CaseForm from './components/CaseForm'
import ResultCard from './components/ResultCard'
import LoadingOverlay from './components/LoadingOverlay'
import { analyzeCase, healthCheck } from './api/legalApi'
import styles from './App.module.css'

export default function App() {
  const [phase, setPhase] = useState('form') // 'form' | 'loading' | 'result' | 'error'
  const [result, setResult] = useState(null)
  const [errorMsg, setErrorMsg] = useState('')
  const [loadingStep, setLoadingStep] = useState(0)
  const [backendStatus, setBackendStatus] = useState('checking') // 'checking' | 'ok' | 'down'
  const stepRef = useRef(null)

  // ── Health-check backend on mount ─────────────────────────────────────────
  useEffect(() => {
    healthCheck()
      .then(() => setBackendStatus('ok'))
      .catch(() => setBackendStatus('down'))
  }, [])

  // ── Rotate loading messages every 3s ─────────────────────────────────────
  useEffect(() => {
    if (phase !== 'loading') return
    stepRef.current = setInterval(() => {
      setLoadingStep(s => s + 1)
    }, 3000)
    return () => clearInterval(stepRef.current)
  }, [phase])

  // ── Submit handler ────────────────────────────────────────────────────────
  async function handleSubmit(name, caseDescription) {
    setPhase('loading')
    setLoadingStep(0)
    setErrorMsg('')
    setResult(null)

    try {
      const data = await analyzeCase(name, caseDescription)
      setResult(data)
      setPhase('result')
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        err.message ||
        'An unexpected error occurred. Please try again.'
      setErrorMsg(msg)
      setPhase('error')
    }
  }

  function handleReset() {
    setPhase('form')
    setResult(null)
    setErrorMsg('')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className={styles.app}>
      <Header />

      <main className={styles.main}>
        {/* ── Backend status banner ── */}
        {backendStatus === 'down' && (
          <div className={styles.statusBanner}>
            <span>⚠</span>
            <span>Cannot reach the backend at <code>localhost:8000</code>. Make sure the FastAPI server is running.</span>
          </div>
        )}

        {/* ── Hero tagline ── */}
        {phase === 'form' && (
          <div className={styles.hero}>
            <h2 className={styles.heroTitle}>
              AI-Powered<br />
              <em>Legal Intelligence</em>
            </h2>
            <p className={styles.heroDesc}>
              Describe your case in plain language. Our system retrieves relevant IPC sections
              via semantic search and generates structured legal reasoning using a large language model.
            </p>
          </div>
        )}

        {/* ── Main content area ── */}
        <div className={styles.contentArea}>
          {phase === 'form' && (
            <CaseForm
              onSubmit={handleSubmit}
              isLoading={false}
            />
          )}

          {phase === 'loading' && (
            <LoadingOverlay step={loadingStep} />
          )}

          {phase === 'result' && result && (
            <ResultCard result={result} onReset={handleReset} />
          )}

          {phase === 'error' && (
            <div className={styles.errorCard}>
              <div className={styles.errorIcon}>⚠</div>
              <h3 className={styles.errorTitle}>Analysis Failed</h3>
              <p className={styles.errorMsg}>{errorMsg}</p>
              <button className={styles.retryBtn} onClick={handleReset}>
                ← Try Again
              </button>
            </div>
          )}
        </div>
      </main>

      <footer className={styles.footer}>
        <p>AI Legal Case Predictor </p>
        <p className={styles.footerSub}>For informational purposes only — not legal advice</p>
      </footer>
    </div>
  )
}
