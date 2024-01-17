<script setup>
  import { Listbox } from "@headlessui/vue"
</script>

<template>
  <Listbox as="span" class="relative">
    <slot />
  </Listbox>
</template>
