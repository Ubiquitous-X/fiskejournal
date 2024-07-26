<template>
  <div class="tooltip tooltip-top" :data-tip="moonPhaseName">
    <img :src="moonPhaseImage" :alt="moonPhaseName" class="w-5 h-5" />
  </div>
</template>

<script>
import { computed } from 'vue';
import newMoon from '@/assets/moon/new_moon.png';
import waxingCrescent from '@/assets/moon/waxing_crescent.png';
import firstQuarter from '@/assets/moon/first_quarter.png';
import waxingGibbous from '@/assets/moon/waxing_gibbous.png';
import fullMoon from '@/assets/moon/full_moon.png';
import waningGibbous from '@/assets/moon/waning_gibbous.png';
import lastQuarter from '@/assets/moon/last_quarter.png';
import waningCrescent from '@/assets/moon/waning_crescent.png';

export default {
  name: 'MoonPhase',
  props: {
    phase: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const moonPhaseImage = computed(() => {
      switch (props.phase) {
        case 'Nymåne': return newMoon;
        case 'Tilltagande skära': return waxingCrescent;
        case 'Första kvarteret': return firstQuarter;
        case 'Tilltagande halvmåne': return waxingGibbous;
        case 'Fullmåne': return fullMoon;
        case 'Avtagande halvmåne': return waningGibbous;
        case 'Sista kvarteret': return lastQuarter;
        case 'Avtagande skära': return waningCrescent;
        default: return null;
      }
    });

    const moonPhaseName = computed(() => props.phase);

    return {
      moonPhaseImage,
      moonPhaseName
    };
  }
};
</script>

<style scoped>
.moon-phase {
  display: flex;
  align-items: center;
}
.moon-phase img {
  margin-right: 8px;
}
</style>
