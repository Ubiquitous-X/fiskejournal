<template>
  <div class="w-full mb-8 grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
    <!-- Formulär för att lägga till/redigera beten -->
    <div class="flex flex-col mb-4 border-r border-base-300 pr-4">
      <div class="form-control col-span-1 mb-2">
        <input
          v-model="newBaitType"
          type="text"
          placeholder="Ange betestyp"
          class="input input-bordered w-full"
        />
      </div>
      <div class="form-control col-span-1 mb-2">
        <button @click="editingBait ? updateBait() : addBait()" class="btn btn-primary w-full">
          {{ editingBait ? "Uppdatera betet" : "Lägg till nytt bete" }}
        </button>
      </div>
      <div class="form-control col-span-1" v-if="editingBait">
        <button @click="cancelEdit" class="btn btn-secondary w-full mt-2">Avbryt</button>
      </div>
    </div>

    <!-- Listan med beten -->
    <ul class="w-full">
      <li v-for="bait in baits" :key="bait.id" :class="{'bg-base-200': bait.id === editingBait?.id}" class="flex flex-col md:flex-row justify-between items-start md:items-center p-2 border-b">
        <span class="mb-2 md:mb-0 font-bold">{{ bait.type }}</span>
        <div class="flex">
          <button @click="editBait(bait)" class="btn btn-sm btn-warning mr-2">Redigera</button>
          <button @click="deleteBait(bait.id)" class="btn btn-sm btn-error">Radera</button>
        </div>
      </li>
    </ul>
  </div>
</template>


<script>
import { ref, onMounted } from 'vue';
import apiClient from '../api';
import { useToast } from 'vue-toastification';

export default {
  name: 'BaitManagement',
  setup() {
    const baits = ref([]);
    const newBaitType = ref('');
    const editingBait = ref(null);
    const toast = useToast();

    const fetchBaits = async () => {
      try {
        const response = await apiClient.get('/baits/all');
        baits.value = response.data;
      } catch (error) {
        console.error('Fel vid hämtning av beten:', error);
      }
    };

    const addBait = async () => {
      try {
        const response = await apiClient.post('/baits/', { type: newBaitType.value });
        baits.value.push(response.data);
        newBaitType.value = '';
        toast.success('Bete tillagt!');
      } catch (error) {
        console.error('Fel vid skapande av bete:', error);
      }
    };

    const editBait = (bait) => {
      editingBait.value = bait;
      newBaitType.value = bait.type;
    };

    const cancelEdit = () => {
      editingBait.value = null;
      newBaitType.value = '';
    };

    const updateBait = async () => {
      try {
        const response = await apiClient.put(`/baits/edit/${editingBait.value.id}`, { type: newBaitType.value });
        const index = baits.value.findIndex(b => b.id === editingBait.value.id);
        baits.value[index] = response.data;
        editingBait.value = null;
        newBaitType.value = '';
        toast.success('Betet uppdaterat!');
      } catch (error) {
        console.error('Fel vid uppdatering av bete:', error);
      }
    };

    const deleteBait = async (baitId) => {
      const confirmed = window.confirm("Är du säker på att du vill radera betet?");
      
      if (confirmed) {
        try {
          await apiClient.delete(`/baits/delete/${baitId}`);
          baits.value = baits.value.filter(bait => bait.id !== baitId);
          toast.success('Bete raderat!');
        } catch (error) {
          console.error('Fel vid radering av bete:', error);
          toast.error('Ett fel uppstod vid radering av betet.');
        }
      } 
    };

    onMounted(fetchBaits);

    return {
      baits,
      newBaitType,
      addBait,
      editBait,
      cancelEdit,
      updateBait,
      deleteBait,
      editingBait
    };
  }
};
</script>
