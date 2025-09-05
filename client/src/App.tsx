import React, { useEffect, useState } from 'react'
import './styles.css'
import { iconPath } from './assets'

// get the API URL from environment variable or default to localhost
const API_URL = (import.meta.env.API_URL as string) || 'http://localhost:8000'

// define the possible game statuses
type Status = 'playing' | 'x_won' | 'o_won' | 'draw'

// main App component
export default function App() {
    const [board, setBoard] = useState<string>('.........')
    const [status, setStatus] = useState<Status>('playing')
    const [busy, setBusy] = useState(false)
    const side = Math.sqrt(board.length) | 0
  
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
  
    // function to render each cell
    const renderCell = (ch: string, i: number) => {
      let src = ''
      let alt = ''
      if (ch === 'X') { src = iconPath('tick'); alt = 'tick (X)'; }
      if (ch === 'O') { src = iconPath('eyeball'); alt = 'eyeball (O)'; }
  
      return (
        <button
          key={i}
          role="gridcell"
          aria-label={`cell ${i}`}
          className="cell"
          onClick={() => clickCell(i)}
          disabled={busy || ch !== '.' || status !== 'playing'}
        >
          {ch === '.' ? null : (
            <img src={src} alt={alt} width={56} height={56} className="icon" />
          )}
        </button>
      )
    }
  
    return (
      <main className="board-wrap" aria-live="polite">
        <header className="header">
          <div className="title">Tïck-Tac-Toe</div>
          <div className="subtitle">a tiny, unbeatable diversion</div>
        </header>
  
        <section
          className="board"
          role="grid"
          aria-label={`Tic Tac Toe board ${side} by ${side}`}
          style={{ gridTemplateColumns: `repeat(${side}, 84px)` }}
        >
          {Array.from(board).map((ch, i) => renderCell(ch, i))}
        </section>
  
        <p className="status">
          {status === 'playing' ? (busy ? <span className="ai">thinking…</span> : 'your move') :
           status === 'x_won' ? <span className="win">you win! (resetting)</span> :
           status === 'o_won' ? <span className="win">AI wins! (resetting)</span> :
           'draw (resetting)'}
        </p>
      </main>
    )
  }