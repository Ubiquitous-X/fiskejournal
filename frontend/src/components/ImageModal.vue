<template>
  <div v-if="isVisible" class="modal-overlay" @click="closeModal">
    <div class="modal-content bg-base-100 dark:bg-base-300" @click.stop>
      <div class="relative">
        <!-- Stängningsknapp -->
        <button class="absolute top-2 right-2 btn btn-circle btn-sm" @click="closeModal">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <img :src="imageUrl" alt="Större bild" class="w-full h-auto rounded-md">
        <div class="absolute bottom-0 left-0 right-0 bg-opacity-75 bg-neutral text-neutral-content p-2 text-center">
          <p class="text-sm md:text-base">
            {{ fish.species.name }} fångad
            <span v-if="fish.bait">
              på en {{ fish.bait.type.charAt(0).toLowerCase() + fish.bait.type.slice(1) }}
            </span>
            i {{ fish.location }}
          </p>
          <p class="block sm:inline text-sm">{{ formatDate(fish.timestamp) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, toRefs } from 'vue';

export default defineComponent({
  props: {
    isVisible: Boolean,
    imageUrl: String,
    fish: Object
  },
  setup(props, { emit }) {
    const { isVisible, imageUrl, fish } = toRefs(props);

    const closeModal = () => {
      emit('close');
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

    return {
      isVisible,
      imageUrl,
      fish,
      closeModal,
      formatDate
    };
  }
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  padding: 5px;
  border-radius: 8px;
}
</style>
