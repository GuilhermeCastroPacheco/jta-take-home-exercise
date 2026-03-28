<template>
  <div class="table-wrapper">

    <div class="controls">
      <div class="control-group">
        <label>Group by</label>
        <select v-model="selectedSegment">
          <option value="gender">Gender</option>
          <option value="age">Age group</option>
          <option value="state">State</option>
        </select>
      </div>
      <div class="control-group" v-if="selectedSegment === 'state'">
        <label>Show</label>
        <select v-model="stateFilter">
          <option value="top5">Top 5 avg. rating</option>
          <option value="bottom5">Bottom 5 avg. rating</option>
        </select>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th>{{ segmentLabel }}</th>
          <th>Users</th>
          <th>Total reviews</th>
          <th>MIN</th>
          <th>MAX</th>
          <th>AVG</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in displayData" :key="row.segment">
          <td class="segment-label">{{ row.segment }}</td>
          <td>{{ row.userCount }}</td>
          <td>{{ row.totalReviews }}</td>
          <td>{{ row.minRating }}</td>
          <td>{{ row.maxRating }}</td>
          <td>
            <span class="rating-badge" :class="ratingClass(row.avgRating)">
              {{ row.avgRating }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  userReviewData: Array
})

const selectedSegment = ref('gender')
const stateFilter = ref('top5')

const AGE_GROUPS = ['18-25', '26-30', '31-35', '36-40', '40+']

const getAgeGroup = (age) => {
  if (age <= 25) return '18-25'
  if (age <= 30) return '26-30'
  if (age <= 35) return '31-35'
  if (age <= 40) return '36-40'
  return '40+'
}

const segmentLabel = computed(() => {
  if (selectedSegment.value === 'gender') return 'Gender'
  if (selectedSegment.value === 'age') return 'Age group'
  return 'State'
})

const tableData = computed(() => {
  const groups = {}

  props.userReviewData.forEach(user => {
    const key = selectedSegment.value === 'age'
      ? getAgeGroup(user.age)
      : user[selectedSegment.value]

    if (!groups[key]) groups[key] = { users: [], ratings: [] }

    const userAvg = user.reviews.length > 0
      ? user.reviews.reduce((sum, r) => sum + r.rating, 0) / user.reviews.length
      : null

    groups[key].users.push(user)
    if (userAvg !== null) groups[key].ratings.push(userAvg)
  })

  const keys = selectedSegment.value === 'age'
    ? AGE_GROUPS
    : Object.keys(groups).sort()

  return keys.map(key => {
    const group = groups[key] || { users: [], ratings: [] }
    const ratings = group.ratings

    return {
      segment: key,
      userCount: group.users.length,
      totalReviews: group.users.reduce((sum, u) => sum + u.reviews.length, 0),
      minRating: ratings.length > 0 ? Math.min(...ratings).toFixed(2) : '—',
      maxRating: ratings.length > 0 ? Math.max(...ratings).toFixed(2) : '—',
      avgRating: ratings.length > 0
        ? (ratings.reduce((a, b) => a + b, 0) / ratings.length).toFixed(2)
        : '—'
    }
  })
})

const displayData = computed(() => {
  if (selectedSegment.value !== 'state') return tableData.value

  const withRatings = tableData.value.filter(r => r.avgRating !== '—')
  const sorted = [...withRatings].sort((a, b) =>
    parseFloat(b.avgRating) - parseFloat(a.avgRating)
  )

  return stateFilter.value === 'top5' ? sorted.slice(0, 5) : sorted.slice(-5).reverse()
})

const ratingClass = (rating) => {
  if (rating === '—') return ''
  const val = parseFloat(rating)
  if (val >= 4) return 'rating-green'
  if (val >= 3) return 'rating-amber'
  return 'rating-red'
}
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

.segment-label {
  font-weight: 500;
}

.rating-badge {
  display: inline-block;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 20px;
}

.rating-green { background: #f0fdf4; color: #15803d; }
.rating-amber { background: #fffbeb; color: #b45309; }
.rating-red   { background: #fef2f2; color: #b91c1c; }
</style>