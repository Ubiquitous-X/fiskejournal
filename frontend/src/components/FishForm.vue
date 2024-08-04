<template>
  <form @submit.prevent="updateFish" class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="form-control col-span-1">
      <label for="species" class="label">
        <span class="label-text">Art:</span>
      </label>
      <select v-model="localEditingSpecies" id="species" class="select select-bordered w-full">
        <option v-for="species in fishSpecies" :key="species.id" :value="species.id">{{ species.name }}</option>
      </select>
    </div>
    <div class="form-control col-span-1">
      <label for="bait" class="label">
        <span class="label-text">Bete:</span>
      </label>
      <select v-model="localEditingBait" id="bait" class="select select-bordered w-full">
        <option v-for="bait in fishBaits" :key="bait.id" :value="bait.id">{{ bait.type }}</option>
      </select>
    </div>
    <div class="form-control col-span-1">
      <label for="weight" class="label">
        <span class="label-text">Vikt (kg):</span>
      </label>
      <input v-model.number="localEditingFish.weight" id="weight" type="number" step="0.01" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="length" class="label">
        <span class="label-text">Längd (cm):</span>
      </label>
      <input v-model.number="localEditingFish.length" id="length" type="number" step="0.1" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="location" class="label">
        <span class="label-text">Fångstplats:</span>
      </label>
      <input v-model="localEditingFish.location" id="location" type="text" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="weather" class="label">
        <span class="label-text">Väder:</span>
      </label>
      <input v-model="localEditingFish.weather" id="weather" type="text" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="latitude" class="label">
        <span class="label-text">Latitud:</span>
      </label>
      <input v-model.number="localEditingFish.latitude" id="latitude" type="number" step="0.0001" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="longitude" class="label">
        <span class="label-text">Longitud:</span>
      </label>
      <input v-model.number="localEditingFish.longitude" id="longitude" type="number" step="0.0001" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="air_temperature" class="label">
        <span class="label-text">Lufttemperatur (°C):</span>
      </label>
      <input v-model.number="localEditingFish.air_temperature" id="air_temperature" type="number" step="0.1" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="air_pressure" class="label">
        <span class="label-text">Lufttryck (hPa):</span>
      </label>
      <input v-model.number="localEditingFish.air_pressure" id="air_pressure" type="number" step="1" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="wind_speed" class="label">
        <span class="label-text">Vindhastighet (m/s):</span>
      </label>
      <input v-model.number="localEditingFish.wind_speed" id="wind_speed" type="number" step="0.1" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="wind_dir" class="label">
        <span class="label-text">Vindriktning:</span>
      </label>
      <input v-model="localEditingFish.wind_dir" id="wind_dir" type="text" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="air_humidity" class="label">
        <span class="label-text">Luftfuktighet (%):</span>
      </label>
      <input v-model.number="localEditingFish.air_humidity" id="air_humidity" type="number" step="1" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="uv_index" class="label">
        <span class="label-text">UV-index:</span>
      </label>
      <input v-model.number="localEditingFish.uv_index" id="uv_index" type="number" step="0.1" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="moon_phase" class="label">
        <span class="label-text">Månfas:</span>
      </label>
      <input v-model="localEditingFish.moon_phase" id="moon_phase" type="text" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="moon_illumination" class="label">
        <span class="label-text">Månens belysning (%):</span>
      </label>
      <input v-model.number="localEditingFish.moon_illumination" id="moon_illumination" type="number" step="0.1" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="medium_image_url" class="label">
        <span class="label-text">Medium foto URL:</span>
      </label>
      <input v-model="localEditingFish.medium_image_url" id="medium_image_url" type="text" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="thumbnail_image_url" class="label">
        <span class="label-text">Thumbnail foto URL:</span>
      </label>
      <input v-model="localEditingFish.thumbnail_image_url" id="thumbnail_image_url" type="text" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1">
      <label for="weather_icon_url" class="label">
        <span class="label-text">Väderikon URL:</span>
      </label>
      <input v-model="localEditingFish.weather_icon_url" id="weather_icon_url" type="text" class="input input-bordered w-full" />
    </div>
    <div class="form-control col-span-1 md:col-span-2">
      <label for="description" class="label">
        <span class="label-text">Beskrivning:</span>
      </label>
      <textarea v-model="localEditingFish.description" id="description" class="textarea textarea-bordered w-full"></textarea>
    </div>
    <div class="col-span-1 md:col-span-2 flex justify-between">
      <button type="submit" class="btn btn-primary w-1/2 mr-2">Uppdatera</button>
      <button @click="cancelEdit" class="btn btn-secondary w-1/2">Avbryt</button>
    </div>
  </form>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  name: 'FishForm',
  props: {
    fish: Object,
    fishSpecies: Array,
    fishBaits: Array,
    onUpdate: Function,
    onCancel: Function,
  },
  setup(props) {
    const localEditingFish = ref({ ...props.fish });
    const localEditingSpecies = ref(props.fish.species ? props.fish.species.id : null);
    const localEditingBait = ref(props.fish.bait ? props.fish.bait.id : null);

    watch(
      () => props.fish,
      (newFish) => {
        localEditingFish.value = { ...newFish };
        localEditingSpecies.value = newFish.species ? newFish.species.id : null;
        localEditingBait.value = newFish.bait ? newFish.bait.id : null;
      }
    );

    const updateFish = () => {
      const payload = {
        ...localEditingFish.value,
        species: localEditingSpecies.value,
        bait: localEditingBait.value,
      };

      Object.keys(payload).forEach((key) => {
        if (payload[key] === '') {
          payload[key] = null;
        }
      });

      props.onUpdate(payload);
    };

    const cancelEdit = () => {
      props.onCancel();
    };

    return {
      localEditingFish,
      localEditingSpecies,
      localEditingBait,
      updateFish,
      cancelEdit,
    };
  },
};
</script>
