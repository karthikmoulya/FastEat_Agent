import { useState } from 'react'
import IngredientsPanel from './IngredientsPanel.jsx'
import RecipePanel from './RecipePanel.jsx'
import ChatPanel from './ChatPanel.jsx'
import { findRecipe, sendChat } from '../api.js'

const PREFERENCES = ['Vegetarian', 'Under 30 min', 'No oven', 'Spicy']

export default function Workspace({ sessionId, photo, ingredients, setIngredients, detecting, detectError }) {
  const [prefs, setPrefs] = useState([])
  const [recipe, setRecipe] = useState(null)
  const [recipeLoading, setRecipeLoading] = useState(false)
  const [recipeError, setRecipeError] = useState('')
  // chat messages: { role: 'user' | 'chef', text, changes?, recipe?, applied? }
  const [messages, setMessages] = useState([])
  const [thinking, setThinking] = useState(false)

  async function searchRecipe() {
    setRecipeLoading(true)
    setRecipeError('')
    try {
      const reply = await findRecipe(sessionId, ingredients, prefs, recipe !== null)
      setRecipe(reply.recipe)
      setMessages((m) => [...m, { role: 'chef', text: reply.message }])
    } catch (e) {
      setRecipeError(e.message)
    } finally {
      setRecipeLoading(false)
    }
  }

  async function chat(text) {
    setMessages((m) => [...m, { role: 'user', text }])
    setThinking(true)
    try {
      const reply = await sendChat(sessionId, text)
      setMessages((m) => [...m, { role: 'chef', text: reply.message, changes: reply.changes, recipe: reply.recipe }])
    } catch (e) {
      setMessages((m) => [...m, { role: 'chef', text: `Sorry, something went wrong: ${e.message}` }])
    } finally {
      setThinking(false)
    }
  }

  function applyChanges(index) {
    setRecipe(messages[index].recipe)
    setMessages((m) => m.map((msg, i) => (i === index ? { ...msg, applied: true } : msg)))
  }

  function togglePref(label) {
    setPrefs((p) => (p.includes(label) ? p.filter((x) => x !== label) : [...p, label]))
  }

  return (
    <main className="workspace">
      <IngredientsPanel
        photo={photo}
        detecting={detecting}
        detectError={detectError}
        ingredients={ingredients}
        setIngredients={setIngredients}
        preferences={PREFERENCES}
        selectedPrefs={prefs}
        onTogglePref={togglePref}
        onSearch={searchRecipe}
        searching={recipeLoading}
        hasRecipe={recipe !== null}
      />
      <RecipePanel recipe={recipe} loading={recipeLoading} error={recipeError} />
      <ChatPanel
        messages={messages}
        thinking={thinking}
        enabled={recipe !== null && !recipeLoading}
        onSend={chat}
        onApply={applyChanges}
      />
    </main>
  )
}
