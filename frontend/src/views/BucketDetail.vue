<template>
  <div class="container" v-if="bucket">
    <h1>{{ bucket.name }} - {{ bucket.location }}</h1>

    <!-- Progress Bar -->
    <div class="progress-container">
      <label>Progress: {{ completedCount }}/{{ totalCount }}</label>
      <progress :value="completedCount" :max="totalCount"></progress>
    </div>

    <ul>
      <li v-for="item in bucket.items" :key="item.id" class="bucket-item">
        <span :style="{ textDecoration: item.completed ? 'line-through' : 'none' }">
          {{ item.title }}
        </span>

        <button @click="markComplete(item.id)" :disabled="actionLoading">
          ✅
        </button>

        <input type="file" @change="upload(item.id, $event)" :disabled="actionLoading" />

        <div v-if="item.photo" class="photo-preview">
          <img :src="mediaBase + item.photo" width="150" />
        </div>
      </li>
    </ul>

    <!-- Collage Controls -->
    <div class="collage-controls">
      <label for="collageType">Choose Collage Type:</label>
      <select id="collageType" v-model="collageType">
        <option value="horizontal">Horizontal</option>
        <option value="vertical">Vertical</option>
      </select>

      <button
        @click="generatePreview"
        :disabled="!allCompleted || previewLoading || actionLoading"
      >
        {{ previewLoading ? "Generating preview…" : "Generate Preview" }}
      </button>

      <button
        @click="downloadCollage"
        :disabled="!allCompleted || !previewUrl || actionLoading"
      >
        {{ actionLoading ? "Downloading…" : "Download Collage" }}
      </button>

      <p v-if="!allCompleted" style="color: gray; font-size: 0.9em;">
        Complete all items first to enable preview & download
      </p>

      <p v-if="previewError" style="color: red; font-size: 0.9em;">
        {{ previewError }}
      </p>

      <p v-if="actionError" style="color: red; font-size: 0.9em;">
        {{ actionError }}
      </p>

      <div v-if="previewUrl" class="collage-preview">
        <img
          :src="previewUrl"
          @load="onPreviewLoaded"
          @error="onPreviewError"
          alt="Collage preview"
        />
      </div>
    </div>
  </div>

  <p v-else>Loading adventure...</p>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue"
import { useRoute } from "vue-router"
import api from "../services/api"

const route = useRoute()
const bucket = ref(null)
const collageType = ref("horizontal") // default type

const mediaBase = "http://127.0.0.1:8000" // for image URLs
const apiBase = "http://127.0.0.1:8000/api" // used for collage preview URLs

const previewUrl = ref(null)
const previewLoading = ref(false)
const previewError = ref(null)

const actionLoading = ref(false)
const actionError = ref(null)

watch(collageType, () => {
  // Clear preview whenever type changes (user must regenerate)
  previewUrl.value = null
  previewError.value = null
})

async function loadBucket() {
  try {
    bucket.value = await api.getBucketDetail(route.params.id)
  } catch (err) {
    alert("Failed to load bucket")
  }
}

// Completion toggle
async function markComplete(id) {
  actionLoading.value = true
  actionError.value = null
  try {
    await api.completeItem(id)
    await loadBucket()
  } catch (err) {
    actionError.value = "Failed to update item. Please try again."
  }
  actionLoading.value = false
}

// Upload photo for a bucket item
async function upload(id, event) {
  const file = event.target.files[0]
  if (!file) return

  actionLoading.value = true
  actionError.value = null
  try {
    await api.uploadPhoto(id, file)
    await loadBucket()
  } catch (err) {
    actionError.value = "Failed to upload photo. Please try again."
  }
  actionLoading.value = false
}

// Preview collage
function getCollageEndpoint(preview = false) {
  return `${apiBase}/buckets/${bucket.value.id}/collage/?type=${collageType.value}&preview=${preview}`
}

function onPreviewLoaded() {
  previewLoading.value = false
}

function onPreviewError() {
  previewLoading.value = false
  previewError.value = "Failed to load preview"
}

async function generatePreview() {
  if (!allCompleted.value) {
    alert("Complete all items to generate a preview!")
    return
  }

  previewError.value = null
  previewLoading.value = true
  previewUrl.value = getCollageEndpoint(true)
}

// Download collage
async function downloadCollage() {
  if (!allCompleted.value) {
    alert("Complete all items to download the collage!")
    return
  }

  actionLoading.value = true
  actionError.value = null
  try {
    const blob = await api.generateCollage(bucket.value.id, collageType.value)
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `${bucket.value.name}_collage.png`
    a.click()
    URL.revokeObjectURL(url)
  } catch (err) {
    actionError.value = "Failed to generate collage. Please try again."
  }
  actionLoading.value = false
}

// Computed properties for progress
const totalCount = computed(() => bucket.value?.items.length || 0)
const completedCount = computed(() => bucket.value?.items.filter(i => i.completed).length || 0)
const allCompleted = computed(() => totalCount.value > 0 && completedCount.value === totalCount.value)

onMounted(loadBucket)
</script>

<style>
.container {
  max-width: 600px;
  margin: auto;
  padding: 40px;
}

.bucket-item {
  margin-bottom: 20px;
}

.photo-preview {
  margin-top: 5px;
}

.progress-container {
  margin-bottom: 20px;
}

.collage-controls {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.collage-preview {
  margin-top: 20px;
  border: 1px solid #ddd;
  padding: 10px;
  background: #fafafa;
}

.collage-preview img {
  max-width: 100%;
  display: block;
  margin: auto;
}
</style>