<template>
  <div class="user-detail">

    <div class="page-header">
      <div>
        <h1 v-if="user">{{ user.firstName }} {{ user.lastName }}</h1>
        <p v-if="user">{{ user.company?.title }} · {{ user.company?.name }}</p>
      </div>
      <RouterLink to="/users/all" class="back-link">
        <i class="pi pi-arrow-left" /> Back to users
      </RouterLink>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else-if="user">

      <div class="row">

        <!-- Informação pessoal -->
        <div class="card">
          <h3>Personal info</h3>
          <div class="info-list">
            <div class="info-row">
              <span class="info-label">Age</span>
              <span class="info-value">{{ user.age }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Gender</span>
              <span class="info-value">{{ user.gender }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Birth date</span>
              <span class="info-value">{{ user.birthDate }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Email</span>
              <span class="info-value">{{ user.email }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">University</span>
              <span class="info-value">{{ user.university }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Role</span>
              <span class="info-value">
                <span class="pill pill-blue">{{ user.role }}</span>
              </span>
            </div>
          </div>
        </div>

        <!-- Localização -->
        <div class="card">
          <h3>Location</h3>
          <div class="info-list">
            <div class="info-row">
              <span class="info-label">City</span>
              <span class="info-value">{{ user.address?.city }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">State</span>
              <span class="info-value">{{ user.address?.state }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Country</span>
              <span class="info-value">{{ user.address?.country }}</span>
            </div>
          </div>
        </div>

      </div>

      <div class="row">

        <!-- Empresa -->
        <div class="card">
          <h3>Company</h3>
          <div class="info-list">
            <div class="info-row">
              <span class="info-label">Name</span>
              <span class="info-value">{{ user.company?.name }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Department</span>
              <span class="info-value">{{ user.company?.department }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Title</span>
              <span class="info-value">{{ user.company?.title }}</span>
            </div>
          </div>
        </div>

      </div>

    </template>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getUser } from '../../services/api'

const route = useRoute()
const user = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await getUser(route.params.id)
    user.value = res.data
  } catch (e) {
    error.value = 'Failed to load user'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.user-detail {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-header h1 {
  font-size: 1.4rem;
  font-weight: 500;
  color: #111827;
}

.page-header p {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 2px;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: #1d4ed8;
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}

.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.card {
  background: #ffffff;
  border: 0.5px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card h3 {
  font-size: 0.9rem;
  font-weight: 500;
  color: #111827;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 0.5px solid #f3f4f6;
  font-size: 0.85rem;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  color: #6b7280;
}

.info-value {
  color: #111827;
  text-align: right;
}

.pill {
  display: inline-block;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 20px;
}

.pill-blue {
  background: #eff6ff;
  color: #1d4ed8;
}

@media (max-width: 768px) {
  .row {
    grid-template-columns: 1fr;
  }
}
</style>