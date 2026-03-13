<script setup>
import { ref, onMounted } from "vue"
import { healthCheck } from "./services/api"

const message = ref("Connecting to API...")

onMounted(async () => {
  try {
    const data = await healthCheck()
    message.value = data.message
  } catch {
    message.value = "Failed to connect to API"
  }
})
</script>

<template>
  <div style="padding:40px">
    <h1>Bucket</h1>
    <p>{{ message }}</p>
  </div>
</template>
