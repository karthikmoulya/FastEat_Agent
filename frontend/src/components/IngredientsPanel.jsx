import { useState } from 'react'
import { CloseIcon, PlusIcon, SearchIcon } from './Icons.jsx'

export default function IngredientsPanel({
  photo, detecting, detectError, ingredients, setIngredients,
  preferences, selectedPrefs, onTogglePref, onSearch, searching, hasRecipe,
}) {
  const [draft, setDraft] = useState('')

  function add(e) {
    e.preventDefault()
    const name = draft.trim()
    if (name && !ingredients.some((i) => i.toLowerCase() === name.toLowerCase())) {
      setIngredients([...ingredients, name])
    }
    setDraft('')
  }

  let heading = 'What do you have?'
  if (detecting) heading = 'Spotting ingredients…'
  else if (photo) heading = `We spotted ${ingredients.length} ingredient${ingredients.length === 1 ? '' : 's'}`

  return (
    <aside className="panel ingredients" aria-label="Your ingredients">
      {(photo || detecting) && (
        <div className="photo">
          {photo ? <img src={photo} alt="Your ingredients" /> : <span className="photo__loading">Reading your photo…</span>}
        </div>
      )}

      <div className="stack-4">
        <h2 className="panel-title">{heading}</h2>
        <p className="muted">
          {photo ? "Remove mistakes or add what's out of frame." : 'Add each ingredient you want to cook with.'}
        </p>
      </div>

      {detectError && <p className="error" role="alert">{detectError}</p>}

      {ingredients.length > 0 && (
        <ul className="chips" aria-label="Ingredients">
          {ingredients.map((name) => (
            <li key={name} className="chip">
              {name}
              <button
                className="chip__remove"
                aria-label={`Remove ${name}`}
                onClick={() => setIngredients(ingredients.filter((x) => x !== name))}
              >
                <CloseIcon size={14} stroke="var(--ink-3)" width={2.2} />
              </button>
            </li>
          ))}
        </ul>
      )}

      <form className="stack-6" onSubmit={add}>
        <label htmlFor="add-ing" className="label">Add an ingredient</label>
        <div className="row-8">
          <input id="add-ing" className="input" placeholder="e.g. paneer" value={draft}
            onChange={(e) => setDraft(e.target.value)} />
          <button className="icon-btn icon-btn--dark" aria-label="Add">
            <PlusIcon stroke="var(--bg)" width={2.2} />
          </button>
        </div>
      </form>

      <div className="stack-8">
        <span className="label">Preferences</span>
        <div className="toggles">
          {preferences.map((label) => {
            const on = selectedPrefs.includes(label)
            return (
              <button key={label} className={`toggle ${on ? 'toggle--on' : ''}`} aria-pressed={on}
                onClick={() => onTogglePref(label)}>
                {label}
              </button>
            )
          })}
        </div>
      </div>

      <button className="btn btn--dark" onClick={onSearch} disabled={searching || detecting || ingredients.length === 0}>
        <SearchIcon size={16} stroke="var(--bg)" />
        {searching ? 'Searching…' : hasRecipe ? 'Find another recipe' : 'Find a recipe'}
      </button>
    </aside>
  )
}
