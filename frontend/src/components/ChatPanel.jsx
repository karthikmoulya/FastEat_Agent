import { useEffect, useRef, useState } from 'react'
import { ArrowRightIcon, SendIcon } from './Icons.jsx'

const QUICK_REPLIES = ['Make it spicier', 'Halve servings', 'No onion or garlic']

export default function ChatPanel({ messages, thinking, enabled, onSend, onApply }) {
  const [draft, setDraft] = useState('')
  const listRef = useRef(null)

  // keep the newest message in view
  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, thinking])

  const canSend = enabled && !thinking

  function submit(e) {
    e.preventDefault()
    const text = draft.trim()
    if (!text || !canSend) return
    onSend(text)
    setDraft('')
  }

  return (
    <section className="panel chat" aria-label="Chat with your chef">
      <div className="chat__header">
        <h2 className="panel-title">Tweak this recipe</h2>
        <span className="muted small">Your chef remembers the conversation</span>
      </div>

      <div className="chat__messages" ref={listRef} aria-live="polite">
        {messages.length === 0 && (
          <p className="muted small chat__empty">Once you have a recipe, ask for changes here.</p>
        )}
        {messages.map((msg, i) =>
          msg.role === 'user' ? (
            <div key={i} className="bubble bubble--user">{msg.text}</div>
          ) : (
            <div key={i} className="chef-reply">
              <div className="bubble bubble--chef">{msg.text}</div>
              {msg.changes?.length > 0 && (
                <div className="changes">
                  <span className="changes__label">Recipe changes</span>
                  {msg.changes.map((c, j) => (
                    <div key={j} className="changes__row">
                      <span className="changes__from">{c.from}</span>
                      <ArrowRightIcon size={12} stroke="var(--ink-3)" />
                      <span className="changes__to">{c.to}</span>
                    </div>
                  ))}
                  {msg.recipe && (
                    <button className="btn btn--outline btn--tiny" onClick={() => onApply(i)} disabled={msg.applied}>
                      {msg.applied ? 'Applied ✓' : 'Apply to recipe'}
                    </button>
                  )}
                </div>
              )}
            </div>
          )
        )}
        {thinking && <div className="bubble bubble--chef muted">Chef is thinking…</div>}
      </div>

      <div className="chat__footer">
        <div className="quick-replies">
          {QUICK_REPLIES.map((label) => (
            <button key={label} className="quick-reply" disabled={!canSend} onClick={() => onSend(label)}>
              {label}
            </button>
          ))}
        </div>
        <form className="row-8" onSubmit={submit}>
          <label htmlFor="chat-in" className="visually-hidden">Message the chef</label>
          <input id="chat-in" className="input input--round" placeholder="I don't have an oven…"
            value={draft} onChange={(e) => setDraft(e.target.value)} disabled={!enabled} />
          <button className="icon-btn icon-btn--accent" aria-label="Send" disabled={!canSend || !draft.trim()}>
            <SendIcon stroke="#fff" />
          </button>
        </form>
      </div>
    </section>
  )
}
