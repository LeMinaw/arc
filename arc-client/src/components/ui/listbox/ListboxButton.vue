<script setup>
  import { ListboxButton } from "@headlessui/vue"
  import { ChevronDownIcon } from "@heroicons/vue/24/outline"
</script>

<template>
  <ListboxButton
    class="inline-flex h-8 bg-zinc-100 border border-zinc-300 ui-open:border-zinc-700"
  >
    <span class="flex items-center px-1.5">
      <slot />
    </span>

    <span
      class="flex w-8 items-center bg-zinc-800 text-zinc-200 ui-open:rotate-180 transition-all"
    >
      <ChevronDownIcon class="h-5 m-auto" />
    </span>
  </ListboxButton>
</template>
