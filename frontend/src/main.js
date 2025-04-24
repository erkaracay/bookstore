import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createPinia } from 'pinia'
import router from './router'
import { useAuthStore } from '@/store/auth'
import '@vuepic/vue-datepicker/dist/main.css'
import Toast, { useToast } from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast)
app.mount('#app')

const auth = useAuthStore()

if (auth.access) {
  auth.fetchUser()
}
