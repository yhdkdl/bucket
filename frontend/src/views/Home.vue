<template>
  <div class="container">
    <h1>Bucket Adventure Generator</h1>
    <p class="history-link-wrap">
      <router-link to="/history" class="history-link">View your bucket history</router-link>
    </p>

    <div class="form">
      <input v-model="name" placeholder="Name your bucket list" />
      <input v-model="location" placeholder="Location" />
      <select v-model="budget">
        <option disabled value="">Select budget</option>
        <option value="free">Free</option>
        <option value="budget">Budget Friendly</option>
      </select>
      <select v-model="groupType">
        <option disabled value="">Group Type</option>
        <option value="solo">Solo</option>
        <option value="friends">Friends</option>
        <option value="family">Family</option>
      </select>
      <button @click="submitForm" :disabled="loading">
        {{ loading ? "Generating…" : "Generate Bucket" }}
      </button>
      <p v-if="loading" class="loading">Generating your adventure… ✨ AI is thinking</p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>

    <!-- <div v-if="items.length" class="results">
      <h2>Your Adventure List</h2>
      <ul>
        <li v-for="item in items" :key="item.title">{{ item.title }}</li>
      </ul>
    </div> -->
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const name = ref("")
const location = ref("")
const budget = ref("")
const groupType = ref("")
const loading = ref(false)
const error = ref("")

async function submitForm() {
  if (!name.value || !location.value || !budget.value || !groupType.value) {
    error.value = "Please fill in all fields"
    return
  }

  loading.value = true
  error.value = ""

  try {
    const data = await api.generateBucket({
      name: name.value,
      location: location.value,
      budget: budget.value,
      group_type: groupType.value
    })

    router.push(`/bucket/${data.bucket_id}`)

  } catch (err) {
    if (err.message === "Unauthorized") {
      localStorage.removeItem("token")
      router.push("/login")
      return
    }
    console.error(err)
    error.value = "Failed to generate bucket. Please try again."
  }

  loading.value = false
}
</script>

<style>
.container {
  max-width: 600px;
  margin: auto;
  padding: 40px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.loading {
  color: #007bff;
  font-style: italic;
}

.error {
  color: #dc3545;
  font-weight: bold;
}

.results {
  margin-top: 30px;
}

.history-link-wrap {
  margin-bottom: 16px;
}

.history-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 600;
}

.history-link:hover {
  text-decoration: underline;
}
</style>
