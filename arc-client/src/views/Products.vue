<script setup>
  import { watchEffect, ref, reactive, computed, watch } from "vue"
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
  const lines = ref([])

  const selectedSpecs = reactive({})
  const selectedLines = reactive([])

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
    products.value
      .filter(product =>
        selectedLines.length
          ? selectedLines.map(line => line.id).includes(product.line_id)
          : true
      )
      .filter(product =>
        Object.entries(selectedSpecs).every(([property, value]) => {
          if (value === null) {
            return true
          } else if (value instanceof Array && value.length) {
            return value.includes(product.specs[property])
          } else {
            return product.specs[property] === value
          }
        })
      )
  )

  watch(products, async products => {
    const uris = [...new Set(products.map(product => product.line))]

    lines.value = await Promise.all(
      uris.map(async uri => fetch(uri).then(r => r.json()))
    )
  })
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

    <!-- <pre>{{ products }}</pre> -->

    <ProductFilter
      :category="category"
      :lines="lines"
      v-model:selectedSpecs="selectedSpecs"
      v-model:selectedLines="selectedLines"
    />

    <ProductList :products="filteredProducts" />
  </div>
</template>
