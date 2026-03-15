<template>
  <div class="history-page">
    <h2>Bucket History</h2>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="bucket in history" :key="bucket.bucket_id" class="bucket-card">
        <h3>{{ bucket.name }} - {{ bucket.location }}</h3>
        <p>Budget: {{ bucket.budget }}, Group: {{ bucket.group_type }}</p>
        <ul>
          <li v-for="item in bucket.items" :key="item.title">{{ item.title }}</li>
        </ul>
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
      loading: true
    };
  },
  async created() {
    try {
      const res = await api.getHistory();
      this.history = res;
    } catch (err) {
      console.error("Failed to load history", err);
    } finally {
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.bucket-card {
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
}
</style>