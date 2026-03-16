<template>
  <div class="container" v-if="bucket">
    <h1>{{ bucket.name }} - {{ bucket.location }}</h1>

    <ul>
      <li v-for="item in bucket.items" :key="item.id">
        <span
          :style="{ textDecoration: item.completed ? 'line-through' : 'none' }"
        >
          {{ item.title }}
        </span>

        <button v-if="!item.completed" @click="markComplete(item.id)">
          Complete
        </button>

        <span v-else>✅ Done</span>
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
  await api.completeItem(id)

  // reload updated state
  await loadBucket()
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