<template>
  <div>
    <Listbox :modelValue="modelValue" @update:modelValue="emit('update:modelValue', $event)">
      <ListboxLabel v-if="label" class="block text-sm font-medium mb-1">{{ label }}</ListboxLabel>
      <div class="relative">
        <ListboxButton
          class="relative w-full border border-gray-300 rounded bg-white py-2 pl-4 pr-10 text-left cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary"
        >
          {{ modelValue }}
          <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M19 9l-7 7-7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </span>
        </ListboxButton>

        <ListboxOptions
          class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded border border-gray-200 bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
        >
          <ListboxOption
            v-for="option in options"
            :key="option"
            :value="option"
            v-slot="{ active, selected }"
          >
            <li
              :class="[
                'cursor-pointer select-none relative py-2 pl-10 pr-4',
                active ? 'bg-accent text-white' : 'text-gray-900'
              ]"
            >
              {{ option }}
              <span
                v-if="selected"
                class="absolute inset-y-0 left-0 flex items-center pl-3 text-primary"
              >
                ✔
              </span>
            </li>
          </ListboxOption>
        </ListboxOptions>
      </div>
    </Listbox>
  </div>
</template>

<script setup>
import {
  Listbox,
  ListboxButton,
  ListboxLabel,
  ListboxOption,
  ListboxOptions
} from '@headlessui/vue'

const props = defineProps({
  modelValue: String,
  options: Array,
  label: String
})

const emit = defineEmits(['update:modelValue'])
</script>
