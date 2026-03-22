<template>
  <div class="products">

    <div class="page-header">
      <h1>Products</h1>
      <p>Summary and insights about the product catalogue</p>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else>

      <!-- Stat cards -->
      <div class="stats-grid">
        <StatCard
          label="Total products"
          :value="productsSummary.total"
          badge="In catalogue"
          badgeType="green"
        />
        <StatCard
          label="Avg. price"
          :value="`$${productsSummary.avg_price}`"
          badge="Per product"
          badgeType="green"
        />
        <StatCard
          label="Avg. rating"
          :value="productsSummary.avg_rating"
          badge="Out of 5"
          badgeType="green"
        />
        <StatCard
          label="Low stock"
          :value="productsSummary.low_stock.length"
          badge="Needs attention"
          badgeType="red"
        />
      </div>

      <!-- Gráficos por categoria -->
      <div class="row">
        <div class="card">
          <h3>Products by category</h3>
          <Bar :data="categoryCountData" :options="horizontalBarOptions" />
        </div>
        <div class="card">
          <h3>Avg. price by category</h3>
          <Bar :data="categoryPriceData" :options="horizontalBarOptions" />
        </div>
      </div>

      <!-- Insights -->
      <div class="row">
        <div class="card">
          <h3>Price vs. rating</h3>
          <Scatter :data="priceVsRatingData" :options="scatterOptions" />
        </div>
        <div class="card">
          <h3>Availability distribution</h3>
          <Doughnut :data="availabilityData" :options="doughnutOptions" />
        </div>
      </div>

      <!-- Tabela de produtos recentes -->
      <div class="card">
        <div class="card-header">
          <h3>Recent products</h3>
          <RouterLink to="/products/all" class="see-more">See all</RouterLink>
        </div>
        <DataTable :columns="productColumns" :data="productsSummary.recent_products" />
      </div>

    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Bar, Doughnut, Scatter } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'

import StatCard from '../../components/StatCard.vue'
import DataTable from '../../components/DataTable.vue'
import { useProducts } from '../../composables/useProducts'

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, ArcElement, Tooltip, Legend)

const { productsSummary, insights, loading, error } = useProducts()

const categoryCountData = computed(() => ({
  labels: (productsSummary.value?.by_category || []).map(c => c.category),
  datasets: [{
    label: 'Products',
    data: (productsSummary.value?.by_category || []).map(c => c.count),
    backgroundColor: '#378ADD',
    borderRadius: 6
  }]
}))

const categoryPriceData = computed(() => ({
  labels: (productsSummary.value?.by_category || []).map(c => c.category),
  datasets: [{
    label: 'Avg. price ($)',
    data: (productsSummary.value?.by_category || []).map(c => c.avg_price),
    backgroundColor: '#639922',
    borderRadius: 6
  }]
}))

const priceVsRatingData = computed(() => ({
  datasets: [{
    label: 'Products',
    data: (insights.value?.price_vs_rating || []).map(p => ({ x: p.price, y: p.rating })),
    backgroundColor: '#378ADD'
  }]
}))

const availabilityData = computed(() => ({
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

const horizontalBarOptions = {
  responsive: true,
  indexAxis: 'y',
  plugins: { legend: { display: false } },
  scales: {
    x: { beginAtZero: true, grid: { color: '#f3f4f6' } },
    y: { grid: { display: false } }
  }
}

const scatterOptions = {
  responsive: true,
  plugins: { legend: { display: false } },
  scales: {
    x: { title: { display: true, text: 'Price ($)' }, grid: { color: '#f3f4f6' } },
    y: { title: { display: true, text: 'Rating' }, min: 0, max: 5, grid: { color: '#f3f4f6' } }
  }
}

const doughnutOptions = {
  responsive: true,
  plugins: { legend: { position: 'bottom' } }
}

const productColumns = [
  { field: 'title', header: 'Product' },
  { field: 'category', header: 'Category' },
  { field: 'price', header: 'Price', prefix: '$' },
  { field: 'rating', header: 'Rating' },
  { field: 'availabilityStatus', header: 'Status' }
]
</script>

<style scoped>
.products {
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

  .row {
    grid-template-columns: 1fr;
  }
}
</style>