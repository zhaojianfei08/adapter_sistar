// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Run from '../views/Run.vue'; // 引入首页组件
import Config from '../views/Config.vue'; // 引入配置页面
import Init from '../views/Init.vue'; 
import Alarm from '../views/Alarm.vue';
import LogViewer from '../views/LogViewer.vue';

const routes = [
  {
    path: '/',
    name: 'Run',
    component: Run,
  },
  {
    path: '/config',
    name: 'Config',
    component: Config,
  },
  {
    path: '/init',
    name: 'Init',
    component: Init,
  },
  {
    path: '/alarm',
    name: 'Alarm',
    component: Alarm,
  },
  {
    path: '/log',
    name: 'LogViewer',
    component: LogViewer,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
