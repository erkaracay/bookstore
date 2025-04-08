<template>
  <form @submit.prevent="handleRegister" class="space-y-6 relative">
    <div
      v-if="formError"
      class="bg-red-100 border border-red-300 text-red-700 px-4 py-2 rounded text-sm flex items-center justify-between"
    >
      <span>{{ formError }}</span>
      <button @click="formError = ''" class="text-red-500 hover:underline text-xs">Dismiss</button>
    </div>

    <div class="grid grid-cols-2 gap-2">
      <FormField
        v-model="form.first_name"
        name="First Name"
        field="first_name"
        type="text"
        :error="errors.first_name"
        hint="Required"
        @validate="validateField"
        @focus="focused = 'first_name'"
        @blur="focused = ''"
        :focused="focused === 'first_name'"
      />
      <FormField
        v-model="form.last_name"
        name="Last Name"
        field="last_name"
        type="text"
        :error="errors.last_name"
        hint="Required"
        @validate="validateField"
        @focus="focused = 'last_name'"
        @blur="focused = ''"
        :focused="focused === 'last_name'"
      />
    </div>

    <FormField
      v-model="form.email"
      name="Email"
      field="email"
      type="email"
      :error="errors.email"
      hint="Must be a valid email address"
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
      hint="Min 6 characters required"
      @validate="validateField"
      @focus="focused = 'password'"
      @blur="focused = ''"
      :focused="focused === 'password'"
    />

    <button type="submit" class="w-full bg-primary text-white py-2 rounded hover:bg-opacity-90">
      Register as Seller (Individual)
    </button>

    <div v-if="success" class="mt-4 text-sm text-green-600 bg-green-50 p-3 rounded border border-green-300">
      🎉 Registration successful! Redirecting to login...
    </div>
  </form>
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
const errors = ref({})
const formError = ref('')

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
})

const schema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
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

async function handleRegister() {
  if (!validateAll()) return

  try {
    await axios.post('/users/register/', {
      ...form.value,
      user_type: 'seller',
      company_name: 'Individual',
    })

    success.value = true
    setTimeout(() => router.push('/login'), 2000)
  } catch (err) {
    console.error('Registration error:', err)

    const response = err.response
    if (!response) {
      formError.value = 'Network error. Please check your connection.'
      return
    }

    if (response.status === 400) {
      // DRF returns field errors in 400
      const data = response.data

      if (data.email?.[0]?.includes('already exists')) {
        formError.value = 'An account with this email already exists.'
      } else if (data.password?.[0]) {
        formError.value = `Password: ${data.password[0]}`
      } else {
        // fallback for other field validation
        formError.value = 'Please correct the highlighted fields.'
      }
    } else if (response.status >= 500) {
      formError.value = 'Server error. Please try again later.'
    } else {
      formError.value = 'Registration failed. Please check your information.'
    }
  }

}
</script>
