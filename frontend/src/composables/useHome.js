import { ref, onMounted } from 'vue'
import { getUsersSummary, getProductsSummary } from '../services/api'

export function useHome() {
  const usersSummary = ref(null)
  const productsSummary = ref(null)
  const loading = ref(true)
  const error = ref(null)

  onMounted(async () => {
    try {
      const [usersRes, productsRes] = await Promise.all([
        getUsersSummary(),
        getProductsSummary()
      ])
      usersSummary.value = usersRes.data
      productsSummary.value = productsRes.data
    } catch (e) {
      error.value = 'Failed to load dashboard data'
    } finally {
      loading.value = false
    }
  })

  return { usersSummary, productsSummary, loading, error }
}