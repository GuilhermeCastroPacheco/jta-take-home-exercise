<template>
  <div class="user-detail">

    <div class="page-header">
      <div class="header-left">
        <img v-if="user" :src="user.image" :alt="user.firstName" class="user-avatar" />
        <div>
          <h1 v-if="user">{{ user.firstName }} {{ user.lastName }}</h1>
          <p v-if="user">{{ user.company?.title }}</p>
        </div>
      </div>
      <RouterLink to="/users/all" class="back-link">
        <i class="pi pi-arrow-left" /> Back to users
      </RouterLink>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else-if="user">

      <div class="row">
        <div class="card">
          <h3>Personal info</h3>
          <div class="info-list">
            <div class="info-row">
              <span class="info-label">Username</span>
              <span class="info-value">{{ user.username }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Age</span>
              <span class="info-value">{{ user.age }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Gender</span>
              <span class="info-value">{{ user.gender }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Birth date</span>
              <span class="info-value">{{ user.birthDate }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Email</span>
              <span class="info-value info-email">{{ user.email }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Phone</span>
              <span class="info-value">{{ user.phone }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Height</span>
              <span class="info-value">{{ user.height }} cm</span>
            </div>
            <div class="info-row">
              <span class="info-label">Weight</span>
              <span class="info-value">{{ user.weight }} kg</span>
            </div>
            <div class="info-row">
              <span class="info-label">Role</span>
              <span class="info-value">{{ user.role }}</span>
            </div>
          </div>
        </div>

        <div class="card">
          <h3>Location</h3>
          <div class="info-list">
            <div class="info-row">
              <span class="info-label">Address</span>
              <span class="info-value">{{ user.address?.address }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">City</span>
              <span class="info-value">{{ user.address?.city }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">State</span>
              <span class="info-value">{{ user.address?.state }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Postal code</span>
              <span class="info-value">{{ user.address?.postalCode }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Country</span>
              <span class="info-value">{{ user.address?.country }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="card">
          <h3>Company</h3>
          <div class="info-list">
            <div class="info-row">
              <span class="info-label">Name</span>
              <span class="info-value">{{ user.company?.name }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Department</span>
              <span class="info-value">{{ user.company?.department }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Title</span>
              <span class="info-value">{{ user.company?.title }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Address</span>
              <span class="info-value">{{ user.company?.address?.address }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">City</span>
              <span class="info-value">{{ user.company?.address?.city }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">State</span>
              <span class="info-value">{{ user.company?.address?.state }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Postal code</span>
              <span class="info-value">{{ user.company?.address?.postalCode }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Country</span>
              <span class="info-value">{{ user.company?.address?.country }}</span>
            </div>
          </div>
        </div>

        <div class="card">
          <h3>University</h3>
          <div class="info-list">
            <div class="info-row">
              <span class="info-label">Name</span>
              <span class="info-value">{{ user.university }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Address</span>
              <span class="info-value">{{ user.university_data?.address }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">City</span>
              <span class="info-value">{{ user.university_data?.city }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">State</span>
              <span class="info-value">{{ user.university_data?.state }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Postal code</span>
              <span class="info-value">{{ user.university_data?.postalCode }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Country</span>
              <span class="info-value">{{ user.university_data?.country }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Reviews summary -->
      <div class="card" v-if="user.reviews_summary?.total">
        <h3>Reviews summary</h3>
        <div class="summary-grid">
          <div class="summary-stat">
            <span class="summary-label">Total reviews</span>
            <span class="summary-value">{{ user.reviews_summary.total }}</span>
          </div>
          <div class="summary-stat">
            <span class="summary-label">Avg. rating</span>
            <span class="summary-value">{{ user.reviews_summary.avg_rating }}</span>
          </div>
          <div class="summary-stat">
            <span class="summary-label">Min rating</span>
            <span class="summary-value">{{ user.reviews_summary.min_rating }}</span>
          </div>
          <div class="summary-stat">
            <span class="summary-label">Max rating</span>
            <span class="summary-value">{{ user.reviews_summary.max_rating }}</span>
          </div>
        </div>

        <div class="row-inner">
          <div class="left-col">
            <div>
              <p class="sub-label">By category</p>
              <div class="tag-list">
                <span v-for="(count, cat) in user.reviews_summary.by_category" :key="cat" class="tag">
                  {{ cat }} ({{ count }})
                </span>
              </div>
            </div>
            <div>
              <p class="sub-label">By product</p>
              <div class="tag-list">
                <span v-for="(count, product) in user.reviews_summary.by_product" :key="product" class="tag">
                  {{ product }} ({{ count }})
                </span>
              </div>
            </div>
            <div>
              <p class="sub-label">By tags</p>
              <div class="tag-list">
                <span v-for="(count, tag) in user.reviews_summary.by_tags" :key="tag" class="tag">
                  {{ tag }} ({{ count }})
                </span>
              </div>
            </div>
          </div>
          <div>
            <p class="sub-label">By rating</p>
            <div class="rating-bars">
              <div v-for="(count, rating) in user.reviews_summary.by_rating" :key="rating" class="rating-bar-row">
                <span class="rating-num">{{ rating }}★</span>
                <div class="rating-track">
                  <div class="rating-fill" :style="{ width: `${(count / user.reviews_summary.total) * 100}%` }"></div>
                </div>
                <span class="rating-count">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Reviews -->
      <div class="card" v-if="user.reviews?.length">
        <h3>Reviews ({{ user.reviews.length }})</h3>
        <div class="reviews">
          <div v-for="(review, index) in user.reviews" :key="index" class="review">
            <div class="review-header">
              <div class="review-product">
                <img :src="review.productThumbnail" :alt="review.productTitle" class="review-thumb" />
                <RouterLink :to="`/products/${review.productId}`" class="review-title">
                  {{ review.productTitle }}
                </RouterLink>
              </div>
              <span class="review-rating">{{ '★'.repeat(review.rating) }}{{ '☆'.repeat(5 - review.rating) }}</span>
            </div>
            <p class="review-comment">{{ review.comment }}</p>
            <div class="review-tags">
              <span class="tag">{{ review.productCategory }}</span>
              <span v-if="review.productBrand !== 'No brand'" class="tag">{{ review.productBrand }}</span>
            </div>
          </div>
        </div>
      </div>
      <!-- Suggested products -->
      <div class="card" v-if="suggestions?.suggestions?.length">
        <div>
          <h3>Suggested products</h3>
          <p class="suggestions-note">
            Based on {{ suggestions.based_on.top_categories.join(', ') }} preferences
            · {{ suggestions.based_on.similar_users_count }} similar users considered
          </p>
        </div>
        <div class="suggestions-grid">
          <RouterLink
            v-for="product in suggestions.suggestions"
            :key="product.id"
            :to="`/products/${product.id}`"
            class="suggestion-card"
          >
            <img :src="product.thumbnail" :alt="product.title" class="suggestion-thumb" />
            <div class="suggestion-info">
              <span class="suggestion-title">{{ product.title }}</span>
              <span class="suggestion-meta">{{ product.category }} · ${{ product.price }}</span>
              <span class="suggestion-rating">★ {{ product.rating }}</span>
            </div>
          </RouterLink>
        </div>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getUser, getUserSuggestions } from '../../services/api'

const route = useRoute()
const user = ref(null)
const loading = ref(true)
const error = ref(null)
const suggestions = ref(null)
const suggestionsLoading = ref(true)

onMounted(async () => {
  try {
    const res = await getUser(route.params.id)
    user.value = res.data

    // Buscar sugestões em paralelo
    const suggestionsRes = await getUserSuggestions(route.params.id)
    suggestions.value = suggestionsRes.data
  } catch (e) {
    error.value = 'Failed to load user'
  } finally {
    loading.value = false
    suggestionsLoading.value = false
  }
})
</script>

<style scoped>
.user-detail {
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

.user-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  object-fit: cover;
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
  align-items: center;
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

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.75rem;
}

.summary-stat {
  background: #f9fafb;
  border-radius: 8px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.summary-label {
  font-size: 11px;
  color: #6b7280;
}

.summary-value {
  font-size: 1.25rem;
  font-weight: 500;
  color: #111827;
}

.row-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.sub-label {
  font-size: 11px;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 8px;
}

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

.rating-bars {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.rating-bar-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
}

.rating-num {
  color: #6b7280;
  width: 24px;
  flex-shrink: 0;
}

.rating-track {
  flex: 1;
  height: 6px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}

.rating-fill {
  height: 100%;
  background: #378ADD;
  border-radius: 4px;
}

.rating-count {
  color: #6b7280;
  width: 16px;
  text-align: right;
  flex-shrink: 0;
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
  margin-bottom: 6px;
}

.review-product {
  display: flex;
  align-items: center;
  gap: 8px;
}

.review-thumb {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  object-fit: cover;
}

.review-title {
  font-size: 0.85rem;
  font-weight: 500;
  color: #1d4ed8;
  text-decoration: none;
}

.review-title:hover {
  text-decoration: underline;
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
  margin-bottom: 6px;
}

.review-tags {
  display: flex;
  gap: 6px;
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

  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .row-inner {
    grid-template-columns: 1fr;
  }

  .info-email {
    overflow-x: auto;
    max-width: 180px;
    white-space: nowrap;
  }

  .suggestions-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  
}

.left-col {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.suggestions-note {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 2px;
}

.suggestions-grid {
  display: flex;
  gap: 0.75rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.suggestion-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-decoration: none;
  padding: 0.75rem;
  border: 0.5px solid #e5e7eb;
  border-radius: 8px;
  transition: background 0.15s;
  min-width: 130px;
  max-width: 130px;
  flex-shrink: 0;
}

.suggestion-card:hover {
  background: #f9fafb;
}

.suggestion-thumb {
  width: 100%;
  aspect-ratio: 1;
  object-fit: contain;
  border-radius: 6px;
  background: #f9fafb;
  padding: 4px;
}

.suggestion-title {
  font-size: 0.75rem;
  font-weight: 500;
  color: #111827;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.suggestion-meta {
  font-size: 0.7rem;
  color: #6b7280;
}

.suggestion-rating {
  font-size: 0.7rem;
  color: #BA7517;
}
</style>