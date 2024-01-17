<script setup>
  import { ListboxOptions } from "@headlessui/vue"
</script>

<template>
  <ListboxOptions
    class="absolute z-10 left-0 bg-zinc-100 border border-zinc-400 shadow-md"
  >
    <slot />
  </ListboxOptions>
</template>
