<template>
  <div class="register-container">
    <h2>Register</h2>

    <form @submit.prevent="handleRegister">
      <input
        v-model="username"
        type="text"
        placeholder="Username"
        required
      />

      <input
        v-model="email"
        type="email"
        placeholder="Email"
        required
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />

      <button type="submit" :disabled="loading">
        {{ loading ? "Creating account..." : "Register" }}
      </button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
    <p class="auth-link">
      Already have an account?
      <router-link to="/login">Go to login</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../../services/api"

const router = useRouter()

const username = ref("")
const email = ref("")
const password = ref("")
const loading = ref(false)
const error = ref("")

async function handleRegister() {
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

<style>
.register-container {
  max-width: 400px;
  margin: auto;
  padding: 60px;
}

.error {
  color: red;
}

.auth-link {
  margin-top: 12px;
}
</style>
