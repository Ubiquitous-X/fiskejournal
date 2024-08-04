<template>
    <!-- Antalet fiskar-kolumnen -->
    <div class="flex-grow-[2] hidden lg:flex p-2 flex-col text-neutral-content">
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
</template>

<script>
import { ref, onMounted } from 'vue';
import CountUp from 'vue-countup-v3';
import apiClient from '../api';
import { useToast } from 'vue-toastification';

export default {
  name: "StatsWidget",
  components: {
    CountUp,
  },
  setup() {
    const fishCounts = ref({
      'Gädda': 0,
      'Abborre': 0,
      'Gös': 0
    });
    const loading = ref(true);
    const toast = useToast();

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

    onMounted(() => {
      fetchFishCounts();
    });

    return {
      fishCounts,
      loading
    };
  }
};
</script>