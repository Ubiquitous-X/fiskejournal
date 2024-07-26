<template>
  <div class="flex flex-col h-full z-0">
    <div class="flex-1 relative">
      <Spinner v-if="loading" class="absolute inset-0 z-10 flex items-center justify-center" />
      <div id="map" class="w-full h-full z-0"></div>
    </div>
    <ImageModal :isVisible="isModalVisible" :imageUrl="selectedImageUrl" :fish="selectedFish" @close="() => { isModalVisible = false }" />
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import 'leaflet.markercluster';
import apiClient from '../api';
import Spinner from '@/components/Spinner.vue';
import ImageModal from '@/components/ImageModal.vue';

export default {
  name: 'MapView',
  components: {
    Spinner,
    ImageModal
  },
  setup() {
    const loading = ref(true);
    const map = ref(null);
    const markers = ref(null);
    const isSmallScreen = window.innerWidth < 768;
    const isModalVisible = ref(false);
    const selectedImageUrl = ref('');
    const selectedFish = ref(null);
    const router = useRouter();
    const route = useRoute();

    const openModal = (event) => {
      const url = event.target.getAttribute('data-full-image-url');
      const fishData = JSON.parse(event.target.getAttribute('data-fish'));
      selectedImageUrl.value = url;
      selectedFish.value = fishData;
      isModalVisible.value = true;
    };

    window.openModal = openModal;

    const getColorBySpecies = (species) => {
      switch (species) {
        case 'Gös':
          return '#0077be'; // Blå
        case 'Abborre':
          return '#00be77'; // Grön
        case 'Gädda':
          return '#be0000'; // Röd
        default:
          return '#000000'; // Svart som standard
      }
    };

    const createCustomIcon = (species) => {
      const color = getColorBySpecies(species);
      return L.divIcon({
        html: `<i class="fa fa-fish fa-xl" style="color: ${color}; text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;"></i>`,
        className: 'custom-div-icon',
      });
    };

    const formatDate = (timestamp) => {
      const date = new Date(timestamp);
      const day = String(date.getDate());
      const month = String(date.getMonth() + 1);
      const year = String(date.getFullYear()).slice(-2);
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${day}/${month}-${year} kl.${hours}:${minutes}`;
    };

    const fetchFishData = async () => {
      try {
        const response = await apiClient.get('/fish/all');
        const fishData = response.data;

        const bounds = L.latLngBounds();

        fishData.forEach(fish => {
          const marker = L.marker([fish.latitude, fish.longitude], { icon: createCustomIcon(fish.species.name) })
            .bindPopup(`
              <b>${fish.species.name}</b><br>
              <i class="location">${fish.location}</i>
              <div style="text-align: center;">
                <img src="${fish.thumbnail_image_url}" alt="${fish.species} image" class="popup-image" data-full-image-url="${fish.medium_image_url}" data-fish='${JSON.stringify(fish)}' onclick="openModal(event)" style="display: block; margin: 10px auto;">
                <i>${formatDate(fish.timestamp)}</i><br>
                <button class="btn btn-ghost btn-xs mt-4" onclick="openSingleFishView('${fish.slug}')">Visa detaljer</button>
              </div>
            `);

          markers.value.addLayer(marker);
          bounds.extend(marker.getLatLng());
        });

        if (fishData.length > 0) {
          // Kontrollera om det finns specifika lat/lng-parametrar
          if (!route.query.lat || !route.query.lng) {
            if (isSmallScreen) {
              map.value.fitBounds(bounds, { padding: [10, 10] });
            } else {
              map.value.fitBounds(bounds);
            }
          }
        }
      } catch (error) {
        console.error("Error fetching fish data: ", error);
      } finally {
        loading.value = false;
      }
    };

    const addLegend = () => {
      const legend = L.control({ position: 'topright' });

      legend.onAdd = () => {
        const div = L.DomUtil.create('div', 'info legend');
        div.classList.add('p-2', 'shadow-md', 'rounded-md', 'bg-white', 'dark:bg-gray-800');
        const species = ['Gös', 'Abborre', 'Gädda', 'Annan'];
        const labels = [];

        species.forEach(species => {
          const color = getColorBySpecies(species);
          labels.push(
            `<i class="fa fa-fish" style="color: ${color};"></i> ${species}`
          );
        });

        div.innerHTML = labels.join('<br>');
        return div;
      };

      legend.addTo(map.value);
    };

    window.openSingleFishView = (slug) => {
      const mapState = {
        center: map.value.getCenter(),
        zoom: map.value.getZoom()
      };
      sessionStorage.setItem('mapState', JSON.stringify(mapState));

      sessionStorage.setItem('previousRoute', router.currentRoute.value.fullPath);
      router.replace({ name: 'SingleFishView', params: { slug } });
    };

    const updateUrl = () => {
      const center = map.value.getCenter();
      const zoom = map.value.getZoom();
      const { lat, lng } = center;

      const params = new URLSearchParams();
      params.set('lat', lat.toFixed(5));
      params.set('lng', lng.toFixed(5));
      params.set('zoom', zoom);

      router.replace({ query: Object.fromEntries(params.entries()) });
    };

    const setCanonicalUrl = () => {
      const existingCanonicalLink = document.querySelector("link[rel='canonical']");
      if (existingCanonicalLink) {
        existingCanonicalLink.remove();
      }
      const link = document.createElement('link');
      link.setAttribute('rel', 'canonical');
      link.setAttribute('href', 'https://olundsfiske.se/karta');
      document.head.appendChild(link);
    };

    onMounted(() => {
      setCanonicalUrl();

      const lat = parseFloat(route.query.lat);
      const lng = parseFloat(route.query.lng);
      const zoom = parseInt(route.query.zoom, 10);

      const initialCenter = (lat && lng) ? [lat, lng] : [59.3801, 17.0358];
      const initialZoom = zoom || 13;

      map.value = L.map('map').setView(initialCenter, initialZoom);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map.value);

      // Initiera marker cluster group med custom options
      markers.value = L.markerClusterGroup({
        maxClusterRadius: 10,
      });
      map.value.addLayer(markers.value);

      // Lyssna på moveend och zoomend händelser för att uppdatera URL:en
      map.value.on('moveend', updateUrl);
      map.value.on('zoomend', updateUrl);

      // Återställ kartans position och zoomnivå om den finns i sessionStorage
      const savedMapState = sessionStorage.getItem('mapState');
      if (savedMapState && !lat && !lng) {
        const mapState = JSON.parse(savedMapState);
        map.value.setView(mapState.center, mapState.zoom);
      }

      fetchFishData();
      addLegend();
    });

    onBeforeUnmount(() => {
      const params = new URLSearchParams(window.location.search);
      params.delete('lat');
      params.delete('lng');
      params.delete('zoom');
      const newUrl = window.location.pathname;
      window.history.replaceState({}, '', newUrl);
    });

    return {
      loading,
      isModalVisible,
      selectedImageUrl,
      selectedFish
    };
  }
};
</script>

<style>
#map {
  width: 100%;
  height: 100%;
}

.custom-div-icon {
  background: none;
  border: none;
}

.info.legend {
  line-height: 18px;
  font-size: 14px;
  background-color: rgba(255, 255, 255, 0.6);
}

.legend i {
  width: 18px;
  height: 18px;
  float: left;
  margin-right: 8px;
  opacity: 1;  
}

.marker-cluster div {
  color: black !important;
}

.marker-cluster-small {
  background-color: rgba(31, 100, 24, 0.7) !important;
}

.marker-cluster-medium {
  background-color: rgba(31, 100, 24, 0.7) !important;
}

.marker-cluster-large {
  background-color: rgba(31, 100, 24, 0.7) !important;
}

.popup-image {
  display: block;
  width: 120px !important;
  height: auto !important;
  max-width: none !important;
  max-height: none !important;
  margin-bottom: 0px !important;
  border: 1px solid rgba(0, 0, 0, 0.4);
  border-radius: 4px;
}

.leaflet-popup-content-wrapper {
  padding: 12px !important;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  width: auto !important;
  max-width: none !important;
}

.leaflet-popup-content {
  margin: 0px !important;
  font-family: Arial, sans-serif;
  line-height: 1.5;
}

.leaflet-popup-content .location {
  display: block;
  font-size: 12px;
  color: #555;
  margin-bottom: 0px !important;
}

.leaflet-popup-tip-container {
  display: none;
}
</style>
