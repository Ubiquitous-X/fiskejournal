<template>
  <div class="flex items-center">
    <i @click="fileInput.click()" class="fas fa-cloud-upload-alt text-xl sm:text-2xl cursor-pointer text-primary mr-3"></i>
    <input type="file" ref="fileInput" class="hidden" @change="onFileChange">
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import apiClient from '../api';
import { useToast } from 'vue-toastification';

export default {
  setup() {
    const fileInput = ref(null);
    const toast = useToast();
    let socket = null;
    let retryCount = 0; // Håller reda på antalet återanslutningsförsök
    const maxRetries = 3; // Maximalt antal återanslutningsförsök
    let socketOpened = false; // Indikator för om socket är öppen

    const handleNotification = (data) => {
      const message = data.message || data.detail || 'Okänt fel';
      const notificationType = data.notification_type || 'info';

      switch (notificationType) {
        case 'success':
          toast.success(message);
          break;
        case 'error':
          toast.error(message);
          break;
        case 'info':
          toast.info(message);
          break;
        case 'warning':
          toast.warning(message);
          break;
        default:
          toast(message);
      }
    };

    const onFileChange = (event) => {
      const file = event.target.files[0];
      if (file) {
        uploadFile(file);
      }
    };

    const uploadFile = async (file) => {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await apiClient.post('/file/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          skipInterceptor: true  // För att förhindra dubbla felmeddelanden i Toast
        });
        handleNotification(response.data);
      } catch (error) {
        console.error('Fel vid uppladdningen', error);

        if (error.response) {
          console.log('Error response:', error.response.data);
          handleNotification(error.response.data);
        } else {
          toast.error('Fel vid uppladdningen (från Vue)');
        }
      }
    };

    const connectWebSocket = () => {
      if (socket) {
        socket.close(); // Stäng befintlig socket innan vi öppnar en ny
      }

      socket = new WebSocket(import.meta.env.VITE_WS_BASE_URL);

      socket.onopen = () => {
        console.log('WebSocket connected');
        retryCount = 0; // Nollställ återanslutningsräknaren vid lyckad anslutning
        socketOpened = true; // Indikerar att socket nu är öppen
      };

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleNotification(data);
      };

      socket.onerror = (error) => {
        console.error('WebSocket error:', error);

        // Försök återansluta upp till maxRetries gånger
        if (retryCount < maxRetries) {
          retryCount++;
          console.log(`Försöker återansluta WebSocket (${retryCount}/${maxRetries})...`);
          setTimeout(connectWebSocket, 1000); // Försök igen efter 1 sekund
        } else {
          toast.error('Kunde inte ansluta till WebSocket efter flera försök');
        }
      };

      socket.onclose = () => {
        console.log('WebSocket closed');
        socketOpened = false; // Indikerar att socket nu är stängd
      };
    };

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        // Återanslut WebSocket om det inte redan är anslutet
        if (!socketOpened) {
          connectWebSocket();
        }
      } else {
        // Stäng WebSocket om sidan blir osynlig
        if (socket && socketOpened) {
          socket.close();
        }
      }
    };

    onMounted(() => {
      connectWebSocket(); // Starta WebSocket-anslutning när komponenten monteras

      // Lägg till event listener för att lyssna på synlighetsändringar
      document.addEventListener('visibilitychange', handleVisibilityChange);
    });

    onUnmounted(() => {
      // Stäng WebSocket när komponenten avmonteras, om den är öppen
      if (socket && socketOpened) {
        socket.close();
      }
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    });

    return {
      fileInput,
      onFileChange,
    };
  },
};
</script>
