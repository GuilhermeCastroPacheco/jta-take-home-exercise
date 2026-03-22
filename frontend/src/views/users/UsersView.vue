<template>
  <div class="users">

    <div class="page-header">
      <h1>Users</h1>
      <p>Summary and insights about the user base</p>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else>

      <!-- Stat cards -->
      <div class="stats-grid">
        <StatCard
          label="Total users"
          :value="usersSummary.total"
          badge="Active"
          badgeType="green"
        />
        <StatCard
          label="Male"
          :value="usersSummary.gender_distribution.male"
          badge="Users"
          badgeType="green"
        />
        <StatCard
          label="Female"
          :value="usersSummary.gender_distribution.female"
          badge="Users"
          badgeType="green"
        />
        <StatCard
          label="Avg. age"
          :value="avgAge"
          badge="Years old"
          badgeType="green"
        />
      </div>

      <!-- Gráficos -->
      <div class="row">
        <div class="card">
          <h3>Users by age group</h3>
          <Bar :data="ageChartData" :options="barOptions" />
        </div>
        <div class="card">
          <h3>Users by role</h3>
          <Doughnut :data="roleChartData" :options="doughnutOptions" />
        </div>
      </div>

      <!-- Top companies -->
      <div class="row row--asymmetric">
        <div class="card">
          <h3>Top companies</h3>
          <Bar :data="companiesChartData" :options="horizontalBarOptions" />
        </div>
        <div class="card">
          <h3>Gender distribution</h3>
          <Doughnut :data="genderChartData" :options="doughnutOptions" />
        </div>
      </div>

      <!-- Tabela de utilizadores recentes -->
      <div class="card">
        <div class="card-header">
          <h3>Recent users</h3>
          <RouterLink to="/users/all" class="see-more">See all</RouterLink>
        </div>
        <DataTable :columns="userColumns" :data="usersSummary.recent_users" />
      </div>

    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Bar, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'

import StatCard from '../../components/StatCard.vue'
import DataTable from '../../components/DataTable.vue'
import { useUsers } from '../../composables/useUsers'

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend)

const { usersSummary, loading, error } = useUsers()

const avgAge = computed(() => {
  if (!usersSummary.value?.age_groups) return 0
  const groups = { '18-25': 21, '26-35': 30, '36-50': 43, '50+': 57 }
  const total = Object.values(usersSummary.value.age_groups).reduce((a, b) => a + b, 0)
  const weighted = Object.entries(usersSummary.value.age_groups)
    .reduce((sum, [key, val]) => sum + (groups[key] * val), 0)
  return (weighted / total).toFixed(1)
})

const ageChartData = computed(() => ({
  labels: Object.keys(usersSummary.value?.age_groups || {}),
  datasets: [{
    label: 'Users',
    data: Object.values(usersSummary.value?.age_groups || {}),
    backgroundColor: '#378ADD',
    borderRadius: 6
  }]
}))

const genderChartData = computed(() => ({
  labels: Object.keys(usersSummary.value?.gender_distribution || {}),
  datasets: [{
    data: Object.values(usersSummary.value?.gender_distribution || {}),
    backgroundColor: ['#378ADD', '#D4537E']
  }]
}))

const roleChartData = computed(() => ({
  labels: Object.keys(usersSummary.value?.role_distribution || {}),
  datasets: [{
    data: Object.values(usersSummary.value?.role_distribution || {}),
    backgroundColor: ['#378ADD', '#639922', '#BA7517', '#D4537E']
  }]
}))

const companiesChartData = computed(() => ({
  labels: (usersSummary.value?.top_companies || []).map(c => c.name),
  datasets: [{
    label: 'Users',
    data: (usersSummary.value?.top_companies || []).map(c => c.count),
    backgroundColor: '#378ADD',
    borderRadius: 6
  }]
}))

const barOptions = {
  responsive: true,
  plugins: { legend: { display: false } },
  scales: {
    y: { beginAtZero: true, grid: { color: '#f3f4f6' } },
    x: { grid: { display: false } }
  }
}

const horizontalBarOptions = {
  responsive: true,
  indexAxis: 'y',
  plugins: { legend: { display: false } },
  scales: {
    x: { beginAtZero: true, grid: { color: '#f3f4f6' } },
    y: { grid: { display: false } }
  }
}

const doughnutOptions = {
  responsive: true,
  plugins: { legend: { position: 'bottom' } }
}

const userColumns = [
  { field: 'firstName', header: 'First name' },
  { field: 'lastName', header: 'Last name' },
  { field: 'email', header: 'Email' },
  { field: 'role', header: 'Role' },
  { field: 'company', header: 'Company' }
]
</script>

<style scoped>
.users {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.row--asymmetric {
  grid-template-columns: 1.5fr 1fr;
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

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.see-more {
  font-size: 0.8rem;
  color: #1d4ed8;
  text-decoration: none;
}

.see-more:hover {
  text-decoration: underline;
}

.loading {
  color: #6b7280;
  font-size: 0.9rem;
}

.error {
  color: #b91c1c;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .row, .row--asymmetric {
    grid-template-columns: 1fr;
  }
}
</style>