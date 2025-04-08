<template>
  <form @submit.prevent="handleRegister" class="space-y-6 relative">
    <!-- First + Last Name -->
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

    <!-- Email -->
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

    <!-- Password -->
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

    <!-- Submit -->
    <button
      type="submit"
      class="w-full bg-primary text-white py-2 rounded hover:bg-opacity-90"
    >
      Register as Buyer
    </button>

    <!-- Success Message -->
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

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
})

const errors = ref({})

// zod schema
const schema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
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

async function handleRegister() {
  if (!validateAll()) return

  try {
    await axios.post('/users/register/', {
      ...form.value,
      user_type: 'buyer',
    })

    success.value = true
    setTimeout(() => router.push('/login'), 2000)
  } catch (err) {
    console.error(err)
    alert('Something went wrong!')
  }
}
</script>
