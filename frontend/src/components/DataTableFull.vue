<template>
  <div class="table-full-wrapper">

    <!-- Filtros e pesquisa -->
    <div class="toolbar">
      <div class="search-group">
        <input
          v-model="search"
          type="text"
          :placeholder="searchPlaceholder"
          class="search-input"
        />
      </div>
      <div class="filters-group">
        <select
          v-for="filter in filters"
          :key="filter.field"
          v-model="activeFilters[filter.field]"
          class="select-input"
        >
          <option value="">{{ filter.label }}</option>
          <option v-for="opt in filter.options" :key="opt" :value="opt">{{ opt }}</option>
        </select>
      </div>
    </div>

    <!-- Info e sort -->
    <div class="table-meta">
      <span class="total-info">
        Showing {{ firstItem }}–{{ lastItem }} of {{ filteredData.length }}
      </span>
      <div class="sort-group">
        <span class="sort-label">Sort by</span>
        <select v-model="sortField" class="select-input select-input--sm">
          <option value="">None</option>
          <option v-for="s in sortOptions" :key="s.field" :value="s.field">{{ s.label }}</option>
        </select>
        <button class="sort-dir-btn" @click="toggleSortDir" :title="sortDir === 'asc' ? 'Ascending' : 'Descending'">
          {{ sortDir === 'asc' ? '↑' : '↓' }}
        </button>
      </div>
    </div>

    <!-- Tabela -->
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th v-for="col in columns" :key="col.field">{{ col.header }}</th>
            <th v-if="detailRoute"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in paginatedData" :key="index">
            <td
              v-for="col in columns"
              :key="col.field"
              :class="{ muted: col.muted }"
            >
              <img
                v-if="col.type === 'image'"
                :src="row[col.field]"
                :alt="col.field"
                class="table-avatar"
              />
              <span v-else-if="col.field === 'availabilityStatus'">
                <span class="pill" :class="statusClass(row[col.field])">{{ row[col.field] }}</span>
              </span>
              <span v-else-if="col.type === 'stock'" :class="stockClass(row)">
                {{ row[col.field] }}
              </span>
              <span v-else-if="col.formatter">{{ col.formatter(row) }}</span>
              <span v-else>{{ col.prefix || '' }}{{ row[col.field] }}</span>
            </td>
            <td v-if="detailRoute">
              <RouterLink :to="`${detailRoute}/${row.id}`" class="detail-link">
                View <i class="pi pi-arrow-right" />
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginação -->
    <div class="pagination">
      <button class="page-btn" :disabled="currentPage === 1" @click="currentPage--">
        <i class="pi pi-chevron-left" />
      </button>
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button class="page-btn" :disabled="currentPage === totalPages" @click="currentPage++">
        <i class="pi pi-chevron-right" />
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  columns: Array,
  data: Array,
  filters: {
    type: Array,
    default: () => []
  },
  sortOptions: {
    type: Array,
    default: () => []
  },
  searchPlaceholder: {
    type: String,
    default: 'Search...'
  },
  searchFields: {
    type: Array,
    default: () => []
  },
  detailRoute: {
    type: String,
    default: null
  },
  pageSize: {
    type: Number,
    default: 10
  }
})

const search = ref('')
const currentPage = ref(1)
const sortField = ref('')
const sortDir = ref('asc')

const activeFilters = ref(
  Object.fromEntries(props.filters.map(f => [f.field, '']))
)

const toggleSortDir = () => {
  sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
}

// Reset página quando filtros ou pesquisa mudam
watch([search, activeFilters, sortField, sortDir], () => {
  currentPage.value = 1
}, { deep: true })

