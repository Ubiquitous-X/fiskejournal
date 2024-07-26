<template>
  <div :class="['flex justify-center items-center h-full', { 'mt-14': marginTop }]">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
</template>

<script>
import { defineComponent, toRefs } from 'vue';

export default defineComponent({
  name: 'Spinner',
  props: {
    marginTop: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const { marginTop } = toRefs(props);
    return {
      marginTop
    };
  }
});
</script>
