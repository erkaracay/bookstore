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
      class="bg-white hover:shadow-lg transition rounded-lg border border-gray-200 p-4 flex flex-col"
    >
      <div class="flex-1">
        <h2 class="text-lg font-semibold text-gray-800 mb-1">
          {{ book.title }}
        </h2>
        <p class="text-sm text-gray-500 mb-2">by {{ book.author }}</p>
      </div>

      <div class="mt-auto pt-4 border-t">
        <p class="text-primary text-lg font-bold">
          {{ book.price != null ? `$${Number(book.price).toFixed(2)}` : 'N/A' }}
        </p>
      </div>
    </router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from '@/utils/axios.js'

const books = ref([])
const loading = ref(true)

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
</script>

<script>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
export default {
  layout: DefaultLayout,
}
</script>
