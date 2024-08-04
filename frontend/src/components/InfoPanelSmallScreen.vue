<template>
  <div class="flex flex-wrap w-full h-full bg-neutral p-2 text-neutral-content">
    <div
      v-if="latestCatch"
      class="flex items-center cursor-pointer"
      @click="openSingleFishView(latestCatch.slug)"
    >
      <div class="avatar mr-4">
        <div class="mask rounded-xl h-10 w-10">
          <img
            v-if="latestCatch.thumbnail_image_url"
            :src="latestCatch.thumbnail_image_url"
            alt="Senaste fångst bild"
          />
          <span v-else class="flex items-center justify-center h-full w-full bg-base-200 text-base-300">Fisk</span>
        </div>
      </div>
<!--       <div class="flex flex-col">
        <p class="font-bold text-sm mb-1">Senaste fångst: {{ formatDate(latestCatch.timestamp) }}</p>
        <p class="text-xs">En {{ latestCatch.species.name.charAt(0).toLowerCase() + latestCatch.species.name.slice(1) }} fångad i {{ latestCatch.location }}</p>
      </div> -->
      <div class="flex flex-col">
        <p class="font-bold text-sm mb-1">Senaste fångsten var en {{ latestCatch.species.name.charAt(0).toLowerCase() + latestCatch.species.name.slice(1) }}!</p>
        <p class="text-xs">Fångad i {{ latestCatch.location }} den {{ formatDate(latestCatch.timestamp) }}</p>
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
  name: "InfoPanelSmallScreen",
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
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
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
