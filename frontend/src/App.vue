<template>
  <AppSidebar>
    <RouterView />
  </AppSidebar>
</template>

<script setup>
import AppSidebar from './components/AppSidebar.vue'
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  background: var(--p-surface-50);
  color: var(--p-text-color);
  transition: background 0.3s, color 0.3s;
  font-family: 'Inter', sans-serif;
}
</style>