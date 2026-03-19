<template>
  <div class="login-container">
    <h2>Login</h2>

    <form @submit.prevent="handleLogin">
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

      <button type="submit">Login</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
    <p class="auth-link">
      New here?
      <router-link to="/register">Create an account</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../../services/api"

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

    router.push("/generator")
  } catch (err) {
    error.value = "Invalid credentials"
  }
}
</script>

<style>
.login-container {
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
