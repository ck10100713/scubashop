<template>
    <div class="container mt-5">
      <div class="row">
        <!-- 商品圖片 -->
        <div class="col-md-6">
          <div v-if="product && product.images && product.images.length">
            <img v-for="image in product.images" :key="image.id" :src="image.image.url" :alt="product.name + ' image'" class="img-fluid" style="max-width: 100%; height: auto;">
          </div>
          <div v-else>
            <img src="/static/img/no_image.png" alt="no image" class="img-fluid" style="max-width: 100%; height: auto;">
          </div>
        </div>
        <!-- 商品資訊 -->
        <div class="col-md-6">
          <h2 v-if="product">{{ product.name }}</h2>
          <h4 v-if="product">價格: NT${{ product.price }}</h4>
          <p v-if="product">規格: {{ product.size }} / {{ product.color }}</p>
          <p v-if="product">{{ product.description }}</p>
          <form v-if="product" @submit.prevent="addToCart">
            <div class="form-group">
              <label for="quantity">數量:</label>
              <select v-model="quantity" id="quantity" class="form-control" required>
                <option v-for="num in 9" :key="num" :value="num">{{ num }}</option>
              </select>
            </div>
            <a href="javascript:history.back()" class="btn btn-success">返回</a>
            <button type="submit" class="btn btn-primary">加入購物車</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        product: null,
        quantity: 1
      };
    },
    created() {
      const productId = this.$route.params.id;
      // 使用 axios 調用 Django 的 API
      this.$axios.get(`shop/product-detail/${productId}/`)
        .then(response => {
          this.product = response.data;
        })
        .catch(error => {
          console.error('Error fetching product details:', error);
        });
    },
    methods: {
      addToCart() {
        // 處理加入購物車的邏輯
        this.$axios.post(`/cart/add_to_cart/${this.product.id}/`, {
          quantity: this.quantity
        })
        .then(response => {
          // 處理成功邏輯
          console.log('Added to cart:', response.data);
        })
        .catch(error => {
          // 處理錯誤邏輯
          console.error('Error adding to cart:', error);
        });
      }
    }
  };
  </script>
  
  <style scoped>
  /* 添加你的樣式 */
  </style>