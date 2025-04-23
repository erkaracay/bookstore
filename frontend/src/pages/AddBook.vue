<template>
  <div class="max-w-xl mx-auto pt-10 pb-16">
    <h1 class="text-2xl font-bold mb-6 text-primary text-center">📘 Add a New Book</h1>

    <form @submit.prevent="submitBook" class="space-y-6">
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

      <!-- 📖 Description -->
      <div>
        <label class="block text-sm font-medium mb-1" for="description">Description</label>
        <textarea
          id="description"
          v-model="form.description"
          rows="4"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
        ></textarea>
        <p v-if="errors.description" class="text-sm text-red-600 mt-1">{{ errors.description }}</p>
      </div>

      <!-- 💰 Price -->
      <FormField
        v-model="form.price"
        field="price"
        name="Price"
        type="number"
        :error="errors.price"
        @validate="validateField"
      />

      <!-- 📦 Stock -->
      <FormField
        v-model="form.stock"
        field="stock"
        name="Stock"
        type="number"
        :error="errors.stock"
        @validate="validateField"
      />

      <!-- 📅 Published Date -->
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
        {{ loading ? 'Saving...' : 'Add Book' }}
      </button>

      <p v-if="success" class="text-green-600 text-center mt-4">
        ✔️ Book created successfully!
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { z } from 'zod'
import axios from '@/utils/axios'
import FormField from '@/components/form/FormField.vue'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()

// ✅ Form State
const form = reactive({
  title: '',
  author: auth.user?.first_name || '',
  description: '',
  price: '',
  stock: '',
  published_date: '',
})

const errors = reactive({})
const loading = ref(false)
const success = ref(false)

// ✅ Zod Schema
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

function formatDateToString(date) {
  if (!(date instanceof Date)) return ''
  return date.toISOString().split('T')[0] // YYYY-MM-DD
}

async function submitBook() {
  try {
    loading.value = true
    success.value = false
    errors.value = {}

    const parsed = schema.parse({
      ...form,
      price: parseFloat(form.price),
      stock: parseInt(form.stock),
      published_date: formatDateToString(form.published_date),
    })

    await axios.post('/books/', parsed)

    success.value = true
    Object.keys(form).forEach(key => (form[key] = ''))
  } catch (err) {
    if (err.name === 'ZodError') {
      err.errors.forEach(e => (errors[e.path[0]] = e.message))
    } else {
      console.error('Book creation failed:', err)
      alert('Failed to create book. Check console.')
    }
  } finally {
    loading.value = false
  }
}
</script>
