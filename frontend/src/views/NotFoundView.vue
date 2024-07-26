<template>
  <div class="flex items-center justify-center h-screen bg-base-200">
    <div class="text-center">
      <h1 class="text-6xl font-bold text-primary mb-4">404 - Bottennapp</h1>
      <p class="text-xl text-secondary mb-8">Sidan kunde inte hittas.</p>
      <router-link to="/" class="btn btn-primary">Till startsidan</router-link>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'NotFoundView',
  components: {}
});
</script>
