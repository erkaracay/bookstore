<template>
  <div class="pt-10 max-w-3xl mx-auto bg-white rounded shadow p-6">
    <div v-if="loading" class="text-center text-gray-500">Loading book...</div>

    <div v-else-if="!book" class="text-center text-red-500">Book not found.</div>

    <div v-else>
      <h1 class="text-3xl font-bold text-primary mb-2">{{ book.title }}</h1>
      <p class="text-sm text-gray-500 mb-4">by {{ book.author }}</p>
      <p class="text-lg font-semibold text-gray-800">${{ Number(book.price).toFixed(2) }}</p>
      <p class="text-sm text-gray-500 mb-4">Stock: {{ book.stock }}</p>
      <p class="mb-6 text-gray-700">{{ book.description }}</p>

      <div
        v-if="auth.user?.user_type === 'buyer'"
        class="flex items-center gap-4 mt-6"
      >
      <!-- Quantity Input with +/- buttons -->
      <div class="flex items-center border rounded px-2 py-1">
        <button
          type="button"
          @click="quantity = Math.max(1, quantity - 1)"
          class="text-lg px-2 text-gray-500 hover:text-primary"
        >
          −
        </button>

        <input
          type="number"
          v-model.number="quantity"
          min="1"
          :max="book.stock"
          class="w-12 text-center outline-none"
        />

        <button
          type="button"
          @click="quantity = Math.min(book.stock, quantity + 1)"
          class="text-lg px-2 text-gray-500 hover:text-primary"
        >
          +
        </button>
      </div>

      <!-- Add to Cart Button -->
      <button
        @click="addToCart"
        class="bg-primary text-white px-5 py-2 rounded hover:bg-opacity-90 transition whitespace-nowrap"
        :disabled="adding || book.stock === 0 || quantity < 1"
      >
        {{ adding ? 'Adding...' : book.stock === 0 ? 'Out of Stock' : 'Add to Cart' }}
      </button>
    </div>

      <p v-if="addedSuccess" class="text-green-600 mt-4">✔️ Book added to cart!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/utils/axios'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const slug = route.params.slug
const auth = useAuthStore()

const loading = ref(true)
const book = ref(null)
const adding = ref(false)
const addedSuccess = ref(false)
const quantity = ref(1)

watch(quantity, (val) => {
  if (val > book.value.stock) {
    quantity.value = book.value.stock
  } else if (val < 1) {
    quantity.value = 1
  }
})

async function addToCart() {
  if (!book.value || quantity.value < 1) return

  try {
    adding.value = true
    await axios.post('/cart/items/', {
      book_id: book.value.id,
      quantity: quantity.value,
    })
    addedSuccess.value = true
  } catch (err) {
    console.error('Add to cart failed:', err)
    alert('Could not add book to cart.')
  } finally {
    adding.value = false
  }
}

onMounted(async () => {
  try {
    const res = await axios.get(`/books/${slug}/`)
    book.value = res.data
  } catch (err) {
    console.error('Error loading book:', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
  input[type="number"]::-webkit-inner-spin-button,
  input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  input[type="number"] {
    -moz-appearance: textfield; /* Firefox */
}
</style>