<template>
  <div class="flex flex-wrap w-full h-full bg-neutral">
    <!-- Väderkolumnen -->
    <div class="w-full lg:w-1/3 p-2" v-if="weatherData">
      <div class="bg-neutral text-neutral-content h-full rounded-2xl ml-16">
        <div class="p-2 h-full">
          <div class="flex flex-col md:flex-row w-full h-full items-start">
            <!-- Dagens väder -->
            <div class="flex items-start w-full md:w-1/2 mb-2 md:mb-0 p-2">
              <div>
                <h2 class="font-bold text-lg">{{ formattedDateDisplay(new Date()) }}</h2>
                <div class="flex mt-2 items-center">
                  <div class="flex-1">
                    <div class="text-sm font-bold">Strängnäs</div>
                    <div class="text-3xl font-bold" v-html="`${weatherData.current.temp_c} &deg;C`"></div>
                    <div class="text-xs">Vind: {{ (weatherData.current.wind_kph / 3.6).toFixed(1) }} m/s {{ weatherData.current.wind_dir }}</div>
                    <div class="text-xs">Lufttryck: {{ weatherData.current.pressure_mb }} hPa</div>
                    <div class="text-xs">Luftfuktighet: {{ weatherData.current.humidity }} %</div>
                  </div>
                  <div class="w-24 h-24 ml-2 tooltip tooltip-top" :data-tip="weatherData.current.condition.text">
                    <img :src="`https:${weatherData.current.condition.icon}`" :alt="weatherData.current.condition.text" loading="lazy" class="w-full h-full">
                  </div>
                </div>
              </div>
            </div>
            <!-- Kommande dagars väder -->
            <div class="w-full md:w-1/2 p-2 mr-16">
              <div class="grid grid-cols-2 gap-2">
                <div class="bg-neutral p-2 m-0 h-full rounded-xl flex flex-col items-center" v-for="(forecast, key) in weatherData.forecast.forecastday.slice(1)" :key="key">
                  <div class="text-xs text-center">{{ formattedDate(forecast.date) }}</div>
                  <div class="mx-auto tooltip tooltip-top" :data-tip="forecast.day.condition.text">
                    <img :src="`https:${forecast.day.condition.icon}`" :alt="forecast.day.condition.text" loading="lazy" class="block mx-auto">
                  </div>
                  <div class="font-semibold mt-1.5 text-center" v-html="`${forecast.day.maxtemp_c} &deg;C`"></div>
                  <div class="text-xs text-center">Vind: {{ (forecast.day.maxwind_kph / 3.6).toFixed(1) }} m/s {{ forecast.day.wind_dir }}</div>
                  <div class="text-xs text-center">
                    Tryck: {{ getWeatherForHour(forecast, 10)?.pressure_mb ?? 'N/A' }} hPa
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Placeholder för laddning -->
    <div v-else class="animate-pulse p-2 w-full lg:w-1/3">
      <div class="bg-neutral text-neutral-content h-full rounded-2xl ml-16">
        <div class="p-2 h-full">
          <div class="flex flex-col md:flex-row w-full h-full items-start">
            <!-- Placeholder för dagens väder -->
            <div class="flex items-start w-full md:w-1/2 mb-2 md:mb-0 p-2">
              <div>
                <h2 class="font-bold text-lg bg-base-300 rounded h-4 w-3/4 mb-2"></h2>
                <div class="flex mt-2 items-center">
                  <div class="flex-1">
                    <div class="text-sm font-bold bg-base-300 rounded h-4 w-1/2 mb-1.5"></div>
                    <div class="text-3xl font-bold bg-base-300 rounded h-6 w-1/2 mb-1.5"></div>
                    <div class="text-xs bg-base-300 rounded h-3 w-3/4 mb-1.5"></div>
                    <div class="text-xs bg-base-300 rounded h-3 w-3/4 mb-1.5"></div>
                    <div class="text-xs bg-base-300 rounded h-3 w-3/4 mb-1.5"></div>
                  </div>
                  <div class="w-24 h-24 ml-2 bg-base-300 rounded-full"></div>
                </div>
              </div>
            </div>
            <!-- Placeholder för kommande dagars väder -->
            <div class="w-full md:w-1/2 p-2 mr-16">
              <div class="grid grid-cols-2 gap-2">
                <div class="bg-base-300 p-2 m-0 h-full rounded-xl flex flex-col items-center" v-for="n in 2" :key="n">
                  <div class="text-xs text-center bg-base-300 rounded h-3 w-3/4 mb-1.5"></div>
                  <div class="mx-auto bg-base-300 rounded-full w-12 h-12 mb-1.5"></div>
                  <div class="font-semibold mt-1.5 text-center bg-base-300 rounded h-4 w-1/2 mb-1.5"></div>
                  <div class="text-xs text-center bg-base-300 rounded h-3 w-3/4"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Antalet fiskar-kolumnen -->
    <div class="hidden lg:flex lg:w-2/3 p-2 flex-col text-neutral-content">
      <div class="w-full h-full p-4">
        <div class="flex flex-row w-full h-full">
          <!-- Gösar -->
          <div class="w-1/3 flex flex-col items-center p-2 tooltip tooltip-bottom" data-tip="Fångade gösar">
            <figure class="h-20 w-full">
              <img src="@/assets/gös.png" alt="Gös" class="rounded-xl w-full h-full object-contain">
            </figure>
            <div class="items-center text-center p-2">
              <count-up v-if="Number.isFinite(fishCounts['Gös'])" :endVal="fishCounts['Gös']" :duration="2" class="text-3xl font-extrabold" />
            </div>
          </div>
          <!-- Gäddor -->
          <div class="w-1/3 flex flex-col items-center p-2 tooltip tooltip-bottom" data-tip="Fångade gäddor">
            <figure class="h-20 w-full">
              <img src="@/assets/gädda.png" alt="Gädda" class="rounded-xl w-full h-full object-contain">
            </figure>
            <div class="items-center text-center p-2">
              <count-up v-if="Number.isFinite(fishCounts['Gädda'])" :endVal="fishCounts['Gädda']" :duration="2" class="text-3xl font-extrabold" />
            </div>
          </div>
          <!-- Abborrar -->
          <div class="w-1/3 flex flex-col items-center p-2 tooltip tooltip-bottom" data-tip="Fångade abborrar">
            <figure class="h-20 w-full">
              <img src="@/assets/abborre.png" alt="Abborre" class="rounded-xl w-full h-full object-contain">
            </figure>
            <div class="items-center text-center p-2">
              <count-up v-if="Number.isFinite(fishCounts['Abborre'])" :endVal="fishCounts['Abborre']" :duration="2" class="text-3xl font-extrabold" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import CountUp from 'vue-countup-v3';
