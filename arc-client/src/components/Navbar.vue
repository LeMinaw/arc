<script setup>
  import { UserCircleIcon } from "@heroicons/vue/24/solid"
</script>

<template>
  <div class="flex bg-zinc-700 text-zinc-200 shadow-lg">
    <div>
      <router-link :to="{ name: 'index' }">
        <img src="img/arc.svg" />
      </router-link>
    </div>

    <nav class="flex grow justify-center">
      <router-link :to="{ name: 'index' }"> Accueil </router-link>

      <router-link :to="{ name: 'products' }"> Produits </router-link>

      <router-link :to="{ name: 'about' }"> À propos </router-link>
    </nav>

    <div>
      <UserCircleIcon class="w-10" />
    </div>
  </div>
</template>
