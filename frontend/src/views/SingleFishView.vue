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
            <p class="mb-2 mt-4" v-if="fish.description">{{ fish.description }}</p>
          </div>
          <!-- Första raden med knappen "Visa på kartan" -->
          <div class="flex gap-4 mt-4">
            <button @click="showOnMap" class="btn btn-sm btn-primary">
              <i class="fas fa-map-marker-alt mr-2"></i>
              Visa på kartan
            </button>
          </div>
          <!-- Andra raden med knapparna "Redigera" och "Radera" visas endast om användaren är inloggad -->
          <div class="flex gap-4 mt-2" v-if="isLoggedIn">
            <button @click="editFish(fish)" class="btn btn-sm btn-warning">
              <i class="fas fa-edit mr-2"></i>
              Redigera
            </button>
            <button @click="deleteFish(fish.id)" class="btn btn-sm btn-error">
              <i class="fas fa-trash mr-2"></i>
              Radera
            </button>
          </div>
        </div>
      </div>
      <!-- Formulärkomponent -->
      <transition name="fade">
        <div v-if="editingFish && editingFish.id === fish.id" class="w-full mt-4">
          <form @submit.prevent="updateFish" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="form-control col-span-1">
              <label for="species" class="label">
                <span class="label-text">Art:</span>
              </label>
              <select v-model="editingSpecies" id="species" class="select select-bordered w-full">
                <option v-for="species in fishSpecies" :key="species.id" :value="species.id">{{ species.name }}</option>
              </select>
            </div>
            <div class="form-control col-span-1">
              <label for="bait" class="label">
                <span class="label-text">Bete:</span>
              </label>
              <select v-model="editingBait" id="bait" class="select select-bordered w-full">
                <option v-for="bait in fishBaits" :key="bait.id" :value="bait.id">{{ bait.type }}</option>
              </select>
            </div>
            <div class="form-control col-span-1">
              <label for="weight" class="label">
                <span class="label-text">Vikt (kg):</span>
              </label>
              <input v-model.number="editingFish.weight" id="weight" type="number" step="0.01" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="length" class="label">
                <span class="label-text">Längd (cm):</span>
              </label>
              <input v-model.number="editingFish.length" id="length" type="number" step="0.1" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="location" class="label">
                <span class="label-text">Fångstplats:</span>
              </label>
              <input v-model="editingFish.location" id="location" type="text" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="weather" class="label">
                <span class="label-text">Väder:</span>
              </label>
              <input v-model="editingFish.weather" id="weather" type="text" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="latitude" class="label">
                <span class="label-text">Latitud:</span>
              </label>
              <input v-model.number="editingFish.latitude" id="latitude" type="number" step="0.0001" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="longitude" class="label">
                <span class="label-text">Longitud:</span>
              </label>
              <input v-model.number="editingFish.longitude" id="longitude" type="number" step="0.0001" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="air_temperature" class="label">
                <span class="label-text">Lufttemperatur (°C):</span>
              </label>
              <input v-model.number="editingFish.air_temperature" id="air_temperature" type="number" step="0.1" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="air_pressure" class="label">
                <span class="label-text">Lufttryck (hPa):</span>
              </label>
              <input v-model.number="editingFish.air_pressure" id="air_pressure" type="number" step="1" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="wind_speed" class="label">
                <span class="label-text">Vindhastighet (m/s):</span>
              </label>
              <input v-model.number="editingFish.wind_speed" id="wind_speed" type="number" step="0.1" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="wind_dir" class="label">
                <span class="label-text">Vindriktning:</span>
              </label>
              <input v-model="editingFish.wind_dir" id="wind_dir" type="text" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="air_humidity" class="label">
                <span class="label-text">Luftfuktighet (%):</span>
              </label>
              <input v-model.number="editingFish.air_humidity" id="air_humidity" type="number" step="1" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="uv_index" class="label">
                <span class="label-text">UV-index:</span>
              </label>
              <input v-model.number="editingFish.uv_index" id="uv_index" type="number" step="0.1" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="moon_phase" class="label">
                <span class="label-text">Månfas:</span>
              </label>
              <input v-model="editingFish.moon_phase" id="moon_phase" type="text" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="moon_illumination" class="label">
                <span class="label-text">Månens belysning (%):</span>
              </label>
              <input v-model.number="editingFish.moon_illumination" id="moon_illumination" type="number" step="0.1" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="medium_image_url" class="label">
                <span class="label-text">Medium foto URL:</span>
              </label>
              <input v-model="editingFish.medium_image_url" id="medium_image_url" type="text" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="thumbnail_image_url" class="label">
                <span class="label-text">Thumbnail foto URL:</span>
              </label>
              <input v-model="editingFish.thumbnail_image_url" id="thumbnail_image_url" type="text" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1">
              <label for="weather_icon_url" class="label">
                <span class="label-text">Väderikon URL:</span>
              </label>
              <input v-model="editingFish.weather_icon_url" id="weather_icon_url" type="text" class="input input-bordered w-full" />
            </div>
            <div class="form-control col-span-1 md:col-span-2">
              <label for="description" class="label">
                <span class="label-text">Beskrivning:</span>
              </label>
              <textarea v-model="editingFish.description" id="description" class="textarea textarea-bordered w-full"></textarea>
            </div>
            <div class="col-span-1 md:col-span-2 flex justify-between">
              <button type="submit" class="btn btn-primary w-1/2 mr-2">Uppdatera</button>
              <button @click="cancelEdit" class="btn btn-secondary w-1/2">Avbryt</button>
            </div>
          </form>
        </div>
      </transition>
      <!-- Ny rad: Beskrivning -->
      <p class="mt-4" v-html="fish.species.description" v-if="!editingFish"></p>
    </div>
    <ImageModal :isVisible="isModalVisible" :imageUrl="selectedImageUrl" :fish="fish" @close="isModalVisible = false" />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import apiClient from '../api';
