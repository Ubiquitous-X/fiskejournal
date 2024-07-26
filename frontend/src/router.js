import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import MapView from '@/views/MapView.vue';
import FishTableView from '@/views/FishTableView.vue';
import AboutView from '@/views/AboutView.vue';
import SingleFishView from '@/views/SingleFishView.vue';
import AdminView from '@/views/AdminView.vue';
import NotFoundView from '@/views/NotFoundView.vue'
import store from '@/store';

const routes = [
  {
    path: '/',
    name: 'Hem',
    component: HomeView,
  },
  {
    path: '/karta',
    name: 'Karta',
    component: MapView,
  },
  {
    path: '/fiskar',
    name: 'Fiskar',
    component: FishTableView,
  },
  {
    path: '/fisk/:slug',
    name: 'SingleFishView',
    component: SingleFishView,
    props: true
  },
  {
    path: '/om',
    name: 'Om',
    component: AboutView,
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFoundView',
    component: NotFoundView,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Global navigationsvakt
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Kontrollera om användaren är inloggad
    if (!store.getters.isLoggedIn) {
      // Om inte, omdirigera till startsidan
      next({ path: '/' });
    } else {
      // Annars fortsätt till den begärda sidan
      next();
    }
  } else {
    next(); // Fortsätt om ingen autentisering krävs
  }
});

export default router;
