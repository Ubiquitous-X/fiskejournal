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
      socket = new WebSocket(import.meta.env.VITE_WS_BASE_URL);

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleNotification(data);
      };

      socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        toast.error('WebSocket error');
      };
    };

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        if (socket && socket.readyState !== WebSocket.OPEN) {
          console.log('Reconnecting WebSocket...');
          connectWebSocket();
        }
      }
    };

    onMounted(() => {
      connectWebSocket();

      document.addEventListener('visibilitychange', handleVisibilityChange);
    });

    onUnmounted(() => {
      if (socket) {
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
