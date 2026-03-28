<template>
  <div class="table-wrapper">

    <div class="controls">
      <div class="control-group">
        <label>Category</label>
        <select v-model="selectedCategory">
          <option value="">All</option>
          <option v-for="cat in availableCategories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
      <div class="control-group">
        <label>Brand</label>
        <select v-model="selectedBrand">
          <option value="">All</option>
          <option v-for="brand in availableBrands" :key="brand" :value="brand">{{ brand }}</option>
        </select>
      </div>
      <button v-if="isFiltered" class="clear-btn" @click="clearFilters">
        Clear filters
      </button>
    </div>

    <p class="count-info">{{ aggregated.count }} product{{ aggregated.count !== 1 ? 's' : '' }}</p>

    <table>
      <thead>
        <tr>
          <th>Metric</th>
          <th>Price ($)</th>
          <th>Stock</th>
          <th>Rating</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="metric-label">Min</td>
          <td>${{ aggregated.price?.min }}</td>
          <td>{{ aggregated.stock?.min }}</td>
          <td>{{ aggregated.rating?.min }}</td>
        </tr>
        <tr>
          <td class="metric-label">Max</td>
          <td>${{ aggregated.price?.max }}</td>
          <td>{{ aggregated.stock?.max }}</td>
          <td>{{ aggregated.rating?.max }}</td>
        </tr>
        <tr>
          <td class="metric-label">Avg</td>
          <td>${{ aggregated.price?.avg }}</td>
          <td>{{ aggregated.stock?.avg }}</td>
          <td>{{ aggregated.rating?.avg }}</td>
        </tr>
        <tr>
          <td class="metric-label">Median</td>
          <td>${{ aggregated.price?.median }}</td>
          <td>{{ aggregated.stock?.median }}</td>
          <td>{{ aggregated.rating?.median }}</td>
        </tr>
      </tbody>
    </table>

    <div class="inventory-value">
      <span class="inventory-label">Total inventory value</span>
      <span class="inventory-amount">${{ inventoryValue }}</span>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  aggregationData: Object
})

const selectedCategory = ref('')
const selectedBrand = ref('')

const isFiltered = computed(() => !!selectedCategory.value || !!selectedBrand.value)

const availableBrands = computed(() => {
  if (!props.aggregationData) return []
  if (selectedCategory.value) {
    return Object.keys(props.aggregationData.by_category_brand?.[selectedCategory.value] || {})
  }
  return props.aggregationData.filter_options.brands
})

const availableCategories = computed(() => {
  if (!props.aggregationData) return []
  if (selectedBrand.value) {
    return props.aggregationData.filter_options.categories.filter(cat =>
      props.aggregationData.by_category_brand?.[cat]?.[selectedBrand.value] !== undefined
    )
  }
  return props.aggregationData.filter_options.categories
})

// Reset brand se já não estiver disponível após mudar categoria
watch(selectedCategory, () => {
  if (selectedBrand.value && !availableBrands.value.includes(selectedBrand.value)) {
    selectedBrand.value = ''
  }
})

// Reset category se já não estiver disponível após mudar brand
watch(selectedBrand, () => {
  if (selectedCategory.value && !availableCategories.value.includes(selectedCategory.value)) {
    selectedCategory.value = ''
  }
})

const clearFilters = () => {
  selectedCategory.value = ''
  selectedBrand.value = ''
}

const aggregated = computed(() => {
  if (!props.aggregationData) return {}
  if (selectedCategory.value && selectedBrand.value) {
    return props.aggregationData.by_category_brand?.[selectedCategory.value]?.[selectedBrand.value] || {}
  }
  if (selectedCategory.value) return props.aggregationData.by_category[selectedCategory.value] || {}
  if (selectedBrand.value) return props.aggregationData.by_brand[selectedBrand.value] || {}
  return props.aggregationData.overall
})

const inventoryValue = computed(() => {
  if (!aggregated.value?.price?.total || !aggregated.value?.stock?.total) return '—'
  return (aggregated.value.price.avg * aggregated.value.stock.total).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
})
</script>

<style scoped>
.table-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.controls {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.control-group label {
  font-size: 11px;
  color: #6b7280;
  font-weight: 500;
}

select {
  padding: 0.4rem 0.6rem;
  border: 0.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.8rem;
  font-family: inherit;
  color: #111827;
  background: #ffffff;
  outline: none;
}

select:focus {
  border-color: #378ADD;
}

.count-info {
  font-size: 12px;
  color: #6b7280;
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

td.metric-label {
  font-weight: 500;
  color: #6b7280;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td.muted {
  color: #6b7280;
}

.clear-btn {
  align-self: flex-end;
  padding: 0.4rem 0.75rem;
  border: 0.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.8rem;
  font-family: inherit;
  color: #6b7280;
  background: #ffffff;
  cursor: pointer;
}

.clear-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

.inventory-value {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0 0 0;
  border-top: 0.5px solid #e5e7eb;
  font-size: 0.85rem;
  padding-right: 2rem;
}

.inventory-label {
  color: #6b7280;
  font-weight: 500;
}

.inventory-amount {
  color: #111827;
  font-weight: 500;
}
</style>