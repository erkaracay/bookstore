<template>
  <div class="relative">
    <!-- 👁️ Icon wrapper + Input -->
    <div class="relative h-[44px]">
      <input
        :id="field"
        :type="computedType"
        v-model="model"
        @input="$emit('validate', field)"
        @focus="$emit('focus')"
        @blur="$emit('blur')"
        class="peer input pt-5 pb-2 pr-10"
        :placeholder="' '"
        :class="{ 'border-red-500': error }"
      />

      <!-- 👁️ Password toggle -->
      <button
        v-if="type === 'password'"
        type="button"
        @click="togglePassword"
        class="absolute top-1/2 right-3 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
      >
        <svg v-if="show" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24"
             stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24"
             stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.269-2.943-9.542-7a9.956 9.956 0 012.397-4.398M6.537 6.537A9.953 9.953 0 0112 5c4.478 0 8.269 2.943 9.542 7a9.958 9.958 0 01-4.293 5.166M15 12a3 3 0 00-3-3m0 0a3 3 0 00-3 3m6 0a3 3 0 01-3 3m0 0a3 3 0 01-3-3m0 0L3 3m18 18l-3-3"/>
        </svg>
      </button>

      <!-- Floating Label -->
      <label
        :for="field"
        class="absolute left-3 top-1 text-xs text-gray-500 transition-all duration-200 ease-in-out origin-[0]
          peer-placeholder-shown:top-3 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400
          peer-placeholder-shown:scale-100
          peer-focus:top-1 peer-focus:scale-90 peer-focus:text-primary"
      >
        {{ name }}
      </label>
    </div>

    <!-- Error Message (outside, no impact on layout) -->
    <p v-if="error" class="text-sm text-red-600 mt-1">{{ error }}</p>
  </div>
</template>


<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: String,
  name: String,
  field: String,
  type: { type: String, default: 'text' },
  error: String,
  hint: String,
  focused: Boolean,
})

const emit = defineEmits(['update:modelValue', 'validate', 'focus', 'blur'])

const model = defineModel()

const show = ref(false)

const computedType = computed(() => {
  if (props.type === 'password') return show.value ? 'text' : 'password'
  return props.type
})

function togglePassword() {
  show.value = !show.value
}
</script>

<style scoped>
.input {
  @apply w-full px-3 border rounded focus:outline-none focus:ring-2 focus:ring-primary;
  @apply h-[44px];
}
</style>
