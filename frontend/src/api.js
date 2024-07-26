import axios from 'axios';
import { useToast } from 'vue-toastification';

const toast = useToast();

// Skapa en instans av axios med bas-URL
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true, // Viktigt för att skicka kakor
});

// Funktion för att hämta CSRF-token
async function fetchCSRFToken() {
  try {
    const response = await apiClient.get('/auth/csrf-token');
    const csrfToken = response.data.csrfToken;
    localStorage.setItem('csrfToken', csrfToken);
    apiClient.defaults.headers['X-CSRFToken'] = csrfToken;
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
  }
}

// Hämta CSRF-token när appen laddas
fetchCSRFToken();

// Uppdatera headers med CSRF-token vid varje förfrågan
apiClient.interceptors.request.use(config => {
  const csrfToken = localStorage.getItem('csrfToken');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// Hantera fel med en interceptor
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.config && error.config.skipInterceptor) {
      // Skippa interceptorn för specifik begäran
      return Promise.reject(error);
    }

    if (error.response) {
      const status = error.response.status;
      if (status === 401) {
        toast.error('Du är inte inloggad');
      } else if (status === 403) {
        toast.error('Du har inte behörighet');
      } else if (status === 404) {
        toast.error('Kunde ej hittas (404)');
      } else {
        toast.error(`Misslyckades - statuskod: ${status}`);
      }
    } else {
      toast.error('Ett okänt fel inträffade');
    }
    return Promise.reject(error);
  }
);

export default apiClient;
