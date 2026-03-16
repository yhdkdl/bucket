<template>
  <div class="container">
    <h1>Bucket Adventure Generator</h1>

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
      <button @click="submitForm">Generate Bucket</button>
      <p v-if="loading">Generating adventure...</p>
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

async function submitForm() {
  loading.value = true

  try {
    const data = await api.generateBucket({
      name: name.value,
      location: location.value,
      budget: budget.value,
      group_type: groupType.value
    })

    router.push(`/bucket/${data.bucket_id}`)

  } catch (err) {
    console.error(err)
    alert("Failed to generate bucket")
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

.results {
  margin-top: 30px;
}
</style>
