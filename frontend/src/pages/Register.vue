<template>
  <div class="pt-16 pb-10 bg-neutral min-h-screen px-4">
    <div class="max-w-md mx-auto bg-white p-6 rounded shadow">
      <h2 class="text-2xl font-bold text-primary mb-4 text-center">Register</h2>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div class="grid grid-cols-2 gap-2">
          <input v-model="first_name" placeholder="First Name" required class="input" />
          <input v-model="last_name" placeholder="Last Name" required class="input" />
        </div>

        <input v-model="email" type="email" placeholder="Email" required class="input" />
        <input v-model="password" type="password" placeholder="Password" required class="input" />

        <!-- User Type -->
        <BaseSelect
          v-model="user_type"
          label="User Type"
          :options="userTypes"
        />

        <!-- Seller extras -->
        <div v-if="user_type === 'Seller'">
          <!-- Are you a company checkbox -->
          <div class="flex items-center space-x-2 mt-2">
            <input
              type="checkbox"
              id="isCompany"
              v-model="isCompany"
              class="rounded border-gray-300 focus:ring-primary text-primary"
            />
            <label for="isCompany" class="text-sm text-gray-700">Registering as a company?</label>
          </div>

          <div v-if="isCompany">
            <input
              v-model="company_name"
              placeholder="Company Name"
              class="input mt-2"
            />
          </div>
        </div>

        <button type="submit" class="w-full bg-primary text-white py-2 rounded hover:bg-opacity-90">
          Register
        </button>
      </form>

      <p class="mt-4 text-sm text-center text-gray-600">
        Already have an account?
        <router-link to="/login" class="text-primary font-medium">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'
import BaseSelect from '@/components/BaseSelect.vue'

const first_name = ref('')
const last_name = ref('')
const email = ref('')
const password = ref('')
const user_type = ref('Buyer')
const isCompany = ref(false)
const company_name = ref('')
const router = useRouter()

const userTypes = ['Buyer', 'Seller']

async function handleRegister() {
  try {
    const payload = {
      first_name: first_name.value,
      last_name: last_name.value,
      email: email.value,
      password: password.value,
      user_type: user_type.value.toLowerCase(), // send as expected by API
    }

    if (user_type.value === 'Seller' && isCompany.value) {
      payload.company_name = company_name.value
    }

    await axios.post('/users/register/', payload)
    alert('Registration successful! You can now log in.')
    router.push('/login')
  } catch (err) {
    console.error(err)
    alert('Registration failed. Please check your info.')
  }
}
</script>

<script>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
export default {
  layout: DefaultLayout,
}
</script>

<style scoped>
.input {
  @apply w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary;
}
</style>
