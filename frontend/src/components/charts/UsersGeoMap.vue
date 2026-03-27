<template>
  <div class="map-wrapper">

    <div class="controls">
      <div class="control-group">
        <label>Location type</label>
        <select v-model="selectedType" @change="selectedState = ''">
          <option value="address">Address</option>
          <option value="company">Company</option>
          <option value="university">University</option>
        </select>
      </div>
      <div class="control-group">
        <label>State</label>
        <select v-model="selectedState">
          <option value="">All states</option>
          <option v-for="state in availableStates" :key="state" :value="state">{{ state }}</option>
        </select>
      </div>
    </div>

    <div ref="mapContainer" class="map-container"></div>

    <div v-if="selectedState" class="city-breakdown">
      <h4>{{ selectedState }} — cities</h4>
      <div class="city-list">
        <div
          v-for="(count, city) in currentData.by_city[selectedState]"
          :key="city"
          class="city-row"
        >
          <span class="city-name">{{ city }}</span>
          <span class="city-count">{{ count }} user{{ count !== 1 ? 's' : '' }}</span>
        </div>
      </div>
    </div>

    <div class="legend">
      <span class="leg-label">0</span>
      <div class="leg-bar">
        <div class="leg-swatch" style="background:#EBF5FF"></div>
        <div class="leg-swatch" style="background:#B5D4F4"></div>
        <div class="leg-swatch" style="background:#85B7EB"></div>
        <div class="leg-swatch" style="background:#378ADD"></div>
        <div class="leg-swatch" style="background:#185FA5"></div>
        <div class="leg-swatch" style="background:#0C447C"></div>
      </div>
      <span class="leg-label">{{ maxCount }}+ users</span>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import * as d3 from 'd3'
import * as topojson from 'topojson-client'

const props = defineProps({
  geoData: Object
})

const mapContainer = ref(null)
const selectedType = ref('address')
const selectedState = ref('')

let svg = null
let projection = null
let pathGenerator = null
let usAtlas = null

const STATE_NAMES = {
  "01":"Alabama","02":"Alaska","04":"Arizona","05":"Arkansas","06":"California",
  "08":"Colorado","09":"Connecticut","10":"Delaware","11":"District of Columbia",
  "12":"Florida","13":"Georgia","15":"Hawaii","16":"Idaho","17":"Illinois",
  "18":"Indiana","19":"Iowa","20":"Kansas","21":"Kentucky","22":"Louisiana",
  "23":"Maine","24":"Maryland","25":"Massachusetts","26":"Michigan","27":"Minnesota",
  "28":"Mississippi","29":"Missouri","30":"Montana","31":"Nebraska","32":"Nevada",
  "33":"New Hampshire","34":"New Jersey","35":"New Mexico","36":"New York",
  "37":"North Carolina","38":"North Dakota","39":"Ohio","40":"Oklahoma","41":"Oregon",
  "42":"Pennsylvania","44":"Rhode Island","45":"South Carolina","46":"South Dakota",
  "47":"Tennessee","48":"Texas","49":"Utah","50":"Vermont","51":"Virginia",
  "53":"Washington","54":"West Virginia","55":"Wisconsin","56":"Wyoming"
}

const currentData = computed(() => {
  if (!props.geoData) return { by_state: {}, by_city: {} }
  return props.geoData[selectedType.value] || { by_state: {}, by_city: {} }
})

const availableStates = computed(() => {
  return Object.keys(currentData.value.by_state).sort()
})

const maxCount = computed(() => {
  const counts = Object.values(currentData.value.by_state)
  return counts.length > 0 ? Math.max(...counts) : 1
})

const colorScale = computed(() => {
  return d3.scaleQuantize()
    .domain([0, maxCount.value])
    .range(['#EBF5FF', '#B5D4F4', '#85B7EB', '#378ADD', '#185FA5', '#0C447C'])
})

const getStateFill = (stateId) => {
  const name = STATE_NAMES[stateId.toString().padStart(2, '0')]
  if (!name) return '#f3f4f6'
  const count = currentData.value.by_state[name] || 0
  return count > 0 ? colorScale.value(count) : '#f3f4f6'
}

