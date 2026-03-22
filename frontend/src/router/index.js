import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },
    /*{ path: '/users', component: () => import('../views/users/UsersView.vue') },
    { path: '/users/all', component: () => import('../views/users/UsersTableView.vue') },
    { path: '/users/:id', component: () => import('../views/users/UserDetailView.vue') },
    { path: '/products', component: () => import('../views/products/ProductsView.vue') },
    { path: '/products/all', component: () => import('../views/products/ProductsTableView.vue') },
    { path: '/products/:id', component: () => import('../views/products/ProductDetailView.vue') },*/
  ]
})

export default router
