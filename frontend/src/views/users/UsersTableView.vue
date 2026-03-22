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
        <div class="card-header">
          <span class="total">{{ filteredUsers.length }} users</span>
          <input
            v-model="search"
            type="text"
            placeholder="Search by name, email or role..."
            class="search-input"
          />
        </div>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Company</th>
              <th>Department</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id">
              <td>{{ user.firstName }} {{ user.lastName }}</td>
              <td class="muted">{{ user.email }}</td>
              <td><span class="pill pill-blue">{{ user.role }}</span></td>
              <td>{{ user.company?.name }}</td>
              <td class="muted">{{ user.company?.department }}</td>
              <td>
                <RouterLink :to="`/users/${user.id}`" class="detail-link">
                  View <i class="pi pi-arrow-right" />
                </RouterLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUsers } from '../../composables/useUsers'

const { users, loading, error } = useUsers()

const search = ref('')

const filteredUsers = computed(() => {
  if (!search.value) return users.value
  const q = search.value.toLowerCase()
  return users.value.filter(u =>
    `${u.firstName} ${u.lastName}`.toLowerCase().includes(q) ||
    u.email.toLowerCase().includes(q) ||
    u.role.toLowerCase().includes(q)
  )
})
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
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow-x: auto;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.total {
  font-size: 0.85rem;
  color: #6b7280;
  white-space: nowrap;
}

.search-input {
  padding: 0.5rem 0.75rem;
  border: 0.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.85rem;
  font-family: inherit;
  color: #111827;
  outline: none;
  width: 280px;
}

.search-input:focus {
  border-color: #378ADD;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

th {
  text-align: left;
  font-size: 0.75rem;
  font-weight: 500;
  color: #6b7280;
  padding: 0 0 8px 0;
  border-bottom: 0.5px solid #e5e7eb;
}

td {
  padding: 10px 0;
  color: #111827;
  border-bottom: 0.5px solid #f3f4f6;
}

tr:last-child td {
  border-bottom: none;
}

td.muted {
  color: #6b7280;
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

.detail-link {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.8rem;
  color: #1d4ed8;
  text-decoration: none;
  justify-content: flex-end;
}

.detail-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .search-input {
    width: 100%;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>