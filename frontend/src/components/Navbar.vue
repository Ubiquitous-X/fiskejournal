<template>
  <div>
    <div class="navbar bg-base-100 relative shadow-lg z-50 min-h-12 sm:min-h-16 py-0">
      <div class="navbar-start">
        <div class="relative dropdown dropdown-bottom">
          <div tabindex="0" role="button" class="btn btn-ghost lg:hidden px-2" @click="toggleDropdown">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
            </svg>
          </div>
          <ul v-show="dropdownOpen" tabindex="0" class="dropdown-content menu bg-base-100 rounded-box w-52 p-2 shadow z-[1]">
            <li>
              <router-link to="/" exact-active-class="active" @click="closeDropdown">
                <i class="fas fa-home mr-2"></i>Hem
              </router-link>
            </li>
            <li>
              <router-link to="/fiskar" exact-active-class="active" @click="closeDropdown">
                <i class="fas fa-fish mr-2"></i>Fiskar
              </router-link>
            </li>
            <li>
              <router-link to="/karta" exact-active-class="active" @click="closeDropdown">
                <i class="fas fa-map mr-2"></i>Karta
              </router-link>
            </li>
            <li>
              <router-link to="/galleri" exact-active-class="active" @click="closeDropdown">
                <i class="fas fa-camera mr-2"></i>Galleri
              </router-link>
            </li>
            <li>
              <router-link to="/om" exact-active-class="active" @click="closeDropdown">
                <i class="fas fa-info-circle mr-2"></i>Om sidan
              </router-link>
            </li>
            <li>
              <a href="https://github.com/Ubiquitous-X/fiskejournal" target="_blank">
                <i class="fab fa-github text-base xs:text-xl mr-2"></i>
                Github
              </a>
            </li>
          </ul>
        </div>
        <router-link to="/" class="btn btn-ghost normal-case text-base sm:text-lg flex items-center px-2 sm:px-4">
          <span class="hidden md:inline">
            <i class="fas fa-fish-fins text-current h-6 ml-2 sm:ml-0"></i>
          </span>
          Ölunds Fiske
        </router-link>
      </div>
      <div class="navbar-center hidden lg:flex">
        <ul class="menu menu-horizontal px-1 space-x-4">
          <li :class="{'border-l border-base-content': $route.path !== '/', 'first:border-0': true}">
            <router-link to="/" exact-active-class="active">
              <i class="fas fa-home mr-1"></i>Hem
            </router-link>
          </li>
          <li :class="{'border-l border-base-content': $route.path !== '/fiskar'}">
            <router-link to="/fiskar" exact-active-class="active">
              <i class="fas fa-fish mr-1"></i>Fiskar
            </router-link>
          </li>
          <li :class="{'border-l border-base-content': $route.path !== '/karta'}">
            <router-link to="/karta" exact-active-class="active">
              <i class="fas fa-map mr-1"></i>Karta
            </router-link>
          </li>
          <li :class="{'border-l border-base-content': $route.path !== '/galleri'}">
            <router-link to="/galleri" exact-active-class="active">
              <i class="fas fa-camera mr-1"></i>Galleri
            </router-link>
          </li>
          <li :class="{'border-l border-base-content': $route.path !== '/om'}">
            <router-link to="/om" exact-active-class="active">
              <i class="fas fa-info-circle mr-1"></i>Om sidan
            </router-link>
          </li>
        </ul>
      </div>
      <div class="navbar-end flex items-center space-x-2 sm:space-x-4 container mx-auto">
        <div class="flex items-center">
          <ThemeSwitcher />
        </div>
        <div class="items-center hidden lg:flex">
          <a href="https://github.com/Ubiquitous-X/fiskejournal" target="_blank">
            <i class="fab fa-github text-base sm:text-xl mr-1"></i>
          </a>
        </div>
        <LoginIcon />
        <FileUpload v-if="isLoggedIn" />
      </div>
    </div>
    <div v-if="shouldShowStats">
      <div v-if="showStats" class="stats-widget bg-base-100 text-base-content rounded-lg transition-height duration-300 hidden md:block">
        <component :is="infoPanelComponent" />
        <div class="flex justify-center mt-2">
          <button @click="toggleStats" class="btn btn-circle btn-sm">
            <i class="fas fa-chevron-up"></i>
          </button>
        </div>
      </div>
      <div v-else class="flex justify-center mt-2">
        <button @click="toggleStats" class="btn btn-circle btn-sm">
          <i class="fas fa-chevron-down"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, defineAsyncComponent } from 'vue';
import ThemeSwitcher from './ThemeSwitcher.vue';
import LoginIcon from './LoginIcon.vue';
import FileUpload from './FileUpload.vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';

export default {
  components: {
    ThemeSwitcher,
    LoginIcon,
    FileUpload
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const dropdownOpen = ref(false);
    const showStats = ref(true);

    const isLoggedIn = computed(() => store.getters.isLoggedIn);
    const shouldShowStats = computed(() => {
      const routesToShowStats = ['/', '/fiskar'];
      return routesToShowStats.includes(route.path);
    });

    const infoPanelComponent = ref(null);

    const toggleDropdown = (event) => {
      event.preventDefault();
      dropdownOpen.value = !dropdownOpen.value;
    };

    const closeDropdown = (event) => {
      dropdownOpen.value = false;
    };

    const toggleStats = () => {
      showStats.value = !showStats.value;
      localStorage.setItem('showStats', showStats.value);
    };

    const loadStatsState = () => {
      const savedState = localStorage.getItem('showStats');
      if (savedState !== null) {
        showStats.value = savedState === 'true';
      }
    };

    onMounted(() => {
      loadStatsState();
      // Kontrollera skärmstorlek och dynamiskt importera InfoPanel
      if (window.matchMedia('(min-width: 768px)').matches) {
        infoPanelComponent.value = defineAsyncComponent(() =>
          import('./InfoPanel.vue')
        );
      }
    });

    return {
      dropdownOpen,
      showStats,
      isLoggedIn,
      shouldShowStats,
      toggleDropdown,
      closeDropdown,
      toggleStats,
      infoPanelComponent,
    };
  },
};
</script>

<style scoped>
.active {
  font-weight: bold;
}
</style>
