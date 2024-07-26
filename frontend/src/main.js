import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import '@fortawesome/fontawesome-free/css/all.css';

if (import.meta.env.VITE_ENV === 'production') {
  import('../dist/style.css');
} else {
  import('./tailwind.css');
}

const app = createApp(App);
app.use(router);
app.use(store);
app.use(Toast, {
  timeout: 3000,
  newestOnTop: false,
  pauseOnFocusLoss: false,
  pauseOnHover: false,
  hideProgressBar: true,
  closeButton: false,
  bodyClassName: 'font-sans font-bold'
});
app.mount('#app');

// Kontrollera inloggningsstatus vid appens laddning
store.dispatch('checkLoginStatus');
