<template>
  <MainLayout>
    <div class="auth-page">
      <div class="auth-card">
        <h1 class="auth-title">Welcome back.</h1>
        <p class="auth-subtitle">Continue your adventure with Bucket.</p>

        <form @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label for="email">EMAIL ADDRESS</label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="name@domain.com"
              required
            />
          </div>

          <div class="form-group">
            <div class="label-row">
              <label for="password">PASSWORD</label>
              <a href="#" class="forgot-link">Forgot Password?</a>
            </div>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="••••••••"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary btn-block">
            Login
          </button>
        </form>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <p class="auth-footer">
          Don't have an account? <router-link to="/register">Sign Up</router-link>
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

const email = ref("")
const password = ref("")
const error = ref("")

async function handleLogin() {
  try {
    const res = await api.login({
      email: email.value,
      password: password.value
    })
    
    localStorage.setItem("token", res.access)
    // The MainLayout expects this token directly or re-evaluates.
    // If it doesn't instantly react, a reload or pinia store is better, 
    // but a router push to a protected route will work fine.
    router.push("/generator")
  } catch (err) {
    error.value = "Invalid credentials"
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6rem 1rem;
  /* subtle radial gradient */
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

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #1a202c;
  letter-spacing: 0.05em;
}

.forgot-link {
  font-size: 0.75rem;
  color: #00b5d8;
  font-weight: 600;
  text-decoration: none;
}

input {
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

.btn-block {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  margin-top: 1rem;
  border-radius: 12px;
}

.btn-primary {
  background-color: #00e5ff;
  color: #0f172a;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
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
