import React, { useEffect, useState } from 'react'

// get the API URL from environment variable or default to localhost
const API_URL = (import.meta.env.API_URL as string) || 'http://localhost:8000'

// define the possible game statuses
type Status = 'playing' | 'x_won' | 'o_won' | 'draw'

// main App component
export default function App() {
    const [board, setBoard] = useState<string>('.........')
    const [status, setStatus] = useState<Status>('playing')
    const [busy, setBusy] = useState(false)
  
    // initialize a new game on component mount
    useEffect(() => {
      fetch(`${API_URL}/api/new`, { method: 'POST' }).then(r => r.json()).then(d => {
        console.debug(d);
        setBoard(d.board)
        setStatus('playing')
      })
    }, [])
  
    // function to handle cell click
    const clickCell = async (i: number) => {
      if (busy || status !== 'playing' || board[i] !== '.') return
      setBusy(true)
      const res = await fetch(`${API_URL}/api/move`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board, move: i })
      })
      const d = await res.json()
      console.debug(d);
      setBoard(d.board)
      setStatus(d.status)
      setBusy(false)
  
      if (d.status !== 'playing') {
        setTimeout(() => restart(), 2500)
      }
    }

    // function to restart the game
    const restart = async () => {
      const r = await fetch(`${API_URL}/api/new`, { method: 'POST' })
      const d = await r.json()
      setBoard(d.board)
      setStatus('playing')
    }
  
    return (
      <main style={{ display: 'grid', placeItems: 'center', minHeight: '100vh', gap: 16 }}>
        <h1>Tic-Tac-Toe</h1>
        <div role="grid" aria-label="Tic Tac Toe board" style={{
          display: 'grid', gridTemplateColumns: 'repeat(3, 80px)', gap: 6
        }}>
          {Array.from(board).map((ch, i) => (
            <button
              key={i}
              role="gridcell"
              aria-label={`cell ${i}`}
              onClick={() => clickCell(i)}
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