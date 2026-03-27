import { ref, onMounted } from 'vue'
import { getUsersSummary, getUsers, getUsersGeo } from '../services/api'

export function useUsers() {
  const usersSummary = ref(null)
  const users = ref([])
  const usersGeo = ref(null)
  const loading = ref(true)
  const error = ref(null)

  onMounted(async () => {
    try {
      const [summaryRes, usersRes, geoRes] = await Promise.all([
        getUsersSummary(),
        getUsers(),
        getUsersGeo()
      ])
      usersSummary.value = summaryRes.data
      users.value = usersRes.data
      usersGeo.value = geoRes.data
    } catch (e) {
      error.value = 'Failed to load users data'
    } finally {
      loading.value = false
    }
  })

  return { usersSummary, users, usersGeo, loading, error }
}