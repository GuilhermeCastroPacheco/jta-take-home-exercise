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

      <!-- Chart1 e Chart2 -->
      <div class="row">
        <div class="card">
          <h3>Product aggregation</h3>
          <ProductAggregationTable :aggregationData="productsAggregation" />
        </div>
        <div class="card">
          <h3>Top / bottom products</h3>
          <ProductTopBarChart
            :products="products"
            :filterOptions="productsAggregation.filter_options"
          />
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
import StatCard from '../../components/StatCard.vue'
import DataTable from '../../components/DataTable.vue'
import ProductAggregationTable from '../../components/tables/ProductAggregationTable.vue'
import ProductTopBarChart from '../../components/charts/ProductTopBarChart.vue'
import { useProducts } from '../../composables/useProducts'

const { productsSummary, products, productsAggregation, loading, error } = useProducts()

const productColumns = [
  { field: 'thumbnail', header: '', type: 'image' },
  { field: 'title', header: 'Product' },
  { field: 'category', header: 'Category', muted: true },
  { field: 'brand', header: 'Brand', formatter: (row) => row.brand || '—' },
  { field: 'price', header: 'Price', muted: true, prefix: '$' },
  { field: 'rating', header: 'Rating' },
  { field: 'availabilityStatus', header: 'Status', muted: true }
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
  grid-template-columns: repeat(3, minmax(0, 1fr));
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