const renderMap = () => {
  if (!usAtlas || !mapContainer.value) return

  const container = mapContainer.value
  const width = container.offsetWidth
  const height = width * 0.6

  d3.select(container).selectAll('*').remove()

  svg = d3.select(container)
    .append('svg')
    .attr('width', '100%')
    .attr('viewBox', `0 0 ${width} ${height}`)

  projection = d3.geoAlbersUsa()
    .scale(width * 1.2)
    .translate([width / 2, height / 2])

  pathGenerator = d3.geoPath().projection(projection)

  const states = topojson.feature(usAtlas, usAtlas.objects.states)

  // Tooltip
  const tooltip = d3.select(container)
    .append('div')
    .attr('class', 'map-tooltip')
    .style('display', 'none')

  svg.selectAll('.state')
    .data(states.features)
    .enter()
    .append('path')
    .attr('class', 'state')
    .attr('d', pathGenerator)
    .attr('fill', d => getStateFill(d.id))
    .attr('stroke', '#fff')
    .attr('stroke-width', 0.5)
    .style('cursor', 'pointer')
    .on('mousemove', function(event, d) {
      const name = STATE_NAMES[d.id.toString().padStart(2, '0')]
      const count = currentData.value.by_state[name] || 0
      tooltip
        .style('display', 'block')
        .style('left', (event.offsetX + 12) + 'px')
        .style('top', (event.offsetY - 10) + 'px')
        .html(`<div class="tt-title">${name}</div><div class="tt-row">${count} user${count !== 1 ? 's' : ''}</div>`)
      d3.select(this).attr('stroke', '#378ADD').attr('stroke-width', 1.5)
    })
    .on('mouseleave', function() {
      tooltip.style('display', 'none')
      d3.select(this).attr('stroke', '#fff').attr('stroke-width', 0.5)
    })
    .on('click', function(event, d) {
      const name = STATE_NAMES[d.id.toString().padStart(2, '0')]
      if (currentData.value.by_state[name]) {
        selectedState.value = selectedState.value === name ? '' : name
      }
    })
}

const updateColors = () => {
  if (!svg) return
  svg.selectAll('.state')
    .attr('fill', d => getStateFill(d.id))
}

watch(currentData, () => updateColors())
watch(selectedState, () => updateColors())

onMounted(async () => {
  const res = await fetch('https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json')
  usAtlas = await res.json()
  renderMap()

  window.addEventListener('resize', renderMap)
})

onUnmounted(() => {
  window.removeEventListener('resize', renderMap)
})
</script>

<style scoped>
.map-wrapper {
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

.map-container {
  width: 100%;
  position: relative;
}

.map-container :deep(.map-tooltip) {
  position: absolute;
  background: #ffffff;
  border: 0.5px solid #e5e7eb;
  border-radius: 8px;
  padding: 8px 10px;
  font-size: 12px;
  pointer-events: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.map-container :deep(.tt-title) {
  font-weight: 500;
  color: #111827;
  margin-bottom: 2px;
}

.map-container :deep(.tt-row) {
  color: #6b7280;
  font-size: 11px;
}

.city-breakdown {
  background: #f9fafb;
  border: 0.5px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.75rem 1rem;
}

.city-breakdown h4 {
  font-size: 0.85rem;
  font-weight: 500;
  color: #111827;
  margin-bottom: 0.5rem;
}

.city-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.city-row {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  border-bottom: 0.5px solid #e5e7eb;
  font-size: 0.8rem;
}

.city-row:last-child {
  border-bottom: none;
}

.city-name {
  color: #111827;
}

.city-count {
  color: #6b7280;
}

.legend {
  display: flex;
  align-items: center;
  gap: 8px;
}

.leg-label {
  font-size: 11px;
  color: #6b7280;
}

.leg-bar {
  display: flex;
  gap: 2px;
}

.leg-swatch {
  width: 20px;
  height: 10px;
  border-radius: 2px;
}
</style>