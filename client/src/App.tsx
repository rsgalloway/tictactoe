import React, { useEffect, useState } from 'react'

const API_URL = (import.meta.env.API_URL as string) || 'http://localhost:8000'

type Status = 'playing' | 'x_won' | 'o_won' | 'draw'

export default function App() {
  const [board, setBoard] = useState<string>('.........')
  const [status, setStatus] = useState<Status>('playing')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    fetch(`${API_URL}/api/new`, { method: 'POST' }).then(r => r.json()).then(d => {
      setBoard(d.board)
      setStatus('playing')
    })
  }, [])

  return (
    <main style={{ display: 'grid', placeItems: 'center', minHeight: '100vh', gap: 16 }}>
      <h1>AI Tic-Tac-Toe</h1>
      <div role="grid" aria-label="Tic Tac Toe board" style={{
        display: 'grid', gridTemplateColumns: 'repeat(3, 80px)', gap: 6
      }}>
        {Array.from(board).map((ch, i) => (
          <button
            key={i}
            role="gridcell"
            aria-label={`cell ${i}`}
            disabled={busy || ch !== '.' || status !== 'playing'}
            style={{ width: 80, height: 80, fontSize: 40 }}>
            {ch === '.' ? '' : ch}
          </button>
        ))}
      </div>
      <p aria-live="polite">
        {status === 'playing' ? (busy ? 'Thinking…' : 'Your move') :
          status === 'x_won' ? 'You win! (auto-reset in 2.5s)' :
          status === 'o_won' ? 'AI wins! (auto-reset in 2.5s)' : 'Draw. (auto-reset in 2.5s)'}
      </p>
    </main>
  )
}