<template>
  <div class="pt-16 pb-10 bg-neutral min-h-screen px-4">
    <div class="max-w-md mx-auto bg-white p-6 rounded shadow">
      <h2 class="text-2xl font-bold text-primary mb-6 text-center">Login</h2>

      <form @submit.prevent="handleLogin" class="space-y-6 relative">
        <FormField
          v-model="form.email"
          name="Email"
          field="email"
          type="email"
          :error="errors.email"
          hint="Enter your registered email"
          @validate="validateField"
          @focus="focused = 'email'"
          @blur="focused = ''"
          :focused="focused === 'email'"
        />

        <FormField
          v-model="form.password"
          name="Password"
          field="password"
          type="password"
          :error="errors.password"
          hint="Password must be at least 6 characters"
          @validate="validateField"
          @focus="focused = 'password'"
          @blur="focused = ''"
          :focused="focused === 'password'"
        />

        <button
          type="submit"
          class="w-full bg-primary text-white py-2 rounded hover:bg-opacity-90"
        >
          Login
        </button>

        <div v-if="success" class="mt-4 text-sm text-green-600 bg-green-50 p-3 rounded border border-green-300">
          ✅ Login successful! Redirecting...
        </div>
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
import { useRouter } from 'vue-router'
import { z } from 'zod'
import axios from '@/utils/axios'
import FormField from '@/components/form/FormField.vue'

const router = useRouter()
const focused = ref('')
const success = ref(false)

const form = ref({
  email: '',
  password: '',
})

const errors = ref({})

const schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
})

function validateField(field) {
  try {
    schema.pick({ [field]: true }).parse({ [field]: form.value[field] })
    delete errors.value[field]
  } catch (e) {
    errors.value[field] = e.errors?.[0]?.message
  }
}

function validateAll() {
  const result = schema.safeParse(form.value)
  if (!result.success) {
    const fieldErrors = {}
    result.error.errors.forEach(err => {
      fieldErrors[err.path[0]] = err.message
    })
    errors.value = fieldErrors
    return false
  }
  errors.value = {}
  return true
}

async function handleLogin() {
  if (!validateAll()) return

  try {
    const res = await axios.post('/api/token/', {
      email: form.value.email,
      password: form.value.password,
    })

    localStorage.setItem('access', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)

    success.value = true
    setTimeout(() => {
      router.push('/')
    }, 1500)
  } catch (err) {
    console.error(err)
    errors.value.email = 'Invalid email or password'
    errors.value.password = ' '
  }
}
</script>
