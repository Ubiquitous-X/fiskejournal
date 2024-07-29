<template>
  <div class="p-4">
    <div class="max-w-6xl mx-auto mt-2 rounded-xl shadow-2xl p-6">
      <!-- Tabs navigation -->
      <p>Version 0.2.1b</p>
      <div class="tabs tabs-boxed font-bold">
        <a @click="selectedTab = 'fish'" :class="{'tab-active': selectedTab === 'fish'}" class="tab tab-bordered">Fiskar</a>
        <a @click="selectedTab = 'bait'" :class="{'tab-active': selectedTab === 'bait'}" class="tab tab-bordered">Beten</a>
        <a @click="selectedTab = 'species'" :class="{'tab-active': selectedTab === 'species'}" class="tab tab-bordered">Fiskarter</a>
      </div>

      <!-- Tab innehåll -->
      <div class="mt-4">
        <div v-if="selectedTab === 'bait'" class="w-full">
          <BaitManagement />
        </div>
        <div v-if="selectedTab === 'species'" class="w-full">
          <SpeciesManagement />
        </div>
        <div v-if="selectedTab === 'fish'" class="w-full">
          <FishManagement />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, defineComponent } from 'vue';
import BaitManagement from '@/components/BaitManagement.vue';
import SpeciesManagement from '@/components/SpeciesManagement.vue';
import FishManagement from '@/components/FishManagement.vue';

export default defineComponent({
  name: 'ManagementView',
  components: {
    BaitManagement,
    SpeciesManagement,
    FishManagement,
  },
  setup() {
    const selectedTab = ref('fish'); // Starta på tabben 'Fiskar'

    return {
      selectedTab,
    };
  },
});
</script>
