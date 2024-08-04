<template>
  <!-- Väderkolumnen -->
  <div v-if="weatherData" class="w-full md:w-2/3 lg:w-1/3 p-2">
    <div class="bg-neutral text-neutral-content h-full rounded-2xl ml-10">
      <div class="p-2 h-full">
        <div class="flex flex-col md:flex-row w-full h-full items-start">
          <!-- Dagens väder -->
          <div class="flex items-start w-full md:w-1/2 mt-1 mb-2 md:mb-0 p-2 lg:pr-4">
            <div>
              <h2 class="font-bold text-lg">{{ formattedDateDisplay(new Date()) }}</h2>
              <div class="flex mt-2 items-center">
                <div class="flex-1">
                  <div class="text-sm font-bold">Strängnäs just nu</div>
                  <div class="text-3xl font-bold" v-html="`${weatherData.current.temp_c} &deg;C`"></div>
                  <div class="text-xs">Vind: {{ (weatherData.current.wind_kph / 3.6).toFixed(1) }} m/s {{ translateWindDir(weatherData.current.wind_dir) }}</div>
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
          <div class="w-full md:w-1/2 p-2 lg:pl-4">
            <div class="grid grid-cols-2 gap-2">
              <div class="bg-neutral p-2 h-full rounded-xl flex flex-col items-center" v-for="(forecast, key) in weatherData.forecast.forecastday.slice(1)" :key="key">
                <div class="text-xs text-center">{{ formattedDate(forecast.date) }}</div>
                <div class="mx-auto tooltip tooltip-top" :data-tip="forecast.day.condition.text">
                  <img :src="`https:${forecast.day.condition.icon}`" :alt="forecast.day.condition.text" loading="lazy" class="block mx-auto">
                </div>
                <div class="font-semibold text-center" v-html="`${getWeatherForHour(forecast, 18)?.temp_c ?? 'N/A'} &deg;C`"></div>
                <div class="text-xs text-center">Vind: {{ (getWeatherForHour(forecast, 18)?.wind_kph / 3.6).toFixed(1) ?? 'N/A' }} m/s
                  {{ translateWindDir(getWeatherForHour(forecast, 18)?.wind_dir ?? 'N/A') }}</div>
                <div class="text-xs text-center">
                  Tryck: {{ getWeatherForHour(forecast, 18)?.pressure_mb ?? 'N/A' }} hPa
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Placeholder för laddning -->
  <div v-else class="animate-pulse p-2 w-full md:w-2/3 lg:w-1/3">
    <div class="bg-neutral text-neutral-content h-full rounded-2xl ml-10">
      <div class="p-2 h-full">
        <div class="flex flex-col md:flex-row w-full h-full items-start">
          <!-- Placeholder för dagens väder -->
          <div class="flex items-start w-full md:w-1/2 mb-2 md:mb-0 p-2 lg:pr-4">
            <div>
              <h2 class="font-bold text-lg bg-base-300 rounded h-6 w-3/4 mb-2"></h2>
              <div class="flex mt-2 items-center">
                <div class="flex-1">
                  <div class="text-sm font-bold bg-base-300 rounded h-4 w-1/2 mb-1.5"></div>
                  <div class="text-3xl font-bold bg-base-300 rounded h-10 w-1/2 mb-1.5"></div>
                  <div class="text-xs bg-base-300 rounded h-3 w-3/4 mb-1.5"></div>
                  <div class="text-xs bg-base-300 rounded h-3 w-3/4 mb-1.5"></div>
                  <div class="text-xs bg-base-300 rounded h-3 w-3/4 mb-1.5"></div>
                </div>
                <div class="w-24 h-24 ml-2 bg-base-300 rounded-full"></div>
              </div>
            </div>
          </div>
          <!-- Placeholder för kommande dagars väder -->
          <div class="w-full md:w-1/2 p-2 lg:pl-4">
            <div class="grid grid-cols-2 gap-2">
              <div class="bg-base-300 p-2 h-full rounded-xl flex flex-col items-center" v-for="n in 2" :key="n">
                <div class="text-xs text-center bg-base-300 rounded h-3 w-3/4 mb-1.5"></div>
                <div class="mx-auto bg-base-300 rounded-full w-16 h-16 mb-1.5"></div>
                <div class="font-semibold mt-1.5 text-center bg-base-300 rounded h-4 w-1/2 mb-1.5"></div>
                <div class="text-xs text-center bg-base-300 rounded h-3 w-3/4"></div>
                <div class="text-xs text-center bg-base-300 rounded h-3 w-3/4 mt-1.5"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import apiClient from '../api';
import { useToast } from 'vue-toastification';

export default {
  name: "WeatherWidget",
  setup() {
    const weatherData = ref(null);
    const loading = ref(true);
    const toast = useToast();

    // Funktion för att hämta väderdata
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
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchWeatherData(); // Hämta väderdata vid montering
    });

    const formattedDateDisplay = (date) => {
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      const formattedDate = new Date(date).toLocaleDateString('sv-SE', options);
      const [weekday, rest] = formattedDate.split(', ');
      return `${capitalizeFirstLetter(weekday)}`;
    };

    const formattedDate = (date) => {
      const dateObj = new Date(date);
      const weekday = dateObj.toLocaleDateString('sv-SE', { weekday: 'long' });
      const day = dateObj.getDate();
      const month = dateObj.toLocaleDateString('sv-SE', { month: 'short' });
      return `${capitalizeFirstLetter(weekday)} ${day} ${month}`;
    };

    const capitalizeFirstLetter = (string) => {
      return string.charAt(0).toUpperCase() + string.slice(1);
    };

    const getWeatherForHour = (forecastDay, targetHour) => {
      return forecastDay.hour.find(hourData => {
        const hourTime = new Date(hourData.time).getHours();
        return hourTime === targetHour;
      });
    };

    const translateWindDir = (dir) => {
      return dir.replace(/W/g, 'V').replace(/E/g, 'Ö');
    };

    return {
      weatherData,
      loading,
      formattedDateDisplay,
      formattedDate,
      getWeatherForHour,
      translateWindDir,
    };
  }
};
</script>
