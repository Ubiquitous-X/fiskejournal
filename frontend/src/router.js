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
    meta: {
      title: 'Ölunds Fiske - Start',
      description: 'Ölunds Fiske är en webbapp jag skapat som automatiskt loggar mina fångster i realtid med diverse information och placerar ut dem på kartan. Jag fiskar främst gädda, gös och abborre i och runt Mälaren.Välkommen till Ölunds Fiske, logga dina fångster här!'
    }
  },
  {
    path: '/karta',
    name: 'Karta',
    component: MapView,
    meta: {
      title: 'Ölunds Fiske - Karta',
      description: 'Här visas alla fångster på kartan med information om fiskarna'
    }
  },
  {
    path: '/fiskar',
    name: 'Fiskar',
    component: FishTableView,
    meta: {
      title: 'Ölunds Fiske - Alla fångster',
      description: 'Här är listan på alla fångade fiskar och information om dessa'
    }
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
    meta: {
      title: 'Ölunds Fiske - Om sidan',
      description: 'Här ser du information om tekniken bakom webbappen, hur den är skapad och fungerar'
    }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView,
    meta: { 
      requiresAuth: true,
      title: "Ölunds Fiske - Administrationspanel",
      description: 'Administrationspanelen för databasen' 
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFoundView',
    component: NotFoundView,
    meta: {
      title: "Ölunds Fiske - 404 Bottennapp",
      description: 'Har du nått den här sidan så har draget landat i vassen'
    }
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
