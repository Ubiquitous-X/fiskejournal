<template>
  <div class="flex justify-center">
    <div class="w-full lg:w-3/4 p-4 md:p-8 rounded-lg">
      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4">
        <!-- Döljer knappen på små skärmar -->
        <router-link
          to="/"
          exact-active-class="active"
          class="btn btn-ghost mb-2 hidden sm:flex sm:items-center"
        >
          <i class="fas fa-arrow-left mr-2"></i>
          Tillbaka
        </router-link>
        <!-- Filter toggles -->
        <div class="flex gap-4 justify-start mt-2 sm:mt-0">
          <div v-for="species in speciesList" :key="species" class="flex items-center">
            <span class="mr-2 text-sm md:text-base">{{ species }}</span>
            <input
              type="checkbox"
              class="toggle toggle-sm md:toggle-md"
              :checked="isSpeciesActive(species)"
              @change="toggleFilter(species)"
            />
          </div>
        </div>
      </div>
      <div class="masonry-grid">
        <div
          v-for="(fish, index) in filteredFishData"
          :key="fish.id"
          :class="['masonry-item', getRandomSize(index)]"
          @click="openModal(fish.medium_image_url, fish)"
        >
          <div
            :class="{ 'loading-placeholder': loadingImages[index] }"
            class="relative w-full h-full overflow-hidden rounded-lg shadow-md group"
          >
            <img
              :src="fish.medium_image_url"
              alt="Fish image"
              class="w-full h-full object-cover transition-opacity duration-300"
              @load="handleImageLoad(index)"
              :style="{ opacity: loadingImages[index] ? 0 : 1 }"
            />
            <!-- Laddningsindikator -->
            <div
              v-if="loadingImages[index]"
              class="absolute inset-0 flex items-center justify-center bg-base-300 bg-opacity-50"
            >
              <span class="loading loading-spinner loading-md text-base-content"></span>
            </div>
            <!-- Hover Overlay -->
            <div class="absolute inset-0 bg-neutral bg-opacity-50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 cursor-pointer">
              <div class="text-center text-base-100 p-4">
                <p class="text-lg font-bold">{{ fish.species.name }}</p>
                <p class="text-sm">Fångad i {{ fish.location }}</p>
                <p class="text-xs mt-4">{{ formatDate(fish.timestamp) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <ImageModal
      :isVisible="isModalVisible"
      :imageUrl="selectedImageUrl"
      :fish="selectedFish"
      @close="isModalVisible = false"
    />
  </div>
</template>

<script>
import { defineComponent, onMounted, ref, computed } from 'vue';
import apiClient from '../api';
import ImageModal from '@/components/ImageModal.vue';

export default defineComponent({
  name: "GalleryView",
  components: { ImageModal },
  setup() {
    const fishData = ref([]);
    const isModalVisible = ref(false);
    const selectedImageUrl = ref('');
    const selectedFish = ref(null);
    const loadingImages = ref([]);

    const fetchFishData = async () => {
      try {
        const response = await apiClient.get('/fish/all');
        fishData.value = response.data;
        // Initiera laddningsstatus för varje bild
        loadingImages.value = new Array(response.data.length).fill(true);
      } catch (error) {
        console.error('Error fetching fish data:', error);
      }
    };

    // Lista över fiskarter
    const speciesList = ['Abborre', 'Gädda', 'Gös'];
    const activeFilters = ref(new Set(speciesList)); // Alla aktiva från början

    // Beräknad egenskap för att filtrera fisken
    const filteredFishData = computed(() => {
      return fishData.value.filter(fish => activeFilters.value.has(fish.species.name));
    });

    const toggleFilter = (species) => {
      if (activeFilters.value.has(species)) {
        activeFilters.value.delete(species);
      } else {
        activeFilters.value.add(species);
      }
    };

    const isSpeciesActive = (species) => {
      return activeFilters.value.has(species);
    };

    const getRandomSize = (index) => {
      const sizes = ['small', 'medium', 'large'];
      return sizes[index % sizes.length];
    };

    const openModal = (url, fish) => {
      selectedImageUrl.value = url;
      selectedFish.value = fish;
      isModalVisible.value = true;
    };

    const handleImageLoad = (index) => {
      loadingImages.value[index] = false; // Bilden är inladdad, ta bort laddningsindikatorn
    };

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      const day = date.getDate();
      const month = date.toLocaleString('sv-SE', { month: 'long' });
      const year = date.getFullYear();
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');

      return `${day} ${month} ${year} ${hours}:${minutes}`;
    };

    onMounted(() => {
      fetchFishData();
    });

    return {
      fishData,
      filteredFishData,
      speciesList,
      toggleFilter,
      isSpeciesActive,
      getRandomSize,
      isModalVisible,
      selectedImageUrl,
      selectedFish,
      openModal,
      loadingImages,
      handleImageLoad,
      formatDate,
    };
  }
});
</script>

<style scoped>
.masonry-grid {
  column-count: 2; /* Default till 2 kolumner på minsta skärmarna */
  column-gap: 1rem;
}

@media (min-width: 640px) {
  /* Små skärmar */
  .masonry-grid {
    column-count: 4;
  }
}

@media (min-width: 1024px) {
  /* Större skärmar */
  .masonry-grid {
    column-count: 5;
  }
}

.masonry-item {
  margin-bottom: 1rem;
  break-inside: avoid;
  overflow: hidden;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.loading-placeholder {
  background-color: #e5e7eb; /* Ljusgrå bakgrund för laddning */
  position: relative;
}

/* Mindre bildstorlekar för små skärmar */
.small {
  height: 150px;
}

.medium {
  height: 230px;
}

.large {
  height: 270px;
}

/* Större bildstorlekar för medelstora skärmar */
@media (min-width: 640px) {
  .small {
    height: 300px;
  }

  .medium {
    height: 350px;
  }

  .large {
    height: 400px;
  }
}

/* Störst bildstorlekar för större skärmar */
@media (min-width: 1024px) {
  .small {
    height: 375px;
  }

  .medium {
    height: 450px;
  }

  .large {
    height: 500px;
  }
}
</style>
