<template>
  <div class="search-bar-wrapper">
    <div class="search-bar" :class="{ loading: isLoading }">
      <i class="pi pi-search search-icon" />
      <input
        v-model="query"
        type="text"
        placeholder="Search anything... e.g. 'female users aged 26-30' or 'low stock sunglasses'"
        class="search-input"
        @keydown.enter="handleSearch"
        :disabled="isLoading"
      />
      <button
        v-if="query && !isLoading"
        class="search-btn"
        @click="handleSearch"
      >
        Go
      </button>
      <span v-if="isLoading" class="loading-text">Thinking...</span>
    </div>
    <p v-if="errorMsg" class="search-error">{{ errorMsg }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { aiSearch } from '../services/api'

const router = useRouter()
const query = ref('')
const isLoading = ref(false)
const errorMsg = ref('')

const handleSearch = async () => {
  if (!query.value.trim()) return

  isLoading.value = true
  errorMsg.value = ''

  try {
    const res = await aiSearch(query.value)
    const result = res.data

    if (result.error) {
      errorMsg.value = result.error
      return
    }

    const params = new URLSearchParams()
    if (result.filters) {
      Object.entries(result.filters).forEach(([key, val]) => {
        if (val) params.set(key, val)
      })
    }
    if (result.sortField) params.set('sort', result.sortField)
    if (result.sortDir) params.set('dir', result.sortDir)

    const queryString = params.toString()
    const fullRoute = queryString ? `${result.route}?${queryString}` : result.route

    query.value = ''
    router.push(fullRoute)

  } catch (e) {
    errorMsg.value = 'Something went wrong. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.search-bar-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #ffffff;
  border: 0.5px solid #e5e7eb;
  border-radius: 12px;
  padding: 0.75rem 1rem;
  transition: border-color 0.15s;
}

.search-bar:focus-within {
  border-color: #378ADD;
}

.search-bar.loading {
  opacity: 0.7;
}

.search-icon {
  color: #6b7280;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 0.875rem;
  font-family: inherit;
  color: #111827;
  background: transparent;
}

.search-input::placeholder {
  color: #9ca3af;
}

.search-input:disabled {
  cursor: not-allowed;
}

.search-btn {
  padding: 4px 12px;
  background: #378ADD;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  font-family: inherit;
  cursor: pointer;
  flex-shrink: 0;
}

.search-btn:hover {
  background: #185FA5;
}

.loading-text {
  font-size: 0.8rem;
  color: #6b7280;
  flex-shrink: 0;
}

.search-error {
  font-size: 0.8rem;
  color: #b91c1c;
  padding: 0 0.25rem;
}
</style>