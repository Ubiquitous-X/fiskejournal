<template>
  <div class="tooltip tooltip-top" :data-tip="weatherDescription">
    <img :src="weatherIconUrl" :alt="weatherDescription" class="w-12 h-12" />
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'WeatherIcon',
  props: {
    weatherDescription: {
      type: String,
      required: true
    },
    weatherIconUrl: {
      type: String,
      required: true
    }
  }
});
</script>

<style scoped>
.tooltip {
  display: inline-block;
  position: relative;
}
.tooltip .tooltip-left {
  position: absolute;
  left: 100%;
  margin-left: 10px;
  z-index: 10;
  background-color: #333;
  color: #fff;
  padding: 5px 10px;
  border-radius: 3px;
  white-space: nowrap;
  display: none;
}
.tooltip:hover .tooltip-left {
  display: block;
}
</style>
