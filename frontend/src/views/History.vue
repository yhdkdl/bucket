<template>
  <div class="history-page">
    <h2>Bucket History</h2>
    <div v-if="loading" class="loading">Loading your adventures…</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-for="bucket in history" :key="bucket.bucket_id" class="bucket-card">
        <div class="card-header">
          <h3>{{ bucket.name }}</h3>
          <p class="location">{{ bucket.location }}</p>
          <p class="date">Created: {{ formatDate(bucket.created_at) }}</p>
        </div>
        
        <div class="progress-section">
          <label>Progress: {{ progressPercent(bucket) }}%</label>
          <progress :value="completedCount(bucket)" :max="bucket.items.length"></progress>
        </div>
        
        <div v-if="bucket.has_collage" class="thumbnail">
          <img v-if="thumbnails[bucket.bucket_id]" :src="thumbnails[bucket.bucket_id]" alt="Collage thumbnail" />
        </div>
        
        <router-link :to="`/bucket/${bucket.bucket_id}`" class="view-button">
          View Bucket
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  name: "History",
  data() {
    return {
      history: [],
      thumbnails: {},
      loading: true,
      error: null
    };
  },
  async created() {
    try {
      const res = await api.getHistory();
      this.history = res;
      await this.loadThumbnails();
    } catch (err) {
      if (err.message === "Unauthorized") {
        localStorage.removeItem("token")
        this.$router.push("/login")
        return
      }
      console.error("Failed to load history", err);
      this.error = "Failed to load history. Please try refreshing the page.";
    } finally {
      this.loading = false;
    }
  },
  beforeUnmount() {
    Object.values(this.thumbnails).forEach((url) => {
      URL.revokeObjectURL(url);
    });
  },
  methods: {
    async loadThumbnails() {
      const entries = await Promise.all(this.history.map(async (bucket) => {
        if (!bucket.has_collage) {
          return [bucket.bucket_id, null];
        }

        try {
          const blob = await api.generateCollage(bucket.bucket_id, "horizontal", { size: "small", preview: true });
          return [bucket.bucket_id, URL.createObjectURL(blob)];
        } catch (_err) {
          return [bucket.bucket_id, null];
        }
      }));

      this.thumbnails = Object.fromEntries(entries.filter(([, url]) => Boolean(url)));
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },
    completedCount(bucket) {
      return bucket.items.filter(item => item.completed).length;
    },
    progressPercent(bucket) {
      const completed = this.completedCount(bucket);
      const total = bucket.items.length;
      return total > 0 ? Math.round((completed / total) * 100) : 0;
    }
  }
};
</script>

<style scoped>
.history-page {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.bucket-card {
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.card-header h3 {
  margin: 0;
  font-size: 1.2em;
}

.location {
  color: #666;
  font-weight: bold;
}

.date {
  color: #999;
  font-size: 0.9em;
}

.progress-section {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.thumbnail {
  text-align: center;
}

.thumbnail img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.view-button {
  align-self: flex-start;
  padding: 8px 16px;
  background: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background 0.2s;
}

.view-button:hover {
  background: #0056b3;
}

.loading {
  color: #007bff;
  font-style: italic;
  text-align: center;
  padding: 20px;
}

.error {
  color: #dc3545;
  font-weight: bold;
  text-align: center;
  padding: 20px;
}
</style>
