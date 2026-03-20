<template>
  <MainLayout>
    <div class="bucket-detail-page">
      <div v-if="bucket" class="content-wrapper">
        
        <!-- Header & Progress -->
        <div class="header-section">
          <div class="header-left">
            <div class="eyebrow">CURRENT ADVENTURE</div>
            <h1 class="adventure-title">{{ bucket.name }}</h1>
            <p class="adventure-subtitle">Explore your custom bucket list for {{ bucket.location }}!</p>
          </div>
          
          <div class="progress-widget">
            <div class="progress-info">
              <span class="progress-label">YOUR PROGRESS</span>
              <div class="progress-stats">
                <span class="progress-percent">{{ Math.round((completedCount / totalCount) * 100) || 0 }}%</span>
                <span class="progress-text">Complete</span>
              </div>
            </div>
            <div class="progress-circle">
              <svg viewBox="0 0 36 36" class="circular-chart">
                <path class="circle-bg"
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path class="circle"
                  :stroke-dasharray="`${(completedCount / totalCount) * 100 || 0}, 100`"
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div class="circle-text">{{ completedCount }}/{{ totalCount }}</div>
            </div>
          </div>
        </div>

        <!-- Horizontal Progress Bar -->
        <div class="progress-bar-container">
          <div class="progress-bar-fill" :style="{ width: `${(completedCount / totalCount) * 100 || 0}%` }"></div>
        </div>

        <!-- Task List -->
        <div class="task-list">
          <div 
            v-for="item in bucket.items" 
            :key="item.id" 
            class="task-card"
            :class="{ 'is-completed': item.completed }"
          >
            <div class="task-left">
              <button 
                class="checkbox-btn" 
                :class="{ 'checked': item.completed }" 
                @click="markComplete(item.id)" 
                :disabled="actionLoading"
              >
                <svg v-if="item.completed" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
              </button>
              <div class="task-text">
                <h3>{{ item.title }}</h3>
                <!-- Assume we don't have descriptions in API, just a generic nice placeholder or omit -->
                <p>Complete this challenge to earn progress.</p>
              </div>
            </div>
            
            <div class="task-right">
              <!-- Upload Photo Button -->
              <div class="upload-wrapper">
                <input 
                  :id="'file-upload-' + item.id" 
                  type="file" 
                  @change="upload(item.id, $event)" 
                  :disabled="actionLoading"
                  class="hidden-input"
                  accept="image/*"
                />

                <!-- Photo Thumbnail (Re-uploadable) -->
                <div v-if="item.photo" class="photo-thumbnail">
                  <label :for="'file-upload-' + item.id" class="reupload-label" :class="{ 'disabled': actionLoading }">
                    <img :src="mediaBase + item.photo" alt="Task photo" />
                    <div class="reupload-overlay">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 2v6h-6M2 22l5.5-5.5M21.34 15.57a10 10 0 1 1-.59-9.27v0"></path></svg>
                    </div>
                  </label>
                </div>

                <!-- Add Photo Button -->
                <label v-else :for="'file-upload-' + item.id" class="btn-add-photo" :class="{ 'disabled': actionLoading }">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                  Add Photo
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Sticky Bottom CTA -->
        <div class="bottom-cta-wrap">
          <button 
            class="btn-generate-collage" 
            :disabled="!allCompleted || actionLoading"
            @click="showModal = true"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            Generate Memory Collage
          </button>
          <p class="unlock-text" v-if="!allCompleted">Unlocks when all {{ totalCount }} tasks are completed</p>
        </div>
      </div>

      <div v-else class="loading-state">
        <p>Loading adventure...</p>
      </div>

      <!-- Collage Modal Overlay -->
      <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
        <div class="modal-content">
          <button class="modal-close" @click="showModal = false">&times;</button>
          
          <div class="modal-header">
            <h2>Customize Your Collage</h2>
            <p>Your adventure is complete! Pick your preferred layout and save your memories.</p>
          </div>

          <!-- Type Toggle -->
          <div class="type-toggle">
            <button 
              class="toggle-btn" 
              :class="{ 'active': collageType === 'horizontal' }"
              @click="collageType = 'horizontal'"
            >
              Horizontal
            </button>
            <button 
              class="toggle-btn" 
              :class="{ 'active': collageType === 'vertical' }"
              @click="collageType = 'vertical'"
            >
              Vertical
            </button>
          </div>

          <!-- Preview Area -->
          <div class="collage-preview-box">
            <div v-if="previewLoading" class="preview-spinner">Generating...</div>
            <img 
              v-else-if="previewUrl" 
              :src="previewUrl" 
              class="modal-preview-img" 
            />
            <div v-else class="preview-placeholder">
              <div class="placeholder-grid" :class="collageType">
                <div class="grid-item"></div>
                <div class="grid-item"></div>
                <div class="grid-item"></div>
              </div>
            </div>
          </div>

          <p v-if="previewError" class="modal-error">{{ previewError }}</p>
          <p v-if="actionError" class="modal-error">{{ actionError }}</p>

          <!-- Modal Actions -->
          <div class="modal-actions">
            <button 
              class="btn-modal btn-preview" 
              @click="generatePreview"
              :disabled="previewLoading || actionLoading"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
              {{ previewLoading ? "Loading..." : "Show Preview" }}
            </button>

            <button 
              class="btn-modal btn-download" 
              @click="downloadCollage"
              :disabled="!previewUrl || actionLoading"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
              {{ actionLoading ? "Downloading..." : "Download" }}
            </button>
          </div>

        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "../services/api"
