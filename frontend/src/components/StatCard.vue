<template>
  <div class="stat-card">
    <div class="stat-label">{{ label }}</div>
    <div class="stat-value">{{ value }}</div>
    <span v-if="badge" class="stat-badge" :class="badgeClass">{{ badge }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  value: [String, Number],
  badge: String,
  badgeType: {
    type: String,
    default: 'green'
  }
})

const badgeClass = computed(() => `badge-${props.badgeType}`)
</script>

<style scoped>
.stat-card {
  background: #ffffff;
  border: 0.5px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
}

.stat-value {
  font-size: 28px;
  font-weight: 500;
  color: #111827;
}

.stat-badge {
  display: inline-block;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 20px;
  margin-top: 4px;
  width: fit-content;
}

.badge-green {
  background: #f0fdf4;
  color: #15803d;
}

.badge-amber {
  background: #fffbeb;
  color: #b45309;
}

.badge-red {
  background: #fef2f2;
  color: #b91c1c;
}
</style>