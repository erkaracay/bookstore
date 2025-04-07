<template>
  <div class="pt-16 pb-10 bg-neutral min-h-screen">
    <div class="max-w-md mx-auto bg-white p-6 rounded shadow">
      <h2 class="text-2xl font-bold text-primary mb-4 text-center">Login</h2>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="email" class="block mb-1 text-sm font-medium">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            class="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
            required
          />
        </div>

        <div>
          <label for="password" class="block mb-1 text-sm font-medium">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
            required
          />
        </div>

        <button
          type="submit"
          class="w-full bg-primary text-white py-2 rounded hover:bg-opacity-90"
        >
          Log In
        </button>
      </form>

      <p class="mt-4 text-sm text-center text-gray-600">
        Don't have an account?
        <router-link to="/register" class="text-primary font-medium">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/utils/axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const router = useRouter()

async function handleLogin() {
  try {
    const res = await axios.post('/api/token/', {
      email: email.value,
      password: password.value,
    })

    // Store tokens
    localStorage.setItem('access', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)

    // Optionally fetch user profile
    const userRes = await axios.get('/users/me/')
    localStorage.setItem('user', JSON.stringify(userRes.data))

    // Navigate to home or dashboard
    router.push('/')
  } catch (err) {
    console.error(err)
    alert('Invalid credentials')
  }
}
</script>

<script>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
export default {
  layout: DefaultLayout,
}
</script>
