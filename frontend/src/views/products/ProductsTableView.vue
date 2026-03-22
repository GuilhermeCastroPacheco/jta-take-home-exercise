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
        <div class="card-header">
          <span class="total">{{ filteredProducts.length }} products</span>
          <div class="filters">
            <select v-model="selectedCategory" class="select-input">
              <option value="">All categories</option>
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
            <input
              v-model="search"
              type="text"
              placeholder="Search by name or brand..."
              class="search-input"
            />
          </div>
        </div>
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Category</th>
              <th>Brand</th>
              <th>Price</th>
              <th>Rating</th>
              <th>Stock</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in filteredProducts" :key="product.id">
              <td>{{ product.title }}</td>
              <td class="muted">{{ product.category }}</td>
              <td class="muted">{{ product.brand || '—' }}</td>
              <td>${{ product.price }}</td>
              <td>{{ product.rating }}</td>
              <td :class="stockClass(product)">{{ product.stock }}</td>
              <td>
                <span class="pill" :class="statusClass(product.availabilityStatus)">
                  {{ product.availabilityStatus }}
                </span>
              </td>
              <td>
                <RouterLink :to="`/products/${product.id}`" class="detail-link">
                  View <i class="pi pi-arrow-right" />
                </RouterLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useProducts } from '../../composables/useProducts'

const { products, loading, error } = useProducts()

const search = ref('')
const selectedCategory = ref('')

const categories = computed(() => {
  const cats = products.value.map(p => p.category)
  return [...new Set(cats)].sort()
})

const filteredProducts = computed(() => {
  return products.value.filter(p => {
    const matchesSearch = !search.value ||
      p.title.toLowerCase().includes(search.value.toLowerCase()) ||
      (p.brand || '').toLowerCase().includes(search.value.toLowerCase())
    const matchesCategory = !selectedCategory.value || p.category === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})

const statusClass = (status) => {
  if (!status) return ''
  const s = status.toLowerCase()
  if (s.includes('low')) return 'pill-amber'
  if (s.includes('out')) return 'pill-red'
  return 'pill-green'
}

const stockClass = (product) => {
  if (product.stock < product.minimumOrderQuantity) return 'stock-red'
  if (product.stock < product.minimumOrderQuantity * 2) return 'stock-amber'
  return ''
}
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
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow-x: auto;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.total {
  font-size: 0.85rem;
  color: #6b7280;
  white-space: nowrap;
}

.filters {
  display: flex;
  gap: 0.75rem;
}

.search-input,
.select-input {
  padding: 0.5rem 0.75rem;
  border: 0.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.85rem;
  font-family: inherit;
  color: #111827;
  outline: none;
  background: #ffffff;
}

.search-input {
  width: 240px;
}

.search-input:focus,
.select-input:focus {
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

td.muted {
  color: #6b7280;
}

td.stock-red {
  color: #b91c1c;
  font-weight: 500;
}

td.stock-amber {
  color: #b45309;
  font-weight: 500;
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

.detail-link {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.8rem;
  color: #1d4ed8;
  text-decoration: none;
  justify-content: flex-end;
}

.detail-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }

  .search-input {
    width: 100%;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>