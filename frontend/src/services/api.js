import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
})

export const getUsersSummary = () => api.get('/users/summary')
export const getProductsSummary = () => api.get('/products/summary')
export const getUsers = () => api.get('/users/list')
export const getUser = (id) => api.get(`/users/${id}`)
export const getProducts = () => api.get('/products/list')
export const getProduct = (id) => api.get(`/products/${id}`)
export const getProductsInsights = () => api.get('/products/insights')
export const getUsersInsights = () => api.get('/users/insights')
export const getProductsAggregation = () => api.get('/products/aggregation')
export const getUsersGeo = () => api.get('/users/geo')
export const aiSearch = (query) => api.post('/search', { query })

export const getUserSuggestions = (id) => api.get(`/users/${id}/suggestions`)