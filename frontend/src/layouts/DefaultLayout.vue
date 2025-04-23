<template>
  <div class="min-h-screen flex flex-col bg-neutral text-gray-900">
    <!-- Header -->
    <header class="bg-white shadow border-b border-gray-200">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <router-link to="/" class="text-2xl font-extrabold text-primary">
          📚 Bookstore
        </router-link>

        <nav class="relative flex items-center gap-4 text-sm sm:text-base">
          <router-link to="/" class="text-gray-700 hover:text-primary transition">Home</router-link>

          <template v-if="auth.isAuthenticated">
            <!-- 👤 Profile Dropdown -->
            <div class="relative" ref="dropdownRef">
              <button
                @click="showDropdown = !showDropdown"
                class="flex items-center gap-2 text-gray-700 hover:text-primary transition"
              >
                👋 Hi, {{ auth.user?.first_name === 'Company' && auth.user?.last_name === 'Account' ? auth.user?.company_name : auth.user?.first_name }}
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- Dropdown Menu -->
              <div
                v-if="showDropdown"
                class="absolute right-0 mt-2 w-40 bg-white border rounded shadow z-50"
              >
              <router-link to="/dashboard" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                {{ dashboardLabel }}
              </router-link>

                <!-- Future: Profile page -->
                <router-link
                  to="/profile"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >Profile</router-link>

                <button
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-red-500 hover:bg-red-100"
                >Logout</button>
              </div>
            </div>
            <router-link
              v-if="auth.user?.user_type === 'buyer'"
              to="/cart"
              class="hover:text-primary"
            >
              Cart
            </router-link>
          </template>

          <template v-else>
            <router-link to="/login" class="text-gray-700 hover:text-primary transition">Login</router-link>
            <router-link to="/register" class="text-gray-700 hover:text-primary transition">Register</router-link>
          </template>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow container mx-auto px-4 py-10">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t text-center text-sm text-gray-500 py-4">
      © {{ new Date().getFullYear() }} Bookstore Inc.
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useClickOutside } from '@/composables/useClickOutside'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const showDropdown = ref(false)
const dropdownRef = ref(null)

const dashboardLabel = computed(() => {
  if (!auth.user) return 'Dashboard'

  switch (auth.user.user_type) {
    case 'buyer':
      return 'My Orders'
    case 'seller':
      return 'My Books'
    case 'admin':
      return 'Admin Panel'
    default:
      return 'Dashboard'
  }
})

useClickOutside(dropdownRef, () => {
  showDropdown.value = false
})

const handleLogout = () => {
  router.push('/')
  auth.logout()
  showDropdown.value = false
}
</script>
