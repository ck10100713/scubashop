import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import router from './router';

// 設置 axios 的全局配置，例如基礎 URL
axios.defaults.baseURL = 'http://localhost:8000/api/';

const app = createApp(App);

// 將 axios 添加到 Vue 的全局屬性中，這樣你可以在組件中通過 this.$axios 訪問它
app.config.globalProperties.$axios = axios;

app.use(router);

app.mount('#app');