const filteredData = computed(() => {
  let result = [...(props.data || [])]

  // Pesquisa
  if (search.value) {
    const q = search.value.toLowerCase()
    result = result.filter(row =>
      props.searchFields.some(field => {
        const val = typeof field === 'function'
          ? field(row)
          : row[field]
        return String(val || '').toLowerCase().includes(q)
      })
    )
  }

  // Filtros
  props.filters.forEach(filter => {
    const val = activeFilters.value[filter.field]
    if (val) {
      result = result.filter(row => {
        const rowVal = filter.getValue ? filter.getValue(row) : row[filter.field]
        return rowVal === val
      })
    }
  })

  // Sort
  if (sortField.value) {
    result.sort((a, b) => {
      const sortOpt = props.sortOptions.find(s => s.field === sortField.value)
      const valA = sortOpt?.getValue ? sortOpt.getValue(a) : a[sortField.value]
      const valB = sortOpt?.getValue ? sortOpt.getValue(b) : b[sortField.value]
      if (valA < valB) return sortDir.value === 'asc' ? -1 : 1
      if (valA > valB) return sortDir.value === 'asc' ? 1 : -1
      return 0
    })
  }

  return result
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredData.value.length / props.pageSize))
)

const firstItem = computed(() =>
  filteredData.value.length === 0 ? 0 : (currentPage.value - 1) * props.pageSize + 1
)

const lastItem = computed(() =>
  Math.min(currentPage.value * props.pageSize, filteredData.value.length)
)

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * props.pageSize
  return filteredData.value.slice(start, start + props.pageSize)
})

const statusClass = (status) => {
  if (!status) return ''
  const s = status.toLowerCase()
  if (s.includes('low')) return 'pill-amber'
  if (s.includes('out')) return 'pill-red'
  return 'pill-green'
}

const stockClass = (row) => {
  if (row.stock < row.minimumOrderQuantity) return 'stock-red'
  if (row.stock < row.minimumOrderQuantity * 2) return 'stock-amber'
  return ''
}
</script>

<style scoped>
.table-full-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.toolbar {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
}

.search-group {
  flex: 1;
  min-width: 200px;
}

.filters-group {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.search-input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 0.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.85rem;
  font-family: inherit;
  color: #111827;
  outline: none;
}

.search-input:focus {
  border-color: #378ADD;
}

.select-input {
  padding: 0.5rem 0.6rem;
  border: 0.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.8rem;
  font-family: inherit;
  color: #111827;
  background: #ffffff;
  outline: none;
}

.select-input--sm {
  padding: 0.35rem 0.5rem;
  font-size: 0.75rem;
}

.select-input:focus {
  border-color: #378ADD;
}

.table-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.8rem;
}

.total-info {
  color: #6b7280;
}

.sort-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-label {
  font-size: 0.75rem;
  color: #6b7280;
}

.sort-dir-btn {
  background: none;
  border: 0.5px solid #e5e7eb;
  border-radius: 6px;
  padding: 4px 8px;
  font-size: 0.85rem;
  cursor: pointer;
  color: #374151;
}

.sort-dir-btn:hover {
  background: #f3f4f6;
}

.table-scroll {
  overflow-x: auto;
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
  padding: 0 12px 8px 0;
  border-bottom: 0.5px solid #e5e7eb;
}

td {
  padding: 10px 12px 10px 0;
  color: #111827;
  border-bottom: 0.5px solid #f3f4f6;
}

tr:last-child td {
  border-bottom: none;
}

td.muted {
  color: #6b7280;
}

.table-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.pill {
  display: inline-block;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 20px;
}

.pill-green { background: #f0fdf4; color: #15803d; }
.pill-amber { background: #fffbeb; color: #b45309; }
.pill-red   { background: #fef2f2; color: #b91c1c; }

.detail-link {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.8rem;
  color: #1d4ed8;
  text-decoration: none;
  white-space: nowrap;
}

.detail-link:hover {
  text-decoration: underline;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.page-btn {
  background: none;
  border: 0.5px solid #e5e7eb;
  border-radius: 6px;
  padding: 6px 10px;
  cursor: pointer;
  color: #374151;
  font-size: 0.8rem;
}

.page-btn:hover:not(:disabled) {
  background: #f3f4f6;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.8rem;
  color: #6b7280;
}

.stock-red { color: #b91c1c; font-weight: 500; }
.stock-amber { color: #b45309; font-weight: 500; }
</style>