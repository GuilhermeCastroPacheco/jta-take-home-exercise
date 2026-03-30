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
  font-family: 'Inter', sans-serif;
}
</style>