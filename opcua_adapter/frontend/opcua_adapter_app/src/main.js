import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 路由
import { createPinia } from 'pinia'; // 状态管理
import piniaPersistedState from 'pinia-plugin-persistedstate';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'; // Element Plus 样式

// 创建 Vue 应用实例
const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPersistedState);  // 启用持久化插件

app.use(router);
app.use(pinia);
app.use(ElementPlus);

app.mount('#app');
