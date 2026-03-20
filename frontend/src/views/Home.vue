<template>
  <MainLayout>
    <div class="generator-page">
      <div class="generator-container">
        <!-- Back link -->
        <router-link to="/history" class="back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
          BACK TO DASHBOARD
        </router-link>

        <!-- Header -->
        <div class="page-header">
          <h1>Create New Adventure</h1>
          <p>Design your next legendary hunt with our AI navigator.</p>
        </div>

        <div class="form">
          <!-- Title Input -->
          <div class="form-group">
            <label>ADVENTURE TITLE</label>
            <input 
              v-model="name" 
              type="text" 
              placeholder="e.g., Portland Foodie Hunt" 
              :disabled="loading"
            />
          </div>

          <!-- Destination Input -->
          <div class="form-group">
            <label>DESTINATION</label>
            <div class="input-with-icon">
              <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
              <input 
                v-model="location" 
                type="text" 
                placeholder="e.g., Portland, OR" 
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Budget Level (Card Selectors) -->
          <div class="form-group">
            <label>BUDGET LEVEL</label>
            <div class="card-grid budget-grid">
              <div 
                v-for="opt in budgetOptions" 
                :key="opt.value"
                class="selection-card" 
                :class="{ active: budget === opt.value }"
                @click="budget = opt.value"
              >
                <!-- Simplified SVG Path visual for icon -->
                <div class="card-icon" v-html="opt.icon"></div>
                <span class="card-label">{{ opt.label }}</span>
              </div>
            </div>
          </div>

          <!-- Group Type (Card Selectors) -->
          <div class="form-group">
            <label>GROUP TYPE</label>
            <div class="card-grid group-grid">
              <div 
                v-for="opt in groupOptions" 
                :key="opt.value"
                class="selection-card" 
                :class="{ active: groupType === opt.value }"
                @click="groupType = opt.value"
              >
                <div class="card-icon" v-html="opt.icon"></div>
                <span class="card-label">{{ opt.label }}</span>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <button @click="submitForm" class="btn btn-primary btn-generate" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? "GENERATING..." : "GENERATE HUNT ⚡" }}
          </button>
          
          <p v-if="error" class="error-msg">{{ error }}</p>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"
import MainLayout from "../components/MainLayout.vue"

const router = useRouter()

const name = ref("")
const location = ref("")
const budget = ref("")
const groupType = ref("")
const loading = ref(false)
const error = ref("")

// Options for the UI cards
const budgetOptions = [
  { value: 'free', label: 'Free', icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 5c-1.5 0-2.8 1.4-3 2-3.5-1.5-11-.3-11 5 0 1.8 0 3 2 4.5V20h4v-2h3v2h4v-4c1-.5 1.5-1 2-2h2v-4h-2c0-1-.5-1.5-1-2h0V5z"/><path d="M2 9v1c0 1.1.9 2 2 2h1"/><path d="M16 11h.01"/></svg>' },
  { value: 'budget', label: 'Budget', icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>' },
  { value: 'splurge', label: 'Splurge', icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12l4 6-10 13L2 9Z"/><path d="M11 3 8 9l4 13"/><path d="M13 3l3 6-4 13"/><path d="M2 9h20"/></svg>' },
]

const groupOptions = [
  { value: 'solo', label: 'Solo', icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>' },
  { value: 'couple', label: 'Couple', icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>' },
  { value: 'friends', label: 'Friends', icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>' },
  { value: 'family', label: 'Family', icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 21v-2a4 4 0 0 0-4-4H4a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><circle cx="19" cy="11" r="2"/><path d="M22 21v-2a2 2 0 0 0-2-2h-3"/></svg>' },
]

async function submitForm() {
  if (!name.value || !location.value || !budget.value || !groupType.value) {
    error.value = "Please fill in all fields (including budget and group type)"
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
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.generator-page {
  display: flex;
  justify-content: center;
  padding: 4rem 1rem;
  background: radial-gradient(circle at center top, #ffffff 0%, #f1f5f9 100%);
  min-height: calc(100vh - 400px);
}

.generator-container {
  width: 100%;
  max-width: 640px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: #64748b;
  text-decoration: none;
  letter-spacing: 0.05em;
  margin-bottom: 2rem;
  transition: color 0.2s;
}

.back-link:hover {
  color: #0f172a;
}

.page-header {
  margin-bottom: 3rem;
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.page-header p {
  color: #64748b;
  font-size: 1.1rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

label {
  font-size: 0.75rem;
  font-weight: 800;
  color: #00b5d8;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

input[type="text"] {
  width: 100%;
  padding: 1rem 1.25rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background-color: #ffffff;
  font-size: 1rem;
  font-weight: 500;
  color: #1a202c;
  outline: none;
  transition: all 0.2s;
  box-sizing: border-box;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
}

input[type="text"]:focus {
  border-color: #00e5ff;
  box-shadow: 0 4px 12px rgba(0, 229, 255, 0.15);
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1.25rem;
  color: #94a3b8;
}

.input-with-icon input[type="text"] {
  padding-left: 3rem;
}

/* Card Grids */
.card-grid {
  display: grid;
  gap: 1rem;
}

.budget-grid {
  grid-template-columns: repeat(3, 1fr);
}

.group-grid {
  grid-template-columns: repeat(4, 1fr);
}

.selection-card {
  background-color: white;
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 1.5rem 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  cursor: pointer;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.02);
  transition: all 0.2s ease;
  user-select: none;
}

.selection-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
}

.selection-card.active {
  background-color: #ffffff;
  border-color: #00e5ff;
  box-shadow: 0 0 0 1px #00e5ff, 0 8px 16px rgba(0, 229, 255, 0.15);
}

.card-icon {
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
}

.selection-card.active .card-icon {
  color: #00e5ff;
}

.card-label {
  font-size: 0.875rem;
  font-weight: 700;
  color: #1e293b;
}

/* Submit Button */
.btn-generate {
  margin-top: 1rem;
  padding: 1.25rem;
  font-size: 1.125rem;
  border-radius: 12px;
  letter-spacing: 0.05em;
  color: #0f172a;
  background-color: #00e5ff;
  border: none;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 10px 20px -5px rgba(0, 229, 255, 0.4);
  transition: all 0.2s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 15px 25px -5px rgba(0, 229, 255, 0.5);
  background-color: #00d6ef;
}

.btn-generate:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 3px solid rgba(15, 23, 42, 0.2);
  border-top-color: #0f172a;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-msg {
  color: #ef4444;
  font-weight: 500;
  text-align: center;
}

/* Responsive constraints */
@media (max-width: 640px) {
  .budget-grid, .group-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
