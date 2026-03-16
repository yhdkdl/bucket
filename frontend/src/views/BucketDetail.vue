<template>
  <div class="container" v-if="bucket">
    <h1>{{ bucket.name }} - {{ bucket.location }}</h1>

    <ul>
     <li v-for="item in bucket.items" :key="item.id">

  <span :style="{ textDecoration: item.completed ? 'line-through' : 'none' }">
    {{ item.title }}
  </span>

  <button @click="markComplete(item.id)">
    ✅
  </button>

  <input type="file" @change="upload(item.id, $event)" />

  <div v-if="item.photo">
    <img :src="'http://127.0.0.1:8000' + item.photo" width="150" />
  </div>

</li>
    </ul>
  </div>

  <p v-else>Loading adventure...</p>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import api from "../services/api"

const route = useRoute()
const bucket = ref(null)

async function loadBucket() {
  bucket.value = await api.getBucketDetail(route.params.id)
}

async function markComplete(id) {
  try {
    const data = await api.completeItem(id)
    await loadBucket() // refresh completed state
  } catch (err) {
    alert("Failed to update item")
  }
}
async function upload(id, event) {

  const file = event.target.files[0]

  if (!file) return

  await api.uploadPhoto(id, file)

  await loadBucket()   // refresh UI
}

onMounted(loadBucket)
</script>

<style>
.container {
  max-width: 600px;
  margin: auto;
  padding: 40px;
}
</style>