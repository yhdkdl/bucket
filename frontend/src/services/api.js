const API_BASE = "http://127.0.0.1:8000/api"

function getAuthHeaders() {
  const token = localStorage.getItem("token")

  if (!token) {
    return {}
  }

  return { "Authorization": `Bearer ${token}` }
}

async function authFetch(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      ...getAuthHeaders()
    }
  })

  if (response.status === 401) {
    throw new Error("Unauthorized")
  }

  return response
}


const api = {
  generateBucket: async (payload) => {
    const response = await authFetch(`${API_BASE}/buckets/generate/`, {
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
    const response = await authFetch(`${API_BASE}/buckets/history/`)

    if (!response.ok) {
      throw new Error("Failed to fetch history")
    }

    return await response.json()
  },

  getBucketDetail: async (id) => {
    const response = await authFetch(`${API_BASE}/buckets/${id}/`)

    if (!response.ok) {
      throw new Error("Failed to fetch bucket detail")
    }

    return await response.json()
  },

  completeItem: async (id) => {
  const response = await authFetch(
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

  const response = await authFetch(
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

generateCollage: async (bucketId, type, options = {}) => {
  const size = options.size || "normal"
  const preview = options.preview || false
  const response = await authFetch(`${API_BASE}/buckets/${bucketId}/collage/?type=${type}&size=${size}&preview=${preview}`)

  if (!response.ok) {
    throw new Error("Failed to generate collage")
  }

  return await response.blob()
},

login: async (payload) => {
  const response = await fetch(`${API_BASE}/auth/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })

  if (!response.ok) {
    throw new Error("Login failed")
  }

  return await response.json()
},

}

export default api
