<script setup>
  import { ref, watch, watchEffect } from "vue"
  import { useRoute } from "vue-router"

  import Title from "../components/ui/Title.vue"
  import Subtitle from "../components/ui/Subtitle.vue"
  import ProductSpecs from "../components/ProductSpecs.vue"
  import Button from "../components/ui/Button.vue"
  import CategoryBreadcrumb from "../components/CategoryBreadcrumb.vue"

  import { formatRelativeTime } from "../business/time"

  import { fetchProduct } from "../business/arc"

  const route = useRoute()

  const product = ref()
  const kind = ref()
  const line = ref()

  watchEffect(async () => {
    product.value = await fetchProduct(route.params.id)
  })

  watchEffect(async () => {
    if (typeof product.value !== "undefined") {
      kind.value = await fetch(product.value.kind).then(r => r.json())
      line.value = await fetch(product.value.line).then(r => r.json())
    }
  })
</script>

<template>
  <div v-if="product && kind && line">
    <Title>{{ product.name }} - {{ kind.name }} {{ line.manufacturer.name }}</Title>

    <CategoryBreadcrumb :categories="kind.parents" />

    <img
      v-if="line.manufacturer.logo_url"
      class="w-64"
      :src="line.manufacturer.logo_url"
    />

    <img v-if="product.image" class="w-64" :src="product.image" />

    <p v-if="product.reference" class="text-zinc-600">Réf. {{ product.reference }}</p>

    <a
      v-if="product.link"
      :href="product.link"
      target="_blank"
      rel="noopener noreferrer"
    >
      <Button> Voir sur le site de {{ line.manufacturer.name }} </Button>
    </a>

    <p>
      Dans la gamme <a href="">{{ line.name }}</a> de
      <a href="">{{ line.manufacturer.name }}</a>
    </p>

    <p>
      {{ product.stock.length }} en stock, dernière mise à jour
      {{ formatRelativeTime(product.last_mod_date) }}
    </p>

    <Subtitle>Spécifications</Subtitle>

    <ProductSpecs :product="product" :schema="kind.specs_schema" />

    <Subtitle>Produits liés</Subtitle>

    <p>Cette fonctionnalité n'est pas disponible dans cette version d'ARC.</p>
  </div>
</template>
