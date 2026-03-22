import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000'
})

export const getUsersSummary = () => api.get('/users/summary')
export const getProductsSummary = () => api.get('/products/summary')
export const getUsers = () => api.get('/users/list')
export const getUser = (id) => api.get(`/users/${id}`)
export const getProducts = () => api.get('/products/list')
export const getProduct = (id) => api.get(`/products/${id}`)
export const getProductsInsights = () => api.get('/products/insights')