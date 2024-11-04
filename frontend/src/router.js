import { createRouter, createWebHistory } from 'vue-router';
import ShopPage from './components/ShopPage.vue';
import ProductDetail from './components/ProductDetail.vue';

const routes = [
  {
    path: '/',
    redirect: '/shop'
  },
  {
    path: '/shop',
    name: 'ShopPage',
    component: ShopPage
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: ProductDetail
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;