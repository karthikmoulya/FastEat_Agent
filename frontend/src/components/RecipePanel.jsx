import { useState } from 'react'
import { ExternalIcon, HaveIcon, MissingIcon } from './Icons.jsx'

export default function RecipePanel({ recipe, loading, error }) {
  if (loading || error || !recipe) {
    return (
      <article className="panel recipe recipe--empty" aria-busy={loading}>
        {loading ? (
          <>
            <div className="spinner" aria-hidden="true" />
            <p className="panel-title">Your chef is searching the web…</p>
            <p className="muted">This usually takes 10–20 seconds.</p>
          </>
        ) : error ? (
          <p className="error" role="alert">{error}</p>
        ) : (
          <>
            <p className="panel-title">Your recipe will appear here</p>
            <p className="muted">Check your ingredients, pick any preferences, then tap “Find a recipe”.</p>
          </>
        )}
      </article>
    )
  }

  const have = recipe.ingredients.filter((i) => i.have).length
  const total = recipe.ingredients.length
  const missing = total - have
  const meta = [`${recipe.time_minutes} min`, `Serves ${recipe.servings}`, recipe.difficulty, ...recipe.tags]

  return (
    <article className="panel recipe">
      <RecipeImage key={recipe.image_url} url={recipe.image_url} />
      <div className="recipe__body">
        <div className="stack-10">
          <a className="source" href={recipe.source_url} target="_blank" rel="noreferrer">
            <ExternalIcon size={12} stroke="var(--ink-2)" /> Found on {recipe.source_name}
          </a>
          <h1 className="recipe__title">{recipe.title}</h1>
          <div className="recipe__meta">
            {meta.map((m) => <span key={m}>{m}</span>)}
          </div>
        </div>

        <div className="progress">
          <div className="progress__row">
            <span className="progress__label">You have {have} of {total}</span>
            {missing > 0 && <span className="progress__missing">{missing} missing</span>}
          </div>
          <div className="progress__track" role="progressbar" aria-valuemin={0} aria-valuemax={total} aria-valuenow={have}>
            <div className="progress__fill" style={{ width: `${(have / total) * 100}%` }} />
          </div>
        </div>

        <div className="recipe__columns">
          <section className="recipe__ingredients">
            <h2 className="panel-title">Ingredients</h2>
            <ul>
              {recipe.ingredients.map((ing) => (
                <li key={ing.name}>
                  <div className="ing">
                    {ing.have ? <HaveIcon /> : <MissingIcon />}
                    <span className="ing__name">{ing.name}</span>
                    <span className="ing__qty">{ing.qty}</span>
                  </div>
                  {!ing.have && ing.substitute && <div className="ing__sub">Missing — {ing.substitute}</div>}
                </li>
              ))}
            </ul>
          </section>
          <section className="recipe__steps">
            <h2 className="panel-title">Steps</h2>
            <ol>
              {recipe.steps.map((step, i) => (
                <li key={i}>
                  <span className="step__num">{i + 1}</span>
                  <p>{step}</p>
                </li>
              ))}
            </ol>
          </section>
        </div>
      </div>
    </article>
  )
}

function RecipeImage({ url }) {
  const [failed, setFailed] = useState(false)
  if (!url || failed) return null
  return <img className="recipe__image" src={url} alt="" onError={() => setFailed(true)} />
}
