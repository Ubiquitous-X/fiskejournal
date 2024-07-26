import { createStore } from 'vuex';
import apiClient from './api';

export default createStore({
  state: {
    isLoggedIn: false,
    csrfToken: null,
  },
  mutations: {
    setLoggedIn(state, status) {
      state.isLoggedIn = status;
    },
    setCSRFToken(state, token) {
      state.csrfToken = token;
      localStorage.setItem('csrfToken', token);
    },
  },
  actions: {
    async login({ commit }) {
      commit('setLoggedIn', true);
    },
    async logout({ commit }) {
      commit('setLoggedIn', false);
      localStorage.removeItem('csrfToken');
    },
    async checkLoginStatus({ commit }) {
      try {
        const response = await apiClient.get('/auth/status');
        commit('setLoggedIn', response.data.is_logged_in);
      } catch (error) {
        commit('setLoggedIn', false);
      }
    },
  },
  getters: {
    isLoggedIn: state => state.isLoggedIn,
  },
});

