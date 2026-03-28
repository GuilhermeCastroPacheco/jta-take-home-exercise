<template>
  <div class="chart-wrapper">

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

    <Doughnut :data="chartData" :options="chartOptions" />

    <p v-if="isFiltered" class="filter-note">
      * {{ noReviewCount }} users have no reviews and are excluded when filters are applied
    </p>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  userReviewData: Array,
  noReviewCount: Number,
  totalUsers: Number,
  filterOptions: Object
})

const selectedCategory = ref('')
const selectedBrand = ref('')

const RATING_BANDS = ['0-1', '1-2', '2-3', '3-4', '4-5']

const getRatingBand = (avg) => {
  if (avg <= 1) return '0-1'
  if (avg <= 2) return '1-2'
  if (avg <= 3) return '2-3'
  if (avg <= 4) return '3-4'
  return '4-5'
}

const isFiltered = computed(() => !!selectedCategory.value || !!selectedBrand.value)

const clearFilters = () => {
  selectedCategory.value = ''
  selectedBrand.value = ''
}

const availableBrands = computed(() => {
  if (!props.filterOptions) return []
  if (selectedCategory.value) {
    return [...new Set(
      props.userReviewData
        .flatMap(u => u.reviews)
        .filter(r => r.productCategory === selectedCategory.value && r.productBrand !== 'No brand')
        .map(r => r.productBrand)
    )].sort()
  }
  return props.filterOptions.brands
})

const availableCategories = computed(() => {
  if (!props.filterOptions) return []
  if (selectedBrand.value) {
    return [...new Set(
      props.userReviewData
        .flatMap(u => u.reviews)
        .filter(r => r.productBrand === selectedBrand.value)
        .map(r => r.productCategory)
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

const filteredData = computed(() => {
  return props.userReviewData.map(user => {
    const filteredReviews = user.reviews.filter(r => {
      const matchCategory = !selectedCategory.value || r.productCategory === selectedCategory.value
      const matchBrand = !selectedBrand.value || r.productBrand === selectedBrand.value
      return matchCategory && matchBrand
    })
    return { ...user, reviews: filteredReviews }
  })
})

const chartData = computed(() => {
  const bands = {}
  RATING_BANDS.forEach(b => bands[b] = 0)

  let usersWithReviews = 0

  filteredData.value.forEach(user => {
    if (user.reviews.length === 0) return
    usersWithReviews++
    const avg = user.reviews.reduce((sum, r) => sum + r.rating, 0) / user.reviews.length
    bands[getRatingBand(avg)]++
  })

  const labels = [...RATING_BANDS]
  const data = [...RATING_BANDS.map(b => bands[b])]
  const colors = ['#E24B4A', '#BA7517', '#378ADD', '#639922', '#1D9E75']

  if (!isFiltered.value) {
    const noReviews = props.totalUsers - usersWithReviews
    labels.push('No reviews')
    data.push(noReviews)
    colors.push('#e5e7eb')
  }

  return {
    labels,
    datasets: [{ data, backgroundColor: colors }]
  }
})

const chartOptions = computed(() => ({
  responsive: true,
  plugins: {
    legend: { position: 'bottom' },
    tooltip: {
      callbacks: {
        label: (context) => {
          const value = context.raw
          const total = isFiltered.value
            ? props.totalUsers - props.noReviewCount
            : props.totalUsers
          const pct = ((value / total) * 100).toFixed(1)
          return ` ${value} users (${pct}%)`
        }
      }
    }
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

.filter-note {
  font-size: 11px;
  color: #9ca3af;
  font-style: italic;
  margin-top: 4px;
}
</style>