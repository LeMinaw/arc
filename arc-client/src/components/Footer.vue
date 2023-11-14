<script setup>
  import { version, name } from "/package.json"
</script>

<template>
  <div class="p-4 bg-zinc-900 text-zinc-200 border-t-8 border-orange-400 shadow-lg">
    <p class="font-mono">{{ name }} v{{ version }}</p>
  </div>
</template>