import apiClient from '../api';
import { useToast } from 'vue-toastification';

export default {
  name: "StatsWidget",
  components: {
    CountUp
  },
  setup() {
    const weatherData = ref(null);
    const fishCounts = ref({
      'Gädda': 0,
      'Abborre': 0,
      'Gös': 0
    });
    const loading = ref(true);
    const toast = useToast();

    const fetchWeatherData = async () => {
      try {
        const response = await apiClient.get('/weather/key', { skipInterceptor: true });
        weatherData.value = response.data;
      } catch (error) {
        if (error.response && error.response.status === 500) {
          toast.error('Väderdata kunde ej hämtas');
        } else {
          console.error('Fel vid hämtning av väderdata:', error);
        }
      }
    };

    const fetchFishCounts = async () => {
      loading.value = true;
      try {
        const response = await apiClient.get('/fish/count');
        fishCounts.value = response.data;
      } catch (error) {
        console.error('Fel vid hämtning av fiskdata:', error);
      } finally {
        loading.value = false;
      }
    };

    const formattedDateDisplay = (date) => {
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString('sv-SE', options);
    };

    const formattedDate = (date) => {
      return date.split('-').reverse().join('/');
    };

    const getWeatherForHour = (forecastDay, targetHour) => {
      return forecastDay.hour.find(hourData => {
        const hourTime = new Date(hourData.time).getHours();
        return hourTime === targetHour;
      });
    };

    onMounted(() => {
      fetchWeatherData();
      fetchFishCounts();
    });

    return {
      weatherData,
      fishCounts,
      loading,
      formattedDateDisplay,
      formattedDate,
      getWeatherForHour
    };
  }
};
</script>

