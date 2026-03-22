import { ref, onMounted } from 'vue'
import { getUsersSummary, getUsers } from '../services/api'

export function useUsers() {
  const usersSummary = ref(null)
  const users = ref([])
  const loading = ref(true)
  const error = ref(null)

  onMounted(async () => {
    try {
      const [summaryRes, usersRes] = await Promise.all([
        getUsersSummary(),
        getUsers()
      ])
      usersSummary.value = summaryRes.data
      users.value = usersRes.data
    } catch (e) {
      error.value = 'Failed to load users data'
    } finally {
      loading.value = false
    }
  })

  return { usersSummary, users, loading, error }
}