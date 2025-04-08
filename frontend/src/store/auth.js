import { defineStore } from 'pinia'
import axios from '@/utils/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    access: localStorage.getItem('access') || sessionStorage.getItem('access'),
    refresh: localStorage.getItem('refresh') || sessionStorage.getItem('refresh'),
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.access && !!state.user,
  },

  actions: {
    setTokens({ access, refresh }) {
      this.access = access
      this.refresh = refresh
      localStorage.setItem('access', access)
      localStorage.setItem('refresh', refresh)
    },

    async fetchUser() {
      try {
        const res = await axios.get('/users/me/')
        this.user = res.data
      } catch (err) {
        console.error('Failed to fetch user:', err)
        this.logout()
      }
    },

    logout() {
      this.access = null
      this.refresh = null
      this.user = null
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    },
  },
})
