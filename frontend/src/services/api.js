const API_BASE = "http://127.0.0.1:8000/api"

export async function generateBucket(payload) {

  const response = await fetch(`${API_BASE}/buckets/generate/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })

  if (!response.ok) {
    throw new Error("Failed to generate bucket")
  }

  return await response.json()
}