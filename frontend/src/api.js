// Small wrappers around the FastAPI endpoints in server.py

async function request(url, options) {
  const res = await fetch(url, options)
  const body = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(body.detail || `Something went wrong (${res.status})`)
  return body
}

function postJson(url, data) {
  return request(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}

export function detectIngredients(file) {
  const form = new FormData()
  form.append('photo', file)
  return request('/api/detect', { method: 'POST', body: form })
}

export function findRecipe(sessionId, ingredients, preferences, another) {
  return postJson('/api/recipe', { session_id: sessionId, ingredients, preferences, another })
}

export function sendChat(sessionId, message) {
  return postJson('/api/chat', { session_id: sessionId, message })
}
