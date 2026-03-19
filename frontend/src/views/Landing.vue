<template>
  <div class="landing-page">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo">
        <span class="logo-icon">B</span>
        <span class="logo-text">Bucket</span>
      </div>
      <div class="nav-links">
        <a href="#how-it-works">How it works</a>
        <a href="#features">Features</a>
        <a href="#categories">Categories</a>
        
      </div>
      <div class="auth-buttons">
        <template v-if="isAuthenticated">
          <router-link to="/generator" class="btn btn-primary">Go to Generator</router-link>
          <button @click="logout" class="btn btn-outline">Logout</button>
        </template>
        <template v-else>
          <router-link to="/register" class="btn btn-primary">Sign Up</router-link>
          <router-link to="/login" class="btn btn-outline">Login</router-link>
        </template>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <div class="badge">AI-POWERED EXPLORATION</div>
        <h1>Your Next Adventure,<br><span class="highlight">Powered by AI</span></h1>
        <p>Bucket generates personalized scavenger hunts and bucket lists tailored to your location and interests. Stop dreaming, start doing.</p>
        <div class="hero-cta">
          <router-link to="/generator" class="btn btn-lg btn-primary">Start Your Adventure</router-link>
          <a href="#how-it-works" class="play-btn">
            <span class="play-icon">▶</span> See how it works
          </a>
        </div>
      </div>
      <div class="hero-image">
        <!-- Placeholder for hero image -->
        <div class="hero-image-placeholder">
          <!-- Two people looking at phone in city, visually -->
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how-it-works" class="how-it-works">
      <h2>How it works</h2>
      <p class="subtitle">These simple steps to start your epic journey</p>
      
      <div class="steps-grid">
        <div class="step-card">
          <div class="step-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg>
          </div>
          <h3>Define Your Vibe</h3>
          <p>Tell us what you like, your activity level, and your current location.</p>
        </div>
        <div class="step-card">
          <div class="step-icon">
             <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path><path d="M12 9v4"></path><path d="M12 17h.01"></path></svg>
          </div>
          <h3>AI Generates the Plan</h3>
          <p>Our AI crafts a unique scavenger hunt or list tailored just for you.</p>
        </div>
        <div class="step-card">
          <div class="step-icon">
             <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"></path><path d="M22 2 11 13"></path></svg>
          </div>
          <h3>Go Explore</h3>
          <p>Grab your phone, follow the clues, and start checking items off your list.</p>
        </div>
      </div>
    </section>

    <!-- Adventure Categories -->
    <section id="categories" class="categories-section">
      <div class="categories-header">
        <div>
          <h2>Adventure Categories</h2>
          <p>Choose your style and dive into curated experiences built for every type of explorer.</p>
        </div>
        <a href="#" class="view-all">View All Categories <span>→</span></a>
      </div>

      <div class="categories-grid">
        <div class="category-card urban">
          <div class="category-info">
            <h3>Urban Explorer</h3>
            <p>Hidden gems & city secrets</p>
          </div>
        </div>
        <div class="category-card nature">
          <div class="category-info">
            <h3>Nature Quest</h3>
            <p>Trails, parks & waterfalls</p>
          </div>
        </div>
        <div class="category-card foodie">
          <div class="category-info">
            <h3>Foodie Trail</h3>
            <p>Local flavors & secret eats</p>
          </div>
        </div>
        <div class="category-card photo">
          <div class="category-info">
            <h3>Photo Hunt</h3>
            <p>The most Instagrammable spots</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Why Bucket Section -->
    <section id="features" class="why-bucket">
      <h2>Why Bucket?</h2>
      <p class="subtitle">The ultimate tool for modern explorers and thrill-seekers.</p>

      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg>
          </div>
          <h3>Personalized AI</h3>
          <p>Tailored specifically to your physical ability, time constraints, and niche interests.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
             <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg>
          </div>
          <h3>Global Coverage</h3>
          <p>Works in over 150 countries with hyper-local insights you won't find in travel guides.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"></path><path d="M22 2 11 13"></path></svg>
          </div>
          <h3>Gamified Experience</h3>
          <p>Earn badges, level up your explorer status, and compete with friends globally.</p>
        </div>
      </div>
    </section>

    <!-- Bottom CTA -->
    <section class="bottom-cta">
      <div class="cta-card">
        <h2>Ready to find your<br>next favorite memory?</h2>
        <p>Join 50,000+ explorers already using Bucket to turn everyday outings into epic adventures.</p>
        <router-link to="/register" class="btn btn-lg btn-primary">Get Started for Free</router-link>
      </div>
    </section>

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
import { useRouter } from 'vue-router';

const router = useRouter();
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
.landing-page {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #1a202c;
  background-color: #f8fafc;
  line-height: 1.6;
}

