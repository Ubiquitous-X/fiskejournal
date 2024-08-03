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
            <FishForm
              :fish="editingFish"
              :fishSpecies="fishSpecies"
              :fishBaits="fishBaits"
              :onUpdate="updateFish"
              :onCancel="cancelEdit"
            />
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
import FishForm from '@/components/FishForm.vue'; // Importera FishForm

export default {
  components: {
    FishForm, // Lägg till FishForm-komponenten här
  },
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

    const updateFish = async (payload) => {
      if (!editingFish.value) {
        return;
      }

      try {
        // Använd payload som erhålls från FishForm-komponenten
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
      toast.info('Redigering avbröts');
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
