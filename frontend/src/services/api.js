// frontend/src/services/api.js
const API_BASE = "http://127.0.0.1:8000/api"

const api = {
  generateBucket: async (payload) => {
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
  },

  getHistory: async () => {
    const response = await fetch(`${API_BASE}/buckets/history/`, {
      method: "GET"
    })

    if (!response.ok) {
      throw new Error("Failed to fetch history")
    }

    return await response.json()
  }
}

export default api