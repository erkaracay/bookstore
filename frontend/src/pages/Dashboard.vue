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
      <ul v-else class="space-y-4">
        <li
          v-for="order in orders"
          :key="order.id"
          class="bg-white border rounded shadow p-4"
        >
          <p class="font-semibold text-sm text-gray-800 mb-1">
            Order #{{ order.id }} – {{ formatDate(order.created_at) }}
          </p>
          <p class="text-sm mb-2">
            Status:
            <span :class="statusBadgeClass(order.status)">
              {{ capitalize(order.status) }}
            </span>
          </p>
          <p class="text-sm text-gray-600 mb-3 font-medium">Total: ${{ Number(order.total_price).toFixed(2) }}</p>

          <ul class="pl-4 space-y-1">
            <li
              v-for="item in order.items"
              :key="`${order.id}-${item.book}`"
              class="text-sm text-gray-700"
            >
              📚 {{ item.quantity }} × {{ item.book.title }}
            </li>
          </ul>
          <button
            v-if="order.status === 'pending'"
            @click="promptCancel(order.id)"
            class="mt-3 inline-block text-sm text-red-600 hover:underline"
          >
            Cancel Order
          </button>
          <p
            v-if="cancelSuccessId === order.id"
            class="text-green-600 text-sm mt-2"
          >
            ✅ Order cancelled successfully.
          </p>
        </li>
      </ul>
      <Teleport to="body">
        <div
          v-if="showConfirm"
          class="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
        >
          <div class="bg-white rounded shadow p-6 max-w-sm w-full space-y-4">
            <h2 class="text-lg font-semibold text-gray-800">Cancel this order?</h2>
            <p class="text-sm text-gray-600">Are you sure you want to cancel Order #{{ confirmTargetOrderId }}?</p>

            <div class="flex justify-end gap-3 mt-4">
              <button
                @click="showConfirm = false"
                class="px-4 py-2 text-sm bg-gray-200 rounded hover:bg-gray-300"
              >
                No, go back
              </button>
              <button
                @click="confirmCancel"
                class="px-4 py-2 text-sm bg-red-600 text-white rounded hover:bg-red-700"
              >
                Yes, cancel it
              </button>
            </div>
          </div>
        </div>
      </Teleport>
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
const cancelSuccessId = ref(null)
const showConfirm = ref(false)
const confirmTargetOrderId = ref(null)

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

function statusBadgeClass(status) {
  switch (status) {
    case 'pending':
      return 'inline-block text-yellow-800 bg-yellow-100 px-2 py-0.5 rounded text-xs font-semibold'
    case 'shipped':
      return 'inline-block text-green-800 bg-green-100 px-2 py-0.5 rounded text-xs font-semibold'
    case 'cancelled':
      return 'inline-block text-red-800 bg-red-100 px-2 py-0.5 rounded text-xs font-semibold'
    default:
      return 'inline-block text-gray-600 bg-gray-100 px-2 py-0.5 rounded text-xs font-semibold'
  }
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1)
}

function promptCancel(orderId) {
  confirmTargetOrderId.value = orderId
  showConfirm.value = true
}

async function confirmCancel() {
  const orderId = confirmTargetOrderId.value
  try {
    await axios.post(`/orders/${orderId}/cancel/`)
    orders.value = orders.value.map(o =>
      o.id === orderId ? { ...o, status: 'cancelled' } : o
    )
    cancelSuccessId.value = orderId
  } catch (err) {
    console.error('Failed to cancel order:', err)
  } finally {
    showConfirm.value = false
    confirmTargetOrderId.value = null
  }

  setTimeout(() => {
    cancelSuccessId.value = null
  }, 4000)
}
</script>
