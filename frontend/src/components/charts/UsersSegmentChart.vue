<template>
  <div class="chart-wrapper">
    <div class="controls">
      <div class="control-group">
        <label>Segment by</label>
        <select v-model="selectedSegment">
          <option value="gender">Gender</option>
          <option value="age">Age group</option>
          <option value="age_gender">Age + Gender</option>
        </select>
      </div>
    </div>
    <Doughnut :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  usersSummary: Object
})

const selectedSegment = ref('gender')

const COLORS = [
  '#378ADD', '#D4537E', '#639922', '#BA7517',
  '#1D9E75', '#E24B4A', '#8B5CF6', '#F59E0B',
  '#10B981', '#EF4444', '#6366F1', '#EC4899'
]

const chartData = computed(() => {
  if (!props.usersSummary) return { labels: [], datasets: [] }

  let labels = []
  let data = []

  if (selectedSegment.value === 'gender') {
    labels = Object.keys(props.usersSummary.gender_distribution)
    data = Object.values(props.usersSummary.gender_distribution)
  } else if (selectedSegment.value === 'age') {
    labels = Object.keys(props.usersSummary.age_groups)
    data = Object.values(props.usersSummary.age_groups)
  } else {
    const dist = props.usersSummary.age_gender_distribution || {}
    labels = Object.keys(dist)
    data = Object.values(dist)
  }

  return {
    labels,
    datasets: [{
      data,
      backgroundColor: COLORS.slice(0, labels.length)
    }]
  }
})

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' },
    tooltip: {
      callbacks: {
        label: (context) => {
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const pct = ((context.raw / total) * 100).toFixed(1)
          return ` ${context.raw} users (${pct}%)`
        }
      }
    }
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