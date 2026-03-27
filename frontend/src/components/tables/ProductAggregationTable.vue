<template>
  <div class="table-wrapper">

    <div class="controls">
      <div class="control-group">
        <label>Filter by</label>
        <select v-model="filterType">
          <option value="overall">Overall</option>
          <option value="category">Category</option>
          <option value="brand">Brand</option>
          <option value="tag">Tag</option>
        </select>
      </div>
      <div class="control-group" v-if="filterType !== 'overall'">
        <label>{{ filterTypeLabel }}</label>
        <select v-model="filterValue">
          <option value="">All</option>
          <option v-for="opt in currentOptions" :key="opt" :value="opt">{{ opt }}</option>
        </select>
      </div>
    </div>

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
          <td class="metric-label">Count</td>
          <td>{{ aggregated.count }}</td>
          <td>{{ aggregated.count }}</td>
          <td>{{ aggregated.count }}</td>
        </tr>
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
      </tbody>
    </table>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  aggregationData: Object
})

const filterType = ref('overall')
const filterValue = ref('')

const filterTypeLabel = computed(() => {
  if (filterType.value === 'category') return 'Category'
  if (filterType.value === 'brand') return 'Brand'
  if (filterType.value === 'tag') return 'Tag'
  return ''
})

const currentOptions = computed(() => {
  if (!props.aggregationData) return []
  if (filterType.value === 'category') return props.aggregationData.filter_options.categories
  if (filterType.value === 'brand') return props.aggregationData.filter_options.brands
  if (filterType.value === 'tag') return props.aggregationData.filter_options.tags
  return []
})

const aggregated = computed(() => {
  if (!props.aggregationData) return {}
  if (filterType.value === 'overall') return props.aggregationData.overall

  const map = {
    category: 'by_category',
    brand: 'by_brand',
    tag: 'by_tag'
  }

  const key = map[filterType.value]
  if (!filterValue.value) return props.aggregationData.overall
  return props.aggregationData[key][filterValue.value] || {}
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
</style>