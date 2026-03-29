<template>
  <div class="product-detail">

    <div class="page-header">
      <div class="header-left">
        <div>
          <h1 v-if="product">{{ product.title }}</h1>
          <p v-if="product" class="product-sku">{{ product.sku }}</p>
        </div>
        <span v-if="product" class="pill" :class="statusClass">{{ product.availabilityStatus }}</span>
      </div>
      <RouterLink to="/products/all" class="back-link">
        <i class="pi pi-arrow-left" /> Back to products
      </RouterLink>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else-if="product">
      <!-- Description -->
      <div class="card card--description">
        <img :src="product.thumbnail" :alt="product.title" class="product-image-large" />
        <div class="description-content">
          <h3>Description</h3>
          <p class="description-text">{{ product.description }}</p>
        </div>
      </div>

      <div class="row">
        <!-- Product info -->
        <div class="card">
          <h3>Product info</h3>
          <div class="info-list">
            <div class="info-row">
              <span class="info-label">Category</span>
              <span class="info-value">{{ product.category }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Brand</span>
              <span class="info-value">{{ product.brand || '—' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Tags</span>
              <span class="info-value">
                <div class="tag-list">
                  <span v-for="tag in product.tags" :key="tag" class="tag">{{ tag }}</span>
                </div>
              </span>
            </div>
            <div class="info-row">
              <span class="info-label">Price</span>
              <span class="info-value">${{ product.price }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Discount</span>
              <span class="info-value">{{ product.discountPercentage }}%</span>
            </div>
            <div class="info-row">
              <span class="info-label">Rating</span>
              <span class="info-value">{{ product.rating }} / 5</span>
            </div>
            <div class="info-row">
              <span class="info-label">Stock</span>
              <span class="info-value" :class="stockClass">{{ product.stock }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Min. order qty</span>
              <span class="info-value">{{ product.minimumOrderQuantity }}</span>
            </div>
          </div>
        </div>

        <!-- Details -->
        <div class="card">
          <h3>Details</h3>
          <div class="info-list">
            <div class="info-row">
              <span class="info-label">Weight</span>
              <span class="info-value">{{ product.weight }} kg</span>
            </div>
            <div class="info-row">
              <span class="info-label">Width</span>
              <span class="info-value">{{ product.dimensions?.width }} cm</span>
            </div>
            <div class="info-row">
              <span class="info-label">Height</span>
              <span class="info-value">{{ product.dimensions?.height }} cm</span>
            </div>
            <div class="info-row">
              <span class="info-label">Depth</span>
              <span class="info-value">{{ product.dimensions?.depth }} cm</span>
            </div>
            <div class="info-row">
              <span class="info-label">Warranty</span>
              <span class="info-value">{{ product.warrantyInformation }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Shipping</span>
              <span class="info-value">{{ product.shippingInformation }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Return policy</span>
              <span class="info-value">{{ product.returnPolicy }}</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Reviews -->
      <div class="card" v-if="product.reviews?.length">
        <h3>Reviews ({{ product.reviews.length }})</h3>
        <div class="reviews">
          <div v-for="(review, index) in product.reviews" :key="index" class="review">
            <div class="review-header">
              <span class="review-name">{{ review.reviewerName }}</span>
              <span class="review-rating">{{ '★'.repeat(review.rating) }}{{ '☆'.repeat(5 - review.rating) }}</span>
            </div>
            <p class="review-comment">{{ review.comment }}</p>
          </div>
        </div>
      </div>

    </template>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProduct } from '../../services/api'

const route = useRoute()
const product = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await getProduct(route.params.id)
    product.value = res.data
  } catch (e) {
    error.value = 'Failed to load product'
  } finally {
    loading.value = false
  }
})

const statusClass = computed(() => {
  if (!product.value) return ''
  const s = product.value.availabilityStatus.toLowerCase()
  if (s.includes('low')) return 'pill-amber'
  if (s.includes('out')) return 'pill-red'
  return 'pill-green'
})

const stockClass = computed(() => {
  if (!product.value) return ''
  if (product.value.stock < product.value.minimumOrderQuantity) return 'stock-red'
  if (product.value.stock < product.value.minimumOrderQuantity * 2) return 'stock-amber'
  return ''
})
</script>

<style scoped>
.product-detail {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-header h1 {
  font-size: 1.4rem;
  font-weight: 500;
  color: #111827;
}

.product-sku {
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

.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.card {
  background: #ffffff;
  border: 0.5px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card h3 {
  font-size: 0.9rem;
  font-weight: 500;
  color: #111827;
}

.info-list {
  display: flex;
  flex-direction: column;
}

.info-row {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 1rem;
  padding: 8px 0;
  border-bottom: 0.5px solid #f3f4f6;
  font-size: 0.85rem;
  align-items: start;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  color: #6b7280;
}

.info-value {
  color: #111827;
}

.stock-red { color: #b91c1c; font-weight: 500; }
.stock-amber { color: #b45309; font-weight: 500; }

.pill {
  display: inline-block;
  font-size: 13px;
  padding: 4px 12px;
  border-radius: 20px;
}

.pill-green { background: #f0fdf4; color: #15803d; box-shadow: 0 0 0 1.5px #15803d; }
.pill-amber { background: #fffbeb; color: #b45309; box-shadow: 0 0 0 1.5px #b45309; }
.pill-red   { background: #fef2f2; color: #b91c1c; box-shadow: 0 0 0 1.5px #b91c1c; }

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 20px;
  background: #f3f4f6;
  color: #374151;
}

.reviews {
  display: flex;
  flex-direction: column;
}

.review {
  padding: 0.75rem 0;
  border-bottom: 0.5px solid #f3f4f6;
}

.review:last-child {
  border-bottom: none;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.review-name {
  font-size: 0.85rem;
  font-weight: 500;
  color: #111827;
}

.review-rating {
  font-size: 0.85rem;
  color: #BA7517;
  letter-spacing: 2px;
}

.review-comment {
  font-size: 0.8rem;
  color: #6b7280;
  line-height: 1.5;
}

.loading {
  color: #6b7280;
  font-size: 0.9rem;
}

.error {
  color: #b91c1c;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .row {
    grid-template-columns: 1fr;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .header-left {
    flex-wrap: wrap;
  }

  .back-link {
    align-self: flex-end;
  }
}

.card--description {
  flex-direction: row;
  gap: 1.5rem;
  align-items: flex-start;
}

.product-image-large {
  width: 120px;
  min-width: 120px;
  height: 120px;
  object-fit: contain;
  border-radius: 8px;
  background: #f9fafb;
  padding: 8px;
  border: 0.5px solid #e5e7eb;
}

.description-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.description-text {
  font-size: 0.85rem;
  color: #374151;
  line-height: 1.6;
}
</style>