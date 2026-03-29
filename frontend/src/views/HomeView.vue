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
          @click="goToAttention"
          class="clickable"
        />
      </div>

      <!-- Chart1 e Chart2 -->
      <div class="row">
        <div class="card">
          <h3>Avg. review rating by user segment</h3>
          <UserReviewBarChart
            :userReviewData="usersInsights.user_review_data"
            :filterOptions="usersInsights.filter_options"
          />
        </div>
        <div class="card">
          <h3>Users by avg. review rating</h3>
          <UserReviewDoughnutChart
            :userReviewData="usersInsights.user_review_data"
            :noReviewCount="usersInsights.no_review_count"
            :totalUsers="usersInsights.total_users"
            :filterOptions="usersInsights.filter_options"
          />
        </div>
      </div>

      <!-- Table1 e Table2 -->
      <div class="row">
        <div class="card">
          <div class="card-content">
            <h3>Product aggregation</h3>
            <ProductAggregationTable
              :aggregationData="productsAggregation"
            />
          </div>
          <div class="card-footer">
            <RouterLink to="/products" class="explore-link">Explore products →</RouterLink>
          </div>
        </div>
        <div class="card">
          <div class="card-content">
            <h3>Average review by user segment aggregation</h3>
            <UserReviewAggregationTable
              :userReviewData="usersInsights.user_review_data"
            />
          </div>
          <div class="card-footer">
            <RouterLink to="/users" class="explore-link">Explore users →</RouterLink>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup>
import StatCard from '../components/StatCard.vue'
import UserReviewBarChart from '../components/charts/UserReviewBarChart.vue'
import UserReviewDoughnutChart from '../components/charts/UserReviewDoughnutChart.vue'
import ProductAggregationTable from '../components/tables/ProductAggregationTable.vue'
import UserReviewAggregationTable from '../components/tables/UserReviewAggregationTable.vue'
import { useHome } from '../composables/useHome'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToAttention = () => {
  router.push('/products/all?attention=true')
}

const { usersSummary, productsSummary, usersInsights, productsAggregation, loading, error } = useHome()
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

.card {
  background: #ffffff;
  border: 0.5px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: hidden;
}

.card h3 {
  font-size: 0.9rem;
  font-weight: 500;
  color: #111827;
}

.loading {
  color: #6b7280;
  font-size: 0.9rem;
}

.error {
  color: #b91c1c;
  font-size: 0.9rem;
}

.clickable {
  cursor: pointer;
  transition: opacity 0.15s;
}
.clickable:hover {
  opacity: 0.85;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 0.75rem;
  border-top: 0.5px solid #f3f4f6;
}

.explore-link {
  font-size: 0.8rem;
  color: #1d4ed8;
  text-decoration: none;
  padding: 6px 12px;
  border: 0.5px solid #e5e7eb;
  border-radius: 8px;
}

.explore-link:hover {
  background: #f3f4f6;
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