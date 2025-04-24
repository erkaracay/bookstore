<template>
  <div class="pt-10 space-y-6">
    <h1 class="text-2xl font-bold text-primary text-center">
      {{ pageTitle }}
    </h1>

    <div v-if="loading" class="text-center text-gray-500">Loading...</div>

    <!-- Buyer: Purchase History -->
    <div v-else-if="auth.user?.user_type === 'buyer'">
      <div v-if="orders.length === 0" class="text-gray-500">
        You haven't placed any orders yet.
      </div>

      <ul v-else class="space-y-6">
        <li
          v-for="order in orders"
          :key="order.id"
          class="bg-white border rounded shadow p-4"
        >
          <!-- Order Metadata -->
          <div class="mb-3">
            <p class="text-sm text-gray-500">
              {{ new Date(order.created_at).toLocaleString('en-GB', { hour12: false }) }}
              — {{ formatRelativeTime(order.created_at) }}
            </p>
            <p class="text-sm mt-1">
              Status:
              <span :class="statusBadgeClass(order.status)">
                {{ capitalize(order.status) }}
              </span>
            </p>
            <p class="text-sm text-gray-600 font-medium mt-1">
              Total: ${{ Number(order.total_price).toFixed(2) }}
            </p>
          </div>

          <!-- Items -->
          <ul class="mt-2 space-y-1 border-t pt-3 pl-4">
            <li
              v-for="item in order.items"
              :key="`${order.id}-${item.book?.id || item.book}`"
              class="text-sm text-gray-700"
            >
              📚 {{ item.quantity }} × {{ item.book?.title || 'Unknown Book' }}
            </li>
          </ul>
        </li>
      </ul>
    </div>

    <!-- Seller -->
    <div v-else-if="auth.user?.user_type === 'seller'">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Add, Edit or Delete Books</h2>
        <router-link
          to="/books/create"
          class="text-sm bg-primary text-white px-3 py-1 rounded hover:bg-opacity-90 transition"
        >
          + Add Book
        </router-link>
      </div>

      <div v-if="books.length === 0" class="text-gray-500">No books listed yet.</div>

      <ul v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <li
          v-for="book in books"
          :key="book.id"
          class="bg-white border p-4 rounded shadow-sm space-y-1"
        >
          <p class="text-lg font-semibold text-gray-800">{{ book.title }}</p>
          <p class="text-sm text-gray-500">by {{ book.author }}</p>
          <p class="text-sm text-gray-700 font-medium">${{ book.price }}</p>

          <div class="flex gap-2 mt-3">
            <router-link
              :to="`/books/${book.id}/edit`"
              class="text-sm text-blue-600 hover:underline"
            >
              Edit
            </router-link>
            <button
              @click="promptDelete(book.id)"
              class="text-sm text-red-600 hover:underline"
            >
              Delete
            </button>
          </div>
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

  <ModalConfirm
  :show="showModal"
  title="Delete Book"
  message="Are you sure you want to delete this book? This action cannot be undone."
  confirm-text="Delete"
  @cancel="showModal = false"
  @confirm="confirmDelete"
/>
</template>

<script setup>
import { ref, onMounted, computed, h } from 'vue'
import axios from '@/utils/axios'
import { useAuthStore } from '@/store/auth'
import dayjs from '@/utils/dayjs'
import ModalConfirm from '@/components/ModalConfirm.vue'
import { useToast } from 'vue-toastification'

const auth = useAuthStore()
const loading = ref(true)
const orders = ref([])
const books = ref([])

const showModal = ref(false)
const bookToDelete = ref(null)
const toast = useToast()
const recentlyDeleted = ref(null)
let undoTimer = null

const pageTitle = computed(() => {
  const type = auth.user?.user_type
  if (type === 'buyer') return 'Purchase History'
  if (type === 'seller') return 'Your Books'
  return 'Dashboard'
})

onMounted(async () => {
  try {
    const userType = auth.user?.user_type

    if (userType === 'buyer') {
      const res = await axios.get('/orders/')
      orders.value = res.data.reverse()
    }

    if (userType === 'seller') {
      const res = await axios.get('/books/', {
        params: { seller: auth.user.email }
      })
      books.value = res.data
    }

    // Admin view: no data yet
  } catch (err) {
    console.error('Dashboard error:', err)
  } finally {
    loading.value = false
  }
})

function promptDelete(bookId) {
  showModal.value = true
  bookToDelete.value = bookId
}

async function confirmDelete() {
  if (!bookToDelete.value) return

  const id = bookToDelete.value
  const book = books.value.find(b => b.id === id)

  if (!book) return

  books.value = books.value.filter(b => b.id !== id)
  recentlyDeleted.value = book

  // Show toast using a custom Vue component
  toast(
    () =>
      h('div', { class: 'flex justify-between items-center gap-3' }, [
        h('span', '📚 Book deleted.'),
        h(
          'button',
          {
            class: 'bg-white text-blue-600 px-3 py-1 rounded text-sm hover:bg-gray-100 transition',
            onClick: () => {
              books.value.push(book)
              books.value.sort((a, b) => a.id - b.id)
              recentlyDeleted.value = null
              clearTimeout(undoTimer)
              toast.clear()
            },
          },
          'Undo'
        ),
      ]),
    {
      timeout: 5000,
      closeOnClick: false,
      hideProgressBar: false,
    }
  )

  clearTimeout(undoTimer)
  undoTimer = setTimeout(async () => {
    if (recentlyDeleted.value?.id === id) {
      try {
        await axios.delete(`/books/${id}/`)
      } catch (err) {
        console.error('Actual delete failed:', err)
      } finally {
        recentlyDeleted.value = null
      }
    }
  }, 5000)

  showModal.value = false
  bookToDelete.value = null
}

function formatRelativeTime(iso) {
  return dayjs(iso).fromNow() // e.g. "3 hours ago"
}

function statusBadgeClass(status) {
  switch (status) {
    case 'pending':
      return 'inline-block text-yellow-800 bg-yellow-100 px-2 py-0.5 rounded text-xs font-semibold'
    case 'shipped':
      return 'inline-block text-green-800 bg-green-100 px-2 py-0.5 rounded text-xs font-semibold'
    default:
      return 'inline-block text-gray-600 bg-gray-100 px-2 py-0.5 rounded text-xs font-semibold'
  }
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>
