<template>
  <div class="chart-wrapper">

    <div class="controls">
      <div class="control-group">
        <label>Group by</label>
        <select v-model="selectedSegment">
          <option value="age">Age group</option>
          <option value="gender">Gender</option>
          <option value="age_gender">Age + Gender</option>
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

    <Bar :data="chartData" :options="chartOptions" />

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
  userReviewData: Array,
  filterOptions: Object
})

const selectedSegment = ref('age')
const selectedCategory = ref('')
const selectedBrand = ref('')

const AGE_GROUPS = ['18-25', '26-30', '31-35', '36-40', '40+']
const GENDERS = ['male', 'female']

const isFiltered = computed(() => !!selectedCategory.value || !!selectedBrand.value)

const clearFilters = () => {
  selectedCategory.value = ''
  selectedBrand.value = ''
}

const getAgeGroup = (age) => {
  if (age <= 25) return '18-25'
  if (age <= 30) return '26-30'
  if (age <= 35) return '31-35'
  if (age <= 40) return '36-40'
  return '40+'
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
  }).filter(user => user.reviews.length > 0)
})

const chartData = computed(() => {
  const groups = {}

  if (selectedSegment.value === 'age') {
    AGE_GROUPS.forEach(g => groups[g] = { total: 0, count: 0 })
  } else if (selectedSegment.value === 'age_gender') {
    AGE_GROUPS.forEach(age =>
      GENDERS.forEach(gender => {
        const key = `${gender} ${age}`
        groups[key] = { total: 0, count: 0 }
      })
    )
  }

  filteredData.value.forEach(user => {
    let key
    if (selectedSegment.value === 'age') {
      key = getAgeGroup(user.age)
    } else if (selectedSegment.value === 'gender') {
      key = user.gender
    } else {
      key = `${user.gender} ${getAgeGroup(user.age)}`
    }

    if (!groups[key]) groups[key] = { total: 0, count: 0 }

    const avg = user.reviews.reduce((sum, r) => sum + r.rating, 0) / user.reviews.length
    groups[key].total += avg
    groups[key].count += 1
  })

  // Só labels com count > 0
  const allLabels = selectedSegment.value === 'gender'
    ? Object.keys(groups)
    : selectedSegment.value === 'age'
      ? AGE_GROUPS
      : AGE_GROUPS.flatMap(age => GENDERS.map(gender => `${gender} ${age}`))

  const activeLabels = allLabels.filter(k => groups[k]?.count > 0)

  return {
    labels: activeLabels,
    datasets: [{
      label: 'Avg. review rating',
      data: activeLabels.map(k =>
        parseFloat((groups[k].total / groups[k].count).toFixed(2))
      ),
      backgroundColor: activeLabels.map(l =>
        l.includes('female') ? '#D4537E' :
        l.includes('male') ? '#378ADD' : '#378ADD'
      ),
      borderRadius: 6
    }]
  }
})

const chartOptions = {
  responsive: true,
  plugins: { legend: { display: false } },
  scales: {
    y: {
      beginAtZero: false,
      min: 0,
      max: 5,
      grid: { color: '#f3f4f6' },
      title: { display: true, text: 'Avg. rating' }
    },
    x: { grid: { display: false } }
  }
}
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
</style>