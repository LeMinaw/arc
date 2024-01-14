<script setup>
  import { UserCircleIcon } from "@heroicons/vue/24/solid"

  const LINKS = {
    index: "Accueil",
    products: "Catalogue",
    check: "Vérifier un article",
    about: "À propos",
  }
</script>

<template>
  <div class="flex bg-zinc-800 text-zinc-200 shadow-lg">
    <div>
      <router-link :to="{ name: 'index' }">
        <img class="h-12" src="/img/arc.svg" />
      </router-link>
    </div>

    <nav class="grow flex justify-center">
      <router-link
        v-for="(title, name) in LINKS"
        :to="{ name }"
        class="px-2 flex flex-col justify-center border-orange-400 hover:border-b-4 transition-all"
      >
        <span>
          {{ title }}
        </span>
      </router-link>
    </nav>

    <a class="w-12 flex flex-col justify-center items-center">
      <UserCircleIcon class="w-10" />
    </a>
  </div>
</template>
