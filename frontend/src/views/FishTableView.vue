<template>
  <div class="flex-1 p-4">
    <Spinner v-if="loading" :marginTop="true" />
    <div class="overflow-x-auto">
      <table class="table w-full lg:w-3/4 lg:mx-auto">
        <thead>
          <tr>
            <th>Fisk</th>
            <th>Fångad</th>
            <th class="hidden md:table-cell">Väder</th>
            <th class="hidden md:table-cell">Lufttemp</th>
            <th class="hidden md:table-cell">Lufttryck</th>
            <th class="hidden lg:table-cell">Luftfuktighet</th>
            <th class="hidden lg:table-cell">Vind</th>
            <th class="hidden lg:table-cell">UV-index</th>
            <th class="hidden lg:table-cell">Månfas</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="fish in fishes" :key="fish.id" class="hover:bg-base-200 cursor-pointer" @click="openSingleFishView(fish.slug)">
            <td>
              <div class="flex items-center gap-3">
                <div class="avatar">
                  <div class="mask mask-squircle h-12 w-12 lg:w-14 lg:h-14 lg:mr-2">
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
            <td>{{ fish.timestamp ? formatDate(fish.timestamp) : 'Saknas' }}</td>
            <td class="hidden md:table-cell">
              <WeatherIcon :weatherDescription="fish.weather || 'Saknas'" :weatherIconUrl="fish.weather_icon_url || 'path/to/default/icon.png'" />
            </td>
            <td class="hidden md:table-cell">{{ fish.air_temperature !== null ? formatTemperature(fish.air_temperature) : 'Saknas' }}</td>
            <td class="hidden md:table-cell">{{ fish.air_pressure !== null ? fish.air_pressure + ' hPa' : 'Saknas' }}</td>
            <td class="hidden lg:table-cell">{{ fish.air_humidity !== null ? fish.air_humidity + ' %' : 'Saknas' }}</td>
            <td class="hidden lg:table-cell">{{ fish.wind_speed !== null ? Math.round(fish.wind_speed) + ' m/s ' + fish.wind_dir : 'Saknas' }}</td>
            <td class="hidden lg:table-cell">{{ fish.uv_index !== null ? Math.round(fish.uv_index) : 'Saknas' }}</td>
            <td class="hidden lg:table-cell">
              <MoonPhase :phase="fish.moon_phase || 'Saknas'" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
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
    const loading = ref(true);
    const router = useRouter();

    const fetchFishes = async () => {
      loading.value = true;
      try {
        const response = await apiClient.get('/fish/all');
        fishes.value = response.data;
      } catch (error) {
        console.error('Fel vid hämtning av fiskar:', error);
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

    onMounted(() => {
      setCanonicalUrl();
      fetchFishes();
    });

    return {
      fishes,
      loading,
      formatDate,
      formatTemperature,
      openSingleFishView
    };
  }
};
</script>

<style scoped>
th {
  font-weight: 800;
}
</style>