import moment from 'moment';
import Spinner from '@/components/Spinner.vue';
import ImageModal from '@/components/ImageModal.vue';
import { useToast } from 'vue-toastification';

export default {
  name: 'SingleFishView',
  components: {
    Spinner,
    ImageModal,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    const fish = ref(null);
    const loading = ref(true);
    const isModalVisible = ref(false);
    const selectedImageUrl = ref('');
    const editingFish = ref(null);
    const editingSpecies = ref(null);
    const editingBait = ref(null);
    const fishSpecies = ref([]);
    const fishBaits = ref([]);
    const toast = useToast();

    const isLoggedIn = computed(() => store.getters.isLoggedIn);

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

    const fetchSpeciesAndBaits = async () => {
      try {
        const speciesResponse = await apiClient.get('/species/all');
        const baitsResponse = await apiClient.get('/baits/all');
        fishSpecies.value = speciesResponse.data;
        fishBaits.value = baitsResponse.data;
      } catch (error) {
        console.error('Fel vid hämtning av arter eller beten:', error);
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

    const editFish = (fish) => {
      editingFish.value = { ...fish };
      editingSpecies.value = fish.species.id;
      editingBait.value = fish.bait ? fish.bait.id : null;
    };

    const updateFish = async () => {
      if (!editingFish.value) {
        return;
      }

      try {
        const payload = {
          ...editingFish.value,
          species: editingSpecies.value,
          bait: editingBait.value,
        };

        // Kontrollera och konvertera numeriska fält till null om de är tomma strängar
        Object.keys(payload).forEach((key) => {
          if (payload[key] === '') {
            payload[key] = null;
          }
        });

        const response = await apiClient.put(`/fish/edit/${editingFish.value.id}`, payload);
        fish.value = response.data;
        editingFish.value = null;
        editingSpecies.value = null;
        editingBait.value = null;
        toast.success('Fisk uppdaterad!');
      } catch (error) {
        console.error('Fel vid uppdatering av fisk:', error);
        toast.error('Ett fel uppstod vid uppdatering av fisken.');
      }
    };

    const deleteFish = async (fishId) => {
      const confirmed = window.confirm('Är du säker på att du vill radera fisken?');

      if (confirmed) {
        try {
          await apiClient.delete(`/fish/delete/${fishId}`);
          toast.success('Fisk raderad!');
          router.replace('/fiskar');
        } catch (error) {
          console.error('Fel vid radering av fisk:', error);
          toast.error('Ett fel uppstod vid radering av fisken.');
        }
      }
    };

    const cancelEdit = () => {
      editingFish.value = null;
      editingSpecies.value = null;
      editingBait.value = null;
      toast.info('Redigering avbröts');
    };

    onMounted(() => {
      fetchFish(route.params.slug);
      fetchSpeciesAndBaits();
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
      showOnMap,
      editingFish,
      editingSpecies,
      editingBait,
      fishSpecies,
      fishBaits,
      editFish,
      updateFish,
      deleteFish,
      cancelEdit,
      isLoggedIn,
    };
  },
};
</script>
