<template>
  <div class="w-full mb-8 grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
    <!-- Formulär för att lägga till/redigera arter -->
    <div class="flex flex-col mb-4 border-r border-base-300 pr-4">
      <div class="form-control col-span-1 mb-2">
        <input
          v-model="newSpeciesName"
          type="text"
          placeholder="Ange artens namn"
          class="input input-bordered w-full"
        />
      </div>
      <div class="form-control col-span-1 mb-2">
        <input
          v-model="newSpeciesLatinName"
          type="text"
          placeholder="Ange det latinska namnet"
          class="input input-bordered w-full"
        />
      </div>
      <div class="form-control col-span-1 mb-2">
        <textarea
          v-model="newSpeciesDescription"
          placeholder="Ange artens beskrivning (i HTML)"
          class="textarea textarea-bordered w-full"
        ></textarea>
      </div>
      <div class="form-control col-span-1 mb-2">
        <button @click="editingSpecies ? updateSpecies() : addSpecies()" class="btn btn-primary w-full">
          {{ editingSpecies ? "Uppdatera arten" : "Lägg till ny art" }}
        </button>
      </div>
      <div class="form-control col-span-1" v-if="editingSpecies">
        <button @click="cancelEdit" class="btn btn-secondary w-full mt-2">Avbryt</button>
      </div>
    </div>

    <!-- Listan med arter -->
    <ul class="w-full">
      <li v-for="species in speciesList" :key="species.id" :class="{'bg-base-200': species.id === editingSpecies?.id}" class="flex flex-col md:flex-row justify-between items-start md:items-center p-2 border-b">
        <span class="mb-2 md:mb-0">
          <span class="font-bold">{{ species.name }}</span> 
          <span class="italic"> ({{ species.latin_name }})</span>
        </span>
        <div class="flex">
          <button @click="editSpecies(species)" class="btn btn-sm btn-warning mr-2">Redigera</button>
          <button @click="deleteSpecies(species.id)" class="btn btn-sm btn-error">Radera</button>
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
  name: 'SpeciesManagement',
  setup() {
    const speciesList = ref([]);
    const newSpeciesName = ref('');
    const newSpeciesLatinName = ref('');
    const newSpeciesDescription = ref('');
    const editingSpecies = ref(null);
    const toast = useToast();

    const fetchSpecies = async () => {
      try {
        const response = await apiClient.get('/species/all');
        speciesList.value = response.data;
      } catch (error) {
        console.error('Fel vid hämtning av arter:', error);
      }
    };

    const addSpecies = async () => {
      try {
        const response = await apiClient.post('/species/', {
          name: newSpeciesName.value,
          latin_name: newSpeciesLatinName.value,
          description: newSpeciesDescription.value
        });
        speciesList.value.push(response.data);
        newSpeciesName.value = '';
        newSpeciesLatinName.value = '';
        newSpeciesDescription.value = '';
        toast.success('Ny fiskart tillagd!');
      } catch (error) {
        console.error('Fel vid skapande av fiskart:', error);
      }
    };

    const editSpecies = (species) => {
      editingSpecies.value = species;
      newSpeciesName.value = species.name;
      newSpeciesLatinName.value = species.latin_name;
      newSpeciesDescription.value = species.description;
    };

    const cancelEdit = () => {
      editingSpecies.value = null;
      newSpeciesName.value = '';
      newSpeciesLatinName.value = '';
      newSpeciesDescription.value = '';
    };

    const updateSpecies = async () => {
      try {
        const response = await apiClient.put(`/species/edit/${editingSpecies.value.id}`, {
          name: newSpeciesName.value,
          latin_name: newSpeciesLatinName.value,
          description: newSpeciesDescription.value
        });
        const index = speciesList.value.findIndex(s => s.id === editingSpecies.value.id);
        speciesList.value[index] = response.data;
        editingSpecies.value = null;
        newSpeciesName.value = '';
        newSpeciesLatinName.value = '';
        newSpeciesDescription.value = '';
        toast.success('Fiskarten uppdaterad!');
      } catch (error) {
        console.error('Fel vid uppdatering av fiskart:', error);
      }
    };

    const deleteSpecies = async (speciesId) => {
      const confirmed = window.confirm("Är du säker på att du vill radera fiskarten?");
      
      if (confirmed) {
        try {
          const response = await apiClient.delete(`/species/delete/${speciesId}`);
          
          if (response.data.error) {
            toast.error(response.data.error);
          } else {
            speciesList.value = speciesList.value.filter(species => species.id !== speciesId);
            toast.success('Fiskarten raderad!');
          }
        } catch (error) {
          console.error('Fel vid radering av fiskart:', error);
          toast.error('Ett fel uppstod vid radering av fiskarten.');
        }
      }
    };

    onMounted(fetchSpecies);

    return {
      speciesList,
      newSpeciesName,
      newSpeciesLatinName,
      newSpeciesDescription,
      addSpecies,
      editSpecies,
      cancelEdit,
      updateSpecies,
      deleteSpecies,
      editingSpecies
    };
  }
};
</script>
