<script setup>
  import ProductCard from "./ProductCard.vue"

  defineProps({ products: Array })
</script>

<template>
  <div class="flex flex-wrap justify-stretch justify-items-stretch m-2 gap-2">
    <ProductCard v-for="product in products" :product="product" />
  </div>
</template>
