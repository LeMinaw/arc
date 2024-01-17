<script setup>
  import { formatRelativeTime } from "../business/time"

  defineProps({ product: Object })
</script>

<template>
  <router-link
    class="basis-72 flex-grow flex flex-col bg-zinc-200 shadow-lg shadow-zinc-500/30 hover:-translate-y-0.5 transition"
    :to="{ name: 'product', params: { id: product.id } }"
  >
    <div class="flex text-xl font-bold bg-orange-400 text-zinc-900">
      <div class="flex-grow p-2">
        <h4>{{ product.name }}</h4>
      </div>

      <div class="flex flex-col justify-center bg-zinc-900 text-zinc-200">
        <span class="p-2 font-mono"> {{ product.stock.length }}x </span>
      </div>
    </div>

    <div
      class="box flex-grow flex flex-col justify-between border-x border-zinc-400 border-b-8"
    >
      <div class="p-2">
        <p class="">{{ product.line_name }}</p>
        <p v-if="product.reference" class="text-zinc-600">
          Réf. {{ product.reference }}
        </p>
      </div>

      <div>
        <img
          v-if="product.image"
          class="aspect-square object-cover"
          :src="product.image"
        />
        <img v-if="!product.image" class="m-auto w-48" :src="product.logo" />
      </div>

      <div class="p-2">
        <p>
          Dernier ajout {{ formatRelativeTime(product.last_mod_date) }} dans
          <a href="">super machins</a>
        </p>
      </div>
    </div>
  </router-link>
</template>
