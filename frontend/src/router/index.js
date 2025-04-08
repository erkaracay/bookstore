import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import Dashboard from '@/pages/Dashboard.vue'
import NotFound from '@/pages/NotFound.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login, meta: { guestOnly: true } },
  { path: '/register', name: 'Register', component: Register, meta: { guestOnly: true } },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  // { path: '/admin', component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()

  // If not loaded yet (fresh reload), try to fetch user
  if (!auth.user && auth.access) {
    try {
      await auth.fetchUser()
    } catch (e) {
      // Invalid token
      auth.logout()
    }
  }

  // Redirect unauthenticated users from protected routes
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next({ name: 'Login' })
  }

  // Redirect logged-in users away from login/register
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return next({ name: 'Dashboard' }) // Or maybe 'Home'
  }

  // Role-based protection (later)
  if (to.meta.role && auth.user?.user_type !== to.meta.role) {
    return next({ name: 'Home' }) // Or redirect to AccessDenied.vue
  }

  next()
})

export default router
