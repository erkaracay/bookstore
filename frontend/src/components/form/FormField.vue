<template>
  <div class="relative">
    <input
      :id="field"
      :type="type"
      v-model="model"
      @input="$emit('validate', field)"
      @focus="$emit('focus')"
      @blur="$emit('blur')"
      class="peer input pt-5 pb-2"
      :placeholder="' '"
      :class="{ 'border-red-500': error }"
    />

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


    <!-- Hint Tooltip -->
    <div
      v-if="focused && hint"
      class="absolute z-10 left-0 top-full mt-1 w-max max-w-xs bg-gray-100 text-xs text-gray-600 px-3 py-1 rounded shadow border border-gray-300"
    >
      {{ hint }}
    </div>

    <!-- Error -->
    <p v-if="error" class="text-sm text-red-600 mt-1">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  modelValue: String,
  name: String,
  field: String,
  type: {
    type: String,
    default: 'text',
  },
  error: String,
  hint: String,
  focused: Boolean,
})

defineEmits(['update:modelValue', 'validate', 'focus', 'blur'])

const model = defineModel()
</script>

<style scoped>
.input {
  @apply w-full px-3 py-3 border rounded focus:outline-none focus:ring-2 focus:ring-primary;
}
</style>
