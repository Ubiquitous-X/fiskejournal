<template>
  <div class="flex flex-wrap w-full h-full bg-neutral">
    <WeatherWidget />
    <StatsWidget />
  </div>
</template>

<script>
import WeatherWidget from './WeatherWidget.vue';
import StatsWidget from './StatsWidget.vue';

export default {
  name: "InfoPanel",
  components: {
    WeatherWidget,
    StatsWidget
  }
};
</script>