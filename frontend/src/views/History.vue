<template>
  <MainLayout>
    <div class="history-page">
      <div class="history-container">
        <!-- Header -->
        <div class="header-section">
          <h1 class="page-title">My Adventures</h1>
          <p class="page-subtitle">Relive your past scavenger hunts and track current progress across the globe.</p>
        </div>

        <!-- Tabs Navigation -->
        <div class="tabs-nav">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            class="tab-btn" 
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            {{ tab.label }}
          </button>
        </div>

        <!-- Content Area -->
        <div v-if="loading" class="loading-state">
          Loading your adventures...
        </div>
        <div v-else-if="error" class="error-state">
          {{ error }}
        </div>
        <div v-else class="adventures-grid">
          
          <!-- Bucket Cards -->
          <div 
            v-for="bucket in filteredHistory" 
            :key="bucket.bucket_id" 
            class="adventure-card"
            @click="goToBucket(bucket.bucket_id)"
          >
            <!-- COMPLETED CARD -->
            <template v-if="bucketStatus(bucket) === 'completed'">
              <div class="card-image-wrap">
                <img v-if="thumbnails[bucket.bucket_id]" :src="thumbnails[bucket.bucket_id]" alt="Adventure Collage" class="card-image" />
                <div v-else class="card-image-placeholder bg-complete"></div>
                <div class="status-pill green-pill">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                  COMPLETED
                </div>
              </div>
              
              <div class="card-content">
                <div class="card-tag">{{ bucket.location.toUpperCase() }}</div>
                <h3 class="card-title">{{ bucket.name }}</h3>
                <div class="card-meta">
                  <span>
                     <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                     {{ formatDate(bucket.created_at) }}
                  </span>
                  <span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                    Team of {{ bucket.group_type === 'solo' ? '1' : (bucket.group_type === 'couple' ? '2' : (bucket.group_type === 'friends' ? '4' : 'Family')) || '4' }}
                  </span>
                </div>
                <button class="card-action-btn btn-cyan" @click.stop="goToBucket(bucket.bucket_id)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
                  View Memory Collage
                </button>
              </div>
            </template>

            <!-- ONGOING CARD -->
            <template v-else-if="bucketStatus(bucket) === 'ongoing'">
              <div class="card-image-wrap">
                <div class="card-image-placeholder bg-ongoing"></div>
                <div class="status-pill yellow-pill">
                  ONGOING
                </div>
              </div>

              <div class="card-content">
                <div class="card-tag">{{ bucket.location.toUpperCase() }}</div>
                <h3 class="card-title">{{ bucket.name }}</h3>
                <div class="progress-block">
                  <div class="progress-text">
                    <span>Progress</span>
                    <span class="progress-count">{{ completedCount(bucket) }}/{{ bucket.items.length }} items Found</span>
                  </div>
                  <div class="progress-bar-bg">
                    <div class="progress-bar-fill" :style="{ width: progressPercent(bucket) + '%' }"></div>
                  </div>
                </div>
                <div class="card-meta location-meta">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                  {{ bucket.location }}
                </div>
                <button class="card-action-btn btn-light" @click.stop="goToBucket(bucket.bucket_id)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                  Resume Hunt
                </button>
              </div>
            </template>

            <!-- SAVED CARD -->
            <template v-else-if="bucketStatus(bucket) === 'saved'">
              <div class="card-image-wrap">
                <div class="card-image-placeholder bg-saved"></div>
                <div class="status-pill gray-pill">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"></path></svg>
                  SAVED
                </div>
              </div>

              <div class="card-content">
                <div class="card-tag">{{ bucket.location.toUpperCase() }}</div>
                <h3 class="card-title">{{ bucket.name }}</h3>
                <div class="card-meta">
                  <span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                    Estimated: 3 Days
                  </span>
                </div>
                <button class="card-action-btn btn-outline" @click.stop="goToBucket(bucket.bucket_id)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2l.5-.5a15.24 15.24 0 0 0 3-4.59L17.5 8C19 6.5 21 2 21 2s-4.5 2-6 3.5l-6.41 6.5a15.24 15.24 0 0 0-4.59 3l-.5.5Z"></path><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"></path><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"></path></svg>
                  Start Adventure
                </button>
              </div>
            </template>
          </div>

          <!-- STATIC NEW ADVENTURE CARD (Always rendered at the end of grid) -->
          <div class="adventure-card card-new" @click="$router.push('/generator')">
            <div class="new-icon-wrap">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
            </div>
            <h3>New Adventure</h3>
            <p>Start a new hunt or browse the community catalog</p>
          </div>

        </div>
        
        <!-- Empty State (if needed but handled by active view mostly) -->
        <div v-if="!loading && !error && filteredHistory.length === 0" class="empty-state">
          <p>No adventures found in this category.</p>
        </div>

      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"
