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
          <option v-for="cat in filterOptions.categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
      <div class="control-group">
        <label>Brand</label>
        <select v-model="selectedBrand">
          <option value="">All</option>
          <option v-for="brand in filterOptions.brands" :key="brand" :value="brand">{{ brand }}</option>
        </select>
      </div>
      <div class="control-group">
        <label>Tag</label>
        <select v-model="selectedTag">
          <option value="">All</option>
          <option v-for="tag in filterOptions.tags" :key="tag" :value="tag">{{ tag }}</option>
        </select>
      </div>
    </div>

    <Bar :data="chartData" :options="chartOptions" />

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
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
const selectedTag = ref('')

const AGE_GROUPS = ['18-25', '26-30', '31-35', '36-40', '40+']
const GENDERS = ['male', 'female']

const getAgeGroup = (age) => {
  if (age <= 25) return '18-25'
  if (age <= 30) return '26-30'
  if (age <= 36) return '31-36'
  if (age <= 40) return '36-40'
  return '40+'
}

const filteredData = computed(() => {
  return props.userReviewData.map(user => {
    const filteredReviews = user.reviews.filter(r => {
      const matchCategory = !selectedCategory.value || r.productCategory === selectedCategory.value
      const matchBrand = !selectedBrand.value || r.productBrand === selectedBrand.value
      const matchTag = !selectedTag.value || r.productTags.includes(selectedTag.value)
      return matchCategory && matchBrand && matchTag
    })
    return { ...user, reviews: filteredReviews }
  }).filter(user => user.reviews.length > 0)
})

const chartData = computed(() => {
  const groups = {}

  let labels = []
  if (selectedSegment.value === 'age') {
    AGE_GROUPS.forEach(g => groups[g] = { total: 0, count: 0 })
    labels = AGE_GROUPS
  } else if (selectedSegment.value === 'gender') {
    labels = []
  } else if (selectedSegment.value === 'age_gender') {
    AGE_GROUPS.forEach(age =>
      GENDERS.forEach(gender => {
        const key = `${gender} ${age}`
        groups[key] = { total: 0, count: 0 }
      })
    )
    labels = AGE_GROUPS.flatMap(age => GENDERS.map(gender => `${gender} ${age}`))
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

  if (selectedSegment.value === 'gender') {
    labels = Object.keys(groups)
  }

  return {
    labels,
    datasets: [{
      label: 'Avg. review rating',
      data: labels.map(k => groups[k]?.count > 0
        ? parseFloat((groups[k].total / groups[k].count).toFixed(2))
        : 0
      ),
      backgroundColor: labels.map(l =>
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
      min: 1,
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
</style>