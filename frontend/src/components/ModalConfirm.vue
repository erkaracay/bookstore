<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40"
  >
    <div class="bg-white rounded-lg shadow-lg w-full max-w-sm p-6 space-y-4">
      <h2 class="text-lg font-semibold text-gray-800">{{ title }}</h2>
      <p class="text-sm text-gray-600">{{ message }}</p>

      <div class="flex justify-end gap-3 mt-4">
        <button
          class="px-4 py-2 text-sm rounded border hover:bg-gray-100"
          @click="$emit('cancel')"
        >
          Cancel
        </button>
        <button
          class="px-4 py-2 text-sm rounded bg-red-600 text-white hover:bg-red-700"
          @click="$emit('confirm')"
        >
          {{ confirmText || 'Delete' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: Boolean,
  title: String,
  message: String,
  confirmText: String
})
defineEmits(['cancel', 'confirm'])
</script>
