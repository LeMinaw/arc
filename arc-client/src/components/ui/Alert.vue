<script setup>
  import { computed } from "vue"
  import {
    InformationCircleIcon,
    CheckCircleIcon,
    ExclamationCircleIcon,
    ExclamationTriangleIcon,
  } from "@heroicons/vue/24/outline"

  const props = defineProps({
    class: { default: "" },
  })

  const icons = {
    // Root element class name: icon component
    "alert-info": InformationCircleIcon,
    "alert-success": CheckCircleIcon,
    "alert-warning": ExclamationCircleIcon,
    "alert-error": ExclamationTriangleIcon,
  }

  const icon = computed(() => {
    for (const [className, icon] of Object.entries(icons)) {
      if (props.class.includes(className)) return icon
    }
  })
</script>

<template>
  <div :class="'w-fit m-6 p-6 shadow-lg ' + props.class">
    <div class="flex items-center gap-2 text-lg">
      <icon class="w-8" v-if="icon" />

      <slot></slot>
    </div>
  </div>
</template>

<style>
  .alert-error {
    @apply bg-red-500 border border-red-700 shadow-red-700/40 text-zinc-950;
  }
</style>
