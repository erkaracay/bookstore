import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import BookDetail from '@/pages/BookDetail.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/books/:slug', component: BookDetail }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
