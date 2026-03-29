<template>
  <div class="users-table">

    <div class="page-header">
      <div>
        <h1>All users</h1>
        <p>Complete list of users</p>
      </div>
      <RouterLink to="/users" class="back-link">
        <i class="pi pi-arrow-left" /> Back to summary
      </RouterLink>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else>
      <div class="card">
        <DataTableFull
          :columns="userColumns"
          :data="users"
          :filters="userFilters"
          :sortOptions="sortOptions"
          :searchFields="searchFields"
          searchPlaceholder="Search by name, email or job title..."
          detailRoute="/users"
          :pageSize="10"
        />
      </div>
    </template>

  </div>
</template>

<script setup>
import { computed } from 'vue'
import DataTableFull from '../../components/DataTableFull.vue'
import { useUsers } from '../../composables/useUsers'

const { users, loading, error } = useUsers()

const userColumns = [
  { field: 'image', header: '', type: 'image' },
  { field: 'firstName', header: 'Name', formatter: (row) => `${row.firstName} ${row.lastName}` },
  { field: 'email', header: 'Email', muted: true },
  { field: 'gender', header: 'Gender', formatter: (row) => row.gender === 'male' ? 'M' : 'F' },
  { field: 'age', header: 'Age', muted: true },
  { field: 'address', header: 'Location', formatter: (row) => `${row.address.city}, ${row.address.state}` },
  { field: 'company', header: 'Job title', formatter: (row) => row.company.title, muted: true},
  { field: 'role', header: 'Role' }
]

const userFilters = computed(() => {
  if (!users.value?.length) return []

  const unique = (fn) => [...new Set(users.value.map(fn))].sort()

  return [
    {
      field: 'role',
      label: 'Role',
      options: unique(u => u.role)
    },
    {
      field: 'gender',
      label: 'Gender',
      options: unique(u => u.gender)
    },
    {
      field: 'state',
      label: 'State',
      options: unique(u => u.address.state),
      getValue: (row) => row.address.state
    },
    {
      field: 'city',
      label: 'City',
      options: unique(u => u.address.city),
      getValue: (row) => row.address.city
    },
    {
      field: 'age_range',
      label: 'Age range',
      options: ['18-25', '26-30', '31-35', '36-40', '40+'],
      getValue: (row) => {
        if (row.age <= 25) return '18-25'
        if (row.age <= 30) return '26-30'
        if (row.age <= 35) return '31-35'
        if (row.age <= 40) return '36-40'
        return '40+'
      }
    }
  ]
})

const sortOptions = [
  { field: 'name', label: 'Name', getValue: (row) => `${row.firstName} ${row.lastName}` },
  { field: 'age', label: 'Age', getValue: (row) => row.age }
]

const searchFields = [
  (row) => `${row.firstName} ${row.lastName}`,
  'email',
  (row) => row.company.title
]
</script>

<style scoped>
.users-table {
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

.card {
  background: #ffffff;
  border: 0.5px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
}

.loading {
  color: #6b7280;
  font-size: 0.9rem;
}

.error {
  color: #b91c1c;
  font-size: 0.9rem;
}


</style>