import MainLayout from "../components/MainLayout.vue"

const router = useRouter()

const history = ref([])
const thumbnails = ref({})
const loading = ref(true)
const error = ref(null)

const tabs = [
  { id: 'completed', label: 'COMPLETED' },
  { id: 'ongoing', label: 'ONGOING' },
  { id: 'saved', label: 'SAVED' },
]
const activeTab = ref('completed')

const filteredHistory = computed(() => {
  return history.value.filter(bucket => bucketStatus(bucket) === activeTab.value)
})

onMounted(async () => {
  try {
    const res = await api.getHistory()
    history.value = res
    // Note: To match mockup, auto-switch to ONGOING tab if no completed ones exist but ongoing do
    if (history.value.some(b => bucketStatus(b) === 'ongoing') && !history.value.some(b => bucketStatus(b) === 'completed')) {
      activeTab.value = 'ongoing'
    } else if (history.value.some(b => bucketStatus(b) === 'saved') && history.value.length > 0 && !history.value.some(b => bucketStatus(b) === 'completed' || bucketStatus(b) === 'ongoing')) {
      activeTab.value = 'saved'
    }
    
    await loadThumbnails()
  } catch (err) {
    if (err.message === "Unauthorized") {
      localStorage.removeItem("token")
      router.push("/login")
      return
    }
    console.error("Failed to load history", err)
    error.value = "Failed to load history. Please try refreshing the page."
  } finally {
    loading.value = false
  }
})

onBeforeUnmount(() => {
  Object.values(thumbnails.value).forEach((url) => {
    URL.revokeObjectURL(url)
  })
})

function bucketStatus(bucket) {
  const total = bucket.items?.length || 0;
  const comp = completedCount(bucket);
  if (total > 0 && comp === total) return 'completed';
  if (total === 0) return 'saved'; // Example interpretation of saved state if empty
  return 'ongoing';
}

function completedCount(bucket) {
  return bucket.items?.filter(item => item.completed).length || 0
}

function progressPercent(bucket) {
  const completed = completedCount(bucket)
  const total = bucket.items?.length || 0
  return total > 0 ? Math.round((completed / total) * 100) : 0
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function goToBucket(id) {
  router.push(`/bucket/${id}`)
}

async function loadThumbnails() {
  const entries = await Promise.all(history.value.map(async (bucket) => {
    if (!bucket.has_collage) {
      return [bucket.bucket_id, null]
    }
    try {
      const blob = await api.generateCollage(bucket.bucket_id, "horizontal", { size: "small", preview: true })
      return [bucket.bucket_id, URL.createObjectURL(blob)]
    } catch (_err) {
      return [bucket.bucket_id, null]
    }
  }))

  thumbnails.value = Object.fromEntries(entries.filter(([, url]) => Boolean(url)))
}
</script>

<style scoped>
.history-page {
  display: flex;
  justify-content: center;
  padding: 4rem 1rem 8rem;
  background-color: #f8fafc;
  min-height: calc(100vh - 400px);
}

.history-container {
  width: 100%;
  max-width: 1100px;
}

/* Header */
.header-section {
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #64748b;
  font-size: 1rem;
}

/* Tabs */
.tabs-nav {
  display: flex;
  gap: 2rem;
  margin-bottom: 3rem;
  border-bottom: 2px solid #e2e8f0;
}

.tab-btn {
  background: transparent;
  border: none;
  font-size: 0.8rem;
  font-weight: 800;
  color: #64748b;
  padding: 0 0 1rem 0;
  cursor: pointer;
  letter-spacing: 0.05em;
  transition: all 0.2s;
  position: relative;
}

.tab-btn:hover {
  color: #0f172a;
}

.tab-btn.active {
  color: #0f172a;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #00e5ff;
}

/* States */
.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 4rem;
  color: #64748b;
  font-weight: 500;
  background: white;
  border-radius: 16px;
  border: 2px dashed #e2e8f0;
}

