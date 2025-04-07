<template>
  <div class="min-h-screen flex flex-col bg-neutral text-gray-900">
    <!-- Header -->
    <header class="bg-white shadow border-b border-gray-200">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <router-link to="/" class="text-2xl font-extrabold text-primary">
          📚 Bookstore
        </router-link>

        <nav class="space-x-4 text-sm sm:text-base">
          <router-link to="/" class="text-gray-700 hover:text-primary transition">Home</router-link>
          <router-link to="/login" class="text-gray-700 hover:text-primary transition">Login</router-link>
          <router-link to="/register" class="text-gray-700 hover:text-primary transition">Register</router-link>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow container mx-auto px-4 py-10">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t text-center text-sm text-gray-500 py-4">
      © {{ new Date().getFullYear() }} Bookstore Inc.
    </footer>
  </div>
</template>

<script setup>
</script>