import MainLayout from "../components/MainLayout.vue"

const route = useRoute()
const router = useRouter()
const bucket = ref(null)
const collageType = ref("horizontal")
const showModal = ref(false)

const mediaBase = "http://127.0.0.1:8000"

const previewUrl = ref(null)
const previewLoading = ref(false)
const previewError = ref(null)

const actionLoading = ref(false)
const actionError = ref(null)

watch(collageType, () => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
  previewUrl.value = null
  previewError.value = null
})

function handleUnauthorized(err) {
  if (err.message === "Unauthorized") {
    localStorage.removeItem("token")
    router.push("/login")
    return true
  }
  return false
}

async function loadBucket() {
  try {
    bucket.value = await api.getBucketDetail(route.params.id)
  } catch (err) {
    if (handleUnauthorized(err)) return
    alert("Failed to load bucket")
  }
}

async function markComplete(id) {
  actionLoading.value = true
  actionError.value = null
  try {
    await api.completeItem(id)
    await loadBucket()
  } catch (err) {
    if (handleUnauthorized(err)) return
    actionError.value = "Failed to update item. Please try again."
  }
  actionLoading.value = false
}

async function upload(id, event) {
  const file = event.target.files[0]
  if (!file) return

  actionLoading.value = true
  actionError.value = null
  try {
    await api.uploadPhoto(id, file)
    await loadBucket()
  } catch (err) {
    if (handleUnauthorized(err)) return
    actionError.value = "Failed to upload photo. Please try again."
  }
  actionLoading.value = false
}

async function generatePreview() {
  if (!allCompleted.value) return

  previewError.value = null
  previewLoading.value = true

  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }

  try {
    const blob = await api.generateCollage(bucket.value.id, collageType.value, { preview: true })
    previewUrl.value = URL.createObjectURL(blob)
    previewLoading.value = false
  } catch (err) {
    if (handleUnauthorized(err)) return
    previewError.value = "Failed to load preview"
    previewLoading.value = false
  }
}

async function downloadCollage() {
  if (!allCompleted.value) return

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
    if (handleUnauthorized(err)) return
    actionError.value = "Failed to generate collage. Please try again."
  }
  actionLoading.value = false
}

const totalCount = computed(() => bucket.value?.items.length || 0)
const completedCount = computed(() => bucket.value?.items.filter(i => i.completed).length || 0)
const allCompleted = computed(() => totalCount.value > 0 && completedCount.value === totalCount.value)

onMounted(loadBucket)
onBeforeUnmount(() => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
})
</script>

<style scoped>
.bucket-detail-page {
  display: flex;
  justify-content: center;
  padding: 4rem 1rem;
  background-color: #f8fafc;
  min-height: calc(100vh - 400px);
}

.content-wrapper {
  width: 100%;
  max-width: 800px;
}

.loading-state {
  text-align: center;
  color: #64748b;
  font-weight: 500;
  margin-top: 4rem;
}

/* Header & Progress Widgets */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
}

.header-left {
  max-width: 60%;
}

.eyebrow {
  color: #00b5d8;
  font-weight: 800;
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}

.adventure-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
}

.adventure-subtitle {
  color: #64748b;
  font-size: 1rem;
}

.progress-widget {
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.progress-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.progress-label {
  font-size: 0.65rem;
  font-weight: 800;
  color: #94a3b8;
  letter-spacing: 0.1em;
  margin-bottom: 0.25rem;
}

.progress-stats {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
}

.progress-percent {
  font-size: 1.5rem;
  font-weight: 900;
  color: #0f172a;
}

.progress-text {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

.progress-circle {
  position: relative;
  width: 50px;
  height: 50px;
}

.circular-chart {
  display: block;
  margin: 0 auto;
  max-width: 100%;
  max-height: 250px;
}

.circle-bg {
  fill: none;
  stroke: #f1f5f9;
  stroke-width: 3.8;
}

.circle {
  fill: none;
  stroke-width: 3.8;
  stroke-linecap: round;
  stroke: #00e5ff;
  transition: stroke-dasharray 0.5s ease-out;
}

.circle-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  fill: #0f172a;
  font-size: 0.8rem;
  font-weight: 800;
}

/* Linear Progress Bar */
.progress-bar-container {
  width: 100%;
  height: 8px;
  background-color: #e2e8f0;
  border-radius: 999px;
  margin-bottom: 3rem;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #00e5ff;
  border-radius: 999px;
  transition: width 0.5s ease-out;
}

/* Task List Cards */
.task-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.task-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
  border-left: 6px solid #e2e8f0;
  border-right: 1px solid #f1f5f9;
  border-top: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
  transition: all 0.3s ease;
}

