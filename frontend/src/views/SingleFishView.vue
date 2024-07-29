<template>
  <div class="p-4">
    <div class="max-w-4xl mx-auto flex flex-col items-start">
      <button @click="goBack" class="btn btn-ghost mb-4">
        <i class="fas fa-arrow-left mr-2"></i>
        Tillbaka
      </button>
    </div>
    <Spinner v-if="loading" :marginTop="true" />
    <div v-if="fish" class="max-w-4xl mx-auto flex flex-col gap-4">
      <div class="flex flex-col md:flex-row items-center md:items-start gap-4">
        <!-- Vänster kolumn: Foto -->
        <div class="flex justify-center items-center w-full md:w-1/2 p-2 rounded-lg border border-base-300 shadow-xl bg-base-100">
          <img :src="fish.medium_image_url" alt="Bild på (förmodligen) episk fångst" class="w-full h-auto rounded-lg" @click="openModal(fish.medium_image_url)">
        </div>
        <!-- Divider -->
        <div class="divider divider-horizontal md:block hidden"></div>
        <!-- Höger kolumn: Information -->
        <div class="w-full md:w-1/2 p-4 rounded-lg border border-base-300 shadow-xl bg-base-100">
          <h2 class="text-2xl font-bold">{{ fish.species.name }}</h2>
          <p class="text-sm italic text-gray-500 mb-4">{{ fish.species.latin_name }}</p>
          <div class="text-sm">
            <p class="mb-2"><strong>Fångad:</strong> {{ formatDate(fish.timestamp) }}</p>
            <p class="mb-2" v-if="fish.location"><strong>Plats:</strong> {{ fish.location }}</p>
            <p class="mb-2" v-if="fish.bait"><strong>Bete:</strong> {{ fish.bait.type }}</p>
            <p class="mb-2" v-if="fish.weight"><strong>Vikt:</strong> {{ fish.weight }} kg</p>
            <p class="mb-2" v-if="fish.length"><strong>Längd:</strong> {{ fish.length }} cm</p>
            <p class="mb-2" v-if="fish.weather"><strong>Väder:</strong> {{ fish.weather }}</p>
            <p class="mb-2" v-if="fish.air_temperature"><strong>Lufttemperatur:</strong> {{ formatTemperature(fish.air_temperature) }}</p>
            <p class="mb-2" v-if="fish.air_pressure"><strong>Lufttryck:</strong> {{ fish.air_pressure }} hPa</p>
            <p class="mb-2" v-if="fish.air_humidity"><strong>Luftfuktighet:</strong> {{ fish.air_humidity }} %</p>
            <p class="mb-2" v-if="fish.wind_speed"><strong>Vind:</strong> {{ Math.round(fish.wind_speed) }} m/s {{ fish.wind_dir }}</p>
            <p class="mb-2" v-if="fish.uv_index"><strong>UV-index:</strong> {{ Math.round(fish.uv_index) }}</p>
            <p class="mb-2" v-if="fish.moon_phase"><strong>Månfas:</strong> {{ fish.moon_phase }}</p>
            <p class="mb-2" v-if="fish.moon_illumination"><strong>Månbelysning:</strong> {{ fish.moon_illumination }}%</p>
          </div>
          <button @click="showOnMap" class="btn btn-sm btn-primary mt-4">
            <i class="fas fa-map-marker-alt mr-2"></i>
            Visa på kartan
          </button>
        </div>
      </div>
      <!-- Ny rad: Beskrivning -->
      <p class="mt-4" v-html="fish.species.description"></p>
    </div>
    <ImageModal :isVisible="isModalVisible" :imageUrl="selectedImageUrl" :fish="fish" @close="isModalVisible = false" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '../api';
import moment from 'moment';
import Spinner from '@/components/Spinner.vue';
import ImageModal from '@/components/ImageModal.vue';

export default {
  name: 'SingleFishView',
  components: {
    Spinner,
    ImageModal
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const fish = ref(null);
    const loading = ref(true);
    const isModalVisible = ref(false);
    const selectedImageUrl = ref('');

    const fetchFish = async (slug) => {
      loading.value = true;
      try {
        const response = await apiClient.get(`/fish/${slug}`);
        fish.value = response.data;
        if (fish.value) {
          const formattedDate = formatDate(fish.value.timestamp);
          const speciesName = fish.value.species.name.toLowerCase();
          document.title = `Ölunds Fiske - ${fish.value.species.name} fångad i ${fish.value.location} ${formattedDate}`;
          const descriptionMetaTag = document.querySelector('meta[name="description"]');
          if (descriptionMetaTag) {
            descriptionMetaTag.setAttribute('content', `Information om en ${speciesName} som fångades i ${fish.value.location} ${formattedDate}.`);
          } else {
            const newMetaTag = document.createElement('meta');
            newMetaTag.name = 'description';
            newMetaTag.content = `Information om en ${speciesName} som fångades i ${fish.value.location} ${formattedDate}.`;
            document.getElementsByTagName('head')[0].appendChild(newMetaTag);
          }

          // Sätt canonical URL
          const canonicalLink = document.querySelector('link[rel="canonical"]');
          if (canonicalLink) {
            canonicalLink.setAttribute('href', 'https://olundsfiske.se/fiskar');
          } else {
            const newCanonicalLink = document.createElement('link');
            newCanonicalLink.rel = 'canonical';
            newCanonicalLink.href = 'https://olundsfiske.se/fiskar';
            document.getElementsByTagName('head')[0].appendChild(newCanonicalLink);
          }

          // Sätt noindex meta-tagg
          let robotsMetaTag = document.querySelector('meta[name="robots"]');
          if (robotsMetaTag) {
            robotsMetaTag.setAttribute('content', 'noindex');
          } else {
            robotsMetaTag = document.createElement('meta');
            robotsMetaTag.name = 'robots';
            robotsMetaTag.content = 'noindex';
            document.getElementsByTagName('head')[0].appendChild(robotsMetaTag);
          }
        }
      } catch (error) {
        console.error('Fel vid hämtning av fisken:', error);
      } finally {
        loading.value = false;
      }
    };

    const formatDate = (timestamp) => {
      return moment(timestamp).format('YYYY-MM-DD HH:mm');
    };

    const formatTemperature = (temperature) => {
      return `${temperature.toFixed(1)} °C`;
    };

    const goBack = () => {
      const previousRoute = sessionStorage.getItem('previousRoute');
      const currentHostname = window.location.hostname;
      // Om besökaren kommer från direktlänk utifrån, omdirigera till /
      if (previousRoute && new URL(previousRoute, window.location.origin).hostname === currentHostname) {
        router.replace(previousRoute);
      } else {
        router.replace('/');
      }
    };

    const openModal = (url) => {
      selectedImageUrl.value = url;
      isModalVisible.value = true;
    };

    const showOnMap = () => {
      if (fish.value) {
        const { latitude, longitude } = fish.value;
        router.push({ name: 'Karta', query: { lat: latitude, lng: longitude, zoom: 15 } });
      }
    };

    onMounted(() => {
      fetchFish(route.params.slug);
    });

    return {
      fish,
      loading,
      formatDate,
      formatTemperature,
      goBack,
      isModalVisible,
      selectedImageUrl,
      openModal,
      showOnMap
    };
  }
};
</script>
