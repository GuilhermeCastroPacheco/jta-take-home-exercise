<template>
  <div class="table-wrapper">
    <table>
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.field">{{ col.header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in data" :key="index">
          <td v-for="col in columns" :key="col.field">
            <span v-if="col.field === 'availabilityStatus'">
              <span class="pill" :class="statusClass(row[col.field])">{{ row[col.field] }}</span>
            </span>
            <span v-else>{{ col.prefix || '' }}{{ row[col.field] }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  columns: Array,
  data: Array
})

const statusClass = (status) => {
  if (!status) return ''
  const s = status.toLowerCase()
  if (s.includes('low')) return 'pill-amber'
  if (s.includes('out')) return 'pill-red'
  return 'pill-green'
}
</script>

<style scoped>
.table-wrapper {
  overflow-x: auto;
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
  padding: 8px 0;
  color: #111827;
  border-bottom: 0.5px solid #f3f4f6;
}

tr:last-child td {
  border-bottom: none;
}

.pill {
  display: inline-block;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 20px;
}

.pill-green { background: #f0fdf4; color: #15803d; }
.pill-amber { background: #fffbeb; color: #b45309; }
.pill-red   { background: #fef2f2; color: #b91c1c; }
</style>