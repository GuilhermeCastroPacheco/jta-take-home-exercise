<template>
  <div class="products-table">

    <div class="page-header">
      <div>
        <h1>All products</h1>
        <p>Complete list of products</p>
      </div>
      <RouterLink to="/products" class="back-link">
        <i class="pi pi-arrow-left" /> Back to summary
      </RouterLink>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else>
      <div class="card">
        <DataTableFull
          :columns="productColumns"
          :data="products"
          :filters="productFilters"
          :sortOptions="sortOptions"
          :searchFields="searchFields"
          :attentionIds="attentionIds"
          :initialAttention="route.query.attention === 'true'"
          searchPlaceholder="Search by title..."
          detailRoute="/products"
          :pageSize="10"
        />
      </div>
    </template>

  </div>
</template>

<script setup>
import { computed } from 'vue'
import DataTableFull from '../../components/DataTableFull.vue'
import { useProducts } from '../../composables/useProducts'
import { useRoute } from 'vue-router'

const route = useRoute()

const { products, loading, error } = useProducts()

const attentionIds = computed(() => {
  if (!products.value?.length) return null
  const attentionProducts = products.value.filter(p =>
    p.stock < p.minimumOrderQuantity ||
    p.availabilityStatus === 'Low Stock' ||
    p.availabilityStatus === 'Out of Stock'
  )
  return new Set(attentionProducts.map(p => p.id))
})

const productColumns = [
  { field: 'thumbnail', header: '', type: 'image' },
  { field: 'title', header: 'Product' },
  { field: 'category', header: 'Category', muted: true },
  { field: 'brand', header: 'Brand', formatter: (row) => row.brand || '—' },
  { field: 'price', header: 'Price', muted: true, prefix: '$' },
  { field: 'rating', header: 'Rating' },
  { field: 'stock', header: 'Stock', type: 'stock' },
  { field: 'availabilityStatus', header: 'Status' }
]

const productFilters = computed(() => {
  if (!products.value?.length) return []
  const unique = (fn) => [...new Set(products.value.map(fn).filter(Boolean))].sort()
  return [
    { field: 'category', label: 'Category', options: unique(p => p.category) },
    { field: 'brand', label: 'Brand', options: unique(p => p.brand) },
    { field: 'availabilityStatus', label: 'Status', options: unique(p => p.availabilityStatus) }
  ]
})

const sortOptions = [
  { field: 'price', label: 'Price', getValue: (row) => row.price },
  { field: 'rating', label: 'Rating', getValue: (row) => row.rating },
  { field: 'stock', label: 'Stock', getValue: (row) => row.stock }
]

const searchFields = ['title']
</script>

<style scoped>
.products-table {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-header h1 {
  font-size: 1.4rem;
  font-weight: 500;
  color: #111827;
}

.page-header p {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 2px;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: #1d4ed8;
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}

.card {
  background: #ffffff;
  border: 0.5px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
}

.loading {
  color: #6b7280;
  font-size: 0.9rem;
}

.error {
  color: #b91c1c;
  font-size: 0.9rem;
}
</style>