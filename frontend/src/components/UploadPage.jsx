import { useState } from 'react'
import { CameraIcon, UploadIcon } from './Icons.jsx'

const STEPS = [
  ['Snap or upload', 'One photo of everything on your counter.'],
  ['We spot the ingredients', 'Fix anything we missed before searching.'],
  ['Get a matching recipe', "Found on the web, with what you're missing flagged."],
  ['Refine in chat', '"Make it vegetarian." "I don\'t have an oven."'],
]

export default function UploadPage({ onPhoto, onTypeInstead }) {
  const [dragging, setDragging] = useState(false)

  function pick(e) {
    const file = e.target.files?.[0]
    if (file) onPhoto(file)
  }

  function drop(e) {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files?.[0]
    if (file) onPhoto(file)
  }

  return (
    <main className="page">
      <section className="hero">
        <div className="hero__text">
          <span className="badge">Your personal chef agent</span>
          <h1 className="hero__title">Snap what's in your kitchen. Cook something good tonight.</h1>
          <p className="hero__intro">
            Upload a photo of your ingredients. FastEat spots what you have, finds a recipe on the web,
            and tells you what's missing. Then tweak it in chat.
          </p>
        </div>

        <div className="hero__upload">
          <label
            className={`dropzone ${dragging ? 'dropzone--active' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
            onDragLeave={() => setDragging(false)}
            onDrop={drop}
          >
            <input className="visually-hidden" type="file" accept="image/*,.heic" onChange={pick} />
            <span className="dropzone__icon"><UploadIcon size={32} stroke="#fff" width={1.8} /></span>
            <span className="dropzone__title">Drop your photo here</span>
            <span className="dropzone__hint">
              or click to browse. JPG, PNG and HEIC, any size.
            </span>
          </label>
          <div className="hero__actions">
            <label className="btn btn--dark">
              <input className="visually-hidden" type="file" accept="image/*" capture="environment" onChange={pick} />
              <CameraIcon stroke="var(--bg)" width={1.8} /> Take a photo
            </label>
            <button className="btn btn--outline" onClick={onTypeInstead}>Type ingredients instead</button>
          </div>
        </div>
      </section>

      <section id="how" className="how">
        <h2 className="section-title">How it works</h2>
        <div className="how__grid">
          {STEPS.map(([title, text], i) => (
            <div key={title} className="card how__card">
              <span className="how__num">{i + 1}</span>
              <span className="how__title">{title}</span>
              <span className="how__text">{text}</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
