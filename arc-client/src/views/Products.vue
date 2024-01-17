<script setup>
  import { watchEffect, ref, provide, computed, watch, reactive } from "vue"
  import { useRoute } from "vue-router"
  import {
    fetchRootCategories,
    fetchCategory,
    fetchProducts,
    fetchChildCategories,
  } from "../business/arc"

  import Title from "../components/ui/Title.vue"
  import Subtitle from "../components/ui/Subtitle.vue"
  import ProductFilter from "../components/ProductFilter.vue"
  import ProductList from "../components/ProductList.vue"
  import CategoryBreadcrumb from "../components/categorybreadcrumb.vue"

  const route = useRoute()

  const category = ref()
  const subCategories = ref([])
  const products = ref([])
  const filters = reactive({})

  watchEffect(async () => {
    if (
      typeof route.params.categories === "undefined" ||
      !route.params.categories.length
    ) {
      category.value = null
    } else {
      const slug = route.params.categories.at(-1)
      category.value = await fetchCategory(slug)
    }
  })

  watchEffect(async () => {
    if (typeof category.value === "undefined") return

    if (category.value === null) {
      subCategories.value = await fetchRootCategories()
    } else {
      subCategories.value = await fetchChildCategories(category.value.id)
      products.value = await fetchProducts(category.value.id)
    }
  })

  const filteredProducts = computed(() =>
    products.value.filter(product =>
      Object.entries(filters).every(([_, filter]) => filter(product))
    )
  )

  provide("category", category)
  provide("products", products)
</script>

<template>
  <Title>
    {{ category ? category.name : "Catalogue" }}
  </Title>

  <CategoryBreadcrumb :categories="category ? category.parents : []" />

  <div v-if="subCategories && subCategories.length">
    <Subtitle>Sous-catégories</Subtitle>

    <router-link
      v-for="categ of subCategories"
      :to="{ name: 'products', params: { categories: [categ.slug] } }"
    >
      <div>{{ categ.name }}</div>
    </router-link>
  </div>

  <div v-if="products && products.length">
    <Subtitle>Produits</Subtitle>

    <div class="flex flex-wrap sm:flex-nowrap">
      <ProductFilter v-model="filters" class="w-full sm:w-auto sm:min-w-72" />

      <ProductList :products="filteredProducts" />
    </div>
  </div>
</template>
