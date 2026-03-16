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
    const response = await fetch(`${API_BASE}/buckets/history/`)

    if (!response.ok) {
      throw new Error("Failed to fetch history")
    }

    return await response.json()
  },

  getBucketDetail: async (id) => {
    const response = await fetch(`${API_BASE}/buckets/${id}/`)

    if (!response.ok) {
      throw new Error("Failed to fetch bucket detail")
    }

    return await response.json()
  },

  completeItem: async (id) => {
  const response = await fetch(
    `${API_BASE}/buckets/items/${id}/complete/`,
    { method: "POST" }
  )

  if (!response.ok) {
    throw new Error("Failed to complete item")
  }

  return await response.json()
},

uploadPhoto: async (id, file) => {

  const formData = new FormData()
  formData.append("photo", file)

  const response = await fetch(
    `${API_BASE}/buckets/items/${id}/upload-photo/`,
    {
      method: "POST",
      body: formData
    }
  )

  if (!response.ok) {
    throw new Error("Failed to upload photo")
  }

  return await response.json()
},

generateCollage: async (bucketId, type) => {
  const response = await fetch(`${API_BASE}/buckets/${bucketId}/collage/?type=${type}`)

  if (!response.ok) {
    throw new Error("Failed to generate collage")
  }

  return await response.blob()
}

}

export default api