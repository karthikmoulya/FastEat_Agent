import { useState } from 'react'
import Header from './components/Header.jsx'
import UploadPage from './components/UploadPage.jsx'
import Workspace from './components/Workspace.jsx'
import { detectIngredients } from './api.js'

export default function App() {
  // 'upload' = landing page, 'cook' = workspace
  const [view, setView] = useState('upload')
  // a fresh id per photo gives the agent a fresh conversation memory
  const [sessionId, setSessionId] = useState(() => crypto.randomUUID())
  const [photo, setPhoto] = useState(null)
  const [ingredients, setIngredients] = useState([])
  const [detecting, setDetecting] = useState(false)
  const [error, setError] = useState('')

  async function handlePhoto(file) {
    setView('cook')
    setPhoto(null)
    setIngredients([])
    setError('')
    setDetecting(true)
    try {
      const result = await detectIngredients(file)
      setPhoto(result.preview)
      setIngredients(result.detected_ingredients)
    } catch (e) {
      setError(e.message)
    } finally {
      setDetecting(false)
    }
  }

  function handleTypeInstead() {
    setView('cook')
    setPhoto(null)
    setIngredients([])
    setError('')
  }

  function startOver() {
    setSessionId(crypto.randomUUID())
    setView('upload')
  }

  return (
    <div className="app">
      <Header view={view} onHome={startOver} />
      {view === 'upload' ? (
        <UploadPage onPhoto={handlePhoto} onTypeInstead={handleTypeInstead} />
      ) : (
        <Workspace
          key={sessionId}
          sessionId={sessionId}
          photo={photo}
          ingredients={ingredients}
          setIngredients={setIngredients}
          detecting={detecting}
          detectError={error}
        />
      )}
    </div>
  )
}
