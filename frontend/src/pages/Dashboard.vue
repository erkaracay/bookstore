<template>
  <div class="pt-10 space-y-6">
    <h1 class="text-2xl font-bold text-primary text-center">
      {{ pageTitle }}
    </h1>

    <div v-if="loading" class="text-center text-gray-500">Loading...</div>

    <!-- Buyer -->
    <div v-else-if="auth.user?.user_type === 'buyer'">
      <h2 class="text-xl font-semibold mb-4">Your Orders</h2>
      <div v-if="orders.length === 0" class="text-gray-500">No orders yet.</div>
      <ul v-else class="space-y-3">
        <li v-for="order in orders" :key="order.id" class="bg-white border p-4 rounded shadow-sm">
          <p class="text-sm text-gray-600">Order #{{ order.id }} – {{ formatDate(order.created_at) }}</p>
          <p class="text-sm">Status: <span class="font-medium">{{ order.status }}</span></p>
          <p class="text-sm text-gray-700 font-semibold">Total: ${{ order.total_price }}</p>
        </li>
      </ul>
    </div>

    <!-- Seller -->
    <div v-else-if="auth.user?.user_type === 'seller'">
      <h2 class="text-xl font-semibold mb-4">Your Books</h2>
      <div v-if="books.length === 0" class="text-gray-500">No books listed yet.</div>
      <ul v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <li v-for="book in books" :key="book.id" class="bg-white border p-4 rounded shadow-sm">
          <p class="text-lg font-semibold text-gray-800">{{ book.title }}</p>
          <p class="text-sm text-gray-500">by {{ book.author }}</p>
          <p class="text-sm text-gray-700 font-medium">${{ book.price }}</p>
        </li>
      </ul>
    </div>

    <!-- Admin -->
    <div v-else-if="auth.user?.user_type === 'admin'">
      <h2 class="text-xl font-semibold mb-4">Admin Panel</h2>
      <p class="text-sm text-gray-500 mb-4">Redirecting you to the Django Admin Panel...</p>
      <a
        href="http://localhost:8000/admin/"
        target="_blank"
        class="inline-block bg-primary text-white px-4 py-2 rounded hover:bg-opacity-90 text-sm"
      >
        Open Django Admin
      </a>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from '@/utils/axios'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()

const loading = ref(true)
const orders = ref([])
const books = ref([])

const pageTitle = computed(() => {
  const type = auth.user?.user_type
  if (type === 'buyer') return 'My Orders'
  if (type === 'seller') return 'My Books'
  return 'Dashboard'
})


onMounted(async () => {
  try {
    const userType = auth.user?.user_type

    if (userType === 'buyer') {
      const res = await axios.get('/orders/')
      orders.value = res.data
    }

    if (userType === 'seller') {
      const res = await axios.get('/books/')
      books.value = res.data.filter(book => book.author === auth.user.first_name) // adjust filter as needed
    }

    // Admin view: no data yet
  } catch (err) {
    console.error('Dashboard error:', err)
  } finally {
    loading.value = false
  }
})

function formatDate(iso) {
  return new Date(iso).toLocaleDateString()
}
</script>