.task-card.is-completed {
  border-left-color: #00e5ff;
}

.task-card:hover {
  transform: translateX(4px);
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
}

.task-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.checkbox-btn {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: 2px solid #cbd5e1;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: white;
  padding: 0;
}

.checkbox-btn.checked {
  background-color: #0f172a;
  border-color: #0f172a;
}

.checkbox-btn:hover:not(:disabled) {
  border-color: #0f172a;
}

.checkbox-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.task-text h3 {
  font-size: 1.125rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.25rem;
}

.task-text p {
  color: #64748b;
  font-size: 0.875rem;
  margin: 0;
}

.task-right {
  display: flex;
  align-items: center;
}

.hidden-input {
  display: none;
}

.btn-add-photo {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #ecfeff;
  color: #00b5d8;
  font-weight: 700;
  font-size: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add-photo:hover:not(.disabled) {
  background-color: #cffafe;
  transform: translateY(-1px);
}

.btn-add-photo.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.photo-thumbnail {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.photo-thumbnail img {
  display: block;
  width: 60px;
  height: 60px;
  object-fit: cover;
}

.reupload-label {
  cursor: pointer;
  position: relative;
  display: block;
}

.reupload-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15, 23, 42, 0.6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
  border-radius: 8px;
}

.reupload-label:not(.disabled):hover .reupload-overlay {
  opacity: 1;
}

.reupload-label.disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* Bottom CTA */
.bottom-cta-wrap {
  margin-top: 3rem;
  text-align: center;
}

.btn-generate-collage {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background-color: #00e5ff;
  color: #0f172a;
  font-size: 0.95rem;
  font-weight: 800;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 8px 15px -3px rgba(0, 229, 255, 0.4);
}

.btn-generate-collage:hover:not(:disabled) {
  background-color: #00d6ef;
  transform: translateY(-2px);
  box-shadow: 0 12px 20px -3px rgba(0, 229, 255, 0.5);
}

.btn-generate-collage:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  box-shadow: none;
  filter: grayscale(100%);
}

.unlock-text {
  margin-top: 1rem;
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 600;
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.modal-content {
  background: white;
  width: 100%;
  max-width: 540px;
  border-radius: 24px;
  padding: 3rem 2.5rem;
  position: relative;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: modal-pop 0.3s ease-out;
}

@keyframes modal-pop {
  0% { opacity: 0; transform: scale(0.95) translateY(20px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}

.modal-close {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #94a3b8;
  cursor: pointer;
  transition: color 0.2s;
}

.modal-close:hover {
  color: #0f172a;
}

.modal-header {
  text-align: center;
  margin-bottom: 2rem;
}

.modal-header h2 {
  font-size: 1.75rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.modal-header p {
  color: #64748b;
  font-size: 0.9rem;
}

.type-toggle {
  display: flex;
  background: #f1f5f9;
  border-radius: 12px;
  padding: 0.25rem;
  margin: 0 auto 2.5rem;
  width: max-content;
}

.toggle-btn {
  padding: 0.5rem 1.5rem;
  border-radius: 10px;
  border: none;
  background: transparent;
  font-weight: 700;
  font-size: 0.875rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-btn.active {
  background: #00e5ff;
  color: #0f172a;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.collage-preview-box {
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 16px;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2.5rem;
  overflow: hidden;
}

.preview-placeholder {
  width: 100%;
  padding: 2rem;
  display: flex;
  justify-content: center;
}

.placeholder-grid {
  display: flex;
  gap: 1rem;
}

.placeholder-grid.horizontal {
  flex-direction: row;
}

.placeholder-grid.vertical {
  flex-direction: column;
}

.grid-item {
  width: 80px;
  height: 80px;
  background: #e2e8f0;
  border-radius: 8px;
}

.modal-preview-img {
  max-width: 100%;
  max-height: 300px;
  display: block;
}

.preview-spinner {
  color: #94a3b8;
  font-weight: 600;
  font-size: 0.875rem;
}

.modal-error {
  color: #ef4444;
  font-size: 0.875rem;
  text-align: center;
  margin-bottom: 1rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
}

.btn-modal {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-preview {
  background: #ecfeff;
  color: #00b5d8;
}

.btn-preview:hover:not(:disabled) {
  background: #cffafe;
}

.btn-download {
  background: white;
  color: #00b5d8;
  border: 2px solid #00b5d8;
}

.btn-download:hover:not(:disabled) {
  background: #00b5d8;
  color: white;
}

.btn-modal:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive constraints */
@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }
  .header-left {
    max-width: 100%;
  }
}
</style>
