<template>
  <div class="w-full mb-8 grid grid-cols-1 gap-4 mt-4">
    <ul class="w-full mb-4">
      <li v-for="fish in fishList" :key="fish.id" :class="{'bg-base-200': fish.id === editingFish?.id}" class="flex flex-col p-2 border-b">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center w-full">
          <div class="flex items-center w-full mb-2 md:mb-0">
            <div class="avatar mr-4">
              <div class="mask mask-squircle h-12 w-12">
                <img v-if="fish.thumbnail_image_url" :src="fish.thumbnail_image_url" alt="Fisk" />
                <span v-else class="flex items-center justify-center h-full w-full bg-base-200 text-base-300">Fisk</span>
              </div>
            </div>
            <div class="flex-1">
              <span class="font-bold">{{ formatDate(fish.timestamp) }}</span><br>
              <span>{{ fish.species.name }} - {{ fish.location }}</span>
            </div>
          </div>
          <div class="flex">
            <button @click="editFish(fish)" class="btn btn-sm btn-warning mr-2">Redigera</button>
            <button @click="deleteFish(fish.id)" class="btn btn-sm btn-error">Radera</button>
          </div>
        </div>
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
                <label for="air_humidity" class="label">
                  <span class="label-text">Luftfuktighet (%):</span>
                </label>
                <input v-model.number="editingFish.air_humidity" id="air_humidity" type="number" step="1" class="input input-bordered w-full" />
              </div>
              <div class="form-control col-span-1">
                <label for="weather" class="label">
                  <span class="label-text">Väder:</span>
                </label>
                <input v-model="editingFish.weather" id="weather" type="text" class="input input-bordered w-full" />
              </div>
              <div class="form-control col-span-1">
                <label for="weather_icon_url" class="label">
                  <span class="label-text">Väderikon URL:</span>
                </label>
                <input v-model="editingFish.weather_icon_url" id="weather_icon_url" type="text" class="input input-bordered w-full" />
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
                <label for="location" class="label">
                  <span class="label-text">Fångstplats:</span>
                </label>
                <input v-model="editingFish.location" id="location" type="text" class="input input-bordered w-full" />
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
      </li>
    </ul>
  </div>
</template>


<script>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import moment from 'moment';
import apiClient from '../api';

export default {
  setup() {
    const fishList = ref([]);
    const editingFish = ref(null);
    const editingSpecies = ref(null);
    const editingBait = ref(null);
    const fishSpecies = ref([]);
    const fishBaits = ref([]);
    const toast = useToast();

    onMounted(async () => {
      await loadData();
    });

    const loadData = async () => {
      try {
        const [fishData, speciesData, baitsData] = await Promise.all([
          fetchFishList(),
          fetchFishSpecies(),
          fetchFishBaits(),
        ]);
        fishList.value = fishData;
        fishSpecies.value = speciesData;
        fishBaits.value = baitsData;
      } catch (error) {
        console.error('Fel vid laddning av data:', error);
      }
    };

    const formatDate = (timestamp) => {
      return moment(timestamp).format('YYYY-MM-DD HH:mm');
    };

    const fetchFishList = async () => {
      const response = await apiClient.get('/fish/all');
      return response.data;
    };

    const fetchFishSpecies = async () => {
      const response = await apiClient.get('/species/all');
      return response.data;
    };

    const fetchFishBaits = async () => {
      const response = await apiClient.get('/baits/all');
      return response.data;
    };

    const editFish = (fish) => {
      if (editingFish.value && editingFish.value.id === fish.id) {
        cancelEdit();
      } else {
        editingFish.value = { ...fish };
        editingSpecies.value = fish.species.id;
        editingBait.value = fish.bait ? fish.bait.id : null;
      }
    };

    const updateFish = async () => {
      if (!editingFish.value) {
        return;
      }

      try {
        // Konvertera tomma strängar till null för numeriska värden
        const payload = { 
          ...editingFish.value, 
          species: editingSpecies.value,
          bait: editingBait.value
        };

        // Kontrollera och konvertera numeriska fält till null om de är tomma strängar
        Object.keys(payload).forEach(key => {
          if (payload[key] === '') {
            payload[key] = null;
          }
        });

        console.log('Payload:', payload);
        const response = await apiClient.put(`/fish/edit/${editingFish.value.id}`, payload);
        const index = fishList.value.findIndex(f => f.id === editingFish.value.id);
        fishList.value[index] = response.data;
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
      const confirmed = window.confirm("Är du säker på att du vill radera fisken?");
      
      if (confirmed) {
        try {
          await apiClient.delete(`/fish/delete/${fishId}`);
          fishList.value = fishList.value.filter(fish => fish.id !== fishId);
          toast.success('Fisk raderad!');
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
    };

    return {
      fishList,
      editingFish,
      editingSpecies,
      editingBait,
      fishSpecies,
      fishBaits,
      editFish,
      updateFish,
      deleteFish,
      cancelEdit,
      formatDate,
    };
  }
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>
