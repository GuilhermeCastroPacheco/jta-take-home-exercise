<template>
  <div class="chart-wrapper">

    <div class="controls">
      <div class="control-group">
        <label>Show</label>
        <select v-model="selectedDirection">
          <option value="top">Top 5</option>
          <option value="bottom">Bottom 5</option>
        </select>
      </div>
      <div class="control-group">
        <label>By</label>
        <select v-model="selectedMetric">
          <option value="price">Price</option>
          <option value="rating">Rating</option>
          <option value="stock">Stock</option>
        </select>
      </div>
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

    <p v-if="filteredProducts.length === 0" class="no-results">
      No products match the selected filters.
    </p>

    <Bar v-else :data="chartData" :options="chartOptions" />

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

const props = defineProps({
  products: Array,
  filterOptions: Object
})

const selectedDirection = ref('top')
const selectedMetric = ref('price')
const selectedCategory = ref('')
const selectedBrand = ref('')

const COLORS = {
  price: '#378ADD',
  rating: '#639922',
  stock: '#BA7517'
}

const PREFIXES = {
  price: '$',
  rating: '',
  stock: ''
}

const isFiltered = computed(() => !!selectedCategory.value || !!selectedBrand.value)

const filteredProducts = computed(() => {
  return (props.products || []).filter(p => {
    const matchCategory = !selectedCategory.value || p.category === selectedCategory.value
    const matchBrand = !selectedBrand.value || p.brand === selectedBrand.value
    return matchCategory && matchBrand
  })
})

const availableBrands = computed(() => {
  if (!props.products) return []
  if (selectedCategory.value) {
    return [...new Set(
      props.products
        .filter(p => p.category === selectedCategory.value && p.brand)
        .map(p => p.brand)
    )].sort()
  }
  return props.filterOptions.brands
})

const availableCategories = computed(() => {
  if (!props.products) return []
  if (selectedBrand.value) {
    return [...new Set(
      props.products
        .filter(p => p.brand === selectedBrand.value)
        .map(p => p.category)
    )].sort()
  }
  return props.filterOptions.categories
})

watch(selectedCategory, () => {
  if (selectedBrand.value && !availableBrands.value.includes(selectedBrand.value)) {
    selectedBrand.value = ''
  }
})

watch(selectedBrand, () => {
  if (selectedCategory.value && !availableCategories.value.includes(selectedCategory.value)) {
    selectedCategory.value = ''
  }
})

const clearFilters = () => {
  selectedCategory.value = ''
  selectedBrand.value = ''
}

const chartData = computed(() => {
  const sorted = [...filteredProducts.value].sort((a, b) =>
    selectedDirection.value === 'top'
      ? b[selectedMetric.value] - a[selectedMetric.value]
      : a[selectedMetric.value] - b[selectedMetric.value]
  ).slice(0, 5)

  return {
    labels: sorted.map(p => p.title.length > 20 ? p.title.slice(0, 20) + '...' : p.title),
    datasets: [{
      label: selectedMetric.value,
      data: sorted.map(p => p[selectedMetric.value]),
      backgroundColor: COLORS[selectedMetric.value],
      borderRadius: 6
    }]
  }
})

const chartOptions = computed(() => ({
  responsive: true,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context) => ` ${PREFIXES[selectedMetric.value]}${context.raw}`
      }
    }
  },
  scales: {
    y: { beginAtZero: true, grid: { color: '#f3f4f6' } },
    x: { grid: { display: false } }
  }
}))
</script>

<style scoped>
.chart-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.controls {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  align-items: flex-end;
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

.no-results {
  font-size: 0.85rem;
  color: #6b7280;
  text-align: center;
  padding: 2rem 0;
}
</style>