.error-state {
  color: #ef4444;
  border-color: #fca5a5;
}

/* Grid Layout */
.adventures-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.adventure-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
  display: flex;
  flex-direction: column;
  cursor: pointer;
  border: 1px solid #f1f5f9;
  transition: all 0.3s ease;
}

.adventure-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px -8px rgba(0,0,0,0.08);
}

/* Static Card: New Adventure */
.card-new {
  border: 2px dashed #cbd5e1;
  background: transparent;
  box-shadow: none;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 3rem 2rem;
  min-height: 340px;
}

.card-new:hover {
  border-color: #00e5ff;
  background: #f8fafc;
}

.new-icon-wrap {
  width: 48px;
  height: 48px;
  background: #00e5ff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.card-new h3 {
  font-size: 1.125rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.card-new p {
  color: #64748b;
  font-size: 0.875rem;
}

/* Image wrappers */
.card-image-wrap {
  height: 160px;
  position: relative;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-image-placeholder {
  width: 100%;
  height: 100%;
}

.bg-complete { background: linear-gradient(135deg, #10b981, #059669); }
.bg-ongoing { background: linear-gradient(135deg, #0f172a, #334155); }
.bg-saved { background: linear-gradient(135deg, #64748b, #94a3b8); }

/* Status Pills */
.status-pill {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.green-pill { background-color: #10b981; }
.yellow-pill { background-color: #f59e0b; }
.gray-pill { background-color: #94a3b8; }

/* Card Content */
.card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-tag {
  color: #00b5d8;
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  text-transform: capitalize;
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.card-meta span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.location-meta {
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  gap: 0.25rem;
  text-transform: none;
}

/* Progress Section */
.progress-block {
  margin-bottom: 1rem;
}

.progress-text {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.progress-count {
  color: #64748b;
}

.progress-bar-bg {
  width: 100%;
  height: 6px;
  background-color: #e2e8f0;
  border-radius: 99px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #00e5ff;
  border-radius: 99px;
  transition: width 0.3s ease;
}

/* Action Buttons */
.card-action-btn {
  margin-top: auto;
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.btn-cyan {
  background-color: #00e5ff;
  color: #0f172a;
  box-shadow: 0 4px 6px -1px rgba(0, 229, 255, 0.2);
}

.btn-cyan:hover {
  background-color: #00d6ef;
  box-shadow: 0 6px 10px -1px rgba(0, 229, 255, 0.3);
}

.btn-light {
  background-color: #f1f5f9;
  color: #0f172a;
}

.btn-light:hover {
  background-color: #e2e8f0;
}

.btn-outline {
  background-color: transparent;
  color: #00e5ff;
  border: 1px solid #00e5ff;
}

.btn-outline:hover {
  background-color: #ecfeff;
}

/* Responsive */
@media (max-width: 1024px) {
  .adventures-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .adventures-grid {
    grid-template-columns: 1fr;
  }
}
</style>
