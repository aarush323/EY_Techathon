import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

function App() {
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/dashboard')
        if (!response.ok) {
          throw new Error('Report not ready yet')
        }
        const data = await response.json()
        setReport(data)
        setError(null)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchReport()
    const interval = setInterval(fetchReport, 10000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="container">
      <header>
        <h1>Automotive Maintenance Dashboard</h1>
        {report && <p className="timestamp">Last updated: {new Date(report.timestamp).toLocaleString()}</p>}
      </header>

      <main>
        {loading && !report && <div className="loading">Loading report...</div>}

        {error && !report && (
          <div className="error">
            <p>{error}</p>
            <p className="hint">Please run the AI agent to generate the report.</p>
          </div>
        )}

        {report && (
          <div className="report-content">
            <ReactMarkdown>{report.content}</ReactMarkdown>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
