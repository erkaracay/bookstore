<template>
  <div class="max-w-xl mx-auto pt-10 pb-16">
    <h1 class="text-2xl font-bold mb-6 text-primary text-center">✏️ Edit Book</h1>
    <router-link
      to="/dashboard"
      class="text-sm text-primary hover:underline inline-block mb-2"
    >
      ← Back to your books
    </router-link>

    <form @submit.prevent="updateBook" class="space-y-6" v-if="loaded">
      <FormField
        v-model="form.title"
        field="title"
        name="Title"
        :error="errors.title"
        @validate="validateField"
      />
      <FormField
        v-model="form.author"
        field="author"
        name="Author"
        :error="errors.author"
        @validate="validateField"
      />
      <div>
        <label class="block text-sm font-medium mb-1" for="description">Description</label>
        <textarea
          id="description"
          v-model="form.description"
          rows="4"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
        />
        <p v-if="errors.description" class="text-sm text-red-600 mt-1">{{ errors.description }}</p>
      </div>

      <FormField
        v-model="form.price"
        field="price"
        name="Price"
        type="number"
        :error="errors.price"
        @validate="validateField"
      />
      <FormField
        v-model="form.stock"
        field="stock"
        name="Stock"
        type="number"
        :error="errors.stock"
        @validate="validateField"
      />
      <div>
        <label class="block text-sm font-medium mb-1" for="published_date">Published Date</label>
        <FormField
          v-model="form.published_date"
          field="published_date"
          name=""
          type="date"
          :error="errors.published_date"
          @validate="validateField"
        />
      </div>

      <button
        type="submit"
        class="w-full bg-primary text-white py-2 rounded hover:bg-opacity-90 transition"
        :disabled="loading"
      >
        {{ loading ? 'Saving...' : 'Update Book' }}
      </button>

      <p v-if="success" class="text-green-600 text-center mt-4">
        ✔️ Book updated successfully!
      </p>
    </form>

    <p v-if="!loaded && !loading" class="text-center text-red-600">❌ Failed to load book.</p>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/utils/axios'
import FormField from '@/components/form/FormField.vue'
import { z } from 'zod'

const route = useRoute()
const router = useRouter()
const bookId = route.params.id

const loading = ref(false)
const loaded = ref(false)
const success = ref(false)

const form = reactive({
  title: '',
  author: '',
  description: '',
  price: '',
  stock: '',
  published_date: '',
})

const errors = reactive({})

const schema = z.object({
  title: z.string().min(2, 'Title is required'),
  author: z.string().min(2, 'Author is required'),
  description: z.string().min(5, 'Description is too short'),
  price: z.number().min(0.01, 'Price must be greater than 0'),
  stock: z.number().int().min(0, 'Stock must be a whole number'),
  published_date: z
    .string()
    .regex(/^\d{4}-\d{2}-\d{2}$/, 'Date must be in YYYY-MM-DD format')
    .refine(val => !isNaN(Date.parse(val)), { message: 'Invalid date' }),
})

function validateField(field) {
  try {
    schema.pick({ [field]: true }).parse({ [field]: form[field] })
    errors[field] = ''
  } catch (err) {
    errors[field] = err.errors?.[0]?.message || 'Invalid'
  }
}

onMounted(async () => {
  try {
    const res = await axios.get(`/books/${bookId}/`)
    const book = res.data
    form.title = book.title
    form.author = book.author
    form.description = book.description
    form.price = book.price
    form.stock = book.stock
    form.published_date = book.published_date // ISO string
    loaded.value = true
  } catch (err) {
    console.error('Failed to load book:', err)
  }
})

async function updateBook() {
  try {
    loading.value = true
    success.value = false

    form.published_date = new Date(form.published_date).toISOString().split('T')[0]

    const parsed = schema.parse({
      ...form,
      price: parseFloat(form.price),
      stock: parseInt(form.stock),
    })

    await axios.put(`/books/${bookId}/`, parsed)
    success.value = true
  } catch (err) {
    if (err.name === 'ZodError') {
      err.errors.forEach(e => (errors[e.path[0]] = e.message))
    } else {
      console.error('Update failed:', err)
      alert('Update failed')
    }
  } finally {
    loading.value = false
  }
}
</script>
