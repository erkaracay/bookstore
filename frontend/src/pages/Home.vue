<template>
  <h1 class="text-3xl sm:text-4xl font-bold mb-6 text-primary text-center">
    Browse Our Collection
  </h1>

  <div v-if="loading" class="text-center text-gray-500">
    Loading books...
  </div>

  <div v-else-if="validBooks.length === 0" class="text-center text-gray-500">
    No books available at the moment.
  </div>

  <div v-else class="grid gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
    <router-link
      v-for="book in validBooks"
      :key="book.id"
      :to="`/books/${book.slug}`"
      :class="[
        'bg-white hover:shadow-lg transition rounded-lg border p-4 flex flex-col',
        book.stock <= 3 ? 'border-red-300' : 'border-gray-200'
      ]"    >
      <div class="flex-1">
        <span
          v-if="book.stock === 0"
          class="inline-block self-start text-xs font-semibold text-white bg-red-500 px-2 py-0.5 rounded mb-2"
        >
          ❌ Out of Stock
        </span>

        <h2 class="text-lg font-semibold text-gray-800 mb-1">
          {{ book.title }}
        </h2>
        <p class="text-sm text-gray-500 mb-2">by {{ book.author }}</p>
      </div>

      <div class="mt-auto pt-4 border-t flex items-center justify-between">
        <p class="text-primary text-lg font-bold">
          {{ book.price != null ? `$${Number(book.price).toFixed(2)}` : 'N/A' }}
        </p>

        <button
          v-if="auth.user?.user_type === 'buyer'"
          @click.stop.prevent="addToOrder(book.id)"
          class="text-sm px-3 py-1 rounded transition"
          :class="[
            book.stock === 0
              ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
              : 'bg-primary text-white hover:bg-opacity-90'
          ]"
          :disabled="book.stock === 0"
        >
          {{ book.stock === 0 ? 'Out of Stock' : 'Add' }}
        </button>
      </div>
      <!-- Low stock warning -->
      <p
        v-if="book.stock > 0 && book.stock <= 10"
        class="text-red-600 text-xs mt-1 font-medium"
      >
        ⚠️ Only {{ book.stock }} left in stock!
      </p>

      <p
        v-if="lastAddedBookId === book.id"
        class="text-green-600 text-sm mt-2"
      >
        ✅ Book added to order!
      </p>
    </router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from '@/utils/axios.js'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()
const books = ref([])
const loading = ref(true)
const lastAddedBookId = ref(null)
const validBooks = computed(() =>
  books.value.filter(book => book?.title && book?.slug)
)

onMounted(async () => {
  try {
    const res = await axios.get('/books/')
    console.log('📚 API raw response:', res.data)
    books.value = res.data
  } catch (error) {
    console.error('❌ Error fetching books:', error)
  } finally {
    loading.value = false
  }
})

async function addToOrder(bookId) {
  try {
    await axios.post('/orders/', {
      items: [{ book: bookId, quantity: 1 }],
    })

    const book = books.value.find(b => b.id === bookId)
    if (book && book.stock > 0) {
      book.stock -= 1
    }

    lastAddedBookId.value = bookId

    setTimeout(() => {
      lastAddedBookId.value = null
    }, 3000)
  } catch (err) {
    console.error(err)
    alert('Failed to add book to order.')
  }
}

</script>

<script>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
export default {
  layout: DefaultLayout,
}
</script>
