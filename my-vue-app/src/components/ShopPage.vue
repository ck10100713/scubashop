<template>
  <div class="container-fluid">
    <div class="row">
      <!-- 商品类别筛选栏 -->
      <div class="col-lg-3 col-md-4">
        <div class="list-group">
          <a href="#" @click.prevent="fetchProducts()" class="list-group-item list-group-item-action">全部商品</a>
          <!-- 商品类别筛选 -->
          <a v-for="category in categories" :key="category.id" href="#" @click.prevent="fetchProducts({ category: category.id })" 
             class="list-group-item list-group-item-action" :class="{ active: selectedCategory === category.id }">
            {{ category.name }}
          </a>
          <hr>
          <!-- 商品品牌筛选 -->
          <div class="list-group">
            <a href="#" @click.prevent="fetchProducts({ brand: null })" class="list-group-item list-group-item-action">全部品牌</a>
            <a v-for="brand in brands" :key="brand.id" href="#" @click.prevent="fetchProducts({ brand: brand.id })" 
               class="list-group-item list-group-item-action" :class="{ active: selectedBrand === brand.id }">
              {{ brand.name }}
            </a>
          </div>
          <hr>
          <form @submit.prevent="applyFilters">
            <div v-for="field in formFields" :key="field.name" class="form-group">
              <label :for="field.name">{{ field.label }}</label>
              <input v-if="field.type === 'text'" :type="field.type" :name="field.name" v-model="filters[field.name]" class="form-control">
              <select v-if="field.type === 'select'" :name="field.name" v-model="filters[field.name]" class="form-control">
                <option v-for="option in field.options" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary">篩選</button>
          </form>
        </div>
      </div>
      <!-- 商品列表 -->
      <div class="col-lg-9 col-md-8">
        <div v-if="products && products.length" class="row">
          <div v-for="product in products" :key="product.id" class="col-lg-4 col-md-6 mb-4">
            <div class="card h-100">
              <a :href="`/product/${product.id}`">
                <img v-if="product.image" :src="product.image" :alt="product.name" class="img-fluid">
                <img v-else src="/static/img/no_image.png" alt="no image" class="img-fluid">
              </a>
              <div class="card-body">
                <h4 class="card-title">
                  <a :href="`/product/${product.id}`">{{ product.name }}</a>
                </h4>
                <h5>NT${{ product.price }}</h5>
                <p class="card-text">{{ product.description }}</p>
              </div>
              <div class="card-footer">
                <a :href="`/cart/add_to_cart/${product.id}`" class="btn btn-primary">加入購物車</a>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="col-lg-12">
          <p>沒有符合條件的商品。</p>
        </div>
        <!-- 分頁導航 -->
        <nav v-if="pagination && pagination.page_range" aria-label="Page navigation">
          <ul class="pagination">
            <li v-if="pagination.has_previous" class="page-item">
              <a class="page-link" href="#" @click.prevent="fetchProducts({ page: 1 })" aria-label="First">
                <span aria-hidden="true">&laquo;&laquo;</span>
              </a>
            </li>
            <li v-if="pagination.has_previous" class="page-item">
              <a class="page-link" href="#" @click.prevent="fetchProducts({ page: pagination.previous_page_number })" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li v-for="num in pagination.page_range" :key="num" class="page-item" :class="{ active: pagination.current_page === num }">
              <a class="page-link" href="#" @click.prevent="fetchProducts({ page: num })">{{ num }}</a>
            </li>
            <li v-if="pagination.has_next" class="page-item">
              <a class="page-link" href="#" @click.prevent="fetchProducts({ page: pagination.next_page_number })" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
            <li v-if="pagination.has_next" class="page-item">
              <a class="page-link" href="#" @click.prevent="fetchProducts({ page: pagination.num_pages })" aria-label="Last">
                <span aria-hidden="true">&raquo;&raquo;</span>
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ShopPage',
  data() {
    return {
      categories: [],
      brands: [],
      products: [],
      pagination: {},
      filters: {
        category: null,
        brand: null,
        sort_by: null,
        page: 1
      },
      formFields: [
        { name: 'sort_by', label: '排序', type: 'select', options: [
          { value: '', label: '默認' },
          { value: 'price', label: '價格' },
          { value: 'name', label: '名稱' }
        ]}
      ],
      selectedCategory: null,
      selectedBrand: null
    };
  },
  created() {
    this.fetchCategories();
    this.fetchBrands();
    this.fetchProducts();
  },
  methods: {
    fetchCategories() {
      this.$axios.get('/shop/categories/')
        .then(response => {
          this.categories = response.data;
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
        });
    },
    fetchBrands() {
      this.$axios.get('/shop/brands/')
        .then(response => {
          this.brands = response.data;
        })
        .catch(error => {
          console.error('Error fetching brands:', error);
        });
    },
    fetchProducts(params = {}) {
      const queryParams = { ...this.filters, ...params };
      console.log('Fetching products with params:', queryParams); // 調試日誌
      this.$axios.get('/shop/products/', { params: queryParams })
        .then(response => {
          console.log('Products fetched:', response.data); // 調試日誌
          this.products = response.data.results || response.data; // 根據 API 返回的數據結構設置 products
          this.pagination = response.data.pagination || {}; // 根據 API 返回的數據結構設置 pagination
          this.selectedCategory = queryParams.category;
          this.selectedBrand = queryParams.brand;
        })
        .catch(error => {
          console.error('Error fetching products:', error);
        });
    },
    applyFilters() {
      this.fetchProducts();
    }
  }
};
</script>

<style scoped>
/* 添加你的樣式 */
</style>