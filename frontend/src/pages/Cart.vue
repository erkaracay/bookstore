<template>
  <div class="max-w-4xl mx-auto pt-10 pb-16">
    <h1 class="text-2xl font-bold mb-6 text-center">🛒 Your Cart</h1>

    <div v-if="loading" class="text-center text-gray-500">Loading cart...</div>

    <div v-else>
      <!-- ✅ Success message -->
      <div v-if="checkoutSuccess" class="text-center py-20 space-y-4">
        <div class="flex justify-center">
          <div class="bg-green-100 text-green-600 rounded-full p-4 inline-flex">
            <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>

        <h2 class="text-xl font-bold text-green-700">Your order was placed successfully!</h2>

        <router-link
          to="/dashboard"
          class="inline-block mt-4 bg-primary text-white px-5 py-2 rounded hover:bg-opacity-90 hover:text-gray-100 transition"
        >
          View My Orders
        </router-link>
      </div>

      <!-- ❌ Cart is empty and not a success case -->
      <div v-else-if="cart.items.length === 0" class="text-center text-gray-500">
        Your cart is empty.
      </div>

      <!-- 🛒 Cart items and checkout button -->
      <div v-else>
        <ul class="space-y-4 mb-6">
          <li
            v-for="item in cart.items"
            :key="item.id"
            class="flex items-center justify-between bg-white rounded border p-4"
          >
            <div class="flex-1">
              <h2 class="font-semibold text-gray-800">{{ item.book.title }}</h2>
              <p class="text-sm text-gray-500">${{ Number(item.book.price).toFixed(2) }} each</p>
            </div>

            <div class="flex items-center gap-3">
              <!-- Quantity Control -->
              <div class="flex items-center border rounded px-2 py-1">
                <button
                  type="button"
                  @click="changeQuantity(item, -1)"
                  class="text-lg px-2 text-gray-500 hover:text-primary"
                >
                  −
                </button>

                <input
                  type="number"
                  v-model.number="item.quantity"
                  @input="handleQuantityInput(item)"
                  class="w-12 text-center outline-none no-spin"
                />

                <button
                  type="button"
                  @click="changeQuantity(item, 1)"
                  class="text-lg px-2 text-gray-500 hover:text-primary"
                >
                  +
                </button>
              </div>

              <!-- Item Total -->
              <p class="text-sm text-gray-500 font-medium w-20 text-right">
                ${{ (item.book.price * item.quantity).toFixed(2) }}
              </p>

              <!-- Remove -->
              <button
                @click="removeItem(item.id)"
                class="text-red-600 text-sm hover:underline"
              >
                Remove
              </button>
            </div>
          </li>

        </ul>

        <!-- Total + Checkout -->
        <div class="flex items-center justify-between border-t pt-4">
          <p class="text-lg font-semibold text-gray-800">Total: ${{ cart.total.toFixed(2) }}</p>
          <button
            @click="checkout"
            class="bg-primary text-white px-6 py-2 rounded hover:bg-opacity-90"
          >
            Checkout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/axios'

const cart = ref({ items: [], total: 0 })
const loading = ref(true)
const checkoutSuccess = ref(false)

onMounted(fetchCart)

async function fetchCart() {
  try {
    const res = await axios.get('/cart/')
    cart.value = res.data
  } catch (err) {
    console.error('Failed to load cart:', err)
  } finally {
    loading.value = false
  }
}

function changeQuantity(item, delta) {
  const max = item.book?.stock ?? Infinity
  let newQty = item.quantity + delta

  if (newQty > max) newQty = max
  if (newQty < 1) newQty = 1

  item.quantity = newQty
  updateItem(item)
}

function handleQuantityInput(item) {
  const max = item.book?.stock ?? Infinity

  if (item.quantity > max) {
    item.quantity = max
  } else if (item.quantity < 1) {
    item.quantity = 1
  }

  updateItem(item)
}

async function updateItem(item) {
  try {
    await axios.patch(`/cart/items/${item.id}/`, {
      quantity: item.quantity,
    })
    fetchCart()
  } catch (err) {
    console.error('Update failed:', err)
  }
}

async function removeItem(id) {
  try {
    await axios.delete(`/cart/items/${id}/`)
    fetchCart()
  } catch (err) {
    console.error('Remove failed:', err)
  }
}

async function checkout() {
  try {
    await axios.post('/cart/checkout/')
    checkoutSuccess.value = true
    fetchCart()
  } catch (err) {
    console.error('Checkout failed:', err)
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

button {
  @apply text-sm font-medium;
}
input[type="number"] {
  @apply text-sm;
}

input[type='number']::-webkit-outer-spin-button,
input[type='number']::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type='number'] {
  -moz-appearance: textfield; /* Firefox */
}
</style>
