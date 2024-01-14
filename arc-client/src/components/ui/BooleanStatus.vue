<script setup>
  import { CheckCircleIcon, NoSymbolIcon } from "@heroicons/vue/24/outline"

  defineProps({
    value: {
      type: Boolean,
      default: false,
    },
  })
</script>

<template>
  <span
    v-if="value"
    class="inline-flex items-center p-1 gap-0.5 bg-green-500 text-zinc-950 text-sm"
  >
    <CheckCircleIcon class="inline h-4" />
    Oui
  </span>

  <span
    v-else
    class="inline-flex items-center p-1 gap-0.5 bg-red-600 text-zinc-50 text-sm"
  >
    <NoSymbolIcon class="inline h-4" />
    Non
  </span>
</template>
