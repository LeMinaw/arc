<script setup>
  import { HomeIcon, ChevronDoubleRightIcon } from "@heroicons/vue/24/outline"

  defineProps({
    categories: {
      type: Array,
      default: [],
    },
  })
</script>

<template>
  <div class="flex flex-col items-start sm:flex-row">
    <router-link
      :to="{ name: 'products' }"
      class="flex items-center h-8 bg-zinc-800 text-zinc-100"
    >
      <HomeIcon class="p-0.5 w-8" />
      <span class="px-2 py-0.5">Catalogue</span>
    </router-link>

    <div v-for="category of categories" class="flex h-8 items-stretch">
      <ChevronDoubleRightIcon class="p-0.5 w-8 bg-orange-500 text-zinc-100" />

      <router-link
        :to="{ name: 'products', params: { categories: [category.slug] } }"
        class="flex items-center px-2 py-0.5 bg-zinc-800 text-zinc-100"
      >
        {{ category.name }}
      </router-link>
    </div>
  </div>
</template>