h1, h2, h3, h4 {
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

.btn-lg {
  padding: 0.875rem 2rem;
  font-size: 1rem;
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

.auth-buttons {
  display: flex;
  gap: 0.5rem;
}

/* Hero Section */
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4rem 5% 6rem;
  gap: 4rem;
}

.hero-content {
  flex: 1;
  max-width: 600px;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background-color: #e6fffa;
  color: #00b5d8;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  margin-bottom: 1.5rem;
}

.hero h1 {
  font-size: 4.5rem;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}

.highlight {
  color: #00e5ff;
}

.hero p {
  font-size: 1.125rem;
  color: #64748b;
  margin-bottom: 2.5rem;
  max-width: 480px;
}

.hero-cta {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.play-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 0.875rem;
}

.play-icon {
  width: 24px;
  height: 24px;
  background-color: #0f172a;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.5rem;
}

.hero-image {
  flex: 1;
}

.hero-image-placeholder {
  width: 100%;
  height: 480px;
  background: linear-gradient(135deg, #cbd5e1, #94a3b8);
  border-radius: 24px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;
}

/* Sections Base */
section {
  padding: 6rem 5%;
}

.subtitle {
  color: #64748b;
  margin-top: 0.5rem;
  margin-bottom: 4rem;
  text-align: center;
}

section > h2 {
  text-align: center;
  font-size: 2.5rem;
}

/* How It Works & Why Bucket */
.how-it-works {
  background-color: #f1f5f9;
}

.steps-grid, .features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.step-card, .feature-card {
  background-color: white;
  padding: 3rem 2rem;
  border-radius: 24px;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.step-card:hover, .feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.step-icon, .feature-icon {
  width: 64px;
  height: 64px;
  background-color: #ecfeff;
  color: #00e5ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.step-card h3, .feature-card h3 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.step-card p, .feature-card p {
  color: #64748b;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* Categories */
.categories-section {
  background-color: #f8fafc;
}

.categories-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 3rem;
}

.categories-header h2 {
  text-align: left;
}

.categories-header p {
  color: #64748b;
  margin-top: 0.5rem;
  max-width: 500px;
}

.view-all {
  color: #06b6d4;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.category-card {
  height: 360px;
  border-radius: 20px;
  padding: 2rem;
  display: flex;
  align-items: flex-end;
  color: white;
  background-size: cover;
  background-position: center;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.category-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 60%);
}

.category-card:hover {
  transform: scale(1.02);
}

.category-info {
  position: relative;
  z-index: 1;
}

.category-info h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: white;
}

.category-info p {
  font-size: 0.875rem;
  opacity: 0.9;
  margin: 0;
  color: #f8fafc;
}

/* Specific Category Backgrounds - Placeholder Gradients */
.urban { background: linear-gradient(to bottom right, #0f172a, #3b82f6); }
.nature { background: linear-gradient(to bottom right, #14532d, #22c55e); }
.foodie { background: linear-gradient(to bottom right, #78350f, #f59e0b); }
.photo { background: linear-gradient(to bottom right, #4a044e, #d946ef); }

/* Bottom CTA */
.bottom-cta {
  padding: 4rem 5% 8rem;
  background-color: #f1f5f9;
}

.cta-card {
  background-color: #0f172a; 
  border-radius: 32px;
  padding: 6rem 2rem;
  text-align: center;
  color: white;
}

.cta-card h2 {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  color: white;
}

.cta-card p {
  color: #94a3b8;
  margin-bottom: 3rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  font-size: 1.125rem;
}

/* Footer */
.footer {
  padding: 4rem 5% 2rem;
  background-color: #f8fafc;
  border-top: 1px solid #e2e8f0;
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
@media (max-width: 1024px) {
  .hero {
    flex-direction: column;
    text-align: center;
    padding-top: 2rem;
    gap: 3rem;
  }
  
  .hero-content {
    max-width: 100%;
  }
  
  .hero p {
    margin: 0 auto 2.5rem;
  }
  
  .hero-cta {
    justify-content: center;
  }
  
  .categories-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .steps-grid, .features-grid {
    grid-template-columns: 1fr;
  }
  
  .nav-links {
    display: none;
  }
  
  .hero h1 {
    font-size: 3rem;
  }
  
  .categories-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 3rem;
  }
  
  .footer-links {
    flex-wrap: wrap;
    gap: 3rem;
  }
  
  .cta-card {
    padding: 4rem 2rem;
  }
  
  .cta-card h2 {
    font-size: 2.5rem;
  }
}

@media (max-width: 480px) {
  .categories-grid {
    grid-template-columns: 1fr;
  }
  
  .cta-card h2 {
    font-size: 2rem;
  }
  
  .hero h1 {
    font-size: 2.5rem;
  }
}
</style>
