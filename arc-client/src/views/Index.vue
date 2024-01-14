<script setup>
  import { ref } from "vue"

  import { fetchLastProducts } from "../business/arc"
  import ProductList from "../components/ProductList.vue"
  import Subtitle from "../components/ui/Subtitle.vue"
  import Title from "../components/ui/Title.vue"

  const products = ref()

  products.value = await fetchLastProducts()
</script>

<template>
  <div class="max-w-prose">
    <Title>Ici, c'est Arc.</Title>

    <Subtitle>Super. Et alors ?</Subtitle>

    <p class="mx-2 my-4">
      Arc est une base de données destinée à organiser le réemploi de matériels
      électriques.
    </p>

    <Subtitle>Derniers produits</Subtitle>
  </div>

  <ProductList :products="products" />
</template>
