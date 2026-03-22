<template>
  <div class="home">

    <div class="page-header">
      <h1>Dashboard</h1>
      <p>Overview of users and products</p>
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
          label="Total products"
          :value="productsSummary.total"
          badge="In catalogue"
          badgeType="green"
        />
        <StatCard
          label="Avg. product rating"
          :value="productsSummary.avg_rating"
          badge="Out of 5"
          badgeType="green"
        />
        <StatCard
          label="Low stock products"
          :value="productsSummary.low_stock.length"
          badge="Needs attention"
          badgeType="red"
        />
      </div>

      <!-- Gráficos de users -->
      <div class="row">
        <div class="card">
          <h3>Users by age group</h3>
          <Bar :data="ageChartData" :options="barOptions" />
        </div>
        <div class="card">
          <h3>Gender distribution</h3>
          <Doughnut :data="genderChartData" :options="doughnutOptions" />
        </div>
      </div>

      <!-- Tabela de produtos recentes + disponibilidade -->
      <div class="row row--asymmetric">
        <div class="card">
          <div class="card-header">
            <h3>Recent products</h3>
            <RouterLink to="/products/all" class="see-more">See all</RouterLink>
          </div>
          <DataTable :columns="productColumns" :data="productsSummary.recent_products" />
        </div>
        <div class="card">
          <h3>Availability</h3>
          <Doughnut :data="availabilityChartData" :options="doughnutOptions" />
        </div>
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

import StatCard from '../components/StatCard.vue'
import DataTable from '../components/DataTable.vue'
import { useHome } from '../composables/useHome'

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend)

const { usersSummary, productsSummary, loading, error } = useHome()

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

const availabilityChartData = computed(() => ({
  labels: Object.keys(productsSummary.value?.availability_distribution || {}),
  datasets: [{
    data: Object.values(productsSummary.value?.availability_distribution || {}),
    backgroundColor: ['#639922', '#BA7517', '#E24B4A']
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

const doughnutOptions = {
  responsive: true,
  plugins: { legend: { position: 'bottom' } }
}

const productColumns = [
  { field: 'title', header: 'Product' },
  { field: 'price', header: 'Price', prefix: '$' },
  { field: 'availabilityStatus', header: 'Status' }
]
</script>

<style scoped>
.home {
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