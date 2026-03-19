<template>
  <MainLayout>
    <div class="auth-page">
      <div class="auth-card">
        <div class="eyebrow">BEGIN YOUR JOURNEY</div>
        <h1 class="auth-title">Create your account</h1>
        <p class="auth-subtitle">Join the next generation of digital explorers.</p>

        <form @submit.prevent="handleRegister" class="auth-form">
          <div class="form-group">
            <label for="username">USERNAME</label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="neon_navigator"
              required
            />
          </div>

          <div class="form-group">
            <label for="email">EMAIL ADDRESS</label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="explorer@bucket.io"
              required
            />
          </div>

          <div class="form-group">
            <label for="password">PASSWORD</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="••••••••"
              required
            />
          </div>

          <div class="checkbox-group">
            <input type="checkbox" id="terms" required v-model="terms" />
            <label for="terms" class="checkbox-label">
              I agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
            </label>
          </div>

          <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
            {{ loading ? "CREATING..." : "CREATE ACCOUNT" }}
          </button>
        </form>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <p class="auth-footer">
          Already have an account? <router-link to="/login">Log In</router-link>
        </p>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../../services/api"
import MainLayout from "../../components/MainLayout.vue"

const router = useRouter()

const username = ref("")
const email = ref("")
const password = ref("")
const terms = ref(false)
const loading = ref(false)
const error = ref("")

async function handleRegister() {
  if (!terms.value) {
    error.value = "You must agree to the Terms of Service."
    return
  }

  loading.value = true
  error.value = ""

  try {
    await api.register({
      username: username.value,
      email: email.value,
      password: password.value
    })
    router.push("/login")
  } catch (err) {
    error.value = err.message || "Registration failed"
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6rem 1rem;
  background: radial-gradient(circle at center, #ffffff 0%, #f1f5f9 100%);
  min-height: calc(100vh - 400px);
}

.auth-card {
  background: white;
  width: 100%;
  max-width: 440px;
  padding: 3.5rem 2.5rem;
  border-radius: 20px;
  box-shadow: 0 20px 40px -10px rgba(0,0,0,0.05);
  text-align: center;
}

.eyebrow {
  font-size: 0.75rem;
  font-weight: 700;
  color: #00b5d8;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
}

.auth-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.auth-subtitle {
  color: #64748b;
  font-size: 0.95rem;
  margin-bottom: 2.5rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  text-align: left;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #1a202c;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 0.875rem 1rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background-color: #f8fafc;
  font-size: 0.95rem;
  color: #1a202c;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

input:focus {
  border-color: #00e5ff;
  background-color: white;
}

.checkbox-group {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

input[type="checkbox"] {
  margin-top: 0.25rem;
}

.checkbox-label {
  font-size: 0.8rem;
  font-weight: 500;
  color: #4a5568;
  letter-spacing: normal;
  text-transform: none;
  line-height: 1.5;
}

.checkbox-label a {
  color: #00b5d8;
  font-weight: 600;
  text-decoration: none;
}

.btn-block {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  margin-top: 0.5rem;
  border-radius: 12px;
}

.btn-primary {
  background-color: #00e5ff;
  color: #0f172a;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.btn-primary:hover {
  background-color: #00c6dd;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 229, 255, 0.25);
}

.error-msg {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 1rem;
  font-weight: 500;
}

.auth-footer {
  margin-top: 2rem;
  font-size: 0.9rem;
  color: #64748b;
}

.auth-footer a {
  color: #00b5d8;
  font-weight: 700;
  text-decoration: none;
}
</style>
