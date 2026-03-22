import { ref } from 'vue'

export function useAppLayout() {
  const isDark = ref(false)
  const drawerOpen = ref(false)

  const toggleDark = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark-mode', isDark.value)
}

  return { isDark, drawerOpen, toggleDark }
}