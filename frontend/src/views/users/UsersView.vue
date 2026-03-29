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
          label="Users with avg. rating ≥ 4"
          :value="`${highRatingPct}%`"
          badge="Of users with reviews"
          badgeType="green"
        />
        <StatCard
          label="Avg. age"
          :value="avgAge"
          badge="Years old"
          badgeType="green"
        />
      </div>

      <!-- Map and segment chart -->
      <div class="row">
        <div class="card card--wide">
          <h3>User distribution by location</h3>
          <UsersGeoMap :geoData="usersGeo" />
        </div>
        <div class="card">
          <h3>Users by segment</h3>
          <UsersSegmentChart :usersSummary="usersSummary" />
        </div>
      </div>

      <!-- Recent users table -->
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
import StatCard from '../../components/StatCard.vue'
import DataTable from '../../components/DataTable.vue'
import UsersGeoMap from '../../components/charts/UsersGeoMap.vue'
import UsersSegmentChart from '../../components/charts/UsersSegmentChart.vue'
import { useUsers } from '../../composables/useUsers'

const { usersSummary, usersGeo, loading, error } = useUsers()

const avgAge = computed(() => {
  if (!usersSummary.value?.age_groups) return 0
  const groups = { '18-25': 21, '26-30': 28, '31-35': 33, '36-40': 38, '40+': 47 }
  const total = Object.values(usersSummary.value.age_groups).reduce((a, b) => a + b, 0)
  const weighted = Object.entries(usersSummary.value.age_groups)
    .reduce((sum, [key, val]) => sum + (groups[key] * val), 0)
  return (weighted / total).toFixed(1)
})

const highRatingPct = computed(() => {
  if (!usersSummary.value?.high_rating_pct) return 0
  return usersSummary.value.high_rating_pct
})

const userColumns = [
  { field: 'image', header: '', type: 'image' },
  { field: 'firstName', header: 'Name', formatter: (row) => `${row.firstName} ${row.lastName}` },
  { field: 'email', header: 'Email', muted: true },
  { field: 'gender', header: 'Gender', formatter: (row) => row.gender === 'male' ? 'M' : 'F' },
  { field: 'age', header: 'Age', muted: true },
  { field: 'address', header: 'Location', formatter: (row) => `${row.address.city}, ${row.address.state}` },
  { field: 'role', header: 'Role', muted: true }
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
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.row {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
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

  .card {
    padding: 1rem;
    overflow: hidden;
  }
}

</style>