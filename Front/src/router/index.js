import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import PatientChatPage from '@/components/PatientChatPage.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/patient/:id', component: PatientChatPage, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;