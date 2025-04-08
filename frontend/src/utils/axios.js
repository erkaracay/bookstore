import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000/',
  withCredentials: false,
})

const publicEndpoints = [
  '/api/token/',
  '/users/register/',
  '/books/',
]

instance.interceptors.request.use(config => {
  const token = localStorage.getItem('access')
  const urlPath = new URL(config.url, config.baseURL).pathname
  const isPublic = publicEndpoints.some(endpoint => urlPath.startsWith(endpoint))

  if (token && !isPublic) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

export default instance
