import { onMounted, onBeforeUnmount } from 'vue'

export function useClickOutside(targetRef, callback) {
  function handleClick(e) {
    if (targetRef.value && !targetRef.value.contains(e.target)) {
      callback()
    }
  }

  onMounted(() => document.addEventListener('click', handleClick))
  onBeforeUnmount(() => document.removeEventListener('click', handleClick))
}
