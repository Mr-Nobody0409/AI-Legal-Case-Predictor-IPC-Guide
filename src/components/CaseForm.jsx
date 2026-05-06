import { useState } from 'react'
import styles from './CaseForm.module.css'

const EXAMPLE_CASES = [
  "The accused broke into a residential house at night and stole gold jewellery worth ₹2 lakhs. The owner confronted him and was severely beaten, sustaining grievous injuries.",
  "A company director collected ₹50 lakhs from investors promising 40% returns on a real estate project that never existed. He transferred the funds to personal accounts.",
  "The accused sent threatening messages to his ex-partner online, demanding she return or he would harm her family. He also created fake profiles to defame her on social media.",
]

export default function CaseForm({ onSubmit, isLoading }) {
  const [name, setName] = useState('')
  const [caseText, setCaseText] = useState('')
  const [charCount, setCharCount] = useState(0)
  const [error, setError] = useState('')

  function handleCaseChange(e) {
    setCaseText(e.target.value)
    setCharCount(e.target.value.length)
    if (error) setError('')
  }

  function handleExampleClick(example) {
    setCaseText(example)
    setCharCount(example.length)
    setError('')
  }

  function handleSubmit(e) {
    e.preventDefault()
    if (!name.trim()) { setError('Please enter your name.'); return }
    if (caseText.trim().length < 20) { setError('Please describe the case in more detail (at least 20 characters).'); return }
    onSubmit(name.trim(), caseText.trim())
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit} noValidate>
      <div className={styles.header}>
        <h2 className={styles.formTitle}>Case Analysis Request</h2>
        <p className={styles.formSubtitle}>
          Describe the facts of the case. Our AI will identify applicable IPC sections and provide legal reasoning.
        </p>
      </div>

      <div className={styles.field}>
        <label className={styles.label} htmlFor="name">
          Your Name <span className={styles.required}>*</span>
        </label>
        <input
          id="name"
          type="text"
          className={styles.input}
          placeholder="e.g., Arjun Sharma"
          value={name}
          onChange={e => setName(e.target.value)}
          disabled={isLoading}
          autoComplete="name"
        />
      </div>

      <div className={styles.field}>
        <label className={styles.label} htmlFor="case">
          Case Description <span className={styles.required}>*</span>
        </label>
        <textarea
          id="case"
          className={styles.textarea}
          placeholder="Describe the incident in detail — who was involved, what happened, where, and any relevant context..."
          value={caseText}
          onChange={handleCaseChange}
          disabled={isLoading}
          rows={7}
        />
        <div className={styles.textareaFooter}>
          <span className={styles.charCount}>{charCount} characters</span>
          <span className={styles.minHint}>{charCount < 20 ? `${20 - charCount} more needed` : '✓ Ready'}</span>
        </div>
      </div>

      <div className={styles.examplesSection}>
        <span className={styles.examplesLabel}>Try an example:</span>
        <div className={styles.examples}>
          {EXAMPLE_CASES.map((ex, i) => (
            <button
              key={i}
              type="button"
              className={styles.exampleBtn}
              onClick={() => handleExampleClick(ex)}
              disabled={isLoading}
            >
              Example {i + 1}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className={styles.error}>
          <span>⚠</span> {error}
        </div>
      )}

      <button type="submit" className={styles.submitBtn} disabled={isLoading}>
        {isLoading ? (
          <>
            <span className={styles.spinner} />
            Analysing Case…
          </>
        ) : (
          <>
            <span className={styles.submitIcon}>⚖</span>
            Analyse Case
          </>
        )}
      </button>
    </form>
  )
}
