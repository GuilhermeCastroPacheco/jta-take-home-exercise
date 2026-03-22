import { ref, onMounted } from 'vue'
import { getProductsSummary, getProducts, getProductsInsights } from '../services/api'

export function useProducts() {
  const productsSummary = ref(null)
  const products = ref([])
  const insights = ref(null)
  const loading = ref(true)
  const error = ref(null)

  onMounted(async () => {
    try {
      const [summaryRes, productsRes, insightsRes] = await Promise.all([
        getProductsSummary(),
        getProducts(),
        getProductsInsights()
      ])
      productsSummary.value = summaryRes.data
      products.value = productsRes.data
      insights.value = insightsRes.data
    } catch (e) {
      error.value = 'Failed to load products data'
    } finally {
      loading.value = false
    }
  })

  return { productsSummary, products, insights, loading, error }
}