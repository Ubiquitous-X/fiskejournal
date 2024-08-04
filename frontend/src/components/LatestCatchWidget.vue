<template>
  <div class="flex-grow hidden md:flex p-2 flex-col text-neutral-content">
    <h2 class="font-bold text-lg mt-5">Senaste fångst:</h2>
    <p v-if="latestCatch" class="text-xs">{{ formatDate(latestCatch.timestamp) }}</p>
    <div v-if="latestCatch" class="latest-catch flex items-center">
      <div class="avatar mt-4">
        <div class="mask mask-squircle h-16 w-16 lg:w-18 lg:h-18 lg:mr-2">
          <img v-if="latestCatch.thumbnail_image_url" :src="latestCatch.thumbnail_image_url" alt="Senaste fångst bild" class="cursor-pointer" @click="openSingleFishView(latestCatch.slug)">
          <span v-else class="flex items-center justify-center h-full w-full bg-base-200 text-base-300">Fisk</span>
        </div>
      </div>
      <div class="ml-4">
        <p class="mt-4 text-sm"><strong>Art:</strong> {{ latestCatch.species.name }}</p>
        <p class="text-sm"><strong>Plats:</strong> {{ latestCatch.location }}</p>
        <p class="text-sm"><strong>Väder:</strong> {{ latestCatch.weather }}, {{ latestCatch.air_temperature !== null ? formatTemperature(latestCatch.air_temperature) : 'Saknas' }}</p>
      </div>
    </div>
    <div v-else>
      <p>Ingen senaste fångst tillgänglig.</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../api';

export default {
  name: "LatestCatchWidget",
  setup() {
    const latestCatch = ref(null);
    const loading = ref(true);
    const router = useRouter();

    const fetchLatestCatch = async () => {
      loading.value = true;
      try {
        const response = await apiClient.get('/fish/latest');
        latestCatch.value = response.data;
      } catch (error) {
        console.error('Fel vid hämtning av senaste fångst:', error);
      } finally {
        loading.value = false;
      }
    };

    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString('sv-SE', options);
    };

    const formatTemperature = (temperature) => {
      return `${temperature.toFixed(1)} °C`;
    };

    const openSingleFishView = (slug) => {
      sessionStorage.setItem('previousRoute', router.currentRoute.value.fullPath);
      router.push({ name: 'SingleFishView', params: { slug } });
    };

    onMounted(fetchLatestCatch);

    return {
      latestCatch, 
      loading,
      openSingleFishView,
      formatDate,
      formatTemperature
    };
  },
};
</script>
