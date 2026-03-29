<template>
  <div class="layout">

    <!-- Desktop sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <span class="sidebar-logo">JTA</span>
        <span class="sidebar-sub">Data Scientists</span>
      </div>
      <nav class="sidebar-nav">
        <RouterLink to="/" class="nav-item">
          <i class="pi pi-home" />
          Home
        </RouterLink>
        <RouterLink to="/users" class="nav-item">
          <i class="pi pi-users" />
          Users
        </RouterLink>
        <RouterLink to="/users/all" class="nav-item nav-item--sub">
          <i class="pi pi-table" />
          Users Detail
        </RouterLink>
        <RouterLink to="/products" class="nav-item">
          <i class="pi pi-box" />
          Products
        </RouterLink>
        <RouterLink to="/products/all" class="nav-item nav-item--sub">
          <i class="pi pi-table" />
          Products Detail
        </RouterLink>
      </nav>
    </aside>

    <!-- Mobile topbar -->
    <div class="topbar">
      <Button icon="pi pi-bars" text @click="drawerOpen = true" />
      <span class="sidebar-logo">JTA</span>
    </div>

    <!-- Mobile drawer -->
    <Drawer v-model:visible="drawerOpen" position="left">
      <template #header>
        <span class="sidebar-logo">JTA</span>
      </template>
      <nav class="sidebar-nav">
        <RouterLink to="/" class="nav-item" @click="drawerOpen = false">
          <i class="pi pi-home" />
          Home
        </RouterLink>
        <RouterLink to="/users" class="nav-item" @click="drawerOpen = false">
          <i class="pi pi-users" />
          Users
        </RouterLink>
        <RouterLink to="/users/all" class="nav-item nav-item--sub" @click="drawerOpen = false">
          <i class="pi pi-table" />
          Users Detail
        </RouterLink>
        <RouterLink to="/products" class="nav-item" @click="drawerOpen = false">
          <i class="pi pi-box" />
          Products
        </RouterLink>
        <RouterLink to="/products/all" class="nav-item nav-item--sub" @click="drawerOpen = false">
          <i class="pi pi-table" />
          Products Detail
        </RouterLink>
      </nav>
    </Drawer>

    <!-- Main content -->
    <main class="main-content">
      <slot />
    </main>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import Button from 'primevue/button'
import Drawer from 'primevue/drawer'

const drawerOpen = ref(false)
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
  max-width: 100vw;
  overflow-x: hidden;
}

.sidebar {
  width: 220px;
  min-height: 100vh;
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  border-right: 1px solid #e5e7eb;
  background: #ffffff;
}

.sidebar-header {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 0 0.5rem;
}

.sidebar-logo {
  font-weight: 600;
  font-size: 1.1rem;
  color: #111827;
}

.sidebar-sub {
  font-size: 0.75rem;
  color: #6b7280;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.6rem 0.75rem;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.9rem;
  color: #374151;
  transition: background 0.15s;
}

.nav-item:hover {
  background: #f3f4f6;
}

.nav-item.router-link-active {
  background: #eff6ff;
  color: #1d4ed8;
}

.topbar {
  display: none;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e7eb;
  background: #ffffff;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background: #f9fafb;
  min-width: 0;
  max-width: 100%;
}

.nav-item--sub {
  padding-left: 1.75rem;
  font-size: 0.85rem;
  color: #6b7280;
}

@media (max-width: 768px) {
  .sidebar {
    display: none;
  }

  .topbar {
    display: flex;
  }

  .main-content {
    padding: 5rem 1rem 1rem;
  }
}
</style>