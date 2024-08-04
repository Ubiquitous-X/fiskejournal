<template>
  <div class="flex flex-wrap w-full h-full bg-neutral">
    <WeatherWidget />
    <StatsWidget />
    <LatestCatchWidget />
  </div>
</template>

<script>
import WeatherWidget from './WeatherWidget.vue';
import StatsWidget from './StatsWidget.vue';
import LatestCatchWidget from './LatestCatchWidget.vue';

export default {
  name: "InfoPanel",
  components: {
    WeatherWidget,
    StatsWidget,
    LatestCatchWidget
}
};
</script>