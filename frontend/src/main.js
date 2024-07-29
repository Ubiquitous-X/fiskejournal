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

router.beforeEach((to, from, next) => {
  // Ta bort noindex meta-tagg om den finns
  const noindexMetaTag = document.querySelector('meta[name="robots"]');
  if (noindexMetaTag) {
    noindexMetaTag.remove();
  }

  // Uppdatera titel
  if (to.meta.title) {
    document.title = to.meta.title;
  }

  // Uppdatera meta beskrivning
  if (to.meta.description) {
    const descriptionMetaTag = document.querySelector('meta[name="description"]');
    if (descriptionMetaTag) {
      descriptionMetaTag.setAttribute('content', to.meta.description);
    } else {
      const newMetaTag = document.createElement('meta');
      newMetaTag.name = 'description';
      newMetaTag.content = to.meta.description;
      document.getElementsByTagName('head')[0].appendChild(newMetaTag);
    }
  }

  next();
});

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
