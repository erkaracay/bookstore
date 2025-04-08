<template>
  <div class="pt-16 pb-10 bg-neutral min-h-screen px-4">
    <div class="max-w-md mx-auto bg-white p-6 rounded shadow">
      <h2 class="text-2xl font-bold text-primary mb-6 text-center">Login</h2>

      <form @submit.prevent="handleLogin" class="space-y-6 relative">
        <div
          v-if="formError"
          class="bg-red-100 border border-red-300 text-red-700 px-4 py-2 rounded text-sm flex items-center justify-between">
          <span>{{ formError }}</span>
          <button @click="formError = ''" class="text-red-500 hover:underline text-xs">Dismiss</button>
        </div>

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

        <div class="flex items-center gap-2 pl-1 text-sm mt-2">
          <input
            type="checkbox"
            id="remember"
            v-model="rememberMe"
            class="accent-primary shrink-0 w-4 h-4 mt-0.5"
          />
          <label for="remember" class="text-gray-600 cursor-pointer select-none">Remember Me</label>
        </div>

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
import { useAuthStore } from '@/store/auth'
import FormField from '@/components/form/FormField.vue'

const auth = useAuthStore()
const router = useRouter()
const focused = ref('')
const success = ref(false)
const rememberMe = ref(true)
const formError = ref('')

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
  formError.value = ''
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

    const storage = rememberMe.value ? localStorage : sessionStorage
    storage.setItem('access', res.data.access)
    storage.setItem('refresh', res.data.refresh)

    auth.setTokens(res.data)
    await auth.fetchUser()

    formError.value = ''
    success.value = true
    setTimeout(() => router.push('/'), 1500)

  } catch (err) {
    console.error(err)
    formError.value = 'Invalid email or password. Please try again.'
  }
}
</script>

