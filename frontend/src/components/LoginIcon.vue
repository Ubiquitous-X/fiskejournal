<template>
  <div>
    <div v-if="isLoggedIn" class="relative dropdown dropdown-bottom dropdown-end">
      <div tabindex="0" role="button" class="cursor-pointer" @click="toggleDropdown">
        <i :class="iconClass" class="text-base sm:text-xl mr-1"></i>
      </div>
      <ul v-show="isDropdownOpen" tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[1] w-52 p-2 shadow">
        <li>
          <a @click="goToAdmin" class="flex items-center">
            <i class="fas fa-cog mr-2"></i> Adminpanel
          </a>
        </li>
        <li>
          <a @click="handleLogout" class="flex items-center">
            <i class="fas fa-sign-out-alt mr-2"></i> Logga ut
          </a>
        </li>
      </ul>
    </div>
    <div v-else @click="openModal" class="cursor-pointer">
      <i :class="iconClass" class="text-base sm:text-xl mr-1"></i>
    </div>

    <!-- DaisyUI Modal -->
    <div :class="{'modal modal-open': isModalOpen, 'modal': !isModalOpen}">
      <div class="modal-box relative w-full max-w-xs sm:max-w-lg sm:w-96">
        <button class="btn btn-sm btn-circle absolute right-2 top-2" @click="closeModal">✕</button>
        
        <div v-if="isLoggedIn">
          <h3 class="text-lg font-bold text-left">Logga ut?</h3>
          <div class="divider"></div>
          <blockquote class="text-base">
            <p>Är du säker på att du vill logga ut?</p>
          </blockquote>
          <div class="flex justify-center">
            <img :src="loginImage" alt="Loginbild" class="mt-4 mb-4 max-w-[150px] hidden sm:block">
          </div>
          <div class="modal-action flex flex-col sm:flex-row mt-2">
            <button class="btn btn-primary mb-2 sm:mb-0" @click="handleLogout">Logga ut</button>
            <button class="btn" @click="closeModal">Avbryt</button>
          </div>
        </div>
        
        <div v-else>
          <h3 class="text-lg font-bold text-left">Logga in</h3>
          <div class="divider"></div>
          <div class="flex justify-center">
            <img :src="loginImage" alt="Loginbild" class="mb-8 max-w-[150px] hidden sm:block">
          </div>
          <form @submit.prevent="handleLogin">
            <div class="form-control">
              <label class="input input-bordered flex items-center gap-2">
                <i class="fas fa-user h-4 w-4 opacity-70"></i>
                <input type="text" v-model="username" class="grow" placeholder="Användarnamn" required />
              </label>
            </div>
            <div class="form-control mt-4">
              <label class="input input-bordered flex items-center gap-2">
                <i class="fas fa-lock h-4 w-4 opacity-70"></i>
                <input type="password" v-model="password" class="grow" placeholder="Lösenord" required />
              </label>
            </div>
            <div class="modal-action flex flex-col sm:flex-row mt-4">
              <button type="submit" class="btn btn-primary mb-2 sm:mb-0">Logga in</button>
              <button type="button" class="btn" @click="closeModal">Avbryt</button>
            </div>
          </form>
        </div>
      </div>
      <div class="modal-backdrop" @click="closeModal"></div>
    </div>
    
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import apiClient from '../api';
import loginImage from '@/assets/logo.png';

export default {
  name: 'LoginIcon',
  setup() {
    const store = useStore();
    const router = useRouter();
    const toast = useToast();

    const isModalOpen = ref(false);
    const isDropdownOpen = ref(false);
    const username = ref('');
    const password = ref('');
    const isLoggedIn = computed(() => store.getters.isLoggedIn);
    const iconClass = computed(() => (isLoggedIn.value ? 'fas fa-user-check' : 'fas fa-user'));

    const openModal = () => {
      isModalOpen.value = true;
    };

    const closeModal = () => {
      isModalOpen.value = false;
    };

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value;
    };

    const closeDropdown = () => {
      isDropdownOpen.value = false;
    };

    const handleClickOutside = (event) => {
      if (!event.target.closest('.dropdown')) {
        closeDropdown();
      }
    };

    const handleLogin = async () => {
      try {
        const response = await apiClient.post('/auth/login', {
          username: username.value,
          password: password.value,
        }, {
          skipInterceptor: true  // Använder flaggan i interceptorn
        });

        if (response.status === 200) {
          store.commit('setLoggedIn', true);

          // Hämta CSRF-token efter lyckad inloggning
          const csrfResponse = await apiClient.get('/auth/csrf-token');
          const csrfToken = csrfResponse.data.csrfToken;
          localStorage.setItem('csrfToken', csrfToken);
          apiClient.defaults.headers['X-CSRFToken'] = csrfToken;

          toast.success(response.data.message || 'Inloggning lyckades!');
          closeModal();
        } else {
          toast.error(response.data.message || 'Inloggning misslyckades');
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          toast.error('Fel användarnamn eller lösenord');
        } else {
          const message = error.response?.data?.message || 'Ett fel uppstod under inloggningen.';
          toast.error(message);
        }
      }
    };


    const handleLogout = async () => {
      try {
        const response = await apiClient.post('/auth/logout');

        if (response.status === 200) {
          store.commit('setLoggedIn', false);
          toast.success(response.data.message || 'Utloggning lyckades!');
          closeModal();
          if (router.currentRoute.value.name === 'Admin') {
            router.replace('/');
          }
        } else {
          toast.error(response.data.message || 'Utloggning misslyckades');
        }
      } catch (error) {
        toast.error('Ett fel uppstod under utloggningen.');
      }
    };

    const goToAdmin = () => {
      router.push('/admin');
      closeDropdown();
    };

    onMounted(() => {
      document.addEventListener('click', handleClickOutside);
    });

    onBeforeUnmount(() => {
      document.removeEventListener('click', handleClickOutside);
    });

    return {
      isModalOpen,
      isDropdownOpen,
      username,
      password,
      loginImage,
      isLoggedIn,
      iconClass,
      openModal,
      closeModal,
      toggleDropdown,
      handleLogin,
      handleLogout,
      goToAdmin,
    };
  },
};
</script>
