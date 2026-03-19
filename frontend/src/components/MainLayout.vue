<template>
  <div class="main-layout">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo">
        <router-link to="/" class="logo-link">
          <span class="logo-icon">B</span>
          <span class="logo-text">Bucket</span>
        </router-link>
      </div>
      <div class="nav-links">
        <a href="/#how-it-works">How it works</a>
        <a href="/#features">Features</a>
        <a href="/#categories">Categories</a>
      </div>
      <div class="auth-buttons">
        <template v-if="isAuthenticated">
          <router-link to="/history" class="history-link">My History</router-link>
          <router-link to="/generator" class="btn btn-primary">Go to Generator</router-link>
          <button @click="logout" class="btn btn-outline">Logout</button>
        </template>
        <template v-else>
          <router-link to="/login" class="btn btn-outline" style="margin-right: 0.5rem;">Login</router-link>
          <router-link to="/register" class="btn btn-primary">Sign Up</router-link>
        </template>
      </div>
    </nav>

    <!-- Page Content Slot -->
    <main class="main-content">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-brand">
          <div class="logo">
            <span class="logo-icon">B</span>
            <span class="logo-text">Bucket</span>
          </div>
          <p class="footer-p">AI-generated adventures for the modern explorer. Discover new favorites in exploring the world.</p>
        </div>
        <div class="footer-links">
          <div class="link-column">
            <h4>Company</h4>
            <a href="#">About Us</a>
            <a href="#">Careers</a>
            <a href="#">Contact</a>
          </div>
          <div class="link-column">
            <h4>Legal</h4>
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Bucket Technologies Inc. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const isAuthenticated = ref(false);

onMounted(() => {
  const token = localStorage.getItem('token');
  if (token) {
    isAuthenticated.value = true;
  }
});

const logout = () => {
  localStorage.removeItem('token');
  isAuthenticated.value = false;
  router.push('/login');
};
</script>

<style scoped>
/* Base Styles */
.main-layout {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #1a202c;
  background-color: #f8fafc;
  line-height: 1.6;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
}

h4 {
  font-weight: 800;
  line-height: 1.2;
  margin: 0;
  color: #0f172a;
}

a {
  text-decoration: none;
  color: inherit;
  transition: color 0.2s;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1.25rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-primary {
  background-color: #00e5ff;
  color: #0f172a;
}
.btn-primary:hover {
  background-color: #00c6dd;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 229, 255, 0.2);
}

.btn-outline {
  background-color: transparent;
  color: #4a5568;
  border: 1px solid transparent;
}
.btn-outline:hover {
  background-color: #edf2f7;
}

/* Navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 5%;
  background-color: #f8fafc;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 800;
  font-size: 1.25rem;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo-icon {
  background-color: #00e5ff;
  color: #0f172a;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 2rem;
  font-weight: 600;
  font-size: 0.875rem;
  color: #64748b;
}

.nav-links a:hover {
  color: #0f172a;
}

.history-link {
  margin-right: 1.5rem;
  font-weight: 600;
  font-size: 0.875rem;
  color: #64748b;
  display: flex;
  align-items: center;
}
.history-link:hover {
  color: #0f172a;
}

.auth-buttons {
  display: flex;
  align-items: center;
}

/* Footer */
.footer {
  padding: 4rem 5% 2rem;
  background-color: #f8fafc;
  border-top: 1px solid #e2e8f0;
  margin-top: auto;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4rem;
}

.footer-brand {
  max-width: 300px;
}

.footer-brand .logo {
  margin-bottom: 1.5rem;
}

.footer-p {
  color: #64748b;
  font-size: 0.95rem;
  line-height: 1.5;
}

.footer-links {
  display: flex;
  gap: 6rem;
}

.link-column h4 {
  font-size: 1rem;
  margin-bottom: 1.5rem;
  color: #0f172a;
}

.link-column a {
  display: block;
  color: #64748b;
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

.link-column a:hover {
  color: #0f172a;
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid #e2e8f0;
  color: #94a3b8;
  font-size: 0.875rem;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-links {
    display: none;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 3rem;
  }
  
  .footer-links {
    flex-wrap: wrap;
    gap: 3rem;
  }
}
</style>
