<script setup>
  import { ListboxOption } from "@headlessui/vue"
  import { CheckIcon } from "@heroicons/vue/24/outline"
</script>

<template>
  <ListboxOption
    class="flex h-8 cursor-pointer ui-selected:bg-zinc-300 ui-active:bg-orange-400 ui-disabled:text-zinc-400 ui-disabled:cursor-not-allowed"
  >
    <span class="flex flex-grow items-center px-1.5 whitespace-nowrap">
      <slot />
    </span>

    <span
      class="invisible flex w-8 items-center bg-zinc-400 ui-selected:visible ui-active:bg-orange-500"
    >
      <CheckIcon class="h-5 m-auto" />
    </span>
  </ListboxOption>
</template>
