<template>
  <div class="flex-1 p-2">
    <Spinner v-if="loading" :marginTop="true" />
    <div class="overflow-x-auto">
      <table class="table w-full lg:w-3/4 lg:mx-auto">
        <thead>
          <tr>
            <th>Fisk och fångstplats</th>
            <th>Tidpunkt</th>
            <th class="hidden md:table-cell">Väder</th>
            <th class="hidden md:table-cell">Lufttemp</th>
            <th class="hidden md:table-cell">Lufttryck</th>
            <th class="hidden lg:table-cell">Luftfuktighet</th>
            <th class="hidden lg:table-cell">Vind</th>
            <th class="hidden lg:table-cell">UV-index</th>
            <th class="hidden lg:table-cell">Månbelysning</th>
            <th class="hidden lg:table-cell">Månfas</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="fish in fishes" :key="fish.id" class="hover:bg-base-200 cursor-pointer" @click="openSingleFishView(fish.slug)">
            <td>
              <div class="flex items-center gap-3">
                <div class="avatar">
                  <div class="mask rounded-xl h-12 w-12 lg:w-14 lg:h-14 lg:mr-2">
                    <img v-if="fish.thumbnail_image_url" :src="fish.thumbnail_image_url" alt="Fisk" />
                    <span v-else class="flex items-center justify-center h-full w-full bg-base-200 text-base-300">Fisk</span>
                  </div>
                </div>
                <div>
                  <div class="font-bold">{{ fish.species.name }}</div>
                  <div class="text-sm opacity-50">{{ fish.location || 'Saknas' }}</div>
                </div>
              </div>
            </td>
            <td>
            <div>
              <div>{{ formatDate(fish.timestamp).date }}</div>
              <div class="text-sm opacity-50">{{ formatDate(fish.timestamp).time }}</div>
            </div>
            </td>
            <td class="hidden md:table-cell">
              <WeatherIcon :weatherDescription="fish.weather || 'Saknas'" :weatherIconUrl="fish.weather_icon_url || 'path/to/default/icon.png'" />
            </td>
            <td class="hidden md:table-cell">{{ fish.air_temperature !== null ? formatTemperature(fish.air_temperature) : 'Saknas' }}</td>
            <td class="hidden md:table-cell">{{ fish.air_pressure !== null ? fish.air_pressure + ' hPa' : 'Saknas' }}</td>
            <td class="hidden lg:table-cell">{{ fish.air_humidity !== null ? fish.air_humidity + ' %' : 'Saknas' }}</td>
            <td class="hidden lg:table-cell">{{ fish.wind_speed !== null ? Math.round(fish.wind_speed) + ' m/s ' + fish.wind_dir : 'Saknas' }}</td>
            <td class="hidden lg:table-cell">{{ fish.uv_index !== null ? Math.round(fish.uv_index) : 'Saknas' }}</td>
             <td class="hidden lg:table-cell">{{ fish.moon_illumination !== null ? fish.moon_illumination + ' %' : 'Saknas' }}</td>
            <td class="hidden lg:table-cell">
              <MoonPhase :phase="fish.moon_phase || 'Saknas'" />
            </td>           
          </tr>
        </tbody>
      </table>
    </div>
    <div ref="loadMoreTrigger" style="height: 1px;"></div>
    <div class="max-w-4xl mx-auto flex justify-between items-center mt-4 sm:hidden">
      <router-link to="/" class="btn btn-ghost">
        <i class="fas fa-arrow-left mr-2"></i>
        Till startsidan
      </router-link>
      <router-link to="/karta" class="btn btn-ghost flex items-center">
        Till kartan
        <i class="fas fa-arrow-right ml-2"></i>
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import apiClient from '../api';
import moment from 'moment';
import Spinner from '@/components/Spinner.vue';
import MoonPhase from '@/components/MoonPhase.vue';
import WeatherIcon from '@/components/WeatherIcon.vue';
import { useRouter } from 'vue-router';

export default {
  name: 'FishView',
  components: {
    Spinner,
    MoonPhase,
    WeatherIcon
  },
  setup() {
    const fishes = ref([]);
    const loading = ref(false);
    const loadMoreTrigger = ref(null);
    const router = useRouter();

    const loadMoreFishes = async () => {
      if (loading.value) return;
      loading.value = true;
      try {
        const response = await apiClient.get('/fish/paginated', { params: { offset: fishes.value.length, limit: 30 } });
        fishes.value.push(...response.data);
      } catch (error) {
        console.error('Fel vid hämtning av fiskar:', error);
      } finally {
        loading.value = false;
      }
    };

    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        loadMoreFishes();
      }
    }, {
      root: null,
      threshold: 0.1
    });

    onMounted(() => {
      setCanonicalUrl();
      if (loadMoreTrigger.value) {
        observer.observe(loadMoreTrigger.value);
      }
      loadMoreFishes();
    });

    onUnmounted(() => {
      if (loadMoreTrigger.value) {
        observer.unobserve(loadMoreTrigger.value);
      }
    });

    const formatDate = (timestamp) => {
      return {
        date: moment(timestamp).format('YYYY-MM-DD'),
        time: moment(timestamp).format('HH:mm')
      };
    };

    const formatTemperature = (temperature) => {
      return `${temperature.toFixed(1)} °C`;
    };

    const openSingleFishView = (slug) => {
      sessionStorage.setItem('previousRoute', router.currentRoute.value.fullPath);
      router.push({ name: 'SingleFishView', params: { slug } });
    };

    const setCanonicalUrl = () => {
      const existingCanonicalLink = document.querySelector("link[rel='canonical']");
      if (existingCanonicalLink) {
        existingCanonicalLink.remove();
      }
      const link = document.createElement('link');
      link.setAttribute('rel', 'canonical');
      link.setAttribute('href', 'https://olundsfiske.se/fiskar');
      document.head.appendChild(link);
    };

    return {
      fishes,
      loading,
      formatDate,
      formatTemperature,
      openSingleFishView,
      loadMoreTrigger
    };
  }
};
</script>

<style scoped>
th {
  font-weight: 800;
}
</style>
