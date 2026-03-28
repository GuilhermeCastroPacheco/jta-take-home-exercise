import { ref, onMounted } from 'vue'
import { getProductsSummary, getProducts, getProductsInsights, getProductsAggregation } from '../services/api'

export function useProducts() {
  const productsSummary = ref(null)
  const products = ref([])
  const insights = ref(null)
  const productsAggregation = ref(null)
  const loading = ref(true)
  const error = ref(null)

  onMounted(async () => {
    try {
      const [summaryRes, productsRes, insightsRes, aggregationRes] = await Promise.all([
        getProductsSummary(),
        getProducts(),
        getProductsInsights(),
        getProductsAggregation()
      ])
      productsSummary.value = summaryRes.data
      products.value = productsRes.data
      insights.value = insightsRes.data
      productsAggregation.value = aggregationRes.data
    } catch (e) {
      error.value = 'Failed to load products data'
    } finally {
      loading.value = false
    }
  })

  return { productsSummary, products, insights, productsAggregation, loading, error }
}