<template>
  <div v-if="!loading" class="flex flex-col h-screen overflow-hidden">
    <Navbar class="flex-none" />
    <div :class="{'flex-1 relative overflow-hidden': isMapView, 'flex-1 overflow-auto': !isMapView}">
      <router-view></router-view>
    </div>
  </div>
  <div v-else class="flex items-center justify-center h-screen">
    <Spinner />
  </div>
</template>

<script>
import { ref, onMounted, computed, onBeforeMount } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
import Spinner from '@/components/Spinner.vue';

export default {
  name: 'App',
  components: {
    Navbar,
    Spinner
  },
  setup() {
    const loading = ref(true);
    const route = useRoute();

    const isMapView = computed(() => route.name === 'MapView');

    onBeforeMount(() => {
      loading.value = true;
    });

    onMounted(() => {
      // Simulera väntetid för att säkerställa att allt är färdigladdat
      setTimeout(() => {
        loading.value = false;
      }, 700); 
    });

    return {
      loading,
      isMapView
    };
  }
};
</script>

<style scoped>
.active {
  font-weight: bold;
}
</style>

